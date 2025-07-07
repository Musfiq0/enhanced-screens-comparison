#!/bin/bash
# Enhanced Screenshot Comparison Tool - Docker Helper Script
# Cross-platform Docker management for the comparison tool

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

print_colored() {
    echo -e "${1}${2}${NC}"
}

print_header() {
    echo ""
    print_colored $CYAN "========================================"
    print_colored $CYAN "  Screenshot Comparison - Docker Helper"
    print_colored $CYAN "========================================"
    echo ""
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_colored $RED "❌ Docker not found!"
        print_colored $YELLOW "Please install Docker Desktop and try again."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_colored $RED "❌ Docker daemon not running!"
        print_colored $YELLOW "Please start Docker Desktop and try again."
        exit 1
    fi
    
    print_colored $GREEN "✅ Docker is ready"
}

build_image() {
    print_colored $BLUE "🔨 Building Docker image..."
    docker build -t enhanced-screenshot-comparison:latest .
    print_colored $GREEN "✅ Image built successfully"
}

show_menu() {
    echo ""
    print_colored $WHITE "Docker Operations:"
    echo ""
    print_colored $GREEN "1. 🔨  Build Docker Image"
    print_colored $BLUE "2. 🖼️  Run GUI Mode (X11 forwarding)"
    print_colored $CYAN "3. 💻  Run Interactive CLI"
    print_colored $MAGENTA "4. ⚡  Run Advanced CLI"
    print_colored $YELLOW "5. 📦  Run with Docker Compose"
    print_colored $WHITE "6. 🧹  Clean Docker Resources"
    print_colored $WHITE "7. ℹ️   Show Docker Info"
    echo ""
    print_colored $WHITE "0. ❌  Exit"
    echo ""
}

run_gui() {
    print_colored $BLUE "🖼️ Starting GUI mode..."
    
    # Detect platform for X11 forwarding
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux with X11 forwarding
        xhost +local:docker 2>/dev/null || true
        docker run -it --rm \
            -e DISPLAY=$DISPLAY \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            -v $(pwd):/workspace \
            -v $(pwd)/Screenshots:/app/Screenshots \
            --name screenshot-comparison-gui \
            enhanced-screenshot-comparison:latest \
            python gui_app.py
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS with XQuartz
        print_colored $YELLOW "⚠️  GUI mode on macOS requires XQuartz:"
        print_colored $WHITE "   1. Install XQuartz: brew install --cask xquartz"
        print_colored $WHITE "   2. Start XQuartz and enable 'Allow connections from network clients'"
        print_colored $WHITE "   3. Run: xhost +localhost"
        echo ""
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker run -it --rm \
                -e DISPLAY=host.docker.internal:0 \
                -v $(pwd):/workspace \
                -v $(pwd)/Screenshots:/app/Screenshots \
                --name screenshot-comparison-gui \
                enhanced-screenshot-comparison:latest \
                python gui_app.py
        fi
    else
        # Windows or other
        print_colored $YELLOW "⚠️  GUI mode requires X11 forwarding setup"
        print_colored $WHITE "   Consider using CLI mode instead"
        print_colored $WHITE "   Or set up X11 forwarding (VcXsrv, Xming, etc.)"
    fi
}

run_cli() {
    print_colored $CYAN "💻 Starting interactive CLI..."
    docker run -it --rm \
        -v $(pwd):/workspace \
        -v $(pwd)/Screenshots:/app/Screenshots \
        --name screenshot-comparison-cli \
        enhanced-screenshot-comparison:latest \
        python comparev2.py
}

run_advanced_cli() {
    print_colored $MAGENTA "⚡ Advanced CLI mode"
    print_colored $WHITE "Enter your command arguments (or press Enter for help):"
    read -r args
    
    if [ -z "$args" ]; then
        args="--help"
    fi
    
    docker run -it --rm \
        -v $(pwd):/workspace \
        -v $(pwd)/Screenshots:/app/Screenshots \
        --name screenshot-comparison-advanced \
        enhanced-screenshot-comparison:latest \
        python comp-cli.py $args
}

run_compose() {
    print_colored $YELLOW "📦 Docker Compose options:"
    echo ""
    print_colored $WHITE "1. Interactive CLI service"
    print_colored $WHITE "2. GUI service (Linux only)"
    print_colored $WHITE "3. Batch processing example"
    echo ""
    read -p "Select service (1-3): " choice
    
    case $choice in
        1)
            docker-compose run --rm screenshot-comparison-cli
            ;;
        2)
            if [[ "$OSTYPE" == "linux-gnu"* ]]; then
                xhost +local:docker 2>/dev/null || true
                docker-compose run --rm screenshot-comparison python gui_app.py
            else
                print_colored $YELLOW "⚠️  GUI service only supported on Linux"
            fi
            ;;
        3)
            print_colored $BLUE "🔄 Running batch processing example..."
            docker-compose run --rm screenshot-comparison-batch
            ;;
        *)
            print_colored $RED "Invalid option"
            ;;
    esac
}

clean_docker() {
    print_colored $YELLOW "🧹 Cleaning Docker resources..."
    
    # Stop and remove containers
    docker ps -a --filter "name=screenshot-comparison" --format "{{.Names}}" | xargs -r docker rm -f
    
    # Remove images (optional)
    read -p "Remove Docker image? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker rmi enhanced-screenshot-comparison:latest 2>/dev/null || true
    fi
    
    # Clean up system
    docker system prune -f
    print_colored $GREEN "✅ Cleanup completed"
}

show_docker_info() {
    print_colored $CYAN "ℹ️  Docker Information:"
    echo ""
    
    print_colored $WHITE "Docker Version:"
    docker --version
    
    print_colored $WHITE "\nDocker Images:"
    docker images | grep -E "(enhanced-screenshot|REPOSITORY)" || echo "No images found"
    
    print_colored $WHITE "\nRunning Containers:"
    docker ps --filter "name=screenshot-comparison" || echo "No running containers"
    
    print_colored $WHITE "\nDocker Compose Services:"
    if [ -f "docker-compose.yml" ]; then
        docker-compose config --services
    else
        echo "docker-compose.yml not found"
    fi
}

main() {
    print_header
    check_docker
    
    # Check if image exists
    if ! docker images | grep -q "enhanced-screenshot-comparison"; then
        print_colored $YELLOW "⚠️  Docker image not found. Building..."
        build_image
    fi
    
    while true; do
        show_menu
        read -p "$(print_colored $WHITE "Enter your choice: ")" choice
        
        case $choice in
            1)
                build_image
                ;;
            2)
                run_gui
                ;;
            3)
                run_cli
                ;;
            4)
                run_advanced_cli
                ;;
            5)
                run_compose
                ;;
            6)
                clean_docker
                ;;
            7)
                show_docker_info
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

main "$@"
