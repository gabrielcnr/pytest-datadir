import os
import shutil
import sys
from copy import copy

if sys.version_info[0] == 2:
    from pathlib2 import Path
else:
    from pathlib import Path

import pytest

# the datadir factory uses a tmp_path_factory to get a temp dir. This
# is the name of the dir within the tempdir tree to use for datadir,
# since these are potentially session scoped fixtures
DATADIR_DIRNAME = 'datadir'

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
def original_datadir(request):
    return Path(os.path.splitext(request.module.__file__)[0])



class DatadirFactory(object):
    """Factory class for generating datadir fixtures."""

    def __init__(self, request, tmp_path_factory):

        self.tmp_path_factory = tmp_path_factory
        self.request = request

    def mkdatadir(self, original_datadir='data'):

        # special condition if the datadir is specified as None, which
        # automatically gets the path that matches the basename of the
        # module we are in
        if original_datadir is None:
            original_datadir = Path(os.path.splitext(self.request.module.__file__)[0])


        # get the path to the shared data dir
        original_path = Path(self.request.fspath.dirname) / original_datadir

        # make sure that the path exists and it is a directory
        exists = True
        if not original_path.exists():
            # raise the flag that it doesn't exist so we can generate
            # a directory for it instead of copying
            exists = False

        # make sure the path is a directory if it exists
        elif not original_path.is_dir():
            raise ValueError("datadir path is not a directory")

        # generate a base temporary directory and receive the path to it
        temp_path = self.tmp_path_factory.mktemp('')

        # in order to use the shutil.copytree util the target directory
        # must not exist so we specify a dir in the generated tempdir for it
        temp_data_path = temp_path / DATADIR_DIRNAME

        # windows-ify the paths
        original_path = Path(_win32_longpath(original_path))
        temp_data_path = Path(_win32_longpath(str(temp_data_path)))

        # copy or create empty directory depending on whether the
        # original one exists
        if exists:

            # copy all the files in the original data dir to the temp
            # dir
            shutil.copytree(original_path, temp_data_path)

        else:
            # otherwise just give them a fallback tmpdir
            temp_data_path.mkdir()

        return temp_data_path

# to clean up for the different scopes we need tmp_path_factory to be
# scoped differently; just copy the code from module and change the
# decorator

@pytest.fixture(scope="session")
def session_tmp_path_factory(request):
    """Return a :class:`_pytest.tmpdir.TempPathFactory` instance for the test session.
    """
    return request.config._tmp_path_factory

@pytest.fixture(scope="module")
def module_tmp_path_factory(request):
    """Return a :class:`_pytest.tmpdir.TempPathFactory` instance for the test session.
    """
    return request.config._tmp_path_factory


@pytest.fixture(scope="class")
def class_tmp_path_factory(request):
    """Return a :class:`_pytest.tmpdir.TempPathFactory` instance for the test session.
    """
    return request.config._tmp_path_factory

@pytest.fixture(scope="function")
def function_tmp_path_factory(request):
    """Return a :class:`_pytest.tmpdir.TempPathFactory` instance for the test session.
    """
    return request.config._tmp_path_factory

# scoped factories
@pytest.fixture(scope='module')
def module_datadir_factory(request, module_tmp_path_factory):

    return DatadirFactory(request, module_tmp_path_factory)

@pytest.fixture(scope='class')
def class_datadir_factory(request, class_tmp_path_factory):

    return DatadirFactory(request, class_tmp_path_factory)

@pytest.fixture(scope='function')
def function_datadir_factory(request, function_tmp_path_factory):

    return DatadirFactory(request, function_tmp_path_factory)


# shared datadirs

@pytest.fixture(scope='module')
def module_shared_datadir(request, module_datadir_factory):

    return module_datadir_factory.mkdatadir()

@pytest.fixture(scope='class')
def class_shared_datadir(request, class_datadir_factory):

    return class_datadir_factory.mkdatadir()

@pytest.fixture(scope='function')
def function_shared_datadir(request, function_datadir_factory):

    return function_datadir_factory.mkdatadir()

shared_datadir = function_shared_datadir


# test module datadirs

@pytest.fixture(scope='module')
def module_datadir(request, module_datadir_factory):

    return module_datadir_factory.mkdatadir(original_datadir=None)

@pytest.fixture(scope='class')
def class_datadir(request, class_datadir_factory):

    return class_datadir_factory.mkdatadir(original_datadir=None)

@pytest.fixture(scope='function')
def function_datadir(request, function_datadir_factory):

    return function_datadir_factory.mkdatadir(original_datadir=None)

datadir = function_datadir
