import asyncio

from typing import Union

from abc import ABC, ABCMeta, abstractmethod

from auto_compiler.source import Source

Error = tuple[str, str]

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
    def add_file(self, file: Source) -> None:
        """
            Adds a file to the list of file to compile
        """

    @abstractmethod
    async def build_files(self) -> tuple[list[str], list[Error]]:
        """
            Builds all files added and returns the paths to the executables
        """
        ...

    @abstractmethod
    async def build_file(self, file: Source) -> tuple[bool, Union[str, Error]]:
        """
           Builds the file and returns the path to the executable
        """
        ...

    @abstractmethod
    def clean_files(self) -> None:
        """
            Removes executable and eventual extra files generated
            by the build_files method
        """
        ...
