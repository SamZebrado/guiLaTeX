#!/usr/bin/env python3
"""
UI Smoke Test for Qt Interface

This script tests the basic functionality of the Qt interface,
including UI structure, property panel scrollability, and basic interactions.
"""

import os
import sys
import json
from PyQt6.QtWidgets import QApplication

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_ui_structure():
    """Test UI structure"""
    print("=== Testing UI Structure ===")
    
    try:
        from gui.main import MainWindow
        
        # Create application
        app = QApplication(sys.argv)
        
        # Create main window
        window = MainWindow()
        
        # Test UI components
        print("✓ MainWindow created successfully")
        print(f"✓ Window title: {window.windowTitle()}")
        print(f"✓ Window size: {window.size().width()}x{window.size().height()}")
        
        # Test PDF canvas
        if hasattr(window, 'pdf_canvas'):
            print("✓ PDF canvas initialized")
        
        # Test property panel
        if hasattr(window, 'property_panel'):
            print("✓ Property panel initialized")
            print(f"✓ Property panel minimum width: {window.property_panel.minimumWidth()}")
            print(f"✓ Property panel maximum width: {window.property_panel.maximumWidth()}")
        
        # Test menu bar
        menu_bar = window.menuBar()
        if menu_bar:
            print("✓ Menu bar created")
            # Check menu items
            menus = menu_bar.actions()
            menu_names = [action.text() for action in menus]
            print(f"✓ Menu items: {menu_names}")
        
        # Close window
        window.close()
        
        print("=== UI Structure Test PASSED ===")
        return True
        
    except Exception as e:
        print(f"=== UI Structure Test FAILED: {e} ===")
        return False

def test_property_panel_scroll():
    """Test property panel scrollability"""
    print("=== Testing Property Panel Scrollability ===")
    
    try:
        from gui.properties import PropertyPanel
        
        # Create application
        app = QApplication(sys.argv)
        
        # Create property panel
        panel = PropertyPanel()
        
        # Check if scroll area exists
        if hasattr(panel, 'scroll_area'):
            print("✓ Scroll area initialized")
            print(f"✓ Scroll area widget resizable: {panel.scroll_area.widgetResizable()}")
        else:
            print("✗ Scroll area not found")
            return False
        
        # Close panel
        panel.close()
        
        print("=== Property Panel Scroll Test PASSED ===")
        return True
        
    except Exception as e:
        print(f"=== Property Panel Scroll Test FAILED: {e} ===")
        return False

def test_font_list():
    """Test font list contains only safe fonts"""
    print("=== Testing Font List ===")
    
    try:
        from gui.properties import PropertyPanel
        
        # Create application
        app = QApplication(sys.argv)
        
        # Create property panel
        panel = PropertyPanel()
        
        # Check font lists
        safe_fonts = ["Noto Sans SC", "Source Han Sans SC", "Inter", "Noto Sans", "Sans Serif"]
        
        # Check Chinese font list
        zh_fonts = [panel.font_family_zh_combo.itemText(i) for i in range(panel.font_family_zh_combo.count())]
        print(f"✓ Chinese font list: {zh_fonts}")
        for font in zh_fonts:
            if font not in safe_fonts:
                print(f"✗ Found non-safe font: {font}")
                return False
        
        # Check English font list
        en_fonts = [panel.font_family_en_combo.itemText(i) for i in range(panel.font_family_en_combo.count())]
        print(f"✓ English font list: {en_fonts}")
        for font in en_fonts:
            if font not in safe_fonts:
                print(f"✗ Found non-safe font: {font}")
                return False
        
        # Close panel
        panel.close()
        
        print("=== Font List Test PASSED ===")
        return True
        
    except Exception as e:
        print(f"=== Font List Test FAILED: {e} ===")
        return False

def test_export_ir():
    """Test IR export functionality"""
    print("=== Testing IR Export ===")
    
    try:
        from gui.main import MainWindow
        
        # Create application
        app = QApplication(sys.argv)
        
        # Create main window
        window = MainWindow()
        
        # Test IR export
        if hasattr(window, 'export_ir'):
            # Mock PDF canvas for testing
            if hasattr(window, 'pdf_canvas') and hasattr(window.pdf_canvas, 'export_model_to_ir'):
                ir_data = window.pdf_canvas.export_model_to_ir()
                if ir_data:
                    print("✓ IR export successful")
                    print(f"✓ IR data contains {len(ir_data.get('elements', []))} elements")
                else:
                    print("✗ IR export returned None")
                    return False
            else:
                print("✗ PDF canvas or export_model_to_ir method not found")
                return False
        else:
            print("✗ export_ir method not found")
            return False
        
        # Close window
        window.close()
        
        print("=== IR Export Test PASSED ===")
        return True
        
    except Exception as e:
        print(f"=== IR Export Test FAILED: {e} ===")
        return False

def main():
    """Run all tests"""
    print("Starting Qt UI Smoke Tests...\n")
    
    tests = [
        test_ui_structure,
        test_property_panel_scroll,
        test_font_list,
        test_export_ir
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Summary
    print("=== Test Summary ===")
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(tests) - sum(results)}")
    
    if all(results):
        print("\n🎉 All tests PASSED!")
        return 0
    else:
        print("\n❌ Some tests FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
