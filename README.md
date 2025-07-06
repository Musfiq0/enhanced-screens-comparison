# 🎬 Enhanced Screenshot Comparison Tool

*Because comparing video quality shouldn't be a pain in the ass* 😤

[![Windows](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)](https://github.com) 
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://python.org) 
[![GUI](https://img.shields.io/badge/Interface-GUI%20%2B%20CLI-orange)](https://github.com) 
[![Quality](https://img.shields.io/badge/Quality-Actually%20Good-brightgreen)](https://github.com)

> Ever wanted to compare multiple videos but got tired of writing VapourSynth/AviSynth scripts for each comparison? This tool automates the entire process and even uploads the results to slow.pics automatically! 🚀

## 🎯 What does this thing do?

**TL;DR**: Load videos → Get comparison screenshots → Automatic upload → Share with friends! 📈

- 🖼️ **Automatic screenshot generation** from multiple videos
- 🎨 **Smart cropping** (bye bye black bars!)  
- 📐 **Intelligent resizing** (4K → 1080p without breaking aspect ratios)
- 🌐 **Auto-upload to slow.pics** (and opens in your browser like magic)
- 🎭 **GUI for normies, Console for nerds** 
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
git clone https://github.com/Musfiq0/enhanced-screens-comparison.git
cd enhanced-screens-comparison
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
2. **Configure settings** in the Settings tab:
   - **File Management**: Auto-clear screenshots before/after generation
   - **Frame Selection**: Choose interval or custom frames
   - **Upload Options**: Enable slow.pics upload with episode support
3. **Pick your poison**:
   - `Multiple Sources` → Compare different releases of the same anime
   - `Source vs Encode` → Compare your encode against the original
4. **Add videos** → Choose your method:
   - **🆕 Drag & Drop**: Simply drag video files from Windows Explorer into the app
   - **Classic Method**: Click "Add Video" button and browse for files
   - Configure each video with nice names like "Netflix" or "My Trash Encode"
   - Pick from **tons of crop presets** (letterbox, streaming logos, dirty lines, etc.)
   - Choose target resolution (480p to 4K because why not)
5. **Hit Generate** → Watch the magic happen ✨
6. **Get results** → Screenshots saved locally + auto-uploaded to slow.pics with proper naming

#### 🆕 New Drag & Drop Features
- **Persistent Drop Zone**: Drag area stays visible for adding multiple videos
- **Smart File Detection**: Automatically validates video formats (MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V)
- **Auto Configuration**: Configuration dialog opens automatically for each dropped video
- **Multiple File Support**: Drop several videos at once - each gets its own configuration
- **Visual Feedback**: Drop zone changes appearance during drag operations
- **Progress Tracking**: Shows current video count and encourages adding more

### ⌨️ Console Mode (For the command line warriors)

```bash
# Easy way: Use the launcher
START_HERE.bat
# Choose option 2: Run Console Version

# Direct way: Interactive mode (asks you questions like a friendly robot)
python comparev2.py

# Quick help and info
python comparev2.py --help       # Show usage information
python comparev2.py --demo       # Show detected video processing backends
python comparev2.py --version    # Show version information
```
**Example Console Output:**
```
[INFO] Detecting available video processing libraries...
[OK] VapourSynth detected and imported successfully
[OK] awsmfunc detected and imported successfully
[MODE] Using VapourSynth mode (high-quality video processing)

[🎬] Starting Multiple Sources processing...
[🔄] Processing frame 5000 (1/10) - 10.0%
[🔄] Processing frame 10000 (2/10) - 20.0%
[📊] Screenshot generation complete:
[✅] Successfully generated: 20/20
```

## 🎨 Cool Features That Actually Work

### 🔧 Smart Video Processing
- **Crop Presets Galore**: Remove letterbox, pillarbox, streaming logos, dirty lines
- **Resolution Magic**: Handles everything from potato quality to 4K without breaking
- **Aspect Ratio Respect**: Won't stretch your waifus (that would be a crime)
- **Trim & Pad**: Cut out intros/outros or sync videos that are slightly off

### 🎮 User Experience That Doesn't Suck  
- **🆕 Drag & Drop Interface**: Drag videos directly from Windows Explorer - no more clicking through folders
- **Persistent Drop Zone**: Add multiple videos easily with visual feedback and progress tracking
- **File Management**: Auto-clear screenshots folder before/after generation
- **Episode Support**: Dedicated options for single episodes vs season packs
- **Launcher**: START_HERE.bat with complete menu system
- **Dual Interface**: Choose GUI for ease or CLI for power
- **One-Click Stop**: Panic button that actually works
- **Progress Bars**: So you know it's not frozen
- **Scrollable Everything**: Works on your tiny laptop screen
- **No Installation Hell**: Just download and run
- **Smart Dependencies**: Automatic library checking and installation

### 🌐 Upload Integration
- **Auto slow.pics**: Generates comparison page and opens in browser
- **Episode Support**: Choose between single episode or season pack uploads
- **Smart Collection Names**: Automatic naming like "ShowName S01E01 source vs encode"
- **File Management**: Auto-clear screenshots before generation or after upload
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
- **🆕 Drag & Drop**: Native Windows drag and drop support via tkinterdnd2

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

- ✅ **Episode Support for slow.pics** - Single episode vs season pack upload options
- ✅ **File Management Options** - Auto-clear screenshots before/after generation
- ✅ **Dynamic Processing Display** - Shows actual processing steps in console
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
- **Cool Layout**: Clean ASCII art and logical option grouping
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

### Version 2.1 Features  
- ✅ **🆕 Drag & Drop Support** - Simply drag video files from Windows Explorer into the GUI
- ✅ **Persistent Drop Zone** - Drag area remains visible for adding multiple videos easily
- ✅ **Smart File Validation** - Automatic detection of valid video formats with helpful error messages
- ✅ **Auto Configuration** - Configuration dialog opens automatically for each dropped video
- ✅ **Multiple File Handling** - Drop several videos at once with individual configuration
- ✅ **Visual Feedback** - Dynamic drop zone appearance with clear instructions and status
- ✅ **Robust File Parsing** - Handles various path formats and edge cases from different applications
- ✅ **Episode Support for slow.pics uploads** - Choose between single episode and season pack
- ✅ **Smart Collection Naming** - Automatic "ShowName S01E01 source vs encode" format
- ✅ **File Management Options** - Auto-clear screenshots before generation or after upload
- ✅ **Dynamic Processing Display** - Console shows actual processing steps instead of static text
- ✅ **Custom Frames Fallback** - Uses default frames (100,500,1000) instead of switching to interval

### Version 2.0 Features
- ✅ **Enhanced launcher system** with interactive menu and CLI integration
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

**Enhanced Screenshot Comparison Tool** - Hassle-free video comparison.

For questions, issues, or contributions, please refer to the project repository.
