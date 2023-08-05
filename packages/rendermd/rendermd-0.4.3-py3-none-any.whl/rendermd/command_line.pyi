from .command_parser import parse_command_line as parse_command_line
from .printer import Printer as Printer
from .shell import ShellGenerator as ShellGenerator
from .toc import TocGenerator as TocGenerator
from typing import Any, List

GENERATORS: Any

def get_mardown_files(patterns: List[str], recursive: bool) -> List[str]: ...
def rewrite_markdown(file_path: str) -> None: ...
def main() -> None: ...
