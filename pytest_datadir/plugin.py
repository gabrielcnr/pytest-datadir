import os
import shutil
import sys
from copy import copy

if sys.version_info[0] == 2:
    from pathlib2 import Path
else:
    from pathlib import Path

import pytest

# Root temp dir name to use for all pytest-datadir directories
TMPDIR_NAME = "pytest-datadir"

# the datadir factory uses a tmp_path_factory to get a temp dir. This
# is the name of the dir within the tempdir tree to use for datadir,
# since these are potentially session scoped fixtures
DATADIR_DIRNAME = 'datadir'


# for the shared datadirs, to maintain backwards compatibility we set these to
# have the default behavior of using the shared data dir called "data"
SHARED_DATADIR_NAME = 'data'



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

    def mkdatadir(self, original_datadir=None):
        """Create a temporary directory for this factory's scope.


        """

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
        temp_path = self.tmp_path_factory.mktemp(TMPDIR_NAME)

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


# scoped factories

# we must provide a module scoped factory because a session scoped one
# cannot work with the module filename for that is used for module
# named datadirs
@pytest.fixture(scope='module')
def datadir_factory(request, tmp_path_factory):

    return DatadirFactory(request, tmp_path_factory)



@pytest.fixture(scope='module')
def module_datadir(request, datadir_factory):

    return datadir_factory.mkdatadir()

@pytest.fixture(scope='class')
def class_datadir(request, datadir_factory):

    return datadir_factory.mkdatadir()

@pytest.fixture(scope='function')
def function_datadir(request, datadir_factory):

    return datadir_factory.mkdatadir()

# for backwards compatibility
datadir = function_datadir


# shared datadirs, to maintain backwards compatibility we set these to
# have the default behavior of saving the data dir with the name 'data'

@pytest.fixture(scope='module')
def module_shared_datadir(request, datadir_factory):

    return datadir_factory.mkdatadir(original_datadir=SHARED_DATADIR_NAME)

@pytest.fixture(scope='class')
def class_shared_datadir(request, datadir_factory):

    return datadir_factory.mkdatadir(original_datadir=SHARED_DATADIR_NAME)

@pytest.fixture(scope='function')
def function_shared_datadir(request, datadir_factory):

    return datadir_factory.mkdatadir(original_datadir=SHARED_DATADIR_NAME)

# for backwards compatibility
shared_datadir = function_shared_datadir
