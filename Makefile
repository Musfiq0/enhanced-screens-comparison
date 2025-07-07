# Enhanced Screenshot Comparison Tool - Cross-Platform Makefile
# Provides common commands for building and running across platforms

.PHONY: help setup install clean build build-windows build-macos build-linux build-docker run-gui run-cli run-console test lint format docker-build docker-run docker-clean

# Default target
help:
	@echo "Enhanced Screenshot Comparison Tool - Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  setup          - Run cross-platform setup"
	@echo "  install        - Install Python dependencies"
	@echo "  clean          - Clean build artifacts"
	@echo "  build          - Build for current platform"
	@echo "  build-windows  - Build Windows executable (.exe)"
	@echo "  build-macos    - Build macOS application (.app)"
	@echo "  build-linux    - Build Linux binary (AppImage)"
	@echo "  build-docker   - Build Docker image"
	@echo "  run-gui        - Run GUI application"
	@echo "  run-cli        - Run interactive CLI"
	@echo "  run-console    - Run console version"
	@echo "  test           - Run tests"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format code"
	@echo "  docker-build   - Build Docker image"
	@echo "  docker-run     - Run in Docker container"
	@echo "  docker-clean   - Clean Docker artifacts"

# Setup and installation
setup:
	python setup.py

install:
	pip install -r requirements.txt

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.spec
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true

# Build targets
build:
ifeq ($(OS),Windows_NT)
	$(MAKE) build-windows
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Darwin)
		$(MAKE) build-macos
	else
		$(MAKE) build-linux
	endif
endif

build-windows:
	python build_exe.py

build-macos:
	python build_app.py

build-linux:
	python build_linux.py

build-docker:
	docker build -t enhanced-screenshot-comparison:latest .

# Run targets
run-gui:
	python gui_app.py

run-cli:
	python comp-cli.py

run-console:
	python comparev2.py

# Development targets
test:
	@echo "Running basic import tests..."
	python -c "import gui_app; print('✅ GUI module import OK')"
	python -c "import comparev2; print('✅ Core comparison module import OK')"
	python -c "import comparev2; libs=comparev2.detect_available_libraries(); print(f'✅ Video backends: {libs}')"

lint:
	@echo "Code linting not configured yet"
	@echo "Consider adding flake8, pylint, or black to requirements.txt"

format:
	@echo "Code formatting not configured yet"
	@echo "Consider adding black or autopep8 to requirements.txt"

# Docker targets
docker-build: build-docker

docker-run:
	./docker_helper.sh

docker-clean:
	docker rmi enhanced-screenshot-comparison:latest 2>/dev/null || true
	docker system prune -f

# Platform detection
show-platform:
	@python -c "import platform; print(f'Platform: {platform.system()} {platform.machine()}')"
	@python -c "import sys; print(f'Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"

# Quick start guide
quick-start:
	@echo "Quick Start Guide:"
	@echo ""
	@echo "1. Setup:    make setup"
	@echo "2. Install:  make install"
	@echo "3. Run GUI:  make run-gui"
	@echo "4. Or CLI:   make run-cli"
	@echo ""
	@echo "For Docker:  make docker-build && make docker-run"
