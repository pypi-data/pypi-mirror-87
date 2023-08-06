from pathlib import Path
from typing import List

from dwalk.directories import directories


def test_directories() -> None:
    # Build our own list of expected directories.
    expect_directories: List[Path] = []
    expect_directories.append(Path.home().absolute())
    for path in reversed(Path().absolute().parents):
        expect_directories.append(path.absolute())
    expect_directories.append(Path().absolute())

    # Assert that all the yielded directories are correct.
    actuals = directories()
    for expect in expect_directories:
        assert next(actuals, None) == expect

    # Assert that no more directories are yielded.
    assert next(actuals, None) is None
