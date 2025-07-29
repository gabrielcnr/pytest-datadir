import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import pytest


def _win32_longpath(path: str) -> str:
    """
    Helper function to add the long path prefix for Windows, so that shutil.copytree
     won't fail while working with paths with 255+ chars.
    """
    if sys.platform == "win32":
        # The use of os.path.normpath here is necessary since "the "\\?\" prefix
        # to a path string tells the Windows APIs to disable all string parsing
        # and to send the string that follows it straight to the file system".
        # (See https://docs.microsoft.com/pt-br/windows/desktop/FileIO/naming-a-file)
        normalized = os.path.normpath(path)
        if not normalized.startswith("\\\\?\\"):
            is_unc = normalized.startswith("\\\\")
            # see https://en.wikipedia.org/wiki/Path_(computing)#Universal_Naming_Convention # noqa: E501
            if (
                is_unc
            ):  # then we need to insert an additional "UNC\" to the longpath prefix
                normalized = normalized.replace("\\\\", "\\\\?\\UNC\\")
            else:
                normalized = "\\\\?\\" + normalized
        return normalized
    else:
        return path


@pytest.fixture
def shared_datadir(request: pytest.FixtureRequest, tmp_path: Path) -> Path:
    original_shared_path = os.path.join(request.fspath.dirname, "data")
    temp_path = tmp_path / "data"
    shutil.copytree(
        _win32_longpath(original_shared_path), _win32_longpath(str(temp_path))
    )
    return temp_path


@pytest.fixture(scope="module")
def original_datadir(request: pytest.FixtureRequest) -> Path:
    return Path(request.path).with_suffix("")


@pytest.fixture
def datadir(original_datadir: Path, tmp_path: Path) -> Path:
    result = tmp_path / original_datadir.stem
    if original_datadir.is_dir():
        shutil.copytree(
            _win32_longpath(str(original_datadir)), _win32_longpath(str(result))
        )
    else:
        result.mkdir()
    return result


@dataclass(frozen=True)
class LazyDataDir:
    """
    A dataclass to represent a lazy data directory.

    Unlike the datadir fixture, this class copies files and directories to the
    temporary directory when requested via the `joinpath` method or the `/` operator.
    """

    original_datadir: Path
    tmp_path: Path

    def joinpath(self, other: Union[Path, str]) -> Path:
        """
        Return `other` joined with the temporary directory.

        If `other` exists in the data directory, the corresponding file or directory is
        copied to the temporary directory before being returned.

        Note that the file or directory is only copied once per test. Subsequent calls
        with the same argument within the same test will not trigger another copy.
        """
        original = self.original_datadir / other
        target = self.tmp_path / other
        if original.exists() and not target.exists():
            if original.is_file():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(
                    _win32_longpath(str(original)), _win32_longpath(str(target))
                )
            elif original.is_dir():
                shutil.copytree(
                    _win32_longpath(str(original)), _win32_longpath(str(target))
                )
        return target

    def __truediv__(self, other: Union[Path, str]) -> Path:
        return self.joinpath(other)


@pytest.fixture
def lazy_datadir(original_datadir: Path, tmp_path: Path) -> LazyDataDir:
    """
    Return a lazy data directory.

    Here, "lazy" means that the temporary directory is initially created empty.

    Files and directories are then copied from the data directory only when first
    accessed via the ``joinpath`` method or the ``/`` operator.

    Args:
        original_datadir: The original data directory.
        tmp_path: Pytest's built-in fixture providing a temporary directory path.
    """
    return LazyDataDir(original_datadir, tmp_path)


@pytest.fixture
def lazy_shared_datadir(request: pytest.FixtureRequest, tmp_path: Path) -> LazyDataDir:
    """
    Return a lazy version of the shared data directory.

    Here, "lazy" means that the temporary directory is initially created empty.

    Files and directories are then copied from the data directory only when first
    accessed via the ``joinpath`` method or the ``/`` operator.

    Args:
        request: The Pytest fixture request object.
        tmp_path: Pytest's built-in fixture providing a temporary directory path.
    """
    original_shared_path = Path(os.path.join(request.fspath.dirname, "data"))
    temp_path = tmp_path / "data"
    temp_path.mkdir(parents=True, exist_ok=False)

    return LazyDataDir(original_shared_path, temp_path)
