def test_missing_data_dir_starts_empty(datadir):
    assert list(datadir.iterdir()) == []

def test_missing_lazy_data_dir_starts_empty(lazy_datadir):
    assert list(lazy_datadir.iterdir()) == []
