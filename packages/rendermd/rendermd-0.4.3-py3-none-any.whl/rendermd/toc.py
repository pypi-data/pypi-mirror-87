import difflib
from typing import List, Tuple

import md_toc

from .core import Diff, MarkdownGenerator


class TocGenerator(MarkdownGenerator):
    block_start = "[//]: # (start:toc)"

    def generate_content(
        self, original_lines: List[str], file_path: str
    ) -> Tuple[str, Diff]:
        """Given a markdown file, generate table of contents.

        Returns:
            (content, diff)
        """
        resulted_lines = []

        inside_toc_block = False
        contains_toc = False

        for line in original_lines:

            if line.startswith(self.block_start):
                inside_toc_block = True
                contains_toc = True

                resulted_lines += [line] + self.get_toc(file_path).splitlines() + [""]
            elif inside_toc_block and line.startswith(self.block_end):
                resulted_lines.append(self.block_end)
                inside_toc_block = False
                continue

            if not inside_toc_block:
                resulted_lines.append(line)

        return (
            "\n".join(resulted_lines),
            contains_toc
            and Diff(list(difflib.context_diff(original_lines, resulted_lines)))
            or Diff([]),
        )

    def get_toc(self, file_path: str) -> str:
        table_of_contents = md_toc.build_toc(file_path, parser="redcarpet")
        return "\n".join(
            [
                "Table of Contents",
                "=================",
                table_of_contents,
            ]
        )
