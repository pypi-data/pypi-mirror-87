from copy import deepcopy
from typing import Any, Dict, List, Optional


def merge(
    from_dict: Dict[Any, Any],
    from_src: Optional[str],
    to_dict: Dict[Any, Any],
) -> None:
    """
    Merges two dictionaries.

    Args:
        from_dict:     Source dictionary.

        from_filename: Optional path and filename of the `from_dict` dictionary.

                       If set, a `__KEY:dwalk:src__` key will be added as a
                       sibling of every key added or overwritten by this merge.

        to_dict:       Destination dictionary.
    """
    for key in from_dict:
        if key not in to_dict or not isinstance(from_dict[key], dict):
            to_dict[key] = deepcopy(from_dict[key])
            if from_src:
                add_metadata(to_dict=to_dict, key=key, src=from_src)
        else:
            merge(
                from_dict=from_dict[key],
                from_src=from_src,
                to_dict=to_dict[key],
            )


def add_metadata(to_dict: Dict[Any, Any], key: str, src: str) -> None:
    set_key(to_dict=to_dict, path=["__dwalk__", key, "src"], value=src)


def set_key(to_dict: Dict[Any, Any], path: List[str], value: Any) -> None:
    parent = to_dict
    for index, key in enumerate(path):
        if index == len(path) - 1:
            parent[key] = value
        elif key not in parent:
            parent[key] = {}
        parent = parent[key]
