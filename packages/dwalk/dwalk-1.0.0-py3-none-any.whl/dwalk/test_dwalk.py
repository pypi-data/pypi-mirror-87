from pathlib import Path
from typing import List

from pytest import mark

from dwalk import dwalk

project_dir = Path(__file__).parent.parent
testing_dir = project_dir.joinpath("testing")
bottom_dir = testing_dir.joinpath("bottom")


def test() -> None:
    test_dir = project_dir.joinpath("testing").joinpath("bottom")
    actual = dwalk(filenames=["dwalk.2.yml", "dwalk.1.yml"], directory=test_dir)
    assert actual == {
        "alphabet": {"a": "alpha", "b": "bravo", "c": "charlie", "d": "delta"},
        "favourite_colour": "purple",
        "is_bottom_1": True,
        "is_bottom_2": True,
        "is_top_1": True,
        "is_top_2": True,
        "shopping_list": ["atari", "bismuth", "cookies"],
        "side_count": {"hexagon": 6, "pentagon": 5, "square": 4, "triangle": 3},
    }


@mark.parametrize(
    "directory, filenames, expect",
    [
        (
            bottom_dir,
            ["dwalk.2.yml", "dwalk.1.yml"],
            bottom_dir.joinpath("dwalk.1.yml"),
        ),
        (bottom_dir, ["dwalk.3.yml"], testing_dir.joinpath("dwalk.3.yml")),
    ],
)
def test_most_specific_src(directory: Path, filenames: List[str], expect: Path) -> None:
    actual = dwalk(directory=directory, filenames=filenames, include_meta=True)
    assert actual["__dwalk__"]["__dwalk__"]["most_specific_src"] == str(expect)
