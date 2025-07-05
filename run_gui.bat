@echo off
title Enhanced Screenshot Comparison Tool
echo.
echo ========================================================
echo  Enhanced Screenshot Comparison Tool - GUI
echo ========================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo.
    echo Alternatively, use the pre-built ScreenshotComparison.exe
    pause
    exit /b 1
)

echo [OK] Python detected
echo.

:: Check for required files
if not exist "gui_app.py" (
    echo [X] gui_app.py not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

if not exist "comparev2.py" (
    echo [X] comparev2.py not found
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

echo [OK] Required files found
echo.

:: Install dependencies if needed
echo [INFO] Checking dependencies...
pip show opencv-python >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [WARN] Some packages could not be installed
        echo The application may work with reduced functionality
    )
)

echo.
echo [START] Starting Enhanced Screenshot Comparison Tool...
echo.

:: Run the GUI application
python gui_app.py

echo.
echo Application closed.
pause
