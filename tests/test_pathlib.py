from pytest_datadir.plugin import _win32_longpath


def test_win32_longpath_idempotent(datadir):
    """Double application should not prepend twice."""
    first = _win32_longpath(str(datadir))
    second = _win32_longpath(first)
    assert first == second
