import os
import os.path as osp
import pytest


def test_shared_module_write(module_datadir):

    write_path = osp.join(module_datadir, 'module_target.txt')
    with open(write_path, 'x') as wf:
        wf.write("hello")

def test_shared_module_read(module_datadir):

    target_path = osp.join(module_datadir, 'module_target.txt')

    assert osp.exists(target_path)

def test_shared_function_write(function_datadir):

    # write and see if we see it in the module and class scopes
    write_path = osp.join(function_datadir, 'function_target.txt')
    with open(write_path, 'x') as wf:
        wf.write("hello")

def test_shared_function_read(function_datadir):

    target_path = osp.join(function_datadir, 'function_target.txt')

    assert not osp.exists(target_path)

def test_shared_module_from_function_read(module_datadir):

    target_path = osp.join(module_datadir, 'module_target.txt')

    assert osp.exists(target_path)


class TestSharedClass():

    def test_shared_class_write(self, class_datadir):

        # write and see if we see it in the module and class scopes
        write_path = osp.join(class_datadir, 'class_target.txt')
        with open(write_path, 'x') as wf:
            wf.write("hello")

    def test_shared_class_read(self, class_datadir):

        target_path = osp.join(class_datadir, 'class_target.txt')

        assert osp.exists(target_path)

    def test_shared_module_from_class_read(self, module_datadir):

        target_path = osp.join(module_datadir, 'module_target.txt')

        assert osp.exists(target_path)


class TestDatadirScopeConflict():

    def test_write_hello(self, class_datadir):

        write_path = osp.join(class_datadir, 'target.txt')
        with open(write_path, 'x') as wf:
            wf.write("hello")

    def test_hello_exist(self, class_datadir):

        write_path = osp.join(class_datadir, 'target.txt')

        assert osp.exists(write_path)

    @pytest.mark.xfail
    def test_overwrite_hello(self, class_datadir):

        write_path = osp.join(class_datadir, 'target.txt')
        with open(write_path, 'x') as wf:
            wf.write("hello")
