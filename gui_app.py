#!/usr/bin/env python3
"""
Enhanced Screenshot Comparison Tool - GUI Application

A Windows GUI application for video screenshot comparison with slow.pics upload.
Built with tkinter for native Windows look and feel.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.scrolledtext as scrolledtext
import threading
import os
import webbrowser

# Try to import drag and drop support
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD  # type: ignore[import-untyped]
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("Warning: tkinterdnd2 not available. Drag and drop functionality will be disabled.")
    # Create dummy classes to avoid NameError
    class TkinterDnD:
        @staticmethod
        def Tk():
            import tkinter
            return tkinter.Tk()
    
    DND_FILES = None

# Import the core comparison functionality
try:
    from comparev2 import (
        detect_available_libraries, create_video_processor, upload_to_slowpics,
        apply_processing, apply_frame_processing, add_frame_info,
        Colors, colored_print, print_header, PROCESSING_MODE
    )
    COMPARISON_CORE_AVAILABLE = True
except ImportError as e:
    COMPARISON_CORE_AVAILABLE = False
    print(f"Warning: Could not import comparison core: {e}")

class SettingsDialog:
    """Dialog for configuring screenshot generation settings"""
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config.copy()  # Work with a copy
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Screenshot Generation Settings")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the settings dialog UI"""
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # File Management settings
        file_mgmt_frame = ttk.LabelFrame(main_frame, text="File Management", padding=10)
        file_mgmt_frame.pack(fill='x', pady=(0, 15))
        
        self.clear_before_var = tk.BooleanVar(value=self.config.get('clear_before_generation', False))
        ttk.Checkbutton(file_mgmt_frame, text="Clear screenshots folder before generating new screenshots", 
                       variable=self.clear_before_var).pack(anchor='w')
        
        self.clear_after_upload_var = tk.BooleanVar(value=self.config.get('clear_after_upload', False))
        ttk.Checkbutton(file_mgmt_frame, text="Clear screenshots folder after successful upload to slow.pics", 
                       variable=self.clear_after_upload_var).pack(anchor='w', pady=(5, 0))
        
        # Frame selection
        frame_frame = ttk.LabelFrame(main_frame, text="Frame Selection", padding=10)
        frame_frame.pack(fill='x', pady=(0, 15))
        
        # Determine current method
        current_method = 'custom' if self.config.get('custom_frames') else 'interval'
        
        self.frame_method_var = tk.StringVar(value=current_method)
        ttk.Radiobutton(frame_frame, text="Use frame interval", 
                       variable=self.frame_method_var, value='interval',
                       command=self.on_frame_method_change).pack(anchor='w')
        
        interval_frame = ttk.Frame(frame_frame)
        interval_frame.pack(fill='x', padx=(20, 0))
        
        ttk.Label(interval_frame, text="Interval:").pack(side='left')
        self.interval_var = tk.IntVar(value=self.config.get('frame_interval', 150))
        ttk.Spinbox(interval_frame, from_=1, to=1000, textvariable=self.interval_var, 
                   width=10).pack(side='left', padx=(5, 0))
        ttk.Label(interval_frame, text="frames").pack(side='left', padx=(5, 0))
        
        ttk.Radiobutton(frame_frame, text="Specify custom frame numbers", 
                       variable=self.frame_method_var, value='custom',
                       command=self.on_frame_method_change).pack(anchor='w', pady=(10, 0))
        
        custom_frame = ttk.Frame(frame_frame)
        custom_frame.pack(fill='x', padx=(20, 0))
        
        ttk.Label(custom_frame, text="Frames:").pack(side='left')
        
        # Convert custom frames to string if they exist
        custom_frames_str = ""
        if self.config.get('custom_frames'):
            custom_frames_str = ",".join(map(str, self.config['custom_frames']))
        
        self.custom_frames_var = tk.StringVar(value=custom_frames_str or "100,500,1000")
        self.custom_frames_entry = ttk.Entry(custom_frame, textvariable=self.custom_frames_var, width=30)
        self.custom_frames_entry.pack(side='left', padx=(5, 0))
        
        ttk.Label(custom_frame, text="(comma-separated)").pack(side='left', padx=(5, 0))
        
        # Upload settings
        upload_frame = ttk.LabelFrame(main_frame, text="slow.pics Upload", padding=10)
        upload_frame.pack(fill='x', pady=(0, 15))
        
        self.upload_var = tk.BooleanVar(value=self.config.get('upload_to_slowpics', False))
        ttk.Checkbutton(upload_frame, text="Upload to slow.pics", 
                       variable=self.upload_var,
                       command=self.on_upload_change).pack(anchor='w')
        
        self.upload_settings_frame = ttk.Frame(upload_frame)
        self.upload_settings_frame.pack(fill='x', padx=(20, 0))
        
        # Show name
        name_frame = ttk.Frame(self.upload_settings_frame)
        name_frame.pack(fill='x', pady=(5, 0))
        
        ttk.Label(name_frame, text="Show/Movie name:").pack(side='left')
        self.show_name_var = tk.StringVar(value=self.config.get('show_name', ''))
        ttk.Entry(name_frame, textvariable=self.show_name_var, width=30).pack(side='left', padx=(5, 0))
        
        # Season
        season_frame = ttk.Frame(self.upload_settings_frame)
        season_frame.pack(fill='x', pady=(5, 0))
        
        # Determine if series based on season_number
        is_series = bool(self.config.get('season_number', ''))
        self.is_series_var = tk.BooleanVar(value=is_series)
        ttk.Checkbutton(season_frame, text="TV Series (has seasons)", 
                       variable=self.is_series_var,
                       command=self.on_series_change).pack(side='left')
        
        ttk.Label(season_frame, text="Season:").pack(side='left', padx=(20, 0))
        
        # Extract season number if it exists
        season_num = 1
        if self.config.get('season_number'):
            try:
                season_num = int(self.config['season_number'][1:])  # Remove 'S' prefix
            except (ValueError, IndexError):
                season_num = 1
        
        self.season_var = tk.IntVar(value=season_num)
        self.season_spinbox = ttk.Spinbox(season_frame, from_=1, to=50, 
                                         textvariable=self.season_var, width=5)
        self.season_spinbox.pack(side='left', padx=(5, 0))
        
        # Episode
        episode_frame = ttk.Frame(self.upload_settings_frame)
        episode_frame.pack(fill='x', pady=(5, 0))
        
        # Determine if episode based on episode_number
        is_episode = bool(self.config.get('episode_number', ''))
        self.is_episode_var = tk.BooleanVar(value=is_episode)
        ttk.Checkbutton(episode_frame, text="Single episode (not season pack)", 
                       variable=self.is_episode_var,
                       command=self.on_episode_change).pack(side='left')
        
        ttk.Label(episode_frame, text="Episode:").pack(side='left', padx=(20, 0))
        
        # Extract episode number if it exists
        episode_num = 1
        if self.config.get('episode_number'):
            try:
                episode_num = int(self.config['episode_number'][1:])  # Remove 'E' prefix
            except (ValueError, IndexError):
                episode_num = 1
        
        self.episode_var = tk.IntVar(value=episode_num)
        self.episode_spinbox = ttk.Spinbox(episode_frame, from_=1, to=999, 
                                          textvariable=self.episode_var, width=5)
        self.episode_spinbox.pack(side='left', padx=(5, 0))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right')
        ttk.Button(button_frame, text="OK", command=self.ok).pack(side='right', padx=(0, 10))
        
        # Initialize state
        self.on_frame_method_change()
        self.on_upload_change()
        self.on_series_change()
        self.on_episode_change()
    
    def on_frame_method_change(self):
        """Handle frame method change"""
        if self.frame_method_var.get() == 'custom':
            self.custom_frames_entry.configure(state='normal')
        else:
            self.custom_frames_entry.configure(state='disabled')
    
    def on_upload_change(self):
        """Handle upload checkbox change"""
        self.toggle_upload_settings(self.upload_var.get())
    
    def on_series_change(self):
        """Handle series checkbox change"""
        if self.is_series_var.get():
            self.season_spinbox.configure(state='normal')
        else:
            self.season_spinbox.configure(state='disabled')
            self.is_episode_var.set(False)
            self.on_episode_change()
    
    def on_episode_change(self):
        """Handle episode checkbox change"""
        if self.is_episode_var.get() and self.is_series_var.get():
            self.episode_spinbox.configure(state='normal')
        else:
            self.episode_spinbox.configure(state='disabled')
    
    def toggle_upload_settings(self, enabled):
        """Toggle upload settings widgets"""
        state = 'normal' if enabled else 'disabled'
        for widget in self.upload_settings_frame.winfo_children():
            for child in widget.winfo_children():
                if hasattr(child, 'configure'):
                    try:
                        # Only configure widgets that support state
                        if isinstance(child, (ttk.Entry, ttk.Checkbutton, ttk.Spinbox)):
                            child.configure(state=state)
                    except (tk.TclError, AttributeError):
                        pass  # Some widgets don't support state
        
        # Handle spinboxes separately
        if hasattr(self, 'season_spinbox'):
            if enabled and self.is_series_var.get():
                self.season_spinbox.configure(state='normal')
            else:
                self.season_spinbox.configure(state='disabled')
        
        if hasattr(self, 'episode_spinbox'):
            if enabled and self.is_series_var.get() and self.is_episode_var.get():
                self.episode_spinbox.configure(state='normal')
            else:
                self.episode_spinbox.configure(state='disabled')
    
    def ok(self):
        """Apply settings and close dialog"""
        # Update config with current values
        self.config['clear_before_generation'] = self.clear_before_var.get()
        self.config['clear_after_upload'] = self.clear_after_upload_var.get()
        
        if self.frame_method_var.get() == 'interval':
            self.config['frame_interval'] = self.interval_var.get()
            self.config['custom_frames'] = None
        else:
            try:
                frames_text = self.custom_frames_var.get().strip()
                if frames_text:
                    self.config['custom_frames'] = [int(f.strip()) for f in frames_text.split(',') if f.strip()]
                    self.config['frame_interval'] = None
                else:
                    raise ValueError("No frames specified")
            except ValueError:
                messagebox.showwarning("Warning", "Invalid custom frames. Using default interval.")
                self.config['frame_interval'] = 150
                self.config['custom_frames'] = None
        
        self.config['upload_to_slowpics'] = self.upload_var.get()
        self.config['show_name'] = self.show_name_var.get().strip()
        
        if self.is_series_var.get():
            self.config['season_number'] = f"S{self.season_var.get():02d}"
            if self.is_episode_var.get():
                self.config['episode_number'] = f"E{self.episode_var.get():02d}"
            else:
                self.config['episode_number'] = ""
        else:
            self.config['season_number'] = ""
            self.config['episode_number'] = ""
        
        self.result = self.config
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.dialog.destroy()


class ScreenshotComparisonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Screenshot Comparison Tool")
        self.root.geometry("800x650")
        self.root.minsize(750, 550)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('vista')  # Modern Windows style
        
        # Data storage
        self.videos = []
        self.config = {
            'comparison_type': 'multiple_sources',
            'frame_interval': 150,
            'custom_frames': None,
            'upload_to_slowpics': False,
            'show_name': '',
            'season_number': '',
            'episode_number': '',
            'clear_before_generation': False,
            'clear_after_upload': False
        }
        
        # Stop event for screenshot generation
        self.stop_event = threading.Event()
        self.generation_active = False
        
        # Drag and drop state
        self.drag_active = False
        
        # Check for comparison core
        if not COMPARISON_CORE_AVAILABLE:
            messagebox.showerror("Error", 
                "Could not load comparison core functionality. "
                "Please ensure comparev2.py is in the same directory.")
        
        self.setup_ui()
        self.update_processing_info()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Main tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Video Configuration")
        
        # Results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        
        self.setup_main_tab()
        self.setup_results_tab()
        
    def setup_main_tab(self):
        """Set up the main configuration tab"""
        # Title and info
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(title_frame, text="Enhanced Screenshot Comparison Tool", 
                 font=('Arial', 16, 'bold')).pack()
        
        self.info_label = ttk.Label(title_frame, text="Loading processing backend...", 
                                   foreground='blue')
        self.info_label.pack()
        
        # Top controls frame
        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        # Comparison type (left side)
        type_frame = ttk.LabelFrame(controls_frame, text="Comparison Type", padding=10)
        type_frame.pack(side='left', fill='y', padx=(0, 10))
        
        self.comparison_var = tk.StringVar(value='multiple_sources')
        ttk.Radiobutton(type_frame, text="Multiple Sources", 
                       variable=self.comparison_var, value='multiple_sources',
                       command=self.on_comparison_type_change).pack(anchor='w')
        ttk.Radiobutton(type_frame, text="Source vs Encode", 
                       variable=self.comparison_var, value='source_vs_encode',
                       command=self.on_comparison_type_change).pack(anchor='w')
        
        # Middle controls frame - Action buttons
        action_controls = ttk.LabelFrame(controls_frame, text="Actions", padding=10)
        action_controls.pack(side='left', fill='y', padx=(0, 10))
        
        # First row of action buttons
        action_row1 = ttk.Frame(action_controls)
        action_row1.pack(fill='x', pady=(0, 5))
        
        self.generate_button = ttk.Button(action_row1, text="🎬 Generate", 
                  command=self.start_generation, style='Accent.TButton', width=14)
        self.generate_button.pack(side='left', padx=(0, 5))
        
        ttk.Button(action_row1, text="📤 Upload", 
                  command=self.upload_existing, width=14).pack(side='left')
        
        # Second row of action buttons
        action_row2 = ttk.Frame(action_controls)
        action_row2.pack(fill='x')
        
        self.stop_button = ttk.Button(action_row2, text="⏹ Stop", 
                  command=self.stop_generation, width=14, state='disabled')
        self.stop_button.pack(side='left', padx=(0, 5))
        
        ttk.Button(action_row2, text="⚙ Settings", 
                  command=self.open_settings_dialog, width=14).pack(side='left')
        
        # Right controls frame - Video management
        video_controls = ttk.LabelFrame(controls_frame, text="Video Management", padding=10)
        video_controls.pack(side='left', fill='y', padx=(0, 10))
        
        # Video control buttons in a grid layout
        ttk.Button(video_controls, text="🗑 Remove", 
                  command=self.remove_video, width=14).grid(row=0, column=0, padx=(0, 5), pady=(0, 2))
        ttk.Button(video_controls, text="✏ Edit", 
                  command=self.edit_video, width=14).grid(row=0, column=1, pady=(0, 2))
        ttk.Button(video_controls, text="🗂 Clear All", 
                  command=self.clear_videos, width=14).grid(row=1, column=0, columnspan=2, pady=(2, 0))
        
        # Status and progress area (far right)
        status_frame = ttk.LabelFrame(controls_frame, text="Status", padding=10)
        status_frame.pack(side='right', fill='both', expand=True)
        
        self.status_label = ttk.Label(status_frame, text="Ready", font=('Arial', 10, 'bold'))
        self.status_label.pack(pady=(0, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          mode='determinate')
        self.progress_bar.pack(fill='x')
        
        # Video list
        video_frame = ttk.LabelFrame(self.main_frame, text="Video Sources", padding=10)
        video_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Clickable drag and drop area
        self.drop_label = tk.Label(video_frame, 
                                   text="📁 Click here or drag and drop video files\n" +
                                        "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V",
                                   font=('Arial', 10, 'italic'),
                                   fg='#666666',
                                   bg='#f0f0f0',
                                   relief='ridge',
                                   borderwidth=2,
                                   justify='center',
                                   pady=10,
                                   cursor='hand2')
        self.drop_label.pack(fill='x', pady=(0, 10))
        
        # Make drop label clickable
        self.drop_label.bind('<Button-1>', self.on_drop_label_click)
        
        # Video list with scrollbar
        list_frame = ttk.Frame(video_frame)
        list_frame.pack(fill='both', expand=True)
        
        # Treeview for video list
        columns = ('Name', 'Path', 'Type', 'Resolution')
        self.video_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.video_tree.heading(col, text=col)
            self.video_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.video_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.video_tree.xview)
        self.video_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.video_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Configure drag and drop for the video list area
        self.setup_drag_and_drop()
        
    def on_drop_label_click(self, event):
        """Handle click on the drop label to open file dialog"""
        self.add_video()
        
    def open_settings_dialog(self):
        """Open the settings configuration dialog"""
        dialog = SettingsDialog(self.root, self.config)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            # Update configuration with results from dialog
            self.config.update(dialog.result)
        
    def setup_results_tab(self):
        """Set up the results tab"""
        # Results display
        results_frame = ttk.Frame(self.results_frame)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(results_frame, text="Generation Results", 
                 font=('Arial', 14, 'bold')).pack(pady=(0, 10))
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap='word')
        self.results_text.pack(fill='both', expand=True)
        
        # Action buttons
        action_frame = ttk.Frame(results_frame)
        action_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(action_frame, text="Open Screenshots Folder", 
                  command=self.open_screenshots_folder).pack(side='left')
        
        self.url_button = ttk.Button(action_frame, text="Open Comparison URL", 
                                   command=self.open_comparison_url, state='disabled')
        self.url_button.pack(side='left', padx=(10, 0))
        
        ttk.Button(action_frame, text="Clear Results", 
                  command=self.clear_results).pack(side='right')
        
        self.comparison_url = None
        
        # ROLLBACK OPTION: If resize-first approach doesn't work well, there's commented rollback code 
        # in comparev2.py that implements the original crop-first approach with aspect-ratio-aware resizing
        
    def update_processing_info(self):
        """Update processing backend information"""
        if not COMPARISON_CORE_AVAILABLE:
            self.info_label.config(text="Comparison core not available", foreground='red')
            return
            
        try:
            # Detect available libraries in a separate thread to avoid blocking UI
            threading.Thread(target=self._update_processing_info_worker, daemon=True).start()
        except Exception as e:
            self.info_label.config(text=f"Error detecting libraries: {str(e)}", foreground='red')
    
    def _update_processing_info_worker(self):
        """Worker thread for detecting processing libraries"""
        try:
            mode = detect_available_libraries()
            
            # Update UI in main thread
            self.root.after(0, lambda: self._update_processing_info_ui(mode))
        except Exception as e:
            self.root.after(0, lambda: self.info_label.config(
                text=f"Error: {str(e)}", foreground='red'))
    
    def _update_processing_info_ui(self, mode):
        """Update UI with processing information"""
        mode_text = {
            'vapoursynth': 'VapourSynth Mode (High Quality)',
            'opencv': 'OpenCV Mode (Good Performance)',
            'pil': 'PIL Mode (Basic Processing)'
        }
        
        self.info_label.config(text=mode_text.get(mode, f'{mode.title()} Mode'), 
                              foreground='green')
    
    def on_comparison_type_change(self):
        """Handle comparison type change"""
        self.config['comparison_type'] = self.comparison_var.get()
        
    def add_video(self):
        """Add a video file"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm *.m4v"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.open_video_dialog(file_path)
    
    def open_video_dialog(self, file_path, edit_index=None):
        """Open dialog for video configuration"""
        existing_video = self.videos[edit_index] if edit_index is not None else None
        dialog = VideoConfigDialog(self.root, file_path, self.comparison_var.get(), edit_index, existing_video)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            if edit_index is not None:
                # Edit existing video
                self.videos[edit_index] = dialog.result
                self.update_video_list()
            else:
                # Add new video
                self.videos.append(dialog.result)
                self.update_video_list()
    
    def remove_video(self):
        """Remove selected video"""
        selection = self.video_tree.selection()
        if selection:
            index = self.video_tree.index(selection[0])
            del self.videos[index]
            self.update_video_list()
    
    def edit_video(self):
        """Edit selected video"""
        selection = self.video_tree.selection()
        if selection:
            index = self.video_tree.index(selection[0])
            video = self.videos[index]
            self.open_video_dialog(video['path'], index)
    
    def clear_videos(self):
        """Clear all videos"""
        if messagebox.askyesno("Confirm", "Remove all videos?"):
            self.videos.clear()
            self.update_video_list()
    
    def update_video_list(self):
        """Update the video list display"""
        for item in self.video_tree.get_children():
            self.video_tree.delete(item)
        
        for video in self.videos:
            video_type = "Source" if video.get('is_source', True) else "Encode"
            
            # Calculate final resolution after processing
            original_width = video.get('width', 0)
            original_height = video.get('height', 0)
            
            # NEW PROCESSING ORDER for sources: resize first, then crop
            # For encodes: crop first (if any), then no resize
            
            final_width, final_height = original_width, original_height
            intermediate_resolution = None
            
            if video.get('is_source', True):
                # SOURCE: Apply resize first, then crop at target resolution
                
                # Step 1: Apply resize if specified
                if video.get('resize'):
                    final_width, final_height = video['resize']
                    if (final_width, final_height) != (original_width, original_height):
                        intermediate_resolution = f"{final_width}x{final_height}"
                
                # Step 2: Apply crop at target resolution (after resize)
                if video.get('crop') and isinstance(video['crop'], dict):
                    crop = video['crop']
                    left = crop.get('left', 0)
                    right = crop.get('right', 0)
                    top = crop.get('top', 0)
                    bottom = crop.get('bottom', 0)
                    
                    # Calculate dimensions after cropping at target resolution
                    final_width = final_width - left - right
                    final_height = final_height - top - bottom
                    
                    # Ensure positive dimensions
                    final_width = max(1, final_width)
                    final_height = max(1, final_height)
            else:
                # ENCODE: Apply crop first (if any), then no resize
                
                # Step 1: Apply crop at original resolution
                if video.get('crop') and isinstance(video['crop'], dict):
                    crop = video['crop']
                    left = crop.get('left', 0)
                    right = crop.get('right', 0)
                    top = crop.get('top', 0)
                    bottom = crop.get('bottom', 0)
                    
                    # Calculate dimensions after cropping at original resolution
                    crop_width = original_width - left - right
                    crop_height = original_height - top - bottom
                    
                    # Ensure positive dimensions
                    crop_width = max(1, crop_width)
                    crop_height = max(1, crop_height)
                    
                    if crop_width != original_width or crop_height != original_height:
                        intermediate_resolution = f"{crop_width}x{crop_height}"
                    
                    final_width, final_height = crop_width, crop_height
                
                # Step 2: No resize for encodes (resize should be None)
            
            # Build resolution display string
            resolution = f"{final_width}x{final_height}"
            if (final_width, final_height) != (original_width, original_height):
                if intermediate_resolution and video.get('is_source', True):
                    # Source: show original → resized → cropped
                    resolution += f" (from {original_width}x{original_height} → {intermediate_resolution})"
                elif intermediate_resolution:
                    # Encode: show original → cropped
                    resolution += f" (from {original_width}x{original_height})"
                else:
                    # Direct change
                    resolution += f" (from {original_width}x{original_height})"
            
            self.video_tree.insert('', 'end', values=(
                video['name'], 
                os.path.basename(video['path']), 
                video_type,
                resolution
            ))
        
        # Update drop label visibility
        self.update_drop_label_visibility()
    
    def start_generation(self):
        """Start screenshot generation"""
        if not self.videos:
            messagebox.showwarning("Warning", "Please add at least one video source.")
            return
        
        if not COMPARISON_CORE_AVAILABLE:
            messagebox.showerror("Error", "Comparison core not available.")
            return
        
        # Validate configuration
        if not self._validate_config():
            return
        
        # Update configuration
        self._update_config()
        
        # Switch to Results tab immediately
        self.notebook.select(self.results_frame)
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, "Starting screenshot generation...\n\n")
        
        # Reset stop event and mark generation as active
        self.stop_event.clear()
        self.generation_active = True
        
        # Update UI state
        self.generate_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="Generating...")
        self.progress_var.set(0)
        
        # Start generation in separate thread
        generation_thread = threading.Thread(target=self._generation_worker, daemon=True)
        generation_thread.start()
    
    def stop_generation(self):
        """Stop screenshot generation"""
        if self.generation_active:
            self.stop_event.set()
            self.status_label.config(text="Stopping...")
            messagebox.showinfo("Stopping", "Stop signal sent. Generation will halt after the current frame completes.")
    
    def _validate_config(self):
        """Validate current configuration"""
        if self.comparison_var.get() == 'source_vs_encode':
            sources = [v for v in self.videos if v.get('is_source', True)]
            encodes = [v for v in self.videos if not v.get('is_source', True)]
            
            if not sources:
                messagebox.showwarning("Warning", "Source vs Encode mode requires at least one source video.")
                return False
            if not encodes:
                messagebox.showwarning("Warning", "Source vs Encode mode requires at least one encode video.")
                return False
        
        # Check upload settings from config instead of UI variables
        if self.config.get('upload_to_slowpics', False) and not self.config.get('show_name', '').strip():
            messagebox.showwarning("Warning", "Show/Movie name is required for slow.pics upload.")
            return False
        
        return True
    
    def _update_config(self):
        """Update configuration from UI"""
        # Only update comparison type here - other settings are handled by the settings dialog
        self.config['comparison_type'] = self.comparison_var.get()
    
    def _generation_worker(self):
        """Worker thread for screenshot generation"""
        try:
            if not COMPARISON_CORE_AVAILABLE:
                raise Exception("Comparison core not available")
            
            # Check if stopped before starting
            if self.stop_event.is_set():
                self.root.after(0, lambda: self._generation_stopped())
                return
            
            # Import the necessary functions
            from comparev2 import (
                create_video_processor, apply_processing, add_frame_info,
                upload_to_slowpics, apply_frame_processing, generate_screenshots
            )
            
            # Initialize processor
            self.root.after(0, lambda: self.status_label.config(text="Initializing processor..."))
            processor = create_video_processor()
            
            # Check if stopped after processor creation
            if self.stop_event.is_set():
                self.root.after(0, lambda: self._generation_stopped())
                return
            
            # Process videos
            processed_videos = []
            total_videos = len(self.videos)
            
            for i, video_config in enumerate(self.videos):
                # Check if stopped before processing each video
                if self.stop_event.is_set():
                    self.root.after(0, lambda: self._generation_stopped())
                    return
                
                progress = (i / total_videos) * 50  # First 50% for video processing
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda v=video_config['name']: self.status_label.config(text=f"Loading {v}..."))
                
                try:
                    # Load video
                    video_clip = processor.load_video(video_config['path'])
                    
                    # Check if stopped after loading video
                    if self.stop_event.is_set():
                        self.root.after(0, lambda: self._generation_stopped())
                        return
                    
                    # Get video properties
                    if processor.mode == "vapoursynth":
                        original_frames = len(video_clip)
                        original_width, original_height = video_clip.width, video_clip.height
                    elif processor.mode == "opencv":
                        original_frames = processor.get_frame_count(video_clip)
                        original_width = int(video_clip.get(processor.cv2.CAP_PROP_FRAME_WIDTH))
                        original_height = int(video_clip.get(processor.cv2.CAP_PROP_FRAME_HEIGHT))
                    else:
                        original_frames = 1
                        original_width, original_height = 1920, 1080
                    
                    # Apply processing if in VapourSynth mode
                    if processor.mode == "vapoursynth":
                        processed_clip = apply_processing(
                            video_clip,
                            video_config.get('trim_start', 0),
                            video_config.get('trim_end', 0),
                            video_config.get('pad_start', 0),
                            video_config.get('pad_end', 0),
                            video_config.get('crop', None),
                            video_config.get('resize', None),
                            video_config.get('is_source', True)
                        )
                        processed_frames = len(processed_clip)
                        
                        # Get final processed dimensions
                        final_width = processed_clip.width
                        final_height = processed_clip.height
                    else:
                        processed_clip = {
                            'video': video_clip,
                            'trim_start': video_config.get('trim_start', 0),
                            'trim_end': video_config.get('trim_end', 0),
                            'pad_start': video_config.get('pad_start', 0),
                            'pad_end': video_config.get('pad_end', 0),
                            'crop': video_config.get('crop', None),
                            'resize_target': video_config.get('resize', None),
                            'is_source': video_config.get('is_source', True),
                            'original_width': original_width,
                            'original_height': original_height
                        }
                        processed_frames = original_frames
                        
                        # Calculate final dimensions for non-VapourSynth mode
                        final_width, final_height = original_width, original_height
                        
                        # Apply resize if specified
                        if video_config.get('resize'):
                            final_width, final_height = video_config['resize']
                        
                        # Apply crop if specified (reduces resolution)
                        if video_config.get('crop') and isinstance(video_config['crop'], dict):
                            crop = video_config['crop']
                            left = crop.get('left', 0)
                            right = crop.get('right', 0)
                            top = crop.get('top', 0)
                            bottom = crop.get('bottom', 0)
                            
                            # Calculate new dimensions after cropping
                            final_width = final_width - left - right
                            final_height = final_height - top - bottom
                            
                            # Ensure positive dimensions
                            final_width = max(1, final_width)
                            final_height = max(1, final_height)
                    
                    # Update video config with final processed dimensions
                    if i < len(self.videos):
                        self.videos[i]['width'] = final_width
                        self.videos[i]['height'] = final_height
                    
                    processed_videos.append({
                        'clip': processed_clip,
                        'name': video_config['name'],
                        'original_frames': original_frames,
                        'processed_frames': processed_frames
                    })
                    
                except Exception as e:
                    raise Exception(f"Error processing {video_config['name']}: {str(e)}")
            
            # Generate frame numbers
            self.root.after(0, lambda: self.status_label.config(text="Calculating frames..."))
            
            # Check if stopped before frame calculation
            if self.stop_event.is_set():
                self.root.after(0, lambda: self._generation_stopped())
                return
            
            total_frames = min(video['processed_frames'] for video in processed_videos)
            
            if self.config['custom_frames']:
                frames = [f for f in self.config['custom_frames'] if 0 <= f < total_frames]
            else:
                frames = list(range(0, total_frames, self.config['frame_interval']))
            
            if not frames:
                raise Exception("No valid frames to process")
            
            # Check if stopped before screenshot generation
            if self.stop_event.is_set():
                self.root.after(0, lambda: self._generation_stopped())
                return
            
            # Generate screenshots
            self.root.after(0, lambda: self.status_label.config(text="Generating screenshots..."))
            
            # Clear screenshots folder before generation if option is enabled
            if self.config.get('clear_before_generation', False):
                self.root.after(0, lambda: self.status_label.config(text="Clearing screenshots folder..."))
                if self.clear_screenshots_folder():
                    self.root.after(0, lambda: self.status_label.config(text="Screenshots folder cleared, generating screenshots..."))
                else:
                    self.root.after(0, lambda: self.status_label.config(text="Warning: Could not clear screenshots folder, continuing..."))
            
            # Clean up existing screenshots
            screenshots_folder = "Screenshots"
            if not os.path.exists(screenshots_folder):
                os.makedirs(screenshots_folder)
            
            # Add frame info to clips
            video_info_clips = []
            for video in processed_videos:
                if processor.mode == "vapoursynth":
                    video_info_clip = add_frame_info(video['clip'], video['name'])
                    video_info_clips.append({
                        'clip': video_info_clip,
                        'name': video['name']
                    })
                else:
                    video_info_clips.append({
                        'clip': add_frame_info(video['clip'], video['name']),
                        'name': video['name']
                    })
            
            # Generate screenshots frame by frame
            screenshot_count = 0
            
            for frame_i, frame_num in enumerate(frames):
                # Check if stopped before processing each frame
                if self.stop_event.is_set():
                    self.root.after(0, lambda: self._generation_stopped())
                    return
                
                frame_progress = 50 + (frame_i / len(frames)) * 40  # 50-90% for screenshot generation
                self.root.after(0, lambda p=frame_progress: self.progress_var.set(p))
                self.root.after(0, lambda f=frame_num: self.status_label.config(text=f"Processing frame {f}..."))
                
                for video_info in video_info_clips:
                    # Check if stopped before processing each video source
                    if self.stop_event.is_set():
                        self.root.after(0, lambda: self._generation_stopped())
                        return
                    
                    # Create source-specific folder
                    source_folder = os.path.join(screenshots_folder, video_info['name'])
                    os.makedirs(source_folder, exist_ok=True)
                    
                    try:
                        if processor.mode == "vapoursynth":
                            # VapourSynth mode - validate core and vs references first
                            if not hasattr(processor, 'core') or processor.core is None:
                                raise AttributeError("VapourSynth processor 'core' attribute is None or missing")
                            if not hasattr(processor, 'vs') or processor.vs is None:
                                raise AttributeError("VapourSynth processor 'vs' attribute is None or missing")
                                
                            src_frame = video_info['clip'][frame_num:frame_num+1]
                            src_frame_rgb = processor.core.resize.Bicubic(src_frame, format=processor.vs.RGB24, matrix_in_s="709")
                            
                            filename = f"{source_folder}/{video_info['name']}_{frame_num:06d}.png"
                            
                            # Convert VapourSynth frame to numpy array and save using PIL (more reliable)
                            import numpy as np
                            from PIL import Image
                            
                            vs_frame = src_frame_rgb.get_frame(0)
                            
                            # Use the built-in frame-to-array conversion
                            # This handles all the complexity of stride, format, etc.
                            rgb_array = np.asarray(vs_frame)
                            
                            # VapourSynth arrays are in (plane, height, width) format
                            # We need to transpose to (height, width, plane) for PIL
                            if rgb_array.ndim == 3 and rgb_array.shape[0] == 3:
                                # Transpose from (3, height, width) to (height, width, 3)
                                rgb_array = rgb_array.transpose(1, 2, 0)
                            
                            # Create PIL image and save
                            img = Image.fromarray(rgb_array)
                            img.save(filename)
                        else:
                            # Fallback mode
                            processed_frame = apply_frame_processing(video_info['clip'], frame_num)
                            filename = f"{source_folder}/{video_info['name']}_{frame_num:06d}.png"
                            processor.save_frame_as_png(processed_frame, filename)
                        
                        screenshot_count += 1
                        
                    except Exception as e:
                        raise Exception(f"Error generating screenshot for frame {frame_num}, source {video_info['name']}: {str(e)}")
            
            # Generate results summary
            results = f"Successfully generated {screenshot_count} screenshots!\n\n"
            results += f"Processing Summary:\n"
            results += f"• Videos processed: {len(processed_videos)}\n"
            results += f"• Frames captured: {len(frames)}\n"
            results += f"• Total screenshots: {screenshot_count}\n"
            results += f"• Processing mode: {processor.mode.upper()}\n"
            results += f"• Comparison type: {self.config['comparison_type']}\n\n"
            
            results += f"Screenshots saved to:\n"
            for video in processed_videos:
                results += f"  • Screenshots/{video['name']}/\n"
            
            results += f"\nFrame numbers: {frames[:10]}"
            if len(frames) > 10:
                results += f" ... and {len(frames) - 10} more"
            results += "\n"
            
            # Upload to slow.pics if requested
            if self.config['upload_to_slowpics']:
                # Check if stopped before upload
                if self.stop_event.is_set():
                    self.root.after(0, lambda: self._generation_stopped())
                    return
                
                self.root.after(0, lambda: self.status_label.config(text="Uploading to slow.pics..."))
                self.root.after(0, lambda: self.progress_var.set(90))
                
                try:
                    comparison_url = upload_to_slowpics({
                        'show_name': self.config['show_name'],
                        'season_number': self.config['season_number'],
                        'episode_number': self.config['episode_number'],
                        'upload_to_slowpics': True
                    }, frames, processed_videos)
                    
                    if comparison_url:
                        self.comparison_url = comparison_url
                        results += f"\nUploaded to slow.pics: {comparison_url}\n"
                        results += "Comparison opened in your browser!\n"
                        
                        # Clear screenshots folder after successful upload if option is enabled
                        if self.config.get('clear_after_upload', False):
                            if self.clear_screenshots_folder():
                                results += "Screenshots folder cleared after successful upload.\n"
                            else:
                                results += "Warning: Could not clear screenshots folder after upload.\n"
                    else:
                        results += "\nUpload to slow.pics failed, but screenshots are saved locally.\n"
                        
                except Exception as e:
                    results += f"\nUpload failed: {str(e)}\nScreenshots are saved locally.\n"
            
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self._generation_complete(results))
            
        except Exception as e:
            import traceback
            error_msg = f"Error during generation: {str(e)}\n\nDetails:\n{traceback.format_exc()}"
            self.root.after(0, lambda: self._generation_error(error_msg))
    
    def _generation_complete(self, results):
        """Handle generation completion"""
        self.generation_active = False
        self.generate_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Complete")
        self.progress_var.set(100)
        
        # Update video list to show final processed resolutions
        self.update_video_list()
        
        # Show results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
        
        # Enable URL button if uploaded
        if self.comparison_url:
            self.url_button.config(state='normal')
        
        # Switch to results tab
        self.notebook.select(self.results_frame)
        
        messagebox.showinfo("Complete", "Screenshot generation completed successfully!")
    
    def _generation_error(self, error_msg):
        """Handle generation error"""
        self.generation_active = False
        self.generate_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Error")
        self.progress_var.set(0)
        
        messagebox.showerror("Error", error_msg)
    
    def _generation_stopped(self):
        """Handle generation stop"""
        self.generation_active = False
        self.generate_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Stopped")
        
        messagebox.showinfo("Stopped", "Screenshot generation has been stopped. Any screenshots generated so far have been saved.")
    
    def upload_existing(self):
        """Upload existing screenshots"""
        screenshots_folder = "Screenshots"
        if not os.path.exists(screenshots_folder):
            messagebox.showwarning("Warning", 
                "Screenshots folder not found. Generate screenshots first.")
            return
        
        # Check for existing screenshots
        has_screenshots = False
        for item in os.listdir(screenshots_folder):
            item_path = os.path.join(screenshots_folder, item)
            if os.path.isdir(item_path):
                png_files = [f for f in os.listdir(item_path) if f.endswith('.png')]
                if png_files:
                    has_screenshots = True
                    break
        
        if not has_screenshots:
            messagebox.showwarning("Warning", 
                "No screenshots found in Screenshots folder.")
            return
        
        # Check if show name is set in config
        if not self.config.get('show_name', '').strip():
            messagebox.showwarning("Warning", 
                "Please enter a show/movie name in Settings first.")
            return
        
        # Switch to Results tab immediately
        self.notebook.select(self.results_frame)
        
        # Clear previous results and show upload status
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, "Starting upload to slow.pics...\n\n")
        
        # Start upload process
        self.status_label.config(text="Uploading...")
        upload_thread = threading.Thread(target=self._upload_worker, daemon=True)
        upload_thread.start()
    
    def _upload_worker(self):
        """Worker thread for uploading existing screenshots"""
        try:
            if not COMPARISON_CORE_AVAILABLE:
                raise Exception("Comparison core not available")
                
            from comparev2 import upload_to_slowpics
            
            # Analyze existing screenshots
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
                                # Handle multiple possible formats:
                                # Format 1: SourceName_000000.png (standard format)
                                # Format 2: SourceName_000000_000000.png (alternative format)
                                parts = png_file.replace('.png', '').split('_')
                                if len(parts) >= 2:
                                    # Try to get the frame number from the last numeric part
                                    frame_part = parts[-1]  # Get the last part after underscore
                                    frame_num = int(frame_part)
                                    all_frames.add(frame_num)
                            except (ValueError, IndexError):
                                # If parsing fails, try alternative approach
                                try:
                                    # Look for 6-digit numbers in the filename
                                    import re
                                    numbers = re.findall(r'\d{6}', png_file)
                                    if numbers:
                                        frame_num = int(numbers[-1])  # Use the last 6-digit number
                                        all_frames.add(frame_num)
                                except (ValueError, IndexError):
                                    continue
            
            if not source_folders or not all_frames:
                raise Exception("No valid screenshots found in Screenshots folder")
            
            frames = sorted(list(all_frames))
            
            processed_videos = []
            for source in source_folders:
                processed_videos.append({'name': source, 'clip': None})
            
            self.root.after(0, lambda: self.status_label.config(text="Uploading to slow.pics..."))
            
            # Update configuration for upload
            show_name = self.config.get('show_name', '').strip()
            season_number = self.config.get('season_number', '')
            episode_number = self.config.get('episode_number', '')
            
            comparison_url = upload_to_slowpics({
                'show_name': show_name,
                'season_number': season_number,
                'episode_number': episode_number,
                'upload_to_slowpics': True
            }, frames, processed_videos)
            
            if comparison_url:
                self.comparison_url = comparison_url
                results = f"Successfully uploaded existing screenshots!\n\n"
                results += f"Upload Summary:\n"
                results += f"• Sources: {len(source_folders)}\n"
                results += f"• Frames: {len(frames)}\n"
                results += f"• Total screenshots: {len(frames) * len(source_folders)}\n"
                results += f"• Show: {show_name}\n"
                if season_number:
                    results += f"• Season: {season_number}\n"
                results += f"\nComparison URL: {comparison_url}\n"
                results += "Opened in your browser!\n"
                
                # Clear screenshots folder after successful upload if option is enabled
                if self.clear_after_upload_var.get():
                    if self.clear_screenshots_folder():
                        results += "Screenshots folder cleared after successful upload.\n"
                    else:
                        results += "Warning: Could not clear screenshots folder after upload.\n"
            else:
                raise Exception("Upload failed - no URL returned")
            
            self.root.after(0, lambda: self._upload_complete(results))
            
        except Exception as e:
            import traceback
            error_msg = f"Upload failed: {str(e)}\n\nDetails:\n{traceback.format_exc()}"
            self.root.after(0, lambda: self._upload_error(error_msg))
    
    def _upload_complete(self, results):
        """Handle upload completion"""
        self.status_label.config(text="Uploaded")
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
        
        if self.comparison_url:
            self.url_button.config(state='normal')
            # Auto-open URL
            webbrowser.open(self.comparison_url)
        
        self.notebook.select(self.results_frame)
        messagebox.showinfo("Complete", "Upload completed successfully!")
    
    def _upload_error(self, error_msg):
        """Handle upload error"""
        self.status_label.config(text="Upload Failed")
        messagebox.showerror("Upload Error", error_msg)
    
    def open_screenshots_folder(self):
        """Open the screenshots folder"""
        screenshots_folder = os.path.abspath("Screenshots")
        if os.path.exists(screenshots_folder):
            os.startfile(screenshots_folder)
        else:
            messagebox.showinfo("Info", "Screenshots folder not found.")
    
    def open_comparison_url(self):
        """Open the comparison URL"""
        if self.comparison_url:
            webbrowser.open(self.comparison_url)
    
    def clear_results(self):
        """Clear the results text"""
        self.results_text.delete(1.0, tk.END)
        self.comparison_url = None
        self.url_button.config(state='disabled')
    
    def clear_screenshots_folder(self):
        """Clear all contents of the Screenshots folder"""
        screenshots_folder = "Screenshots"
        if os.path.exists(screenshots_folder):
            try:
                import shutil
                # Remove all subdirectories and files
                for filename in os.listdir(screenshots_folder):
                    file_path = os.path.join(screenshots_folder, filename)
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)
                return True
            except Exception as e:
                print(f"Error clearing screenshots folder: {e}")
                return False
        return True  # Folder doesn't exist, consider it "cleared"
    
    def setup_drag_and_drop(self):
        """Set up drag and drop functionality for video files"""
        if not DND_AVAILABLE:
            # Update label to indicate drag and drop is not available
            self.drop_label.config(
                text="📁 Click here to add video files\n" +
                     "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V\n" +
                     "(Drag and drop not available - install tkinterdnd2 for this feature)",
                fg='#999999'
            )
            return
            
        try:
            # Enable drag and drop on multiple widgets
            self.video_tree.drop_target_register(DND_FILES)
            self.drop_label.drop_target_register(DND_FILES)
            
            # Bind drop events
            self.video_tree.dnd_bind('<<Drop>>', self.on_video_drop)
            self.drop_label.dnd_bind('<<Drop>>', self.on_video_drop)
            
            # Bind drag enter/leave events for visual feedback
            self.video_tree.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            self.video_tree.dnd_bind('<<DragLeave>>', self.on_drag_leave)
            self.drop_label.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            self.drop_label.dnd_bind('<<DragLeave>>', self.on_drag_leave)
            
        except Exception as e:
            print(f"Warning: Could not set up drag and drop: {e}")
            # Update label to indicate drag and drop failed
            self.drop_label.config(
                text="📁 Click here to add video files\n" +
                     "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V\n" +
                     "(Drag and drop initialization failed)",
                fg='#999999'
            )
    
    def on_drag_enter(self, event):
        """Handle drag enter event for visual feedback"""
        if not DND_AVAILABLE:
            return
            
        if not self.drag_active:
            self.drag_active = True
            # Change visual appearance to indicate drop zone
            self.drop_label.config(
                text="🎬 Drop video files here!\n" +
                     "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V",
                bg='#e6f3ff',
                fg='#0066cc'
            )
    
    def on_drag_leave(self, event):
        """Handle drag leave event to restore normal appearance"""
        if not DND_AVAILABLE:
            return
            
        if self.drag_active:
            self.drag_active = False
            # Restore normal appearance
            self.drop_label.config(
                text="📁 Click here or drag and drop video files\n" +
                     "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V",
                bg='#f0f0f0',
                fg='#666666'
            )
    
    def on_video_drop(self, event):
        """Handle video file drop event"""
        if not DND_AVAILABLE:
            return
            
        try:
            # Restore normal appearance
            self.on_drag_leave(event)
            
            # Get dropped files - handle different formats
            raw_data = event.data
            
            # Parse file paths - tkinterdnd2 formats paths differently on Windows
            files = []
            
            if raw_data.startswith('{') and raw_data.endswith('}'):
                # Handle braced format: {C:/path/file1.mp4} {C:/path/file2.mp4}
                import re
                files = re.findall(r'\{([^}]+)\}', raw_data)
            elif ' ' in raw_data and not raw_data.startswith('"'):
                # Handle space-separated format for multiple files
                # Try to split smartly by looking for drive letters or path separators
                import re
                # Look for patterns like "C:\" or "/" to identify separate file paths
                potential_files = re.split(r'(?=[A-Z]:\\)', raw_data)
                files = [f.strip() for f in potential_files if f.strip()]
            else:
                # Handle single file or quoted paths
                files = [raw_data.strip('"\'')]
            
            # Fallback: if we still don't have files, try simple split
            if not files:
                files = raw_data.split()
            
            # Filter video files
            video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
            video_files = []
            
            for file_path in files:
                if not file_path:
                    continue
                    
                # Remove quotes if present and normalize path
                file_path = file_path.strip('"\'').strip()
                
                # Handle different path formats
                if file_path.startswith('file:///'):
                    # Handle file:/// URLs
                    from urllib.parse import unquote
                    file_path = unquote(file_path[8:])  # Remove 'file:///'
                elif file_path.startswith('file://'):
                    # Handle file:// URLs
                    from urllib.parse import unquote
                    file_path = unquote(file_path[7:])  # Remove 'file://'
                
                # Convert forward slashes to backslashes for Windows
                file_path = file_path.replace('/', '\\')
                
                # Check if file exists and has video extension
                if os.path.exists(file_path):
                    file_ext = os.path.splitext(file_path)[1].lower()
                    if file_ext in video_extensions:
                        video_files.append(file_path)
                else:
                    # Try alternative path formats
                    alt_paths = [
                        file_path.replace('\\', '/'),  # Try forward slashes
                        os.path.abspath(file_path),    # Try absolute path
                    ]
                    for alt_path in alt_paths:
                        if os.path.exists(alt_path):
                            file_ext = os.path.splitext(alt_path)[1].lower()
                            if file_ext in video_extensions:
                                video_files.append(alt_path)
                                break
            
            if not video_files:
                messagebox.showwarning("Invalid Files", 
                    f"No valid video files found. Supported formats:\n" +
                    f"MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V\n\n" +
                    f"Please ensure the files have valid video extensions.")
                return
            
            # Process each video file
            for file_path in video_files:
                # Open configuration dialog for each dropped video
                self.open_video_dialog(file_path)
                
            # Show success message if multiple files were processed
            if len(video_files) > 1:
                messagebox.showinfo("Success", 
                    f"Added {len(video_files)} video files successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process dropped files: {str(e)}")
    
    def update_drop_label_visibility(self):
        """Update the visibility of the drop label based on video list content"""
        # Always show the drop label to allow adding more videos
        self.drop_label.pack(fill='x', pady=(0, 10), before=self.video_tree.master)
        
        # Update the label text based on DND availability and current video count
        if DND_AVAILABLE:
            if self.videos:
                # When videos are present, show "add more" message
                self.drop_label.config(
                    text=f"📁 Drag and drop more video files here ({len(self.videos)} video{'s' if len(self.videos) != 1 else ''} added)\n" +
                         "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V",
                    fg='#555555',
                    bg='#f8f8f8'
                )
            else:
                # When no videos, show initial message
                self.drop_label.config(
                    text="📁 Drag and drop video files here to add them\n" +
                         "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V",
                    fg='#666666',
                    bg='#f0f0f0'
                )
        else:
            if self.videos:
                # When videos are present and DND not available
                self.drop_label.config(
                    text=f"📁 Click 'Add Video' button to add more videos ({len(self.videos)} video{'s' if len(self.videos) != 1 else ''} added)\n" +
                         "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V\n" +
                         "(Drag and drop not available - install tkinterdnd2 for this feature)",
                    fg='#999999'
                )
            else:
                # When no videos and DND not available
                self.drop_label.config(
                    text="📁 Click 'Add Video' button to add video files\n" +
                         "Supported formats: MP4, MKV, AVI, MOV, WMV, FLV, WEBM, M4V\n" +
                         "(Drag and drop not available - install tkinterdnd2 for this feature)",
                    fg='#999999'
                )
    

class VideoConfigDialog:
    def __init__(self, parent, file_path, comparison_type, edit_index=None, existing_video=None):
        self.parent = parent
        self.file_path = file_path
        self.comparison_type = comparison_type
        self.edit_index = edit_index
        self.existing_video = existing_video
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Video Configuration - Configure settings and click OK")
        self.dialog.geometry("700x750")
        self.dialog.resizable(True, True)
        self.dialog.minsize(650, 600)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_dialog()
        
        # Load video info
        self.load_video_info()
        
        # Load existing video data if editing
        if self.existing_video:
            self.load_existing_values()
    
    def setup_dialog(self):
        """Set up the dialog UI with scrollable content"""
        # Create main container
        main_container = ttk.Frame(self.dialog)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create scrollable content container
        scroll_container = ttk.Frame(main_container)
        scroll_container.pack(fill='both', expand=True, pady=(0, 10))
        
        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(scroll_container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Update the canvas window width to match the frame width
            canvas_width = event.width
            if canvas.find_all():
                canvas.itemconfig(canvas.find_all()[0], width=canvas_width)
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Configure>", _on_frame_configure)
        
        # Also bind mousewheel to the dialog window
        self.dialog.bind("<MouseWheel>", _on_mousewheel)
        
        # Create content frame inside the scrollable frame
        content_frame = ttk.Frame(self.scrollable_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add instruction label
        instruction = ttk.Label(content_frame, 
                               text="Configure video settings below, then click OK to add the video or Cancel to abort.",
                               font=('TkDefaultFont', 9, 'italic'),
                               foreground='blue')
        instruction.pack(fill='x', pady=(0, 10))
        
        # File info
        info_frame = ttk.LabelFrame(content_frame, text="File Information", padding=10)
        info_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(info_frame, text="File:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        file_label = ttk.Label(info_frame, text=os.path.basename(self.file_path), 
                              foreground='blue')
        file_label.grid(row=0, column=1, sticky='w')
        
        ttk.Label(info_frame, text="Path:").grid(row=1, column=0, sticky='w', padx=(0, 10))
        path_label = ttk.Label(info_frame, text=self.file_path, wraplength=400)
        path_label.grid(row=1, column=1, sticky='w')
        
        self.resolution_label = ttk.Label(info_frame, text="Detecting...")
        ttk.Label(info_frame, text="Resolution:").grid(row=2, column=0, sticky='w', padx=(0, 10))
        self.resolution_label.grid(row=2, column=1, sticky='w')
        
        # Video settings
        settings_frame = ttk.LabelFrame(content_frame, text="Video Settings", padding=10)
        settings_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Display name
        ttk.Label(settings_frame, text="Display Name:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.name_var = tk.StringVar(value=os.path.splitext(os.path.basename(self.file_path))[0])
        ttk.Entry(settings_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, sticky='ew')
        
        # Video type (for source vs encode)
        if self.comparison_type == 'source_vs_encode':
            ttk.Label(settings_frame, text="Video Type:").grid(row=1, column=0, sticky='w', padx=(0, 10))
            self.type_var = tk.StringVar(value='source')
            type_frame = ttk.Frame(settings_frame)
            type_frame.grid(row=1, column=1, sticky='w')
            
            ttk.Radiobutton(type_frame, text="Source", variable=self.type_var, value='source').pack(side='left')
            ttk.Radiobutton(type_frame, text="Encode", variable=self.type_var, value='encode').pack(side='left', padx=(20, 0))
        
        # Processing options
        processing_frame = ttk.LabelFrame(settings_frame, text="Processing Options", padding=10)
        processing_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        
        # Resize options
        ttk.Label(processing_frame, text="Resize:").grid(row=0, column=0, sticky='w')
        self.resize_var = tk.StringVar(value='none')
        
        resize_frame = ttk.Frame(processing_frame)
        resize_frame.grid(row=0, column=1, sticky='w')
        
        ttk.Radiobutton(resize_frame, text="No resize", variable=self.resize_var, 
                       value='none', command=self.update_resize_state).pack(anchor='w')
        ttk.Radiobutton(resize_frame, text="Preset resolution", variable=self.resize_var, 
                       value='preset', command=self.update_resize_state).pack(anchor='w')
        ttk.Radiobutton(resize_frame, text="Custom size", variable=self.resize_var, 
                       value='custom', command=self.update_resize_state).pack(anchor='w')
        
        # Preset resolution dropdown
        self.preset_frame = ttk.Frame(resize_frame)
        self.preset_frame.pack(fill='x', padx=(20, 0))
        
        ttk.Label(self.preset_frame, text="Preset:").pack(side='left')
        self.preset_var = tk.StringVar(value='1080p (1920x1080)')
        
        # Define preset resolution map
        self.preset_map = {
            # Standard Definition (SD)
            '240p (426x240)': (426, 240),
            '360p (640x360)': (640, 360),
            '480p (720x480)': (720, 480),  # NTSC SD
            '480p (854x480)': (854, 480),  # Widescreen SD
            '576p (720x576)': (720, 576),  # PAL SD

            # High Definition (HD)
            '720p (1280x720)': (1280, 720),
            '900p (1600x900)': (1600, 900),

            # Full HD (1080p) and variations
            '1080p (1920x1080)': (1920, 1080),  # Full frame 16:9
            '1080p (1920x1040)': (1920, 1040),  # Mild crop
            '1080p (1920x1036)': (1920, 1036),  # 1.85:1 aspect (widescreen)
            '1080p (1920x960)': (1920, 960),    # 2.00:1 aspect
            '1080p (1920x872)': (1920, 872),    # 2.20:1 (70mm films)
            '1080p (1920x816)': (1920, 816),    # 2.35:1 Cinemascope
            '1080p (1920x804)': (1920, 804),    # 2.39:1 variant
            '1080p (1920x800)': (1920, 800),    # Common cropped Blu-ray
            '1080p (1920x792)': (1920, 792),    # Another scope variation
            '1080p with black bars (1920x1080 letterboxed)': (1920, 1080),  # letterboxed inside 16:9
            '1440x1080 (4:3 anamorphic)': (1440, 1080),

            # Quad HD / 2K / Near 2K
            '1440p (2560x1440)': (2560, 1440),
            '2K (2048x1080)': (2048, 1080),        # DCI 2K full container
            '2K Flat (1998x1080)': (1998, 1080),   # 1.85:1 DCI
            '2K Scope (2048x858)': (2048, 858),    # 2.39:1 DCI cropped

            # 4K and variations
            '4K UHD (3840x2160)': (3840, 2160),     # True 16:9 UHD
            '4K Flat (3840x2076)': (3840, 2076),    # 1.85:1
            '4K Univisium (3840x1920)': (3840, 1920),  # 2.00:1 Netflix
            '4K Scope (3840x1644)': (3840, 1644),   # 2.35:1
            '4K (3840x1600)': (3840, 1600),         # 2.40:1 cropped
            '4K IMAX (3840x2024)': (3840, 2024),    # 1.90:1
            '4K with black bars (3840x2160 letterboxed)': (3840, 2160),  # letterbox encoded into video

            # DCI 4K Variants
            'DCI 4K Full (4096x2160)': (4096, 2160),    # Cinema 4K full
            'DCI 4K Flat (3996x2160)': (3996, 2160),    # 1.85:1
            'DCI 4K Scope (4096x1716)': (4096, 1716),   # 2.39:1
        }
        
        preset_options = list(self.preset_map.keys())
        preset_combobox = ttk.Combobox(self.preset_frame, textvariable=self.preset_var, 
                                      values=preset_options, width=35, state='readonly')
        preset_combobox.pack(side='left', padx=(5, 0))
        
        # Custom resolution frame
        self.custom_frame = ttk.Frame(resize_frame)
        self.custom_frame.pack(fill='x', padx=(20, 0))
        
        ttk.Label(self.custom_frame, text="Width:").pack(side='left')
        self.width_var = tk.IntVar(value=1920)
        self.width_spinbox = ttk.Spinbox(self.custom_frame, from_=1, to=7680, textvariable=self.width_var, width=8)
        self.width_spinbox.pack(side='left', padx=(5, 10))
        
        ttk.Label(self.custom_frame, text="Height:").pack(side='left')
        self.height_var = tk.IntVar(value=1080)
        self.height_spinbox = ttk.Spinbox(self.custom_frame, from_=1, to=4320, textvariable=self.height_var, width=8)
        self.height_spinbox.pack(side='left', padx=(5, 0))
        
        # Crop options
        ttk.Label(processing_frame, text="Crop:").grid(row=1, column=0, sticky='w', pady=(10, 0))
        self.crop_var = tk.StringVar(value='none')
        
        crop_frame = ttk.Frame(processing_frame)
        crop_frame.grid(row=1, column=1, sticky='w', pady=(10, 0))
        
        ttk.Radiobutton(crop_frame, text="No crop", variable=self.crop_var, 
                       value='none', command=self.update_crop_state).pack(anchor='w')
        ttk.Radiobutton(crop_frame, text="Preset crop", variable=self.crop_var, 
                       value='preset', command=self.update_crop_state).pack(anchor='w')
        ttk.Radiobutton(crop_frame, text="Manual", variable=self.crop_var, 
                       value='manual', command=self.update_crop_state).pack(anchor='w')
        
        # Preset crop dropdown
        self.preset_crop_frame = ttk.Frame(crop_frame)
        self.preset_crop_frame.pack(fill='x', padx=(20, 0))
        
        ttk.Label(self.preset_crop_frame, text="Preset:").pack(side='left')
        self.crop_preset_var = tk.StringVar(value='1080p Scope 2.40:1 (140px top/bottom)')
        
        # Define crop preset map with pixel information
        self.crop_preset_map = {
            # Standard Definition (SD) Letterbox Crops
            'letterbox_sd_4:3_to_16:9': {
                'label': 'SD 4:3 → 16:9 (60px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 60, 'bottom': 60}
            },
            'letterbox_sd_2.35': {
                'label': 'SD Scope 2.35:1 (66px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 66, 'bottom': 66}
            },
            
            # HD (720p) Letterbox Crops
            'letterbox_720p_2.40': {
                'label': '720p Scope 2.40:1 (90px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 90, 'bottom': 90}
            },
            'letterbox_720p_2.35': {
                'label': '720p Scope 2.35:1 (86px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 86, 'bottom': 86}
            },
            'letterbox_720p_1.85': {
                'label': '720p Flat 1.85:1 (52px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 52, 'bottom': 52}
            },
            
            # Full HD (1080p) Letterbox Crops - Most Common
            'letterbox_1080p_2.40': {
                'label': '1080p Scope 2.40:1 (140px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 140, 'bottom': 140}
            },
            'letterbox_1080p_2.39': {
                'label': '1080p Scope 2.39:1 (138px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 138, 'bottom': 138}
            },
            'letterbox_1080p_2.35': {
                'label': '1080p Scope 2.35:1 (132px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 132, 'bottom': 132}
            },
            'letterbox_1080p_2.24': {
                'label': '1080p 70mm 2.24:1 (111px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 111, 'bottom': 111}
            },
            'letterbox_1080p_2.20': {
                'label': '1080p Ultra 2.20:1 (102px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 102, 'bottom': 102}
            },
            'letterbox_1080p_2.00': {
                'label': '1080p Univisium 2.00:1 (60px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 60, 'bottom': 60}
            },
            'letterbox_1080p_1.90': {
                'label': '1080p IMAX 1.90:1 (42px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 42, 'bottom': 42}
            },
            'letterbox_1080p_1.85': {
                'label': '1080p Flat 1.85:1 (22px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 22, 'bottom': 22}
            },
            
            # 4K UHD Letterbox Crops
            'letterbox_4k_2.40': {
                'label': '4K Scope 2.40:1 (280px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 280, 'bottom': 280}
            },
            'letterbox_4k_2.35': {
                'label': '4K Scope 2.35:1 (264px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 264, 'bottom': 264}
            },
            'letterbox_4k_2.00': {
                'label': '4K Univisium 2.00:1 (120px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 120, 'bottom': 120}
            },
            'letterbox_4k_1.85': {
                'label': '4K Flat 1.85:1 (42px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 42, 'bottom': 42}
            },
            
            # Pillarbox Crops (Black bars on sides)
            'pillarbox_4:3_in_16:9': {
                'label': 'Pillarbox 4:3 in 16:9 (240px left/right)',
                'crop': {'left': 240, 'right': 240, 'top': 0, 'bottom': 0}
            },
            'pillarbox_16:10_in_16:9': {
                'label': 'Pillarbox 16:10 in 16:9 (144px left/right)',
                'crop': {'left': 144, 'right': 144, 'top': 0, 'bottom': 0}
            },
            'pillarbox_21:9_small': {
                'label': 'Pillarbox narrow 21:9 (120px left/right)',
                'crop': {'left': 120, 'right': 120, 'top': 0, 'bottom': 0}
            },
            'pillarbox_5:4_in_16:9': {
                'label': 'Pillarbox 5:4 in 16:9 (216px left/right)',
                'crop': {'left': 216, 'right': 216, 'top': 0, 'bottom': 0}
            },
            
            # Streaming Service Specific Crops
            'netflix_logo_crop': {
                'label': 'Netflix logo removal (80px right)',
                'crop': {'left': 0, 'right': 80, 'top': 0, 'bottom': 0}
            },
            'disney_plus_logo': {
                'label': 'Disney+ logo removal (100px right)',
                'crop': {'left': 0, 'right': 100, 'top': 0, 'bottom': 0}
            },
            'hbo_max_logo': {
                'label': 'HBO Max logo removal (120px right)',
                'crop': {'left': 0, 'right': 120, 'top': 0, 'bottom': 0}
            },
            'amazon_prime_logo': {
                'label': 'Amazon Prime logo removal (90px right)',
                'crop': {'left': 0, 'right': 90, 'top': 0, 'bottom': 0}
            },
            'apple_tv_logo': {
                'label': 'Apple TV+ logo removal (70px right)',
                'crop': {'left': 0, 'right': 70, 'top': 0, 'bottom': 0}
            },
            
            # Quality Enhancement Crops
            'dirty_lines_minimal': {
                'label': 'Dirty lines minimal (1px each side)',
                'crop': {'left': 1, 'right': 1, 'top': 1, 'bottom': 1}
            },
            'dirty_lines_standard': {
                'label': 'Dirty lines standard (2px each side)',
                'crop': {'left': 2, 'right': 2, 'top': 2, 'bottom': 2}
            },
            'dirty_lines_heavy': {
                'label': 'Dirty lines heavy (4px each side)',
                'crop': {'left': 4, 'right': 4, 'top': 4, 'bottom': 4}
            },
            'dirty_lines_top_only': {
                'label': 'Dirty lines top only (2px top)',
                'crop': {'left': 0, 'right': 0, 'top': 2, 'bottom': 0}
            },
            'dirty_lines_bottom_only': {
                'label': 'Dirty lines bottom only (2px bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 0, 'bottom': 2}
            },
            'dirty_lines_sides_only': {
                'label': 'Dirty lines sides only (2px left/right)',
                'crop': {'left': 2, 'right': 2, 'top': 0, 'bottom': 0}
            },
            
            # Encode Quality Fixes
            'encode_artifacts_light': {
                'label': 'Encode artifacts light (1px each side)',
                'crop': {'left': 1, 'right': 1, 'top': 1, 'bottom': 1}
            },
            'encode_artifacts_medium': {
                'label': 'Encode artifacts medium (2px each side)',
                'crop': {'left': 2, 'right': 2, 'top': 2, 'bottom': 2}
            },
            'encode_artifacts_heavy': {
                'label': 'Encode artifacts heavy (3px each side)',
                'crop': {'left': 3, 'right': 3, 'top': 3, 'bottom': 3}
            },
            
            # Blu-ray Specific Crops
            'bluray_overscan_fix': {
                'label': 'Blu-ray overscan fix (8px each side)',
                'crop': {'left': 8, 'right': 8, 'top': 8, 'bottom': 8}
            },
            'bluray_black_level_fix': {
                'label': 'Blu-ray black level fix (4px each side)',
                'crop': {'left': 4, 'right': 4, 'top': 4, 'bottom': 4}
            },
            
            # DVD Specific Crops
            'dvd_overscan_fix': {
                'label': 'DVD overscan fix (6px each side)',
                'crop': {'left': 6, 'right': 6, 'top': 6, 'bottom': 6}
            },
            'dvd_interlace_fix': {
                'label': 'DVD interlace artifacts (2px top/bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 2, 'bottom': 2}
            },
            
            # Broadcast/TV Crops
            'broadcast_safe_area': {
                'label': 'Broadcast safe area (32px each side)',
                'crop': {'left': 32, 'right': 32, 'top': 32, 'bottom': 32}
            },
            'tv_overscan_10percent': {
                'label': 'TV overscan 10% (96px left/right, 54px top/bottom)',
                'crop': {'left': 96, 'right': 96, 'top': 54, 'bottom': 54}
            },
            'tv_overscan_5percent': {
                'label': 'TV overscan 5% (48px left/right, 27px top/bottom)',
                'crop': {'left': 48, 'right': 48, 'top': 27, 'bottom': 27}
            },
            
            # Anime/Animation Specific
            'anime_letterbox_fix': {
                'label': 'Anime letterbox fix (varies)',
                'crop': {'left': 0, 'right': 0, 'top': 2, 'bottom': 2}
            },
            'animation_border_fix': {
                'label': 'Animation border fix (1px each side)',
                'crop': {'left': 1, 'right': 1, 'top': 1, 'bottom': 1}
            },
            
            # Mobile/Vertical Content
            'mobile_crop_top': {
                'label': 'Mobile UI crop top (100px top)',
                'crop': {'left': 0, 'right': 0, 'top': 100, 'bottom': 0}
            },
            'mobile_crop_bottom': {
                'label': 'Mobile UI crop bottom (100px bottom)',
                'crop': {'left': 0, 'right': 0, 'top': 0, 'bottom': 100}
            },
            
            # Ultra-wide Monitor Crops
            'ultrawide_21:9_bars': {
                'label': 'Ultra-wide 21:9 bars (240px left/right)',
                'crop': {'left': 240, 'right': 240, 'top': 0, 'bottom': 0}
            },
            'ultrawide_32:9_bars': {
                'label': 'Ultra-wide 32:9 bars (480px left/right)',
                'crop': {'left': 480, 'right': 480, 'top': 0, 'bottom': 0}
            },
        }
        
        crop_preset_options = [preset['label'] for preset in self.crop_preset_map.values()]
        crop_preset_combobox = ttk.Combobox(self.preset_crop_frame, textvariable=self.crop_preset_var, 
                                           values=crop_preset_options, width=45, state='readonly')
        crop_preset_combobox.pack(side='left', padx=(5, 0))
        
        # Manual crop frame
        self.manual_crop_frame = ttk.Frame(crop_frame)
        self.manual_crop_frame.pack(fill='x', padx=(20, 0))
        
        crop_grid = ttk.Frame(self.manual_crop_frame)
        crop_grid.pack()
        
        ttk.Label(crop_grid, text="Left:").grid(row=0, column=0)
        self.crop_left_var = tk.IntVar()
        self.crop_left_spinbox = ttk.Spinbox(crop_grid, from_=0, to=1000, textvariable=self.crop_left_var, width=6)
        self.crop_left_spinbox.grid(row=0, column=1, padx=2)
        
        ttk.Label(crop_grid, text="Right:").grid(row=0, column=2, padx=(10, 0))
        self.crop_right_var = tk.IntVar()
        self.crop_right_spinbox = ttk.Spinbox(crop_grid, from_=0, to=1000, textvariable=self.crop_right_var, width=6)
        self.crop_right_spinbox.grid(row=0, column=3, padx=2)
        
        ttk.Label(crop_grid, text="Top:").grid(row=1, column=0)
        self.crop_top_var = tk.IntVar()
        self.crop_top_spinbox = ttk.Spinbox(crop_grid, from_=0, to=1000, textvariable=self.crop_top_var, width=6)
        self.crop_top_spinbox.grid(row=1, column=1, padx=2)
        
        ttk.Label(crop_grid, text="Bottom:").grid(row=1, column=2, padx=(10, 0))
        self.crop_bottom_var = tk.IntVar()
        self.crop_bottom_spinbox = ttk.Spinbox(crop_grid, from_=0, to=1000, textvariable=self.crop_bottom_var, width=6)
        self.crop_bottom_spinbox.grid(row=1, column=3, padx=2)
        
        # Trim/Pad options
        ttk.Label(processing_frame, text="Trim/Pad:").grid(row=2, column=0, sticky='w', pady=(10, 0))
        
        trim_pad_frame = ttk.Frame(processing_frame)
        trim_pad_frame.grid(row=2, column=1, sticky='w', pady=(10, 0))
        
        # Trim options
        trim_frame = ttk.LabelFrame(trim_pad_frame, text="Trim Frames", padding=5)
        trim_frame.pack(fill='x', pady=(0, 5))
        
        trim_grid = ttk.Frame(trim_frame)
        trim_grid.pack()
        
        ttk.Label(trim_grid, text="From start:").grid(row=0, column=0, sticky='w')
        self.trim_start_var = tk.IntVar()
        self.trim_start_spinbox = ttk.Spinbox(trim_grid, from_=0, to=10000, textvariable=self.trim_start_var, width=8)
        self.trim_start_spinbox.grid(row=0, column=1, padx=(5, 10), sticky='w')
        
        ttk.Label(trim_grid, text="From end:").grid(row=0, column=2, sticky='w')
        self.trim_end_var = tk.IntVar()
        self.trim_end_spinbox = ttk.Spinbox(trim_grid, from_=0, to=10000, textvariable=self.trim_end_var, width=8)
        self.trim_end_spinbox.grid(row=0, column=3, padx=(5, 0), sticky='w')
        
        # Pad options
        pad_frame = ttk.LabelFrame(trim_pad_frame, text="Add Padding (Black Frames)", padding=5)
        pad_frame.pack(fill='x')
        
        pad_grid = ttk.Frame(pad_frame)
        pad_grid.pack()
        
        ttk.Label(pad_grid, text="At start:").grid(row=0, column=0, sticky='w')
        self.pad_start_var = tk.IntVar()
        self.pad_start_spinbox = ttk.Spinbox(pad_grid, from_=0, to=10000, textvariable=self.pad_start_var, width=8)
        self.pad_start_spinbox.grid(row=0, column=1, padx=(5, 10), sticky='w')
        
        ttk.Label(pad_grid, text="At end:").grid(row=0, column=2, sticky='w')
        self.pad_end_var = tk.IntVar()
        self.pad_end_spinbox = ttk.Spinbox(pad_grid, from_=0, to=10000, textvariable=self.pad_end_var, width=8)
        self.pad_end_spinbox.grid(row=0, column=3, padx=(5, 0), sticky='w')
        
        settings_frame.grid_columnconfigure(1, weight=1)
        
        # Buttons (always at bottom, outside scrollable area)
        separator = ttk.Separator(main_container, orient='horizontal')
        separator.pack(fill='x', pady=(10, 10))
        
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill='x', pady=(0, 0))
        
        # Add buttons with better styling - OK first (on right), Cancel second (on left)
        ok_btn = ttk.Button(button_frame, text="OK", command=self.ok)
        ok_btn.pack(side='right', padx=(10, 0))
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side='right', padx=(0, 10))
        
        # Make OK button the default and add keyboard shortcuts
        ok_btn.focus_set()
        self.dialog.bind('<Return>', lambda e: self.ok())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Initialize the state of input boxes
        self.update_resize_state()
        self.update_crop_state()
    
    def update_resize_state(self):
        """Enable/disable resize input boxes based on selection"""
        resize_mode = self.resize_var.get()
        
        if resize_mode == 'preset':
            # Enable preset dropdown, disable custom inputs
            for widget in self.preset_frame.winfo_children():
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='readonly')
            self.width_spinbox.config(state='disabled')
            self.height_spinbox.config(state='disabled')
            
        elif resize_mode == 'custom':
            # Disable preset dropdown, enable custom inputs
            for widget in self.preset_frame.winfo_children():
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='disabled')
            self.width_spinbox.config(state='normal')
            self.height_spinbox.config(state='normal')
            
        else:  # 'none'
            # Disable both preset and custom inputs
            for widget in self.preset_frame.winfo_children():
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='disabled')
            self.width_spinbox.config(state='disabled')
            self.height_spinbox.config(state='disabled')
    
    def update_crop_state(self):
        """Enable/disable crop input boxes based on selection"""
        crop_mode = self.crop_var.get()
        
        if crop_mode == 'preset':
            # Enable preset dropdown, disable manual inputs
            for widget in self.preset_crop_frame.winfo_children():
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='readonly')
            self.crop_left_spinbox.config(state='disabled')
            self.crop_right_spinbox.config(state='disabled')
            self.crop_top_spinbox.config(state='disabled')
            self.crop_bottom_spinbox.config(state='disabled')
            
        elif crop_mode == 'manual':
            # Disable preset dropdown, enable manual inputs
            for widget in self.preset_crop_frame.winfo_children():
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='disabled')
            self.crop_left_spinbox.config(state='normal')
            self.crop_right_spinbox.config(state='normal')
            self.crop_top_spinbox.config(state='normal')
            self.crop_bottom_spinbox.config(state='normal')
            
        else:  # 'none'
            # Disable both preset and manual inputs
            for widget in self.preset_crop_frame.winfo_children():
                if isinstance(widget, ttk.Combobox):
                    widget.config(state='disabled')
            self.crop_left_spinbox.config(state='disabled')
            self.crop_right_spinbox.config(state='disabled')
            self.crop_top_spinbox.config(state='disabled')
            self.crop_bottom_spinbox.config(state='disabled')
    
    def load_video_info(self):
        """Load video information"""
        try:
            if not COMPARISON_CORE_AVAILABLE:
                self.resolution_label.config(text="Core not available", foreground='red')
                return
                
            # Try to get video info using the comparison core
            threading.Thread(target=self._load_video_info_worker, daemon=True).start()
            
        except Exception as e:
            self.resolution_label.config(text=f"Error: {str(e)}", foreground='red')
    
    def _load_video_info_worker(self):
        """Worker thread for loading video information"""
        try:
            from comparev2 import create_video_processor
            
            processor = create_video_processor()
            video_clip = processor.load_video(self.file_path)
            
            if processor.mode == "vapoursynth":
                width, height = video_clip.width, video_clip.height
                frames = len(video_clip)
            elif processor.mode == "opencv":
                width = int(video_clip.get(processor.cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video_clip.get(processor.cv2.CAP_PROP_FRAME_HEIGHT))
                frames = int(video_clip.get(processor.cv2.CAP_PROP_FRAME_COUNT))
                video_clip.release()
            else:
                width, height, frames = 1920, 1080, 1000
            
            # Store original dimensions for crop preset scaling
            self._original_width = width
            self._original_height = height
            
            # Update UI in main thread
            resolution_text = f"{width}x{height} ({frames} frames)"
            self.dialog.after(0, lambda: self.resolution_label.config(text=resolution_text, foreground='green'))
            
            # Update default resize values
            self.dialog.after(0, lambda: self.width_var.set(width))
            self.dialog.after(0, lambda: self.height_var.set(height))
            
        except Exception as e:
            error_text = f"Detection failed: {str(e)}"
            self.dialog.after(0, lambda: self.resolution_label.config(text=error_text, foreground='red'))
    
    def get_crop_preset_values(self, preset_label, video_width=1920, video_height=1080):
        """Convert crop preset label to actual crop values based on video dimensions"""
        # Handle empty or none preset
        if not preset_label or preset_label.strip() == '':
            return {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
        
        # Find the preset key by matching the label
        preset_key = None
        for key, preset_data in self.crop_preset_map.items():
            if preset_data['label'] == preset_label:
                preset_key = key
                break
        
        if preset_key and preset_key in self.crop_preset_map:
            base_crop = self.crop_preset_map[preset_key]['crop'].copy()
            
            # NEW BEHAVIOR: Crop values are applied at TARGET resolution (after resize)
            # This means 140px always means exactly 140px regardless of source resolution
            # No scaling needed - crop presets are designed for target resolution (1080p)
            
            # Validate that crop values don't exceed target video dimensions
            # Use standard 1920x1080 as reference since that's what presets are designed for
            target_width = 1920
            target_height = 1080
            
            if (base_crop['left'] + base_crop['right'] >= target_width or 
                base_crop['top'] + base_crop['bottom'] >= target_height):
                print(f"[ERROR] Crop preset '{preset_label}' values {base_crop} would exceed standard target resolution {target_width}x{target_height}")
                return {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
            
            return base_crop
        else:
            print(f"[ERROR] Crop preset '{preset_label}' not found in preset map")
            return {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
    
    def load_existing_values(self):
        """Load existing video configuration values into the dialog"""
        if not self.existing_video:
            return
        
        video = self.existing_video
        
        # Set display name
        if 'name' in video:
            self.name_var.set(video['name'])
        
        # Set video type (for source vs encode)
        if self.comparison_type == 'source_vs_encode' and 'is_source' in video:
            self.type_var.set('source' if video['is_source'] else 'encode')
        
        # Set resize settings
        if 'resize' in video and video['resize']:
            if 'preset_resolution' in video and video['preset_resolution']:
                self.resize_var.set('preset')
                self.preset_var.set(video['preset_resolution'])
            elif 'width' in video and 'height' in video:
                self.resize_var.set('custom')
                self.width_var.set(video['width'])
                self.height_var.set(video['height'])
        else:
            self.resize_var.set('none')
        
        # Set crop settings
        if 'crop' in video and video['crop']:
            if 'preset_crop' in video and video['preset_crop']:
                self.crop_var.set('preset')
                self.crop_preset_var.set(video['preset_crop'])
            elif any(video['crop'].get(k, 0) for k in ['left', 'right', 'top', 'bottom']):
                self.crop_var.set('manual')
                # Set manual crop values
                self.crop_left_var.set(video['crop'].get('left', 0))
                self.crop_right_var.set(video['crop'].get('right', 0))
                self.crop_top_var.set(video['crop'].get('top', 0))
                self.crop_bottom_var.set(video['crop'].get('bottom', 0))
        else:
            self.crop_var.set('none')
        
        # Set trim/pad settings
        if 'trim_start' in video:
            self.trim_start_var.set(video['trim_start'])
        if 'trim_end' in video:
            self.trim_end_var.set(video['trim_end'])
        if 'pad_start' in video:
            self.pad_start_var.set(video['pad_start'])
        if 'pad_end' in video:
            self.pad_end_var.set(video['pad_end'])
        
        # Update the UI state after setting values
        self.dialog.after(10, self.update_resize_state)
        self.dialog.after(10, self.update_crop_state)
    
    def ok(self):
        """Handle OK button"""
        # Build result configuration
        self.result = {
            'path': self.file_path,
            'name': self.name_var.get().strip() or os.path.splitext(os.path.basename(self.file_path))[0],
            'width': 1920,
            'height': 1080,
        }
        
        if self.comparison_type == 'source_vs_encode':
            self.result['is_source'] = self.type_var.get() == 'source'
        else:
            self.result['is_source'] = True
        
        # Process resize settings
        resize_mode = self.resize_var.get()
        if resize_mode == 'preset':
            preset_label = self.preset_var.get()
            if preset_label in self.preset_map:
                width, height = self.preset_map[preset_label]
                self.result['resize'] = (width, height)
                self.result['preset_resolution'] = preset_label  # Save the preset name
            else:
                self.result['resize'] = None
                self.result['preset_resolution'] = None
        elif resize_mode == 'custom':
            self.result['resize'] = (self.width_var.get(), self.height_var.get())
            self.result['preset_resolution'] = None
        else:
            self.result['resize'] = None
            self.result['preset_resolution'] = None
        
        # Process crop settings
        crop_mode = self.crop_var.get()
        if crop_mode == 'preset':
            # Crop presets are now applied at target resolution (no scaling needed)
            preset_crop = self.get_crop_preset_values(
                self.crop_preset_var.get()
            )
            
            if any(preset_crop.values()):
                self.result['crop'] = preset_crop
                self.result['preset_crop'] = self.crop_preset_var.get()  # Save the preset name
            else:
                self.result['crop'] = None
                self.result['preset_crop'] = None
        elif crop_mode == 'manual':
            crop_values = {
                'left': self.crop_left_var.get(),
                'right': self.crop_right_var.get(),
                'top': self.crop_top_var.get(),
                'bottom': self.crop_bottom_var.get()
            }
            if any(crop_values.values()):
                self.result['crop'] = crop_values
                self.result['preset_crop'] = None
            else:
                self.result['crop'] = None
                self.result['preset_crop'] = None
        else:
            self.result['crop'] = None
            self.result['preset_crop'] = None
        
        # Additional settings
        self.result.update({
            'trim_start': self.trim_start_var.get(),
            'trim_end': self.trim_end_var.get(),
            'pad_start': self.pad_start_var.get(),
            'pad_end': self.pad_end_var.get()
        })
        
        self.dialog.destroy()
    
    def cancel(self):
        """Handle Cancel button"""
        self.result = None
        self.dialog.destroy()



    

def main():
    """Main application entry point"""
    if DND_AVAILABLE:
        try:
            root = TkinterDnD.Tk()
        except Exception as e:
            print(f"Warning: Could not initialize drag and drop support: {e}")
            root = tk.Tk()
    else:
        root = tk.Tk()
    
    app = ScreenshotComparisonGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
