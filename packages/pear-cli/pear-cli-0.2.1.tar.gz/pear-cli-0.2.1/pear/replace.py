from pear.file_formatter import FileFormatter
from pear.remove import Remove
from typing import List
from pear.loader import Line


class Replace(FileFormatter):
    def __init__(self, replacement_text: List[str], start_line: int, end_line: int):
        self.replacement_text = replacement_text
        self.start_line = start_line
        self.end_line = end_line

    @classmethod
    def from_json(cls, json: dict) -> "Replace":
        return Replace(json['replacement'], json['start'], json['end'])

    def apply(self, lines: List[Line]) -> List[Line]:
        output = Remove(self.start_line, self.end_line).apply(lines)
        for replacement_line in self.replacement_text:
            output = self.insert(self.start_line, replacement_line, output)
        return output

    def __eq__(self, other: 'Replace') -> bool:
        same_text = self.replacement_text == other.replacement_text
        same_start = self.start_line == other.start_line
        same_end = self.end_line == other.end_line

        return all([same_text, same_start, same_end])
