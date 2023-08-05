import re
from typing import Any, ClassVar, Final, List, Tuple, Union

Diff: Any

class MarkdownGenerator:
    block_start: ClassVar[Union[str, re.Pattern]]
    block_end: Final[str] = ...
    def generate_content(self, original_lines: List[str], file_path: str) -> Tuple[str, Diff]: ...
