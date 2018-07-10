pytest-datadir
==============


1.1.0 (2018-07-10)
------------------

- If the data directory does not exist, the fixture will create an empty directory.

1.0.1 (2017-08-15)
------------------

**Fixes**

- Fixed ``shared_datadir`` contents not being copied to a temp location on each test. `#12
  <https://github.com/gabrielcnr/pytest-datadir/issues/12>`_
