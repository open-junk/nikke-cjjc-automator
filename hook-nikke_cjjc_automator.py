from PyInstaller.utils.hooks import collect_submodules
from distutils.core import setup
from Cython.Build import cythonize
from pathlib import Path
import sys

PACKAGE_NAME = 'src/nikke_cjjc_automator'
py_files = [str(p) for p in Path(PACKAGE_NAME).rglob('*.py') if not p.name.startswith('__init__')]

extra_compile_args = []
if sys.platform == 'win32':
    extra_compile_args = ['/O2']
else:
    extra_compile_args = ['-O3', '-march=native']

extensions = cythonize(
    py_files,
    compiler_directives={
        'language_level': "3",
        'infer_types': True,
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
        'cdivision': True
    }
)

for ext in extensions:
    ext.extra_compile_args = extra_compile_args

setup(
    ext_modules=extensions,
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

excludes = [
    'tests', 
    'docutils', 
    'unittest', 
    'pylint', 
    'pyinstaller',
    'pkg_resources',
]

datas = [
    ('settings.default.toml', '.'),
    ('img/manual.jpg', '.')
]