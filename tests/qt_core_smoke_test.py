#!/usr/bin/env python3
"""
Core Smoke Test for Qt Interface

This script tests the Core integration functionality of the Qt interface,
including IR to LaTeX export via Core functions.
"""

import os
import sys
import json

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_core_imports():
    """Test Core module imports"""
    print("=== Testing Core Imports ===")
    
    try:
        from export.core import normalize_qt_model_to_ir, export_ir_to_latex
        print("✓ Core module imported successfully")
        print("✓ normalize_qt_model_to_ir function found")
        print("✓ export_ir_to_latex function found")
        print("=== Core Imports Test PASSED ===")
        return True
    except Exception as e:
        print(f"=== Core Imports Test FAILED: {e} ===")
        return False

def test_ir_normalization():
    """Test IR normalization"""
    print("=== Testing IR Normalization ===")
    
    try:
        from export.core import normalize_qt_model_to_ir
        
        # Create test IR data
        test_ir = {
            "elements": [
                {
                    "id": "test_element",
                    "type": "textbox",
                    "content": "Test content",
                    "page": 1,
                    "x": 100,
                    "y": 100,
                    "width": 200,
                    "height": 50,
                    "rotation": 0,
                    "layer": 1,
                    "font_family_zh": "Noto Sans SC",
                    "font_family_en": "Inter",
                    "font_size": 12,
                    "color": "#000000",
                    "alignment": "left",
                    "visible": True
                }
            ]
        }
        
        # Normalize IR
        normalized_ir = normalize_qt_model_to_ir(test_ir)
        if normalized_ir:
            print("✓ IR normalization successful")
            print(f"✓ Normalized IR contains {len(normalized_ir.get('elements', []))} elements")
        else:
            print("✗ IR normalization returned None")
            return False
        
        print("=== IR Normalization Test PASSED ===")
        return True
        
    except Exception as e:
        print(f"=== IR Normalization Test FAILED: {e} ===")
        return False

def test_latex_export():
    """Test LaTeX export"""
    print("=== Testing LaTeX Export ===")
    
    try:
        from export.core import normalize_qt_model_to_ir, export_ir_to_latex
        
        # Create test IR data
        test_ir = {
            "elements": [
                {
                    "id": "test_title",
                    "type": "title",
                    "content": "Test Document",
                    "page": 1,
                    "x": 100,
                    "y": 50,
                    "width": 400,
                    "height": 40,
                    "rotation": 0,
                    "layer": 1,
                    "font_family_zh": "Noto Sans SC",
                    "font_family_en": "Inter",
                    "font_size": 24,
                    "color": "#000000",
                    "alignment": "center",
                    "visible": True
                },
                {
                    "id": "test_paragraph",
                    "type": "paragraph",
                    "content": "This is a test paragraph.",
                    "page": 1,
                    "x": 100,
                    "y": 100,
                    "width": 400,
                    "height": 80,
                    "rotation": 0,
                    "layer": 1,
                    "font_family_zh": "Noto Sans SC",
                    "font_family_en": "Inter",
                    "font_size": 12,
                    "color": "#000000",
                    "alignment": "left",
                    "visible": True
                }
            ]
        }
        
        # Normalize IR
        normalized_ir = normalize_qt_model_to_ir(test_ir)
        if not normalized_ir:
            print("✗ IR normalization failed")
            return False
        
        # Export to LaTeX
        latex_code = export_ir_to_latex(normalized_ir)
        if latex_code:
            print("✓ LaTeX export successful")
            print(f"✓ LaTeX code length: {len(latex_code)} characters")
            # Check for basic LaTeX structure
            if "documentclass" in latex_code and "begin{document}" in latex_code:
                print("✓ LaTeX code contains basic structure")
            else:
                print("✗ LaTeX code missing basic structure")
                return False
        else:
            print("✗ LaTeX export returned None")
            return False
        
        print("=== LaTeX Export Test PASSED ===")
        return True
        
    except Exception as e:
        print(f"=== LaTeX Export Test FAILED: {e} ===")
        return False

def test_latex_file_generation():
    """Test LaTeX file generation"""
    print("=== Testing LaTeX File Generation ===")
    
    try:
        from export.core import normalize_qt_model_to_ir, export_ir_to_latex
        
        # Create test IR data
        test_ir = {
            "elements": [
                {
                    "id": "test_element",
                    "type": "textbox",
                    "content": "Test content",
                    "page": 1,
                    "x": 100,
                    "y": 100,
                    "width": 200,
                    "height": 50,
                    "rotation": 0,
                    "layer": 1,
                    "font_family_zh": "Noto Sans SC",
                    "font_family_en": "Inter",
                    "font_size": 12,
                    "color": "#000000",
                    "alignment": "left",
                    "visible": True
                }
            ]
        }
        
        # Normalize IR
        normalized_ir = normalize_qt_model_to_ir(test_ir)
        if not normalized_ir:
            print("✗ IR normalization failed")
            return False
        
        # Export to LaTeX
        latex_code = export_ir_to_latex(normalized_ir)
        if not latex_code:
            print("✗ LaTeX export failed")
            return False
        
        # Save to file
        export_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
        os.makedirs(export_dir, exist_ok=True)
        latex_path = os.path.join(export_dir, 'test_export.tex')
        
        with open(latex_path, 'w', encoding='utf-8') as f:
            f.write(latex_code)
        
        # Check if file exists
        if os.path.exists(latex_path):
            print(f"✓ LaTeX file generated successfully: {latex_path}")
            print(f"✓ File size: {os.path.getsize(latex_path)} bytes")
        else:
            print("✗ LaTeX file not generated")
            return False
        
        print("=== LaTeX File Generation Test PASSED ===")
        return True
        
    except Exception as e:
        print(f"=== LaTeX File Generation Test FAILED: {e} ===")
        return False

def main():
    """Run all tests"""
    print("Starting Qt Core Smoke Tests...\n")
    
    tests = [
        test_core_imports,
        test_ir_normalization,
        test_latex_export,
        test_latex_file_generation
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
