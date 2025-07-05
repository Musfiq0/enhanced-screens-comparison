# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Enhanced Screenshot Comparison Tool
This provides advanced build configuration for creating a professional Windows executable
"""

import os
import sys
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define data files to include
added_files = [
    ('comparev2.py', '.'),  # Include the core comparison module
    ('requirements.txt', '.'),  # Include requirements for reference
    ('README.md', '.'),  # Include readme
]

# Hidden imports - libraries that PyInstaller might miss
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'cv2',
    'numpy',
    'requests',
    'requests_toolbelt',
    'requests_toolbelt.multipart',
    'requests_toolbelt.multipart.encoder',
    'json',
    'uuid',
    'pathlib',
    'webbrowser',
    'threading',
    'traceback',
    'importlib',
    'colorama',
]

# Optional VapourSynth imports (if available)
try:
    import vapoursynth
    hiddenimports.extend(['vapoursynth', 'awsmfunc'])
except ImportError:
    pass

block_cipher = None

a = Analysis(
    ['gui_app.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=added_files,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude packages that aren't needed to reduce size
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'sphinx',
        'pytest',
        'setuptools',
        'distutils',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out unnecessary DLLs and modules to reduce size
def filter_binaries(binaries):
    """Filter out unnecessary binaries to reduce executable size"""
    excluded_dlls = [
        'api-ms-win-',  # Windows API DLLs (usually not needed)
        'msvcp140_1.dll',  # Often duplicated
        'vcruntime140_1.dll',  # Often duplicated
    ]
    
    filtered = []
    for binary in binaries:
        name = binary[0].lower()
        if not any(excluded in name for excluded in excluded_dlls):
            filtered.append(binary)
    
    return filtered

a.binaries = filter_binaries(a.binaries)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ScreenshotComparison',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Use UPX compression to reduce size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window (GUI app)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(current_dir / 'icon.ico') if (current_dir / 'icon.ico').exists() else None,  # Use icon if available
    version=str(current_dir / 'version_info.txt') if (current_dir / 'version_info.txt').exists() else None,  # Version info if available
)
