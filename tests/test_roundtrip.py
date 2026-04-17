# Test roundtrip functionality for ExportCore

import pytest
from export_core import (
    export_ir_to_latex,
    import_own_exported_tex_to_ir,
    validate_tex_profile,
    extract_embedded_ir_from_tex
)


def test_golden_sample_roundtrip():
    """Test roundtrip with golden sample"""
    # Golden sample IR
    golden_ir = {
        "elements": [
            {
                "id": "title-1",
                "type": "title",
                "content": "测试文档",
                "page": 1,
                "x": 50,
                "y": 30,
                "width": 110,
                "height": 20,
                "rotation": 0,
                "layer": 10,
                "font_family_zh": "SimSun",
                "font_family_en": "Times New Roman",
                "font_size": 24,
                "color": "#000000",
                "alignment": "center",
                "visible": True
            },
            {
                "id": "paragraph-1",
                "type": "paragraph",
                "content": "这是一段测试文本",
                "page": 1,
                "x": 30,
                "y": 60,
                "width": 150,
                "height": 20,
                "rotation": 0,
                "layer": 9,
                "font_family_zh": "SimSun",
                "font_family_en": "Times New Roman",
                "font_size": 12,
                "color": "#333333",
                "alignment": "left",
                "visible": True
            },
            {
                "id": "equation-1",
                "type": "equation",
                "content": "E = mc^2",
                "page": 1,
                "x": 80,
                "y": 90,
                "width": 50,
                "height": 20,
                "rotation": 0,
                "layer": 8,
                "font_family_zh": "SimSun",
                "font_family_en": "Times New Roman",
                "font_size": 14,
                "color": "#0066cc",
                "alignment": "center",
                "visible": True
            },
            {
                "id": "image-1",
                "type": "image",
                "content": "test.jpg",
                "page": 1,
                "x": 60,
                "y": 120,
                "width": 90,
                "height": 60,
                "rotation": 0,
                "layer": 7,
                "visible": True
            }
        ]
    }
    
    # Export to LaTeX
    tex_content = export_ir_to_latex(golden_ir)
    assert tex_content
    
    # Validate tex profile
    validation_result = validate_tex_profile(tex_content)
    assert validation_result["ok"], f"Tex profile validation failed: {validation_result['issues']}"
    
    # Import back to IR
    imported_ir = import_own_exported_tex_to_ir(tex_content)
    assert imported_ir
    
    # Compare original and imported IR
    assert len(imported_ir["elements"]) == len(golden_ir["elements"])
    
    for original, imported in zip(golden_ir["elements"], imported_ir["elements"]):
        # Check core fields
        assert original["id"] == imported["id"]
        assert original["type"] == imported["type"]
        assert original["content"] == imported["content"]
        assert original["page"] == imported["page"]
        assert original["x"] == imported["x"]
        assert original["y"] == imported["y"]
        assert original["width"] == imported["width"]
        assert original["height"] == imported["height"]
        assert original["rotation"] == imported["rotation"]
        assert original["layer"] == imported["layer"]
        assert original["visible"] == imported["visible"]
        
        # Check optional fields
        assert original.get("font_family_zh") == imported.get("font_family_zh")
        assert original.get("font_family_en") == imported.get("font_family_en")
        assert original.get("font_size") == imported.get("font_size")
        assert original.get("color") == imported.get("color")
        assert original.get("alignment") == imported.get("alignment")


def test_rotation_sample_roundtrip():
    """Test roundtrip with rotation"""
    rotation_ir = {
        "elements": [
            {
                "id": "rotated-text-1",
                "type": "paragraph",
                "content": "旋转文本",
                "page": 1,
                "x": 50,
                "y": 50,
                "width": 100,
                "height": 20,
                "rotation": 45,
                "layer": 5,
                "font_family_zh": "SimSun",
                "font_family_en": "Times New Roman",
                "font_size": 14,
                "color": "#ff6600",
                "alignment": "center",
                "visible": True
            }
        ]
    }
    
    # Export to LaTeX
    tex_content = export_ir_to_latex(rotation_ir)
    assert tex_content
    
    # Import back to IR
    imported_ir = import_own_exported_tex_to_ir(tex_content)
    assert imported_ir
    
    # Verify rotation is preserved
    assert imported_ir["elements"][0]["rotation"] == 45


def test_extract_embedded_ir_from_tex():
    """Test extracting embedded IR from tex"""
    test_ir = {
        "elements": [
            {
                "id": "test-1",
                "type": "paragraph",
                "content": "Test",
                "page": 1,
                "x": 0,
                "y": 0,
                "width": 100,
                "height": 20,
                "rotation": 0,
                "layer": 0,
                "visible": True
            }
        ]
    }
    
    # Export to get tex with embedded IR
    tex_content = export_ir_to_latex(test_ir)
    
    # Extract IR
    extracted_ir = extract_embedded_ir_from_tex(tex_content)
    assert extracted_ir
    assert len(extracted_ir["elements"]) == 1
    assert extracted_ir["elements"][0]["id"] == "test-1"


def test_validate_tex_profile_invalid():
    """Test validate_tex_profile with invalid tex"""
    invalid_tex = "\\documentclass{article}\\begin{document}Invalid\\end{document}"
    
    validation_result = validate_tex_profile(invalid_tex)
    assert not validation_result["ok"]
    assert len(validation_result["issues"]) > 0