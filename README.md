# pytest-datadir

pytest plugin for manipulating test data directories and files.

[![Build Status](https://github.com/gabrielcnr/pytest-datadir/workflows/build/badge.svg?branch=master)](https://github.com/gabrielcnr/pytest-datadir/workflows/build/badge.svg?branch=master)
[![PyPI](https://img.shields.io/pypi/v/pytest-datadir.svg)](https://pypi.python.org/pypi/pytest-datadir)
[![CondaForge](https://img.shields.io/conda/vn/conda-forge/pytest-datadir.svg)](https://anaconda.org/conda-forge/pytest-datadir)
![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Usage

`pytest-datadir` automatically looks for a directory matching your module's name or a global `data` folder.

Consider the following directory structure:

```
.
├── data/
│   └── hello.txt
├── test_hello/
│   └── spam.txt
└── test_hello.py
```

You can access file contents using the injected fixtures:

- `datadir` (for module-specific `test_*` folders)
- `shared_datadir` (for the global `data` folder)

```python
def test_read_global(shared_datadir):
    contents = (shared_datadir / "hello.txt").read_text()
    assert contents == "Hello World!\n"


def test_read_module(datadir):
    contents = (datadir / "spam.txt").read_text()
    assert contents == "eggs\n"
```

The contents of the data directory are copied to a temporary folder, ensuring safe file modifications without affecting other tests or original files.

Both `datadir` and `shared_datadir` fixtures return `pathlib.Path` objects.

## lazy_datadir

Version 1.7.0 introduced the `lazy_datadir` fixture, which only copies files and directories when accessed via the `joinpath` method or the `/` operator.

```python
def test_read_module(lazy_datadir):
    contents = (lazy_datadir / "spam.txt").read_text()
    assert contents == "eggs\n"
```

Unlike `datadir`, `lazy_datadir` is an object that only implements `joinpath` and `/` operations. While not fully backward-compatible with `datadir`, most tests can switch to `lazy_datadir` without modifications.

### lazy_shared_datadir

`lazy_shared_datadir` is similar to `lazy_datadir`, but applied to the shared data directory `shared_datadir`.
That is, instead of copying all files in `shared_datadir`, files are only copied as necessary when accessed via `joinpath` or the `/` operator.
This allows for a shared data directory to be pulled from lazily in the same manner as `lazy_datadir`.

```python
def test_read_global(lazy_shared_datadir):
    contents = (lazy_shared_datadir / "hello.txt").read_text()
    assert contents == "Hello World!\n"
```

# License

MIT.
