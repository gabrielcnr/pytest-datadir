import os
import shutil
import sys

import pytest


def _win32_longpath(path):
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
def shared_datadir(request, tmp_path):
    original_shared_path = os.path.join(request.fspath.dirname, "data")
    temp_path = tmp_path / "data"
    shutil.copytree(
        _win32_longpath(original_shared_path), _win32_longpath(str(temp_path))
    )
    return temp_path


@pytest.fixture(scope="module")
def original_datadir(request):
    return request.path.parent / request.path.stem


@pytest.fixture
def datadir(original_datadir, tmp_path):
    result = tmp_path / original_datadir.stem
    if original_datadir.is_dir():
        shutil.copytree(
            _win32_longpath(str(original_datadir)), _win32_longpath(str(result))
        )
    else:
        result.mkdir()
    return result
