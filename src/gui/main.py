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
from gui.properties import PropertyPanel
from gui.pdf_canvas import PDFCanvas


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
        
        # Create PDF canvas (now the main visual editor)
        self.pdf_canvas = PDFCanvas()
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
        
        # Create initial PDF document
        self.create_initial_pdf()
        
        # Connect PDF canvas events to property panel
        # TODO: Implement PDF canvas selection events
        
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
        else:
            print("Failed to create initial PDF")
    
    def export_document(self):
        """Export document"""
        # Get PDF path from PDF canvas
        # TODO: Implement PDF to LaTeX export
        pdf_path = "<repo-root>/temp/guiLaTeX_edit.pdf"
        
        if os.path.exists(pdf_path):
            # Show success message
            QMessageBox.information(self, "Export", f"Document exported successfully to:\n{pdf_path}")
        else:
            QMessageBox.warning(self, "Export", "No document to export")
    
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
