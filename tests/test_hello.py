import os


def test_read_hello(datadir):
    assert set(os.listdir(str(datadir))) == {'hello.txt', 'over.txt'}
    with open(str(datadir / 'hello.txt')) as fp:
        contents = fp.read()
    assert contents == 'Hello, world!\n'


def test_modify_hello_does_not_affect_the_original(datadir, original_datadir):
    filename = datadir / 'hello.txt'
    with open(str(filename), 'w') as fp:
        fp.write('Modified text!\n')

    original_filename = original_datadir / 'hello.txt'
    with open(str(original_filename)) as fp:
        assert fp.read() == 'Hello, world!\n'

    with open(str(filename)) as fp:
        assert fp.read() == 'Modified text!\n'


def test_read_spam_from_other_dir(global_datadir):
    filename = global_datadir / 'spam.txt'
    with open(str(filename)) as fp:
        contents = fp.read()
    assert contents == 'eggs\n'

