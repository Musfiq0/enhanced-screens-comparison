#!/usr/bin/env python3
"""
Command Line Interface for Enhanced VapourSynth Screenshot Comparison Tool

A true command-line version of the interactive console from comparev2.py.
Uses VapourSynth for all video operations without external encoding.

Version: 2.0 - CLI Edition
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Import core functionality from comparev2.py
try:
    from comparev2 import (
        # Core functions and classes
        create_video_processor, processor,
        print_header, colored_print, Colors,
        
        # Processing functions we'll use
        vs, core, VAPOURSYNTH_AVAILABLE, OPENCV_AVAILABLE, PIL_AVAILABLE,
        
        # Main processing and upload functions
        process_and_generate_screenshots, upload_to_slowpics,
        get_screenshot_and_upload_config, get_upload_only_config,
        
        # Library availability checks
        PROCESSING_MODE
    )
except ImportError as e:
    print(f"Error importing from comparev2.py: {e}")
    print("Make sure comparev2.py is in the same directory.")
    sys.exit(1)

# ========================================================================
# CROP AND RESOLUTION PRESETS
# ========================================================================

CROP_PRESETS = {
    'tv-full': (240, 0, 240, 0),     # Remove TV show letterboxing
    'tv-hd': (240, 138, 240, 138),   # HD TV show with black bars
    'movie-235': (0, 138, 0, 138),   # 2.35:1 movie letterboxing
    'movie-240': (0, 144, 0, 144),   # 2.40:1 movie letterboxing
    'anime-480': (0, 60, 0, 60),     # Anime letterboxing
    'manual': None                    # User will specify values
}

RESOLUTION_PRESETS = {
    '720p': (1280, 720),
    '1080p': (1920, 1080),
    '1440p': (2560, 1440),
    '4k': (3840, 2160),
    'manual': None
}

class ScreenshotComparisonCLI:
    """Command-line interface for screenshot comparison tool"""
    
    def __init__(self):
        self.parser = self.create_parser()
        
    def create_parser(self):
        """Create comprehensive argument parser"""
        parser = argparse.ArgumentParser(
            description="Enhanced VapourSynth Screenshot Comparison Tool - CLI Version",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Basic comparison of two videos
  comp-cli.py video1.mkv video2.mkv
  
  # Source vs encode with custom frames
  comp-cli.py -m source-encode source.mkv encode.mkv -f 1000,2000,3000
  
  # With cropping and resizing
  comp-cli.py video1.mkv video2.mkv -c tv-full -r 1080p
  
  # Individual video processing
  comp-cli.py v1.mkv v2.mkv --video-crops "240,0,240,0;auto" --video-resolutions "1920,1080;1280,720"
  
  # With upload to slow.pics
  comp-cli.py video1.mkv video2.mkv -u -cn "My Comparison" -s 1 -e 5
  
  # Upload existing screenshots only
  comp-cli.py --upload-only -sd Screenshots -cn "My Collection"
  
Crop presets: tv-full, tv-hd, movie-235, movie-240, anime-480, manual
Resolution presets: 720p, 1080p, 1440p, 4k, manual
            """
        )
        
        # ================================================================
        # POSITIONAL ARGUMENTS
        # ================================================================
        parser.add_argument(
            'videos',
            nargs='*',
            help='Video files to compare'
        )
        
        # ================================================================
        # MODE AND BASIC OPTIONS
        # ================================================================
        parser.add_argument(
            '-m', '--mode',
            choices=['multiple-sources', 'ms', 'source-encode', 'se'],
            default='multiple-sources',
            help='Comparison mode (default: multiple-sources). Use ms/se for short.'
        )
        
        parser.add_argument(
            '-o', '--output-dir',
            help='Output directory for screenshots (default: Screenshots)'
        )
        
        parser.add_argument(
            '-n', '--names',
            nargs='+',
            help='Custom names for videos (default: auto-generated)'
        )
        
        parser.add_argument(
            '-q', '--quiet',
            action='store_true',
            help='Suppress non-essential output'
        )
        
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Enable verbose output'
        )
        
        # ================================================================
        # FRAME SELECTION
        # ================================================================
        frame_group = parser.add_argument_group('Frame Selection')
        
        frame_group.add_argument(
            '-f', '--frames',
            help='Comma-separated frame numbers or ranges (e.g., "1000,2000-2010,3000")'
        )
        
        frame_group.add_argument(
            '--random-frames',
            type=int,
            metavar='COUNT',
            help='Generate COUNT random frames'
        )
        
        frame_group.add_argument(
            '--frame-range',
            metavar='START:END',
            help='Frame range in format START:END (e.g., "1000:5000")'
        )
        
        frame_group.add_argument(
            '--frame-interval',
            type=int,
            metavar='INTERVAL',
            help='Take every Nth frame in range'
        )
        
        # ================================================================
        # GLOBAL PROCESSING OPTIONS
        # ================================================================
        process_group = parser.add_argument_group('Global Video Processing')
        
        process_group.add_argument(
            '-c', '--crop',
            help='Crop preset or manual values. Presets: tv-full, tv-hd, movie-235, movie-240, anime-480. Manual: "left,top,right,bottom"'
        )
        
        process_group.add_argument(
            '-r', '--resolution',
            help='Resolution preset or manual values. Presets: 720p, 1080p, 1440p, 4k. Manual: "width,height"'
        )
        
        process_group.add_argument(
            '--processing-order',
            choices=['crop-first', 'cf', 'resize-first', 'rf'],
            default='resize-first',
            help='Order of processing operations (default: resize-first)'
        )
        
        process_group.add_argument(
            '--trim-start',
            type=int,
            default=0,
            help='Frames to trim from start of all videos'
        )
        
        process_group.add_argument(
            '--trim-end',
            type=int,
            default=0,
            help='Frames to trim from end of all videos'
        )
        
        process_group.add_argument(
            '--pad-start',
            type=int,
            default=0,
            help='Black frames to add at start of all videos'
        )
        
        process_group.add_argument(
            '--pad-end',
            type=int,
            default=0,
            help='Black frames to add at end of all videos'
        )
        
        # ================================================================
        # INDIVIDUAL VIDEO PROCESSING
        # ================================================================
        individual_group = parser.add_argument_group('Individual Video Processing')
        
        individual_group.add_argument(
            '--video-crops',
            help='Semicolon-separated crop values for each video. Use "auto" for auto-detect, "none" for no crop. Example: "240,0,240,0;auto;none"'
        )
        
        individual_group.add_argument(
            '--video-resolutions',
            help='Semicolon-separated resolutions for each video. Example: "1920,1080;1280,720;none"'
        )
        
        individual_group.add_argument(
            '--video-processing-orders',
            help='Semicolon-separated processing orders for each video. Values: crop-first, resize-first'
        )
        
        # ================================================================
        # RESIZE MODE
        # ================================================================
        resize_group = parser.add_argument_group('Resize Configuration')
        
        resize_group.add_argument(
            '--resize-method',
            choices=['none', 'n', 'common', 'c', 'individual', 'i'],
            default='none',
            help='Resize method (default: none). Use n/c/i for short.'
        )
        
        # ================================================================
        # UPLOAD TO SLOW.PICS
        # ================================================================
        upload_group = parser.add_argument_group('Upload to slow.pics')
        
        upload_group.add_argument(
            '-u', '--upload',
            action='store_true',
            help='Upload screenshots to slow.pics'
        )
        
        upload_group.add_argument(
            '-cn', '--collection-name',
            help='Custom collection name for upload'
        )
        
        upload_group.add_argument(
            '-s', '--season',
            type=int,
            help='Season number'
        )
        
        upload_group.add_argument(
            '-e', '--episode',
            type=int,
            help='Episode number'
        )
        
        upload_group.add_argument(
            '-ct', '--collection-type',
            choices=['single', 's', 'season', 'ss'],
            default='single',
            help='Collection type (default: single). Use s/ss for short.'
        )
        
        upload_group.add_argument(
            '--no-browser',
            action='store_true',
            help='Don\'t open browser after upload'
        )
        
        upload_group.add_argument(
            '--dry-run',
            action='store_true',
            help='Test configuration without actually uploading'
        )
        
        # ================================================================
        # UPLOAD ONLY MODE
        # ================================================================
        upload_only_group = parser.add_argument_group('Upload Only Mode')
        
        upload_only_group.add_argument(
            '--upload-only',
            action='store_true',
            help='Upload existing screenshots without processing videos'
        )
        
        upload_only_group.add_argument(
            '-sd', '--screenshots-dir',
            help='Directory containing existing screenshots for upload-only mode'
        )
        
        # ================================================================
        # CONFIGURATION FILES
        # ================================================================
        config_group = parser.add_argument_group('Configuration')
        
        config_group.add_argument(
            '--config',
            help='Load configuration from JSON file'
        )
        
        config_group.add_argument(
            '--save-config',
            help='Save current configuration to JSON file'
        )
        
        return parser
    
    def parse_args(self):
        """Parse and validate command line arguments"""
        args = self.parser.parse_args()
        
        # Validate basic requirements
        if not args.upload_only and not args.videos:
            self.parser.error("Videos are required unless using --upload-only mode")
        
        if args.upload_only and not args.screenshots_dir:
            self.parser.error("--screenshots-dir is required when using --upload-only")
        
        # Normalize choice values
        args = self.normalize_choice_values(args)
        
        return args
    
    def normalize_choice_values(self, args):
        """Normalize short choice values to their long equivalents"""
        # Normalize mode
        if args.mode == 'ms':
            args.mode = 'multiple-sources'
        elif args.mode == 'se':
            args.mode = 'source-encode'
        
        # Normalize resize method
        if args.resize_method == 'n':
            args.resize_method = 'none'
        elif args.resize_method == 'c':
            args.resize_method = 'common'
        elif args.resize_method == 'i':
            args.resize_method = 'individual'
        
        # Normalize processing order
        if args.processing_order == 'cf':
            args.processing_order = 'crop-first'
        elif args.processing_order == 'rf':
            args.processing_order = 'resize-first'
        
        # Normalize collection type
        if args.collection_type == 's':
            args.collection_type = 'single'
        elif args.collection_type == 'ss':
            args.collection_type = 'season'
        
        return args
    
    def validate_videos(self, args):
        """Validate video files exist"""
        if not args.videos:
            return []
        
        validated_videos = []
        for video in args.videos:
            video_path = Path(video)
            if not video_path.exists():
                colored_print(f"[❌] Video file not found: {video}", Colors.RED)
                sys.exit(1)
            validated_videos.append(str(video_path.resolve()))
        
        return validated_videos
    
    def get_video_names(self, args, videos):
        """Get display names for videos"""
        if args.names:
            if len(args.names) != len(videos):
                colored_print(f"[❌] Number of names ({len(args.names)}) must match number of videos ({len(videos)})", Colors.RED)
                sys.exit(1)
            return args.names
        
        # Auto-generate names
        names = []
        for i, video in enumerate(videos):
            if args.mode in ['source-encode', 'se']:
                names.append("Source" if i == 0 else f"Encode{i}")
            else:
                names.append(f"Source{i+1}")
        
        return names
    
    def parse_crop_config(self, crop_arg):
        """Parse crop configuration"""
        if not crop_arg:
            return None
        
        if crop_arg in CROP_PRESETS:
            if crop_arg == 'manual':
                colored_print("[❌] Manual crop preset requires specific values", Colors.RED)
                sys.exit(1)
            return CROP_PRESETS[crop_arg]
        
        # Parse manual crop values
        try:
            values = list(map(int, crop_arg.split(',')))
            if len(values) == 4:
                return tuple(values)
            else:
                colored_print("[❌] Crop values must be: left,top,right,bottom", Colors.RED)
                sys.exit(1)
        except ValueError:
            colored_print(f"[❌] Invalid crop values: {crop_arg}", Colors.RED)
            sys.exit(1)
    
    def parse_resolution_config(self, resolution_arg):
        """Parse resolution configuration"""
        if not resolution_arg:
            return None
        
        if resolution_arg in RESOLUTION_PRESETS:
            if resolution_arg == 'manual':
                colored_print("[❌] Manual resolution preset requires specific values", Colors.RED)
                sys.exit(1)
            return RESOLUTION_PRESETS[resolution_arg]
        
        # Parse manual resolution values
        try:
            values = list(map(int, resolution_arg.split(',')))
            if len(values) == 2:
                return tuple(values)
            else:
                colored_print("[❌] Resolution values must be: width,height", Colors.RED)
                sys.exit(1)
        except ValueError:
            colored_print(f"[❌] Invalid resolution values: {resolution_arg}", Colors.RED)
            sys.exit(1)
    
    def get_frames_config(self, args):
        """Parse frame selection arguments"""
        frames = []
        
        if args.frames:
            # Parse comma-separated frames and ranges
            frame_specs = args.frames.split(',')
            for spec in frame_specs:
                spec = spec.strip()
                if '-' in spec and not spec.startswith('-'):
                    # Range specification
                    try:
                        start, end = map(int, spec.split('-', 1))
                        frames.extend(range(start, end + 1))
                    except ValueError:
                        colored_print(f"[❌] Invalid frame range: {spec}", Colors.RED)
                        sys.exit(1)
                else:
                    # Single frame
                    try:
                        frames.append(int(spec))
                    except ValueError:
                        colored_print(f"[❌] Invalid frame number: {spec}", Colors.RED)
                        sys.exit(1)
        
        elif args.random_frames:
            # Random frames will be generated later when we know video length
            # For now, return None and let comparev2.py handle random generation
            return None
        
        elif args.frame_range:
            # Frame range with optional interval
            try:
                start, end = map(int, args.frame_range.split(':'))
                interval = args.frame_interval or 1
                frames = list(range(start, end + 1, interval))
            except ValueError:
                colored_print(f"[❌] Invalid frame range format: {args.frame_range}", Colors.RED)
                sys.exit(1)
        
        else:
            # No frames specified, will use default from comparev2.py
            return None
        
        if frames:
            return sorted(set(frames))  # Return simple list of integers
        
        return None
    
    def create_config(self, args):
        """Create configuration dictionary compatible with comparev2.py"""
        # Validate videos
        videos = self.validate_videos(args)
        names = self.get_video_names(args, videos)
        
        # Get frame configuration
        custom_frames = self.get_frames_config(args)
        
        # Create video configs using global processing (compatible with comparev2.py)
        config_videos = self.create_global_processed_videos(args, videos, names)
        
        # Get resize configuration
        resize_config = self.get_resize_config(args)
        
        # Build main configuration compatible with comparev2.py structure
        config = {
            'comparison_type': 'source_encode' if args.mode in ['source-encode', 'se'] else 'multiple_sources',
            'videos': config_videos,
            'resize_config': resize_config,
            'upload_to_slowpics': args.upload,
            'no_browser': args.no_browser,
            'quiet': args.quiet,
            'verbose': args.verbose
        }
        
        # Add custom frames if specified
        if custom_frames:
            config['custom_frames'] = custom_frames
        
        # Add upload configuration if enabled
        if args.upload:
            config.update(self.get_upload_config(args))
        
        # Add output directory
        if args.output_dir:
            config['output_dir'] = args.output_dir
        
        return config
    
    def create_global_processed_videos(self, args, videos, names):
        """Create video configs using both global and individual processing settings"""
        # Get global crop and resolution settings (fallback)
        global_crop = self.parse_crop_config(args.crop)
        global_resolution = self.parse_resolution_config(args.resolution)
        
        # Parse individual video processing arguments
        individual_crops, individual_resolutions, individual_processing_orders = self.parse_individual_video_args(args, len(videos))
        
        video_configs = []
        for i, (video, name) in enumerate(zip(videos, names)):
            # Use individual crop if specified, otherwise fall back to global
            crop = individual_crops[i] if individual_crops[i] is not None else global_crop
            
            # Convert crop to dictionary format expected by comparev2.py
            crop_dict = self.convert_crop_to_dict(crop)
            
            # Note: Individual resolutions are now handled in get_resize_config()
            # Don't set resize in individual video configs anymore
            
            video_config = {
                'path': video,
                'name': name,
                'trim_start': args.trim_start,
                'trim_end': args.trim_end,
                'pad_start': args.pad_start,
                'pad_end': args.pad_end,
                'crop': crop_dict,
                # Remove resize from here since it's handled in resize_config
            }
            video_configs.append(video_config)
        
        return video_configs
    
    def get_resize_config(self, args):
        """Get resize configuration compatible with comparev2.py"""
        # Parse individual video processing arguments
        individual_crops, individual_resolutions, individual_processing_orders = self.parse_individual_video_args(args, len(args.videos))
        
        # Check if we have individual resolutions specified
        has_individual_resizes = any(res is not None for res in individual_resolutions)
        
        if has_individual_resizes:
            # Use individual resize method
            config = {
                'resize_method': 'individual',
                'individual_resizes': {}
            }
            
            # Map video names to individual resolutions
            video_names = self.get_video_names(args, args.videos)
            for i, (name, resolution) in enumerate(zip(video_names, individual_resolutions)):
                if resolution is not None:
                    config['individual_resizes'][name] = resolution  # Pass as tuple (width, height)
        else:
            # Use original resize logic
            resize_method = args.resize_method
            
            config = {
                'resize_method': resize_method,
            }
            
            # Get resolution for common resize
            resolution = self.parse_resolution_config(args.resolution)
            if resolution and resize_method == 'common':
                config['common_resolution'] = resolution  # Pass as tuple (width, height)
        
        return config
    
    def get_upload_config(self, args):
        """Get upload configuration"""
        config = {}
        
        if args.collection_name:
            config['collection_name'] = args.collection_name
            # Use collection name as show name for upload system
            config['show_name'] = args.collection_name
        else:
            # No collection name provided - this will be caught in validation
            config['collection_name'] = None
            config['show_name'] = None
        
        config['collection_type'] = args.collection_type
        
        # Add season and episode info if provided
        if args.season:
            config['season'] = args.season
        if args.episode:
            config['episode'] = args.episode
        
        return config
    
    def run(self):
        """Main execution function"""
        args = self.parse_args()
        
        # Handle upload-only mode
        if args.upload_only:
            self.handle_upload_only(args)
            return
        
        try:
            # Create configuration
            config = self.create_config(args)
            
            # Save configuration if requested
            if args.save_config:
                self.save_config_file(config, args.save_config)
            
            # Show configuration summary if not quiet
            if not args.quiet:
                self.show_config_summary(config, args)
            
            # Execute the comparison using comparev2.py functionality
            self.execute_comparison(config, args)
            
        except KeyboardInterrupt:
            colored_print("\n[⚠️] Operation cancelled by user", Colors.YELLOW)
            sys.exit(1)
        except Exception as e:
            colored_print(f"[❌] Error: {e}", Colors.RED)
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    def show_config_summary(self, config, args):
        """Show configuration summary"""
        print_header("CONFIGURATION SUMMARY")
        
        colored_print(f"[📋] Comparison Type: {config.get('comparison_type', 'unknown')}", Colors.CYAN)
        colored_print(f"[📁] Videos: {len(config.get('videos', []))}", Colors.CYAN)
        
        for i, video in enumerate(config.get('videos', [])):
            video_name = video.get('name', f'Video {i+1}')
            video_path = Path(video.get('path', '')).name
            colored_print(f"    {i+1}. {video_name}: {video_path}", Colors.WHITE)
        
        # Show frame configuration
        if config.get('custom_frames'):
            frames = config['custom_frames']
            if isinstance(frames, list):
                colored_print(f"[🎞️] Custom Frames: {len(frames)} frames", Colors.CYAN)
            else:
                colored_print(f"[�️] Custom Frames: {frames}", Colors.CYAN)
        else:
            colored_print("[🎞️] Frames: Default selection", Colors.CYAN)
        
        # Show upload configuration
        if config.get('upload_to_slowpics'):
            colored_print("[🚀] Upload: Enabled", Colors.GREEN)
            if config.get('collection_name'):
                colored_print(f"    Collection: {config['collection_name']}", Colors.WHITE)
        else:
            colored_print("[📷] Upload: Disabled (screenshots only)", Colors.YELLOW)
        
        print()
    
    def execute_comparison(self, config, args):
        """Execute the comparison using comparev2.py functionality"""
        print_header("EXECUTING SCREENSHOT COMPARISON")
        
        try:
            # Import the main screenshot generation function from comparev2.py
            from comparev2 import process_and_generate_screenshots
            
            # Execute screenshot generation
            colored_print("[🎬] Starting video processing and screenshot generation...", Colors.CYAN)
            
            # Use the main function from comparev2.py
            success = process_and_generate_screenshots(config)
            
            if success:
                colored_print("[✅] Screenshots generated successfully", Colors.GREEN)
                colored_print(f"[📁] Screenshots saved in Screenshots/ folder", Colors.BLUE)
            else:
                colored_print("[❌] Screenshot generation failed", Colors.RED)
                sys.exit(1)
                
        except ImportError as e:
            colored_print(f"[❌] Cannot import required functions from comparev2.py: {e}", Colors.RED)
            colored_print("[💡] Make sure comparev2.py is available and up to date", Colors.CYAN)
            sys.exit(1)
        except Exception as e:
            colored_print(f"[❌] Execution error: {e}", Colors.RED)
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    def handle_upload_only(self, args):
        """Handle upload-only mode using comparev2.py functionality"""
        colored_print("\n[�] UPLOAD-ONLY MODE", Colors.YELLOW, bold=True)
        colored_print("Uploading existing screenshots to slow.pics", Colors.CYAN)
        
        screenshots_dir = args.screenshots_dir
        if not os.path.exists(screenshots_dir):
            colored_print(f"[❌] Screenshots directory not found: {screenshots_dir}", Colors.RED)
            sys.exit(1)
        
        # Analyze existing screenshots to determine sources and frames
        source_folders = []
        all_frames = set()
        
        for item in os.listdir(screenshots_dir):
            item_path = os.path.join(screenshots_dir, item)
            if os.path.isdir(item_path):
                png_files = [f for f in os.listdir(item_path) if f.endswith('.png')]
                if png_files:
                    source_folders.append(item)
                    # Extract frame numbers from filenames
                    for png_file in png_files:
                        try:
                            # Assuming format: SourceName_000000.png or SourceName_000000_000000.png
                            parts = png_file.replace('.png', '').split('_')
                            if len(parts) >= 2:
                                frame_part = parts[-1]  # Take the last part as frame number
                                frame_num = int(frame_part)
                                all_frames.add(frame_num)
                        except (ValueError, IndexError):
                            continue
        
        if not source_folders:
            colored_print(f"[❌] No screenshot folders found in {screenshots_dir}", Colors.RED)
            sys.exit(1)
        
        frames = sorted(list(all_frames))
        
        colored_print(f"\n[📁] Found {len(source_folders)} video sources:", Colors.GREEN, bold=True)
        for i, source in enumerate(source_folders):
            source_path = os.path.join(screenshots_dir, source)
            png_files = [f for f in os.listdir(source_path) if f.endswith('.png')]
            png_count = len(png_files)
            colored_print(f"   {i+1}. {source} ({png_count} screenshots)", Colors.CYAN)
        
        colored_print(f"\n[🖼️] Found {len(frames)} unique frames", Colors.BLUE, bold=True)
        if len(frames) <= 20:
            colored_print(f"   Frames: {frames}", Colors.WHITE)
        else:
            colored_print(f"   Frames: {frames[:10]} ... {frames[-5:]} (showing first 10 and last 5)", Colors.WHITE)
        
        total_screenshots = len(frames) * len(source_folders)
        colored_print(f"\n[�] Total screenshots to upload: {total_screenshots}", Colors.MAGENTA, bold=True)
        
        # Build upload config from CLI arguments
        upload_config = {
            'videos': source_folders,  # Use folder names as video names
            'custom_frames': frames,
            'upload_to_slowpics': True,
            'show_name': args.collection_name or "Screenshot Comparison",
            'season_number': f"S{args.season:02d}" if args.season else "",
            'episode_number': f"E{args.episode:02d}" if args.episode else "",
            'collection_type': args.collection_type,
            'no_browser': args.no_browser,
            'output_dir': screenshots_dir,
            'comparison_type': args.mode
        }
        
        # Validate required upload parameters
        if not args.collection_name:
            colored_print("[❌] --collection-name is required for upload", Colors.RED)
            sys.exit(1)
        
        colored_print(f"\n[🔼] Upload configuration ready", Colors.YELLOW, bold=True)
        colored_print(f"Show/Collection: {upload_config['show_name']}", Colors.CYAN)
        
        if args.dry_run:
            colored_print("\n[🧪] DRY RUN MODE - Configuration validated, skipping actual upload", Colors.CYAN, bold=True)
            
            # Save configuration if requested
            if args.save_config:
                self.save_config_file(upload_config, args.save_config)
            
            return
        
        colored_print(f"\n[🔼] Starting upload to slow.pics...", Colors.YELLOW)
        
        try:
            # Use the upload functionality from comparev2.py
            from comparev2 import upload_to_slowpics
            
            # Create processed_videos structure that upload_to_slowpics expects
            processed_videos = []
            for source in source_folders:
                processed_videos.append({
                    'name': source,
                    'clip': None  # Not needed for upload
                })
            
            # Upload screenshots with correct parameters
            success = upload_to_slowpics(upload_config, frames, processed_videos)
            
            if success:
                colored_print("\n[✅] Upload completed successfully!", Colors.GREEN, bold=True)
                
                # Save configuration if requested
                if args.save_config:
                    self.save_config_file(upload_config, args.save_config)
            else:
                colored_print("\n[❌] Upload failed", Colors.RED, bold=True)
                sys.exit(1)
                
        except Exception as e:
            colored_print(f"\n[❌] Upload error: {e}", Colors.RED)
            sys.exit(1)
    
    def save_config_file(self, config, config_path):
        """Save configuration to JSON file"""
        try:
            # Create a clean config for saving (remove non-serializable items)
            save_config = {}
            for key, value in config.items():
                if key in ['videos', 'custom_frames', 'resize_config', 'upload_to_slowpics', 
                          'collection_name', 'show_name', 'collection_type', 'season', 'episode',
                          'comparison_type', 'no_browser', 'quiet', 'verbose', 'output_dir']:
                    save_config[key] = value
            
            with open(config_path, 'w') as f:
                json.dump(save_config, f, indent=2)
            colored_print(f"[✅] Configuration saved to {config_path}", Colors.GREEN)
        except Exception as e:
            colored_print(f"[❌] Failed to save configuration: {e}", Colors.RED)
    
    def parse_individual_video_args(self, args, video_count):
        """Parse semicolon-separated individual video processing arguments"""
        individual_crops = []
        individual_resolutions = []
        individual_processing_orders = []
        
        # Parse individual crops
        if args.video_crops:
            crops = args.video_crops.split(';')
            for i, crop_str in enumerate(crops):
                crop_str = crop_str.strip()
                if crop_str.lower() == 'none':
                    individual_crops.append(None)
                elif crop_str.lower() == 'auto':
                    individual_crops.append('auto')
                else:
                    try:
                        crop_values = tuple(map(int, crop_str.split(',')))
                        if len(crop_values) == 4:
                            individual_crops.append(crop_values)
                        else:
                            colored_print(f"[❌] Invalid crop format for video {i+1}: {crop_str}", Colors.RED)
                            sys.exit(1)
                    except ValueError:
                        colored_print(f"[❌] Invalid crop values for video {i+1}: {crop_str}", Colors.RED)
                        sys.exit(1)
        
        # Parse individual resolutions
        if args.video_resolutions:
            resolutions = args.video_resolutions.split(';')
            for i, res_str in enumerate(resolutions):
                res_str = res_str.strip()
                if res_str.lower() == 'none':
                    individual_resolutions.append(None)
                else:
                    try:
                        # Handle both "1920x1080" and "1920,1080" formats
                        if 'x' in res_str:
                            width, height = map(int, res_str.split('x'))
                        else:
                            width, height = map(int, res_str.split(','))
                        individual_resolutions.append((width, height))
                    except ValueError:
                        colored_print(f"[❌] Invalid resolution format for video {i+1}: {res_str}", Colors.RED)
                        sys.exit(1)
        
        # Parse individual processing orders
        if args.video_processing_orders:
            orders = args.video_processing_orders.split(';')
            for i, order_str in enumerate(orders):
                order_str = order_str.strip()
                if order_str.lower() == 'none':
                    individual_processing_orders.append(None)
                elif order_str in ['crop-first', 'cf']:
                    individual_processing_orders.append('crop-first')
                elif order_str in ['resize-first', 'rf']:
                    individual_processing_orders.append('resize-first')
                else:
                    colored_print(f"[❌] Invalid processing order for video {i+1}: {order_str}", Colors.RED)
                    sys.exit(1)
        
        # Pad lists to match video count
        while len(individual_crops) < video_count:
            individual_crops.append(None)
        while len(individual_resolutions) < video_count:
            individual_resolutions.append(None)
        while len(individual_processing_orders) < video_count:
            individual_processing_orders.append(None)
        
        return individual_crops, individual_resolutions, individual_processing_orders

    def convert_crop_to_dict(self, crop):
        """Convert crop tuple/list to dictionary format expected by comparev2.py"""
        if crop is None or crop == 'auto':
            return crop
        
        if isinstance(crop, (list, tuple)) and len(crop) == 4:
            # Convert (left, top, right, bottom) to dictionary
            left, top, right, bottom = crop
            return {
                'left': left,
                'top': top, 
                'right': right,
                'bottom': bottom
            }
        
        # Already in correct format or unrecognized format
        return crop

def main():
    """Main entry point"""
    try:
        # Initialize the CLI
        cli = ScreenshotComparisonCLI()
        
        # Run the CLI
        cli.run()
        
    except KeyboardInterrupt:
        colored_print("\n[⚠️] Operation cancelled by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        colored_print(f"[❌] Fatal error: {e}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()
