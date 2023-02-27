import os.path

from auto_compiler.source import Source
from auto_compiler.compiler import Compiler
from auto_compiler.compilers import *

class AutoCompiler:
    source_folter: str

    def __init__(self, source_folder: str) -> None:
        self.source_folder = source_folder

    def compile_all(self):
        pass

    def compile_file(self, name: str):
        for source in self._get_sources():
            if source.name == name:
                pass

    def _get_sources(self) -> list[Source]:
        res = []
        for root, dirs, files in os.walk(self.source_folder):
            for name in files:
                res.append(os.path.join(root, name))
        return res

    @staticmethod
    def _get_compilers() -> dict[str, Compiler]:
        res = dict()
        for compiler in Compiler.__inheritors__:
            for supported_file in compiler.supported_files:
                res[supported_file] = compiler()
        return res
