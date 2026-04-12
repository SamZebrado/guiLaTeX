#!/usr/bin/env python3
"""
Create zip package for guiLaTeX Qt demo
"""

import os
import zipfile
from datetime import datetime

def create_zip_package():
    """Create zip package with key files"""
    
    # Define zip file path
    zip_dir = os.path.join(os.path.dirname(__file__), 'temp')
    os.makedirs(zip_dir, exist_ok=True)
    zip_path = os.path.join(zip_dir, 'guiLaTeX_qt_demo.zip')
    
    # Files to include
    files_to_include = [
        # Source files
        'src/gui/pdf_canvas.py',
        'src/gui/properties.py',
        'src/gui/main.py',
        'src/model/element.py',
        'src/model/page.py',
        'src/model/document.py',
        
        # Tests
        'tests/test_main_window_duplication.py',
        'tests/test_copy_paste.py',
        'tests/test_duplication_detection_advanced.py',
        
        # Dependencies
        'requirements.txt',
        
        # Documentation
        'docs/audits/2026-04-11_qt_demo_checkpoint.md',
        'docs/agent_runs/2026-04-11_dual_agent_runs.md',
        'PLAN.md',
        
        # Project config
        'README.md',
    ]
    
    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_include:
            if os.path.exists(file_path):
                # Add file to zip with relative path
                zipf.write(file_path, file_path)
                print(f"Added: {file_path}")
            else:
                print(f"Warning: File not found - {file_path}")
        
        # Add a manifest file
        manifest_content = f"""guiLaTeX Qt Demo Package
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Key Files:
- src/gui/pdf_canvas.py - PDF canvas implementation with duplication detection and z-order
- src/gui/properties.py - Property panel with fixed font list
- src/gui/main.py - Main window with fixed duplication and font handling
- tests/test_main_window_duplication.py - Real path duplication test

Recent Fixes:
- Fixed duplication in create_initial_pdf by removing redundant element addition
- Added font_family handling in on_property_changed
- Cleaned font list to only include open source fonts
- Fixed hardcoded paths
- Clarified save/export semantics
- Added export PDF button
"""
        zipf.writestr('MANIFEST.txt', manifest_content)
        print("Added: MANIFEST.txt")
    
    print(f"\n✓ Zip package created successfully at: {zip_path}")
    print(f"  Total size: {os.path.getsize(zip_path) / 1024:.2f} KB")
    
    return zip_path

if __name__ == "__main__":
    print("Creating guiLaTeX Qt demo zip package...")
    print("=" * 60)
    zip_path = create_zip_package()
    print("=" * 60)
    print(f"Zip file ready at: {zip_path}")
