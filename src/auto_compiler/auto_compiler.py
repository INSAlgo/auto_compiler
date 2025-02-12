import asyncio

from pathlib import Path

from .compiler import Compiler
from .compilers import *
from .errors import CompilerException

class AutoCompiler:
    source_folter: str

    def __init__(
        self,
        source_folder: Path,
        compile_folder: Path = Path("out"),
        result_folder: Path = Path("ais")
    ) -> None:

        self.source_folder = source_folder
        self.compile_folder = compile_folder
        self.result_folder = result_folder

    async def compile_user(self, name: str) -> Path:
        for source in self._get_sources():
            if source.stem == name:
                return await self.compile_file(source)
        raise CompilerException(f"Cannot find the source code for user {name} in {self.source_folder}")

    async def compile_file(self, name: Path) -> Path:
        compilers = self._get_compilers()

        if not name.exists():
            raise CompilerException("File {name} does not exists")

        self.compile_folder.mkdir(parents=True, exist_ok=True)

        try:
            executable = await compilers[name.suffix].build_file(name, self.compile_folder)
        except KeyError:
            raise CompilerException(f"There is no compiler for {name.name}: \
                extension {name.suffix} is not supported")

        symlink = self.result_folder.joinpath(executable.name)
        self.result_folder.mkdir(parents=True, exist_ok=True)

        if symlink.exists():
            symlink.unlink()
        symlink.symlink_to(Path.cwd().joinpath(executable))

        return symlink

    def _get_sources(self) -> list[Path]:
        return [child for child in self.source_folder.iterdir() if child.is_file()]

    @staticmethod
    def _get_compilers() -> dict[str, Compiler]:
        res = dict()
        for compiler in Compiler.__inheritors__:
            for supported_file in compiler.supported_files:
                res[supported_file] = compiler()
        return res