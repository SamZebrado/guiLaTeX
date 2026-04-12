#!/usr/bin/env python3
"""
Test validate_ir_roundtripability function
"""

import json
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from export_core import validate_ir_roundtripability

def test_golden_sample():
    """Test with golden sample (should pass)"""
    with open('export_core/samples/golden_sample_ir.json', 'r', encoding='utf-8') as f:
        ir_data = json.load(f)
    
    result = validate_ir_roundtripability(ir_data)
    
    assert result['ok'] == True, "Golden sample should pass validation"
    assert result['supported'] == 'full', "Golden sample should be fully supported"

def test_with_group_transform_field():
    """Test with group transform field (should return unsupported)"""
    with open('export_core/samples/golden_sample_ir.json', 'r', encoding='utf-8') as f:
        ir_data = json.load(f)
    
    ir_data['elements'][0]['group_id'] = 'group-1'
    
    result = validate_ir_roundtripability(ir_data)
    
    assert result['ok'] == False, "Should fail with group_id field"
    assert result['supported'] == 'unsupported', "Should be unsupported with group_id field"

def test_with_missing_field():
    """Test with missing required field (should return partial)"""
    with open('export_core/samples/golden_sample_ir.json', 'r', encoding='utf-8') as f:
        ir_data = json.load(f)
    
    del ir_data['elements'][0]['rotation']
    
    result = validate_ir_roundtripability(ir_data)
    
    assert result['ok'] == False, "Should fail with missing field"
    assert result['supported'] == 'partial', "Should be partially supported with missing field"

def test_with_multiple_pages():
    """Test with multiple pages (should return partial)"""
    with open('export_core/samples/golden_sample_ir.json', 'r', encoding='utf-8') as f:
        ir_data = json.load(f)
    
    ir_data['elements'][0]['page'] = 2
    
    result = validate_ir_roundtripability(ir_data)
    
    assert result['ok'] == False, "Should fail with multiple pages"
    assert result['supported'] == 'partial', "Should be partially supported with multiple pages"

def test_with_rotation_sample():
    """Test with rotation regression sample (should pass)"""
    with open('export_core/samples/regression_sample_1_rotation.json', 'r', encoding='utf-8') as f:
        ir_data = json.load(f)
    
    result = validate_ir_roundtripability(ir_data)
    
    assert result['ok'] == True, "Rotation sample should pass validation"
    assert result['supported'] == 'full', "Rotation sample should be fully supported"

def test_with_image_font_size_none():
    """Test with image element having font_size=None (Web line real bug)"""
    with open('export_core/samples/golden_sample_ir.json', 'r', encoding='utf-8') as f:
        ir_data = json.load(f)
    
    # Add an image element with font_size=None (Web line real case)
    image_element = {
        "id": "image-test",
        "type": "image",
        "content": "test.jpg",
        "page": 1,
        "x": 100,
        "y": 100,
        "width": 100,
        "height": 100,
        "rotation": 0,
        "layer": 1,
        "font_size": None,  # This is the real bug case
        "color": "#000000",
        "alignment": "left",
        "visible": True
    }
    ir_data['elements'].append(image_element)
    
    result = validate_ir_roundtripability(ir_data)
    
    # This should be partial support since font_size is None
    assert result['ok'] == False, "Should fail with font_size=None"
    assert result['supported'] == 'partial', "Should be partially supported with font_size=None"

def test_with_web_real_exported_ir():
    """Test with real Web exported IR"""
    from export_core import normalize_web_model_to_ir
    
    with open('web_prototype/web_real_exported_ir.json', 'r', encoding='utf-8') as f:
        web_model = json.load(f)
    
    # 先通过 normalize_web_model_to_ir 转换，验证类型映射
    ir_data = normalize_web_model_to_ir(web_model)
    
    # 检查类型是否被正确映射
    types = [element['type'] for element in ir_data['elements']]
    assert 'body' not in types, "'body' type should be mapped to 'paragraph'"
    assert 'formula' not in types, "'formula' type should be mapped to 'equation'"
    assert 'paragraph' in types, "Should contain 'paragraph' type"
    assert 'equation' in types, "Should contain 'equation' type"
    
    # 验证转换后的 IR 应该完全通过验证
    result = validate_ir_roundtripability(ir_data)
    assert result['ok'] == True, "Converted Web IR should pass validation"
    assert result['supported'] == 'full', "Converted Web IR should be fully supported"

if __name__ == '__main__':
    test_golden_sample()
    test_with_group_transform_field()
    test_with_missing_field()
    test_with_multiple_pages()
    test_with_rotation_sample()
    test_with_image_font_size_none()
    test_with_web_real_exported_ir()
    print("All tests passed!")
