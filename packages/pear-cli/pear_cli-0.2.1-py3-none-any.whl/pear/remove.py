from typing import List
from pear.loader import Line
from pear.file_formatter import FileFormatter


class Remove(FileFormatter):
    def __init__(self, start_line: int, end_line: int):
        self.start_line = start_line
        self.end_line = end_line

    @classmethod
    def from_json(cls, json: dict) -> 'Remove':
        return Remove(json['start'], json['end'])

    def apply(self, lines: List[Line]) -> List[Line]:
        output = lines.copy()
        for i in range(self.start_line, self.end_line + 1):
            output = self.remove(i, output)
        return output
