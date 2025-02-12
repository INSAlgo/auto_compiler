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
        cargo_toml = self.make_cargo_toml(file)
        executable = compile_dir.joinpath(Path(f"release/{file.stem}"))
        process = await create_subprocess_exec(
            "cargo", "build", "--release", "--target-dir", str(compile_dir), stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await process.communicate()
        self.remove_cargo_toml(cargo_toml)
        print(stdout.decode("utf-8"))
        if not process.returncode:
            if executable.exists():
                return executable
            else:
                raise CompilerException("File wasn't created")
        else:
            raise CompilerException(stderr.decode("utf-8"))

    @staticmethod
    def make_cargo_toml(file: Path) -> Path:
        cargo_toml = Path("Cargo.toml")
        cargo_file = f"[package]\nname='{file.stem}'\nversion='1.0.0'\nedition='2018'\n[dependencies]\nrand='0.8.4'\n"
        cargo_file += f"[[bin]]\npath='{file}'\nname='{file.stem}'"
        with open(cargo_toml, "w") as f:
            f.write(cargo_file)
        return Path(cargo_toml)

    @staticmethod
    def remove_cargo_toml(cargo_toml: Path) -> None:
        cargo_toml.unlink()
        cargo_toml.parent.joinpath("Cargo.lock").unlink()

