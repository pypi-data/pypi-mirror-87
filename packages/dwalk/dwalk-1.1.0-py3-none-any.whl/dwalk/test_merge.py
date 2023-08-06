from typing import Any, Dict, Optional

from pytest import mark

from dwalk.merge import merge


@mark.parametrize(
    "a, b, src, expect",
    [
        ({}, {}, None, {}),
        ({"a": "alpha"}, {}, None, {"a": "alpha"}),
        (
            {"a": "alpha"},
            {},
            "foo.yml",
            {"__dwalk__": {"a": {"src": "foo.yml"}}, "a": "alpha"},
        ),
        ({}, {"a": "alpha"}, None, {"a": "alpha"}),
        ({}, {"a": "alpha"}, "foo.yml", {"a": "alpha"}),
        ({"a": "alpha"}, {"a": "alfa"}, None, {"a": "alpha"}),
        ({"a": "alpha"}, {"b": "bravo"}, None, {"a": "alpha", "b": "bravo"}),
        ({"d": {"c": "charlie"}}, {}, None, {"d": {"c": "charlie"}}),
        ({}, {"d": {"c": "charlie"}}, None, {"d": {"c": "charlie"}}),
        (
            {"d": {"c": "charlie"}},
            {"d": {"d": "delta"}},
            None,
            {"d": {"c": "charlie", "d": "delta"}},
        ),
        (
            {"d": {"c": "charlie"}},
            {"d": {"d": "delta"}},
            "foo.txt",
            {
                "d": {
                    "__dwalk__": {"c": {"src": "foo.txt"}},
                    "c": "charlie",
                    "d": "delta",
                }
            },
        ),
    ],
)
def test(
    a: Dict[Any, Any],
    b: Dict[Any, Any],
    src: Optional[str],
    expect: Dict[Any, Any],
) -> None:
    merge(from_dict=a, from_src=src, to_dict=b)
    assert b == expect
