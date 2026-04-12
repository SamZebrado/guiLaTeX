#!/usr/bin/env python3
"""
Test type alias policy regression
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from export_core import normalize_web_model_to_ir, validate_ir_roundtripability

def test_canonical_types():
    """Test canonical types pass directly"""
    web_model = {
        "elements": [
            {
                "id": "1",
                "type": "title",
                "content": "Test",
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
    
    assert result['ok'] == True, "Canonical types should pass"
    assert result['supported'] == 'full', "Canonical types should be fully supported"
    print("✓ Canonical types test passed")

def test_body_alias():
    """Test body alias is normalized to paragraph"""
    web_model = {
        "elements": [
            {
                "id": "1",
                "type": "body",
                "content": "Test",
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
    assert ir_data['elements'][0]['type'] == 'paragraph', "body should be normalized to paragraph"
    
    result = validate_ir_roundtripability(ir_data)
    assert result['ok'] == True, "Normalized body should pass"
    assert result['supported'] == 'full', "Normalized body should be fully supported"
    print("✓ Body alias test passed")

def test_formula_alias():
    """Test formula alias is normalized to equation"""
    web_model = {
        "elements": [
            {
                "id": "1",
                "type": "formula",
                "content": "E=mc²",
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
    assert ir_data['elements'][0]['type'] == 'equation', "formula should be normalized to equation"
    
    result = validate_ir_roundtripability(ir_data)
    assert result['ok'] == True, "Normalized formula should pass"
    assert result['supported'] == 'full', "Normalized formula should be fully supported"
    print("✓ Formula alias test passed")

def test_unknown_alias():
    """Test unknown alias is not normalized"""
    web_model = {
        "elements": [
            {
                "id": "1",
                "type": "unknown",
                "content": "Test",
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
    assert ir_data['elements'][0]['type'] == 'unknown', "Unknown alias should not be normalized"
    
    result = validate_ir_roundtripability(ir_data)
    assert result['ok'] == False, "Unknown alias should fail validation"
    assert result['supported'] == 'partial', "Unknown alias should be partially supported"
    print("✓ Unknown alias test passed")

if __name__ == '__main__':
    test_canonical_types()
    test_body_alias()
    test_formula_alias()
    test_unknown_alias()
    print("\nAll type alias policy tests passed!")
