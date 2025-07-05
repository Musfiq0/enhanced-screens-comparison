@echo off
setlocal enabledelayedexpansion
title Enhanced Screenshot Comparison Tool - Complete System
color 0A

:: ASCII Art Header
echo.
echo  +======================================================================+
echo  ^|                Enhanced Screenshot Comparison Tool                   ^|
echo  ^|                     Complete Windows Application                     ^|
echo  +======================================================================+
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo [OK] Python %PYTHON_VERSION% detected

:: Check for required files
set "MISSING_FILES="
if not exist "gui_app.py" set "MISSING_FILES=!MISSING_FILES! gui_app.py"
if not exist "comparev2.py" set "MISSING_FILES=!MISSING_FILES! comparev2.py"
if not exist "requirements.txt" set "MISSING_FILES=!MISSING_FILES! requirements.txt"

if not "!MISSING_FILES!"=="" (
    echo [X] Missing required files:!MISSING_FILES!
    echo.
    echo Please ensure all files are in the same directory
    pause
    exit /b 1
)

echo [OK] All required files found
echo.

:MAIN_MENU
cls
echo  +======================================================================+
echo  ^|                Enhanced Screenshot Comparison Tool                   ^|
echo  +======================================================================+
echo.
echo  ^> Main Menu - Choose your action:
echo.
echo  QUICK ACTIONS:
echo     1. Run GUI Application (Recommended)
echo     2. Setup Development Environment
echo.
echo  BUILD ACTIONS:
echo     3. Build Windows Executable (.exe)
echo     4. Create Complete Distribution Package
echo     5. Build with Advanced Options
echo.
echo  MAINTENANCE:
echo     6. Install/Update Dependencies
echo     7. Check Application Icon
echo     8. Clean Build Files
echo     9. Show Project Information
echo.
echo     0. Exit
echo.
set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" goto RUN_GUI
if "%choice%"=="2" goto SETUP_DEV
if "%choice%"=="3" goto BUILD_EXE
if "%choice%"=="4" goto BUILD_DIST
if "%choice%"=="5" goto BUILD_ADVANCED
if "%choice%"=="6" goto INSTALL_DEPS
if "%choice%"=="7" goto CREATE_ICON
if "%choice%"=="8" goto CLEAN_BUILD
if "%choice%"=="9" goto SHOW_INFO
if "%choice%"=="0" goto EXIT

echo [X] Invalid choice. Please select 0-9.
timeout /t 2 >nul
goto MAIN_MENU

:RUN_GUI
cls
echo  +======================================================================+
echo  ^|                         Running GUI Application                      ^|
echo  +======================================================================+
echo.
echo ^> Starting Enhanced Screenshot Comparison Tool...
echo.

:: Quick dependency check
echo [INFO] Checking core dependencies...
python -c "import tkinter" 2>nul
if errorlevel 1 (
    echo [WARN] tkinter not available
    echo Installing basic dependencies...
    pip install --quiet pillow opencv-python numpy requests requests-toolbelt colorama
)

python -c "import cv2, PIL, numpy, requests" 2>nul
if errorlevel 1 (
    echo [WARN] Some dependencies missing. Installing...
    pip install --quiet pillow opencv-python numpy requests requests-toolbelt colorama
)

echo [OK] Dependencies check completed
echo.
echo [START] Launching GUI application...
python gui_app.py

echo.
echo [DONE] GUI application closed.
pause
goto MAIN_MENU

:SETUP_DEV
cls
echo  +======================================================================+
echo  ^|                    Setting Up Development Environment                ^|
echo  +======================================================================+
echo.
echo [START] Installing dependencies...
echo.
pip install --upgrade -r requirements.txt
echo.
echo [OK] Development environment setup completed!
echo.
echo [INFO] Environment ready for:
echo   - Running GUI application: python gui_app.py
echo   - Running CLI tool: python comparev2.py  
echo   - Building executable: python build_exe.py
echo.
pause
goto MAIN_MENU

