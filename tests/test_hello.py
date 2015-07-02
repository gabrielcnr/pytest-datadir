import os 


def test_read_hello(datadir):
    filename = datadir['hello.txt']
    with open(filename) as fp:
        contents = fp.read()
    assert contents == 'Hello, world!\n'
    assert contents == datadir.read('hello.txt')


def test_modify_hello_does_not_affect_the_original(datadir):
    filename = datadir['hello.txt']
    with open(filename, 'a') as fp:
        fp.write('\nHello again!')

    original_filename = os.path.join(datadir.data_dir, 'hello.txt')
    with open(original_filename) as fp:
        original_contents = fp.read()

    assert original_contents == 'Hello, world!\n'

    with open(filename) as fp:
        modified_contents = fp.read()

    assert modified_contents == 'Hello, world!\n\nHello again!'


