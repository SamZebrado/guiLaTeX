#!/usr/bin/env python3
"""
Test exporter boundary - unknown types should not reach exporter
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from export_core import normalize_web_model_to_ir, validate_ir_roundtripability, export_ir_to_latex

def test_canonical_types_export():
    """Test canonical types can be exported"""
    canonical_types = ['title', 'author', 'paragraph', 'textbox', 'equation', 'image']
    
    for canonical_type in canonical_types:
        web_model = {
            "elements": [
                {
                    "id": "1",
                    "type": canonical_type,
                    "content": f"Test {canonical_type}",
                    "x": 100,
                    "y": 100,
                    "width": 100,
                    "height": 20,
                    "rotation": 0,
                    "layerId": 1,
                    "fontSize": 12,
                    "color": "#000000",
                    "textAlign": "left",
                    "visible": True
                }
            ]
        }
        
        ir_data = normalize_web_model_to_ir(web_model)
        result = validate_ir_roundtripability(ir_data)
        assert result['ok'] == True, f"{canonical_type} should pass validation"
        
        # 应该能成功导出
        try:
            latex_content = export_ir_to_latex(ir_data)
            assert f"Test {canonical_type}" in latex_content, f"exporter should handle {canonical_type}"
        except Exception as e:
            assert False, f"exporter should not crash with {canonical_type}: {e}"
    
    print("✓ Canonical types export test passed")

def test_aliases_export():
    """Test aliases can be exported after normalization"""
    alias_mappings = {
        'body': 'paragraph',
        'formula': 'equation'
    }
    
    for alias_type, canonical_type in alias_mappings.items():
        web_model = {
            "elements": [
                {
                    "id": "1",
                    "type": alias_type,
                    "content": f"Test {alias_type}",
                    "x": 100,
                    "y": 100,
                    "width": 100,
                    "height": 20,
                    "rotation": 0,
                    "layerId": 1,
                    "fontSize": 12,
                    "color": "#000000",
                    "textAlign": "left",
                    "visible": True
                }
            ]
        }
        
        ir_data = normalize_web_model_to_ir(web_model)
        assert ir_data['elements'][0]['type'] == canonical_type, f"{alias_type} should be normalized to {canonical_type}"
        
        result = validate_ir_roundtripability(ir_data)
        assert result['ok'] == True, f"Normalized {alias_type} should pass validation"
        
        # 应该能成功导出
        try:
            latex_content = export_ir_to_latex(ir_data)
            assert f"Test {alias_type}" in latex_content, f"exporter should handle normalized {alias_type}"
        except Exception as e:
            assert False, f"exporter should not crash with normalized {alias_type}: {e}"
    
    print("✓ Aliases export test passed")

def test_unknown_alias_blocked():
    """Test unknown alias is blocked from exporter"""
    web_model = {
        "elements": [
            {
                "id": "1",
                "type": "caption",
                "content": "Test caption",
                "x": 100,
                "y": 100,
                "width": 100,
                "height": 20,
                "rotation": 0,
                "layerId": 1,
                "fontSize": 12,
                "color": "#000000",
                "textAlign": "left",
                "visible": True
            }
        ]
    }
    
    # 1. normalize 不会映射
    ir_data = normalize_web_model_to_ir(web_model)
    assert ir_data['elements'][0]['type'] == 'caption', "caption should not be normalized"
    
    # 2. validator 会失败
    result = validate_ir_roundtripability(ir_data)
    assert result['ok'] == False, "caption should fail validation"
    assert result['supported'] == 'partial', "caption should be partially supported"
    
    # 3. exporter 应该抛出异常
    try:
        latex_content = export_ir_to_latex(ir_data)
        assert False, "exporter should raise error for unknown type"
    except ValueError as e:
        assert "Unknown element type" in str(e), "exporter should raise specific error for unknown type"
    except Exception as e:
        assert False, f"exporter should raise ValueError for unknown type, got: {type(e)}"
    
    print("✓ Unknown alias blocked test passed")

def test_direct_unknown_type_blocked():
    """Test direct unknown type is blocked from exporter"""
    # 直接创建包含未知类型的 IR
    ir_data = {
        "elements": [
            {
                "id": "1",
                "type": "unknown",
                "content": "Test unknown",
                "page": 1,
                "x": 100,
                "y": 100,
                "width": 100,
                "height": 20,
                "rotation": 0,
                "layer": 1,
                "font_size": 12,
                "color": "#000000",
                "alignment": "left",
                "visible": True
            }
        ]
    }
    
    # exporter 应该抛出异常
    try:
        latex_content = export_ir_to_latex(ir_data)
        assert False, "exporter should raise error for direct unknown type"
    except ValueError as e:
        assert "Unknown element type" in str(e), "exporter should raise specific error for direct unknown type"
    except Exception as e:
        assert False, f"exporter should raise ValueError for direct unknown type, got: {type(e)}"
    
    print("✓ Direct unknown type blocked test passed")

if __name__ == '__main__':
    test_canonical_types_export()
    test_aliases_export()
    test_unknown_alias_blocked()
    test_direct_unknown_type_blocked()
    print("\nAll exporter boundary tests passed!")
