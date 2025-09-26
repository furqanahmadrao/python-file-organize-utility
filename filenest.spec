# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for FileNest
Creates single-file executable for easy distribution
"""

import os
import sys
from pathlib import Path

# Get the project directory
project_dir = os.path.dirname(os.path.abspath(SPEC))

# Define the main script
main_script = os.path.join(project_dir, 'organizer.py')

# Additional files to include
added_files = [
    (os.path.join(project_dir, 'readme_docs.md'), '.'),
    (os.path.join(project_dir, 'config_setup.py'), '.'),
    (os.path.join(project_dir, 'log_viewer.py'), '.'),
]

# Hidden imports for optional dependencies
hidden_imports = [
    'watchdog',
    'watchdog.observers',
    'watchdog.events',
]

block_cipher = None

a = Analysis(
    [main_script],
    pathex=[project_dir],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove unnecessary modules to reduce size
excluded_modules = [
    'tkinter', 'tk', 'tcl',  # GUI frameworks
    'matplotlib', 'numpy', 'pandas',  # Data science
    'PIL', 'Pillow',  # Image processing
    'requests', 'urllib3',  # HTTP libraries (if not needed)
    'sqlite3',  # Database (if not needed)
    'email',  # Email modules
    'xml',  # XML processing
    'multiprocessing',  # If not using multiprocessing
]

# Filter out excluded modules
a.binaries = [x for x in a.binaries if not any(exc in x[0].lower() for exc in excluded_modules)]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create single file executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='filenest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression to reduce file size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
)

# Alternative: Create directory distribution (uncomment if preferred)
# exe = EXE(
#     pyz,
#     a.scripts,
#     [],
#     exclude_binaries=True,
#     name='filenest',
#     debug=False,
#     bootloader_ignore_signals=False,
#     strip=False,
#     upx=True,
#     console=True,
#     disable_windowed_traceback=False,
#     argv_emulation=False,
#     target_arch=None,
#     codesign_identity=None,
#     entitlements_file=None,
# )

# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='filenest'
# )