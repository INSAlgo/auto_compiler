import os.path

from typing import NamedTuple


class Source(NamedTuple):
    file: str

    @property
    def name(self) -> str:
        return os.path.splitext(os.path.basename(self.file))[0]

    @property
    def type(self) -> str:
        return os.path.splitext(self.file)[1]
