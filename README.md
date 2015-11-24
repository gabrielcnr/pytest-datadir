# pytest-datadir
pytest plugin for manipulating test data directories and files

# Usage
pytest-datadir will look up for a directory with the name of your module or the global 'data' folder.
Let's say you have a structure like this:
```
.
├── data/
│   └── hello.txt
├── test_hello/
│   └── spam.txt
└── test_hello.py
```
You can access the contents of these files using the dependency injected datadir variable:

```python
def test_read_global(datadir):
    with open(datadir['hello.txt']) as fp:
        contents = fp.read()
    assert contents == 'Hello World!\n'

def test_read_module(datadir):
    with open(datadir['spam.txt']) as fp:
        contents = fp.read()
    assert contents == 'eggs\n'
```

pytest-datadir will copy the original file to a temporary folder, so changing the file contents won't change the original data file.
Happy testing!
