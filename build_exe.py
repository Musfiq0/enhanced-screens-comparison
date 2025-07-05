# Enhanced Screenshot Comparison Tool - Build Script
"""
Build script for creating Windows executable using PyInstaller
Run this script to build the GUI application as a standalone .exe file
"""

import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building Enhanced Screenshot Comparison Tool executable...")
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Check if spec file exists for advanced build
    spec_file = current_dir / "screenshot_comparison.spec"
    
    if spec_file.exists():
        print("📋 Using advanced build configuration (spec file)")
        cmd = [
            "pyinstaller",
            "--clean",                      # Clean cache
            str(spec_file)                  # Use spec file
        ]
    else:
        print("📋 Using standard build configuration")
        # PyInstaller command
        cmd = [
            "pyinstaller",
            "--onefile",                    # Create a single executable file
            "--windowed",                   # Hide console window (GUI app)
            "--name=ScreenshotComparison",  # Name of the executable
            "--icon=" + str(current_dir / "icon.ico"),  # Icon file (absolute path)
            "--add-data=comparev2.py;.",    # Include the core comparison module
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
            "--upx-dir=upx",               # Use UPX compression if available
            "--clean",                      # Clean cache
            str(current_dir / "gui_app.py") # Main script
        ]
        
        # Remove icon parameter if icon doesn't exist
        icon_path = current_dir / "icon.ico"
        if not icon_path.exists():
            cmd = [c for c in cmd if not c.startswith("--icon")]
            print("⚠️ Icon file not found, building without custom icon")
    
    try:
        print(f"📋 Running command: {' '.join(cmd)}")
        print("⏳ This may take several minutes...")
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=current_dir)
        
        print("✅ Build completed successfully!")
        print(f"📁 Executable created in: {current_dir / 'dist'}")
        
        # Check if exe was created
        exe_path = current_dir / "dist" / "ScreenshotComparison.exe"
        if exe_path.exists():
            file_size_mb = exe_path.stat().st_size / (1024*1024)
            print(f"🎉 Executable size: {file_size_mb:.1f} MB")
            print(f"📍 Location: {exe_path}")
            
            # Test the executable
            print("\n🧪 Testing executable...")
            try:
                test_result = subprocess.run([str(exe_path), "--help"], 
                                           capture_output=True, text=True, timeout=10)
                if test_result.returncode == 0 or "Enhanced Screenshot Comparison" in test_result.stdout:
                    print("✅ Executable test passed!")
                else:
                    print("⚠️ Executable test returned non-zero exit code, but this may be normal")
            except subprocess.TimeoutExpired:
                print("⚠️ Executable test timed out (may be normal for GUI apps)")
            except Exception as e:
                print(f"⚠️ Could not test executable: {e}")
            
            # Create a portable package
            print("\n� Creating portable package...")
            try:
                create_portable_package(current_dir, exe_path)
            except Exception as e:
                print(f"⚠️ Could not create portable package: {e}")
        else:
            print("❌ Executable was not created")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    
    return True

def create_portable_package(current_dir, exe_path):
    """Create a portable package with the executable and documentation"""
    import shutil
    
    package_name = "ScreenshotComparison_Portable"
    package_dir = current_dir / package_name
    
    # Clean existing package
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copy executable
    shutil.copy2(exe_path, package_dir / "ScreenshotComparison.exe")
    
    # Copy documentation
    docs_to_copy = [
        ("README_GUI.md", "README.md"),
        ("requirements.txt", "requirements.txt"),
        ("comparev2.py", "comparev2.py"),  # For reference
    ]
    
    for src_name, dst_name in docs_to_copy:
        src_path = current_dir / src_name
        if src_path.exists():
            shutil.copy2(src_path, package_dir / dst_name)
    
    # Create a quick start guide
    quick_start = package_dir / "QUICK_START.txt"
    with open(quick_start, 'w', encoding='utf-8') as f:
        f.write("""Enhanced Screenshot Comparison Tool - Quick Start Guide
=========================================================

🚀 Getting Started:
1. Run ScreenshotComparison.exe
2. Add video files using "Add Video" button
3. Configure settings in the Settings tab
4. Click "Generate Screenshots"

📁 Features:
• Multiple video source comparison
• Source vs Encode comparison with cropping
• Automatic slow.pics upload
• Support for VapourSynth, OpenCV, and PIL backends
• Modern Windows GUI

📋 System Requirements:
• Windows 10/11 (64-bit)
• 4GB RAM minimum (8GB recommended)
• 100MB free disk space
• Internet connection (for slow.pics upload)

🔧 Optional for Best Quality:
• Install VapourSynth from: http://www.vapoursynth.com/

📖 Full Documentation:
See README.md for complete usage instructions.

🌐 slow.pics:
Visit https://slow.pics/ for manual comparison uploads.

Version: 2.0.0
""")
    
    print(f"✅ Portable package created: {package_dir}")
    print(f"📦 Package size: {sum(f.stat().st_size for f in package_dir.rglob('*') if f.is_file()) / (1024*1024):.1f} MB")

def build_with_auto_py_to_exe():
    """Alternative build method using auto-py-to-exe"""
    print("🔨 Building using auto-py-to-exe (interactive)...")
    print("This will open a web interface for configuring the build.")
    
    try:
        subprocess.run(["auto-py-to-exe"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch auto-py-to-exe: {e}")
        return False
    except FileNotFoundError:
        print("❌ auto-py-to-exe not found. Install it with: pip install auto-py-to-exe")
        return False
    
    return True

def main():
    """Main build function"""
    print("🚀 Enhanced Screenshot Comparison Tool - Build System")
    print("=" * 60)
    
    # Check if required tools are available
    tools_available = True
    
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
        print("✅ PyInstaller is available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller not found. Install it with: pip install pyinstaller")
        tools_available = False
    
    if not tools_available:
        print("\n📦 Installing required build tools...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "auto-py-to-exe"], 
                         check=True)
            print("✅ Build tools installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install build tools: {e}")
            return
    
    print("\nChoose build method:")
    print("1. 🔧 Automatic build with PyInstaller (recommended)")
    print("2. 🎨 Interactive build with auto-py-to-exe")
    print("3. 🚪 Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                if build_executable():
                    print("\n🎉 Build completed! Your executable is ready.")
                    print("📁 You can find it in the 'dist' folder.")
                break
            elif choice == "2":
                build_with_auto_py_to_exe()
                break
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n👋 Build cancelled by user.")
            break

if __name__ == "__main__":
    main()
