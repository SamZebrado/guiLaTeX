# guiLaTeX API Documentation

## Overview

This document provides technical documentation for the guiLaTeX project, including its architecture, core components, and API.

## Project Structure

```
guiLaTeX/
├── src/                  # Source code
│   ├── gui/              # GUI components
│   │   ├── main.py       # Main application
│   │   ├── canvas.py     # Canvas component
│   │   ├── properties.py # Property panel
│   │   └── preview.py    # PDF preview
│   ├── latex/            # LaTeX integration
│   │   └── engine.py     # LaTeX engine
│   └── utils/            # Utility functions
├── tests/                # Test files
├── docs/                 # Documentation
├── venv/                 # Virtual environment
├── .git/                 # Git repository
├── STATUS.md             # Project status
├── PROJECT_LOG.md        # Development log
├── PLAN.md               # Development plan
├── README.md             # Project overview
└── requirements.txt      # Dependencies
```

## Core Components

### 1. Main Application (main.py)

**Purpose**: Entry point for the guiLaTeX application

**Key Classes**:
- `MainWindow`: Main application window
  - **Methods**:
    - `__init__()`: Initialize the application
    - `create_menu_bar()`: Create menu bar
    - `export_document()`: Export document to LaTeX
    - `preview_document()`: Preview document as PDF
    - `on_selection_changed()`: Handle canvas selection changes
    - `on_scene_changed()`: Handle canvas scene changes

**Usage**:
```python
from gui.main import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
```

### 2. Canvas Component (canvas.py)

**Purpose**: Visual canvas for LaTeX element rendering and manipulation

**Key Classes**:
- `LaTeXElement`: Base class for all LaTeX elements
  - **Properties**:
    - `text`: Text content
    - `font`: Font properties
    - `color`: Text color
    - `width`, `height`: Element dimensions
  - **Methods**:
    - `boundingRect()`: Return bounding rectangle
    - `paint()`: Paint the element

- `TextElement`: Text element
- `MathElement`: Math formula element

- `Canvas`: Main canvas widget
  - **Methods**:
    - `draw_grid()`: Draw grid background
    - `add_sample_elements()`: Add sample elements
    - `update_selected_items()`: Update selected items list
    - `deselect_all()`: Deselect all items
    - `select_all()`: Select all items
    - `delete_selected_items()`: Delete selected items

**Usage**:
```python
from gui.canvas import Canvas, TextElement

canvas = Canvas()
text_element = TextElement(100, 100, 200, 60)
text_element.text = "Hello World"
canvas.scene.addItem(text_element)
```

### 3. Property Panel (properties.py)

**Purpose**: Panel for editing element properties

**Key Classes**:
- `PropertyPanel`: Property panel widget
  - **Methods**:
    - `set_element()`: Set current element to edit
    - `update_properties()`: Update property fields
    - `on_font_family_changed()`: Handle font family change
    - `on_font_size_changed()`: Handle font size change
    - `on_color_clicked()`: Handle color button click
    - `on_text_changed()`: Handle text content change
    - `on_position_changed()`: Handle position change

**Usage**:
```python
from gui.properties import PropertyPanel

property_panel = PropertyPanel()
property_panel.set_element(selected_element)
```

### 4. PDF Preview (preview.py)

**Purpose**: Real-time PDF preview functionality

**Key Classes**:
- `PDFPreviewThread`: Thread for PDF compilation and rendering
  - **Signals**:
    - `preview_ready`: Emitted when preview is ready
    - `error_occurred`: Emitted when error occurs
  - **Methods**:
    - `run()`: Run PDF compilation and rendering
    - `render_pdf()`: Render PDF to pixmap

- `PDFPreview`: PDF preview widget
  - **Methods**:
    - `set_latex_engines()`: Set LaTeX engines
    - `set_elements()`: Set elements to preview
    - `refresh_preview()`: Refresh PDF preview

**Usage**:
```python
from gui.preview import PDFPreview

pdf_preview = PDFPreview()
pdf_preview.set_latex_engines(latex_engine, latex_generator)
pdf_preview.set_elements(elements)
pdf_preview.refresh_preview()
```

### 5. LaTeX Engine (engine.py)

**Purpose**: Integration with LaTeX engine for compilation and preview

**Key Classes**:
- `LaTeXEngine`: LaTeX engine integration
  - **Methods**:
    - `is_available()`: Check if LaTeX is available
    - `compile()`: Compile LaTeX code to PDF
    - `generate_basic_latex()`: Generate basic LaTeX code
    - `view_pdf()`: View PDF file

- `LaTeXGenerator`: Generate LaTeX code from visual elements
  - **Methods**:
    - `generate()`: Generate LaTeX code from elements

- `LaTeXParser`: Parse LaTeX code to visual elements (TODO: Implement)
  - **Methods**:
    - `parse()`: Parse LaTeX code to elements

**Usage**:
```python
from latex.engine import LaTeXEngine, LaTeXGenerator

engine = LaTeXEngine()
generator = LaTeXGenerator()

# Generate LaTeX code
latex_code = generator.generate(elements)

# Compile to PDF
success, pdf_path, log = engine.compile(latex_code)

if success:
    engine.view_pdf(pdf_path)
```

## Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| PyQt6 | 6.11.0 | GUI framework |
| pytest | 9.0.2 | Testing framework |
| pytest-qt | 4.5.0 | Qt testing support |
| poppler-qt6 | Optional | PDF rendering |

## Testing

### Running Tests

```bash
cd guiLaTeX
source venv/bin/activate
python -m pytest tests/ -v
```

### Test Coverage

- `test_latex_engine.py`: Tests for LaTeX engine functionality
- `test_canvas.py`: Tests for Canvas component functionality

## Development Workflow

1. **Setup**: Install dependencies and create virtual environment
2. **Development**: Implement features and fix bugs
3. **Testing**: Run tests to ensure functionality
4. **Documentation**: Update documentation
5. **Backup**: Backup project to Google Drive
6. **Commit**: Commit changes to Git

## API Versioning

TODO: Implement API versioning

## Future Enhancements

1. **Import/Export**:
   - Import existing LaTeX documents
   - Export to various formats

2. **Advanced Elements**:
   - Tables
   - Figures
   - References
   - Citations

3. **Collaboration**:
   - Real-time collaboration
   - Version control integration

4. **Extensions**:
   - Plugin system
   - Custom templates

5. **Performance**:
   - Optimized rendering
   - Caching

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'gui'**
   - Ensure src directory is in Python path
   - Run from project root directory

2. **LaTeX compilation failed**
   - Check LaTeX installation
   - Verify LaTeX code syntax

3. **PDF preview not rendering**
   - Install Poppler for better PDF rendering
   - Check LaTeX compilation output

## Support

For technical support or questions:

- TODO: Add support contact information

---

**Note**: This API documentation is subject to change as the project evolves.
