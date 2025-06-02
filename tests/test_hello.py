import os
from pathlib import Path

import pytest


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


def test_read_hello(datadir):
    assert set(os.listdir(str(datadir))) == {
        "local_directory",
        "hello.txt",
        "over.txt",
        "a" * 250 + ".txt",
    }
    with (datadir / "hello.txt").open() as fp:
        contents = fp.read()
    assert contents == "Hello, world!\n"


def test_change_test_files(datadir, original_datadir, shared_datadir, request):
    filename = datadir / "hello.txt"
    with filename.open("w") as fp:
        fp.write("Modified text!\n")

    original_filename = original_datadir / "hello.txt"
    with original_filename.open() as fp:
        assert fp.read() == "Hello, world!\n"

    with filename.open() as fp:
        assert fp.read() == "Modified text!\n"

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


def test_file_override(shared_datadir, datadir):
    """The same file is in the module dir and global data.
    Shared files are kept in a different temp directory"""
    shared_filepath = shared_datadir / "over.txt"
    private_filepath = datadir / "over.txt"
    assert shared_filepath.is_file()
    assert private_filepath.is_file()
    assert shared_filepath != private_filepath


def test_local_directory(datadir):
    directory = datadir / "local_directory"
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


def test_lazy_copy(lazy_datadir):
    # The temporary directory starts empty.
    assert {x.name for x in lazy_datadir.tmp_path.iterdir()} == set()

    # Lazy copy file.
    hello = lazy_datadir / "hello.txt"
    assert {x.name for x in lazy_datadir.tmp_path.iterdir()} == {"hello.txt"}
    assert hello.read_text() == "Hello, world!\n"

    # Accessing the same file multiple times does not copy the file again.
    hello.write_text("Hello world, hello world.")
    hello = lazy_datadir / "hello.txt"
    assert hello.read_text() == "Hello world, hello world."

    # Lazy copy data directory.
    local_dir = lazy_datadir / "local_directory"
    assert {x.name for x in lazy_datadir.tmp_path.iterdir()} == {
        "hello.txt",
        "local_directory",
    }
    assert local_dir.is_dir() is True
    assert local_dir.joinpath("file.txt").read_text() == "local contents"

    # It is OK to request a file that does not exist in the data directory.
    fn = lazy_datadir / "new-file.txt"
    assert fn.exists() is False
    fn.write_text("new contents")
    assert {x.name for x in lazy_datadir.tmp_path.iterdir()} == {
        "hello.txt",
        "local_directory",
        "new-file.txt",
    }


def test_lazy_copy_sub_directory(lazy_datadir):
    """Copy via file by using a sub-directory (#99)."""
    # The temporary directory starts empty.
    assert {x.name for x in lazy_datadir.tmp_path.iterdir()} == set()

    # Lazy copy file in a sub-directory.
    fn = lazy_datadir / "local_directory/file.txt"
    assert {x.name for x in lazy_datadir.tmp_path.iterdir()} == {
        "local_directory",
    }
    assert fn.read_text() == "local contents"
