@echo off
title Enhanced Screenshot Comparison - Advanced CLI

echo.
echo ========================================
echo   Enhanced Screenshot Comparison Tool
echo              Advanced CLI
echo ========================================
echo.
echo This launches the professional command-line interface
echo with full automation and scripting capabilities.
echo.
echo For help and examples, run:
echo   python comp-cli.py --help
echo.
echo For available presets, run:
echo   python comp-cli.py --list-presets
echo.
echo Quick start examples:
echo   python comp-cli.py --videos source.mkv encode.mkv
echo   python comp-cli.py --demo
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if the CLI file exists
if not exist "comp-cli.py" (
    echo ERROR: comp-cli.py not found in current directory
    echo Please run this batch file from the Enhanced Screenshot Comparison Tool directory
    pause
    exit /b 1
)

REM If no arguments provided, show help
if "%~1"=="" (
    python comp-cli.py --help
    echo.
    echo Ready for commands! Examples:
    echo   python comp-cli.py --videos *.mkv
    echo   python comp-cli.py --mode source-encode --source original.mkv --encode compressed.mkv
    echo.
    echo Press any key to exit...
    pause >nul
) else (
    REM Pass all arguments to the CLI
    python comp-cli.py %*
    echo.
    if errorlevel 1 (
        echo Command failed with error code %errorlevel%
    ) else (
        echo Command completed successfully!
    )
    echo Press any key to exit...
    pause >nul
)
