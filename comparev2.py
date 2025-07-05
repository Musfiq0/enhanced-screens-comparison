#!/usr/bin/env python3
"""
Enhanced VapourSynth Screenshot Comparison Tool with Dynamic Fallback Support

A screenshot comparison tool with VapourSynth, OpenCV, or PIL fallback.
Supports multiple video source comparison and slow.pics upload.

Version: 2.0 - Dynamic Fallback Edition
"""

import sys
import os
import requests
import json
import time
import uuid
import pathlib
import webbrowser
from typing import Dict, List, Optional, Tuple, Any
from requests import Session
from requests_toolbelt import MultipartEncoder
import importlib
import traceback

# Global variables for dynamic imports
vs = None
awf = None
core = None
cv2 = None
PIL_Image = None
PIL_ImageDraw = None
PIL_ImageFont = None
np = None

# Library availability flags
VAPOURSYNTH_AVAILABLE = False
OPENCV_AVAILABLE = False
PIL_AVAILABLE = False
NUMPY_AVAILABLE = False

# Color codes for terminal styling
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def colored_print(text, color=Colors.WHITE, bold=False, end='\n'):
    """Print colored text to terminal"""
    style = f"{Colors.BOLD if bold else ''}{color}"
    print(f"{style}{text}{Colors.END}", end=end)

def print_header(text):
    """Print a styled header"""
    colored_print(f"\n{'='*60}", Colors.CYAN, bold=True)
    colored_print(f"[*] {text} [*]", Colors.CYAN, bold=True)
    colored_print(f"{'='*60}", Colors.CYAN, bold=True)

def try_import_vapoursynth():
    """Try to import VapourSynth and related libraries"""
    global vs, awf, core, VAPOURSYNTH_AVAILABLE
    try:
        import vapoursynth as vs_module
        vs = vs_module
        core = vs.core
        VAPOURSYNTH_AVAILABLE = True
        colored_print("[OK] VapourSynth detected and imported successfully", Colors.GREEN)
        
        # Try to import awsmfunc
        try:
            import awsmfunc as awf_module
            awf = awf_module
            colored_print("[OK] awsmfunc detected and imported successfully", Colors.GREEN)
        except ImportError:
            colored_print("[WARN] awsmfunc not available (optional for advanced features)", Colors.YELLOW)
            awf = None
            
        return True
    except ImportError as e:
        colored_print(f"[ERROR] VapourSynth not available: {e}", Colors.RED)
        return False

def try_import_opencv():
    """Try to import OpenCV"""
    global cv2, OPENCV_AVAILABLE
    try:
        import cv2 as cv2_module
        cv2 = cv2_module
        OPENCV_AVAILABLE = True
        colored_print("[OK] OpenCV detected and imported successfully", Colors.GREEN)
        return True
    except ImportError as e:
        colored_print(f"[ERROR] OpenCV not available: {e}", Colors.RED)
        return False

def try_import_pil():
    """Try to import PIL/Pillow"""
    global PIL_Image, PIL_ImageDraw, PIL_ImageFont, PIL_AVAILABLE
    try:
        from PIL import Image, ImageDraw, ImageFont
        PIL_Image = Image
        PIL_ImageDraw = ImageDraw
        PIL_ImageFont = ImageFont
        PIL_AVAILABLE = True
        colored_print("[OK] PIL/Pillow detected and imported successfully", Colors.GREEN)
        return True
    except ImportError as e:
        colored_print(f"[ERROR] PIL/Pillow not available: {e}", Colors.RED)
        return False

def try_import_numpy():
    """Try to import numpy"""
    global np, NUMPY_AVAILABLE
    try:
        import numpy as np_module
        np = np_module
        NUMPY_AVAILABLE = True
        colored_print("[OK] NumPy detected and imported successfully", Colors.GREEN)
        return True
    except ImportError as e:
        colored_print(f"[ERROR] NumPy not available: {e}", Colors.RED)
        return False

def detect_available_libraries():
    """Detect which libraries are available and set up the processing mode"""
    colored_print("[INFO] Detecting available video processing libraries...", Colors.CYAN, bold=True)
    
    # Try to import all libraries
    vs_available = try_import_vapoursynth()
    cv_available = try_import_opencv() 
    pil_available = try_import_pil()
    numpy_available = try_import_numpy()
    
    if vs_available:
        colored_print("\n[MODE] Using VapourSynth mode (high-quality video processing)", Colors.GREEN, bold=True)
        return "vapoursynth"
    elif cv_available and numpy_available:
        colored_print("\n[MODE] Using OpenCV fallback mode (basic video processing)", Colors.BLUE, bold=True)
        if not pil_available:
            colored_print("[WARN] PIL not available - text overlays will be simplified", Colors.YELLOW)
        return "opencv"
    elif pil_available and numpy_available:
        colored_print("\n[MODE] Using PIL fallback mode (basic image processing)", Colors.MAGENTA, bold=True)
        colored_print("[WARN] Limited video format support without OpenCV", Colors.YELLOW)
        return "pil"
    else:
        colored_print("\n[ERROR] No suitable video processing libraries found!", Colors.RED, bold=True)
        colored_print("Please install one of the following:", Colors.YELLOW, bold=True)
        colored_print("  - VapourSynth (recommended): pip install vapoursynth", Colors.WHITE)
        colored_print("  - OpenCV: pip install opencv-python", Colors.WHITE)
        colored_print("  - PIL + NumPy: pip install pillow numpy", Colors.WHITE)
        sys.exit(1)

# Detect libraries on import
PROCESSING_MODE = detect_available_libraries()

# ===============================================================================
# VIDEO PROCESSING BACKEND CLASSES
# ===============================================================================

class VideoProcessor:
    """Base class for video processing backends"""
    
    def __init__(self):
        self.mode = "base"
        
    def load_video(self, path: str):
        """Load a video file"""
        raise NotImplementedError
        
    def get_frame_count(self, video) -> int:
        """Get total frame count"""
        raise NotImplementedError
        
    def get_frame(self, video, frame_number: int):
        """Get a specific frame"""
        raise NotImplementedError
        
    def resize_frame(self, frame, width: int, height: int):
        """Resize a frame"""
        raise NotImplementedError
        
    def crop_frame(self, frame, left: int, top: int, right: int, bottom: int):
        """Crop a frame"""
        raise NotImplementedError
        
    def add_text_overlay(self, frame, text: str, position: tuple = (10, 10)):
        """Add text overlay to frame"""
        raise NotImplementedError
        
    def save_frame_as_png(self, frame, filepath: str):
        """Save frame as PNG"""
        raise NotImplementedError

