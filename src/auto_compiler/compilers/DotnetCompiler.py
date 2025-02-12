import re

from pathlib import Path

from asyncio.subprocess import create_subprocess_exec, PIPE

from ..compiler import Compiler
from ..errors import CompilerException


class DotNetCompiler(Compiler):
    supported_files = ['.cs']

    def __init__(self) -> None:
        ...

    async def build_file(self, file: Path, compile_dir: Path) -> Path:
        temp, csproj = self.make_temp_dir(file)
        executable = compile_dir.joinpath(Path(file.stem))
        process = await create_subprocess_exec(
            "dotnet", "publish", "-o", str(compile_dir), str(csproj), stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = await process.communicate()
        self.delete_folder(temp)
        print(stdout.decode("utf-8"))
        if not process.returncode:
            if executable.exists():
                return executable
            else:
                raise CompilerException("File wasn't created")
        else:
            raise CompilerException(stderr.decode("utf-8"))

    @staticmethod
    def make_temp_dir(file: Path) -> tuple[Path, Path]:
        tmp = Path(file.stem)
        tmp.mkdir(exist_ok=True)
        link = tmp.joinpath(file.name)
        try:
            link.symlink_to(file.absolute())
        except FileExistsError:
            pass
        csproj = tmp.joinpath(file.stem+".csproj")
        csproj_content = \
            '<Project Sdk="Microsoft.NET.Sdk">\n<PropertyGroup>\n<OutputType>Exe</OutputType>\n' \
            '<TargetFramework>net9.0</TargetFramework>\n<RootNamespace>test_cs</RootNamespace>\n' \
            '<ImplicitUsings>enable</ImplicitUsings>\n<Nullable>enable</Nullable>\n</PropertyGroup>\n</Project>'

        with open(csproj, "w") as f:
            f.write(csproj_content)
        return tmp, csproj

    def delete_folder(self, pth):
        for sub in pth.iterdir():
            if sub.is_dir():
                self.delete_folder(sub)
            else:
                sub.unlink()
        pth.rmdir()

