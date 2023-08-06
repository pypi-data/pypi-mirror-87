from argparse import ArgumentParser
from json import dumps
from logging import basicConfig, getLogger
from pathlib import Path
from typing import List, Optional

from dwalk import dwalk
from dwalk.version import get_version


class CLI:
    """
    CLI executor.

    Arguments:
        args (List[str]): Optional arguments. Will read from the command line if
                          omitted. Intended for tests.
    """

    def __init__(self, args: Optional[List[str]] = None) -> None:
        self.logger = getLogger()

        self.arg_parser = ArgumentParser(
            "dwalk",
            description="`dwalk` walks directories and merges dictionaries.",
            epilog="Homepage: https://github.com/cariad/dwalk",
        )

        self.arg_parser.add_argument(
            "--version",
            action="store_true",
            help="print the version",
        )
        self.arg_parser.add_argument("--filenames", nargs="+")
        self.arg_parser.add_argument("--directory")
        self.arg_parser.add_argument(
            "--include-meta",
            action="store_true",
            help="include meta data",
        )
        self.arg_parser.add_argument("--log-level", default="INFO")
        self.args = self.arg_parser.parse_args(args)
        self.logger.setLevel(self.args.log_level)

    def execute(self) -> int:
        """
        Executes the discovery.

        Returns:
            int: Shell return code.
        """
        try:

            result = dwalk(
                filenames=self.args.filenames,
                directory=Path(self.args.directory) if self.args.directory else None,
                include_meta=self.args.include_meta,
            )
            print(dumps(result, sort_keys=True, indent=2))
            return 0
        except Exception as e:
            self.logger.exception(e)
            print(f"dwalk failed: {e}")
            return 1

    def invoke(self) -> int:
        """
        Invokes the apppriate task for the given command line arguments.

        Returns:
            int: Shell return code.
        """
        basicConfig()

        if self.args.version:
            return self.print_version()

        if self.args.filenames:
            return self.execute()

        return self.print_help()

    def print_help(self) -> int:
        """
        Prints help.

        Returns:
            int: Shell return code.
        """
        self.arg_parser.print_help()
        return 0

    def print_version(self) -> int:
        """
        Prints the version.

        Returns:
            int: Shell return code.
        """
        print(get_version())
        return 0
