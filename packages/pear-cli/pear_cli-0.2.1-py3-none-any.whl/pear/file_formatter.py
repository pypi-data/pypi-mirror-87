from typing import List
from pear.loader import Line


class FileFormatter:

    def apply(self, lines: List[Line]):
        raise NotImplementedError

    def remove(self, line_number: int, lines: List[Line]) -> List[Line]:
        output = lines.copy()
        output.pop(self._position_of_line_with_line_number(line_number, lines.copy()))
        return output

    def insert(self, line_number: int, text: str,
               lines: List[Line]) -> List[Line]:
        output = lines.copy()
        pos = self._determine_position_for_insertion(line_number, lines)
        output.insert(pos, Line(text))
        return output

    def _position_of_line_with_line_number(self, line_number: int,
                                           lines: List[Line]) -> int:
        try:
            return next(i for i, line in enumerate(lines)
                        if line.line_number == line_number)
        except StopIteration:
            raise MissingLineError(line_number, lines)

    def _determine_position_for_insertion(self, line_number: int,
                                          lines: List[Line]) -> int:
        if len(lines) == 0:
            return 0

        for i, line in enumerate(lines):
            if (line.line_number is not None and line_number <= line.line_number):
                return i
        raise Exception


class MissingLineError(Exception):
    def __init__(self, line_number, lines):
        self.line_number = line_number
        self.lines = lines

        super().__init__(f'Could not find line number {line_number} in \n{self.lines}')
