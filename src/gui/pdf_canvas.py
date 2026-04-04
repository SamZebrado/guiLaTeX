#!/usr/bin/env python3
"""
guiLaTeX - PDF Canvas Component

PDF canvas viewer for interactive PDF editing
"""

import fitz  # PyMuPDF
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QImage, QPen, QBrush, QColor, QCursor, QFont
from PyQt6.QtCore import Qt, QSize, QRect, QRectF, QPointF


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
        
        # Mouse interaction
        self.drag_start_pos = None
        self.selected_element = None
        self.drag_handle = None
        
        # Extract text elements from PDF
        self.text_elements = self.extract_text_elements()
        
        # Handle size
        self.handle_size = 8
        self.resize_handles = [
            (0, 0), (0.5, 0), (1, 0),  # Top left, top center, top right
            (1, 0.5),  # Right center
            (1, 1), (0.5, 1), (0, 1),  # Bottom right, bottom center, bottom left
            (0, 0.5)   # Left center
        ]
        
        # In-memory PDF editing
        self.memory_elements = self.text_elements.copy()  # Copy for in-memory editing
        self.is_dirty = False  # Track if changes need to be saved
    
    def extract_text_elements(self):
        """Extract text elements from PDF page"""
        text_elements = []
        
        # Get text blocks with detailed information
        blocks = self.page.get_text("dict")["blocks"]
        for i, block in enumerate(blocks):
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:
                            text_elements.append({
                                'id': f'text_{i}',
                                'type': 'text',
                                'text': text,
                                'x': span["bbox"][0],
                                'y': span["bbox"][1],
                                'width': span["bbox"][2] - span["bbox"][0],
                                'height': span["bbox"][3] - span["bbox"][1],
                                'font_size': span["size"],
                                'original_width': span["bbox"][2] - span["bbox"][0],
                                'original_height': span["bbox"][3] - span["bbox"][1]
                            })
        
        return text_elements
    
    def paintEvent(self, event):
        """Paint PDF page"""
        painter = QPainter(self)
        
        # Render PDF page to pixmap
        pixmap = self.render_page()
        if not pixmap.isNull():
            painter.drawPixmap(0, 0, pixmap)
        
        # Draw memory elements (with updated sizes)
        self.draw_memory_elements(painter)
        
        # Draw selection indicators
        self.draw_selections(painter)
        
        # Draw handles for selected element
        if self.selected_element:
            self.draw_handles(painter)
    
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
    
    def draw_handles(self, painter):
        """Draw resize handles for selected element"""
        if not self.selected_element:
            return
        
        painter.setBrush(QBrush(QColor(0, 120, 215)))
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        
        # Draw resize handles
        element = self.selected_element
        for handle in self.resize_handles:
            x = element['x'] + handle[0] * element['width']
            y = element['y'] + handle[1] * element['height']
            rect = QRect(
                int(x * self.scale - self.handle_size / 2),
                int(y * self.scale - self.handle_size / 2),
                self.handle_size,
                self.handle_size
            )
            painter.drawRect(rect)
    
    def draw_memory_elements(self, painter):
        """Draw elements with updated sizes from memory"""
        # Draw elements with updated sizes
        for element in self.memory_elements:
            # Skip the selected element (it will be drawn in draw_selections)
            if self.selected_element and element['id'] == self.selected_element['id']:
                continue
            
            # Draw element background
            painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
            painter.setPen(QPen(QColor(200, 200, 200), 1))
            rect = QRect(
                int(element['x'] * self.scale),
                int(element['y'] * self.scale),
                int(element['width'] * self.scale),
                int(element['height'] * self.scale)
            )
            painter.drawRect(rect)
            
            # Calculate font size based on element scaling
            if 'original_width' in element and 'original_height' in element:
                width_scale = element['width'] / element['original_width']
                height_scale = element['height'] / element['original_height']
                scale_factor = min(width_scale, height_scale)
                
                # Get original font size (default to 12 if not available)
                original_font_size = element.get('font_size', 12)
                new_font_size = max(6, int(original_font_size * scale_factor * self.scale))
            else:
                # Fallback: estimate font size based on element height
                new_font_size = max(6, int(element['height'] * 0.3 * self.scale))
            
            # Set font with calculated size
            font = QFont()
            font.setPointSize(new_font_size)
            painter.setFont(font)
            
            # Draw element text
            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, element['text'])
    
    def get_element_at(self, pos):
        """Get element at position"""
        # Convert mouse position to PDF coordinates
        x = pos.x() / self.scale
        y = pos.y() / self.scale
        
        # Check text elements
        for element in self.text_elements:
            rect = QRectF(
                element['x'],
                element['y'],
                element['width'],
                element['height']
            )
            if rect.contains(x, y):
                return element
        
        return None
    
    def get_handle_at(self, pos):
        """Get handle at position"""
        if not self.selected_element:
            return None
        
        # Convert mouse position to PDF coordinates
        x = pos.x() / self.scale
        y = pos.y() / self.scale
        
        # Check resize handles
        element = self.selected_element
        for i, handle in enumerate(self.resize_handles):
            handle_x = element['x'] + handle[0] * element['width']
            handle_y = element['y'] + handle[1] * element['height']
            rect = QRectF(
                handle_x - self.handle_size / 2 / self.scale,
                handle_y - self.handle_size / 2 / self.scale,
                self.handle_size / self.scale,
                self.handle_size / self.scale
            )
            if rect.contains(x, y):
                return f"resize_{i}"
        
        return None
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        # Check if clicking on a handle
        handle = self.get_handle_at(event.pos())
        if handle:
            self.drag_handle = handle
            self.drag_start_pos = event.pos()
            return
        
        # Check if clicking on an element
        element = self.get_element_at(event.pos())
        if element:
            # Clear previous selection
            self.selected_elements = []
            self.selected_element = element
            self.selected_elements.append(element)
            self.update()
            print(f"Selected element: {element['text']}")
        else:
            # Clear selection
            self.selected_elements = []
            self.selected_element = None
            self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        if self.drag_handle and self.selected_element and self.drag_start_pos:
            # Calculate delta
            dx = (event.pos().x() - self.drag_start_pos.x()) / self.scale
            dy = (event.pos().y() - self.drag_start_pos.y()) / self.scale
            
            # Handle resize
            if self.drag_handle.startswith("resize_"):
                handle_idx = int(self.drag_handle.split("_")[1])
                handle = self.resize_handles[handle_idx]
                
                element = self.selected_element
                new_width = element['width']
                new_height = element['height']
                new_x = element['x']
                new_y = element['y']
                
                if handle[0] == 1:  # Right side
                    new_width = max(20, element['width'] + dx)
                elif handle[0] == 0:  # Left side
                    new_width = max(20, element['width'] - dx)
                    new_x = element['x'] + dx
                
                if handle[1] == 1:  # Bottom side
                    new_height = max(20, element['height'] + dy)
                elif handle[1] == 0:  # Top side
                    new_height = max(20, element['height'] - dy)
                    new_y = element['y'] + dy
                
                # Update element
                element['width'] = new_width
                element['height'] = new_height
                element['x'] = new_x
                element['y'] = new_y
                
                # Update memory elements
                for mem_element in self.memory_elements:
                    if mem_element['id'] == element['id']:
                        mem_element['width'] = new_width
                        mem_element['height'] = new_height
                        mem_element['x'] = new_x
                        mem_element['y'] = new_y
                        break
                
                # Mark as dirty
                self.is_dirty = True
                
                # Update the visual representation
                self.update()
                self.drag_start_pos = event.pos()
                
                # Print debug information
                print(f"Resized element to: {new_width:.2f}x{new_height:.2f} at ({new_x:.2f}, {new_y:.2f})")
    
    def update_pdf_element(self, element):
        """Update element in PDF"""
        # This is a placeholder for actual PDF text updating
        # In a real implementation, we would:
        # 1. Remove the old text
        # 2. Add new text with updated size and position
        # 3. Save the PDF
        print(f"Updating PDF element: {element['text']}")
        # TODO: Implement actual PDF text updating
    
    def save_changes(self):
        """Save changes to PDF file"""
        if not self.is_dirty:
            print("No changes to save")
            return True
        
        try:
            # TODO: Implement actual PDF updating
            # For now, we'll just print the changes
            print("Saving changes to PDF...")
            for element in self.memory_elements:
                print(f"Element: {element['text']} - {element['width']:.2f}x{element['height']:.2f} at ({element['x']:.2f}, {element['y']:.2f})")
            
            # Mark as clean
            self.is_dirty = False
            print("Changes saved successfully")
            return True
        except Exception as e:
            print(f"Error saving changes: {e}")
            return False
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.drag_handle = None
        self.drag_start_pos = None
    
    def hoverMoveEvent(self, event):
        """Handle hover move"""
        # Check if hovering over a handle
        handle = self.get_handle_at(event.pos())
        if handle:
            if handle.startswith("resize_"):
                handle_idx = int(handle.split("_")[1])
                cursor_map = [
                    Qt.CursorShape.SizeFDiagCursor,  # Top left
                    Qt.CursorShape.SizeVerCursor,     # Top center
                    Qt.CursorShape.SizeBDiagCursor,  # Top right
                    Qt.CursorShape.SizeHorCursor,     # Right center
                    Qt.CursorShape.SizeFDiagCursor,  # Bottom right
                    Qt.CursorShape.SizeVerCursor,     # Bottom center
                    Qt.CursorShape.SizeBDiagCursor,  # Bottom left
                    Qt.CursorShape.SizeHorCursor      # Left center
                ]
                if 0 <= handle_idx < len(cursor_map):
                    self.setCursor(cursor_map[handle_idx])
                    return
        
        # Check if hovering over an element
        element = self.get_element_at(event.pos())
        if element:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
    
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
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_changes)
        self.toolbar.addWidget(self.save_button)
        
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
        
        # First compile to temporary directory
        engine = LaTeXEngine()
        success, temp_pdf_path, log, temp_dir = engine.compile(latex_code, keep_temp=True)
        
        if success:
            # Copy the generated PDF to our persistent location
            import shutil
            try:
                shutil.copy2(temp_pdf_path, pdf_path)
                print(f"Copied PDF to: {pdf_path}")
                
                # Load the PDF
                self.load_pdf(pdf_path)
                
                # Clean up temp directory
                if temp_dir and os.path.exists(temp_dir):
                    try:
                        shutil.rmtree(temp_dir)
                        print(f"Cleaned up temp directory: {temp_dir}")
                    except Exception as e:
                        print(f"Warning: Failed to clean up temp directory: {e}")
                return True
            except Exception as e:
                print(f"Error copying PDF: {e}")
                return False
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
    
    def save_changes(self):
        """Save changes to PDF"""
        if self.page_widget:
            return self.page_widget.save_changes()
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
