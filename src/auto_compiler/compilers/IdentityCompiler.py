from pathlib import Path

from ..compiler import Compiler


class IdentityCompiler(Compiler):
    supported_files = [".py", ".js", ".out"]

    def __init__(self) -> None:
        ...

    async def build_file(self, file: Path, compile_dir: Path) -> Path:
        return file
