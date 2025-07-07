#!/usr/bin/env python3
"""
Enhanced Screenshot Comparison Tool - Cross-Platform Setup Script
Automatically detects the platform and sets up the environment accordingly
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def print_colored(text, color_code=None):
    """Print colored text for better visibility"""
    colors = {
        'red': '\033[0;31m',
        'green': '\033[0;32m',
        'yellow': '\033[1;33m',
        'blue': '\033[0;34m',
        'cyan': '\033[0;36m',
        'white': '\033[1;37m',
        'reset': '\033[0m'
    }
    
    if color_code and color_code in colors:
        if platform.system() == "Windows":
            # For Windows, try to enable colored output
            try:
                import colorama
                colorama.init()
                print(f"{colors[color_code]}{text}{colors['reset']}")
            except ImportError:
                print(text)
        else:
            print(f"{colors[color_code]}{text}{colors['reset']}")
    else:
        print(text)

def print_header():
    """Print the setup header"""
    print()
    print_colored("=" * 60, 'cyan')
    print_colored("  Enhanced Screenshot Comparison Tool - Setup", 'cyan')
    print_colored("         Cross-Platform Installation", 'cyan')
    print_colored("=" * 60, 'cyan')
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored("❌ Python 3.8+ is required!", 'red')
        print_colored(f"   Current version: {version.major}.{version.minor}.{version.micro}", 'yellow')
        return False
    
    print_colored(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible", 'green')
    return True

def detect_platform():
    """Detect the current platform"""
    system = platform.system()
    architecture = platform.machine()
    
    platform_info = {
        'system': system,
        'architecture': architecture,
        'version': platform.version(),
        'is_windows': system == "Windows",
        'is_macos': system == "Darwin",
        'is_linux': system == "Linux"
    }
    
    print_colored(f"🖥️  Platform: {system} {architecture}", 'blue')
    return platform_info

def check_dependencies():
    """Check for required system dependencies"""
    print_colored("🔍 Checking system dependencies...", 'blue')
    
    missing_deps = []
    
    # Check for pip
    try:
        import pip
        print_colored("✅ pip - Available", 'green')
    except ImportError:
        print_colored("❌ pip - Not found", 'red')
        missing_deps.append("pip")
    
    # Check for git (optional but useful)
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        print_colored("✅ git - Available", 'green')
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_colored("⚠️  git - Not found (optional)", 'yellow')
    
    return missing_deps

def install_python_requirements():
    """Install Python requirements"""
    print_colored("📦 Installing Python dependencies...", 'blue')
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print_colored("❌ requirements.txt not found!", 'red')
        return False
    
    try:
        # Use the same Python interpreter that's running this script
        cmd = [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_colored("✅ Python dependencies installed successfully", 'green')
            return True
        else:
            print_colored("❌ Failed to install Python dependencies", 'red')
            print_colored(f"Error: {result.stderr}", 'red')
            return False
            
    except Exception as e:
        print_colored(f"❌ Error installing dependencies: {e}", 'red')
        return False

def setup_platform_specific():
    """Setup platform-specific configurations"""
    system = platform.system()
    
    if system == "Windows":
        return setup_windows()
    elif system == "Darwin":
        return setup_macos()
    elif system == "Linux":
        return setup_linux()
    else:
        print_colored(f"⚠️  Platform {system} not specifically supported, using generic setup", 'yellow')
        return True

def setup_windows():
    """Windows-specific setup"""
    print_colored("🪟 Setting up Windows configuration...", 'blue')
    
    # Check if START_HERE.bat exists
    bat_file = Path(__file__).parent / "START_HERE.bat"
    if bat_file.exists():
        print_colored("✅ Windows launcher (START_HERE.bat) is ready", 'green')
    else:
        print_colored("⚠️  Windows launcher not found", 'yellow')
    
    return True

def setup_macos():
    """macOS-specific setup"""
    print_colored("🍎 Setting up macOS configuration...", 'blue')
    
    # Make shell scripts executable
    scripts = ["start_here.sh", "docker_helper.sh"]
    for script in scripts:
        script_path = Path(__file__).parent / script
        if script_path.exists():
            try:
                os.chmod(script_path, 0o755)
                print_colored(f"✅ Made {script} executable", 'green')
            except Exception as e:
                print_colored(f"⚠️  Could not make {script} executable: {e}", 'yellow')
    
    return True

def setup_linux():
    """Linux-specific setup"""
    print_colored("🐧 Setting up Linux configuration...", 'blue')
    
    # Make shell scripts executable
    scripts = ["start_here.sh", "docker_helper.sh"]
    for script in scripts:
        script_path = Path(__file__).parent / script
        if script_path.exists():
            try:
                os.chmod(script_path, 0o755)
                print_colored(f"✅ Made {script} executable", 'green')
            except Exception as e:
                print_colored(f"⚠️  Could not make {script} executable: {e}", 'yellow')
    
    # Check for common Linux dependencies
    print_colored("🔍 Checking for system packages...", 'blue')
    
    # Check for tkinter (often needs separate package on Linux)
    try:
        import tkinter
        print_colored("✅ tkinter - Available", 'green')
    except ImportError:
        print_colored("❌ tkinter - Not found", 'red')
        print_colored("   Install with: sudo apt-get install python3-tk (Ubuntu/Debian)", 'yellow')
        print_colored("   or: sudo yum install tkinter (CentOS/RHEL)", 'yellow')
    
    return True

def create_desktop_shortcuts():
    """Create desktop shortcuts (platform-specific)"""
    system = platform.system()
    
    if system == "Windows":
        print_colored("💾 Windows shortcuts available via START_HERE.bat", 'blue')
    elif system == "Darwin":
        print_colored("💾 macOS: Use start_here.sh from terminal or create app bundle", 'blue')
    elif system == "Linux":
        print_colored("💾 Linux: Use start_here.sh or create .desktop file", 'blue')

def test_installation():
    """Test if the installation works"""
    print_colored("🧪 Testing installation...", 'blue')
    
    try:
        # Try importing core modules
        from comparev2 import detect_available_libraries
        print_colored("✅ Core comparison module - OK", 'green')
        
        # Test video processing backends
        backends = detect_available_libraries()
        if backends:
            print_colored(f"✅ Video processing backends: {', '.join(backends)}", 'green')
        else:
            print_colored("⚠️  No video processing backends found", 'yellow')
            print_colored("   You may need to install VapourSynth or additional libraries", 'yellow')
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Installation test failed: {e}", 'red')
        return False

def print_next_steps():
    """Print instructions for using the tool"""
    system = platform.system()
    
    print()
    print_colored("🎉 Setup complete! Next steps:", 'green')
    print()
    
    if system == "Windows":
        print_colored("📂 Run the tool:", 'white')
        print("   • Double-click START_HERE.bat for easy launcher")
        print("   • Or run: python gui_app.py (GUI mode)")
        print("   • Or run: python comparev2.py (Interactive CLI)")
        print("   • Or run: python comp-cli.py -h (Advanced CLI)")
    else:
        print_colored("📂 Run the tool:", 'white')
        print("   • Run: ./start_here.sh for easy launcher")
        print("   • Or run: python3 gui_app.py (GUI mode)")
        print("   • Or run: python3 comparev2.py (Interactive CLI)")
        print("   • Or run: python3 comp-cli.py -h (Advanced CLI)")
    
    print()
    print_colored("🐳 Docker usage:", 'white')
    print("   • Run: ./docker_helper.sh (Docker management)")
    print("   • Or run: docker-compose up screenshot-comparison")
    
    print()
    print_colored("📚 Documentation:", 'white')
    print("   • Check the wiki at: https://github.com/Musfiq0/enhanced-screens-comparison/wiki")
    print("   • Read Installation.md for detailed setup instructions")
    print()

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Detect platform
    platform_info = detect_platform()
    
    # Check system dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print_colored(f"❌ Missing dependencies: {', '.join(missing_deps)}", 'red')
        print_colored("Please install the missing dependencies and run setup again.", 'yellow')
        sys.exit(1)
    
    # Install Python requirements
    if not install_python_requirements():
        print_colored("❌ Failed to install Python requirements", 'red')
        sys.exit(1)
    
    # Platform-specific setup
    if not setup_platform_specific():
        print_colored("❌ Platform-specific setup failed", 'red')
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print_colored("❌ Installation test failed", 'red')
        sys.exit(1)
    
    # Create shortcuts
    create_desktop_shortcuts()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n⚠️  Setup cancelled by user", 'yellow')
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {e}", 'red')
        sys.exit(1)
