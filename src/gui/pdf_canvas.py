#!/usr/bin/env python3
"""
guiLaTeX - PDF Canvas Component

PDF canvas viewer for interactive PDF editing
"""

import fitz  # PyMuPDF
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QImage, QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QSize, QRect


class PDFPageWidget(QWidget):
    """PDF page display widget"""
    
    def __init__(self, pdf_doc, page_num, parent=None):
        super().__init__(parent)
        self.pdf_doc = pdf_doc
        self.page_num = page_num
        self.page = pdf_doc.load_page(page_num)
        self.selected_elements = []
        self.scale = 1.0
        
        # Get page dimensions
        self.page_rect = self.page.rect
        self.width = self.page_rect.width
        self.height = self.page_rect.height
        
        # Set widget size
        self.setMinimumSize(int(self.width * 0.8), int(self.height * 0.8))
        
    def paintEvent(self, event):
        """Paint PDF page"""
        painter = QPainter(self)
        
        # Render PDF page to pixmap
        pixmap = self.render_page()
        if not pixmap.isNull():
            painter.drawPixmap(0, 0, pixmap)
        
        # Draw selection indicators
        self.draw_selections(painter)
    
    def render_page(self):
        """Render PDF page to QPixmap"""
        try:
            # Convert PDF page to pixmap
            pix = self.page.get_pixmap(matrix=fitz.Matrix(self.scale, self.scale))
            img_data = pix.tobytes("ppm")
            image = QImage.fromData(img_data)
            return QPixmap.fromImage(image)
        except Exception as e:
            print(f"Error rendering page: {e}")
            return QPixmap()
    
    def draw_selections(self, painter):
        """Draw selection indicators"""
        painter.setPen(QPen(QColor(0, 120, 215), 2, Qt.PenStyle.DashLine))
        painter.setBrush(QBrush(QColor(0, 120, 215, 50)))
        
        # Draw selection rectangles
        for element in self.selected_elements:
            rect = QRect(
                int(element['x'] * self.scale),
                int(element['y'] * self.scale),
                int(element['width'] * self.scale),
                int(element['height'] * self.scale)
            )
            painter.drawRect(rect)
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        # Convert mouse position to PDF coordinates
        x = event.pos().x() / self.scale
        y = event.pos().y() / self.scale
        
        # TODO: Implement element selection logic
        print(f"Mouse pressed at PDF coords: ({x:.2f}, {y:.2f})")
    
    def set_scale(self, scale):
        """Set zoom scale"""
        self.scale = scale
        self.update()


class PDFCanvas(QWidget):
    """PDF canvas for interactive editing"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        
        # Create toolbar
        self.toolbar = QHBoxLayout()
        self.layout.addLayout(self.toolbar)
        
        # Navigation buttons
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.toolbar.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.toolbar.addWidget(self.next_button)
        
        self.page_label = QLabel("Page 1")
        self.toolbar.addWidget(self.page_label)
        
        # Zoom controls
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.toolbar.addWidget(self.zoom_in_button)
        
        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.toolbar.addWidget(self.zoom_out_button)
        
        # Scroll area for PDF pages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)
        
        # PDF document
        self.pdf_doc = None
        self.current_page = 0
        self.page_widget = None
        self.zoom_scale = 1.0
    
    def load_pdf(self, pdf_path):
        """Load PDF document"""
        try:
            self.pdf_doc = fitz.open(pdf_path)
            self.current_page = 0
            self.update_page_display()
            return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def create_pdf(self, latex_code):
        """Create PDF from LaTeX code"""
        import sys
        import os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from latex.engine import LaTeXEngine
        
        # Create a persistent PDF file in the project directory
        pdf_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, 'guiLaTeX_edit.pdf')
        
        engine = LaTeXEngine()
        success, pdf_path, log, temp_dir = engine.compile(latex_code, output_path=pdf_path, keep_temp=False)
        
        if success:
            self.load_pdf(pdf_path)
            # Clean up temp directory immediately
            import shutil
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    print(f"Cleaned up temp directory: {temp_dir}")
                except Exception as e:
                    print(f"Warning: Failed to clean up temp directory: {e}")
            return True
        else:
            print(f"LaTeX compilation failed: {log}")
            return False
    
    def update_page_display(self):
        """Update page display"""
        if not self.pdf_doc:
            return
        
        # Create new page widget
        self.page_widget = PDFPageWidget(self.pdf_doc, self.current_page)
        self.page_widget.set_scale(self.zoom_scale)
        self.scroll_area.setWidget(self.page_widget)
        
        # Update page label
        self.page_label.setText(f"Page {self.current_page + 1} of {len(self.pdf_doc)}")
    
    def previous_page(self):
        """Go to previous page"""
        if self.pdf_doc and self.current_page > 0:
            self.current_page -= 1
            self.update_page_display()
    
    def next_page(self):
        """Go to next page"""
        if self.pdf_doc and self.current_page < len(self.pdf_doc) - 1:
            self.current_page += 1
            self.update_page_display()
    
    def zoom_in(self):
        """Zoom in"""
        self.zoom_scale += 0.2
        if self.page_widget:
            self.page_widget.set_scale(self.zoom_scale)
    
    def zoom_out(self):
        """Zoom out"""
        if self.zoom_scale > 0.2:
            self.zoom_scale -= 0.2
            if self.page_widget:
                self.page_widget.set_scale(self.zoom_scale)
    
    def get_annotations(self):
        """Get annotations from current page"""
        if not self.pdf_doc:
            return []
        
        page = self.pdf_doc.load_page(self.current_page)
        annotations = page.annots()
        
        # Extract annotations
        annot_data = []
        for annot in annotations:
            if annot.type[0] == 1:  # Text annotation
                content = annot.info.get('content', '')
                rect = annot.rect
                annot_data.append({
                    'type': 'text',
                    'content': content,
                    'x': rect.x0,
                    'y': rect.y0,
                    'width': rect.width,
                    'height': rect.height
                })
        
        return annot_data
    
    def add_annotation(self, x, y, width, height, content):
        """Add annotation to current page"""
        if not self.pdf_doc:
            return False
        
        try:
            page = self.pdf_doc.load_page(self.current_page)
            rect = fitz.Rect(x, y, x + width, y + height)
            annot = page.add_text_annot(rect.tl, content)
            annot.set_info(title="guiLaTeX", content=content)
            annot.set_flags(fitz.ANNOT_FLAG_HIDDEN)
            
            # Save changes
            self.pdf_doc.saveIncr()
            return True
        except Exception as e:
            print(f"Error adding annotation: {e}")
            return False
    
    def closeEvent(self, event):
        """Handle close event"""
        if self.pdf_doc:
            self.pdf_doc.close()
        super().closeEvent(event)


if __name__ == "__main__":
    """Test PDF canvas"""
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create test PDF
    test_latex = r"""\documentclass{article}
\begin{document}
\title{Test Document}
\author{guiLaTeX}
\maketitle

Hello World!

$E = mc^2$

This is a test document for the PDF canvas.
\end{document}
"""
    
    # Create PDF canvas
    canvas = PDFCanvas()
    canvas.create_pdf(test_latex)
    canvas.show()
    
    sys.exit(app.exec())
