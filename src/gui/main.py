#!/usr/bin/env python3
"""
guiLaTeX - Visual LaTeX Editor

Main application entry point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMenuBar, QMenu, QSplitter, QMessageBox, QTabWidget
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules
from latex.engine import LaTeXEngine, LaTeXGenerator
from latex.pdf_reconstructor import PDFToLaTeXConverter
from gui.properties import PropertyPanel
from gui.pdf_canvas import PDFCanvas

# Import model layer
try:
    from model import DocumentModel, PageModel, ElementModel
except ImportError:
    # Fallback: model layer not available
    DocumentModel = None
    PageModel = None
    ElementModel = None


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.setWindowTitle("guiLaTeX - Visual LaTeX Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main splitter (vertical)
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(main_splitter)
        
        # Create top splitter (horizontal) for PDF canvas and properties
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.addWidget(top_splitter)
        
        # Create document model (source of truth)
        self.document_model = None
        if DocumentModel:
            self.document_model = DocumentModel(title='guiLaTeX Document')
            print("DocumentModel created successfully")
        else:
            print("Warning: DocumentModel not available, falling back to old path")
        
        # Create PDF canvas (now the main visual editor)
        self.pdf_canvas = PDFCanvas(document_model=self.document_model)
        top_splitter.addWidget(self.pdf_canvas)
        
        # Create property panel
        self.property_panel = PropertyPanel()
        top_splitter.addWidget(self.property_panel)
        
        # Create LaTeX code view
        from PyQt6.QtWidgets import QTextEdit
        self.latex_view = QTextEdit()
        self.latex_view.setReadOnly(True)
        self.latex_view.setPlaceholderText("Generated LaTeX code will appear here...")
        main_splitter.addWidget(self.latex_view)
        
        # Initialize LaTeX engine
        self.latex_engine = LaTeXEngine()
        self.latex_generator = LaTeXGenerator()
        self.pdf_to_latex_converter = PDFToLaTeXConverter()
        
        # Create initial PDF document
        self.create_initial_pdf()
        
        # Connect PDF canvas events to property panel
        self.connect_pdf_canvas_events()
        
    def create_menu_bar(self):
        """Create menu bar"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As", self)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_document)
        file_menu.addAction(export_action)
        
        preview_action = QAction("Preview PDF", self)
        preview_action.setShortcut("F5")
        preview_action.triggered.connect(self.preview_document)
        file_menu.addAction(preview_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cut", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut("Ctrl++")
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        view_menu.addAction(zoom_out_action)
        
        view_menu.addSeparator()
        
        preview_action = QAction("Toggle Preview", self)
        preview_action.setShortcut("F5")
        view_menu.addAction(preview_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        
        documentation_action = QAction("Documentation", self)
        help_menu.addAction(documentation_action)
    

    
    def create_initial_pdf(self):
        """Create initial PDF document"""
        # Create a simple initial document
        initial_latex = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{geometry}
\geometry{a4paper, margin=2cm}
\begin{document}

\title{guiLaTeX Document}
\author{User}
\maketitle

Hello World!

$E = mc^2$

This is a test document created with guiLaTeX.
\end{document}
"""
        
        # Create PDF
        success = self.pdf_canvas.create_pdf(initial_latex)
        if success:
            # Update LaTeX view
            self.latex_view.setText(initial_latex)
            print("Initial PDF created successfully")
            
            # Update document model with elements from PDF
            if self.document_model and self.pdf_canvas.page_widget:
                try:
                    # Get memory elements from PDF canvas
                    memory_elements = self.pdf_canvas.page_widget.memory_elements
                    
                    # Get or create page model for current page
                    page_model = None
                    for page in self.document_model.pages:
                        if page.number == 0:  # First page
                            page_model = page
                            break
                    
                    if not page_model:
                        page_model = PageModel(number=0)
                        self.document_model.add_page(page_model)
                    
                    # Add elements to page model
                    for elem in memory_elements:
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
                        page_model.add_element(new_elem)
                    
                    print(f"Added {len(memory_elements)} elements to document model")
                    
                    # Refresh PDF canvas to use the model
                    self.pdf_canvas.update_page_display()
                    print("PDF canvas refreshed with document model")
                except Exception as e:
                    print(f"Error updating document model: {e}")
        else:
            print("Failed to create initial PDF")
    
    def connect_pdf_canvas_events(self):
        """Connect PDF canvas events to property panel"""
        if self.pdf_canvas.page_widget:
            # Connect element selection to property panel
            self.pdf_canvas.page_widget.element_selected.connect(self.on_element_selected)
            
            # Connect property changes back to PDF canvas
            self.property_panel.element_changed.connect(self.on_property_changed)
    
    def on_element_selected(self, element):
        """Handle element selection from PDF canvas"""
        self.property_panel.set_element(element)
        print(f"Element selected: {element.get('text', 'Unknown')}")
    
    def on_property_changed(self, element_id, property_name, value):
        """Handle property changes from property panel"""
        if self.pdf_canvas.page_widget:
            # Update text content
            if property_name == 'text':
                self.pdf_canvas.page_widget.update_element_text(element_id, value)
            # Update font size
            elif property_name == 'font_size':
                self.pdf_canvas.page_widget.update_element_font_size(element_id, value)
            # Update position
            elif property_name == 'position':
                x, y = value
                element = self.pdf_canvas.page_widget.get_element_by_id(element_id)
                if element:
                    element['x'] = x
                    element['y'] = y
                    self.pdf_canvas.page_widget.update()
            
            # Sync changes to LaTeX view
            self.sync_to_latex()
    
    def sync_to_latex(self):
        """Sync PDF canvas changes to LaTeX code view"""
        if self.pdf_canvas.page_widget and self.pdf_to_latex_converter:
            # Get memory elements from PDF canvas
            memory_elements = self.pdf_canvas.page_widget.memory_elements
            
            # Convert to LaTeX
            latex_code = self.pdf_to_latex_converter.convert_memory_elements(memory_elements)
            
            # Update LaTeX view
            self.latex_view.setText(latex_code)
            print("Synced changes to LaTeX view")
    
    def export_document(self):
        """Export document"""
        if not self.pdf_canvas.page_widget:
            QMessageBox.warning(self, "Export", "No document to export")
            return
        
        # Get LaTeX code from current state
        memory_elements = self.pdf_canvas.page_widget.memory_elements
        latex_code = self.pdf_to_latex_converter.convert_memory_elements(memory_elements)
        
        # Save LaTeX code to file
        export_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
        os.makedirs(export_dir, exist_ok=True)
        latex_path = os.path.join(export_dir, 'guiLaTeX_export.tex')
        
        try:
            with open(latex_path, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            
            # Show success message
            QMessageBox.information(self, "Export", 
                f"Document exported successfully to:\n{latex_path}")
            print(f"Exported LaTeX to: {latex_path}")
        except Exception as e:
            QMessageBox.warning(self, "Export", f"Failed to export document:\n{str(e)}")
    
    def preview_document(self):
        """Preview document as PDF"""
        # Check if LaTeX engine is available
        if not self.latex_engine.is_available():
            QMessageBox.warning(self, "Preview", "LaTeX engine not found")
            return
        
        # Get PDF path from PDF canvas
        pdf_path = "<repo-root>/temp/guiLaTeX_edit.pdf"
        
        if os.path.exists(pdf_path):
            # View PDF
            success = self.latex_engine.view_pdf(pdf_path)
            if success:
                print(f"Previewing PDF: {pdf_path}")
            else:
                QMessageBox.warning(self, "Preview", "Failed to open PDF viewer")
        else:
            QMessageBox.warning(self, "Preview", "No document to preview")


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
