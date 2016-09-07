

def test_read_hello_from_submodule(datadir):
    filename = datadir / 'hello.txt'
    with open(str(filename)) as fp:
        contents = fp.read()
    assert contents == 'Hello, world!\n'
