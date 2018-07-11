import sys
import pytest

@pytest.mark.skipif(sys.version_info[0] == 3, reason='Python 2 only')
def test_correct_pathlib(datadir):
    """
    Dummy test that we are using the correct backport of Python 3's
    standard pathlib in Python 2.
    """
    (datadir / 'foo').mkdir(parents=True, exist_ok=True)
    (datadir / 'foo').mkdir(parents=True, exist_ok=True)
