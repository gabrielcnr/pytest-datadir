pytest-datadir
==============

1.4.0 (2019-04-30)
------------------

- Implements the ``DatadirFactory`` class which exposes the ``mkdatadir`` method that generates datadir fixtures based on the parameters of a scope and the relative path of the datadir which is intended to be copied to the temporary data directory. This allows for datadirs for different scopes other than function. (`#26 <https://github.com/gabrielcnr/pytest-datadir/issues/26>`_).

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
