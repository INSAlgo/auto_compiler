import asyncio

import os.path

from auto_compiler.source import Source
from auto_compiler.compiler import Compiler, Error
from auto_compiler.compilers import *


class AutoCompiler:
    source_folter: str

    def __init__(self, source_folder: str) -> None:
        self.source_folder = source_folder

    async def make_all_executables(self, out_dir: str) -> tuple[list[str], list[Error]]:
        success, errors = await self._compile_all()
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for el in success:
            path = os.path.join(out_dir, os.path.basename(el))
            print(os.path.islink(path))
            if os.path.islink(path):
                os.unlink(path)
            os.symlink(el,
        return success, errors

    async def _compile_all(self) -> tuple[list[str], list[Error]]:
        coros = []
        compilers = self._get_compilers()
        to_build = set()
        for source in self._get_sources():
            compilers[source.type].add_file(source)
            to_build.add(compilers[source.type])
        for compiler in to_build:
            coros.append(compiler.build_files())
        res = await asyncio.gather(*coros)
        success = []
        errors = []
        for el in res:
            success += el[0]
            errors += el[1]
        return success, errors

    async def compile_file(self, name: str) -> str:
        compilers = self._get_compilers()
        for source in self._get_sources():
            if source.name == name and source.type in compilers:
                return await compilers[source.type].build_file(source)

    def _get_sources(self) -> list[Source]:
        res = []
        for root, dirs, files in os.walk(self.source_folder):
            for name in files:
                res.append(Source(os.path.join(root, name)))
        return res

    @staticmethod
    def _get_compilers() -> dict[str, Compiler]:
        res = dict()
        for compiler in Compiler.__inheritors__:
            for supported_file in compiler.supported_files:
                res[supported_file] = compiler()
        return res