class VapourSynthProcessor(VideoProcessor):
    """VapourSynth-based video processing"""
    
    def __init__(self):
        super().__init__()
        self.mode = "vapoursynth"
        if not VAPOURSYNTH_AVAILABLE:
            raise RuntimeError("VapourSynth not available")
        # Store references to global vs and core for easy access
        self.vs = vs
        self.core = core
        
        # Verify that vs and core are properly initialized
        if self.vs is None or self.core is None:
            raise RuntimeError("VapourSynth core not properly initialized")
            
    def load_video(self, path: str):
        """Load video using VapourSynth"""
        try:
            return core.lsmas.LWLibavSource(path)
        except Exception as e:
            # Fallback to other source filters
            try:
                return core.ffms2.Source(path)
            except:
                try:
                    return core.bs.VideoSource(path)
                except:
                    raise RuntimeError(f"Could not load video {path}: {e}")
                    
    def get_frame_count(self, video) -> int:
        """Get frame count from VapourSynth clip"""
        return len(video)
        
    def get_frame(self, video, frame_number: int):
        """Get specific frame from VapourSynth clip"""
        return video[frame_number:frame_number+1]
        
    def resize_frame(self, frame, width: int, height: int):
        """Resize frame using VapourSynth"""
        return core.resize.Spline36(frame, width=width, height=height)
        
    def crop_frame(self, frame, left: int, top: int, right: int, bottom: int):
        """Crop frame using VapourSynth"""
        return core.std.Crop(frame, left=left, right=right, top=top, bottom=bottom)
        
    def add_text_overlay(self, frame, text: str, position: tuple = (10, 10)):
        """Add text overlay using VapourSynth"""
        # VapourSynth text overlay with enhanced styling
        return core.text.Text(frame, text, alignment=7, scale=2)
        
    def save_frame_as_png(self, frame, filepath: str):
        """Save frame using VapourSynth with PIL backend (more reliable than fpng)"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Convert to RGB24 for PNG output
        rgb_frame = self.core.resize.Bicubic(frame, format=self.vs.RGB24, matrix_in_s="709")
        
        # Get the frame
        vs_frame = rgb_frame.get_frame(0)
        
        # Convert VapourSynth frame to numpy array and save using PIL
        import numpy as np
        from PIL import Image
        
        # Use the built-in frame-to-array conversion
        # This handles all the complexity of stride, format, etc.
        rgb_array = np.asarray(vs_frame)
        
        # VapourSynth arrays are in (plane, height, width) format
        # We need to transpose to (height, width, plane) for PIL
        if rgb_array.ndim == 3 and rgb_array.shape[0] == 3:
            # Transpose from (3, height, width) to (height, width, 3)
            rgb_array = rgb_array.transpose(1, 2, 0)
        
        # Create PIL image and save
        img = Image.fromarray(rgb_array, 'RGB')
        img.save(filepath)

class OpenCVProcessor(VideoProcessor):
    """OpenCV-based video processing"""
    
    def __init__(self):
        super().__init__()
        self.mode = "opencv"
        if not OPENCV_AVAILABLE or not NUMPY_AVAILABLE:
            raise RuntimeError("OpenCV or NumPy not available")
            
    def load_video(self, path: str):
        """Load video using OpenCV"""
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video: {path}")
        return cap
        
    def get_frame_count(self, video) -> int:
        """Get frame count from OpenCV VideoCapture"""
        return int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
    def get_frame(self, video, frame_number: int):
        """Get specific frame from OpenCV VideoCapture"""
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if not ret:
            raise RuntimeError(f"Could not read frame {frame_number}")
        return frame
        
    def resize_frame(self, frame, width: int, height: int):
        """Resize frame using OpenCV"""
        return cv2.resize(frame, (width, height), interpolation=cv2.INTER_LANCZOS4)
        
    def crop_frame(self, frame, left: int, top: int, right: int, bottom: int):
        """Crop frame using OpenCV/NumPy"""
        height, width = frame.shape[:2]
        return frame[top:height-bottom, left:width-right]
        
    def add_text_overlay(self, frame, text: str, position: tuple = (10, 30)):
        """Add text overlay using OpenCV"""
        # Create a copy to avoid modifying original
        overlay_frame = frame.copy()
        
        # Use a more readable font and larger size
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        color = (255, 255, 255)  # White text
        thickness = 2
        
        # Add black outline for better readability
        cv2.putText(overlay_frame, text, position, font, font_scale, (0, 0, 0), thickness + 2)
        cv2.putText(overlay_frame, text, position, font, font_scale, color, thickness)
        
        return overlay_frame
        
    def save_frame_as_png(self, frame, filepath: str):
        """Save frame as PNG using OpenCV"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Convert BGR to RGB for proper color representation
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        success = cv2.imwrite(filepath, cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
        if not success:
            raise RuntimeError(f"Failed to save frame to {filepath}")

class PILProcessor(VideoProcessor):
    """PIL-based image processing (limited video support)"""
    
    def __init__(self):
        super().__init__()
        self.mode = "pil"
        if not PIL_AVAILABLE or not NUMPY_AVAILABLE:
            raise RuntimeError("PIL or NumPy not available")
            
    def load_video(self, path: str):
        """Load video frames using PIL (very basic, frame extraction only)"""
        # PIL can't handle video files directly
        # This is a placeholder - would need external tool like ffmpeg
        raise NotImplementedError("PIL mode requires pre-extracted frames or single images")
        
    def get_frame_count(self, video) -> int:
        """Get frame count (PIL mode limitation)"""
        return 1  # PIL typically works with single images
        
    def get_frame(self, video, frame_number: int):
        """Get frame (for PIL, this would be loading a single image)"""
        if isinstance(video, str):  # Assume it's a path to an image
            return PIL_Image.open(video)
        return video
        
    def resize_frame(self, frame, width: int, height: int):
        """Resize frame using PIL"""
        return frame.resize((width, height), PIL_Image.LANCZOS)
        
    def crop_frame(self, frame, left: int, top: int, right: int, bottom: int):
        """Crop frame using PIL"""
        width, height = frame.size
        return frame.crop((left, top, width - right, height - bottom))
        
    def add_text_overlay(self, frame, text: str, position: tuple = (10, 10)):
        """Add text overlay using PIL"""
        # Create a copy to avoid modifying original
        overlay_frame = frame.copy()
        draw = PIL_ImageDraw.Draw(overlay_frame)
        
        try:
            # Try to use a nice font
            font = PIL_ImageFont.truetype("arial.ttf", 24)
        except:
            # Fallback to default font
            font = PIL_ImageFont.load_default()
            
        # Add text with outline for better readability
        x, y = position
        # Black outline
        for adj in range(-2, 3):
            for adj2 in range(-2, 3):
                draw.text((x + adj, y + adj2), text, font=font, fill='black')
        # White text
        draw.text(position, text, font=font, fill='white')
        
        return overlay_frame
        
    def save_frame_as_png(self, frame, filepath: str):
        """Save frame as PNG using PIL"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        frame.save(filepath, 'PNG')

# ===============================================================================
# PROCESSOR FACTORY
# ===============================================================================

def create_video_processor():
    """Create appropriate video processor based on available libraries"""
    try:
        if PROCESSING_MODE == "vapoursynth":
            return VapourSynthProcessor()
        elif PROCESSING_MODE == "opencv":
            return OpenCVProcessor()
        elif PROCESSING_MODE == "pil":
            return PILProcessor()
        else:
            raise RuntimeError("No suitable video processing backend available")
    except Exception as e:
        colored_print(f"[ERROR] Failed to create video processor: {e}", Colors.RED, bold=True)
        # Try fallback processors
        if PROCESSING_MODE != "opencv" and OPENCV_AVAILABLE:
            colored_print("[WARN] Falling back to OpenCV processor", Colors.YELLOW)
            return OpenCVProcessor()
        elif PROCESSING_MODE != "pil" and PIL_AVAILABLE:
            colored_print("[WARN] Falling back to PIL processor", Colors.YELLOW)
            return PILProcessor()
        else:
            raise RuntimeError(f"Failed to create any video processor: {e}")

# Global processor instance
processor = create_video_processor()
colored_print(f"[TOOL] Video processor initialized: {processor.mode.upper()} mode", Colors.GREEN, bold=True)

def _get_slowpics_header(content_length: str, content_type: str, sess: Session) -> Dict[str, str]:
    """
    Generate headers for slow.pics upload requests.
    Adapted from working comp.py implementation.
    """
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Access-Control-Allow-Origin": "*",
        "Content-Length": content_length,
        "Content-Type": content_type,
        "Origin": "https://slow.pics/",
        "Referer": "https://slow.pics/comparison",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "X-XSRF-TOKEN": sess.cookies.get_dict()["XSRF-TOKEN"]
    }

def get_upload_only_config():
    """Get configuration for uploading existing screenshots only"""
    print_header("UPLOAD EXISTING SCREENSHOTS")
    
    # Analyze existing screenshots to determine sources and frames
    screenshots_folder = "Screenshots"
    source_folders = []
    all_frames = set()
    
    for item in os.listdir(screenshots_folder):
        item_path = os.path.join(screenshots_folder, item)
        if os.path.isdir(item_path):
            png_files = [f for f in os.listdir(item_path) if f.endswith('.png')]
            if png_files:
                source_folders.append(item)
                # Extract frame numbers from filenames
                for png_file in png_files:
                    try:
                        # Assuming format: SourceName_000000_000000.png
                        parts = png_file.split('_')
                        if len(parts) >= 2:
                            frame_num = int(parts[1])
                            all_frames.add(frame_num)
                    except (ValueError, IndexError):
                        continue
    
    frames = sorted(list(all_frames))
    
    colored_print(f"[DIRS] Found {len(source_folders)} video sources:", Colors.GREEN, bold=True)
    for i, source in enumerate(source_folders):
        source_path = os.path.join(screenshots_folder, source)
        png_files = [f for f in os.listdir(source_path) if f.endswith('.png')]
        png_count = len(png_files)
        colored_print(f"   {i+1}. {source} ({png_count} screenshots)", Colors.CYAN)
        
        # Show sample filenames to help user verify
        if png_files:
            sample_files = png_files[:3]  # Show first 3 files
            for sample in sample_files:
                colored_print(f"      - {sample}", Colors.WHITE)
            if len(png_files) > 3:
                colored_print(f"      - ... and {len(png_files) - 3} more files", Colors.WHITE)
    
    colored_print(f"\n[IMAGE]  Found {len(frames)} unique frames", Colors.BLUE, bold=True)
    if len(frames) <= 20:
        colored_print(f"   Frames: {frames}", Colors.WHITE)
    else:
        colored_print(f"   Frames: {frames[:10]} ... {frames[-5:]} (showing first 10 and last 5)", Colors.WHITE)
    
    colored_print(f"\n[INFO] Total screenshots to upload: {len(frames) * len(source_folders)}", Colors.MAGENTA, bold=True)
    
    # Get slow.pics upload options
    colored_print("\n[UPLOAD] slow.pics Upload Options", Colors.YELLOW, bold=True)
    show_name = input(f"{Colors.CYAN}Enter show/movie name: {Colors.END}").strip()
    if not show_name:
        colored_print("[ERROR] Show/movie name is required for upload. Exiting.", Colors.RED, bold=True)
        sys.exit(0)
    
    # Ask if it's a TV series (has seasons)
    colored_print("\nIs this a TV series with seasons?", Colors.YELLOW, bold=True)
    colored_print("1. [TV] Yes (TV series)", Colors.GREEN)
    colored_print("2. [MOVIE] No (Movie)", Colors.BLUE)
    
    while True:
        try:
            series_choice = int(input(f"\n{Colors.CYAN}Enter choice (1 or 2): {Colors.END}"))
            if series_choice in [1, 2]:
                if series_choice == 1:
                    colored_print("[OK] TV series selected!", Colors.GREEN, bold=True)
                else:
                    colored_print("[OK] Movie selected!", Colors.GREEN, bold=True)
                break
            else:
                colored_print("[ERROR] Please enter 1 or 2.", Colors.RED)
        except ValueError:
            colored_print("[ERROR] Please enter a valid number.", Colors.RED)
    
    season_number = ""
    if series_choice == 1:
        season_input = input(f"{Colors.CYAN}Enter season number (e.g., 1, 2, 3): {Colors.END}").strip()
        if season_input:
            try:
                season_num = int(season_input)
                season_number = f"S{season_num:02d}"
                colored_print(f"[OK] Season {season_num} configured!", Colors.GREEN, bold=True)
            except ValueError:
                colored_print("[WARN] Invalid season number, continuing without season.", Colors.YELLOW)
                season_number = ""
    
    # Create mock processed_videos structure
    processed_videos = []
    for source in source_folders:
        processed_videos.append({
            'name': source,
            'clip': None  # Not needed for upload
        })
    
    return {
        'upload_only': True,
        'frames': frames,
        'processed_videos': processed_videos,
        'show_name': show_name,
        'season_number': season_number,
        'upload_to_slowpics': True
    }

def get_user_input():
    """Get user input for video files and processing options interactively"""
    print_header("VIDEO COMPARISON SCREENSHOT GENERATOR")
    colored_print("[VIDEO] Welcome to the Enhanced Screenshot Comparison Tool! [VIDEO]", Colors.MAGENTA, bold=True)
    
    # First, ask for comparison type
    colored_print("\nChoose comparison type:", Colors.YELLOW, bold=True)
    colored_print("1. [DIR] Multiple sources comparison (compare different sources)", Colors.GREEN)
    colored_print("2. [VS] Source vs Encode comparison (compare original with encoded version)", Colors.BLUE)
    
    while True:
        try:
            choice_input = input(f"\n{Colors.CYAN}Enter choice (1 or 2): {Colors.END}")
            comparison_type = int(choice_input)
            if comparison_type in [1, 2]:
                if comparison_type == 1:
                    colored_print("[OK] Multiple sources comparison selected!", Colors.GREEN, bold=True)
                else:
                    colored_print("[OK] Source vs Encode comparison selected!", Colors.GREEN, bold=True)
                break
            else:
                colored_print("[ERROR] Please enter 1 or 2.", Colors.RED)
        except ValueError:
            colored_print("[ERROR] Please enter a valid number.", Colors.RED)
    
    # Check if Screenshots folder exists and has content
    screenshots_folder_exists = os.path.exists("Screenshots") and os.path.isdir("Screenshots")
    has_existing_screenshots = False
    
    if screenshots_folder_exists:
        # Check if there are subdirectories with PNG files
        for item in os.listdir("Screenshots"):
            item_path = os.path.join("Screenshots", item)
            if os.path.isdir(item_path):
                png_files = [f for f in os.listdir(item_path) if f.endswith('.png')]
                if png_files:
                    has_existing_screenshots = True
                    break
    
    # Ask user what they want to do
    if has_existing_screenshots:
        colored_print("\n[INFO] Found existing screenshots in the Screenshots folder!", Colors.YELLOW, bold=True)
        colored_print("\nWhat would you like to do?", Colors.CYAN, bold=True)
        colored_print("1. [NEW] Generate new screenshots (will overwrite existing ones)", Colors.GREEN)
        colored_print("2. [UP] Upload existing screenshots to slow.pics", Colors.BLUE)
        colored_print("3. [EXIT] Exit", Colors.RED)
        
        while True:
            try:
                choice = int(input(f"\n{Colors.CYAN}Enter your choice (1-3): {Colors.END}"))
                if choice in [1, 2, 3]:
                    if choice == 2:
                        colored_print("[OK] Upload existing screenshots selected!", Colors.GREEN, bold=True)
                    elif choice == 3:
                        colored_print("[EXIT] Goodbye!", Colors.YELLOW, bold=True)
                    else:
                        colored_print("[OK] Generate new screenshots selected!", Colors.GREEN, bold=True)
                    break
                else:
                    colored_print("[ERROR] Please enter 1, 2, or 3.", Colors.RED)
            except ValueError:
                colored_print("[ERROR] Please enter a valid number.", Colors.RED)
        
        if choice == 3:
            print("Exiting...")
            sys.exit(0)
        elif choice == 2:
            # Upload existing screenshots
            return get_upload_only_config()
    
    # Continue with video comparison flow based on type
    if comparison_type == 1:
        return get_multiple_sources_config()
    else:
        return get_source_vs_encode_config()

def get_multiple_sources_config():
    """Get configuration for multiple sources comparison"""
    print("\n=== Multiple Sources Comparison ===")
    
    # Get number of video sources
    while True:
        try:
            num_videos = int(input("How many video sources do you want to compare? (2-10): "))
            if 2 <= num_videos <= 10:
                break
            else:
                print("Please enter a number between 2 and 10.")
        except ValueError:
            print("Please enter a valid number.")
    
    videos = []
    
    # Get video file paths and processing options for each source
    for i in range(num_videos):
        print(f"\n--- Video Source {i+1} ---")
        
        # Get video file path
        while True:
            video_path = input(f"Enter path to video {i+1}: ").strip('"')
            if os.path.exists(video_path):
                break
            else:
                print(f"File not found: {video_path}. Please try again.")
        
        # Get display name
        default_name = f"Source{i+1}"
        source_name = input(f"Enter display name for this source (default: {default_name}): ").strip()
        if not source_name:
            source_name = default_name
        
        # Get processing options
        print(f"Processing options for {source_name}:")
        print("1. No processing (use video as-is)")
        print("2. Trim frames only")
        print("3. Add padding only") 
        print("4. Both trim and pad")
        
        while True:
            try:
                process_choice = int(input("Choose processing option (1-4): "))
                if process_choice in [1, 2, 3, 4]:
                    break
                else:
                    print("Please enter 1, 2, 3, or 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        trim_start = trim_end = pad_start = pad_end = 0
        
        if process_choice in [2, 4]:  # Trim frames
            print(f"Trimming options for {source_name}:")
            try:
                trim_start = int(input(f"  Frames to trim from start (default: 0): ") or "0")
                trim_end = int(input(f"  Frames to trim from end (default: 0): ") or "0")
            except ValueError:
                trim_start, trim_end = 0, 0
                print("  Invalid input, using default values (0, 0)")
        
        if process_choice in [3, 4]:  # Add padding
            print(f"Padding options for {source_name}:")
            try:
                pad_start = int(input(f"  Black frames to add at start (default: 0): ") or "0")
                pad_end = int(input(f"  Black frames to add at end (default: 0): ") or "0")
            except ValueError:
                pad_start, pad_end = 0, 0
                print("  Invalid input, using default values (0, 0)")
        
        videos.append({
            'path': video_path,
            'name': source_name,
            'trim_start': trim_start,
            'trim_end': trim_end,
            'pad_start': pad_start,
            'pad_end': pad_end,
            'crop': None,  # No cropping for multiple sources
            'resize': None  # Will be set in common resize config
        })
    
    # Get common screenshot and upload options
    screenshot_config = get_screenshot_and_upload_config()
    
    # Get resize configuration for multiple sources
    resize_config = get_resize_config(videos)
    
    return {
        'comparison_type': 'multiple_sources',
        'videos': videos,
        'resize_config': resize_config,
        **screenshot_config
    }

def get_source_vs_encode_config():
    """Get configuration for source vs encode comparison with cropping"""
    print("\n=== Source vs Encode Comparison ===")
    
    videos = []
    
    # Get source video
    print("--- Primary Source Video ---")
    while True:
        source_path = input("Enter path to primary source video: ").strip('"')
        if os.path.exists(source_path):
            break
        else:
            print(f"File not found: {source_path}. Please try again.")
    
    source_name = input("Enter display name for primary source (default: Source): ").strip() or "Source"
    
    # Get encode video
    print("\n--- Encoded Video ---")
    while True:
        encode_path = input("Enter path to encoded video: ").strip('"')
        if os.path.exists(encode_path):
            break
        else:
            print(f"File not found: {encode_path}. Please try again.")
    
    encode_name = input("Enter display name for encode (default: Encode): ").strip() or "Encode"
    
    # Ask for additional source videos
    print("\n--- Additional Source Videos ---")
    print("You can compare multiple sources with the encoded video")
    while True:
        try:
            num_additional = int(input("How many additional source videos to compare? (0-8): "))
            if 0 <= num_additional <= 8:
                break
            else:
                print("Please enter a number between 0 and 8.")
        except ValueError:
            print("Please enter a valid number.")
    
    additional_sources = []
    for i in range(num_additional):
        print(f"\n--- Additional Source {i+1} ---")
        while True:
            additional_path = input(f"Enter path to additional source {i+1}: ").strip('"')
            if os.path.exists(additional_path):
                break
            else:
                print(f"File not found: {additional_path}. Please try again.")
        
        default_name = f"Source{i+2}"
        additional_name = input(f"Enter display name for additional source {i+1} (default: {default_name}): ").strip() or default_name
        
        # Get cropping options for this additional source
        print(f"\n--- Cropping Options for {additional_name} ---")
        print("Choose cropping method:")
        print("1. No cropping")
        print("2. Auto-detect crop (recommended)")
        print("3. Manual crop values")
        
        while True:
            try:
                crop_choice = int(input("Enter choice (1-3): "))
                if crop_choice in [1, 2, 3]:
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")
        
        additional_crop = None
        if crop_choice == 2:
            additional_crop = "auto"
            print(f"Auto-detect crop will be applied to {additional_name}")
        elif crop_choice == 3:
            print("Enter crop values (pixels to remove from each edge):")
            try:
                crop_left = int(input("  Left: ") or "0")
                crop_right = int(input("  Right: ") or "0") 
                crop_top = int(input("  Top: ") or "0")
                crop_bottom = int(input("  Bottom: ") or "0")
                if crop_left or crop_right or crop_top or crop_bottom:
                    additional_crop = {
                        'left': crop_left,
                        'right': crop_right,
                        'top': crop_top,
                        'bottom': crop_bottom
                    }
                    print(f"Manual crop will be applied: left={crop_left}, right={crop_right}, top={crop_top}, bottom={crop_bottom}")
                else:
                    print("No cropping values entered, proceeding without crop")
            except ValueError:
                print("Invalid crop values, proceeding without crop")
        
        # Get processing options for this additional source
        print(f"\n--- Processing Options for {additional_name} ---")
        print("1. No processing (use video as-is)")
        print("2. Trim frames only")
        print("3. Add padding only") 
        print("4. Both trim and pad")
        
        while True:
            try:
                additional_process_choice = int(input("Choose processing option (1-4): "))
                if additional_process_choice in [1, 2, 3, 4]:
                    break
                else:
                    print("Please enter 1, 2, 3, or 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        additional_trim_start = additional_trim_end = additional_pad_start = additional_pad_end = 0
        
        if additional_process_choice in [2, 4]:  # Trim frames
            print(f"Trimming options for {additional_name}:")
            try:
                additional_trim_start = int(input(f"  Frames to trim from start (default: 0): ") or "0")
                additional_trim_end = int(input(f"  Frames to trim from end (default: 0): ") or "0")
            except ValueError:
                additional_trim_start, additional_trim_end = 0, 0
                print("  Invalid input, using default values (0, 0)")
        
        if additional_process_choice in [3, 4]:  # Add padding
            print(f"Padding options for {additional_name}:")
            try:
                additional_pad_start = int(input(f"  Black frames to add at start (default: 0): ") or "0")
                additional_pad_end = int(input(f"  Black frames to add at end (default: 0): ") or "0")
            except ValueError:
                additional_pad_start, additional_pad_end = 0, 0
                print("  Invalid input, using default values (0, 0)")
        
        additional_sources.append({
            'path': additional_path, 
            'name': additional_name,
            'crop': additional_crop,
            'trim_start': additional_trim_start,
            'trim_end': additional_trim_end,
            'pad_start': additional_pad_start,
            'pad_end': additional_pad_end
        })
    
    print(f"\n[WARN] IMPORTANT: Encode videos will NOT be resized to prevent unwanted upscaling")
    print(f"   Only source videos can be resized. Resize options will only be shown for sources.")
    
    # Collect all source videos for resize configuration
    all_source_videos = [{'path': source_path, 'name': source_name}]
    all_source_videos.extend(additional_sources)
    
    # Get resize configuration for source videos only (before cropping)
    print(f"\n--- Resize Options for Source Videos ---")
    print("Configure resizing for source videos (encode will not be resized)")
    resize_config = get_source_resize_config(all_source_videos)
    
    # Get cropping options for primary source
    print(f"\n--- Cropping Options for {source_name} ---")
    print("Cropping helps when source has black bars or different aspect ratio")
    print("Choose cropping method:")
    print("1. No cropping")
    print("2. Auto-detect crop (recommended)")
    print("3. Manual crop values")
    
    while True:
        try:
            crop_choice = int(input("Enter choice (1-3): "))
            if crop_choice in [1, 2, 3]:
                break
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")
    
    source_crop = None
    if crop_choice == 2:
        source_crop = "auto"
        print("Auto-detect crop will be applied to source video")
    elif crop_choice == 3:
        print("Enter crop values (pixels to remove from each edge):")
        try:
            crop_left = int(input("  Left: ") or "0")
            crop_right = int(input("  Right: ") or "0") 
            crop_top = int(input("  Top: ") or "0")
            crop_bottom = int(input("  Bottom: ") or "0")
            if crop_left or crop_right or crop_top or crop_bottom:
                source_crop = {
                    'left': crop_left,
                    'right': crop_right,
                    'top': crop_top,
                    'bottom': crop_bottom
                }
                print(f"Manual crop will be applied: left={crop_left}, right={crop_right}, top={crop_top}, bottom={crop_bottom}")
            else:
                print("No cropping values entered, proceeding without crop")
        except ValueError:
            print("Invalid crop values, proceeding without crop")
    
    # Set default values (trimming and padding now available for source vs encode)
    source_trim_start = source_trim_end = source_pad_start = source_pad_end = 0
    encode_trim_start = encode_trim_end = encode_pad_start = encode_pad_end = 0
    
    # Ask for trim/pad options for source video
    print(f"\n--- Processing Options for Source Video ({source_name}) ---")
    print("1. No processing (use video as-is)")
    print("2. Trim frames only")
    print("3. Add padding only") 
    print("4. Both trim and pad")
    
    while True:
        try:
            source_process_choice = int(input("Choose processing option for source (1-4): "))
            if source_process_choice in [1, 2, 3, 4]:
                break
            else:
                print("Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    if source_process_choice in [2, 4]:  # Trim frames
        print(f"Trimming options for source {source_name}:")
        try:
            source_trim_start = int(input(f"  Frames to trim from start (default: 0): ") or "0")
            source_trim_end = int(input(f"  Frames to trim from end (default: 0): ") or "0")
        except ValueError:
            source_trim_start, source_trim_end = 0, 0
            print("  Invalid input, using default values (0, 0)")
    
    if source_process_choice in [3, 4]:  # Add padding
        print(f"Padding options for source {source_name}:")
        try:
            source_pad_start = int(input(f"  Black frames to add at start (default: 0): ") or "0")
            source_pad_end = int(input(f"  Black frames to add at end (default: 0): ") or "0")
        except ValueError:
            source_pad_start, source_pad_end = 0, 0
            print("  Invalid input, using default values (0, 0)")
    
    # Ask for trim/pad options for encode video
    print(f"\n--- Processing Options for Encode Video ({encode_name}) ---")
    print("1. No processing (use video as-is)")
    print("2. Trim frames only")
    print("3. Add padding only") 
    print("4. Both trim and pad")
    
    while True:
        try:
            encode_process_choice = int(input("Choose processing option for encode (1-4): "))
            if encode_process_choice in [1, 2, 3, 4]:
                break
            else:
                print("Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    if encode_process_choice in [2, 4]:  # Trim frames
        print(f"Trimming options for encode {encode_name}:")
        try:
            encode_trim_start = int(input(f"  Frames to trim from start (default: 0): ") or "0")
            encode_trim_end = int(input(f"  Frames to trim from end (default: 0): ") or "0")
        except ValueError:
            encode_trim_start, encode_trim_end = 0, 0
            print("  Invalid input, using default values (0, 0)")
    
    if encode_process_choice in [3, 4]:  # Add padding
        print(f"Padding options for encode {encode_name}:")
        try:
            encode_pad_start = int(input(f"  Black frames to add at start (default: 0): ") or "0")
            encode_pad_end = int(input(f"  Black frames to add at end (default: 0): ") or "0")
        except ValueError:
            encode_pad_start, encode_pad_end = 0, 0
            print("  Invalid input, using default values (0, 0)")
    
    print(f"\nFor source vs encode comparison, cropping is applied first, then trim/pad processing")
    print(f"This ensures proper frame-to-frame comparison between source and encode")
    
    # Add primary source video (will be first in comparison: Primary Source vs Encode vs Others)
    videos.append({
        'path': source_path,
        'name': source_name,
        'trim_start': source_trim_start,
        'trim_end': source_trim_end,
        'pad_start': source_pad_start,
        'pad_end': source_pad_end,
        'crop': source_crop,
        'resize': None,  # Will be set from resize config
        'is_source': True
    })
    
    # Add encode video (will be second in comparison)
    videos.append({
        'path': encode_path,
        'name': encode_name,
        'trim_start': encode_trim_start,
        'trim_end': encode_trim_end,
        'pad_start': encode_pad_start,
        'pad_end': encode_pad_end,
        'crop': None,  # Usually encode doesn't need cropping
        'resize': None,  # Encode videos are never resized
        'is_source': False
    })
    
    # Add additional source videos (will be after encode in comparison)
    for additional in additional_sources:
        videos.append({
            'path': additional['path'],
            'name': additional['name'],
            'trim_start': additional.get('trim_start', 0),
            'trim_end': additional.get('trim_end', 0),
            'pad_start': additional.get('pad_start', 0),
            'pad_end': additional.get('pad_end', 0),
            'crop': additional.get('crop', None),  # Use the crop setting from additional source
            'resize': None,  # Will be set from resize config
            'is_source': True
        })
    
    # Apply resize settings to source videos
    if resize_config['resize_method'] != 'none':
        for video in videos:
            if video['is_source']:
                if resize_config['resize_method'] == 'individual':
                    if video['name'] in resize_config.get('individual_resizes', {}):
                        video['resize'] = resize_config['individual_resizes'][video['name']]
                elif resize_config['resize_method'] == 'common':
                    video['resize'] = resize_config.get('common_resolution')
    
    # Get common screenshot and upload options
    screenshot_config = get_screenshot_and_upload_config()
    
    return {
        'comparison_type': 'source_vs_encode',
        'videos': videos,
        'resize_config': resize_config,
        **screenshot_config
    }

def get_screenshot_and_upload_config():
    """Get screenshot options and upload configuration"""
    print("\n--- Screenshot Options ---")
    
    # Frame selection method
    print("Choose frame selection method:")
    print("1. Use frame interval (e.g., every 150 frames)")
    print("2. Specify custom frame numbers")
    
    while True:
        try:
            choice = int(input("Enter choice (1 or 2): "))
            if choice in [1, 2]:
                break
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")
    
    if choice == 1:
        # Frame interval
        try:
            frame_interval = int(input("Enter frame interval for screenshots (default: 150): ") or "150")
        except ValueError:
            frame_interval = 150
            print("Invalid input, using default value (150)")
        custom_frames = None
    else:
        # Custom frames
        frame_interval = None
        custom_frames_input = input("Enter comma-separated frame numbers (e.g., 100,500,1000): ")
        try:
            custom_frames = [int(f.strip()) for f in custom_frames_input.split(',') if f.strip()]
            if not custom_frames:
                raise ValueError("No valid frames provided")
        except ValueError:
            print("Invalid frame numbers, using default interval of 150")
            frame_interval = 150
            custom_frames = None
    
    # Get slow.pics upload options
    print("\n--- slow.pics Upload Options ---")
    print("Would you like to upload screenshots to slow.pics for comparison?")
    print("1. Yes, upload to slow.pics")
    print("2. No, save locally only")
    
    while True:
        try:
            upload_choice = int(input("Enter choice (1 or 2): "))
            if upload_choice in [1, 2]:
                break
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")
    
    upload_to_slowpics = upload_choice == 1
    show_name = ""
    season_number = ""
    
    if upload_to_slowpics:
        show_name = input("Enter show/movie name: ").strip()
        if not show_name:
            print("Show/movie name is required for slow.pics upload. Disabling upload.")
            upload_to_slowpics = False
        else:
            # Ask if it's a TV series (has seasons)
            print("Is this a TV series with seasons?")
            print("1. Yes (TV series)")
            print("2. No (Movie)")
            
            while True:
                try:
                    series_choice = int(input("Enter choice (1 or 2): "))
                    if series_choice in [1, 2]:
                        break
                    else:
                        print("Please enter 1 or 2.")
                except ValueError:
                    print("Please enter a valid number.")
            
            if series_choice == 1:
                season_input = input("Enter season number (e.g., 1, 2, 3): ").strip()
                if season_input:
                    try:
                        season_num = int(season_input)
                        season_number = f"S{season_num:02d}"
                    except ValueError:
                        print("Invalid season number, continuing without season.")
                        season_number = ""
    
    return {
        'frame_interval': frame_interval,
        'custom_frames': custom_frames,
        'upload_to_slowpics': upload_to_slowpics,
        'show_name': show_name,
        'season_number': season_number
    }

def get_resize_config(videos):
    """Get resize configuration for video comparison"""
    print("\n--- Resize Options ---")
    print("Manual resize configuration for video comparison")
    
    # First, load videos to check their resolutions
    print("Checking video resolutions...")
    video_resolutions = []
    for video in videos:
        try:
            temp_clip = processor.load_video(video['path'])
            if processor.mode == "vapoursynth":
                width, height = temp_clip.width, temp_clip.height
            elif processor.mode == "opencv":
                width = int(temp_clip.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(temp_clip.get(cv2.CAP_PROP_FRAME_HEIGHT))
                temp_clip.release()  # Close OpenCV capture
            else:
                # For PIL mode, assume standard resolution as fallback
                width, height = 1920, 1080
                
            video_resolutions.append({
                'name': video['name'],
                'width': width,
                'height': height,
                'path': video['path']
            })
            print(f"  {video['name']}: {width}x{height}")
        except Exception as e:
            print(f"  Error reading {video['name']}: {e}")
            video_resolutions.append({
                'name': video['name'],
                'width': 1920,
                'height': 1080,
                'path': video['path']
            })
    
    print(f"\nChoose resize method:")
    print("1. No resizing (keep original resolutions)")
    print("2. Manual resize - specify resolution for each video individually")
    print("3. Common resolution - resize all videos to the same resolution")
    
    while True:
        try:
            resize_choice = int(input("Enter choice (1-3): "))
            if resize_choice in [1, 2, 3]:
                break
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")
    
    resize_method = 'none'
    individual_resizes = {}
    common_resolution = None
    
    if resize_choice == 1:
        resize_method = 'none'
        print("No resizing will be applied")
    
    elif resize_choice == 2:
        resize_method = 'individual'
        print("\nManual resize for each video:")
        print("Enter new resolution for each video (leave blank to keep original):")
        
        for video_res in video_resolutions:
            print(f"\n{video_res['name']} (current: {video_res['width']}x{video_res['height']}):")
            width_input = input(f"  New width (default: {video_res['width']}): ").strip()
            height_input = input(f"  New height (default: {video_res['height']}): ").strip()
            
            try:
                new_width = int(width_input) if width_input else video_res['width']
                new_height = int(height_input) if height_input else video_res['height']
                
                if new_width > 0 and new_height > 0:
                    if (new_width, new_height) != (video_res['width'], video_res['height']):
                        individual_resizes[video_res['name']] = (new_width, new_height)
                        print(f"  Will resize to {new_width}x{new_height}")
                    else:
                        print(f"  Keeping original resolution")
                else:
                    print(f"  Invalid resolution, keeping original")
            except ValueError:
                print(f"  Invalid input, keeping original resolution")
    
    elif resize_choice == 3:
        resize_method = 'common'
        print("\nCommon resolution for all videos:")
        print("Choose preset or enter custom:")
        print("1. 1080p (1920x1080)")
        print("2. 1440p (2560x1440)")
        print("3. 4K (3840x2160)")
        print("4. 720p (1280x720)")
        print("5. Custom resolution")
        
        while True:
            try:
                preset_choice = int(input("Enter choice (1-5): "))
                if preset_choice in [1, 2, 3, 4, 5]:
                    break
                else:
                    print("Please enter 1, 2, 3, 4, or 5.")
            except ValueError:
                print("Please enter a valid number.")
        
        if preset_choice == 1:
            common_resolution = (1920, 1080)
            print("All videos will be resized to 1920x1080 (1080p)")
        elif preset_choice == 2:
            common_resolution = (2560, 1440)
            print("All videos will be resized to 2560x1440 (1440p)")
        elif preset_choice == 3:
            common_resolution = (3840, 2160)
            print("All videos will be resized to 3840x2160 (4K)")
        elif preset_choice == 4:
            common_resolution = (1280, 720)
            print("All videos will be resized to 1280x720 (720p)")
        elif preset_choice == 5:
            print("Enter custom resolution:")
            try:
                custom_width = int(input("  Width: "))
                custom_height = int(input("  Height: "))
                if custom_width > 0 and custom_height > 0:
                    common_resolution = (custom_width, custom_height)
                    print(f"All videos will be resized to {custom_width}x{custom_height}")
                else:
                    print("Invalid resolution, no resizing will be applied")
                    resize_method = 'none'
            except ValueError:
                print("Invalid resolution values, no resizing will be applied")
                resize_method = 'none'
    
    return {
        'resize_method': resize_method,
        'individual_resizes': individual_resizes,
        'common_resolution': common_resolution,
        'video_resolutions': video_resolutions
    }

def get_source_resize_config(source_videos):
    """Get resize configuration for source videos only (encode videos are never resized)"""
    print("Manual resize configuration for source videos only")
    
    # First, load videos to check their resolutions
    print("Checking source video resolutions...")
    video_resolutions = []
    for video in source_videos:
        try:
            temp_clip = processor.load_video(video['path'])
            if processor.mode == "vapoursynth":
                width, height = temp_clip.width, temp_clip.height
            elif processor.mode == "opencv":
                width = int(temp_clip.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(temp_clip.get(cv2.CAP_PROP_FRAME_HEIGHT))
                temp_clip.release()  # Close OpenCV capture
            else:
                # For PIL mode, assume standard resolution as fallback
                width, height = 1920, 1080
                
            video_resolutions.append({
                'name': video['name'],
                'width': width,
                'height': height,
                'path': video['path']
            })
            print(f"  {video['name']}: {width}x{height}")
        except Exception as e:
            print(f"  Error reading {video['name']}: {e}")
            video_resolutions.append({
                'name': video['name'],
                'width': 1920,
                'height': 1080,
                'path': video['path']
            })
    
    print(f"\nChoose resize method for source videos:")
    print("1. No resizing (keep original resolutions)")
    print("2. Manual resize - specify resolution for each source video individually")
    print("3. Common resolution - resize all source videos to the same resolution")
    
    while True:
        try:
            resize_choice = int(input("Enter choice (1-3): "))
            if resize_choice in [1, 2, 3]:
                break
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")
    
    resize_method = 'none'
    individual_resizes = {}
    common_resolution = None
    
    if resize_choice == 1:
        resize_method = 'none'
        print("No resizing will be applied to source videos")
    
    elif resize_choice == 2:
        resize_method = 'individual'
        print("\nManual resize for each source video:")
        print("Enter new resolution for each source video (leave blank to keep original):")
        
        for video_res in video_resolutions:
            print(f"\n{video_res['name']} (current: {video_res['width']}x{video_res['height']}):")
            width_input = input(f"  New width (default: {video_res['width']}): ").strip()
            height_input = input(f"  New height (default: {video_res['height']}): ").strip()
            
            try:
                new_width = int(width_input) if width_input else video_res['width']
                new_height = int(height_input) if height_input else video_res['height']
                
                if new_width > 0 and new_height > 0:
                    if (new_width, new_height) != (video_res['width'], video_res['height']):
                        individual_resizes[video_res['name']] = (new_width, new_height)
                        print(f"  Will resize to {new_width}x{new_height}")
                    else:
                        print(f"  Keeping original resolution")
                else:
                    print(f"  Invalid resolution, keeping original")
            except ValueError:
                print(f"  Invalid input, keeping original resolution")
    
    elif resize_choice == 3:
        resize_method = 'common'
        print("\nCommon resolution for all source videos:")
        print("Choose preset or enter custom:")
        print("1. 1080p (1920x1080)")
        print("2. 1440p (2560x1440)")
        print("3. 4K (3840x2160)")
        print("4. 720p (1280x720)")
        print("5. Custom resolution")
        
        while True:
            try:
                preset_choice = int(input("Enter choice (1-5): "))
                if preset_choice in [1, 2, 3, 4, 5]:
                    break
                else:
                    print("Please enter 1, 2, 3, 4, or 5.")
            except ValueError:
                print("Please enter a valid number.")
        
        if preset_choice == 1:
            common_resolution = (1920, 1080)
            print("All source videos will be resized to 1920x1080 (1080p)")
        elif preset_choice == 2:
            common_resolution = (2560, 1440)
            print("All source videos will be resized to 2560x1440 (1440p)")
        elif preset_choice == 3:
            common_resolution = (3840, 2160)
            print("All source videos will be resized to 3840x2160 (4K)")
        elif preset_choice == 4:
            common_resolution = (1280, 720)
            print("All source videos will be resized to 1280x720 (720p)")
        elif preset_choice == 5:
            print("Enter custom resolution:")
            try:
                custom_width = int(input("  Width: "))
                custom_height = int(input("  Height: "))
                if custom_width > 0 and custom_height > 0:
                    common_resolution = (custom_width, custom_height)
                    print(f"All source videos will be resized to {custom_width}x{custom_height}")
                else:
                    print("Invalid resolution, no resizing will be applied")
                    resize_method = 'none'
            except ValueError:
                print("Invalid resolution values, no resizing will be applied")
                resize_method = 'none'
    
    return {
        'resize_method': resize_method,
        'individual_resizes': individual_resizes,
        'common_resolution': common_resolution,
        'video_resolutions': video_resolutions
    }

def apply_processing(clip, trim_start=0, trim_end=0, pad_start=0, pad_end=0, crop=None, resize=None, is_source=False):
    """Apply trimming, padding, cropping, and resizing to a video clip (VapourSynth only)"""
    
    if processor.mode != "vapoursynth":
        raise RuntimeError("apply_processing() only works in VapourSynth mode. Use apply_frame_processing() for fallback modes.")
    
    # Processing order for source videos: resize first, then crop
    # This ensures crop values are applied at target resolution (e.g., 140px always means 140px)
    # For encode videos: crop first (if any), then resize (but resize should be None)
    
    if is_source:
        # SOURCE: Resize first, then crop at target resolution
        # This prevents scaling crop values - 140px always means 140px regardless of source resolution
        
        # Apply resizing first for source videos
        if resize and resize != (clip.width, clip.height):
            target_width, target_height = resize
            colored_print(f"  [TOOL] Resizing from {clip.width}x{clip.height} to {target_width}x{target_height} using Spline36", Colors.YELLOW)
            clip = core.resize.Spline36(clip, width=target_width, height=target_height)
        
        # Apply cropping after resizing for source videos (crop values at target resolution)
        if crop:
            if crop == "auto":
                # Auto-detect crop using cropdetect
                colored_print(f"  [INFO] Auto-detecting crop for better comparison...", Colors.CYAN)
                try:
                    # Use awsmfunc for auto crop detection if available
                    if awf and hasattr(awf, 'CropResize'):
                        clip = awf.CropResize(clip, width=clip.width, height=clip.height)
                        colored_print(f"  [OK] Applied auto-crop", Colors.GREEN)
                    else:
                        # Fallback to manual crop detection
                        # Sample a few frames to detect crop
                        test_frames = [clip.num_frames // 4, clip.num_frames // 2, clip.num_frames * 3 // 4]
                        colored_print(f"  [INFO] Analyzing frames {test_frames} for crop detection...", Colors.BLUE)
                        # For now, just continue without cropping if awsmfunc is not available
                        colored_print(f"  [WARN] Auto-crop not available, continuing without crop", Colors.YELLOW)
                except Exception as e:
                    colored_print(f"  [ERROR] Auto-crop failed: {e}, continuing without crop", Colors.RED)
            elif isinstance(crop, dict):
                # Manual cropping at target resolution
                left = crop.get('left', 0)
                right = crop.get('right', 0)
                top = crop.get('top', 0)
                bottom = crop.get('bottom', 0)
                
                if left or right or top or bottom:
                    new_width = clip.width - left - right
                    new_height = clip.height - top - bottom
                    
                    # Validate crop values
                    if new_width <= 0 or new_height <= 0:
                        colored_print(f"  [ERROR] Invalid crop values would result in {new_width}x{new_height}", Colors.RED)
                        colored_print(f"  [ERROR] Current: {clip.width}x{clip.height}, Crop: L={left}, R={right}, T={top}, B={bottom}", Colors.RED)
                        colored_print(f"  [ERROR] Skipping crop to prevent errors", Colors.RED)
                    elif new_width < 100 or new_height < 100:
                        colored_print(f"  [WARN] Crop results in very small resolution: {new_width}x{new_height}", Colors.YELLOW)
                        colored_print(f"  [WARN] This may not be intended - please verify crop values", Colors.YELLOW)
                        clip = core.std.Crop(clip, left=left, right=right, top=top, bottom=bottom)
                        colored_print(f"  [?[CROP] Applied crop: left={left}, right={right}, top={top}, bottom={bottom}", Colors.CYAN)
                        colored_print(f"  [?[RES] New resolution after crop: {new_width}x{new_height}", Colors.GREEN)
                    else:
                        clip = core.std.Crop(clip, left=left, right=right, top=top, bottom=bottom)
                        colored_print(f"  [?[CROP] Applied crop: left={left}, right={right}, top={top}, bottom={bottom}", Colors.CYAN)
                        colored_print(f"  [?[RES] New resolution after crop: {new_width}x{new_height}", Colors.GREEN)
    else:
        # ENCODE: Crop first (if any), then resize
        # Apply cropping first for encode videos (unusual but possible)
        if crop:
            if crop == "auto":
                colored_print(f"  [INFO] Auto-detecting crop...", Colors.CYAN)
                try:
                    if awf and hasattr(awf, 'CropResize'):
                        clip = awf.CropResize(clip, width=clip.width, height=clip.height)
                        colored_print(f"  [OK] Applied auto-crop", Colors.GREEN)
                    else:
                        colored_print(f"  [WARN] Auto-crop not available, continuing without crop", Colors.YELLOW)
                except Exception as e:
                    colored_print(f"  [ERROR] Auto-crop failed: {e}, continuing without crop", Colors.RED)
            elif isinstance(crop, dict):
                left = crop.get('left', 0)
                right = crop.get('right', 0)
                top = crop.get('top', 0)
                bottom = crop.get('bottom', 0)
                
                if left or right or top or bottom:
                    new_width = clip.width - left - right
                    new_height = clip.height - top - bottom
                    
                    # Validate crop values
                    if new_width <= 0 or new_height <= 0:
                        colored_print(f"  [ERROR] Invalid crop values would result in {new_width}x{new_height}", Colors.RED)
                        colored_print(f"  [ERROR] Original: {clip.width}x{clip.height}, Crop: L={left}, R={right}, T={top}, B={bottom}", Colors.RED)
                        colored_print(f"  [ERROR] Skipping crop to prevent errors", Colors.RED)
                    elif new_width < 100 or new_height < 100:
                        colored_print(f"  [WARN] Crop results in very small resolution: {new_width}x{new_height}", Colors.YELLOW)
                        colored_print(f"  [WARN] This may not be intended - please verify crop values", Colors.YELLOW)
                        clip = core.std.Crop(clip, left=left, right=right, top=top, bottom=bottom)
                        colored_print(f"  [?[CROP] Applied crop: left={left}, right={right}, top={top}, bottom={bottom}", Colors.CYAN)
                        colored_print(f"  [?[RES] New resolution: {new_width}x{new_height}", Colors.GREEN)
                    else:
                        clip = core.std.Crop(clip, left=left, right=right, top=top, bottom=bottom)
                        colored_print(f"  [?[CROP] Applied crop: left={left}, right={right}, top={top}, bottom={bottom}", Colors.CYAN)
                        colored_print(f"  [?[RES] New resolution: {new_width}x{new_height}", Colors.GREEN)
        
        # Apply resizing after cropping for encode videos
        # NOTE: In source vs encode mode, encode videos should NEVER be resized
        # This check is here as a safeguard, but resize should already be None for encodes
        if resize and resize != (clip.width, clip.height):
            if not is_source:
                colored_print(f"  [WARN] WARNING: Resize was requested for encode video but will be skipped to prevent upscaling", Colors.YELLOW, bold=True)
                colored_print(f"  [?[KEEP] Keeping original encode resolution: {clip.width}x{clip.height}", Colors.CYAN)
            else:
                target_width, target_height = resize
                colored_print(f"  [TOOL] Resizing from {clip.width}x{clip.height} to {target_width}x{target_height} using Spline36", Colors.YELLOW)
                clip = core.resize.Spline36(clip, width=target_width, height=target_height)
    
    # Apply trimming
    if trim_start > 0 or trim_end > 0:
        end_frame = clip.num_frames - trim_end if trim_end > 0 else clip.num_frames
        clip = clip[trim_start:end_frame]
        colored_print(f"  [?[TRIM] Applied trim: start={trim_start}, end={trim_end}", Colors.BLUE)
    
    # Apply padding
    if pad_start > 0:
        blank_start = core.std.BlankClip(clip, length=pad_start)
        clip = blank_start + clip
        colored_print(f"  [?] Added {pad_start} blank frames at start", Colors.BLUE)
    
    if pad_end > 0:
        blank_end = core.std.BlankClip(clip, length=pad_end)
        clip = clip + blank_end
        colored_print(f"  [?] Added {pad_end} blank frames at end", Colors.BLUE)
    
    return clip

# ROLLBACK OPTION: If resize-first approach doesn't work well, uncomment the code below
# and comment out the current apply_processing function above

"""
# ROLLBACK: Original crop-first approach for sources
def apply_processing_crop_first(clip, trim_start=0, trim_end=0, pad_start=0, pad_end=0, crop=None, resize=None, is_source=False):
    # For source videos: Apply cropping first (at original resolution), then resizing
    # For encode videos: Apply cropping first (if any), then resizing
    
    if is_source:
        # SOURCE: Crop first at original resolution, then resize
        # This ensures proper letterbox/pillarbox removal before scaling
        
        # Apply cropping first for source videos to remove letterbox/pillarbox
        if crop and isinstance(crop, dict):
            left = crop.get('left', 0)
            right = crop.get('right', 0)
            top = crop.get('top', 0)
            bottom = crop.get('bottom', 0)
            
            if left or right or top or bottom:
                new_width = clip.width - left - right
                new_height = clip.height - top - bottom
                
                if new_width > 0 and new_height > 0:
                    clip = core.std.Crop(clip, left=left, right=right, top=top, bottom=bottom)
                    colored_print(f"  [?[CROP] Applied crop: left={left}, right={right}, top={top}, bottom={bottom}", Colors.CYAN)
                    colored_print(f"  [?[RES] New resolution after crop: {new_width}x{new_height}", Colors.GREEN)
        
        # Apply resizing after cropping for source videos with aspect ratio adjustment
        if resize and resize != (clip.width, clip.height):
            target_width, target_height = resize
            
            # For source videos with cropping: adjust resize target to maintain aspect ratio after crop
            if crop and isinstance(crop, dict):
                cropped_aspect_ratio = clip.width / clip.height
                calculated_height = int(target_width / cropped_aspect_ratio)
                colored_print(f"  [TOOL] Resizing from {clip.width}x{clip.height} to {target_width}x{calculated_height} (aspect-ratio-aware)", Colors.YELLOW)
                clip = core.resize.Spline36(clip, width=target_width, height=calculated_height)
            else:
                colored_print(f"  [TOOL] Resizing from {clip.width}x{clip.height} to {target_width}x{target_height} using Spline36", Colors.YELLOW)
                clip = core.resize.Spline36(clip, width=target_width, height=target_height)
    
    # Apply trimming and padding as usual
    # ... rest of function ...
    
    return clip
"""

def upload_to_slowpics(config, frames, processed_videos):
    """
    Upload screenshots to slow.pics using working logic from comp.py.
    """
    print_header("UPLOADING TO SLOW.PICS")
    
    # Generate collection name
    source_names = [video['name'] for video in processed_videos]
    vs_string = " vs ".join(source_names)
    
    if config['season_number']:
        collection_name = f"{config['show_name']} {config['season_number']} {vs_string}"
    else:
        collection_name = f"{config['show_name']} {vs_string}"
    
    colored_print(f"[?[NAME] Collection name: {collection_name}", Colors.CYAN, bold=True)
    
    try:
        # Generate browser ID
        browserId = str(uuid.uuid4())
        
        # Get all image files organized by frame number
        base_screenshots_folder = "Screenshots"
        all_image_files = []
        
        # Collect all PNG files from all source folders
        for video in processed_videos:
            source_folder = os.path.join(base_screenshots_folder, video['name'])
            if os.path.exists(source_folder):
                png_files = [f for f in os.listdir(source_folder) if f.endswith('.png')]
                for png_file in png_files:
                    full_path = os.path.join(source_folder, png_file)
                    all_image_files.append(full_path)
        
        # Sort files to ensure consistent ordering
        all_image_files.sort()
        
        # Verify we have the expected number of images
        expected_images = len(frames) * len(processed_videos)
        if len(all_image_files) < expected_images:
            print(f"Warning: Expected {expected_images} images but found {len(all_image_files)}")
            # Wait a bit and check again
            import time
            time.sleep(2)
            all_image_files = []
            for video in processed_videos:
                source_folder = os.path.join(base_screenshots_folder, video['name'])
                if os.path.exists(source_folder):
                    png_files = [f for f in os.listdir(source_folder) if f.endswith('.png')]
                    for png_file in png_files:
                        full_path = os.path.join(source_folder, png_file)
                        all_image_files.append(full_path)
            all_image_files.sort()
            
            if len(all_image_files) < expected_images:
                raise Exception(f"Missing image files. Expected {expected_images}, found {len(all_image_files)}")
        
        # Build the comparison data structure like comp.py
        fields = {
            'collectionName': collection_name,
            'hentai': 'false',
            'optimize-images': 'true',
            'browserId': browserId,
            'public': 'true'
        }
        
        # Add comparison data for each frame (like comp.py)
        for x in range(0, len(frames)):
            fields[f'comparisons[{x}].name'] = str(frames[x])
            
            # Add image names for this frame
            for i, video in enumerate(processed_videos):
                fields[f'comparisons[{x}].imageNames[{i}]'] = video['name']
        
        colored_print(f"[INFO] Found {len(frames)} frames with {len(processed_videos)} sources each", Colors.BLUE, bold=True)
        
        # Start upload process
        with Session() as sess:
            # Get the initial page to establish session and get XSRF token
            colored_print("[LINK] Establishing session...", Colors.CYAN)
            sess.get('https://slow.pics/comparison')
            
            # Create the comparison
            files = MultipartEncoder(fields, str(uuid.uuid4()))
            
            colored_print("[COPY] Creating comparison...", Colors.CYAN)
            comp_req = sess.post(
                'https://slow.pics/upload/comparison', 
                data=files.to_string(),
                headers=_get_slowpics_header(str(files.len), files.content_type, sess)
            )
            
            if comp_req.status_code != 200:
                raise Exception(f"Failed to create comparison. Status: {comp_req.status_code}, Response: {comp_req.text}")
            
            comp_response = comp_req.json()
            collection = comp_response["collectionUuid"]
            key = comp_response["key"]
            
            colored_print("[?] Comparison created, uploading images...", Colors.GREEN, bold=True)
            
            # Upload each image frame by frame, source by source
            total_images = len(frames) * len(processed_videos)
            uploaded = 0
            
            for frame_index, frame_num in enumerate(frames):
                image_section = comp_response["images"][frame_index]
                
                for source_index, video in enumerate(processed_videos):
                    source_folder = os.path.join(base_screenshots_folder, video['name'])
                    
                    # Find the specific image file for this frame and source
                    expected_filename = f"{video['name']}_{frame_num:06d}.png"
                    image_path = os.path.join(source_folder, expected_filename)
                    
                    if not os.path.exists(image_path):
                        # Fallback: look for any file matching the pattern
                        pattern_files = [f for f in os.listdir(source_folder) 
                                       if f.startswith(f"{video['name']}_{frame_num:06d}") and f.endswith('.png')]
                        
                        if not pattern_files:
                            raise Exception(f"Could not find image for {video['name']} frame {frame_num}")
                        
                        image_path = os.path.join(source_folder, pattern_files[0])
                    image_id = image_section[source_index]
                    
                    upload_info = {
                        "collectionUuid": collection,
                        "imageUuid": image_id,
                        "file": (os.path.basename(image_path), pathlib.Path(image_path).read_bytes(), 'image/png'),
                        'browserId': browserId,
                    }
                    
                    upload_info_encoded = MultipartEncoder(upload_info, str(uuid.uuid4()))
                    upload_response = sess.post(
                        'https://slow.pics/upload/image', 
                        data=upload_info_encoded.to_string(),
                        headers=_get_slowpics_header(str(upload_info_encoded.len), upload_info_encoded.content_type, sess)
                    )
                    
                    if upload_response.status_code != 200 or upload_response.content.decode() != "OK":
                        raise Exception(f"Failed to upload image {os.path.basename(image_path)}. Status: {upload_response.status_code}")
                    
                    uploaded += 1
                    progress = (uploaded / total_images) * 100
                    colored_print(f"[REFRESH] Progress: {uploaded}/{total_images} images uploaded ({progress:.1f}%)", Colors.BLUE, end='\r')
            
            colored_print(f"\n[OK] Upload complete!", Colors.GREEN, bold=True)
            
        slowpics_url = f'https://slow.pics/c/{key}'
        colored_print(f"[WEB] Comparison URL: {slowpics_url}", Colors.CYAN, bold=True)
        
        # Open URL directly in browser
        try:
            webbrowser.open(slowpics_url)
            colored_print("[START] Opening comparison in your default browser...", Colors.GREEN, bold=True)
        except Exception as e:
            colored_print(f"[WARN] Could not open browser: {e}", Colors.YELLOW)
        
        return slowpics_url
        
    except Exception as e:
        colored_print(f"[ERROR] Upload failed: {str(e)}", Colors.RED, bold=True)
        colored_print("[TIP] Screenshots are saved in the Screenshots folder if you want to upload manually.", Colors.YELLOW)
        return None

# =============================================================================
# DEMO AND HELP FUNCTIONS
# ==============================================================================

def show_help():
    """Show help information"""
    print_header("ENHANCED VAPOURSYNTH SCREENSHOT COMPARISON TOOL")
    
    colored_print("[MODE] FEATURES:", Colors.CYAN, bold=True)
    colored_print("[?] Dynamic library detection (VapourSynth, OpenCV, PIL fallback)", Colors.WHITE)
    colored_print("[?] Multiple video source comparison", Colors.WHITE) 
    colored_print("[?] Source vs Encode comparison", Colors.WHITE)
    colored_print("[?] Automatic slow.pics upload", Colors.WHITE)
    
    colored_print("\n[START] USAGE:", Colors.GREEN, bold=True)
    colored_print("python comparev2.py              # Interactive mode", Colors.WHITE)
    colored_print("python comparev2.py --help       # Show this help", Colors.WHITE)
    colored_print("python comparev2.py --demo       # Show available backends", Colors.WHITE)

def show_demo():
    """Show detected backends and capabilities"""
    print_header("DETECTED VIDEO PROCESSING BACKENDS")
    
    colored_print("[INFO] Library Detection Results:", Colors.CYAN, bold=True)
    
    # Show VapourSynth status
    if VAPOURSYNTH_AVAILABLE:
        colored_print("[OK] VapourSynth: Available", Colors.GREEN, bold=True)
        if awf:
            colored_print("   awsmfunc: Available", Colors.GREEN)
        else:
            colored_print("   awsmfunc: Not found", Colors.YELLOW)
    else:
        colored_print("[ERROR] VapourSynth: Not available", Colors.RED)
    
    # Show OpenCV status 
    if OPENCV_AVAILABLE:
        colored_print("[OK] OpenCV: Available", Colors.GREEN, bold=True)
    else:
        colored_print("[ERROR] OpenCV: Not available", Colors.RED)
    
    # Show PIL status
    if PIL_AVAILABLE:
        colored_print("[OK] PIL/Pillow: Available", Colors.GREEN, bold=True)
    else:
        colored_print("[ERROR] PIL/Pillow: Not available", Colors.RED)
    
    # Show NumPy status
    if NUMPY_AVAILABLE:
        colored_print("[OK] NumPy: Available", Colors.GREEN, bold=True)
    else:
        colored_print("[ERROR] NumPy: Not available", Colors.RED)
    
    colored_print(f"\n[MODE] Active Processing Mode: {PROCESSING_MODE.upper()}", Colors.CYAN, bold=True)

def add_frame_info(clip_or_data, title):
    """Add frame information overlay - works with both VapourSynth and fallback modes"""
    if processor.mode == "vapoursynth":
        def frame_props(n, f):
            # Get frame type (I, P, B frame)
            frame_type = f.props.get('_PictType', b'?').decode('utf-8') if '_PictType' in f.props else '?'
            
            # Create enhanced text with emojis and better formatting
            main_text = f"Frame: {n:06d} | {frame_type}-Frame | {title}"
            
            # Use the basic VapourSynth text function with correct parameters
            # alignment=7 is top-left, scale makes text larger
            text_clip = core.text.Text(clip_or_data, main_text, alignment=7, scale=1)
            
            return text_clip
        
        return core.std.FrameEval(clip_or_data, frame_props, prop_src=clip_or_data)
    else:
        # For non-VapourSynth modes, return data structure with overlay info
        return {
            'data': clip_or_data,
            'title': title,
            'overlay_enabled': True
        }

def apply_frame_processing(video_data, frame_number):
    """Apply processing to a single frame in fallback modes"""
    if processor.mode == "vapoursynth":
        return video_data  # Already processed
    
    # Extract processing parameters
    video = video_data['data']['video']
    trim_start = video_data['data']['trim_start']
    trim_end = video_data['data']['trim_end']
    crop = video_data['data']['crop']
    resize_target = video_data['data']['resize_target']
    
    # Calculate adjusted frame number
    adjusted_frame = frame_number + trim_start
    
    # Get the frame
    frame = processor.get_frame(video, adjusted_frame)
    
    # Apply cropping if specified
    if crop and crop != "auto":
        if isinstance(crop, dict):
            frame = processor.crop_frame(frame, crop['left'], crop['top'], crop['right'], crop['bottom'])
    
    # Apply resizing if specified
    if resize_target:
        frame = processor.resize_frame(frame, resize_target[0], resize_target[1])
    
    # Add text overlay if enabled
    if video_data.get('overlay_enabled', False):
        title = video_data['title']
        text = f"Frame: {frame_number:06d} | Source: {title}"
        frame = processor.add_text_overlay(frame, text)
    
    return frame

def process_and_generate_screenshots(config):
    """Complete video processing and screenshot generation pipeline"""
    
    # Initialize video storage
    processed_videos = []
    video_info_clips = []

    print_header(f"LOADING AND PROCESSING {len(config['videos'])} VIDEO SOURCES")

    # Load and process each video
    for i, video_config in enumerate(config['videos']):
        colored_print(f"[VIDEO] Loading {video_config['name']}: {video_config['path']}", Colors.CYAN, bold=True)
        
        try:
            # Load video using dynamic processor
            video_clip = processor.load_video(video_config['path'])
            
            # Get video properties
            if processor.mode == "vapoursynth":
                original_frames = len(video_clip)
                original_width, original_height = video_clip.width, video_clip.height
            elif processor.mode == "opencv":
                original_frames = processor.get_frame_count(video_clip)
                original_width = int(video_clip.get(cv2.CAP_PROP_FRAME_WIDTH))
                original_height = int(video_clip.get(cv2.CAP_PROP_FRAME_HEIGHT))
            else:
                # PIL mode - limited support
                original_frames = 1
                original_width, original_height = 1920, 1080
            
            # Determine resize target for this video
            resize_target = None
            resize_config = config.get('resize_config', {})
            
            if resize_config.get('resize_method') == 'individual':
                # Check if this video has individual resize settings
                if video_config['name'] in resize_config.get('individual_resizes', {}):
                    resize_target = resize_config['individual_resizes'][video_config['name']]
            elif resize_config.get('resize_method') == 'common':
                # Use common resolution for all videos
                resize_target = resize_config.get('common_resolution')
            
            # Determine if this is a source video
            is_source = video_config.get('is_source', False)
            if config.get('comparison_type') == 'multiple_sources':
                is_source = True  # All videos in multiple sources mode are treated as sources
            
            # Apply processing (including cropping and resizing with proper order)
            if processor.mode == "vapoursynth":
                processed_clip = apply_processing(
                    video_clip,
                    video_config['trim_start'],
                    video_config['trim_end'],
                    video_config['pad_start'],
                    video_config['pad_end'],
                    video_config.get('crop', None),
                    resize_target,
                    is_source
                )
                processed_frames = len(processed_clip)
                processed_width, processed_height = processed_clip.width, processed_clip.height
            else:
                # For non-VapourSynth modes, store video object and processing parameters
                # Processing will be done per-frame during screenshot generation
                processed_clip = {
                    'video': video_clip,
                    'trim_start': video_config['trim_start'],
                    'trim_end': video_config['trim_end'],
                    'pad_start': video_config['pad_start'],
                    'pad_end': video_config['pad_end'],
                    'crop': video_config.get('crop', None),
                    'resize_target': resize_target,
                    'is_source': is_source,
                    'original_width': original_width,
                    'original_height': original_height
                }
                processed_frames = original_frames  # Will be calculated properly later
                processed_width, processed_height = resize_target if resize_target else (original_width, original_height)
            
            processed_videos.append({
                'clip': processed_clip,
                'name': video_config['name'],
                'original_frames': original_frames,
                'processed_frames': processed_frames
            })
            
            colored_print(f"  [INFO] Original frames: {original_frames}", Colors.WHITE)
            colored_print(f"  [MODE] Processed frames: {processed_frames}", Colors.GREEN)
            colored_print(f"  [📐] Original resolution: {original_width}x{original_height}", Colors.WHITE)
            colored_print(f"  [🎯] Final resolution: {processed_width}x{processed_height}", Colors.GREEN)
            
            # Show resize info if applied
            if resize_target and resize_target != (original_width, original_height):
                colored_print(f"  [🔧] Resized: {original_width}x{original_height} → {resize_target[0]}x{resize_target[1]}", Colors.YELLOW)
            
            # Only show trim/pad info for multiple sources comparison
            if config.get('comparison_type') == 'multiple_sources':
                if video_config['trim_start'] or video_config['trim_end']:
                    colored_print(f"  [✂️] Trimmed: start={video_config['trim_start']}, end={video_config['trim_end']}", Colors.BLUE)
                if video_config['pad_start'] or video_config['pad_end']:
                    colored_print(f"  [📏] Padded: start={video_config['pad_start']}, end={video_config['pad_end']}", Colors.BLUE)
            
            # Show crop info if applied
            if video_config.get('crop'):
                if video_config['crop'] == "auto":
                    colored_print(f"  [INFO] Cropping: Auto-detected", Colors.MAGENTA)
                elif isinstance(video_config['crop'], dict):
                    crop = video_config['crop']
                    colored_print(f"  [✂️] Cropping: Manual (L:{crop['left']}, R:{crop['right']}, T:{crop['top']}, B:{crop['bottom']})", Colors.MAGENTA)
        
        except Exception as e:
            colored_print(f"[ERROR] Failed to load video {video_config['name']}: {e}", Colors.RED, bold=True)
            colored_print(f"[TIP] Check that the file path is correct and the video format is supported", Colors.YELLOW)
            continue

    if not processed_videos:
        colored_print(f"[ERROR] No videos were successfully loaded!", Colors.RED, bold=True)
        return False

    # Generate frame numbers for comparison
    total_frames = min(video['processed_frames'] for video in processed_videos)

    if config['custom_frames']:
        # Use custom frame numbers
        frames = [f for f in config['custom_frames'] if 0 <= f < total_frames]
        colored_print(f"\n[MODE] Using custom frames: {frames}", Colors.BLUE, bold=True)
        if len(frames) != len(config['custom_frames']):
            excluded = [f for f in config['custom_frames'] if f >= total_frames]
            colored_print(f"[WARN] Excluded frames beyond video length: {excluded}", Colors.YELLOW)
    else:
        # Use frame interval
        frames = list(range(0, total_frames, config['frame_interval']))
        colored_print(f"\n[📊] Using frame interval {config['frame_interval']}: {len(frames)} screenshots will be generated", Colors.BLUE, bold=True)

    colored_print(f"[INFO] Total frames available for comparison: {total_frames}", Colors.BLUE, bold=True)
    colored_print(f"[📸] Number of screenshots to generate: {len(frames)}", Colors.GREEN, bold=True)
    colored_print(f"[📈] Total screenshots to generate: {len(frames) * len(processed_videos)}", Colors.MAGENTA, bold=True)

    # Apply frame info to all video clips
    for i, video in enumerate(processed_videos):
        if processor.mode == "vapoursynth":
            video_info_clip = add_frame_info(video['clip'], video['name'])
            video_info_clips.append({
                'clip': video_info_clip,
                'name': video['name']
            })
        else:
            # For fallback modes, store processing data
            video_info_clips.append({
                'clip': add_frame_info(video['clip'], video['name']),
                'name': video['name']
            })

    # Execute screenshot generation
    print_header("GENERATING SCREENSHOTS")
    colored_print(f"[VIDEO] Processing {len(frames)} frames from {len(processed_videos)} sources...", Colors.CYAN, bold=True)
    colored_print(f"[📊] Total screenshots to generate: {len(frames) * len(processed_videos)}", Colors.MAGENTA, bold=True)
    colored_print(f"[🔧] Using {processor.mode.upper()} processor", Colors.BLUE, bold=True)
    
    # Generate screenshots using the robust function
    success = generate_screenshots_robust(frames, video_info_clips)
    
    if success:
        colored_print(f"\n[✅] Generated {len(frames) * len(processed_videos)} screenshots in source-specific folders", Colors.GREEN, bold=True)
        
        print_header(f"{config.get('comparison_type', 'multiple_sources').replace('_', ' ').title()} Summary")
        
        for video in processed_videos:
            colored_print(f"[OK] {video['name']}: {video['processed_frames']} frames (original: {video['original_frames']})", Colors.GREEN)
            if processor.mode == "vapoursynth":
                # Need to get actual processed clip for VapourSynth mode
                processed_clip = video['clip']
                if hasattr(processed_clip, 'width') and hasattr(processed_clip, 'height'):
                    colored_print(f"    [📐] Resolution: {processed_clip.width}x{processed_clip.height}", Colors.CYAN)
                else:
                    colored_print(f"    [📐] Resolution: Processing applied", Colors.CYAN)
            else:
                # For fallback modes, show target resolution
                video_data = video['clip']
                if isinstance(video_data, dict):
                    resize_target = video_data.get('resize_target')
                    if resize_target:
                        colored_print(f"    [🎯] Target resolution: {resize_target[0]}x{resize_target[1]}", Colors.CYAN)
                    else:
                        original_w = video_data.get('original_width', 1920)
                        original_h = video_data.get('original_height', 1080)
                        colored_print(f"    [📐] Resolution: {original_w}x{original_h}", Colors.CYAN)
        
        colored_print(f"\n[📁] Screenshots organized by source:", Colors.YELLOW, bold=True)
        for video in processed_videos:
            colored_print(f"  - Screenshots/{video['name']}/", Colors.CYAN)
        colored_print(f"[📋] Filename pattern: SourceName_000000.png", Colors.WHITE)
        colored_print(f"[MODE] Frame numbers used: {frames}", Colors.BLUE)
        colored_print(f"[🔧] Using {processor.mode.upper()} backend for frame processing", Colors.MAGENTA)
        
        if config.get('comparison_type') == 'source_vs_encode':
            colored_print(f"[🆚] Source vs Encode comparison with cropping support", Colors.GREEN, bold=True)
        else:
            colored_print(f"[📁] Multiple sources comparison", Colors.GREEN, bold=True)
        
        # Show resize information
        resize_config = config.get('resize_config', {})
        if resize_config.get('resize_method') == 'individual':
            individual_resizes = resize_config.get('individual_resizes', {})
            if individual_resizes:
                colored_print(f"[🔧] Individual video resizing applied using Spline36:", Colors.YELLOW, bold=True)
                for name, resolution in individual_resizes.items():
                    colored_print(f"    {name}: resized to {resolution[0]}x{resolution[1]}", Colors.CYAN)
            else:
                colored_print(f"[📐] No individual resizing applied", Colors.WHITE)
        elif resize_config.get('resize_method') == 'common':
            common_res = resize_config.get('common_resolution')
            colored_print(f"[🔧] All videos resized to {common_res[0]}x{common_res[1]} using Spline36", Colors.YELLOW, bold=True)
        elif resize_config.get('resize_method') == 'none':
            colored_print(f"[📐] Original resolutions maintained", Colors.WHITE)
        
        # Show processing order for source vs encode
        if config.get('comparison_type') == 'source_vs_encode':
            # Count sources and show comparison order
            source_videos = [v for v in processed_videos if v.get('name') != 'Encode']
            encode_videos = [v for v in processed_videos if v.get('name') == 'Encode']
            
            if len(source_videos) == 1:
                colored_print(f"[🔄] Comparison order: {source_videos[0]['name']} vs Encode", Colors.BLUE, bold=True)
            else:
                source_names = [v['name'] for v in source_videos]
                colored_print(f"[🔄] Comparison order: {source_names[0]} vs Encode vs {' vs '.join(source_names[1:])}", Colors.BLUE, bold=True)
            
            colored_print(f"[📋] Processing order: Sources (resize → crop), Encode (crop only - NO RESIZE)", Colors.MAGENTA)
            colored_print(f"[WARN] Encode videos are never resized to prevent unwanted upscaling", Colors.YELLOW, bold=True)
        
        # Upload to slow.pics if requested
        if config['upload_to_slowpics']:
            comparison_url = upload_to_slowpics(config, frames, processed_videos)
            if comparison_url:
                colored_print(f"\n[🌐] Your comparison has been uploaded and opened in your browser!", Colors.GREEN, bold=True)
            else:
                colored_print(f"\n[📁] Screenshots are available locally in the Screenshots/ folder", Colors.BLUE, bold=True)
        else:
            colored_print(f"\n[📁] Screenshots saved locally in the Screenshots/ folder", Colors.BLUE, bold=True)
        
        return True
    else:
        colored_print(f"\n[❌] Screenshot generation failed!", Colors.RED, bold=True)
        return False

def generate_screenshots(frames, video_info_clips):
    """Compatibility wrapper for GUI import - delegates to generate_screenshots_robust"""
    return generate_screenshots_robust(frames, video_info_clips)

def generate_screenshots_robust(frames, video_info_clips):
    """Robust screenshot generation that works across all backends"""
    base_screenshots_folder = "Screenshots"
    os.makedirs(base_screenshots_folder, exist_ok=True)
    
    # Clean up existing screenshots when generating new ones
    colored_print(f"[🧹] Cleaning up existing screenshots...", Colors.YELLOW)
    for video_info in video_info_clips:
        source_folder = os.path.join(base_screenshots_folder, video_info['name'])
        if os.path.exists(source_folder):
            # Remove all PNG files from the source folder
            for file in os.listdir(source_folder):
                if file.endswith('.png'):
                    file_path = os.path.join(source_folder, file)
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        colored_print(f"[WARN] Warning: Could not remove {file_path}: {e}", Colors.YELLOW)
            colored_print(f"  [OK] Cleaned Screenshots/{video_info['name']}/", Colors.GREEN)
        else:
            os.makedirs(source_folder, exist_ok=True)
            colored_print(f"  [📁] Created Screenshots/{video_info['name']}/", Colors.CYAN)
    
    colored_print(f"\n[📸] Generating {len(frames)} screenshots for {len(video_info_clips)} sources...", Colors.MAGENTA, bold=True)
    
    success_count = 0
    error_count = 0
    
    if processor.mode == "vapoursynth":
        # VapourSynth mode - use improved PIL-based saving instead of fpng
        for i, frame_num in enumerate(frames):
            progress = (i + 1) / len(frames) * 100
            colored_print(f"[🔄] Processing frame {frame_num} ({i+1}/{len(frames)}) - {progress:.1f}%", Colors.BLUE)
            
            for video_info in video_info_clips:
                try:
                    # Create source-specific folder
                    source_folder = os.path.join(base_screenshots_folder, video_info['name'])
                    os.makedirs(source_folder, exist_ok=True)
                    
                    # Get single frame from VapourSynth clip
                    src_frame = video_info['clip'][frame_num:frame_num+1]
                    
                    # Save using the processor's improved save method
                    filename = os.path.join(source_folder, f"{video_info['name']}_{frame_num:06d}.png")
                    processor.save_frame_as_png(src_frame, filename)
                    
                    success_count += 1
                    
                except Exception as e:
                    colored_print(f"[ERROR] Error processing frame {frame_num} for {video_info['name']}: {e}", Colors.RED)
                    error_count += 1
    
    else:
        # Fallback mode - process frames individually  
        for i, frame_num in enumerate(frames):
            progress = (i + 1) / len(frames) * 100
            colored_print(f"[🔄] Processing frame {frame_num} ({i+1}/{len(frames)}) - {progress:.1f}%", Colors.BLUE)
            
            for video_info in video_info_clips:
                try:
                    # Create source-specific folder
                    source_folder = os.path.join(base_screenshots_folder, video_info['name'])
                    os.makedirs(source_folder, exist_ok=True)
                    
                    # Process the frame
                    processed_frame = apply_frame_processing(video_info['clip'], frame_num)
                    
                    # Save the frame
                    filename = os.path.join(source_folder, f"{video_info['name']}_{frame_num:06d}.png")
                    processor.save_frame_as_png(processed_frame, filename)
                    
                    success_count += 1
                    
                except Exception as e:
                    colored_print(f"[ERROR] Error processing frame {frame_num} for {video_info['name']}: {e}", Colors.RED)
                    error_count += 1
    
    # Report results
    total_expected = len(frames) * len(video_info_clips)
    colored_print(f"\n[📊] Screenshot generation complete:", Colors.GREEN, bold=True)
    colored_print(f"  [✅] Successfully generated: {success_count}/{total_expected}", Colors.GREEN)
    if error_count > 0:
        colored_print(f"  [❌] Errors encountered: {error_count}", Colors.RED)
    
    return success_count > 0

# =============================================================================
# COMMAND LINE ARGUMENT PARSING
# ==============================================================================

# Only run main execution code when script is executed directly, not when imported
if __name__ == "__main__":
    # Check for basic help/demo/version arguments only
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['--help', '-h', 'help']:
            show_help()
            sys.exit(0)
        elif arg in ['--demo', '-d', 'demo']:
            show_demo()
            sys.exit(0)
        elif arg in ['--version', '-v']:
            colored_print("Enhanced VapourSynth Screenshot Comparison Tool v2.0", Colors.CYAN, bold=True)
            colored_print("Dynamic backend support with VapourSynth, OpenCV, and PIL fallbacks", Colors.CYAN)
            sys.exit(0)

    # Run in interactive mode only
    try:
        config = get_user_input()

        # Check if this is upload-only mode
        if config.get('upload_only', False):
            print_header("UPLOAD ONLY MODE")
            colored_print(f"Uploading existing screenshots to slow.pics...", Colors.BLUE, bold=True)
            
            # Use existing data from config
            frames = config['frames']
            processed_videos = config['processed_videos']
            
            colored_print(f"Found {len(frames)} frames and {len(processed_videos)} sources", Colors.GREEN)
            
            # Upload to slow.pics
            comparison_url = upload_to_slowpics(config, frames, processed_videos)
            if comparison_url:
                colored_print(f"\n[🌐] Your comparison has been uploaded and opened in your browser!", Colors.GREEN, bold=True)
            else:
                colored_print(f"\n[📁] Screenshots are available locally in the Screenshots/ folder", Colors.BLUE, bold=True)
            
            colored_print("\n[✅] Upload complete!", Colors.GREEN, bold=True)
            sys.exit(0)

        # Normal screenshot generation mode
        colored_print(f"\n[🎬] Starting {config.get('comparison_type', 'multiple_sources').replace('_', ' ').title()} processing...", Colors.CYAN, bold=True)
        
        # Process videos and generate screenshots
        success = process_and_generate_screenshots(config)
        
        if success:
            colored_print(f"\n[✅] All operations completed successfully!", Colors.GREEN, bold=True)
        else:
            colored_print(f"\n[❌] Some operations failed. Check the logs above for details.", Colors.RED, bold=True)
            sys.exit(1)
            
    except KeyboardInterrupt:
        colored_print(f"\n[⚠️] Operation cancelled by user", Colors.YELLOW, bold=True)
        sys.exit(0)
    except Exception as e:
        colored_print(f"\n[❌] Unexpected error: {e}", Colors.RED, bold=True)
        colored_print(f"[🔧] Traceback:", Colors.YELLOW)
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Usage:
# Simply run: python comparev2.py
# Follow the interactive prompts to configure your comparison