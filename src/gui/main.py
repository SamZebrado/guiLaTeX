#!/usr/bin/env python3
"""
guiLaTeX - Visual LaTeX Editor

Main application entry point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMenuBar, QMenu, QSplitter, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules
import canvas
from latex.engine import LaTeXEngine, LaTeXGenerator
from gui.properties import PropertyPanel
from gui.preview import PDFPreview


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
        
        # Create top splitter (horizontal) for canvas and properties
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.addWidget(top_splitter)
        
        # Create canvas
        self.canvas = canvas.Canvas()
        top_splitter.addWidget(self.canvas)
        
        # Create property panel
        self.property_panel = PropertyPanel()
        top_splitter.addWidget(self.property_panel)
        
        # Create PDF preview
        self.pdf_preview = PDFPreview()
        main_splitter.addWidget(self.pdf_preview)
        
        # Initialize LaTeX engine
        self.latex_engine = LaTeXEngine()
        self.latex_generator = LaTeXGenerator()
        
        # Set LaTeX engines for PDF preview
        self.pdf_preview.set_latex_engines(self.latex_engine, self.latex_generator)
        
        # Connect canvas selection changes to property panel
        self.canvas.scene.selectionChanged.connect(self.on_selection_changed)
        
        # Connect canvas changes to PDF preview
        self.canvas.scene.changed.connect(self.on_scene_changed)
        
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
    
    def export_document(self):
        """Export document"""
        # Get elements from canvas
        elements = [item for item in self.canvas.scene.items() 
                   if hasattr(item, 'text')]
        
        if not elements:
            QMessageBox.warning(self, "Export", "No elements to export")
            return
        
        # Generate LaTeX code
        latex_code = self.latex_generator.generate(elements)
        
        # Save to file
        # TODO: Implement file save dialog
        print("Generated LaTeX code:")
        print(latex_code)
        
        QMessageBox.information(self, "Export", "Document exported successfully")
    
    def preview_document(self):
        """Preview document as PDF"""
        # Check if LaTeX engine is available
        if not self.latex_engine.is_available():
            QMessageBox.warning(self, "Preview", "LaTeX engine not found")
            return
        
        # Get elements from canvas
        elements = [item for item in self.canvas.scene.items() 
                   if hasattr(item, 'text')]
        
        if not elements:
            QMessageBox.warning(self, "Preview", "No elements to preview")
            return
        
        # Generate LaTeX code
        latex_code = self.latex_generator.generate(elements)
        
        # Compile to PDF
        success, pdf_path, log, temp_dir = self.latex_engine.compile(latex_code, keep_temp=True)
        
        if success:
            # View PDF
            self.latex_engine.view_pdf(pdf_path)
            # Clean up temp directory after viewing
            import shutil
            import os
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    print(f"Cleaned up temp directory: {temp_dir}")
                except Exception as e:
                    print(f"Warning: Failed to clean up temp directory: {e}")
        else:
            QMessageBox.warning(self, "Preview", f"Compilation failed:\n{log}")
    
    def on_selection_changed(self):
        """Handle canvas selection changes"""
        # Get selected items
        selected_items = [item for item in self.canvas.scene.items() if item.isSelected()]
        
        # Set first selected item to property panel
        if selected_items:
            self.property_panel.set_element(selected_items[0])
        else:
            self.property_panel.set_element(None)
    
    def on_scene_changed(self, regions=None):
        """Handle canvas scene changes"""
        # Get all elements
        elements = [item for item in self.canvas.scene.items() 
                   if hasattr(item, 'text')]
        
        # Update PDF preview elements
        self.pdf_preview.set_elements(elements)
        # Refresh preview
        self.pdf_preview.refresh_preview()


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
