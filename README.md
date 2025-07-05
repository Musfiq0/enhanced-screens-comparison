# 🎬 Enhanced Screenshot Comparison Tool

*Because comparing video quality shouldn't be a pain in the ass* 😤

[![Windows](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)](https://github.com) 
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://python.org) 
[![GUI](https://img.shields.io/badge/Interface-GUI%20%2B%20CLI-orange)](https://github.com) 
[![Quality](https://img.shields.io/badge/Quality-Actually%20Good-brightgreen)](https://github.com)

> Ever wanted to compare your encodes but got tired of manually writing VapourSynth/AviSynth scripts for every single screenshot comparison? This tool automates the tedious screenshot workflow and uploads everything to slow.pics automatically! 🚀

## 🎯 What does this thing do?

**TL;DR**: Load videos → Automated VapourSynth processing → Bulk screenshot generation → Auto-upload to slow.pics → No more manual script writing!

- 🖼️ **Automatic screenshot generation** from multiple videos
- 🎨 **Smart cropping** (bye bye black bars!)  
- 📐 **Intelligent resizing** (4K → 1080p without breaking aspect ratios)
- 🌐 **Auto-upload to slow.pics** (and opens in your browser like magic)
- 🎭 **GUI for normies, CLI for pros** 
- ⚡ **Actually fast** (when you have good hardware)
- 🔧 **Multi-backend support** (VapourSynth, OpenCV, PIL with automatic fallback)
- 🎪 **Beautiful console interface** with colored output and progress tracking

## 🚀 Getting Started (Choose Your Adventure)

### 🎮 I just want it to work (Recommended)
```bash
# Double-click START_HERE.bat and choose your option:
# 1. GUI Application (Point and click)
# 2. CLI/Console Version (Command line)
# 4. Build Windows Executable

START_HERE.bat
```

### 🤓 I like Python and want to tinker
```bash
git clone https://github.com/your-repo/Enhanced-Screenshot-Comparison-Tool
cd Enhanced-Screenshot-Comparison-Tool
pip install -r requirements.txt

# GUI Mode
python gui_app.py

# CLI Mode  
python comparev2.py
```

### 🔨 I want to build my own because reasons
```bash
pip install -r requirements.txt
python build_exe.py
# Your .exe will appear in the dist/ folder
```

## 💡 How to Use This Thing

### 🖱️ GUI Mode (For humans)

1. **Launch the app** (wow, such difficulty)
2. **Pick your poison**:
   - `Multiple Sources` → Compare different releases of the same anime
   - `Source vs Encode` → Compare your encode against the original
3. **Add videos** → Click "Add Video" and configure them:
   - Give them nice names like "Netflix" or "My Trash Encode"
   - Pick from **tons of crop presets** (letterbox, streaming logos, dirty lines, etc.)
   - Choose target resolution (480p to 4K because why not)
4. **Hit Generate** → Watch the magic happen ✨
5. **Get results** → Screenshots saved locally + auto-uploaded to slow.pics

### ⌨️ CLI Mode (For the command line warriors)

```bash
# Easy way: Use the launcher
START_HERE.bat
# Choose option 2: Run CLI/Console Version

# Direct way: Interactive mode (asks you questions like a friendly robot)
python comparev2.py

# Quick help and info
python comparev2.py --help       # Show usage information
python comparev2.py --demo       # Show detected video processing backends
python comparev2.py --version    # Show version information
```

**Enhanced Console Features:**
- 🎨 **Beautiful colored output** with progress indicators
- 🔄 **Real-time processing feedback** with percentage completion  
- 🎪 **ASCII art** and status messages
- 🔧 **Automatic backend detection** (VapourSynth → OpenCV → PIL fallback)
- 📊 **Detailed progress tracking** for each video and frame
- 🧹 **Smart cleanup** of existing screenshots before generation

## 🎨 Cool Features That Actually Work

### 🔧 Smart Video Processing
- **Crop Presets Galore**: Remove letterbox, pillarbox, streaming logos, dirty lines
- **Resolution Magic**: Handles everything from potato quality to 4K without breaking
- **Aspect Ratio Respect**: Won't stretch your waifus (that would be a crime)
- **Trim & Pad**: Cut out intros/outros or sync videos that are slightly off
- **Multi-Backend Support**: VapourSynth (premium quality) → OpenCV (reliable) → PIL (fallback)
- **Robust Error Handling**: Graceful fallback when backends fail
- **Smart Screenshot Generation**: Automatic cleanup and organized output

### 🎮 User Experience That Doesn't Suck  
- **Quick Launcher**: START_HERE.bat with complete menu system
- **Dual Interface**: Choose GUI for ease or CLI for power
- **One-Click Stop**: Panic button that actually works
- **Progress Bars**: So you know it's not frozen
- **Scrollable Everything**: Works on your tiny laptop screen
- **Smart Dependencies**: Automatic library checking and installation

### 🌐 Upload Integration
- **Auto slow.pics**: Generates comparison page and opens in browser
- **Smart File Matching**: Figures out which screenshots belong together
- **Retry Logic**: Because the internet is unreliable

## 🛠️ Technical Stuff (For the Curious)

### Processing Backends
- **VapourSynth**: The premium choice (high-quality processing with awsmfunc support)
- **OpenCV**: The reliable workhorse (fast and stable for most use cases) [Yet to be worked on]
- **PIL**: The universal fallback (works everywhere, basic functionality) [Yet to be worked on]

**Smart Backend Selection**: The tool automatically detects available libraries and uses the best one available. Check what's detected with `python comparev2.py --demo`

### What it Supports
- **Input**: Pretty much any video format (MP4, MKV, AVI, etc.)
- **Output**: High-quality PNG screenshots  
- **Platforms**: Windows 10/11 (sorry Linux users, PRs welcome 😅)

## 🎭 Examples That Actually Help

### Various Streaming Sources Comparison
```bash
# Compare different anime releases
python comparev2.py --mode multiple-sources
# Add: Netflix rip, Amazon rip, Crunchyroll rip
# Result: Beautiful comparison showing quality differences
```

### Encode Quality Check  
```bash
# See if your encode is trash
python comparev2.py --mode source-vs-encode
# Add: Original BD rip vs Your compressed version
# Result: Detailed comparison to cry about compression artifacts
```

### Custom Frame Analysis
```bash
# Check specific scenes
python comparev2.py --custom-frames 5000 10000 15000
# Perfect for comparing action scenes or specific moments
```

## 🎪 Console Experience

The enhanced CLI version now features a interactive console interface:

### 📊 Progress Tracking
- **Real-time Updates**: See exactly what's happening as it happens
- **Percentage Progress**: Know how much work is left
- **Frame-by-Frame Status**: Track individual screenshot generation
- **Backend Information**: Clear indication of which processing mode is active

### 🔧 Smart Backend Detection
```bash
# Check what's available on your system
python comparev2.py --demo

# Example output:
# [OK] VapourSynth: Available  
# [OK] OpenCV: Available
# [OK] PIL/Pillow: Available
# [MODE] Active Processing Mode: VAPOURSYNTH
```

## 🐛 When Things Go Wrong

### "It's not working!"
1. **Use START_HERE.bat** for the best experience (handles dependencies automatically)
2. Check if you have videos in a supported format
3. Make sure you have enough disk space
4. Try the CLI version (option 2) if GUI has issues
5. Try turning it off and on again (seriously)

### "VapourSynth errors everywhere!"
- Don't panic! The tool automatically falls back to OpenCV, then PIL
- Install VapourSynth properly if you want the best quality
- Check `python comparev2.py --demo` to see what backends are detected
- All console output is color-coded to help identify the active backend

### "Upload failed!"
- Check your internet connection  
- Use the "Upload Existing" button to retry
- slow.pics might be having a bad day

### "My screenshots look terrible!"
- Install VapourSynth for better quality
- Check your source videos aren't corrupted
## 🎉 Recent Cool Stuff Added

- ✅ **Complete console version rework** with robust screenshot generation
- ✅ **Multi-backend fallback system** (VapourSynth → OpenCV → PIL)
- ✅ **Beautiful colored console output** with real-time progress tracking
- ✅ **Enhanced START_HERE.bat launcher** with complete menu system
- ✅ **CLI option integration** - Easy access to console version via menu
- ✅ **Complete crop preset overhaul** (now with ALL the formats)
- ✅ **Resize-first processing** (crop values work consistently)  
- ✅ **Better error handling** (fewer random crashes)
- ✅ **Improved UI** (less ugly, more functional)
- ✅ **Fixed aspect ratios** (no more stretched anime girls)
- ✅ **GUI-Console compatibility** - Both versions work independently

### 🚀 Launcher Features
- **Complete Menu System**: 10 organized options covering all functionality
- **CLI Integration**: Direct access to console version from main menu
- **Smart Dependencies**: Automatic checking and installation of required packages
- **Cool Layout**: Clean ASCII art and logical option grouping
- **Build Integration**: Complete build system accessible from menu
- **Maintenance Tools**: Built-in cleanup and dependency management

## 📁 Project Structure

```
📦 Your Download
├── 🎬 comparev2.py          # Enhanced CLI with colored output and robust processing
├── 🖼️ gui_app.py            # GUI for point-and-click folks  
├── 📋 requirements.txt      # What Python needs to not explode
├── 🔨 build_exe.py          # Makes the .exe file
├── 🚀 START_HERE.bat        # Main launcher with menu (GUI + CLI)
├── 🏃 run_gui.bat           # Direct GUI launcher
└── 📸 Screenshots/          # Where your results live
```

## 🤝 Contributing

Found a bug? Want a feature? Have a better idea?
1. Fork it
2. Fix it  
3. Send a PR
4. ??? 
5. Profit!

## ⚖️ License

Do whatever you want with this code, just don't blame me if it breaks something. Also, make sure you have the rights to the videos you're processing (don't be that person).

---

**Made with ❤️ and lots of ☕ by someone who got tired of manual screenshot comparisons**

*P.S. - If this tool saved you time, consider starring the repo. It makes me feel good about my life choices.* ⭐

### Standard Build
```bash
# Install all dependencies
pip install -r requirements.txt

# Build executable
python build_exe.py

# Or use batch file
build.bat
```

### Advanced Build Options
```bash
# Build with custom options
pyinstaller screenshot_comparison.spec

# Check build requirements
python -c "import PyInstaller; print('PyInstaller ready')"
```

## 📁 File Structure

```
Enhanced-Screenshot-Comparison-Tool/
├── 📋 Core Application
│   ├── comparev2.py              # CLI comparison engine
│   ├── gui_app.py                # GUI application
│   └── icon.ico                  # Application icon
├── 🔨 Build System  
│   ├── build_exe.py              # Executable builder
│   ├── screenshot_comparison.spec # PyInstaller config
│   ├── version_info.txt          # Version metadata
│   └── build.bat                 # Build script
├── 📦 Dependencies
│   └── requirements.txt          # All dependencies
├── 🚀 Quick Launch
│   ├── START_HERE.bat            # Main launcher with complete menu
│   └── run_gui.bat              # Direct GUI launcher  
├── 📸 Output
│   ├── dist/                    # Built executable
│   └── Screenshots/             # Generated screenshots
└── 📖 Documentation
    └── README.md                # This file
```

## 🎯 Key Features Explained

### Smart Crop Presets
The tool includes professionally-designed crop presets for every common scenario:

- **Cinema Formats**: Perfect letterbox removal for 2.40:1, 2.35:1, 1.85:1 content
- **Streaming Services**: Logo removal presets for major platforms
- **Technical Corrections**: Dirty line removal, overscan correction
- **Format Conversion**: 4:3 to 16:9 pillarbox handling

### Intelligent Processing
- **Resolution-Aware**: Crop values automatically work across all source resolutions
- **Quality Preservation**: Optimal processing order prevents quality loss
- **Aspect Ratio Maintenance**: Smart resizing maintains proper proportions
- **Format Detection**: Automatic handling of various video formats and codecs

### Workflow
- **Batch Processing**: Handle multiple comparisons efficiently
- **Instant Control**: Stop processing at any time without data loss
- **Progress Monitoring**: Real-time feedback with detailed status information
- **Result Management**: Organized output with direct folder access

## 🐛 Troubleshooting

### Common Issues

**Video Loading Errors**
```bash
# Check supported formats
python comparev2.py --demo

# Verify file accessibility
python -c "import cv2; print('OpenCV ready')"
```

**VapourSynth Problems**
```bash
# Check VapourSynth installation
python -c "import vapoursynth; print('VapourSynth available')"

# Application automatically falls back to OpenCV if VapourSynth fails
```

**Upload Issues**
```bash
# Test internet connection
python -c "import requests; print(requests.get('https://slow.pics').status_code)"

# Use "Upload Existing" feature for retry
```

**Build Problems**
```bash
# Verify all dependencies
pip install -r requirements.txt

# Check PyInstaller
python -c "import PyInstaller; print('Build tools ready')"
```

### Performance Tips
- **For 4K videos**: Ensure 8GB+ RAM available
- **For slow processing**: Close other applications
- **For large batches**: Use CLI mode for better performance
- **For best quality**: Install VapourSynth system-wide

## 🆕 Recent Updates

### Version 2.0 Features
- ✅ **Completely reworked console version** with robust multi-backend support
- ✅ **Beautiful colored console interface** with real-time progress and status
- ✅ **Smart backend detection and fallback** (VapourSynth → OpenCV → PIL)
- ✅ **Enhanced error handling** with graceful degradation
- ✅ **Improved screenshot generation** with automatic cleanup and organization
- ✅ **Enhanced launcher system** with interactive menu and CLI integration
- ✅ **Complete crop preset system** with all common video formats
- ✅ **Resize-first processing** for consistent crop behavior  
- ✅ **Enhanced resolution support** from SD to 4K with proper scaling
- ✅ **Smart aspect ratio handling** prevents image distortion
- ✅ **Better UI responsiveness** with scrollable dialogs
- ✅ **Fixed Pillow warnings** for modern compatibility
- ✅ **GUI-Console independence** - Both versions work flawlessly together

### Stability Improvements
- ✅ **Thread-safe stop function** with instant response
- ✅ **Robust file handling** with proper cleanup
- ✅ **Enhanced upload reliability** with better error recovery
- ✅ **Console compatibility** with all Windows encodings
- ✅ **Memory optimization** for large video processing

## 📝 License

This project is provided as-is for educational and personal use. Please ensure you have the right to process and compare the video files you use with this tool.

---

**Enhanced Screenshot Comparison Tool** - A hassle-free video comparison.

For questions, issues, or contributions, please refer to the project repository.
