from pathlib import Path

from dwalk import dwalk


def test() -> None:
    test_dir = Path(__file__).parent.parent.joinpath("testing").joinpath("bottom")
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
