import argparse
from dataclasses import dataclass
from typing import List


@dataclass
class CommandLineOptions:
    patterns: List[str]
    recursive: bool


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rendermd",
        description="""Render markdown templates.

This command recursively search the current directly and find all markdown files
by matching given patterns (default to "**/README.md").

        """,
    )
    parser.add_argument(
        "-p",
        "--pattern",
        dest="patterns",
        default="**/README.md",
        help="Comma separated list of markdown files to populate",
    )
    parser.add_argument(
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Do not search for files recursively",
    )
    return parser


def parse_command_line() -> CommandLineOptions:
    parser = get_parser()
    options = parser.parse_args()
    return CommandLineOptions(
        patterns=options.patterns.split(","), recursive=options.recursive
    )
