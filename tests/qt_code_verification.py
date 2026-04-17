#!/usr/bin/env python3
"""
Code Verification Test for Qt Interface

This script verifies the code structure and syntax of the Qt interface,
without requiring PyQt6 to be installed or running.
"""

import os
import sys
import ast

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_file_syntax(file_path):
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def check_imports(file_path):
    """Check if required imports are present"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required imports
        required_imports = [
            'PyQt6.QtWidgets',
            'PyQt6.QtGui',
            'PyQt6.QtCore',
            'gui.properties',
            'gui.pdf_canvas'
        ]
        
        missing_imports = []
        for imp in required_imports:
            if imp not in content:
                missing_imports.append(imp)
        
        return missing_imports
    except Exception as e:
        return [f"Error checking imports: {e}"]

def check_method_exists(file_path, method_name):
    """Check if a method exists in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple check for method definition
        return f'def {method_name}' in content or f'def {method_name}(' in content
    except Exception as e:
        return False

def check_ui_structure():
    """Check UI structure"""
    print("=== Checking UI Structure ===")
    
    # Check main.py
    main_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'main.py')
    
    # Check syntax
    syntax_valid, error = check_file_syntax(main_file)
    if not syntax_valid:
        print(f"✗ main.py syntax error: {error}")
        return False
    else:
        print("✓ main.py syntax is valid")
    
    # Check imports
    missing_imports = check_imports(main_file)
    if missing_imports:
        print(f"✗ main.py missing imports: {missing_imports}")
        return False
    else:
        print("✓ main.py has all required imports")
    
    # Check required methods
    required_methods = [
        'create_menu_bar',
        'export_ir',
        'export_latex',
        'copy_element',
        'paste_element',
        'delete_element',
        'move_element_up',
        'move_element_down',
        'move_element_to_top',
        'move_element_to_bottom',
        'zoom_in',
        'zoom_out',
        'reset_view'
    ]
    
    missing_methods = []
    for method in required_methods:
        if not check_method_exists(main_file, method):
            missing_methods.append(method)
    
    if missing_methods:
        print(f"✗ main.py missing methods: {missing_methods}")
        return False
    else:
        print("✓ main.py has all required methods")
    
    print("=== UI Structure Check PASSED ===")
    return True

def check_property_panel():
    """Check property panel"""
    print("=== Checking Property Panel ===")
    
    # Check properties.py
    properties_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'properties.py')
    
    # Check syntax
    syntax_valid, error = check_file_syntax(properties_file)
    if not syntax_valid:
        print(f"✗ properties.py syntax error: {error}")
        return False
    else:
        print("✓ properties.py syntax is valid")
    
    # Check for scroll area
    try:
        with open(properties_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'QScrollArea' in content and 'scroll_area' in content:
            print("✓ Property panel has scroll area")
        else:
            print("✗ Property panel missing scroll area")
            return False
    except Exception as e:
        print(f"✗ Error checking scroll area: {e}")
        return False
    
    # Check font list
    try:
        with open(properties_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        safe_fonts = ["Noto Sans SC", "Source Han Sans SC", "Inter", "Noto Sans", "Sans Serif"]
        for font in safe_fonts:
            if font in content:
                print(f"✓ Font '{font}' found in font list")
            else:
                print(f"✗ Font '{font}' missing from font list")
                return False
    except Exception as e:
        print(f"✗ Error checking font list: {e}")
        return False
    
    print("=== Property Panel Check PASSED ===")
    return True

def check_pdf_canvas():
    """Check PDF canvas"""
    print("=== Checking PDF Canvas ===")
    
    # Check pdf_canvas.py
    pdf_canvas_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'pdf_canvas.py')
    
    # Check syntax
    syntax_valid, error = check_file_syntax(pdf_canvas_file)
    if not syntax_valid:
        print(f"✗ pdf_canvas.py syntax error: {error}")
        return False
    else:
        print("✓ pdf_canvas.py syntax is valid")
    
    # Check for export_model_to_ir method
    if check_method_exists(pdf_canvas_file, 'export_model_to_ir'):
        print("✓ export_model_to_ir method found")
    else:
        print("✗ export_model_to_ir method missing")
        return False
    
    print("=== PDF Canvas Check PASSED ===")
    return True

def check_core_integration():
    """Check Core integration"""
    print("=== Checking Core Integration ===")
    
    # Check main.py for Core imports
    main_file = os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'main.py')
    
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'from export.core import normalize_qt_model_to_ir, export_ir_to_latex' in content:
            print("✓ Core imports found")
        else:
            print("✗ Core imports missing")
            return False
    except Exception as e:
        print(f"✗ Error checking Core imports: {e}")
        return False
    
    print("=== Core Integration Check PASSED ===")
    return True

def main():
    """Run all verification checks"""
    print("Starting Qt Code Verification...\n")
    
    checks = [
        check_ui_structure,
        check_property_panel,
        check_pdf_canvas,
        check_core_integration
    ]
    
    results = []
    for check in checks:
        result = check()
        results.append(result)
        print()
    
    # Summary
    print("=== Verification Summary ===")
    print(f"Total checks: {len(checks)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(checks) - sum(results)}")
    
    if all(results):
        print("\n🎉 All verification checks PASSED!")
        return 0
    else:
        print("\n❌ Some verification checks FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
