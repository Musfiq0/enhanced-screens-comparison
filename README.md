# 🎬 Enhanced Screenshot Comparison Tool

*Because comparing video quality shouldn't be a pain in the ass* 😤

[![Cross Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Docker-blue?logo=docker)](https://github.com/Musfiq0/enhanced-screens-comparison) 
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://python.org) 
[![Interface](https://img.shields.io/badge/Interface-GUI%20%2B%20CLI%20%2B%20Pro--CLI-orange)](https://github.com/Musfiq0/enhanced-screens-comparison) 
[![Version](https://img.shields.io/badge/Version-3.3-brightgreen)](https://github.com/Musfiq0/enhanced-screens-comparison)


> Ever wanted to compare multiple videos but got tired of writing VapourSynth/AviSynth scripts for each comparison? This tool automates the entire process and even uploads the results to slow.pics automatically! 🚀

## 🎯 What does this thing do?

**TL;DR**: Load videos → Get comparison screenshots → Automatic upload → Share with friends! 📈

- 🖼️ **Automatic screenshot generation** from multiple videos
- 🎨 **Smart cropping** (bye bye black bars!)  
- 📐 **Intelligent resizing** (4K → 1080p without breaking aspect ratios)
- 🌐 **Auto-upload to slow.pics** (and opens in your browser like magic)

📚 **Want the full nerdy details?** Check out our [comprehensive wiki](https://github.com/Musfiq0/enhanced-screens-comparison/wiki) for all the juicy technical stuff, advanced configs, and step-by-step guides that'll make you a comparison wizard! 🧙‍♂️✨

## 🚀 Getting Started (Choose Your Adventure)

### 🎮 I just want it to work (Recommended)
```bash
# Double-click START_HERE.bat and choose your option:
# 1. GUI Application (Point and click)
# 2. Interactive CLI/Console (Guided prompts)
# 3. Advanced CLI (Professional automation) 🆕
# 4. Build Windows Executable

START_HERE.bat
```

### 🤓 I like Python and want to tinker
```bash
git clone https://github.com/Musfiq0/enhanced-screens-comparison.git
cd enhanced-screens-comparison
pip install -r requirements.txt

# GUI Mode (Visual interface)
python gui_app.py

# Interactive CLI Mode (Guided prompts)
python comparev2.py

# Advanced CLI Mode (Professional automation) 🆕
python comp-cli.py -h

### 🔨 I want to build my own because reasons
```bash
pip install -r requirements.txt
python build_exe.py
# Your .exe will appear in the dist/ folder
```

## 💡 How to Use This Thing

### 🖱️ GUI Mode (For humans)

1. **🎯 Configure Comparison Type** (Left section):
   - `Multiple Sources` → Compare different releases of the same anime/content
   - `Source vs Encode` → Compare your encode against the original source

2. **⚡ Execute Actions** (Center-left section):
   - **🎬 Generate**: Create new screenshots with live progress in Results tab
   - **📤 Upload**: Upload existing screenshots to slow.pics

3. **🎮 Manage Videos** (Center-right section):
   - **🗑 Remove**: Delete selected video from comparison
   - **✏ Edit**: Modify video settings (name, crop, resolution)
   - **🗂 Clear All**: Remove all videos from list
   - **⏹ Stop**: Halt current generation process

4. **📊 Monitor Status** (Right section):
   - Real-time progress bar during operations
   - Current operation status display

**📁 Video Loading**
- **🆕 Click or Drag & Drop**: Click the large drop zone or drag video files directly into the app
- Configure each video with descriptive names like "Netflix", "Crunchyroll", "My Encode"
- Select from **comprehensive crop presets** (letterbox removal, streaming logos, dirty lines, etc.)
- Choose target resolution (480p to 4K)

**⚙️ Settings Configuration** (Accessible via gear icon):
- **File Management**: Auto-clear screenshots before/after generation
- **Frame Selection**: Choose interval or specify custom frames  
- **Upload Options**: Enable slow.pics upload with episode naming support
- **Processing**: VapourSynth backend configuration


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

### 🚀 Advanced CLI Mode (v3.0 - Automation) 

**Perfect for batch processing, automation, and power users!**

```bash
# CLI with full feature support
python comp-cli.py [videos] [options]

# Quick examples:
python comp-cli.py video1.mkv video2.mp4                    # Basic comparison
python comp-cli.py *.mkv -cn "My Collection" -u             # Compare all videos and upload
python comp-cli.py source.mkv encode.mkv -f 1000,5000,9000 # Custom frames
```

#### 📝 Complete Syntax Reference

**Basic Usage:**
```bash
python comp-cli.py video1 video2 [video3...] [options]
```

**Global Options:**
```bash
-f, --frames          Frame numbers (e.g., 1000,5000,9000)
-i, --interval        Frame interval in seconds (e.g., 300 for every 5 minutes)
-s, --screenshot-dir  Directory for screenshots (default: Screenshots)
-o, --output-dir      Output directory for comparisons
-cn, --collection-name Collection name for slow.pics upload (required for upload)
-u, --upload          Upload to slow.pics after generation
-uo, --upload-only    Upload existing screenshots (skip generation)
-nc, --no-collage     Generate individual screenshots only (no comparison collage)
-h, --help           Show detailed help and examples
```

**Individual Video Processing:**
```bash
-vc, --video-crops     "x1,y1,x2,y2;x1,y1,x2,y2"    # Crop coordinates per video
-vr, --video-resolutions   "1920x1080;1280x720"          # Target resolution per video  
-ts, --trim-start     FRAMES                         # Trim frames from start per video
-ps, --pad-start      FRAMES                         # Padding frames per video
-vpo, --video-processing-orders    "cf;rf"           # Processing order per video (cf=crop-first, rf=resize-first)
```

**Upload existing screenshots:**
```bash
python comp-cli.py -uo \
  -cn "Previous Comparison" \
  -sd "old_screenshots"
```

#### ⚠️ Important Notes
- **Individual processing**: Use semicolon `;` to separate values for multiple videos
- **Collection name**: Required for uploads, should describe your comparison
- **Frame selection**: Either use `--frames` OR `--interval`, not both
- **Upload-only**: Skips generation, uploads existing screenshots from specified directory
- **Error handling**: Comprehensive validation with clear error messages

#### 🔄 Integration with GUI/Console
- **Same processing engine**: Uses VapourSynth backend like GUI/Console modes
- **Compatible output**: Screenshots work with all modes  
- **Shared configuration**: Uses same crop presets and processing logic



## 🤝 Contributing

Found a bug? Want a feature? Have a better idea?
1. Fork it
2. Fix it  
3. Send a PR
4. ??? 
5. Profit!

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

## 🆕 Recent Updates

### Version 3.2 - GUI Redesign & UX Improvements 🎨

**🎛️ Complete Interface Overhaul**
- ✅ **Unified Control Panel** - Consolidated all controls into a single top panel with four labeled sections
- ✅ **Comparison Type Panel** - Clear radio button selection for Multiple Sources vs Source vs Encode
- ✅ **Actions Panel** - Primary operations (🎬 Generate, 📤 Upload) with instant Results tab switching  
- ✅ **Video Management Panel** - Compact 2x2 grid layout: 🗑 Remove, ✏ Edit, 🗂 Clear All, ⏹ Stop
- ✅ **Status Panel** - Dedicated progress bar and status display for clear operation feedback

**🎯 User Experience Enhancements**
- ✅ **Clickable Drop Zone** - Large, prominent file selection area (click OR drag-and-drop)
- ✅ **Settings Dialog** - All settings moved to clean modal window accessible via ⚙ Settings button
- ✅ **Visual Icon System** - Descriptive icons on every button for immediate recognition
- ✅ **Space Optimization** - Maximum space allocated to video list, streamlined top controls
- ✅ **Instant Operation Feedback** - Generate/Upload automatically switch to Results tab with live progress
- ✅ **Professional Design** - Modern layout with proper spacing, visual hierarchy, and clean aesthetics
- ✅ **Responsive Layout** - Optimal control arrangement that scales with window size
- ✅ **Removed Clutter** - Eliminated Add Video button, moved settings out of tabs for cleaner interface

## ⚖️ License

Do whatever you want with this code, just don't blame me if it breaks something. Also, make sure you have the rights to the videos you're processing (don't be that person).

---

**Made with ❤️ and lots of ☕ by someone who got tired of manual screenshot comparisons**

*P.S. - If this tool saved you time, consider starring the repo. It makes me feel good about my life choices.* ⭐

---
