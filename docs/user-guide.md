# guiLaTeX User Guide

## Introduction

guiLaTeX is a visual LaTeX editor that allows you to create LaTeX documents using a drag-and-drop interface, similar to Photoshop or Word. This guide will help you get started with guiLaTeX and make the most of its features.

## Installation

### Prerequisites
- Python 3.8 or higher
- PyQt6
- LaTeX distribution (TeX Live, MiKTeX, etc.)

### Installation Steps
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd guiLaTeX
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python src/gui/main.py
   ```

## User Interface Overview

The guiLaTeX interface consists of three main components:

1. **Canvas** (left): The main editing area where you create and manipulate LaTeX elements
2. **Property Panel** (right): Displays and allows editing of properties for selected elements
3. **PDF Preview** (bottom): Shows real-time preview of the generated PDF

## Basic Usage

### Adding Elements

1. **Text Elements**:
   - TODO: Add text element functionality

2. **Math Elements**:
   - TODO: Add math element functionality

3. **Other Elements**:
   - TODO: Add other element types

### Selecting Elements

- **Click** on an element to select it
- **Ctrl+Click** to select multiple elements
- **Ctrl+A** to select all elements
- **Click outside** any element to deselect all

### Manipulating Elements

- **Drag** elements to move them around the canvas
- **Resize** elements using resize handles (TODO: Implement resize functionality)
- **Rotate** elements (TODO: Implement rotate functionality)

### Editing Properties

When an element is selected, its properties are displayed in the Property Panel. You can edit:

- **Font**: Family, size, and color
- **Text**: Content and formatting
- **Position**: X and Y coordinates

### Exporting and Previewing

- **F5** or **File → Preview PDF**: Generate and view PDF
- **Ctrl+E** or **File → Export**: Export LaTeX code

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New document |
| Ctrl+O | Open document |
| Ctrl+S | Save document |
| Ctrl+E | Export document |
| F5 | Preview PDF |
| Ctrl+Q | Exit application |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+X | Cut |
| Ctrl+C | Copy |
| Ctrl+V | Paste |
| Ctrl+A | Select all |
| Ctrl++ | Zoom in |
| Ctrl+- | Zoom out |

## Advanced Features

### LaTeX Integration

guiLaTeX automatically generates LaTeX code from your visual elements. You can:

- View the generated LaTeX code
- Export the code to a .tex file
- Compile to PDF with a single click

### Math Formula Editing

TODO: Add math formula editing instructions

### Tables and Figures

TODO: Add tables and figures instructions

## Troubleshooting

### Common Issues

1. **LaTeX engine not found**:
   - Ensure you have a LaTeX distribution installed
   - Check that LaTeX commands are in your system PATH

2. **PDF preview not working**:
   - Check that LaTeX compilation is successful
   - Ensure you have Poppler installed for PDF rendering

3. **Elements not displaying correctly**:
   - Check that PyQt6 is properly installed
   - Restart the application

## FAQ

**Q: Can I import existing LaTeX documents?**
A: TODO: Implement import functionality

**Q: Is guiLaTeX cross-platform?**
A: Yes, guiLaTeX works on Windows, macOS, and Linux.

**Q: How do I add custom LaTeX packages?**
A: TODO: Implement package management

**Q: Can I collaborate with others on a document?**
A: TODO: Implement collaboration features

## Support

If you encounter any issues or have questions:

1. Check this user guide
2. Refer to the project documentation
3. TODO: Add support contact information

## Contributing

guiLaTeX is an open-source project. Contributions are welcome!

- TODO: Add contribution guidelines

## License

TODO: Add license information

---

**Note**: guiLaTeX is currently in development. Features and functionality may change.
