from __future__ import unicode_literals
import os


def test_read_hello(datadir):
    assert set(os.listdir(str(datadir))) == {'local_directory', 'hello.txt', 'over.txt'}
    with (datadir/'hello.txt').open() as fp:
        contents = fp.read()
    assert contents == 'Hello, world!\n'


def test_change_test_files(datadir, original_datadir, shared_datadir, request):
    filename = datadir / 'hello.txt'
    with filename.open('w') as fp:
        fp.write('Modified text!\n')

    original_filename = original_datadir / 'hello.txt'
    with original_filename.open() as fp:
        assert fp.read() == 'Hello, world!\n'

    with filename.open() as fp:
        assert fp.read() == 'Modified text!\n'

    shared_filename = shared_datadir/'over.txt'
    with shared_filename.open('w') as fp:
        fp.write('changed')
    shared_original = os.path.join(request.fspath.dirname, 'data', 'over.txt')
    with open(shared_original) as fp:
        assert fp.read().strip() == '8000'



def test_read_spam_from_other_dir(shared_datadir):
    filename = shared_datadir / 'spam.txt'
    with filename.open() as fp:
        contents = fp.read()
    assert contents == 'eggs\n'


def test_file_override(shared_datadir, datadir):
    """ The same file is in the module dir and global data.
        Shared files are kept in a different temp directory"""
    shared_filepath = shared_datadir/'over.txt'
    private_filepath = datadir/'over.txt'
    assert shared_filepath.is_file()
    assert private_filepath.is_file()
    assert shared_filepath != private_filepath


def test_local_directory(datadir):
    directory = datadir/'local_directory'
    assert directory.is_dir()
    filename = directory/'file.txt'
    assert filename.is_file()
    with filename.open() as fp:
        contents = fp.read()
    assert contents == 'local contents'


def test_shared_directory(shared_datadir):
    assert shared_datadir.is_dir()
    filename = shared_datadir/'shared_directory'/'file.txt'
    assert filename.is_file()
    with filename.open() as fp:
        contents = fp.read()
    assert contents == 'global contents'

