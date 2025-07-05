# 🎬 Enhanced Screenshot Comparison Tool

*Because comparing video quality shouldn't be a pain in the ass* 😤

[![Windows](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)](https://github.com) 
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://python.org) 
[![GUI](https://img.shields.io/badge/Interface-GUI%20%2B%20CLI-orange)](https://github.com) 
[![Quality](https://img.shields.io/badge/Quality-Actually%20Good-brightgreen)](https://github.com)

> Ever wanted to compare your anime encodes but got tired of opening 47 different video players and taking manual screenshots? This tool does it all for you and even uploads the results to slow.pics automatically! 🚀

## 🎯 What does this thing do?

**TL;DR**: Drag videos → Get comparison screenshots → Automatic upload → Share with friends → Profit! 📈

- 🖼️ **Automatic screenshot generation** from multiple videos
- 🎨 **Smart cropping** (bye bye black bars!)  
- 📐 **Intelligent resizing** (4K → 1080p without breaking aspect ratios)
- 🌐 **Auto-upload to slow.pics** (and opens in your browser like magic)
- 🎭 **GUI for normies, CLI for pros** 
- ⚡ **Actually fast** (when you have good hardware)

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

# Advanced stuff for pros
python comparev2.py --mode multiple-sources --trim-start 100
python comparev2.py --custom-frames 1000 2000 3000
python comparev2.py --help  # When all else fails
```

## 🎨 Cool Features That Actually Work

### 🔧 Smart Video Processing
- **Crop Presets Galore**: Remove letterbox, pillarbox, streaming logos, dirty lines
- **Resolution Magic**: Handles everything from potato quality to 4K without breaking
- **Aspect Ratio Respect**: Won't stretch your waifus (that would be a crime)
- **Trim & Pad**: Cut out intros/outros or sync videos that are slightly off

### 🎮 User Experience That Doesn't Suck  
- **Professional Launcher**: START_HERE.bat with complete menu system
- **Dual Interface**: Choose GUI for ease or CLI for power
- **One-Click Stop**: Panic button that actually works
- **Progress Bars**: So you know it's not frozen
- **Scrollable Everything**: Works on your tiny laptop screen
- **No Installation Hell**: Just download and run
- **Smart Dependencies**: Automatic library checking and installation

### 🌐 Upload Integration
- **Auto slow.pics**: Generates comparison page and opens in browser
- **Smart File Matching**: Figures out which screenshots belong together
- **Retry Logic**: Because the internet is unreliable

## 🛠️ Technical Stuff (For the Curious)

### Processing Backends
- **VapourSynth**: The good stuff (optional, but recommended for quality)
- **OpenCV**: Reliable workhorse (included)
- **PIL**: Basic but gets the job done (fallback)

### What it Supports
- **Input**: Pretty much any video format (MP4, MKV, AVI, etc.)
- **Output**: High-quality PNG screenshots  
- **Platforms**: Windows 10/11 (sorry Linux users, PRs welcome 😅)

## 🐛 When Things Go Wrong

### "It's not working!"
1. **Use START_HERE.bat** for the best experience (handles dependencies automatically)
2. Check if you have videos in a supported format
3. Make sure you have enough disk space
4. Try the CLI version (option 2) if GUI has issues
5. Try turning it off and on again (seriously)

### "VapourSynth errors everywhere!"
- Don't panic, it'll fall back to OpenCV
- Install VapourSynth properly if you want the best quality
- Check `python comparev2.py --demo` to see what's detected

### "Upload failed!"
- Check your internet connection  
- Use the "Upload Existing" button to retry
- slow.pics might be having a bad day

### "My screenshots look terrible!"
- Install VapourSynth for better quality
- Check your source videos aren't corrupted
## 🎉 Recent Cool Stuff Added

- ✅ **Enhanced START_HERE.bat launcher** with complete menu system
- ✅ **CLI option integration** - Easy access to console version via menu
- ✅ **Complete crop preset overhaul** (now with ALL the formats)
- ✅ **Resize-first processing** (crop values work consistently)  
- ✅ **Better error handling** (fewer random crashes)
- ✅ **Improved UI** (less ugly, more functional)
- ✅ **Fixed aspect ratios** (no more stretched anime girls)

### 🚀 New Launcher Features
- **Complete Menu System**: 10 organized options covering all functionality
- **CLI Integration**: Direct access to console version from main menu
- **Smart Dependencies**: Automatic checking and installation of required packages
- **Professional Layout**: Clean ASCII art and logical option grouping
- **Build Integration**: Complete build system accessible from menu
- **Maintenance Tools**: Built-in cleanup and dependency management

## 📁 Project Structure

```
📦 Enhanced-Screenshot-Comparison-Tool/
├── 🎬 comparev2.py              # Enhanced CLI with colored output and robust processing
├── 🖼️ gui_app.py                # GUI application with modern interface
├── 📋 requirements.txt          # Python dependencies
├── 🔨 build_exe.py              # Executable builder script
├── 📄 screenshot_comparison.spec # PyInstaller configuration
├── 📝 version_info.txt          # Version metadata for builds
├── 🎯 icon.ico                  # Application icon
├── 🚀 START_HERE.bat            # Main launcher with complete menu system
├── 🏃 run_gui.bat               # Direct GUI launcher
├── ⚒️ build.bat                 # Build script for executable
├── 📖 README.md                 # This documentation
├── 📜 LICENSE                   # License information
├── 📊 PROJECT_STRUCTURE.md      # Detailed project documentation
├── 📸 Screenshots/              # Generated screenshots folder
│   └── [Video_Name]/            # Organized by video source
├── 🗂️ __pycache__/              # Python cache files
└── 📦 dist/                     # Built executable (after building)
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
│   ├── comparev2.py              # Enhanced CLI comparison engine with multi-backend support
│   ├── gui_app.py                # GUI application with modern interface
│   └── icon.ico                  # Application icon
├── 🔨 Build System  
│   ├── build_exe.py              # Executable builder with PyInstaller
│   ├── screenshot_comparison.spec # PyInstaller configuration file
│   ├── version_info.txt          # Version metadata for Windows builds
│   └── build.bat                 # Batch script for building executable
├── 📦 Dependencies & Config
│   ├── requirements.txt          # All Python dependencies
│   ├── LICENSE                   # Project license
│   └── PROJECT_STRUCTURE.md      # Detailed project documentation
├── 🚀 Quick Launch
│   ├── START_HERE.bat            # Main launcher with complete menu system
│   └── run_gui.bat               # Direct GUI launcher with dependency checking
├── 📸 Output & Cache
│   ├── Screenshots/              # Generated screenshots organized by source
│   ├── __pycache__/              # Python bytecode cache
│   └── dist/                     # Built executable output (after building)
└── 📖 Documentation
    └── README.md                 # Complete user guide and documentation
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

### Professional Workflow
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
- ✅ **Enhanced launcher system** with professional menu and CLI integration
- ✅ **Complete crop preset system** with all common video formats
- ✅ **Resize-first processing** for consistent crop behavior  
- ✅ **Enhanced resolution support** from SD to 4K with proper scaling
- ✅ **Smart aspect ratio handling** prevents image distortion
- ✅ **Improved error handling** with comprehensive validation
- ✅ **Better UI responsiveness** with scrollable dialogs
- ✅ **Fixed Pillow warnings** for modern compatibility

### Stability Improvements
- ✅ **Thread-safe stop function** with instant response
- ✅ **Robust file handling** with proper cleanup
- ✅ **Enhanced upload reliability** with better error recovery
- ✅ **Console compatibility** with all Windows encodings
- ✅ **Memory optimization** for large video processing

## 📝 License

This project is provided as-is for educational and personal use. Please ensure you have the right to process and compare the video files you use with this tool.

---

**Enhanced Screenshot Comparison Tool** - Professional video comparison made simple.

For questions, issues, or contributions, please refer to the project repository.
