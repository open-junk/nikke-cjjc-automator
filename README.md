# NIKKE CJJC Automator

> **Special Thanks:** This project is based on [entishl/nikke-CArena-Helper](https://github.com/entishl/nikke-CArena-Helper).

This project is an automation script for the PC game *NIKKE: Goddess of Victory*, helping players efficiently capture, log, and review data in modes like Champion Arena.

![manual](img/manual.jpg)

## Features

- Modern Python package architecture, MVC layered design, type hints
- Centralized configuration in `settings.default.toml`, auto-management and version check, supports delay parameters
- Interactive CLI (Typer + Questionary), auto menu if no arguments
- Multi-mode automation (strategy pattern), highly modular main flow
- Image caching and auto-merging, supports custom output directory
- Supports PyInstaller onefile EXE, Windows privilege detection and auto-restart
- Hotkey (including Ctrl+C) and safe termination, unified logging for all prompts
- Friendly error handling, all important actions are prompted

## Installation & Usage

### 1. Download Executable

- Go to [Releases](https://github.com/t106362512/releases) and download the latest `nikke-cjjc-automator.exe`
- Double-click to run, or run from command line

### 2. Source Installation

```bash
pdm install
pdm run nikke-cjjc-automator
```

### 3. Build EXE

```bash
pdm run nikke-cjjc-automator-build
```

## Usage

- If not run as administrator, `img/manual.jpg` will be opened and a prompt will appear
- Enter the interactive menu and select an automation mode
- You can adjust delays, hotkeys, output directory, etc. in `settings.toml` or `settings.default.toml`
- Use Ctrl+C or custom hotkey to safely terminate during execution

## Configuration

- On first run, the program automatically copies the built-in `settings.default.toml` to `settings.toml` in the app's working directory and always loads settings from there.
- Key parameters:
  - `START_DELAY`, `INITIAL_PLAYER_DELAY`, `ACTION_DELAY`: Stage delays
  - `OUTPUT_DIR`: Output directory for merged images (default: `output_img` in the app's working directory)
  - `STOP_HOTKEY`: Custom stop hotkey (e.g. ctrl+c)

## Development/Architecture

- Core: `nikke_cjjc_automator/core.py`
- CLI entry: `nikke_cjjc_automator/cli.py`
- Config management: `nikke_cjjc_automator/config.py`
- Controller/Model/View layers for easy extension and maintenance
- Image merging, hotkey, and mode strategies are independent modules

## CI/CD

- Integrated with GitHub Actions, auto-builds EXE and uploads to Release
- Pushing a tag (e.g. v1.0.0) triggers the workflow

## Notes

- Windows only
- Please run as administrator
- If antivirus flags the program, add it to the whitelist

---

For questions or suggestions, please open a GitHub Issue.

<!-- 
pdm run pyi-grab_version C:\Windows\System32\cmd.exe version_info.txt
 -->