#!/usr/bin/env python3
"""
Build script for creating macOS application bundle using PyInstaller
Run this script to build the GUI application as a standalone .app bundle
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_pyinstaller_command(arguments, current_dir):
    """Run PyInstaller through the active Python interpreter."""
    cmd = [sys.executable, "-m", "PyInstaller"] + arguments
    return subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=current_dir)

def build_macos_app():
    """Build the macOS application bundle using PyInstaller"""
    print("🍎 Building Enhanced Screenshot Comparison Tool for macOS...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Check if we're on macOS
    if sys.platform != "darwin":
        print("❌ This build script is for macOS only!")
        print("   Use build_exe.py for Windows or build_linux.py for Linux")
        return False
    
    # Check if spec file exists for advanced build
    spec_file = current_dir / "screenshot_comparison_macos.spec"
    
    if spec_file.exists():
        print("📋 Using advanced build configuration (spec file)")
        cmd = ["--clean", str(spec_file)]
    else:
        print("📋 Using standard build configuration")
        # PyInstaller command for macOS
        cmd = [
            "--onedir",                     # Create a directory bundle (better for debugging)
            "--windowed",                   # Hide console window (GUI app)
            "--name=ScreenshotComparison",  # Name of the application
            "--icon=" + str(current_dir / "icon.icns") if (current_dir / "icon.icns").exists() else "--icon=" + str(current_dir / "icon.ico"),
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
            "--hidden-import=objc",         # macOS Objective-C bridge
            "--hidden-import=Foundation",   # macOS Foundation framework
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
        result = run_pyinstaller_command(cmd, current_dir)
        
        print("✅ Build completed successfully!")
        
        # Check if build was successful
        app_path = current_dir / "dist" / "ScreenshotComparison.app"
        if app_path.exists():
            print(f"📱 Application bundle created: {app_path}")
            
            # Create a disk image (DMG) for distribution
            print("📦 Creating disk image (DMG)...")
            create_dmg(app_path)
            
            print("\n🎉 Build Summary:")
            print(f"   📁 Application: dist/ScreenshotComparison.app")
            print(f"   💿 Disk Image: dist/ScreenshotComparison.dmg")
            print(f"   📏 Size: {get_size_mb(app_path)} MB")
            
            print("\n💡 Usage:")
            print("   • Double-click ScreenshotComparison.app to run")
            print("   • Distribute ScreenshotComparison.dmg to other users")
            print("   • App bundle is self-contained with all dependencies")
            
        else:
            print("❌ Build failed - application bundle not found")
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

def create_dmg(app_path):
    """Create a DMG disk image for distribution"""
    try:
        dmg_path = app_path.parent / "ScreenshotComparison.dmg"
        
        # Remove existing DMG
        if dmg_path.exists():
            dmg_path.unlink()
        
        # Create DMG
        cmd = [
            "hdiutil", "create",
            "-volname", "Screenshot Comparison",
            "-srcfolder", str(app_path),
            "-ov", "-format", "UDZO",
            str(dmg_path)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ DMG created: {dmg_path}")
        
    except subprocess.CalledProcessError:
        print("⚠️  Could not create DMG (optional)")
    except Exception as e:
        print(f"⚠️  DMG creation failed: {e}")

def get_size_mb(path):
    """Get the size of a file or directory in MB"""
    if path.is_file():
        return round(path.stat().st_size / (1024 * 1024), 1)
    elif path.is_dir():
        total_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        return round(total_size / (1024 * 1024), 1)
    return 0

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

if __name__ == "__main__":
    print("🍎 Enhanced Screenshot Comparison Tool - macOS Builder")
    print("=" * 60)
    
    if not check_requirements():
        sys.exit(1)
    
    if build_macos_app():
        print("\n🎉 macOS build completed successfully!")
    else:
        print("\n❌ macOS build failed!")
        sys.exit(1)
