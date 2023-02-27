import asyncio

from auto_compiler.compiler import Compiler
from auto_compiler.source import Source


class IdentityCompiler(Compiler):
    to_build: list[Source]
    supported_files = [".py", ".js", ".out"]

    def __init__(self) -> None:
        self.to_build = list()

    def add_file(self, file: Source) -> None:
        self.to_build.append(file)

    async def build_files(self) -> list[str]:
        return [await self.build_file(file) for file in self.to_build]

    async def build_file(self, file: Source) -> str:
        return file.file

    def clean_files(self) -> None:
        pass
