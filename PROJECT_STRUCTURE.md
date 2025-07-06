# Project File Overview

## Core Application Files
- `gui_app.py` - Main GUI application
- `comparev2.py` - Interactive CLI tool and comparison engine
- `comp-cli.py` - **NEW** Advanced CLI with complete command-line interface
- `icon.ico` - Application icon

## Dependencies & Requirements
- `requirements.txt` - Python dependencies list

## Build System
- `build_exe.py` - Script to build standalone executable
- `screenshot_comparison.spec` - PyInstaller configuration
- `version_info.txt` - Version metadata for executable
- `build.bat` - Windows batch file for easy building

## Quick Launch Scripts
- `START_HERE.bat` - Main launcher with all options (updated)
- `run_gui.bat` - Alternative GUI launcher
- `run_advanced_cli.bat` - **NEW** Advanced CLI launcher

## Configuration and Examples
- `sample_config.json` - **NEW** Sample configuration for Advanced CLI
- `enhanced-screens-comparison.wiki/Advanced-CLI.md` - **NEW** Comprehensive Advanced CLI documentation

## Documentation
- `README.md` - Main project documentation
- `enhanced-screens-comparison.wiki/` - Complete wiki documentation
  - `Command-Line-Interface-(CLI).md` - **UPDATED** with Advanced CLI info
  - `Usage.md` - **UPDATED** with new CLI modes
  - Other wiki pages for features, installation, etc.

## Project Management
- `.gitignore` - Git ignore rules
- `LICENSE` - Project license
- `Screenshots/` - Output directory for generated screenshots

## Interface Modes Available

### 1. GUI Mode (Easiest)
- **File**: `gui_app.py`
- **Launch**: `START_HERE.bat` → Option 1
- **Features**: Complete drag & drop interface
- **Users**: Beginners and visual users

### 2. Interactive CLI (Guided)
- **File**: `comparev2.py`
- **Launch**: `START_HERE.bat` → Option 2
- **Features**: Step-by-step prompts with full functionality
- **Users**: Power users who want guidance

### 3. Advanced CLI (Professional) 🆕
- **File**: `comp-cli.py`
- **Launch**: `START_HERE.bat` → Option 3
- **Features**: Complete command-line control, automation-ready
- **Users**: Professionals, automation, CI/CD pipelines

## Getting Started
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Quick start**: Double-click `START_HERE.bat` and choose your interface
3. **GUI**: `python gui_app.py` or `run_gui.bat`
4. **Interactive CLI**: `python comparev2.py`
5. **Advanced CLI**: `python comp-cli.py --help`
6. **Build executable**: `python build_exe.py`

## Advanced CLI Quick Examples
```bash
# Basic comparison
python comp-cli.py --videos source.mkv encode.mkv

# Professional workflow
python comp-cli.py --mode source-encode --source original.mkv --encode compressed.mkv --crop-preset 2.35:1 --upload

# Batch processing
python comp-cli.py --config sample_config.json --upload --collection-name "Quality Test"
```
