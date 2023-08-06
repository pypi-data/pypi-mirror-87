import typer
from typing import List
from pear.loader import FileContainer
from pear.file_formatter import FileFormatter
from pear.replace import Replace
from pear.remove import Remove
from pathlib import Path
import json
import os


class Configuration:
    def __init__(self, config_file_path: Path):
        with open(config_file_path) as f:
            self.input = json.load(f)

    def files(self) -> List[FileContainer]:
        return [self._map_file(f) for f in self.input['files']]

    def _map_file(self, file: dict) -> FileContainer:
        file_container = FileContainer.from_json(
            file, Path(os.getcwd()).joinpath(Path(self.input['out'])))
        typer.echo(f"Found {file['path']}")
        for layer in file['layers']:
            file_container.formatters.append(self._map_layer(layer))
        return file_container

    def _map_layer(self, layer: dict) -> FileFormatter:
        if layer['type'] == 'replace':
            return Replace.from_json(layer)
        elif layer['type'] == 'remove':
            return Remove.from_json(layer)
