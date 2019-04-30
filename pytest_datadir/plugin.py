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
def original_datadir(request):
    return Path(os.path.splitext(request.module.__file__)[0])

class DatadirFactory(object):
    """Factory class for generating datadir fixtures."""

    # to produce a datadir give it a scope to produce it for and the
    # name of the datadir relative to the request.fspath.dirname
    def mkdatadir(self, scope='function', original_datadir='data'):
        """Generate a datadir fixture with a custom scope and relative path to
        the original datadir that is to be copied to the temporary directory."""

        @pytest.fixture(scope=scope)
        def custom_datadir(request, tmp_path_factory):

            # we want to get a closure of the original_datadir path
            # from the surrounding call to the class method, but since
            # this is a decorated function we can't do it with simple
            # python closure syntax since it is in another lexical context
            nonlocal original_datadir

            # special condition if the datadir is specified as None, which
            # automatically gets the path that matches the basename of the
            # module we are in
            if original_datadir is None:
                original_datadir = Path(os.path.splitext(request.module.__file__)[0])


            # get the path to the shared data dir
            original_path = Path(request.fspath.dirname) / original_datadir

            # make sure that the path exists and it is a directory
            if not original_path.exists():
                raise ValueError("datadir path does not exist")
            elif not original_path.is_dir():
                raise ValueError("datadir path is not a directory")

            # generate a base temporary directory and receive the path to it
            temp_path = tmp_path_factory.mktemp('')

            # in order to use the shutil.copytree util the target directory
            # must not exist so we specify a dir in the generated tempdir for it
            temp_data_path = temp_path / 'data'

            # windows-ify the paths
            original_path = Path(_win32_longpath(original_path))
            temp_data_path = Path(_win32_longpath(str(temp_data_path)))

            # copy all the files in the original data dir to the temp
            # dir
            shutil.copytree(original_path, temp_data_path)

            return temp_data_path

        return custom_datadir

# create a singleton factory
datadir_factory = DatadirFactory()

# generate a fixture for the shared directory for each scope
function_shared_datadir = datadir_factory.mkdatadir(scope='function')
class_shared_datadir = datadir_factory.mkdatadir(scope='class')
module_shared_datadir = datadir_factory.mkdatadir(scope='module')
session_shared_datadir = datadir_factory.mkdatadir(scope='session')

# the original 'shared_datadir' fixture is just an alias for the
# 'function_shared_datadir'
shared_datadir = function_shared_datadir


# the module datadir is just a call to the factory with None as the
# original_datadir
function_datadir = datadir_factory.mkdatadir(scope='function',
                                             original_datadir=None)
class_datadir = datadir_factory.mkdatadir(scope='class',
                                          original_datadir=None)
module_datadir = datadir_factory.mkdatadir(scope='module',
                                           original_datadir=None)
session_datadir = datadir_factory.mkdatadir(scope='session',
                                            original_datadir=None)

# the original 'datadir' fixture is just an alias for the
# 'function_datadir'
datadir = function_datadir
