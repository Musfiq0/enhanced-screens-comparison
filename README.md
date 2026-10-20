# 🎬 Enhanced Screenshot Comparison Tool

> **Professional video comparison made simple** - Compare multiple video sources with automated screenshot generation and instant sharing.

[![Platform](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)](https://github.com/Musfiq0/enhanced-screens-comparison)
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://python.org)
[![Version](https://img.shields.io/badge/Version-3.6.1-brightgreen)](https://github.com/Musfiq0/enhanced-screens-comparison/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Building](#-building-from-source)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

Enhanced Screenshot Comparison Tool automates the tedious process of comparing multiple video sources. Perfect for:

- 📺 **Streaming Quality** - Compare Netflix, Crunchyroll, Amazon Prime, etc.
- 🎞️ **Video Encoding** - Compare your encodes against source material
- 🔍 **Quality Analysis** - Side-by-side frame comparisons with precise control
- 🌐 **Easy Sharing** - Automatic upload to slow.pics with shareable links

**No more manual screenshot taking or complex scripting required!**

---

## ✨ Features

### Core Functionality
- 🎬 **Multiple Video Support** - Compare unlimited video sources simultaneously
- 🖼️ **Automated Screenshots** - Generate comparison images with one click
- 🎲 **Smart Frame Selection** - Random, interval-based, or custom frame selection
- 🎨 **Intelligent Cropping** - Remove black bars and unwanted borders automatically
- 📐 **Smart Resizing** - Maintain aspect ratios while normalizing resolutions
- 🌐 **Auto-Upload** - Direct upload to slow.pics with instant sharing links

### Video Processing
- ⚡ **VapourSynth Integration** - Professional-grade video processing
- 🔄 **Fallback Support** - Automatic OpenCV fallback when VapourSynth unavailable
- 🎯 **Precise Control** - Frame-accurate processing with trim support
- 📊 **Live Progress** - Real-time progress tracking during generation

### User Experience
- 🖱️ **Drag & Drop** - Intuitive video loading
- ⚙️ **Preset Management** - Common crop presets for streaming services
- 🎛️ **Flexible Interface** - GUI for beginners, CLI for power users
- 💾 **Session Memory** - Saves your settings and preferences

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Musfiq0/enhanced-screens-comparison.git
cd enhanced-screens-comparison

# Install dependencies
pip install -r requirements.txt

# Install VapourSynth (required for video processing)
pip install vapoursynth

# Launch GUI
python gui_app.py

# Or use CLI
python comparev2.py
```

---

## 📥 Installation

### Prerequisites
- **Windows 10/11** (64-bit)
- **Python 3.8+**
- **VapourSynth** (install via pip)

### Setup Instructions

```bash
# 1. Clone repository
git clone https://github.com/Musfiq0/enhanced-screens-comparison.git
cd enhanced-screens-comparison

# 2. Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python gui_app.py          # GUI mode
python comparev2.py        # Interactive CLI
python comp-cli.py --help  # Advanced CLI
```

---

## 💻 Usage

### GUI Mode (Easiest)

**Launch:**
```bash
python gui_app.py
# or
run_gui.bat
```

**Workflow:**
1. **Add Videos** - Drag & drop or click to add video files
2. **Configure** - Set names, crops, and resolutions for each video
3. **Settings** - Choose frame selection method and output options
4. **Generate** - Click Generate to create comparison screenshots
5. **Upload** - Optional: Upload to slow.pics for easy sharing

**Tips:**
- Use preset crops for common streaming services (Netflix, Crunchyroll, etc.)
- Random frame selection automatically picks 30-35 distributed frames
- Enable auto-clear to keep your workspace clean

### Interactive CLI Mode

**Launch:**
```bash
python comparev2.py
```

**Features:**
- Step-by-step guided prompts
- Automatic backend detection (VapourSynth/OpenCV)
- Same powerful processing as GUI
- Perfect for scripting and automation

**Example Session:**
```
[INFO] VapourSynth detected and loaded
[PROMPT] Comparison type: (1) Multiple Sources (2) Source vs Encode
Choice: 1
[PROMPT] Enter video paths (one per line, blank to finish):
video1.mkv
video2.mkv

[PROMPT] Frame selection: (1) Interval (2) Custom (3) Random
Choice: 3
[INFO] Selected 33 random frames across video
[SUCCESS] Generated 33 comparison screenshots
```

### Advanced CLI Mode

**Launch:**
```bash
python comp-cli.py [options] video1 video2 [video3...]
```

**Quick Examples:**
```bash
# Basic comparison
python comp-cli.py source.mkv encode.mkv

# Random frames with upload
python comp-cli.py video1.mkv video2.mkv -cn "My Comparison" -u

# Custom frames
python comp-cli.py video1.mkv video2.mkv -f 1000,5000,9000,15000

# With individual video settings
python comp-cli.py video1.mkv video2.mkv \
  -vr "1920x1080;1920x1080" \
  -vc "0,140,1920,940;0,140,1920,940"
```

**Available Options:**
```
-f, --frames              Custom frame numbers (comma-separated)
-i, --interval            Frame interval in seconds
-cn, --collection-name    Collection name for slow.pics
-u, --upload              Upload after generation
-s, --screenshot-dir      Output directory for screenshots
-vr, --video-resolutions  Target resolutions (semicolon-separated)
-vc, --video-crops        Crop coordinates (semicolon-separated)
-h, --help                Show detailed help
```

---

## 🔨 Development

### Running from Source

This project runs directly from source - no build process required.

```bash
# Clone and setup
git clone https://github.com/Musfiq0/enhanced-screens-comparison.git
cd enhanced-screens-comparison

# Install dependencies
pip install -r requirements.txt

# Run the application
python gui_app.py          # GUI mode
python comparev2.py        # Interactive CLI
python comp-cli.py --help  # Advanced CLI
```

### Development Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python gui_app.py  # Test GUI
python comparev2.py  # Test CLI
```

---

## 📚 Documentation

### Main Documentation
- **[Wiki Home](https://github.com/Musfiq0/enhanced-screens-comparison/wiki)** - Complete documentation
- **[Installation Guide](https://github.com/Musfiq0/enhanced-screens-comparison/wiki/Installation)** - Detailed setup instructions
- **[User Guide](https://github.com/Musfiq0/enhanced-screens-comparison/wiki/User-Guide)** - How to use all features
- **[Building Guide](https://github.com/Musfiq0/enhanced-screens-comparison/wiki/Building)** - Build from source
- **[Troubleshooting](https://github.com/Musfiq0/enhanced-screens-comparison/wiki/Troubleshooting)** - Common issues and solutions

### Additional Resources
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [LICENSE](LICENSE) - MIT License

---

## 🎯 Use Cases

### Streaming Service Comparison
Compare the same anime/show across different platforms:
```
Netflix vs Crunchyroll vs Amazon Prime
→ Which service has the best quality?
```

### Encode Quality Check
Verify your video encodes maintain quality:
```
Original Source vs Your Encode
→ Did compression introduce artifacts?
```

### Release Comparison
Compare different release groups:
```
Group A vs Group B vs Group C
→ Which release is better?
```

### Frame-by-Frame Analysis
Examine specific scenes across sources:
```
Custom frame selection at key moments
→ Detailed quality analysis
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Report Bugs** - Open an issue with details
- 💡 **Suggest Features** - Share your ideas in discussions
- 📝 **Improve Docs** - Help make documentation clearer
- 🔧 **Submit PRs** - Fix bugs or add features

### Development Setup
```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/enhanced-screens-comparison.git
cd enhanced-screens-comparison

# Create branch
git checkout -b feature/your-feature-name

# Make changes and test
python gui_app.py  # Test GUI
python comparev2.py  # Test CLI

# Commit and push
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Project Stats

- **Lines of Code:** ~6,000+
- **Supported Formats:** MP4, MKV, AVI, MOV, and more
- **Processing Engines:** VapourSynth + OpenCV
- **Target Platforms:** Windows 10/11 (64-bit)

---

## 🐛 Troubleshooting

### Common Issues

**Application won't start:**
```bash
# Check Python version
python --version  # Should be 3.8+

# Verify dependencies
pip install -r requirements.txt

# Run with error output
python gui_app.py
```

**VapourSynth not working:**
```bash
# Check VapourSynth installation
python -c "import vapoursynth; print('OK')"

# Application automatically falls back to OpenCV
```

**Upload fails:**
```bash
# Check internet connection
# Verify slow.pics is accessible
# Try "Upload Existing" to retry
```

**Frame extraction issues:**
```bash
# VapourSynth colorspace errors are handled automatically
# The app tries BT.709, BT.601, and BT.470BG matrices
```

See [Troubleshooting Wiki](https://github.com/Musfiq0/enhanced-screens-comparison/wiki/Troubleshooting) for more solutions.

---

## 📝 Changelog

### Version 3.6.1 (Latest)
- 🗑️ **Removed:** Portable exe build functionality (now runs from source only)
- 🐛 **Fixed:** TypeError in custom frames input (string to integer conversion)
- 🐛 **Fixed:** Random frame selection error (proper "RANDOM" marker handling)
- 🐛 **Fixed:** VapourSynth colorspace conversion (BT.709/BT.601 matrix specification)
- 📚 **Updated:** Documentation reflects CLI/GUI-only approach

### Version 3.6.0
- 🎲 **Added:** Random frame selection (30-35 distributed frames)
- 🧹 **Cleanup:** Removed Docker and Linux build files
- 📚 **Docs:** Enhanced documentation and wiki

### Version 3.5.2
- 🚀 Advanced CLI mode with professional automation
- 🔧 Enhanced upload system with chunking support
- 📈 Better error handling

[View Full Changelog →](CHANGELOG.md)

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**TL;DR:** Do whatever you want with this code, just don't blame us if something breaks.

---

## 🙏 Acknowledgments

- **VapourSynth** - Professional video processing framework
- **slow.pics** - Awesome comparison hosting service
- **Community** - All contributors and users

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/Musfiq0/enhanced-screens-comparison/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Musfiq0/enhanced-screens-comparison/discussions)
- **Wiki:** [Documentation](https://github.com/Musfiq0/enhanced-screens-comparison/wiki)

---

## ⭐ Star History

If this tool saved you time, consider starring the repo! It helps others discover the project.

[![Star History](https://img.shields.io/github/stars/Musfiq0/enhanced-screens-comparison?style=social)](https://github.com/Musfiq0/enhanced-screens-comparison/stargazers)

---

<div align="center">

**Made with ❤️ and lots of ☕**

*Because video comparison shouldn't be a pain*

[⬆ Back to Top](#-enhanced-screenshot-comparison-tool)

</div>
