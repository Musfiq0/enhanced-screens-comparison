# 📝 Changelog

All notable changes to the Enhanced Screenshot Comparison Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- **Advanced CLI Mode** - Professional automation interface with comprehensive command-line options
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
