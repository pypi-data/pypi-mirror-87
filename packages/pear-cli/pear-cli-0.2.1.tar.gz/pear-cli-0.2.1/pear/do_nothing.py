from pathlib import Path
from pear.output_path import OutputPathGenerator


class DoNothing(OutputPathGenerator):
    def apply(self, path: Path) -> Path:
        return path
