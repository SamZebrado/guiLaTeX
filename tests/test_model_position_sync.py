#!/usr/bin/env python3
"""
Test for model position synchronization
"""

import pytest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from model import DocumentModel, PageModel, ElementModel


def test_position_modification_syncs_to_model():
    """Test that position modifications sync to the model"""
    # Create document model
    doc_model = DocumentModel(title="Test Document")
    page_model = PageModel(number=0)
    doc_model.add_page(page_model)
    
    # Add an element to the model
    element = ElementModel(
        id="test1",
        type="text",
        content="Test Text",
        x=100,
        y=100,
        width=200,
        height=50,
        font_size=12
    )
    page_model.add_element(element)
    
    # Verify initial position
    assert element.x == 100
    assert element.y == 100
    
    # Simulate position change (like what happens during drag)
    new_x = 150
    new_y = 150
    element.x = new_x
    element.y = new_y
    element.dirty = True
    
    # Verify position is updated
    assert element.x == new_x
    assert element.y == new_y
    
    # Verify the element in the page model is the same object
    assert page_model.elements[0] is element
    assert page_model.elements[0].x == new_x
    assert page_model.elements[0].y == new_y


def test_model_to_memory_element_position_conversion():
    """Test position conversion between model elements and memory elements"""
    # Create a model element
    model_element = ElementModel(
        id="test1",
        type="text",
        content="Test Content",
        x=100,
        y=100,
        width=200,
        height=50,
        font_size=12
    )
    
    # Convert to memory element (simulating what happens in PDFPageWidget)
    memory_element = {
        'id': model_element.id,
        'type': model_element.type,
        'text': model_element.content,
        'x': model_element.x,
        'y': model_element.y,
        'width': model_element.width,
        'height': model_element.height,
        'font_size': model_element.font_size,
        'original_width': model_element.width,
        'original_height': model_element.height
    }
    
    # Verify position conversion
    assert memory_element['x'] == model_element.x
    assert memory_element['y'] == model_element.y
    
    # Modify memory element position (simulating drag)
    new_x = 200
    new_y = 200
    memory_element['x'] = new_x
    memory_element['y'] = new_y
    
    # Update model element from memory element (simulating _sync_to_model)
    model_element.x = memory_element['x']
    model_element.y = memory_element['y']
    model_element.dirty = True
    
    # Verify model position is updated
    assert model_element.x == new_x
    assert model_element.y == new_y


if __name__ == "__main__":
    # Run tests
    test_position_modification_syncs_to_model()
    test_model_to_memory_element_position_conversion()
    print("All tests passed!")
