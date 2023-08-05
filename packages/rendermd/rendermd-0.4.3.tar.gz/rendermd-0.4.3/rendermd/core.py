import re
from typing import ClassVar, Final, List, NewType, Tuple, Union

Diff = NewType("Diff", List[str])


class MarkdownGenerator:
    block_start: ClassVar[Union[str, re.Pattern]]
    block_end: Final = "[//]: # (end)"

    def generate_content(
        self, original_lines: List[str], file_path: str
    ) -> Tuple[str, Diff]:
        raise NotImplementedError()
