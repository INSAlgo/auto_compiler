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
        self.modify_class_name(file)
        executable = compile_dir.joinpath(Path(f"{file.stem}.class"))
        process = await create_subprocess_exec(
            "javac", "-d", str(compile_dir), str(file), stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout.decode("utf-8"))
        if not process.returncode:
            if executable.exists():
                return executable
            else:
                raise CompilerException("File wasn't created")
        else:
            raise CompilerException(stderr.decode("utf-8"))

    @staticmethod
    def modify_class_name(file):
        # Should probably use something more robust than regex
        with open(file, "r") as f:
            filedata = f.read()
        filedata = re.sub(r"(public\s+)?class\s.*\n?{", f"class {file.stem} {'{'}\n", filedata)
        with open(file, "w") as f:
            f.write(filedata)
