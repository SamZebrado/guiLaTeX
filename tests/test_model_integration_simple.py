"""
Simple test for model integration in main.py

Tests the model integration logic without requiring Qt dependencies
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model import DocumentModel, PageModel, ElementModel

def test_model_creation():
    """Test that DocumentModel can be created"""
    print("Testing DocumentModel creation...")
    
    # Create document model
    doc = DocumentModel(title='Test Document')
    assert doc.title == 'Test Document'
    assert len(doc.pages) >= 1  # Should have at least one page
    print("  ✓ DocumentModel created successfully")
    print(f"  ✓ Document title: {doc.title}")
    print(f"  ✓ Number of pages: {len(doc.pages)}")
    
    return True

def test_page_model():
    """Test PageModel functionality"""
    print("\nTesting PageModel functionality...")
    
    # Create page model
    page = PageModel(number=0)
    
    # Add element
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
    
    assert len(page.elements) == 1
    assert page.elements[0].content == 'Test Element'
    assert page.elements[0].id == elem.id
    print("  ✓ PageModel with elements created successfully")
    
    return True

def test_model_integration_logic():
    """Test the integration logic that would be in main.py"""
    print("\nTesting model integration logic...")
    
    # Simulate what main.py would do
    
    # 1. Create document model
    doc = DocumentModel(title='guiLaTeX Document')
    
    # 2. Create a page model
    page = PageModel(number=0)
    doc.add_page(page)
    
    # 3. Simulate elements from PDF canvas
    mock_memory_elements = [
        {
            'id': 'text_0',
            'type': 'text',
            'text': 'Hello World!',
            'x': 100,
            'y': 200,
            'width': 150,
            'height': 30,
            'font_size': 12
        },
        {
            'id': 'text_1', 
            'type': 'text',
            'text': 'This is a test',
            'x': 100,
            'y': 250,
            'width': 200,
            'height': 25,
            'font_size': 10
        }
    ]
    
    # 4. Add elements to page model (like main.py would do)
    for elem in mock_memory_elements:
        new_elem = ElementModel(
            id=elem['id'],
            type=elem.get('type', 'text'),
            content=elem['text'],
            x=elem['x'],
            y=elem['y'],
            width=elem['width'],
            height=elem['height'],
            font_size=elem.get('font_size', 12)
        )
        page.add_element(new_elem)
    
    assert len(page.elements) == 2
    assert page.elements[0].content == 'Hello World!'
    assert page.elements[1].content == 'This is a test'
    print(f"  ✓ Added {len(mock_memory_elements)} elements to page model")
    
    # 5. Test model as source of truth
    page.elements[0].content = 'Modified Text'
    page.elements[0].x = 150
    page.elements[0].dirty = True
    
    assert page.elements[0].content == 'Modified Text'
    assert page.elements[0].x == 150
    assert page.elements[0].dirty == True
    assert page.dirty == True
    print("  ✓ Model as source of truth works correctly")
    
    return True

def test_model_passing():
    """Test that model can be passed between components"""
    print("\nTesting model passing...")
    
    # Create document model
    doc = DocumentModel(title='Test Document')
    
    # Simulate passing to PDFCanvas
    class MockPDFCanvas:
        def __init__(self, document_model=None):
            self.document_model = document_model
    
    # Create PDFCanvas with document model
    canvas = MockPDFCanvas(document_model=doc)
    
    assert canvas.document_model is doc
    assert canvas.document_model.title == 'Test Document'
    print("  ✓ DocumentModel passed to PDFCanvas successfully")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("Running Simple Model Integration Tests")
    print("=" * 60 + "\n")
    
    try:
        test_model_creation()
        test_page_model()
        test_model_integration_logic()
        test_model_passing()
        
        print("\n" + "=" * 60)
        print("All tests passed!")
        print("=" * 60)
        print("\nSummary:")
        print("- DocumentModel can be created")
        print("- PageModel can manage elements")
        print("- Elements can be added to page model")
        print("- Model serves as source of truth")
        print("- Model can be passed between components")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
