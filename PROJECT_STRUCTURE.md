# Project File Overview

## Core Application Files
- `gui_app.py` - Main GUI application
- `comparev2.py` - CLI tool and comparison engine
- `icon.ico` - Application icon

## Dependencies & Requirements
- `requirements.txt` - Python dependencies list

## Build System
- `build_exe.py` - Script to build standalone executable
- `screenshot_comparison.spec` - PyInstaller configuration
- `version_info.txt` - Version metadata for executable
- `build.bat` - Windows batch file for easy building

## Quick Launch Scripts
- `START_HERE.bat` - Main launcher (GUI)
- `run_gui.bat` - Alternative GUI launcher

## Project Management
- `README.md` - Main project documentation
- `.gitignore` - Git ignore rules
- `Screenshots/` - Output directory for generated screenshots

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run GUI: `python gui_app.py` or double-click `START_HERE.bat`
3. Run CLI: `python comparev2.py`
4. Build executable: `python build_exe.py`
