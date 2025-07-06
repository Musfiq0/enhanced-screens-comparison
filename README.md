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

📚 **Want the full nerdy details?** Check out our [comprehensive wiki](https://github.com/Musfiq0/enhanced-screens-comparison/wiki) for all the juicy technical stuff, advanced configs, and step-by-step guides that'll make you a comparison wizard! 🧙‍♂️✨

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

## 🛠️ Technical Stuff (For the Curious)

### Processing Backends
- **VapourSynth**: The good stuff (optional, but recommended for quality)
- **OpenCV**: Reliable workhorse (included)
- **PIL**: Basic but gets the job done (fallback)

### What it Supports
- **Input**: Pretty much any video format (MP4, MKV, AVI, etc.)
- **Output**: High-quality PNG screenshots  
- **Platforms**: Windows 10/11 (sorry Linux users, PRs welcome 😅)


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

## ⚖️ License

Do whatever you want with this code, just don't blame me if it breaks something. Also, make sure you have the rights to the videos you're processing (don't be that person).

---

**Made with ❤️ and lots of ☕ by someone who got tired of manual screenshot comparisons**

*P.S. - If this tool saved you time, consider starring the repo. It makes me feel good about my life choices.* ⭐

---
