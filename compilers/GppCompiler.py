import os
import asyncio

from auto_compiler.compiler import Compiler
from auto_compiler.source import Source


class GppCompiler(Compiler):
    to_build: list[Source]
    supported_files = ['.cpp', '.cc', '.C']

    def __init__(self) -> None:
        self.to_build = list()

    def add_file(self, file: Source) -> None:
        self.to_build.append(file)

    async def build_files(self) -> list[str]:
        builders = [self.build_file(file) for file in self.to_build]
        res = await asyncio.gather(*builders)
        return [el[1] for el in res if el[0]], [el[1] for el in res if not el[0]]

    async def build_file(self, file: Source) -> str:
        if not os.path.exists("out/"):
            os.makedirs("out/")
        executable = f"out/{file.name}.out"
        process = await asyncio.subprocess.create_subprocess_exec(
            "g++", "-o", executable, file.file
        )
        code = await process.wait()
        if not code:
            return True, executable
        else :
            return False, (file.file, "Compiler error")

    def clean_files(self) -> None:
        pass
