import os
import shutil
import sys

if sys.version_info[0] == 2:
    from pathlib2 import Path
else:
    from pathlib import Path

import pytest


@pytest.fixture
def shared_datadir(request, tmpdir):
    original_shared_path = os.path.join(request.fspath.dirname, 'data')
    temp_path = Path(str(tmpdir.join('data')))
    shutil.copytree(original_shared_path, str(temp_path))
    return temp_path


@pytest.fixture
def original_datadir(request):
    return Path(os.path.splitext(request.module.__file__)[0])


@pytest.fixture
def datadir(original_datadir, tmpdir):
    result = Path(str(tmpdir.join(original_datadir.stem)))
    if original_datadir.is_dir():
        shutil.copytree(str(original_datadir), str(result))
    else:
        result.mkdir()
    return result
