import typer
from typing import List
from pathlib import Path
import os
from pear.output_path import OutputPathGenerator
from pear.do_nothing import DoNothing
from pear.collapse import CollapsePath


class Line:

    def __init__(self, text: str, line_number: int = None):
        self.text = text
        self.line_number = line_number

    def __eq__(self, other):
        return self.text == other.text and self.line_number == other.line_number

    def __str__(self):
        return f"{self.line_number}: {self.text}"

    def __repr__(self): return str(self)


class FileContainer:
    def __init__(self,
                 path: Path,
                 output_path: Path,
                 tag: str = None,
                 output_path_generator: OutputPathGenerator = DoNothing()):
        self.formatters = []
        self.path = path
        self.output_path = output_path
        self.tag = tag
        self.output_path_generator = output_path_generator
        with open(self.full_input_path()) as f:
            self.lines = []
            for index, line in enumerate(f.readlines(), start=1):
                self.lines.append(Line(line, index))

    def full_input_path(self):
        return Path(os.getcwd()).joinpath(self.path)

    def apply(self) -> List[Line]:
        lines = self.lines
        for formatter in self.formatters:
            lines = formatter.apply(lines)
        return lines

    def write(self):
        os.makedirs(os.path.dirname(self.final_path()), exist_ok=True)
        typer.echo(f'Writing {self.final_path()}')
        with open(self.final_path(), "w") as f:
            f.writelines([self.include_newline(line.text)
                          for line in self.apply()])

    def include_newline(self, line):
        if line.endswith('\n'):
            return line
        else:
            return f'{line}\n'

    def final_path(self):
        without_tag = self._path_without_tag()
        if self.tag is not None:
            return Path(str(without_tag) + '_' + self.tag)
        else:
            return without_tag

    def _path_without_tag(self) -> Path:
        return self.output_path.joinpath(self.output_path_generator.apply(self.path))

    @classmethod
    def from_json(cls, json: dict, output_path: Path) -> 'FileContainer':
        return FileContainer(Path(json['path']),
                             output_path,
                             tag=cls._get_tag_or_none(json),
                             output_path_generator=cls._get_collapse_or_nothing(json))

    @classmethod
    def _get_collapse_or_nothing(self, json: dict):
        default = DoNothing()
        try:
            collapse_character = json['collapse']
            if collapse_character != '':
                return CollapsePath(collapse_character)
        except KeyError:
            pass
        return default

    @classmethod
    def _get_tag_or_none(cls, json: dict):
        try:
            tag = json['tag']
            if tag == '':
                return None
            else:
                return tag
        except KeyError:
            return None
