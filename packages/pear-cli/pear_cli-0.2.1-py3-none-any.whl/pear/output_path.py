from pathlib import Path


class OutputPathGenerator:

    def apply(self, path: Path) -> Path:
        raise NotImplementedError
