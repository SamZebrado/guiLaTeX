#!/usr/bin/env python3
"""
Copy/paste functionality test
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

def test_copy_paste():
    """Test copy/paste functionality"""
    print("=== Test: Copy/Paste Functionality ===")
    
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
    
    # Check initial state
    initial_count = len(page_widget.memory_elements)
    print(f"Initial elements count: {initial_count}")
    
    # Select an element
    if page_widget.memory_elements:
        page_widget.selected_element = page_widget.memory_elements[0]
        print(f"Selected element: {page_widget.selected_element['text']}")
        
        # Copy the element
        copied_element = page_widget.copy_element()
        print(f"Copied element: {copied_element['text'] if copied_element else 'None'}")
        
        # Paste the element
        paste_result = page_widget.paste_element(copied_element)
        print(f"Paste result: {paste_result}")
        
        # Check after paste
        after_paste_count = len(page_widget.memory_elements)
        print(f"After paste elements count: {after_paste_count}")
        
        # Check if we have a new element
        if after_paste_count > initial_count:
            print("✓ Paste successful - new element added")
        else:
            print("✗ Paste failed - no new element added")
        
        # Check for duplicates
        unique_ids = set()
        duplicate_found = False
        for elem in page_widget.memory_elements:
            if elem['id'] in unique_ids:
                duplicate_found = True
                print(f"Duplicate ID found: {elem['id']}")
            unique_ids.add(elem['id'])
        
        print(f"Unique IDs count: {len(unique_ids)}")
        print(f"Duplicate found: {duplicate_found}")
        
        if not duplicate_found:
            print("✓ No duplicates after paste")
        else:
            print("✗ Duplicates found after paste")
    else:
        print("No elements to copy")
    
    # Clean up
    doc.close()
    os.unlink(pdf_path)
    
    return True

if __name__ == "__main__":
    print("Copy/Paste Functionality Test")
    print("=" * 50)
    
    test_copy_paste()
    
    print("\n" + "=" * 50)
    print("Test completed!")
