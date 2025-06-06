from pathlib import Path


def test_missing_data_dir_starts_empty(datadir: Path) -> None:
    assert list(datadir.iterdir()) == []
