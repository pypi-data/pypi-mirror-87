import glob
from typing import List

from .command_parser import parse_command_line
from .printer import Printer
from .shell import ShellGenerator
from .toc import TocGenerator

GENERATORS = [TocGenerator(), ShellGenerator()]


def get_mardown_files(patterns: List[str], recursive: bool) -> List[str]:
    files = []
    for pattern in patterns:
        files += glob.glob(pattern, recursive=bool(recursive))

    return files


def rewrite_markdown(file_path: str) -> None:
    with open(file_path) as infile:
        file_content = infile.read()

    for gen in GENERATORS:
        lines = [line for line in file_content.splitlines()]

        file_content, diff = gen.generate_content(lines, file_path)

        if diff:
            print(f"{gen.__class__.__name__} working on {file_path} ...")
            Printer.print_colored_diff(diff)

    with open(file_path, "w") as outfile:
        print(file_content, file=outfile)


def main() -> None:
    opts = parse_command_line()
    for markdown_file in get_mardown_files(opts.patterns, opts.recursive):
        rewrite_markdown(markdown_file)

    print("rendermd is done!")


if __name__ == "__main__":
    main()
