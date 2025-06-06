import sys
from pathlib import Path

import pytest
from pytest_datadir.plugin import _win32_longpath


def test_win32_longpath_idempotent(datadir: Path) -> None:
    """Double application should not prepend twice."""
    first = _win32_longpath(str(datadir))
    second = _win32_longpath(first)
    assert first == second


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="Only makes sense on Windows"
)
def test_win32_longpath_unc(datadir: Path) -> None:
    unc_path = r"\\ComputerName\SharedFolder\Resource"
    longpath = _win32_longpath(unc_path)
    assert longpath.startswith("\\\\?\\UNC\\")
