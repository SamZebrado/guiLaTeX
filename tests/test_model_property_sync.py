#!/usr/bin/env python3
"""
Test for model property synchronization
"""

import pytest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from model import DocumentModel, PageModel, ElementModel


def test_model_property_sync():
    """Test that property modifications work correctly in the model"""
    # Create document model
    doc_model = DocumentModel(title="Test Document")
    page_model = PageModel(number=0)
    doc_model.add_page(page_model)
    
    # Add an element to the model
    element = ElementModel(
        id="test1",
        type="text",
        content="Original Text",
        x=100,
        y=100,
        width=200,
        height=50,
        font_size=12
    )
    page_model.add_element(element)
    
    # Verify initial state
    assert element.content == "Original Text"
    assert element.font_size == 12
    
    # Modify properties
    element.content = "Modified Text"
    element.font_size = 24
    
    # Verify changes are reflected
    assert element.content == "Modified Text"
    assert element.font_size == 24
    
    # Verify the element in the page model is the same object
    assert page_model.elements[0] is element
    assert page_model.elements[0].content == "Modified Text"
    assert page_model.elements[0].font_size == 24


def test_model_to_memory_element_conversion():
    """Test conversion between model elements and memory elements"""
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
    
    # Verify conversion
    assert memory_element['text'] == model_element.content
    assert memory_element['font_size'] == model_element.font_size
    
    # Modify memory element
    memory_element['text'] = "Modified Content"
    memory_element['font_size'] = 24
    
    # Update model element from memory element (simulating _sync_to_model)
    model_element.content = memory_element['text']
    model_element.font_size = memory_element['font_size']
    
    # Verify model is updated
    assert model_element.content == "Modified Content"
    assert model_element.font_size == 24


if __name__ == "__main__":
    # Run tests
    test_model_property_sync()
    test_model_to_memory_element_conversion()
    print("All tests passed!")
