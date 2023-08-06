from pathlib import Path

from mock import ANY, Mock, patch
from ruamel.yaml import YAML

from dwalk.cli import CLI


def test_args() -> None:
    assert not CLI().args.include_meta
    assert not CLI().args.version


def test_args__version() -> None:
    assert CLI(["--version"]).args.version


@patch("dwalk.cli.CLI.print_version", return_value=0)
def test_invoke__version(print_version: Mock) -> None:
    assert CLI(["--version"]).invoke() == 0
    print_version.assert_called_with()


def test_print_help() -> None:
    assert CLI().print_help() == 0


def test_print_version() -> None:
    assert CLI().print_version() == 0


@patch("dwalk.cli.YAML.dump")
def test_execute(dump: Mock) -> None:
    testing = Path(__file__).parent.parent.joinpath("testing").absolute()
    bottom = testing.joinpath("bottom")
    cli = CLI(
        [
            "--directory",
            str(bottom),
            "--filenames",
            "dwalk.3.yml",
            "dwalk.2.yml",
            "dwalk.1.yml",
        ],
    )
    assert cli.invoke() == 0

    with open(testing.joinpath("expect.yml"), "r") as stream:
        expect = YAML(typ="safe").load(stream)

    dump.assert_called_with(expect, ANY)
