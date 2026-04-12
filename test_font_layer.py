#!/usr/bin/env python3
"""
Test script for font settings and layer functionality
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from PyQt6.QtWidgets import QApplication
from gui.pdf_canvas import PDFPageWidget
import fitz  # PyMuPDF

# Create QApplication instance
app = QApplication(sys.argv)

# Create a simple PDF for testing
def create_test_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), 'temp', 'test_font_layer.pdf')
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    # Create a new PDF
    doc = fitz.open()
    page = doc.new_page()
    
    # Add some text
    page.insert_text((100, 100), "Test Document", fontsize=12)
    page.insert_text((100, 120), "Hello World", fontsize=10)
    
    # Save the PDF
    doc.save(pdf_path)
    doc.close()
    
    return pdf_path

# Test font settings
def test_font_settings():
    print("=== Test: Font Settings ===")
    
    # Create test PDF
    pdf_path = create_test_pdf()
    
    # Open PDF
    doc = fitz.open(pdf_path)
    
    # Create PDFPageWidget
    page_widget = PDFPageWidget(doc, 0)
    
    # Add a test element with font family
    test_element = {
        'id': 'test_element',
        'type': 'text',
        'text': '测试字体设置',
        'x': 100,
        'y': 150,
        'width': 200,
        'height': 40,
        'font_size': 16,
        'font_family': 'Noto Sans SC',
        'original_width': 200,
        'original_height': 40
    }
    page_widget.memory_elements.append(test_element)
    
    # Test font family property
    print(f"Test element font family: {test_element.get('font_family')}")
    print("Font settings test completed")
    print()

# Test layer functionality
def test_layer_functionality():
    print("=== Test: Layer Functionality ===")
    
    # Create test PDF
    pdf_path = create_test_pdf()
    
    # Open PDF
    doc = fitz.open(pdf_path)
    
    # Create PDFPageWidget
    page_widget = PDFPageWidget(doc, 0)
    
    # Test initial layers
    print(f"Initial layers: {[layer['name'] for layer in page_widget.get_layers()]}")
    print(f"Current layer: {page_widget.get_current_layer_id()}")
    
    # Add a new layer
    new_layer_id = page_widget.add_layer("测试图层")
    print(f"New layer ID: {new_layer_id}")
    
    # Test layer visibility
    print(f"Layers after adding new layer: {[layer['name'] for layer in page_widget.get_layers()]}")
    
    # Test toggling layer visibility
    page_widget.toggle_layer_visibility(new_layer_id)
    
    # Test moving element to new layer
    if page_widget.memory_elements:
        element_id = page_widget.memory_elements[0]['id']
        page_widget.move_element_to_layer(element_id, new_layer_id)
        print(f"Moved element {element_id} to layer {new_layer_id}")
    
    # Test deleting layer
    # We can't delete the default layer, but we can try to delete the new one
    # First, move elements back to default layer
    for elem in page_widget.memory_elements:
        page_widget.move_element_to_layer(elem['id'], 'layer_1')
    
    # Now delete the new layer
    page_widget.delete_layer(new_layer_id)
    print(f"Layers after deleting test layer: {[layer['name'] for layer in page_widget.get_layers()]}")
    
    print("Layer functionality test completed")
    print()

if __name__ == "__main__":
    print("Testing font settings and layer functionality")
    print("=" * 50)
    test_font_settings()
    test_layer_functionality()
    print("All tests completed")
