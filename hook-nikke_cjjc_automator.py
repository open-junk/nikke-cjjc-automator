from PyInstaller.utils.hooks import collect_submodules
from distutils.core import setup
from Cython.Build import cythonize
from pathlib import Path
import sys

PACKAGE_NAME = 'src/nikke_cjjc_automator'

extra_compile_args = []
if sys.platform == 'win32':
    extra_compile_args = ['/O2']
else:
    extra_compile_args = ['-O3', '-march=native']

extensions = cythonize(
    [str(p) for p in Path(PACKAGE_NAME).rglob('*.py')],
    compiler_directives={'language_level': "3", 'boundscheck': False, 'wraparound': False, 'cdivision': True, 'initializedcheck': False, 'infer_types': True}
)

for ext in extensions:
    ext.extra_compile_args = extra_compile_args

setup(
    ext_modules=cythonize(extensions),
    script_args=["build_ext", "--inplace"]
)

hiddenimports = collect_submodules(PACKAGE_NAME) + [
    "typer",
    "PIL",
    "PIL.Image",
    "pygetwindow",
    "pyautogui",
    "pyautogui._pyautogui_win",
    "psutil",
    "pywin32",
    "win32gui",
    "win32process",
    "win32con",
    "keyboard",
    "shutil",
    "dynaconf",
    "dynaconf.loaders",
    "questionary",
    "questionary.prompts",
    "questionary.prompts.select",
]