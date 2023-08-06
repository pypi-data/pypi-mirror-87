from pathlib import Path
from pear.output_path import OutputPathGenerator

import os


class CollapsePath(OutputPathGenerator):
    def __init__(self, replace_character: str):
        self.replace_character = replace_character

    def apply(self, path) -> Path:
        return Path(self.replace_character.join(self._parts(path)))

    def _do_collapse(self, path: Path):
        return Path(self._parts(str(path)))

    def _parts(self, path: str) -> [str]:
        if path == '':
            return []
        else:
            split = os.path.split(path)
            return self._parts(split[0]) + [split[1]]

    def __eq__(self, o):
        return self.replace_character == o.replace_character