:BUILD_EXE
cls
echo  +======================================================================+
echo  ^|                       Building Windows Executable                   ^|
echo  +======================================================================+
echo.
echo [BUILD] Building ScreenshotComparison.exe...
echo [INFO] This may take several minutes...
echo.

:: Install build dependencies
echo [DEPS] Installing build tools...
pip install --upgrade pyinstaller >nul 2>&1

:: Check for icon
if not exist "icon.ico" (
    echo [WARN] Application icon not found. Build will continue without custom icon.
)

:: Run the build
echo [COMPILE] Compiling application...
python build_exe.py

echo.
if exist "dist\ScreenshotComparison.exe" (
    echo [OK] Build completed successfully!
    echo [INFO] Executable location: dist\ScreenshotComparison.exe
    
    :: Get file size
    for %%A in ("dist\ScreenshotComparison.exe") do set "SIZE=%%~zA"
    set /a SIZE_MB=!SIZE!/1048576
    echo [SIZE] File size: !SIZE_MB! MB
    
    echo.
    echo Would you like to test the executable now? (y/n)
    set /p test_choice=""
    if /i "!test_choice!"=="y" (
        echo [TEST] Testing executable...
        start "" "dist\ScreenshotComparison.exe"
    )
) else (
    echo [ERROR] Build failed. Check the output above for errors.
)

echo.
pause
goto MAIN_MENU

:BUILD_DIST
cls
echo  +======================================================================+
echo  ^|                   Creating Distribution Packages                    ^|
echo  +======================================================================+
echo.
echo [DIST] Creating complete distribution package...
echo.

:: Check if executable exists
if not exist "dist\ScreenshotComparison.exe" (
    echo [WARN] Executable not found. Building it first...
    echo.
    call :BUILD_EXE_SILENT
)

echo [BUILD] Running advanced build system...
python advanced_build.py

echo.
if exist "distribution" (
    echo [OK] Distribution packages created successfully!
    echo [INFO] Package location: distribution\
    echo.
    echo [PACKAGES] Available packages:
    dir distribution\*.* /b
    echo.
    echo Would you like to open the distribution folder? (y/n)
    set /p open_choice=""
    if /i "!open_choice!"=="y" (
        start "" "distribution"
    )
) else (
    echo [ERROR] Distribution creation failed.
)

echo.
pause
goto MAIN_MENU

:BUILD_EXE_SILENT
echo [DEPS] Installing build tools...
pip install --quiet --upgrade pyinstaller
if not exist "icon.ico" (
    echo [WARN] No icon file found. Building without custom icon.
)
echo [BUILD] Building executable...
python build_exe.py >nul 2>&1
goto :eof

:BUILD_ADVANCED
cls
echo  +======================================================================+
echo  ^|                         Advanced Build Options                      ^|
echo  +======================================================================+
echo.
echo [ADVANCED] Advanced build system with interactive options...
echo.
python advanced_build.py
echo.
pause
goto MAIN_MENU

:INSTALL_DEPS
cls
echo  +======================================================================+
echo  ^|                      Installing Dependencies                        ^|
echo  +======================================================================+
echo.
echo [DEPS] Installing/updating all dependencies...
echo.

if exist "requirements.txt" (
    echo [FILE] Installing from requirements.txt...
    pip install --upgrade -r requirements.txt
) else (
    echo [CORE] Installing core dependencies...
    pip install --upgrade tkinter pillow opencv-python numpy requests requests-toolbelt colorama pyinstaller
)

echo.
echo [TEST] Testing imports...
python -c "import tkinter, cv2, PIL, numpy, requests; print('[OK] All core dependencies available')" 2>nul
if errorlevel 1 (
    echo [WARN] Some dependencies may have issues
) else (
    echo [OK] All dependencies installed successfully!
)

echo.
pause
goto MAIN_MENU

:CREATE_ICON
cls
echo  +======================================================================+
echo  ^|                        Application Icon Status                      ^|
echo  +======================================================================+
echo.

