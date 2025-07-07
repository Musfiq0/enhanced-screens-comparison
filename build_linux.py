#!/usr/bin/env python3
"""
Build script for creating Linux application using PyInstaller
Run this script to build the GUI application as a standalone Linux binary
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_linux_app():
    """Build the Linux application using PyInstaller"""
    print("🐧 Building Enhanced Screenshot Comparison Tool for Linux...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Check if we're on Linux
    if sys.platform not in ["linux", "linux2"]:
        print("❌ This build script is for Linux only!")
        print("   Use build_exe.py for Windows or build_app.py for macOS")
        return False
    
    # Check if spec file exists for advanced build
    spec_file = current_dir / "screenshot_comparison_linux.spec"
    
    if spec_file.exists():
        print("📋 Using advanced build configuration (spec file)")
        cmd = [
            "pyinstaller",
            "--clean",                      # Clean cache
            str(spec_file)                  # Use spec file
        ]
    else:
        print("📋 Using standard build configuration")
        # PyInstaller command for Linux
        cmd = [
            "pyinstaller",
            "--onefile",                    # Create a single executable file
            "--name=ScreenshotComparison",  # Name of the executable
            "--add-data=comparev2.py:.",    # Include the core comparison module
            "--add-data=comp-cli.py:.",     # Include CLI module
            "--add-data=requirements.txt:.", # Include requirements
            "--add-data=README.md:.",       # Include readme
            "--hidden-import=tkinter",      # Ensure tkinter is included
            "--hidden-import=tkinter.ttk",  # Ensure ttk is included
            "--hidden-import=PIL",          # Ensure PIL is included
            "--hidden-import=cv2",          # Ensure OpenCV is included
            "--hidden-import=numpy",        # Ensure NumPy is included
            "--hidden-import=requests",     # Ensure requests is included
            "--hidden-import=requests_toolbelt",  # Ensure requests_toolbelt is included
            "--hidden-import=colorama",     # Ensure colorama is included
            "--exclude-module=matplotlib",  # Exclude large unused modules
            "--exclude-module=scipy",       # Exclude large unused modules
            "--exclude-module=pandas",      # Exclude large unused modules
            "--exclude-module=jupyter",     # Exclude large unused modules
            "--exclude-module=IPython",     # Exclude large unused modules
            "--exclude-module=test",        # Exclude test modules
            "--exclude-module=unittest",    # Exclude unittest
            "--exclude-module=doctest",     # Exclude doctest
            "--clean",                      # Clean cache before building
            "--noconfirm",                  # Overwrite output directory
            "gui_app.py"                    # Main script
        ]
    
    try:
        print("🔨 Starting build process...")
        print("   This may take several minutes...")
        
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Build completed successfully!")
        
        # Check if build was successful
        exe_path = current_dir / "dist" / "ScreenshotComparison"
        if exe_path.exists():
            print(f"🚀 Executable created: {exe_path}")
            
            # Make executable
            exe_path.chmod(0o755)
            
            # Create AppImage if tools are available
            print("📦 Attempting to create AppImage...")
            create_appimage(exe_path)
            
            print("\n🎉 Build Summary:")
            print(f"   📁 Executable: dist/ScreenshotComparison")
            print(f"   📏 Size: {get_size_mb(exe_path)} MB")
            
            # Check for AppImage
            appimage_path = current_dir / "dist" / "ScreenshotComparison.AppImage"
            if appimage_path.exists():
                print(f"   📦 AppImage: dist/ScreenshotComparison.AppImage")
            
            print("\n💡 Usage:")
            print("   • Run: ./dist/ScreenshotComparison")
            print("   • Or: chmod +x dist/ScreenshotComparison && ./dist/ScreenshotComparison")
            if appimage_path.exists():
                print("   • AppImage: ./dist/ScreenshotComparison.AppImage")
            print("   • Binary is self-contained with all dependencies")
            
        else:
            print("❌ Build failed - executable not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def create_appimage(exe_path):
    """Create an AppImage for easier distribution"""
    try:
        # Create AppDir structure
        appdir = exe_path.parent / "ScreenshotComparison.AppDir"
        if appdir.exists():
            shutil.rmtree(appdir)
        
        appdir.mkdir()
        (appdir / "usr" / "bin").mkdir(parents=True)
        (appdir / "usr" / "share" / "applications").mkdir(parents=True)
        (appdir / "usr" / "share" / "icons").mkdir(parents=True)
        
        # Copy executable
        shutil.copy2(exe_path, appdir / "usr" / "bin" / "ScreenshotComparison")
        
        # Create desktop file
        desktop_file = appdir / "ScreenshotComparison.desktop"
        desktop_content = """[Desktop Entry]
Type=Application
Name=Screenshot Comparison
Exec=ScreenshotComparison
Icon=screenshot-comparison
Comment=Enhanced Screenshot Comparison Tool
Categories=AudioVideo;Video;
"""
        desktop_file.write_text(desktop_content)
        
        # Copy icon if available
        icon_files = ["icon.png", "icon.ico", "icon.svg"]
        for icon_file in icon_files:
            icon_path = exe_path.parent.parent / icon_file
            if icon_path.exists():
                shutil.copy2(icon_path, appdir / "usr" / "share" / "icons" / "screenshot-comparison.png")
                break
        
        # Create AppRun
        apprun = appdir / "AppRun"
        apprun_content = """#!/bin/bash
cd "$(dirname "$0")"
exec ./usr/bin/ScreenshotComparison "$@"
"""
        apprun.write_text(apprun_content)
        apprun.chmod(0o755)
        
        # Try to create AppImage using appimagetool if available
        try:
            cmd = ["appimagetool", str(appdir), str(exe_path.parent / "ScreenshotComparison.AppImage")]
            subprocess.run(cmd, check=True, capture_output=True)
            print("✅ AppImage created successfully")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  appimagetool not found - AppImage creation skipped")
            print("   Install appimagetool for AppImage creation")
        
    except Exception as e:
        print(f"⚠️  AppImage creation failed: {e}")

def get_size_mb(path):
    """Get the size of a file in MB"""
    return round(path.stat().st_size / (1024 * 1024), 1)

def check_requirements():
    """Check if build requirements are available"""
    try:
        import PyInstaller
        print("✅ PyInstaller available")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    # Check for main files
    required_files = ["gui_app.py", "comparev2.py", "requirements.txt"]
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ Required file not found: {file}")
            return False
    
    print("✅ All requirements satisfied")
    return True

def install_system_dependencies():
    """Show instructions for installing system dependencies"""
    print("\n📋 System Dependencies (may be required):")
    print("   Ubuntu/Debian:")
    print("     sudo apt-get install python3-tk libgtk-3-dev")
    print("   RHEL/CentOS/Fedora:")
    print("     sudo yum install tkinter gtk3-devel")
    print("     # or: sudo dnf install python3-tkinter gtk3-devel")
    print("   Arch Linux:")
    print("     sudo pacman -S tk gtk3")

if __name__ == "__main__":
    print("🐧 Enhanced Screenshot Comparison Tool - Linux Builder")
    print("=" * 60)
    
    install_system_dependencies()
    
    if not check_requirements():
        sys.exit(1)
    
    if build_linux_app():
        print("\n🎉 Linux build completed successfully!")
    else:
        print("\n❌ Linux build failed!")
        sys.exit(1)
