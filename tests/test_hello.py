import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from pytest_datadir.plugin import _win32_longpath


@pytest.fixture(autouse=True, scope="module")
def create_long_file_path():
    """
    Create a very long file name to ensure datadir can copy it correctly.

    We don't just create this file in the repository because this makes it
    problematic to clone on Windows without LongPaths enabled in the system.
    """
    d = Path(__file__).with_suffix("")
    old_cwd = os.getcwd()
    try:
        os.chdir(d)
        Path("a" * 250 + ".txt").touch()
    finally:
        os.chdir(old_cwd)


def test_read_hello(datadir, lazy_datadir):
    assert set(os.listdir(str(datadir))) == {
        "local_directory",
        "hello.txt",
        "over.txt",
        "a" * 250 + ".txt",
    }
    with (datadir / "hello.txt").open() as fp:
        contents = fp.read()
    assert contents == "Hello, world!\n"
    with (lazy_datadir / "hello.txt").open() as fp:
        contents = fp.read()
    assert contents == "Hello, world!\n"


def test_change_test_files(datadir, lazy_datadir, original_datadir, shared_datadir, request):
    filename = datadir / "hello.txt"
    with filename.open("w") as fp:
        fp.write("Modified text!\n")
    with filename.open() as fp:
        assert fp.read() == "Modified text!\n"

    lazy_filename = lazy_datadir / "hello.txt"
    with lazy_filename.open("w") as fp:
        fp.write("Modified text again!\n")
    with lazy_filename.open() as fp:
        assert fp.read() == "Modified text again!\n"

    original_filename = original_datadir / "hello.txt"
    with original_filename.open() as fp:
        assert fp.read() == "Hello, world!\n"

    shared_filename = shared_datadir / "over.txt"
    with shared_filename.open("w") as fp:
        fp.write("changed")
    shared_original = os.path.join(request.fspath.dirname, "data", "over.txt")
    with open(shared_original) as fp:
        assert fp.read().strip() == "8000"


def test_read_spam_from_other_dir(shared_datadir):
    filename = shared_datadir / "spam.txt"
    with filename.open() as fp:
        contents = fp.read()
    assert contents == "eggs\n"


def test_file_override(shared_datadir, datadir, lazy_datadir):
    """The same file is in the module dir and global data.
    Shared files are kept in a different temp directory"""
    shared_filepath = shared_datadir / "over.txt"
    private_filepath = datadir / "over.txt"
    lazy_filepath = lazy_datadir / "over.txt"
    assert shared_filepath.is_file()
    assert private_filepath.is_file()
    assert shared_filepath != private_filepath
    assert lazy_filepath.is_file()
    assert shared_filepath != lazy_filepath


def test_local_directory(datadir, lazy_datadir):
    for directory in [datadir / "local_directory", lazy_datadir / "local_directory"]:
        assert directory.is_dir()
        filename = directory / "file.txt"
        assert filename.is_file()
        with filename.open() as fp:
            contents = fp.read()
        assert contents.strip() == "local contents"


def test_shared_directory(shared_datadir):
    assert shared_datadir.is_dir()
    filename = shared_datadir / "shared_directory" / "file.txt"
    assert filename.is_file()
    with filename.open() as fp:
        contents = fp.read()
    assert contents.strip() == "global contents"


@pytest.fixture
def mock_copytree():
    with patch('shutil.copytree') as mock:
        yield mock


@pytest.fixture
def eager_create_datadir(original_datadir, tmp_path):
    result = tmp_path / original_datadir.stem
    print(f"vfg2: Lazy datadir: {result}")
    if not result.is_dir():
        print("vfg2: Creating lazy datadir...")
        if original_datadir.is_dir():
            print("vfg2: Copying original datadir...")
            print(f"vfg2: is this a mock? {shutil.copytree}")
            shutil.copytree(
                _win32_longpath(str(original_datadir)), _win32_longpath(str(result))
            )
        else:
            result.mkdir()


def test_lazy_copy_happens_once(eager_create_datadir, mock_copytree, lazy_datadir):
        # Access the same file multiple times
        for _ in range(3):
            _ = lazy_datadir / "hello.txt"
            
        # Access the same directory multiple times    
        for _ in range(3):
            _ = lazy_datadir / "local_directory"
        
        # copytree only called once by eager_create_datadir, not by lazy_datadir
        assert mock_copytree.call_count == 0
