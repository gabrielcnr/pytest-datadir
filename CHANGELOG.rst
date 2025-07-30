pytest-datadir
==============

1.8.0
-----

*2025-07-30*

- New ``lazy_shared_datadir`` fixture, which brings the same lazy functionality as ``lazy_datadir`` for the *shared* directory.
- Fix ``LazyDataDir.joinpath`` typing to also support ``Path`` objects as the right-hand side parameter.

1.7.2
-----

*2025-06-06*

- ``py.typed`` was added to the distribution, enabling users to use ``LazyDataDir`` in type annotations.

1.7.1
-----

*2025-06-02*

- Fixed bug using ``lazy_datadir`` to copy a file using a sub-directory (e.g, ``lazy_datadir / 'subdir' / 'file.txt'``) (`#99 <https://github.com/gabrielcnr/pytest-datadir/issues/99>`__).

1.7.0
-----

*2025-05-30*

- New `lazy_datadir` fixture that lazily copies files when accessed via `joinpath` or `/` operator.


1.6.1
-----

*2025-02-07*

- pytest 7.0+ is now required.

1.6.0
-----

**Note**: this release has been yanked from PyPI due to `#89 <https://github.com/gabrielcnr/pytest-datadir/issues/89>`__.

*2025-02-07*

- Fixed compatibility with ``pytest-describe``.
- ``original_datadir`` fixture is now ``module``-scoped.

1.5.0 (2023-10-02)
------------------

- Added support for Python 3.11 and 3.12.
- Dropped support for Python 3.7.
- Fix handling of UNC paths on Windows (`#33 <https://github.com/gabrielcnr/pytest-datadir/issues/33>`__).

1.4.1 (2022-10-24)
------------------

- Replace usage of ``tmpdir`` by ``tmp_path`` (`#48 <https://github.com/gabrielcnr/pytest-datadir/pull/48>`__).


1.4.0 (2022-01-18)
------------------

- Fix package so the ``LICENSE`` file is no longer in the root of the package.
- Python 3.9 and 3.10 are now officially supported.
- Python 2.7, 3.4 and 3.5 are no longer supported.

1.3.1 (2019-10-22)
------------------

- Add testing for Python 3.7 and 3.8.
- Add ``python_requires`` to ``setup.py`` so ``pip`` will not try to install ``pytest-datadir`` in incompatible Python versions.


1.3.0 (2019-01-15)
------------------

- Add support for long path names on Windows (`#25 <https://github.com/gabrielcnr/pytest-datadir/pull/25>`__).


1.2.1 (2018-07-12)
------------------

- Fix ``pytest_datadir.version`` attribute to point to the correct version.


1.2.0 (2018-07-11)
------------------

- Use ``pathlib2`` on Python 2.7: this is the proper backport of Python 3's standard
  library.

1.1.0 (2018-07-10)
------------------

- If the data directory does not exist, the fixture will create an empty directory.

1.0.1 (2017-08-15)
------------------

**Fixes**

- Fixed ``shared_datadir`` contents not being copied to a temp location on each test. `#12
  <https://github.com/gabrielcnr/pytest-datadir/issues/12>`_
