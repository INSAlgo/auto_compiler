from auto_compiler.compiler import Compiler
from auto_compiler.source import Source


class IdentityCompiler(Compiler):

    supported_files = [".py", ".js", ".out"]

    def __init__(self) -> None:
        pass

    def build_files(self, files: list[Source]) -> list[str]:
        return [self.build_file(file) for file in files]

    def build_file(self, file: Source) -> str:
        return file.file

    def clean_files(self) -> None:
        pass
