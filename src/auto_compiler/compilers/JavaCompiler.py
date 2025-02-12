import re

from pathlib import Path

from asyncio.subprocess import create_subprocess_exec, PIPE

from ..compiler import Compiler
from ..errors import CompilerException


class JavaCompiler(Compiler):
    # to_build: list[Source]
    supported_files = ['.java']

    def __init__(self) -> None:
        ...

    async def build_file(self, file: Path, compile_dir: Path) -> Path:
        compile_ai_dir = compile_dir / file.stem
        if compile_ai_dir.exists():
            for old_file in compile_ai_dir.glob("*.class"):
                old_file.unlink()
        else:
            compile_ai_dir.mkdir(parents=True)
        process = await create_subprocess_exec(
            "javac", "-d", str(compile_ai_dir), str(file), stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout.decode("utf-8"))
        if not process.returncode:
            class_files = list(compile_ai_dir.glob("*.class"))
            if len(class_files) > 0:
                executable = class_files[0]
                return executable.rename(compile_ai_dir / f"{file.stem}.class")
            else:
                raise CompilerException("File wasn't created")
        else:
            raise CompilerException(stderr.decode("utf-8"))
