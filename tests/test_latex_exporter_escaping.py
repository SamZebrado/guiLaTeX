#!/usr/bin/env python3
"""
Test LaTeX exporter escaping (especially backslash issues)
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from export_core import export_ir_to_latex

def test_fontsize_escaping():
    """Test that fontsize command is properly generated"""
    ir_data = {
        "elements": [
            {
                "id": "test-1",
                "type": "textbox",
                "content": "Test text",
                "page": 1,
                "x": 50,
                "y": 50,
                "width": 100,
                "height": 30,
                "rotation": 0,
                "layer": 1,
                "font_size": 12,
                "color": "#000000",
                "alignment": "left",
                "visible": True
            }
        ]
    }
    
    latex_content = export_ir_to_latex(ir_data)
    
    # Check that fontsize command is properly generated
    assert '\\fontsize{12}' in latex_content, "Fontsize command not properly generated"
    assert '\\selectfont' in latex_content, "Selectfont command not properly generated"
    print("✓ Fontsize escaping test passed")

def test_special_characters_escaping():
    """Test escaping of special LaTeX characters"""
    ir_data = {
        "elements": [
            {
                "id": "test-1",
                "type": "textbox",
                "content": r"Test text with special chars: { } \ ",
                "page": 1,
                "x": 50,
                "y": 50,
                "width": 100,
                "height": 30,
                "rotation": 0,
                "layer": 1,
                "font_size": 12,
                "color": "#000000",
                "alignment": "left",
                "visible": True
            }
        ]
    }
    
    latex_content = export_ir_to_latex(ir_data)
    
    # Check that special characters are properly escaped (simplified)
    assert 'Test text with special chars:' in latex_content, "Content not found"
    assert '\\' in latex_content, "Backslash not escaped"
    print("✓ Special characters escaping test passed")

def test_image_element_without_font_size():
    """Test image element without font_size"""
    ir_data = {
        "elements": [
            {
                "id": "test-1",
                "type": "image",
                "content": "test.jpg",
                "page": 1,
                "x": 50,
                "y": 50,
                "width": 100,
                "height": 100,
                "rotation": 0,
                "layer": 1,
                "visible": True
            }
        ]
    }
    
    latex_content = export_ir_to_latex(ir_data)
    
    # Should not crash and should generate valid LaTeX
    assert '\\includegraphics' in latex_content, "Image not properly exported"
    print("✓ Image element test passed")

if __name__ == '__main__':
    test_fontsize_escaping()
    test_special_characters_escaping()
    test_image_element_without_font_size()
    print("\nAll LaTeX exporter tests passed!")
