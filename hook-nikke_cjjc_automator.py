from PyInstaller.utils.hooks import collect_submodules
from distutils.core import setup
from Cython.Build import cythonize
from pathlib import Path

PACKAGE_NAME = 'src/nikke_cjjc_automator'

setup(
    ext_modules=cythonize([str(p) for p in Path(PACKAGE_NAME).rglob('*.py')], compiler_directives={'language_level': "3"}),
    script_args=["build_ext", "--inplace"]
)

hiddenimports = collect_submodules(PACKAGE_NAME)