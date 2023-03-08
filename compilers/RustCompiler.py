import re

from pathlib import Path

from asyncio.subprocess import create_subprocess_exec, PIPE

from ..compiler import Compiler
from ..errors import CompilerException


class RustCompiler(Compiler):
    supported_files = ['.rs']

    def __init__(self) -> None:
        ...

    async def build_file(self, file: Path, compile_dir: Path) -> Path:
        self.make_cargo_toml(file)
        executable = compile_dir.joinpath(Path(f"release/{file.stem}"))
        process = await create_subprocess_exec(
            "cargo", "build", "--release", "--target-dir", str(compile_dir), stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await process.communicate()
        print(stdout.decode("utf-8"))
        if not process.returncode:
            if executable.exists():
                return executable
            else:
                raise CompilerException("File {file} wasn't created")
        else:
            raise CompilerException(stderr.decode("utf-8"))

    @staticmethod
    def make_cargo_toml(file: Path):
        cargo_file = f"[package]\nname='{file.stem}'\nversion='1.0.0'\nedition='2018'\n[dependencies]\nrand='0.8.4'\n"
        cargo_file += f"[[bin]]\npath='{file}'\nname='{file.stem}'"
        with open("Cargo.toml", "w") as f:
            f.write(cargo_file)
