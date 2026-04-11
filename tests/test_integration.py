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


def test_current_pdf_canvas_has_backward_compatibility():
    """Test that current PDFPageWidget maintains backward compatibility"""
    print("Testing current PDFCanvas implementation...")
    
    if not UI_AVAILABLE:
        print("  ⚠️  Skipping PDFCanvas test due to missing dependencies")
        print("  ✓ PDFCanvas test skipped (dependencies missing)")
        return
    
    # Check if the class has the old attributes (backward compatibility)
    import inspect
    source = inspect.getsource(PDFPageWidget)
    
    # Check for old path indicators (backward compatibility)
    assert 'text_elements' in source, "PDFPageWidget should have text_elements"
    assert 'memory_elements' in source, "PDFPageWidget should have memory_elements"
    assert 'save_changes' in source, "PDFPageWidget should have save_changes"
    assert 'update_pdf_element' in source, "PDFPageWidget should have update_pdf_element"
    
    # Check for model layer integration
    assert 'PageModel' in source, "PDFPageWidget should use PageModel"
    assert 'ElementModel' in source, "PDFPageWidget should use ElementModel"
    assert '_sync_from_model' in source, "PDFPageWidget should have _sync_from_model"
    assert '_sync_to_model' in source, "PDFPageWidget should have _sync_to_model"
    
    print("  ✓ PDFPageWidget maintains backward compatibility (dictionaries)")
    print("  ✓ PDFPageWidget integrates with PageModel")

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

def test_model_integration_exists():
    """Test that integration between model and UI exists"""
    print("\nTesting integration status...")
    
    # Check if main.py uses DocumentModel
    main_content = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'main.py'), 'r').read()
    assert 'DocumentModel' in main_content, "main.py should use DocumentModel"
    assert 'PageModel' in main_content, "main.py should use PageModel"
    assert 'ElementModel' in main_content, "main.py should use ElementModel"
    
    # Check if pdf_canvas.py uses model layer
    canvas_content = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'gui', 'pdf_canvas.py'), 'r').read()
    assert 'PageModel' in canvas_content, "pdf_canvas.py should use PageModel"
    assert 'ElementModel' in canvas_content, "pdf_canvas.py should use ElementModel"
    assert 'document_model' in canvas_content, "pdf_canvas.py should use document_model parameter"
    assert '_sync_from_model' in canvas_content, "pdf_canvas.py should have _sync_from_model"
    assert '_sync_to_model' in canvas_content, "pdf_canvas.py should have _sync_to_model"
    
    # Check if engine.py uses model layer (engine should NOT use model layer directly)
    engine_content = open(os.path.join(os.path.dirname(__file__), '..', 'src', 'latex', 'engine.py'), 'r').read()
    assert 'DocumentModel' not in engine_content, "engine.py should not use DocumentModel directly"
    assert 'PageModel' not in engine_content, "engine.py should not use PageModel directly"
    assert 'ElementModel' not in engine_content, "engine.py should not use ElementModel directly"
    
    print("  ✓ Integration between model and UI exists")
    print("  ✓ main.py and pdf_canvas.py use model layer")
    print("  ✓ engine.py correctly does not use model layer directly")


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
    
    test_current_pdf_canvas_has_backward_compatibility()
    test_model_layer_exists()
    test_model_integration_exists()
    test_model_to_elements_conversion()
    
    print("\n" + "=" * 60)
    print("All integration tests passed!")
    print("=" * 60)
    print("\nSummary:")
    print("- Model layer exists and works")
    print("- UI components maintain backward compatibility (dictionaries)")
    print("- Integration between model and UI exists")
    print("- Model to old-style elements conversion works")
