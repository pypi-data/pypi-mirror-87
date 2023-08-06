from logging import getLogger
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ruamel.yaml import YAML

from dwalk.directories import directories
from dwalk.merge import merge, set_key


def dwalk(
    filenames: List[str],
    directory: Optional[Union[Path, str]] = None,
    include_meta: bool = False,
) -> Dict[Any, Any]:
    """
    Discovers and merges dictionaries.

    Args:
        directory:    Directory to walk to. Default is the working directory.

        filenames:    Files to merge if found in each directory.

                      Order is important. The content of files at the end of the
                      list take precedence over files at the beginning.

                      For example a merge between ["2.yml", "1.yml"] would
                      prioritise values in "1.yml" over "2.yml".

        include_meta: If `True`, keys named `__dwalk__` will be added to
                      describe the metadata of each value. Default is `False`.

    Returns:
        Merged dictionary.
    """

    logger = getLogger("dwalk")
    logger.debug("Starting discovery.")
    logger.debug("Directory: %s", directory)

    result: Dict[Any, Any] = {}

    if isinstance(directory, str):
        directory = Path(directory).resolve()

    most_specific: Optional[Path] = None

    for d in directories(bottom=directory):
        logger.debug("Examining directory: %s", d)

        for filename in filenames:
            path = d.joinpath(filename)

            try:
                with open(path, "r") as stream:
                    logger.debug("Reading and merging: %s", path)
                    merge(
                        from_dict=YAML(typ="safe").load(stream),
                        from_src=str(path) if include_meta else None,
                        to_dict=result,
                    )
                    if include_meta:
                        most_specific = path
            except FileNotFoundError:
                logger.debug("File does not exist: %s", path)
                pass
            except Exception as ex:
                logger.error("Failed to read file: %s (%s)", path, ex)

    if include_meta:
        set_key(
            to_dict=result,
            path=["__dwalk__", "__dwalk__", "most_specific_src"],
            value=str(most_specific),
        )

    return result
