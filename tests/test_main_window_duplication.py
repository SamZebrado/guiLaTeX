#!/usr/bin/env python3
"""
MainWindow duplication detection test - 真实路径测试
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from PyQt6.QtWidgets import QApplication
# Create QApplication instance first
app = QApplication(sys.argv)

from gui.main import MainWindow

def test_main_window_duplication():
    """测试 MainWindow.create_initial_pdf 路径下的 duplication"""
    print("=== Test: MainWindow create_initial_pdf Duplication ===")
    
    # Create main window
    window = MainWindow()
    
    # Check initial state
    if window.pdf_canvas and window.pdf_canvas.page_widget:
        page_widget = window.pdf_canvas.page_widget
        
        print(f"After initial PDF - memory_elements count: {len(page_widget.memory_elements)}")
        
        # Check for duplicate IDs
        unique_ids = set()
        duplicate_found = False
        duplicate_ids = []
        
        for elem in page_widget.memory_elements:
            if elem['id'] in unique_ids:
                duplicate_found = True
                duplicate_ids.append(elem['id'])
            unique_ids.add(elem['id'])
        
        print(f"Unique IDs count: {len(unique_ids)}")
        print(f"Duplicate found: {duplicate_found}")
        if duplicate_found:
            print(f"Duplicate IDs: {duplicate_ids}")
        
        # Check model
        if window.document_model and window.document_model.pages:
            page_model = window.document_model.pages[0]
            print(f"Page model elements count: {len(page_model.elements)}")
            
            # Check model for duplicates
            model_ids = set()
            model_duplicate_found = False
            for elem in page_model.elements:
                if elem.id in model_ids:
                    model_duplicate_found = True
                    print(f"Model duplicate ID: {elem.id}")
                model_ids.add(elem.id)
            
            print(f"Model duplicate found: {model_duplicate_found}")
        
        return not duplicate_found
    else:
        print("No page widget available")
        return False

if __name__ == "__main__":
    print("MainWindow Duplication Test - 真实路径测试")
    print("=" * 50)
    
    result = test_main_window_duplication()
    
    print("\n" + "=" * 50)
    if result:
        print("✓ MainWindow duplication test PASSED - 没有发现重复对象")
        sys.exit(0)
    else:
        print("✗ MainWindow duplication test FAILED - 发现重复对象")
        sys.exit(1)
