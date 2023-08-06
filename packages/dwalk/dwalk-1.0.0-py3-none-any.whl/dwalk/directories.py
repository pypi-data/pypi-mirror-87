from pathlib import Path
from typing import Iterator, Optional


def directories(bottom: Optional[Path] = None) -> Iterator[Path]:
    """
    Yields the directories in which to merge dictionaries, in order of lowest-
    to highest-precedence directory.

    Args:
        bottom: Directory to traverse to from the volume root. Will use the
                current working directory if `None`.

    Yields:
        Path: The next-priority path.
    """
    yield Path.home().absolute()
    resolved_bottom = (bottom or Path()).absolute()
    for path in reversed(resolved_bottom.parents):
        yield path.absolute()
    yield resolved_bottom
