

def test_missing_data_dir_starts_empty(datadir):
    assert list(datadir.iterdir()) == []
