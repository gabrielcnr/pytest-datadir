from pathlib import Path

import pytest


@pytest.fixture(scope="module", params=["fixtures", "fixtures/nested"])
def shared_datadir_name(request: pytest.FixtureRequest) -> str:
    return str(request.param)


@pytest.mark.parametrize("fixture_name", ["shared_datadir", "lazy_shared_datadir"])
def test_custom_shared_directory(
    request: pytest.FixtureRequest,
    tmp_path: Path,
    shared_datadir_name: str,
    fixture_name: str,
) -> None:
    directory = request.getfixturevalue(fixture_name)

    copied_file = directory / "custom.txt"

    assert copied_file == tmp_path / shared_datadir_name / "custom.txt"
    assert copied_file.read_text() == "custom shared data\n"
    copied_file.write_text("modified\n")
    original_file = Path(__file__).parent / shared_datadir_name / "custom.txt"
    assert original_file.read_text() == "custom shared data\n"
