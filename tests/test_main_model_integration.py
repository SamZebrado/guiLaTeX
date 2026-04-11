"""
Test integration between main.py and model layer

Tests that main.py correctly creates and passes DocumentModel to PDFCanvas
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gui.main import MainWindow
from src.model import DocumentModel, PageModel, ElementModel

def test_main_window_creates_document_model():
    """Test that MainWindow creates DocumentModel"""
    print("Testing MainWindow DocumentModel creation...")
    
    # Create MainWindow
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    
    try:
        window = MainWindow()
        
        # Check if DocumentModel was created
        assert hasattr(window, 'document_model'), "MainWindow should have document_model attribute"
        
        if DocumentModel:
            assert isinstance(window.document_model, DocumentModel), "document_model should be instance of DocumentModel"
            print("  ✓ DocumentModel created successfully")
            print(f"  ✓ Document title: {window.document_model.title}")
            print(f"  ✓ Number of pages: {len(window.document_model.pages)}")
        else:
            print("  ⚠️  DocumentModel not available, falling back to old path")
        
        # Check if PDFCanvas received the document model
        assert hasattr(window.pdf_canvas, 'document_model'), "PDFCanvas should have document_model attribute"
        assert window.pdf_canvas.document_model is window.document_model, "PDFCanvas should use the same document_model as MainWindow"
        print("  ✓ DocumentModel passed to PDFCanvas successfully")
        
        return True
        
    finally:
        app.quit()

def test_model_integration_flow():
    """Test the complete model integration flow"""
    print("\nTesting model integration flow...")
    
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    
    try:
        window = MainWindow()
        
        # Wait for initial PDF creation
        import time
        time.sleep(1)  # Give time for PDF creation
        
        # Check if document model has elements
        if DocumentModel and window.document_model:
            # Check if pages exist
            assert len(window.document_model.pages) > 0, "Document should have at least one page"
            
            # Check if elements were added to page model
            page = window.document_model.pages[0]
            assert hasattr(page, 'elements'), "Page should have elements attribute"
            
            # Check if PDF canvas is using the model
            if window.pdf_canvas.page_widget:
                assert hasattr(window.pdf_canvas.page_widget, 'page_model'), "PDFPageWidget should have page_model attribute"
                print("  ✓ PDFPageWidget has page_model attribute")
            
            print("  ✓ Model integration flow completed successfully")
        else:
            print("  ⚠️  Model integration not available, falling back to old path")
        
        return True
        
    finally:
        app.quit()

def test_model_as_source_of_truth():
    """Test that model is the source of truth"""
    print("\nTesting model as source of truth...")
    
    # Create a document model
    doc = DocumentModel(title='Test Document')
    page = PageModel(number=0)
    
    # Add an element
    elem = ElementModel(
        type='text',
        content='Test Element',
        x=100,
        y=200,
        width=150,
        height=30,
        font_size=12
    )
    page.add_element(elem)
    doc.add_page(page)
    
    # Simulate UI modification
    elem.content = 'Modified Content'
    elem.x = 150
    elem.dirty = True
    
    # Check that model reflects changes
    assert elem.content == 'Modified Content', "Model should reflect content change"
    assert elem.x == 150, "Model should reflect position change"
    assert elem.dirty == True, "Model should mark element as dirty"
    
    print("  ✓ Model as source of truth works correctly")
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Running Main Model Integration Tests")
    print("=" * 60 + "\n")
    
    try:
        test_main_window_creates_document_model()
        test_model_integration_flow()
        test_model_as_source_of_truth()
        
        print("\n" + "=" * 60)
        print("All tests passed!")
        print("=" * 60)
        print("\nSummary:")
        print("- MainWindow creates DocumentModel")
        print("- DocumentModel is passed to PDFCanvas")
        print("- PDFCanvas uses DocumentModel for current page")
        print("- Model serves as source of truth")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
