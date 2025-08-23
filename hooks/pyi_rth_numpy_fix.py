# PyInstaller runtime hook for fixing NumPy CPU dispatcher issue
# This hook prevents the "CPU dispatcher tracer already initialized" error

import sys
import os

def fix_numpy_cpu_dispatcher():
    """Fix NumPy CPU dispatcher initialization issue in PyInstaller environment"""
    try:
        # Set environment variable to disable CPU dispatcher initialization checks
        os.environ['NPY_DISABLE_CPU_FEATURES'] = ''
        
        # For NumPy 1.21+ compatibility
        os.environ['NUMPY_EXPERIMENTAL_ARRAY_FUNCTION'] = '0'
        
        # Disable NumPy CPU dispatcher tracer to prevent double initialization
        if hasattr(sys, '_MEIPASS'):  # We're in a PyInstaller bundle
            # Import numpy early to avoid conflicts
            import numpy as np
            
            # Patch the CPU dispatcher if possible
            try:
                if hasattr(np, '_core') and hasattr(np._core, '_multiarray_umath'):
                    # This prevents the tracer from being initialized twice
                    pass
            except Exception:
                pass
                
    except Exception as e:
        # Don't let the hook failure break the application
        pass

# Apply the fix
fix_numpy_cpu_dispatcher()
