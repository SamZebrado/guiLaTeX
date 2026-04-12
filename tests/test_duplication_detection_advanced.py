#!/usr/bin/env python3
"""
Advanced duplication detection test
"""

import sys
import os
import tempfile

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from PyQt6.QtWidgets import QApplication
import fitz  # PyMuPDF

# Create QApplication instance
app = QApplication(sys.argv)

from gui.pdf_canvas import PDFPageWidget
from model import DocumentModel, PageModel, ElementModel

def create_test_pdf():
    """Create a simple PDF for testing"""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        pdf_path = f.name
    
    # Create a new PDF
    doc = fitz.open()
    page = doc.new_page()
    
    # Add some text
    page.insert_text((100, 100), "Test Document", fontsize=12)
    
    # Save the PDF
    doc.save(pdf_path)
    doc.close()
    
    return pdf_path

def test_demo_scene_duplication():
    """Test that demo scene has no duplicates"""
    print("=== Test: Demo Scene Duplication ===")
    
    # Create test PDF
    pdf_path = create_test_pdf()
    
    # Open PDF
    doc = fitz.open(pdf_path)
    
    # Create document model
    doc_model = DocumentModel(title="Test Document")
    page_model = PageModel(number=0)
    doc_model.add_page(page_model)
    
    # Create PDFPageWidget with document model
    page_widget = PDFPageWidget(doc, 0, page_model=page_model)
    
    # Check memory elements
    memory_elements = page_widget.memory_elements
    print(f"Memory elements count: {len(memory_elements)}")
    
    # Check for duplicate IDs
    unique_ids = set()
    duplicate_found = False
    for elem in memory_elements:
        if elem['id'] in unique_ids:
            duplicate_found = True
            print(f"Duplicate ID found: {elem['id']}")
        unique_ids.add(elem['id'])
    
    print(f"Unique IDs count: {len(unique_ids)}")
    print(f"Duplicate found: {duplicate_found}")
    
    # Check if we have the expected demo elements
    expected_ids = {'demo_title', 'demo_author', 'demo_body', 'demo_formula', 'demo_image'}
    actual_ids = set(elem['id'] for elem in memory_elements)
    
    print(f"Expected IDs: {expected_ids}")
    print(f"Actual IDs: {actual_ids}")
    print(f"All expected IDs present: {expected_ids.issubset(actual_ids)}")
    
    # Test dragging simulation
    print("\n=== Test: Drag Simulation ===")
    if memory_elements:
        # Select first element
        page_widget.selected_element = memory_elements[0]
        
        # Simulate drag start
        page_widget.is_dragging_element = True
        page_widget.drag_start_pos = None
        page_widget.element_start_pos = (memory_elements[0]['x'], memory_elements[0]['y'])
        
        # Simulate drag end
        page_widget.mouseReleaseEvent(None)
        
        # Check after drag
        print(f"After drag - memory elements count: {len(page_widget.memory_elements)}")
        
        # Check for duplicates again
        unique_ids_after = set()
        duplicate_found_after = False
        for elem in page_widget.memory_elements:
            if elem['id'] in unique_ids_after:
                duplicate_found_after = True
                print(f"Duplicate ID found after drag: {elem['id']}")
            unique_ids_after.add(elem['id'])
        
        print(f"After drag - unique IDs count: {len(unique_ids_after)}")
        print(f"After drag - duplicate found: {duplicate_found_after}")
    
    # Clean up
    doc.close()
    os.unlink(pdf_path)
    
    return not duplicate_found

def test_model_sync_duplication():
    """Test that model sync doesn't create duplicates"""
    print("\n=== Test: Model Sync Duplication ===")
    
    # Create test PDF
    pdf_path = create_test_pdf()
    
    # Open PDF
    doc = fitz.open(pdf_path)
    
    # Create document model
    doc_model = DocumentModel(title="Test Document")
    page_model = PageModel(number=0)
    doc_model.add_page(page_model)
    
    # Create PDFPageWidget with document model
    page_widget = PDFPageWidget(doc, 0, page_model=page_model)
    
    # Check initial model state
    print(f"Initial model elements count: {len(page_model.elements)}")
    
    # Sync to model
    page_widget._sync_to_model()
    print(f"After sync to model - model elements count: {len(page_model.elements)}")
    
    # Sync from model
    page_widget._sync_from_model()
    print(f"After sync from model - memory elements count: {len(page_widget.memory_elements)}")
    
    # Check for duplicates
    unique_ids = set()
    duplicate_found = False
    for elem in page_widget.memory_elements:
        if elem['id'] in unique_ids:
            duplicate_found = True
            print(f"Duplicate ID found after sync: {elem['id']}")
        unique_ids.add(elem['id'])
    
    print(f"Unique IDs count: {len(unique_ids)}")
    print(f"Duplicate found: {duplicate_found}")
    
    # Clean up
    doc.close()
    os.unlink(pdf_path)
    
    return not duplicate_found

if __name__ == "__main__":
    print("Advanced Duplication Detection Test")
    print("=" * 50)
    
    demo_scene_pass = test_demo_scene_duplication()
    model_sync_pass = test_model_sync_duplication()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Demo scene duplication test: {'PASS' if demo_scene_pass else 'FAIL'}")
    print(f"Model sync duplication test: {'PASS' if model_sync_pass else 'FAIL'}")
    
    if demo_scene_pass and model_sync_pass:
        print("\nAll duplication tests passed!")
        sys.exit(0)
    else:
        print("\nSome duplication tests failed!")
        sys.exit(1)
