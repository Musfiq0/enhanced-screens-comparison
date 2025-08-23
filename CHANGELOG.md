# 📝 Changelog

All notable changes to the Enhanced Screenshot Comparison Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.5.1] - 2025-08-23

### 🔧 Fixed
- **NumPy CPU Dispatcher Error** - Fixed "RuntimeError: CPU dispatcher tracer already initialized" that specifically occurred during Source vs Encode comparisons in PyInstaller-built executables
- **PyInstaller Runtime Hook** - Created dedicated runtime hook (`pyi_rth_numpy_fix.py`) to handle NumPy initialization conflicts in frozen environments  
- **Lazy Import System** - Replaced direct NumPy imports in VapourSynth processor methods with global references to prevent multiple initialization attempts
- **Screenshot Generation** - Fixed crashes during frame extraction and PNG saving processes that use NumPy arrays
- **Environment Variables** - Added proper NPY_DISABLE_CPU_FEATURES setup in runtime hook to prevent CPU dispatcher conflicts

### 🎯 Improved
- **Error Handling** - Enhanced NumPy import error handling with CPU dispatcher-specific detection and recovery
- **Build Configuration** - Updated PyInstaller spec file and build scripts to include the new runtime hook automatically
- **Testing Coverage** - Added comprehensive tests for Source vs Encode scenarios to verify NumPy compatibility
- **Code Robustness** - Implemented consistent lazy loading pattern for NumPy usage across all video processing backends

### 📝 Technical Details
- **Runtime Hook**: Created `hooks/pyi_rth_numpy_fix.py` that executes before main application to configure NumPy environment
- **Fixed Methods**: Updated `VapourSynthProcessor.get_frame()`, `VapourSynthProcessor.save_frame_as_png()`, and frame preview functions
- **Environment Setup**: Added early NPY_DISABLE_CPU_FEATURES and KMP_DUPLICATE_LIB_OK configuration for PyInstaller compatibility
- **Import Strategy**: Replaced `import numpy as np` with global `np` references using the centralized `try_import_numpy()` function

## [3.5.0] - 2025-08-06

### 🚀 Added
- **Video Preview** - Enhanced video preview system across multiple videos
- **Mouse Side Button Navigation** - Quick video switching using mouse side buttons (Button-4/Button-5) for improved workflow
- **CLI Preview Integration** - Embedded GUI preview window accessible via `--preview` flag in CLI mode
- **Console Preview Fallback** - Simple text-based frame navigation for systems without GUI support
- **Cross-Platform Mouse Support** - Universal mouse button compatibility across Windows, macOS, and Linux

### 🎯 Improved
- **Preview System Architecture** - Unified preview infrastructure across GUI, CLI, and console modes
- **Error Handling** - Comprehensive try-catch blocks around mouse button bindings and preview operations
- **Graceful Fallbacks** - Automatic degradation from GUI preview to console-based navigation when needed
- **User Experience** - Consistent preview functionality regardless of interaction mode (GUI/CLI/console)

### 🔄 Changed
- **CLI Preview Implementation** - Now uses GUI components with console fallback instead of separate CLI-only preview
- **Function Organization** - Moved preview functions to proper location in code for correct definition order

### 🔒 Security
- **Enhanced Error Handling** - Added safety try-catch blocks to prevent crashes from unsupported mouse button events
- **Robust Fallback System** - Multiple layers of error handling ensure application continues functioning even if preview components fail

## [3.4.0] - 2025-08-02

### 🚀 Added
- **Large Upload Support** - Automatic chunking system for uploads with 500+ images
- **Smart Retry Logic** - Exponential backoff retry mechanism for failed uploads
- **Rate Limiting Detection** - Automatic detection and handling of slow.pics rate limits
- **Enhanced Error Handling** - Comprehensive error messages with actionable guidance

### 🔧 Fixed
- **Frame Detection Accuracy** - Improved PNG filename parsing to handle `SourceName_000000.png` format reliably
- **Upload Reliability** - Fixed 500 Internal Server Error issues with large batch uploads
- **Fallback Frame Detection** - Added regex-based fallback for edge case filename formats
- **Memory Optimization** - Better handling of large image collections to prevent memory issues

### 🎯 Improved
- **Upload Strategy** - Intelligent chunking: tries single upload first, then falls back to 3-5 optimized chunks
- **Progress Feedback** - Enhanced upload progress reporting across GUI, CLI, and console interfaces
- **Error Recovery** - Graceful handling of network timeouts and server errors
- **User Experience** - Consistent frame detection and upload behavior across all interfaces

### 🔄 Changed
- **Upload Function** - Unified `upload_to_slowpics()` function with enhanced capabilities used across all interfaces
- **Frame Processing** - Standardized frame detection logic across GUI, CLI, and core modules

## [3.3.0] - 2025-07-XX

### 🚀 Added
- **Cross Platform Compatibility** - Full support for Windows, macOS, and Linux operating systems
- **Docker Support** - Containerized deployment option for consistent cross-platform execution
- **Platform-Specific Build Scripts** - Automated build processes for different operating systems

## [3.2.0] - 2025-06-XX

### 🎨 GUI Redesign & UX Improvements

#### 🎛️ Complete Interface Overhaul
- **Unified Control Panel** - Consolidated all controls into a single top panel with four labeled sections
- **Comparison Type Panel** - Clear radio button selection for Multiple Sources vs Source vs Encode
- **Actions Panel** - Primary operations (🎬 Generate, 📤 Upload) with instant Results tab switching  
- **Video Management Panel** - Compact 2x2 grid layout: 🗑 Remove, ✏ Edit, 🗂 Clear All, ⏹ Stop
- **Status Panel** - Dedicated progress bar and status display for clear operation feedback

#### 🎯 User Experience Enhancements
- **Clickable Drop Zone** - Large, prominent file selection area (click OR drag-and-drop)
- **Settings Dialog** - All settings moved to clean modal window accessible via ⚙ Settings button
- **Visual Icon System** - Descriptive icons on every button for immediate recognition
- **Space Optimization** - Maximum space allocated to video list, streamlined top controls
- **Instant Operation Feedback** - Generate/Upload automatically switch to Results tab with live progress
- **Professional Design** - Modern layout with proper spacing, visual hierarchy, and clean aesthetics
- **Responsive Layout** - Optimal control arrangement that scales with window size
- **Removed Clutter** - Eliminated Add Video button, moved settings out of tabs for cleaner interface

---

## 📋 Legend

- 🚀 **Added** - New features
- 🔧 **Fixed** - Bug fixes
- 🎯 **Improved** - Enhancements to existing features
- 🔄 **Changed** - Changes in existing functionality
- 🗑️ **Removed** - Deprecated features
- 🔒 **Security** - Security improvements
