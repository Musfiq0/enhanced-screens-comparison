@echo off
title Enhanced Screenshot Comparison Tool - Build System
echo.
echo ========================================================
echo  Enhanced Screenshot Comparison Tool - Build System
echo ========================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python is available
echo.

:: Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [X] pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo [OK] pip is available
echo.

:: Install/upgrade required packages
echo [INFO] Installing/upgrading required packages...
pip install --upgrade -r requirements.txt
if errorlevel 1 (
    echo [X] Failed to install required packages
    pause
    exit /b 1
)

echo [OK] Packages installed successfully
echo.

:: Run the build script
echo [BUILD] Starting build process...
echo.
python build_exe.py

echo.
echo Build process completed!
echo.
echo Check the 'dist' folder for your executable.
echo.
pause
