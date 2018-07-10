# pytest-datadir

pytest plugin for manipulating test data directories and files.

[![Build Status](https://travis-ci.org/gabrielcnr/pytest-datadir.svg?branch=master)](https://travis-ci.org/gabrielcnr/pytest-datadir)
[![PyPI](https://img.shields.io/pypi/v/pytest-datadir.svg)](https://pypi.python.org/pypi/pytest-datadir)
[![PythonVersions](https://img.shields.io/pypi/pyversions/pytest-datadir.svg)](https://pypi.python.org/pypi/pytest-datadir)
[![CondaForge](https://img.shields.io/conda/vn/conda-forge/pytest-datadir.svg)](https://anaconda.org/conda-forge/pytest-datadir)


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
    contents = (shared_datadir / 'hello.txt').read_text()
    assert contents == 'Hello World!\n'

def test_read_module(datadir):
    contents = (datadir / 'spam.txt').read_text()
    assert contents == 'eggs\n'
```

pytest-datadir will copy the original file to a temporary folder, so changing the file contents won't change the original data file.

Both `datadir` and `shared_datadir` fixtures are `pathlib.Path` objects.

# Releases

Follow these steps to make a new release:

1. Create a new branch `release-X.Y.Z` from `master`.
2. Update `CHANGELOG.rst`.
3. Open a PR.
4. After it is **green** and **approved**, push a new tag in the format `X.Y.Z`.

Travis will deploy to PyPI automatically.

Afterwards, update the recipe in [conda-forge/pytest-datadir-feedstock](https://github.com/conda-forge/pytest-datadir-feedstock).

# License

MIT.

