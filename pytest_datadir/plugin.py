import os
import shutil

import pytest


class TestDataDir(object):

    def __init__(self, global_dir, module_dir, tmpdir):
        self.global_dir = global_dir
        self.module_dir = module_dir
        self.tmpdir = tmpdir.strpath
        assert os.path.isdir(self.module_dir) or os.path.isdir(self.global_dir),\
            'neither {} or {} are valid data directories'.format(self.global_dir, self.module_dir)

    def __getitem__(self, filename):
        module_srcpath = os.path.join(self.module_dir, filename)
        global_srcpath = os.path.join(self.global_dir, filename)
        temppath = os.path.join(self.tmpdir, filename)
        if os.path.isfile(module_srcpath):
            shutil.copy(module_srcpath, temppath)
        elif os.path.isdir(module_srcpath):
            shutil.copytree(module_srcpath, temppath)
        elif os.path.isfile(global_srcpath):
            shutil.copy(global_srcpath, temppath)
        elif os.path.isdir(global_srcpath):
            shutil.copytree(global_srcpath, temppath)
        return temppath

    def read(self, filename):
        with open(self[filename]) as fp:
            return fp.read()


@pytest.fixture
def datadir(request, tmpdir):
    base_dir = request.fspath.dirname
    module_dir = os.path.join(request.fspath.dirname,
                              os.path.splitext(request.module.__file__)[0])
    global_dir = os.path.join(base_dir, 'data')
    test_data_dir = TestDataDir(global_dir, module_dir, tmpdir)
    return test_data_dir
