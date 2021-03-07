import sys
from cx_Freeze import setup, Executable

buildOptions = dict(include_files = ['src/config.json'])

setup(  name = "ModSync",
        version = "0.1",
        description = "ModSync for Valheim",
        options = dict(build_exe = buildOptions),
        executables = [Executable("src/modsync.py")])