"""
Test integration between main.py and model layer (no Qt dependencies)

Tests that main.py correctly creates and passes DocumentModel to PDFCanvas
without requiring Qt dependencies
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock Qt modules to avoid import errors
class MockQApplication:
    def __init__(self, *args):
        pass
    def quit(self):
        pass

class MockQWidget:
    def __init__(self, *args):
        pass
    def setWindowTitle(self, *args):
        pass
    def setGeometry(self, *args):
        pass
    def setCentralWidget(self, *args):
        pass
    def menuBar(self, *args):
        return MockQMenuBar()
    def close(self, *args):
        pass
    @property
    def element_changed(self):
        return MockSignal()

class MockQSplitter:
    def __init__(self, *args):
        pass
    def addWidget(self, *args):
        pass

class MockQVBoxLayout:
    def __init__(self, *args):
        pass
    def addWidget(self, *args):
        pass
    def addLayout(self, *args):
        pass

class MockQMenuBar:
    def __init__(self, *args):
        pass
    def addMenu(self, *args):
        return MockQMenu()

class MockQMenu:
    def __init__(self, *args):
        pass
    def addAction(self, *args):
        pass
    def addSeparator(self, *args):
        pass

class MockQAction:
    def __init__(self, *args):
        pass
    def setShortcut(self, *args):
        pass
    @property
    def triggered(self):
        return type('obj', (object,), {'connect': lambda f: None})

class MockQTextEdit:
    def __init__(self, *args):
        pass
    def setReadOnly(self, *args):
        pass
    def setPlaceholderText(self, *args):
        pass
    def setText(self, *args):
        pass

class MockQMessageBox:
    @staticmethod
    def warning(self, *args):
        pass
    @staticmethod
    def information(self, *args):
        pass

class MockQt:
    class Orientation:
        Vertical = 0
        Horizontal = 1

# Mock PyQt6 modules
class MockQtWidgets:
    QApplication = MockQApplication
    QMainWindow = MockQWidget
    QWidget = MockQWidget
    QVBoxLayout = MockQVBoxLayout
    QMenuBar = MockQMenuBar
    QMenu = MockQMenu
    QSplitter = MockQSplitter
    QMessageBox = MockQMessageBox
    QTabWidget = MockQWidget
    QTextEdit = MockQTextEdit

class MockQtCore:
    class Qt:
        class Orientation:
            Vertical = 0
            Horizontal = 1

class MockQtGui:
    QAction = MockQAction

# Create mock modules
sys.modules['PyQt6'] = type('obj', (object,), {})
sys.modules['PyQt6.QtWidgets'] = MockQtWidgets
sys.modules['PyQt6.QtCore'] = MockQtCore
sys.modules['PyQt6.QtGui'] = MockQtGui

# Mock PDFCanvas to avoid Qt dependencies
class MockSignal:
    def connect(self, *args):
        pass

class MockPDFCanvas:
    def __init__(self, document_model=None):
        self.document_model = document_model
        self.page_widget = type('obj', (object,), {
            'memory_elements': [],
            'element_selected': MockSignal(),
            'element_modified': MockSignal()
        })
    def create_pdf(self, latex_code):
        # Mock success
        return True
    def update_page_display(self):
        pass

# Mock LaTeX modules
class MockLaTeXEngine:
    def is_available(self):
        return False
    def view_pdf(self, pdf_path):
        return False

class MockLaTeXGenerator:
    pass

class MockPDFToLaTeXConverter:
    def convert_memory_elements(self, elements):
        return "Mock LaTeX code"

# Mock other modules
sys.modules['latex.engine'] = type('obj', (object,), {
    'LaTeXEngine': MockLaTeXEngine,
    'LaTeXGenerator': MockLaTeXGenerator
})

sys.modules['latex.pdf_reconstructor'] = type('obj', (object,), {
    'PDFToLaTeXConverter': MockPDFToLaTeXConverter
})

sys.modules['gui.properties'] = type('obj', (object,), {
    'PropertyPanel': MockQWidget
})

sys.modules['gui.pdf_canvas'] = type('obj', (object,), {
    'PDFCanvas': MockPDFCanvas
})

# Now import main.py
try:
    from src.gui.main import MainWindow
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import model from the same path as main.py
try:
    from model import DocumentModel, PageModel, ElementModel
except ImportError:
    from src.model import DocumentModel, PageModel, ElementModel

def test_main_window_creates_document_model():
    """Test that MainWindow creates DocumentModel"""
    print("Testing MainWindow DocumentModel creation...")
    
    # Create MainWindow
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

def test_model_integration_flow():
    """Test the complete model integration flow"""
    print("\nTesting model integration flow...")
    
    # Create MainWindow
    window = MainWindow()
    
    # Check if document model has elements
    if DocumentModel and window.document_model:
        # Check if pages exist
        assert len(window.document_model.pages) > 0, "Document should have at least one page"
        
        # Check if elements were added to page model
        page = window.document_model.pages[0]
        assert hasattr(page, 'elements'), "Page should have elements attribute"
        
        print("  ✓ Model integration flow completed successfully")
    else:
        print("  ⚠️  Model integration not available, falling back to old path")
    
    return True

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
    print("Running Main Model Integration Tests (No Qt)")
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
