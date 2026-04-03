#!/usr/bin/env python3
"""
guiLaTeX - PDF Preview Component

Real-time PDF preview functionality
"""

import os
import sys
import shutil
import tempfile
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# Try to import Poppler for PDF rendering
try:
    from popplerqt6 import Poppler
    HAS_POPPLER = True
except ImportError:
    HAS_POPPLER = False


class PDFPreviewThread(QThread):
    """Thread for PDF compilation and rendering"""
    
    # Signals
    preview_ready = pyqtSignal(QPixmap, str)  # pixmap, temp_dir
    error_occurred = pyqtSignal(str)
    
    def __init__(self, latex_engine, latex_generator, elements):
        super().__init__()
        self.latex_engine = latex_engine
        self.latex_generator = latex_generator
        self.elements = elements
        self.running = True
        self.temp_dir = None
    
    def run(self):
        """Run PDF compilation and rendering"""
        if not self.latex_engine.is_available():
            self.error_occurred.emit("LaTeX engine not available")
            return
        
        try:
            # Generate LaTeX code
            latex_code = self.latex_generator.generate(self.elements)
            
            # Compile to PDF (keep temp dir for rendering)
            success, pdf_path, log, temp_dir = self.latex_engine.compile(latex_code, keep_temp=True)
            
            if success:
                # Store temp dir for cleanup later
                self.temp_dir = temp_dir
                
                # Render PDF
                pixmap = self.render_pdf(pdf_path)
                if pixmap:
                    self.preview_ready.emit(pixmap, temp_dir)
                else:
                    self.error_occurred.emit("Failed to render PDF")
                    # Clean up temp dir if rendering failed
                    if temp_dir and os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
            else:
                self.error_occurred.emit(f"Compilation failed:\n{log}")
                # Clean up temp dir if compilation failed
                if temp_dir and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}")
            # Clean up temp dir on exception
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
    
    def render_pdf(self, pdf_path):
        """Render PDF to pixmap"""
        if not HAS_POPPLER:
            # Fallback: just show PDF path
            label = QLabel(f"PDF generated at:\n{pdf_path}")
            pixmap = QPixmap(800, 600)
            painter = QPainter(pixmap)
            painter.fillRect(0, 0, 800, 600, Qt.GlobalColor.white)
            label.render(painter)
            painter.end()
            return pixmap
        
        try:
            # Use Poppler to render PDF
            document = Poppler.Document.load(pdf_path)
            if document and document.numPages() > 0:
                page = document.page(0)
                if page:
                    # Render at 96 DPI
                    image = page.renderToImage(96, 96)
                    if image.isNull():
                        return None
                    pixmap = QPixmap.fromImage(image)
                    return pixmap
            return None
        except Exception:
            return None
    
    def stop(self):
        """Stop the thread"""
        self.running = False
        self.wait()


class PDFPreview(QWidget):
    """PDF preview widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(400)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        
        # Create title
        title_label = QLabel("PDF Preview")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)
        
        # Create scroll area for preview
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Create preview label
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setText("No preview available")
        
        self.scroll_area.setWidget(self.preview_label)
        self.layout.addWidget(self.scroll_area)
        
        # Create refresh button
        self.refresh_button = QPushButton("Refresh Preview")
        self.refresh_button.clicked.connect(self.refresh_preview)
        self.layout.addWidget(self.refresh_button)
        
        # Initialize variables
        self.latex_engine = None
        self.latex_generator = None
        self.elements = []
        self.preview_thread = None
        self.current_temp_dir = None  # Track current temp directory for cleanup
    
    def set_latex_engines(self, latex_engine, latex_generator):
        """Set LaTeX engines"""
        self.latex_engine = latex_engine
        self.latex_generator = latex_generator
    
    def set_elements(self, elements):
        """Set elements to preview"""
        self.elements = elements
    
    def refresh_preview(self):
        """Refresh PDF preview"""
        if not self.latex_engine or not self.latex_generator:
            self.preview_label.setText("LaTeX engines not initialized")
            return
        
        if not self.elements:
            self.preview_label.setText("No elements to preview")
            return
        
        # Clean up previous temp directory
        self._cleanup_temp_dir()
        
        # Stop any running thread
        if self.preview_thread:
            self.preview_thread.stop()
        
        # Start new preview thread
        self.preview_label.setText("Generating preview...")
        self.preview_thread = PDFPreviewThread(
            self.latex_engine, self.latex_generator, self.elements
        )
        self.preview_thread.preview_ready.connect(self.on_preview_ready)
        self.preview_thread.error_occurred.connect(self.on_error_occurred)
        self.preview_thread.start()
    
    def _cleanup_temp_dir(self):
        """Clean up temporary directory"""
        if self.current_temp_dir and os.path.exists(self.current_temp_dir):
            try:
                shutil.rmtree(self.current_temp_dir)
                print(f"Cleaned up temp directory: {self.current_temp_dir}")
            except Exception as e:
                print(f"Warning: Failed to clean up temp directory {self.current_temp_dir}: {e}")
            finally:
                self.current_temp_dir = None
    
    def on_preview_ready(self, pixmap, temp_dir):
        """Handle preview ready signal"""
        self.preview_label.setPixmap(pixmap)
        self.preview_label.setScaledContents(True)
        
        # Store temp directory for cleanup on next refresh or widget destruction
        self.current_temp_dir = temp_dir
        print(f"PDF preview ready, temp dir: {temp_dir}")
    
    def on_error_occurred(self, error_message):
        """Handle error signal"""
        self.preview_label.setText(f"Error:\n{error_message}")
    
    def update_preview(self):
        """Update preview (alias for refresh_preview)"""
        self.refresh_preview()
    
    def closeEvent(self, event):
        """Handle widget close event - clean up temp directory"""
        self._cleanup_temp_dir()
        super().closeEvent(event)
