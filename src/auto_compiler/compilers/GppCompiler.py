from pathlib import Path

from asyncio.subprocess import create_subprocess_exec, PIPE

from ..compiler import Compiler
from ..errors import CompilerException


class GppCompiler(Compiler):
    supported_files = ['.cpp', '.cc', '.C']

    def __init__(self) -> None:
        ...

    async def build_file(self, file: Path, compile_dir: Path) -> Path:
        executable = compile_dir.joinpath(Path(f"{file.stem}.out"))
        process = await create_subprocess_exec(
            "g++", "-o", str(executable), str(file), stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await process.communicate()
        if not process.returncode:
            if executable.exists():
                return executable
            else:
                raise CompilerException("File wasn't created")
        else:
            raise CompilerException(stderr.decode("utf-8"))
    # def clean_files(self) -> None:
    #     pass
