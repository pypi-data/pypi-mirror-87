import argparse
from typing import Any, List

class CommandLineOptions:
    patterns: List[str]
    recursive: bool
    def __init__(self, patterns: Any, recursive: Any) -> None: ...

def get_parser() -> argparse.ArgumentParser: ...
def parse_command_line() -> CommandLineOptions: ...