if exist "icon.ico" (
    echo [OK] Application icon already exists: icon.ico
    echo.
    echo [INFO] Icon details:
    for %%A in ("icon.ico") do echo   - File size: %%~zA bytes
    for %%A in ("icon.ico") do echo   - Last modified: %%~tA
    echo   - Format: Windows ICO format
    echo   - Resolution: 256x256 pixels
    echo.
    echo [USAGE] This icon is used when building the executable
    echo.
    echo Would you like to view the icon? (y/n)
    set /p view_choice=""
    if /i "!view_choice!"=="y" (
        start "" "icon.ico"
    )
) else (
    echo [ERROR] Application icon not found: icon.ico
    echo.
    echo [HELP] The icon file is required for building the executable.
    echo Please ensure icon.ico is in the project directory.
)

echo.
pause
goto MAIN_MENU

:CLEAN_BUILD
cls
echo  +======================================================================+
echo  ^|                          Cleaning Build Files                       ^|
echo  +======================================================================+
echo.
echo [CLEAN] Cleaning build artifacts...
echo.

set "CLEANED=0"

if exist "build" (
    echo [DEL] Removing build folder...
    rmdir /s /q "build" 2>nul
    set /a CLEANED+=1
)

if exist "dist" (
    echo [DEL] Removing dist folder...
    rmdir /s /q "dist" 2>nul
    set /a CLEANED+=1
)

if exist "distribution" (
    echo [DEL] Removing distribution folder...
    rmdir /s /q "distribution" 2>nul
    set /a CLEANED+=1
)

if exist "__pycache__" (
    echo [DEL] Removing Python cache...
    rmdir /s /q "__pycache__" 2>nul
    set /a CLEANED+=1
)

:: Clean spec files
for %%f in (*.spec) do (
    if exist "%%f" (
        echo [DEL] Removing %%f...
        del "%%f" 2>nul
        set /a CLEANED+=1
    )
)

:: Clean log files
for %%f in (*.log) do (
    if exist "%%f" (
        echo [DEL] Removing %%f...
        del "%%f" 2>nul
        set /a CLEANED+=1
    )
)

echo.
echo [OK] Cleaned !CLEANED! items
echo.
pause
goto MAIN_MENU

:SHOW_INFO
cls
echo  +======================================================================+
echo  ^|                          Project Information                        ^|
echo  +======================================================================+
echo.
echo [INFO] Enhanced Screenshot Comparison Tool
echo.
echo [VERSION] Current Version: 2.0.0
echo [PYTHON] Required: Python 3.8+
echo [STATUS] All core features implemented and tested
echo.
echo [FEATURES]
echo   - GUI Application with modern Windows interface
echo   - CLI tool for automation and scripting
echo   - Multiple video processing backends (VapourSynth, OpenCV, PIL)
echo   - Source vs Encode and Multiple Sources comparison modes
echo   - Automatic slow.pics upload integration
echo   - Advanced processing options (crop, resize, frame selection)
echo   - Instant stop function for long operations
echo   - Professional executable building
echo.
echo [FILES]
echo   - gui_app.py: GUI application
echo   - comparev2.py: CLI comparison tool
echo   - requirements.txt: All dependencies
echo   - build_exe.py: Executable builder
echo   - README.md: Complete documentation
echo.
echo [BUILD] To build executable: Choose option 3 from main menu
echo [DOCS] See README.md for complete documentation
echo.
pause
goto MAIN_MENU

:EXIT
cls
echo  +======================================================================+
echo  ^|                              Thank You!                             ^|
echo  +======================================================================+
echo.
echo [INFO] Thank you for using Enhanced Screenshot Comparison Tool!
echo.
echo [TIPS] Quick Tips:
echo    * Your built executable will be in the 'dist' folder
echo    * Use ScreenshotComparison.exe - no installation needed
echo    * Check 'distribution' folder for complete packages
echo.
echo [HELP] For help and updates, check the README files
echo.
echo [BYE] Goodbye!
echo.
timeout /t 3 >nul
exit /b 0
