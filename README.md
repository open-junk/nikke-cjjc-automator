# NIKKE CJJC Automator

NIKKE CJJC Automator is a modern, maintainable, and extensible automation tool for NIKKE, supporting multi-mode automation, interactive CLI, Windows privilege detection, image caching and merging, and safe hotkey termination.

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
- You can adjust delays, hotkeys, output directory, etc. in `settings.default.toml`
- Use Ctrl+C or custom hotkey to safely terminate during execution

## Configuration
- `settings.default.toml`: Centralized management of all parameters, auto-copied to user directory on first run
- Key parameters:
  - `START_DELAY`, `INITIAL_PLAYER_DELAY`, `ACTION_DELAY`: Delays for each stage
  - `OUTPUT_DIR`: Output directory for merged images
  - `STOP_HOTKEY`: Custom stop hotkey (supports ctrl+c)

## Development/Architecture
- Main: `nikke_cjjc_automator/main.py`
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

