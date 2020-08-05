import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=["source", "pyglet", "pymunk"], excludes=[])

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, targetName='Arkius')
]

setup(
    name='Arkius',
    version='jank-rewrite-dev',
    description='Arkius, top-down roguelite.',
    options=dict(build_exe=buildOptions),
    executables=executables
)
