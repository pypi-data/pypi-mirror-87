from enum import Enum
from typing import List, NewType

from .core import Diff


class Printer(Enum):
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    RED = FAIL = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    def print(self, msg: str) -> None:
        print(self.value, msg, Printer.RESET.value)

    @classmethod
    def print_colored_diff(cls, diff: Diff) -> None:
        for line in diff:
            if line.startswith("+"):
                cls.GREEN.print(line)
            elif line.startswith("!"):
                cls.WARNING.print(line)
            elif line.startswith("-") and not line.startswith("---"):
                cls.RED.print(line)
            elif line.startswith("^"):
                cls.BLUE.print(line)
            else:
                print(line)
