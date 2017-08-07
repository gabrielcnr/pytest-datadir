import os
import pathlib
import shutil

import pytest


@pytest.fixture
def shared_datadir(request):
    return pathlib.Path(request.fspath.dirname) / 'data'


@pytest.fixture
def original_datadir(request):
    return pathlib.Path(os.path.splitext(request.module.__file__)[0])


@pytest.fixture
def datadir(original_datadir, tmpdir):
    result = pathlib.Path(str(tmpdir.join(original_datadir.stem)))
    shutil.copytree(str(original_datadir), str(result))
    return result
