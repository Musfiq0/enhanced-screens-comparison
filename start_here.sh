#!/bin/bash
# Enhanced Screenshot Comparison Tool - Cross-Platform Launcher
# Universal launcher for macOS and Linux systems

set -e  # Exit on any error

# Color codes for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to print colored text
print_colored() {
    echo -e "${1}${2}${NC}"
}

# Function to print header
print_header() {
    echo ""
    print_colored $CYAN "========================================"
    print_colored $CYAN "  Enhanced Screenshot Comparison Tool"
    print_colored $CYAN "       Cross-Platform Edition"
    print_colored $CYAN "========================================"
    echo ""
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect Python command
detect_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        # Check if it's Python 3
        if python -c "import sys; exit(0 if sys.version_info[0] == 3 else 1)" 2>/dev/null; then
            PYTHON_CMD="python"
        else
            print_colored $RED "Error: Python 3 is required but only Python 2 found."
            print_colored $YELLOW "Please install Python 3.8+ and try again."
            exit 1
        fi
    else
        print_colored $RED "Error: Python not found in PATH."
        print_colored $YELLOW "Please install Python 3.8+ and try again."
        exit 1
    fi
}

# Function to check Python version
check_python_version() {
    local version=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
        print_colored $RED "Error: Python 3.8+ is required. Found Python $version"
        exit 1
    fi
    
    print_colored $GREEN "✓ Python $version detected"
}

# Function to check/install dependencies
check_dependencies() {
    print_colored $BLUE "Checking dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_colored $RED "Error: requirements.txt not found!"
        exit 1
    fi
    
    # Check if pip is available
    if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
        print_colored $RED "Error: pip not found!"
        print_colored $YELLOW "Please install pip and try again."
        exit 1
    fi
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_colored $YELLOW "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_colored $BLUE "Upgrading pip..."
    python -m pip install --upgrade pip >/dev/null 2>&1
    
    # Install/update dependencies
    print_colored $BLUE "Installing/updating dependencies..."
    pip install -r requirements.txt >/dev/null 2>&1
    
    print_colored $GREEN "✓ Dependencies ready"
}

# Function to show main menu
show_menu() {
    echo ""
    print_colored $WHITE "Select an option:"
    echo ""
    print_colored $GREEN "1. 🖼️  Launch GUI Application"
    print_colored $BLUE "2. 💻  Run Interactive Console"
    print_colored $MAGENTA "3. ⚡  Advanced CLI Interface"
    print_colored $CYAN "4. 📦  Install/Update Dependencies"
    print_colored $YELLOW "5. 🔍  Check System Info"
    echo ""
    print_colored $WHITE "0. ❌  Exit"
    echo ""
}

# Function to launch GUI
launch_gui() {
    print_colored $GREEN "Launching GUI Application..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    $PYTHON_CMD gui_app.py
}

# Function to launch console
launch_console() {
    print_colored $BLUE "Launching Interactive Console..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    $PYTHON_CMD comparev2.py
}

# Function to launch advanced CLI
launch_cli() {
    print_colored $MAGENTA "Advanced CLI Interface:"
    print_colored $WHITE "Usage: python comp-cli.py [videos] [options]"
    echo ""
    print_colored $CYAN "Examples:"
    print_colored $WHITE "  python comp-cli.py video1.mkv video2.mp4"
    print_colored $WHITE "  python comp-cli.py *.mkv -cn \"My Collection\" -u"
    print_colored $WHITE "  python comp-cli.py source.mkv encode.mkv -f 1000,5000,9000"
    echo ""
    print_colored $WHITE "For full help: python comp-cli.py --help"
    echo ""
    
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    $PYTHON_CMD comp-cli.py --help
}

# Function to show system info
show_system_info() {
    print_colored $CYAN "System Information:"
    echo ""
    
    # OS Information
    if command_exists uname; then
        print_colored $WHITE "OS: $(uname -s) $(uname -r)"
        print_colored $WHITE "Architecture: $(uname -m)"
    fi
    
    # Python Information
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    print_colored $WHITE "Python: $($PYTHON_CMD --version)"
    print_colored $WHITE "Pip: $($PYTHON_CMD -m pip --version | cut -d' ' -f1-2)"
    
    # Check video processing backends
    print_colored $BLUE "Checking video processing backends..."
    $PYTHON_CMD comparev2.py --demo
}

# Main script
main() {
    print_header
    
    # Detect Python
    detect_python
    check_python_version
    
    # Check if we're in the right directory
    if [ ! -f "comparev2.py" ]; then
        print_colored $RED "Error: Please run this script from the project directory."
        exit 1
    fi
    
    while true; do
        show_menu
        read -p "$(print_colored $WHITE "Enter your choice: ")" choice
        
        case $choice in
            1)
                launch_gui
                ;;
            2)
                launch_console
                ;;
            3)
                launch_cli
                ;;
            4)
                check_dependencies
                ;;
            5)
                show_system_info
                ;;
            0)
                print_colored $GREEN "Thanks for using Enhanced Screenshot Comparison Tool!"
                exit 0
                ;;
            *)
                print_colored $RED "Invalid option. Please try again."
                ;;
        esac
        
        echo ""
        read -p "$(print_colored $YELLOW "Press Enter to continue...")"
    done
}

# Run main function
main "$@"
