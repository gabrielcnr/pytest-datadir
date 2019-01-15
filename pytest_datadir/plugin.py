import os
import shutil
import sys

if sys.version_info[0] == 2:
    from pathlib2 import Path
else:
    from pathlib import Path

import pytest


def _win32_longpath(path):
    '''
    Helper function to add the long path prefix for Windows, so that shutil.copytree won't fail
    while working with paths with 255+ chars.
    '''
    if sys.platform == 'win32':
        # The use of os.path.normpath here is necessary since "the "\\?\" prefix to a path string
        # tells the Windows APIs to disable all string parsing and to send the string that follows
        # it straight to the file system".
        # (See https://docs.microsoft.com/pt-br/windows/desktop/FileIO/naming-a-file)
        return '\\\\?\\' + os.path.normpath(path)
    else:
        return path


@pytest.fixture
def shared_datadir(request, tmpdir):
    original_shared_path = os.path.join(request.fspath.dirname, 'data')
    temp_path = Path(str(tmpdir.join('data')))
    shutil.copytree(_win32_longpath(original_shared_path), _win32_longpath(str(temp_path)))
    return temp_path


@pytest.fixture
def original_datadir(request):
    return Path(os.path.splitext(request.module.__file__)[0])


@pytest.fixture
def datadir(original_datadir, tmpdir):
    result = Path(str(tmpdir.join(original_datadir.stem)))
    if original_datadir.is_dir():
        shutil.copytree(_win32_longpath(str(original_datadir)), _win32_longpath(str(result)))
    else:
        result.mkdir()
    return result
