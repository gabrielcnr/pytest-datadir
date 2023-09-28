# pytest-datadir

pytest plugin for manipulating test data directories and files.

[![Build Status](https://github.com/gabrielcnr/pytest-datadir/workflows/build/badge.svg?branch=master)](https://github.com/gabrielcnr/pytest-datadir/workflows/build/badge.svg?branch=master)
[![PyPI](https://img.shields.io/pypi/v/pytest-datadir.svg)](https://pypi.python.org/pypi/pytest-datadir)
[![CondaForge](https://img.shields.io/conda/vn/conda-forge/pytest-datadir.svg)](https://anaconda.org/conda-forge/pytest-datadir)
![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


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
You can access the contents of these files using injected variables `datadir` (for *test_* folder) or `shared_datadir`
(for *data* folder):

```python
def test_read_global(shared_datadir):
    contents = (shared_datadir / "hello.txt").read_text()
    assert contents == "Hello World!\n"


def test_read_module(datadir):
    contents = (datadir / "spam.txt").read_text()
    assert contents == "eggs\n"
```

pytest-datadir will copy the original file to a temporary folder, so changing the file contents won't change the original data file.

Both `datadir` and `shared_datadir` fixtures are `pathlib.Path` objects.

# License

MIT.
