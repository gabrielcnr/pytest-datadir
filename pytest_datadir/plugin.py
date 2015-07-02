import os
import shutil

import pytest


class TestDataDir(object):

    def __init__(self, data_dir, tmpdir):
        self.data_dir = data_dir
        self.tmpdir = tmpdir.strpath

    def __getitem__(self, filename):
        srcpath = os.path.join(self.data_dir, filename)
        temppath = os.path.join(self.tmpdir, filename) 
        if os.path.isfile(srcpath):
            shutil.copy(srcpath, temppath)
        return temppath

    def read(self, filename):
        with open(self[filename]) as fp:
            return fp.read()


@pytest.fixture
def datadir(request, tmpdir):
    data_dir = os.path.join(request.fspath.dirname,
                            request.module.__name__)
    assert os.path.isdir(data_dir), 'invalid data dir: {}'.format(data_dir)
    test_data_dir = TestDataDir(data_dir, tmpdir)
    return test_data_dir


