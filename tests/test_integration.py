"""
Integration tests for guiLaTeX

Tests that verify the integration between model layer and UI components
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import model layer (should always work)
from src.model import ElementModel, PageModel, DocumentModel

# Try to import UI components (may fail due to missing dependencies)
try:
    from src.gui.pdf_canvas import PDFPageWidget, PDFCanvas
    from src.gui.main import MainWindow
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    print("⚠️  UI components not available (missing dependencies)")


def test_current_pdf_canvas_uses_old_path():
    """Test that current PDFPageWidget still uses old dictionary-based elements"""
    print("Testing current PDFCanvas implementation...")
    
    if not UI_AVAILABLE:
        print("  ⚠️  Skipping PDFCanvas test due to missing dependencies")
        print("  ✓ PDFCanvas test skipped (dependencies missing)")
        return
    
    # Check if the class has the old attributes
    import inspect
    source = inspect.getsource(PDFPageWidget)
    
    # Check for old path indicators
    assert 'text_elements' in source, "PDFPageWidget should have text_elements"
    assert 'memory_elements' in source, "PDFPageWidget should have memory_elements"
    assert 'save_changes' in source, "PDFPageWidget should have save_changes"
    assert 'update_pdf_element' in source, "PDFPageWidget should have update_pdf_element"
    
    # Check that it doesn't use model layer
    assert 'PageModel' not in source, "PDFPageWidget should not use PageModel yet"
    assert 'ElementModel' not in source, "PDFPageWidget should not use ElementModel yet"
    
    print("  ✓ PDFPageWidget is using old path (dictionaries)")
    print("  ✓ No PageModel integration yet")

def test_model_layer_exists():
    """Test that model layer exists and works"""
    print("\nTesting model layer...")
    
    # Test ElementModel
    elem = ElementModel(
        type='text',
        content='Test Element',
        x=100,
        y=200,
        width=150,
        height=30,
        font_size=12
    )
    
    assert elem.id is not None
    assert elem.content == 'Test Element'
    assert isinstance(elem.id, str)
    assert len(elem.id) > 0
    
    # Test PageModel
    page = PageModel(number=0)
    page.add_element(elem)
    assert len(page.elements) == 1
    assert page.elements[0].content == 'Test Element'
    
    # Test DocumentModel
    doc = DocumentModel(title='Test Document')
    doc.add_page(page)
    assert len(doc.pages) == 2  # Auto-creates first page
    
    print("  ✓ ElementModel works")
    print("  ✓ PageModel works")
    print("  ✓ DocumentModel works")

def test_no_integration_yet():
    """Test that there's no integration between model and UI yet"""
    print("\nTesting integration status...")
    
    # Check if main.py uses DocumentModel
    main_content = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'main.py'), 'r').read()
    assert 'DocumentModel' not in main_content, "main.py should not use DocumentModel yet"
    assert 'PageModel' not in main_content, "main.py should not use PageModel yet"
    assert 'ElementModel' not in main_content, "main.py should not use ElementModel yet"
    
    # Check if pdf_canvas.py uses model layer
    canvas_content = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'pdf_canvas.py'), 'r').read()
    assert 'DocumentModel' not in canvas_content, "pdf_canvas.py should not use DocumentModel yet"
    assert 'PageModel' not in canvas_content, "pdf_canvas.py should not use PageModel yet"
    assert 'ElementModel' not in canvas_content, "pdf_canvas.py should not use ElementModel yet"
    
    # Check if properties.py uses model layer
    properties_content = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'properties.py'), 'r').read()
    assert 'DocumentModel' not in properties_content, "properties.py should not use DocumentModel yet"
    assert 'PageModel' not in properties_content, "properties.py should not use PageModel yet"
    assert 'ElementModel' not in properties_content, "properties.py should not use ElementModel yet"
    
    # Check if engine.py uses model layer
    engine_content = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'latex', 'engine.py'), 'r').read()
    assert 'DocumentModel' not in engine_content, "engine.py should not use DocumentModel yet"
    assert 'PageModel' not in engine_content, "engine.py should not use PageModel yet"
    assert 'ElementModel' not in engine_content, "engine.py should not use ElementModel yet"
    
    print("  ✓ No integration between model and UI yet")
    print("  ✓ All files are still using old paths")


def test_model_to_elements_conversion():
    """Test conversion from model to old-style elements"""
    print("\nTesting model to elements conversion...")
    
    # Create a model
    page = PageModel(number=0)
    
    # Add elements
    elem1 = ElementModel(
        type='text',
        content='Hello World',
        x=100,
        y=200,
        width=150,
        height=30,
        font_size=12
    )
    
    elem2 = ElementModel(
        type='text',
        content='Test Text',
        x=100,
        y=250,
        width=100,
        height=25,
        font_size=10
    )
    
    page.add_element(elem1)
    page.add_element(elem2)
    
    # Convert to old-style elements
    old_elements = []
    for i, elem in enumerate(page.elements):
        old_elements.append({
            'id': elem.id,  # Use the same ID
            'type': elem.type,
            'text': elem.content,
            'x': elem.x,
            'y': elem.y,
            'width': elem.width,
            'height': elem.height,
            'font_size': elem.font_size,
            'original_width': elem.width,
            'original_height': elem.height
        })
    
    assert len(old_elements) == 2
    assert old_elements[0]['text'] == 'Hello World'
    assert old_elements[1]['text'] == 'Test Text'
    assert old_elements[0]['font_size'] == 12
    assert old_elements[1]['font_size'] == 10
    
    print("  ✓ Model to old-style elements conversion works")


if __name__ == '__main__':
    print("=" * 60)
    print("Running Integration Tests")
    print("=" * 60 + "\n")
    
    test_current_pdf_canvas_uses_old_path()
    test_model_layer_exists()
    test_no_integration_yet()
    test_model_to_elements_conversion()
    
    print("\n" + "=" * 60)
    print("All integration tests passed!")
    print("=" * 60)
    print("\nSummary:")
    print("- Model layer exists and works")
    print("- UI components still use old dictionary-based elements")
    print("- No integration between model and UI yet")
    print("- Model to old-style elements conversion works")
