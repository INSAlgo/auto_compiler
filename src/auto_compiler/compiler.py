from pathlib import Path

from abc import ABC, ABCMeta, abstractmethod


class MetaCompiler(ABCMeta):
    __inheritors__ = set()

    def __new__(cls, name, bases, dict):
        subclass = super().__new__(cls, name, bases, dict)
        cls.__inheritors__.update(subclass.mro()[:-3])
        return subclass


class Compiler(ABC, metaclass=MetaCompiler):
    supported_files: list[str]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def build_file(self, file: Path, compile_dir: Path) -> Path:
        """
           Builds the file and returns the path to the executable
        """
        ...
