#!/usr/bin/env python3
"""
guiLaTeX - PDF Canvas Component

PDF canvas viewer for interactive PDF editing
"""

import fitz  # PyMuPDF
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QPainter, QImage, QPen, QBrush, QColor, QCursor, QFont
from PyQt6.QtCore import Qt, QSize, QRect, QRectF, QPointF, pyqtSignal

# Add model layer import
try:
    from model import PageModel, ElementModel
except ImportError:
    # Fallback: model layer not available
    PageModel = None
    ElementModel = None


class PDFPageWidget(QWidget):
    """PDF page display widget"""
    
    # Signals
    element_selected = pyqtSignal(dict)  # Emitted when an element is selected
    element_modified = pyqtSignal(dict)  # Emitted when an element is modified
    
    def __init__(self, pdf_doc, page_num, parent=None, page_model=None):
        super().__init__(parent)
        self.pdf_doc = pdf_doc
        self.page_num = page_num
        self.page = pdf_doc.load_page(page_num)
        self.selected_element = None
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
        self.is_dragging_element = False  # Track if dragging entire element
        self.element_start_pos = None  # Track element start position for move
        
        # Handle size
        self.handle_size = 8
        self.resize_handles = [
            (0, 0), (0.5, 0), (1, 0),  # Top left, top center, top right
            (1, 0.5),  # Right center
            (1, 1), (0.5, 1), (0, 1),  # Bottom right, bottom center, bottom left
            (0, 0.5)   # Left center
        ]
        
        # Model layer integration
        self.page_model = page_model
        
        # Extract text elements from PDF
        self.text_elements = self.extract_text_elements()
        
        # In-memory PDF editing
        self.memory_elements = self.text_elements.copy()  # Copy for in-memory editing
        
        # Layer management
        self.layers = [
            {'id': 'layer_1', 'name': '默认图层', 'visible': True, 'elements': []}
        ]
        self.current_layer_id = 'layer_1'
        
        # Initialize elements with default layer
        for elem in self.memory_elements:
            elem['layer_id'] = 'layer_1'
            self.layers[0]['elements'].append(elem['id'])
        
        self.is_dirty = False  # Track if changes need to be saved
        
        # Enable mouse tracking for hover events
        self.setMouseTracking(True)
        
        # If page model is provided, use it
        if self.page_model and PageModel:
            # First sync from model
            self._sync_from_model()
            
            # If model is empty, add unified demo scene elements and sync back to model
            if not self.memory_elements:
                # Unified demo scene with 5 types of objects
                self.memory_elements = [
                    # Title
                    {
                        'id': 'demo_title',
                        'type': 'text',
                        'text': '可视化编辑 LaTeX 文档',
                        'x': 100,
                        'y': 50,
                        'width': 400,
                        'height': 40,
                        'font_size': 24,
                        'font_family': 'Noto Sans SC',
                        'original_width': 400,
                        'original_height': 40,
                        'rotation': 0
                    },
                    # Author
                    {
                        'id': 'demo_author',
                        'type': 'text',
                        'text': '作者：某某 / 博士生原型测试',
                        'x': 100,
                        'y': 100,
                        'width': 300,
                        'height': 25,
                        'font_size': 14,
                        'font_family': 'Noto Sans SC',
                        'original_width': 300,
                        'original_height': 25,
                        'rotation': 0
                    },
                    # Body text
                    {
                        'id': 'demo_body',
                        'type': 'text',
                        'text': '这是一段用于演示正文对象的内容，可用于测试拖动、选择和后续选择框能力。',
                        'x': 100,
                        'y': 150,
                        'width': 400,
                        'height': 80,
                        'font_size': 12,
                        'font_family': 'Noto Sans SC',
                        'original_width': 400,
                        'original_height': 80,
                        'rotation': 0
                    },
                    # Formula
                    {
                        'id': 'demo_formula',
                        'type': 'text',
                        'text': 'E = mc²',
                        'x': 100,
                        'y': 240,
                        'width': 200,
                        'height': 30,
                        'font_size': 16,
                        'font_family': 'Noto Sans SC',
                        'original_width': 200,
                        'original_height': 30,
                        'rotation': 0
                    },
                    # Image placeholder
                    {
                        'id': 'demo_image',
                        'type': 'text',
                        'text': '图片示例 / 占位图',
                        'x': 100,
                        'y': 280,
                        'width': 300,
                        'height': 200,
                        'font_size': 12,
                        'font_family': 'Noto Sans SC',
                        'original_width': 300,
                        'original_height': 200,
                        'rotation': 0
                    }
                ]
                print("Added unified demo scene elements to empty model")
                # Sync demo elements to model
                self._sync_to_model()
        
        # Startup self-check
        self._perform_startup_check()
    
    def _sync_from_model(self):
        """Sync elements from PageModel to memory_elements"""
        if not self.page_model:
            return
        
        # Clear selection to avoid references to old elements
        self.selected_element = None
        
        # Convert ElementModel objects to old-style elements
        self.memory_elements = []
        for elem in self.page_model.elements:
            old_elem = {
                'id': elem.id,
                'type': elem.type,
                'text': elem.content,
                'x': elem.x,
                'y': elem.y,
                'width': elem.width,
                'height': elem.height,
                'font_size': elem.font_size,
                'font_family': getattr(elem, 'font_family', 'Noto Sans SC'),
                'original_width': elem.width,
                'original_height': elem.height,
                'rotation': getattr(elem, 'rotation', 0)
            }
            self.memory_elements.append(old_elem)
    
    def _perform_startup_check(self):
        """Perform startup self-check and print diagnostic information"""
        # Check memory elements
        memory_count = len(self.memory_elements)
        
        # Check for duplicate IDs
        unique_ids = set()
        duplicate_found = False
        duplicate_ids = []
        for elem in self.memory_elements:
            if elem['id'] in unique_ids:
                duplicate_found = True
                duplicate_ids.append(elem['id'])
            unique_ids.add(elem['id'])
        
        # Check page model if available
        page_model_count = 0
        page_model_ids = []
        if self.page_model:
            page_model_count = len(self.page_model.elements)
            page_model_ids = [elem.id for elem in self.page_model.elements]
        
        # Determine scene mode
        is_demo_mode = any('demo_' in elem['id'] for elem in self.memory_elements)
        scene_mode = 'demo_only' if is_demo_mode else 'unknown'
        
        # Check font status
        font_info = self._check_font_status()
        
        # Print startup info
        print("=== 启动自检信息 ===")
        print(f"startup object_count={memory_count}")
        print(f"startup unique_ids_count={len(unique_ids)}")
        print(f"startup unique_ids={sorted(list(unique_ids))}")
        print(f"startup duplicate_found={duplicate_found}")
        if duplicate_found:
            print(f"startup duplicate_ids={duplicate_ids}")
        print(f"startup page_model_count={page_model_count}")
        print(f"startup memory_elements_count={memory_count}")
        print(f"startup visible_scene_mode={scene_mode}")
        print(f"requested_font_stack={font_info['requested_stack']}")
        print(f"actual_font_family={font_info['actual_family']}")
        print(f"font_exact_match={font_info['exact_match']}")
        print("===================")
        
        # Additional diagnostic info
        if memory_count != len(unique_ids):
            print("警告: 发现重复对象！")
            print(f"内存元素数量: {memory_count}, 唯一ID数量: {len(unique_ids)}")
        if page_model_count != len(set(page_model_ids)):
            print("警告: 模型中存在重复对象！")
            print(f"模型元素数量: {page_model_count}, 唯一ID数量: {len(set(page_model_ids))}")
    
    def _check_font_status(self):
        """Check font status and return font information"""
        from PyQt6.QtGui import QFont
        
        # Requested font stack (只保留开源/免费可商用字体)
        font_stack = [
            "Noto Sans SC",
            "Source Han Sans SC",
            "Inter",
            "Noto Sans",
            "Sans Serif"
        ]
        
        # Try each font in the stack
        actual_family = ""
        exact_match = False
        
        for family in font_stack:
            font = QFont()
            font.setFamily(family)
            if font.exactMatch():
                actual_family = family
                exact_match = True
                break
        
        # If no exact match, use the first available
        if not actual_family:
            for family in font_stack:
                font = QFont()
                font.setFamily(family)
                # Check if the font is available (even if not exact match)
                if font.family() == family:
                    actual_family = family
                    break
        
        # Final fallback
        if not actual_family:
            font = QFont()
            actual_family = font.family()
        
        return {
            'requested_stack': font_stack,
            'actual_family': actual_family,
            'exact_match': exact_match
        }
    
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
        
        # Check if we're in demo mode (has demo elements)
        is_demo_mode = any('demo_' in elem['id'] for elem in self.memory_elements)
        
        # Only render PDF background if not in demo mode
        if not is_demo_mode:
            # Render PDF page to pixmap
            pixmap = self.render_page()
            if not pixmap.isNull():
                painter.drawPixmap(0, 0, pixmap)
        else:
            # Draw a clean white background for demo mode
            painter.fillRect(self.rect(), QColor(255, 255, 255))
        
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
        
        # Draw selection rectangle for the single selected element
        if self.selected_element:
            rect = QRect(
                int(self.selected_element['x'] * self.scale),
                int(self.selected_element['y'] * self.scale),
                int(self.selected_element['width'] * self.scale),
                int(self.selected_element['height'] * self.scale)
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
        # Draw elements with updated sizes, considering layer visibility
        for element in self.memory_elements:
            # Check if element's layer is visible
            layer_id = element.get('layer_id', 'layer_1')
            layer_visible = True
            for layer in self.layers:
                if layer['id'] == layer_id:
                    layer_visible = layer['visible']
                    break
            
            if not layer_visible:
                continue
            
            # Save painter state before rotation
            painter.save()
            
            # Get element position and dimensions
            x = element['x'] * self.scale
            y = element['y'] * self.scale
            width = element['width'] * self.scale
            height = element['height'] * self.scale
            rotation = element.get('rotation', 0)
            
            # Apply rotation around element center
            center_x = x + width / 2
            center_y = y + height / 2
            painter.translate(center_x, center_y)
            painter.rotate(rotation)
            painter.translate(-center_x, -center_y)
            
            # Draw ALL elements including selected one (to show updated size/position)
            # The selection highlight will be drawn on top in draw_selections
            
            # Draw element background
            painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
            painter.setPen(QPen(QColor(200, 200, 200), 1))
            rect = QRect(
                int(x),
                int(y),
                int(width),
                int(height)
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
            
            # First try to use the font family specified in the element
            element_font = element.get('font_family')
            if element_font:
                font.setFamily(element_font)
                if not font.exactMatch():
                    # If specified font is not available, use fallback fonts (只保留开源/免费可商用字体)
                    font_families = [
                        "Noto Sans SC",      # Google's Noto Sans for Simplified Chinese
                        "Source Han Sans SC", # Adobe's Source Han Sans for Simplified Chinese
                        "Inter",            # Inter font (开源)
                        "Noto Sans",        # Google's Noto Sans
                        "Sans Serif"         # Fallback
                    ]
                    for family in font_families:
                        font.setFamily(family)
                        # Check if font is available
                        if font.exactMatch():
                            break
            else:
                # Use default font families for Chinese support (只保留开源/免费可商用字体)
                font_families = [
                    "Noto Sans SC",      # Google's Noto Sans for Simplified Chinese
                    "Source Han Sans SC", # Adobe's Source Han Sans for Simplified Chinese
                    "Inter",            # Inter font (开源)
                    "Noto Sans",        # Google's Noto Sans
                    "Sans Serif"         # Fallback
                ]
                for family in font_families:
                    font.setFamily(family)
                    # Check if font is available
                    if font.exactMatch():
                        break
            font.setPointSize(new_font_size)
            painter.setFont(font)
            
            # Draw element text
            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, element['text'])
            
            # Restore painter state after rotation
            painter.restore()
    
    def get_element_at(self, pos):
        """Get element at position"""
        # Convert mouse position to PDF coordinates
        x = pos.x() / self.scale
        y = pos.y() / self.scale
        
        # Check memory elements (use updated positions/sizes)
        for element in self.memory_elements:
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
            self.is_dragging_element = False
            return
        
        # Check if clicking on an element
        element = self.get_element_at(event.pos())
        if element:
            # Set selection
            self.selected_element = element
            
            # Start dragging the element
            self.is_dragging_element = True
            self.drag_start_pos = event.pos()
            self.element_start_pos = (element['x'], element['y'])
            
            # Emit signal for element selection
            self.element_selected.emit(element)
            
            self.update()
            print(f"Selected element: {element['text']}")
        else:
            # Clear selection
            self.selected_element = None
            self.is_dragging_element = False
            self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        # Handle element resize via handles
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
                
                # Update element (element is already in memory_elements, so direct update works)
                element['width'] = new_width
                element['height'] = new_height
                element['x'] = new_x
                element['y'] = new_y
                
                # Mark as dirty
                self.is_dirty = True
                
                # Update the visual representation
                self.update()
                self.drag_start_pos = event.pos()
                
                # Print debug information
                print(f"Resized element to: {new_width:.2f}x{new_height:.2f} at ({new_x:.2f}, {new_y:.2f})")
        
        # Handle element move (dragging entire element)
        elif self.is_dragging_element and self.selected_element and self.drag_start_pos and self.element_start_pos:
            # Calculate delta from start position
            dx = (event.pos().x() - self.drag_start_pos.x()) / self.scale
            dy = (event.pos().y() - self.drag_start_pos.y()) / self.scale
            
            element = self.selected_element
            start_x, start_y = self.element_start_pos
            
            # Calculate new position
            new_x = start_x + dx
            new_y = start_y + dy
            
            # Update element position (element is already in memory_elements)
            element['x'] = new_x
            element['y'] = new_y
            
            # Mark as dirty
            self.is_dirty = True
            
            # Update the visual representation
            self.update()
            
            # Print debug information
            print(f"Moved element to: ({new_x:.2f}, {new_y:.2f})")
        
        # Update cursor based on what's under the mouse
        self.update_cursor(event.pos())
    
    def update_element_text(self, element_id, new_text):
        """Update text content of an element
        
        Args:
            element_id: ID of the element to update
            new_text: New text content
            
        Returns:
            bool: True if successful
        """
        # Update in memory elements
        for element in self.memory_elements:
            if element['id'] == element_id:
                element['text'] = new_text
                self.is_dirty = True
                self.update()
                # Sync changes to model
                self._sync_to_model()
                print(f"Updated element text: {new_text}")
                return True
        
        # Update in text elements (original PDF data)
        for element in self.text_elements:
            if element['id'] == element_id:
                element['text'] = new_text
                return True
        
        return False
    
    def update_element_font_size(self, element_id, new_font_size):
        """Update font size of an element
        
        Args:
            element_id: ID of the element to update
            new_font_size: New font size
            
        Returns:
            bool: True if successful
        """
        # Update in memory elements
        for element in self.memory_elements:
            if element['id'] == element_id:
                element['font_size'] = new_font_size
                self.is_dirty = True
                self.update()
                # Sync changes to model
                self._sync_to_model()
                print(f"Updated element font size: {new_font_size}")
                return True
        
        return True
    
    def get_element_by_id(self, element_id):
        """Get element by ID
        
        Args:
            element_id: ID of the element
            
        Returns:
            dict: Element data or None
        """
        for element in self.memory_elements:
            if element['id'] == element_id:
                return element
        return None
    
    def update_pdf_element(self, element):
        """Update element in PDF"""
        # This is a placeholder for actual PDF text updating
        # In a real implementation, we would:
        # 1. Remove the old text
        # 2. Add new text with updated size and position
        # 3. Save the PDF
        print(f"Updating PDF element: {element['text']}")
        # TODO: Implement actual PDF text updating using PyMuPDF
    
    def _sync_to_model(self):
        """Sync changes from memory_elements back to PageModel"""
        if not self.page_model or not PageModel:
            return
        
        # Update existing elements or add new ones
        for old_elem in self.memory_elements:
            elem_id = old_elem['id']
            
            # Find existing element in model
            existing_elem = None
            for elem in self.page_model.elements:
                if elem.id == elem_id:
                    existing_elem = elem
                    break
            
            if existing_elem:
                # Update existing element
                existing_elem.content = old_elem['text']
                existing_elem.x = old_elem['x']
                existing_elem.y = old_elem['y']
                existing_elem.width = old_elem['width']
                existing_elem.height = old_elem['height']
                existing_elem.font_size = old_elem['font_size']
                existing_elem.font_family = old_elem.get('font_family', 'Noto Sans SC')
                existing_elem.rotation = old_elem.get('rotation', 0)
                existing_elem.dirty = True
            else:
                # Add new element
                new_elem = ElementModel(
                    id=elem_id,
                    type=old_elem['type'],
                    content=old_elem['text'],
                    x=old_elem['x'],
                    y=old_elem['y'],
                    width=old_elem['width'],
                    height=old_elem['height'],
                    font_size=old_elem['font_size'],
                    font_family=old_elem.get('font_family', 'Noto Sans SC'),
                    rotation=old_elem.get('rotation', 0),
                    dirty=True
                )
                self.page_model.add_element(new_elem)
        
        # Mark page as dirty
        self.page_model.dirty = True
    
    def save_changes(self):
        """Save changes to PDF file"""
        if not self.is_dirty:
            print("No changes to save")
            return True
        
        try:
            # Sync changes to model first
            self._sync_to_model()
            
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
        # If we were dragging an element, print debug info
        if self.is_dragging_element and self.selected_element and self.element_start_pos:
            element = self.selected_element
            old_x, old_y = self.element_start_pos
            new_x, new_y = element['x'], element['y']
            
            # Collect unique IDs to check for duplicates
            unique_ids = set()
            duplicate_found = False
            for elem in self.memory_elements:
                if elem['id'] in unique_ids:
                    duplicate_found = True
                    break
                unique_ids.add(elem['id'])
            
            print("=== 拖动结束调试信息 ===")
            print(f"移动对象 id={element['id']}")
            print(f"原位置=({old_x:.2f}, {old_y:.2f})")
            print(f"新位置=({new_x:.2f}, {new_y:.2f})")
            print(f"对象总数={len(self.memory_elements)}")
            print(f"唯一ID={sorted(list(unique_ids))}")
            print(f"发现重复={duplicate_found}")
            if duplicate_found:
                print("警告: 发现重复对象ID！")
            print("===========================")
        
        self.drag_handle = None
        self.drag_start_pos = None
        self.is_dragging_element = False
        self.element_start_pos = None
        
        # Sync changes to model after drag
        if self.is_dirty:
            self._sync_to_model()
            print("Synced position changes to model")
    
    def update_cursor(self, pos):
        """Update cursor based on position"""
        # Check if hovering over a handle
        handle = self.get_handle_at(pos)
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
        element = self.get_element_at(pos)
        if element:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
    
    def set_scale(self, scale):
        """Set zoom scale"""
        self.scale = scale
        self.update()
    
    def bring_to_front(self):
        """Bring selected element to front"""
        if not self.selected_element:
            return
        
        # Find the element in memory_elements
        index = -1
        for i, elem in enumerate(self.memory_elements):
            if elem['id'] == self.selected_element['id']:
                index = i
                break
        
        if index != -1 and index < len(self.memory_elements) - 1:
            # Move to end (front)
            self.memory_elements.append(self.memory_elements.pop(index))
            self.is_dirty = True
            self.update()
            print(f"元素 {self.selected_element['id']} 移到顶部")
    
    def send_to_back(self):
        """Send selected element to back"""
        if not self.selected_element:
            return
        
        # Find the element in memory_elements
        index = -1
        for i, elem in enumerate(self.memory_elements):
            if elem['id'] == self.selected_element['id']:
                index = i
                break
        
        if index != -1 and index > 0:
            # Move to beginning (back)
            self.memory_elements.insert(0, self.memory_elements.pop(index))
            self.is_dirty = True
            self.update()
            print(f"元素 {self.selected_element['id']} 移到底部")
    
    def bring_forward(self):
        """Bring selected element forward"""
        if not self.selected_element:
            return
        
        # Find the element in memory_elements
        index = -1
        for i, elem in enumerate(self.memory_elements):
            if elem['id'] == self.selected_element['id']:
                index = i
                break
        
        if index != -1 and index < len(self.memory_elements) - 1:
            # Swap with next element
            self.memory_elements[index], self.memory_elements[index + 1] = (
                self.memory_elements[index + 1], self.memory_elements[index]
            )
            self.is_dirty = True
            self.update()
            print(f"元素 {self.selected_element['id']} 上移")
    
    def send_backward(self):
        """Send selected element backward"""
        if not self.selected_element:
            return
        
        # Find the element in memory_elements
        index = -1
        for i, elem in enumerate(self.memory_elements):
            if elem['id'] == self.selected_element['id']:
                index = i
                break
        
        if index != -1 and index > 0:
            # Swap with previous element
            self.memory_elements[index], self.memory_elements[index - 1] = (
                self.memory_elements[index - 1], self.memory_elements[index]
            )
            self.is_dirty = True
            self.update()
            print(f"元素 {self.selected_element['id']} 下移")
    
    def add_layer(self, layer_name):
        """Add a new layer"""
        layer_id = f'layer_{len(self.layers) + 1}'
        new_layer = {
            'id': layer_id,
            'name': layer_name,
            'visible': True,
            'elements': []
        }
        self.layers.append(new_layer)
        self.current_layer_id = layer_id
        print(f"添加新图层: {layer_name} (ID: {layer_id})")
        return layer_id
    
    def delete_layer(self, layer_id):
        """Delete a layer"""
        if layer_id == 'layer_1':  # Don't delete default layer
            print("不能删除默认图层")
            return False
        
        # Remove elements from the layer and move them to default layer
        for layer in self.layers:
            if layer['id'] == layer_id:
                for elem_id in layer['elements']:
                    # Find and update the element
                    for elem in self.memory_elements:
                        if elem['id'] == elem_id:
                            elem['layer_id'] = 'layer_1'
                            # Add to default layer
                            for default_layer in self.layers:
                                if default_layer['id'] == 'layer_1':
                                    default_layer['elements'].append(elem_id)
                                    break
                # Remove the layer
                self.layers.remove(layer)
                # Set current layer to default if deleted layer was current
                if self.current_layer_id == layer_id:
                    self.current_layer_id = 'layer_1'
                print(f"删除图层: {layer['name']} (ID: {layer_id})")
                return True
        return False
    
    def toggle_layer_visibility(self, layer_id):
        """Toggle layer visibility"""
        for layer in self.layers:
            if layer['id'] == layer_id:
                layer['visible'] = not layer['visible']
                self.update()
                print(f"{'显示' if layer['visible'] else '隐藏'} 图层: {layer['name']}")
                return True
        return False
    
    def move_element_to_layer(self, element_id, target_layer_id):
        """Move element to specified layer"""
        # Find the element
        element = None
        for elem in self.memory_elements:
            if elem['id'] == element_id:
                element = elem
                break
        
        if not element:
            return False
        
        # Remove from current layer
        current_layer_id = element['layer_id']
        for layer in self.layers:
            if layer['id'] == current_layer_id:
                if element_id in layer['elements']:
                    layer['elements'].remove(element_id)
                break
        
        # Add to target layer
        for layer in self.layers:
            if layer['id'] == target_layer_id:
                layer['elements'].append(element_id)
                element['layer_id'] = target_layer_id
                self.is_dirty = True
                self.update()
                print(f"移动元素 {element_id} 到图层: {layer['name']}")
                return True
        return False
    
    def get_layers(self):
        """Get all layers"""
        return self.layers
    
    def get_current_layer_id(self):
        """Get current layer ID"""
        return self.current_layer_id
    
    def set_current_layer(self, layer_id):
        """Set current layer"""
        for layer in self.layers:
            if layer['id'] == layer_id:
                self.current_layer_id = layer_id
                print(f"当前图层设置为: {layer['name']}")
                return True
        return False
    
    def copy_element(self):
        """Copy selected element"""
        if not self.selected_element:
            print("没有选中的元素可以复制")
            return None
        
        # Create a copy of the selected element
        import copy
        copied_element = copy.deepcopy(self.selected_element)
        print(f"已复制元素: {copied_element['text']}")
        return copied_element
    
    def paste_element(self, copied_element):
        """Paste copied element"""
        if not copied_element:
            print("没有可粘贴的元素")
            return False
        
        # Generate new ID for the pasted element
        import uuid
        new_id = f"paste_{str(uuid.uuid4())[:8]}"
        copied_element['id'] = new_id
        
        # Offset position slightly
        copied_element['x'] += 20
        copied_element['y'] += 20
        
        # Add to memory elements
        self.memory_elements.append(copied_element)
        
        # Add to current layer
        for layer in self.layers:
            if layer['id'] == self.current_layer_id:
                layer['elements'].append(new_id)
                break
        
        # Select the pasted element
        self.selected_element = copied_element
        
        # Mark as dirty
        self.is_dirty = True
        self.update()
        
        # Sync to model
        self._sync_to_model()
        
        print(f"已粘贴元素: {copied_element['text']} (新ID: {new_id})")
        return True


class PDFCanvas(QWidget):
    """PDF canvas for interactive editing"""
    
    def __init__(self, parent=None, document_model=None):
        super().__init__(parent)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        
        # Create toolbar
        self.toolbar = QHBoxLayout()
        self.layout.addLayout(self.toolbar)
        
        # Navigation buttons
        self.prev_button = QPushButton("上一页")
        self.prev_button.clicked.connect(self.previous_page)
        self.toolbar.addWidget(self.prev_button)
        
        self.next_button = QPushButton("下一页")
        self.next_button.clicked.connect(self.next_page)
        self.toolbar.addWidget(self.next_button)
        
        self.page_label = QLabel("第 1 页")
        self.toolbar.addWidget(self.page_label)
        
        # Zoom controls
        self.zoom_in_button = QPushButton("放大")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.toolbar.addWidget(self.zoom_in_button)
        
        self.zoom_out_button = QPushButton("缩小")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.toolbar.addWidget(self.zoom_out_button)
        
        # Save project button (保存项目模型)
        self.save_button = QPushButton("保存项目")
        self.save_button.clicked.connect(self.save_changes)
        self.toolbar.addWidget(self.save_button)
        
        # Export PDF button (导出 PDF)
        self.export_pdf_button = QPushButton("导出 PDF")
        self.export_pdf_button.clicked.connect(self.export_pdf)
        self.toolbar.addWidget(self.export_pdf_button)
        
        # Export model button (导出 JSON 模型)
        self.export_model_button = QPushButton("导出模型 JSON")
        self.export_model_button.clicked.connect(self.export_model)
        self.toolbar.addWidget(self.export_model_button)
        
        # Z-order buttons
        self.bring_to_front_button = QPushButton("移到顶部")
        self.bring_to_front_button.clicked.connect(self.bring_to_front)
        self.toolbar.addWidget(self.bring_to_front_button)
        
        self.send_to_back_button = QPushButton("移到底部")
        self.send_to_back_button.clicked.connect(self.send_to_back)
        self.toolbar.addWidget(self.send_to_back_button)
        
        self.bring_forward_button = QPushButton("上移")
        self.bring_forward_button.clicked.connect(self.bring_forward)
        self.toolbar.addWidget(self.bring_forward_button)
        
        self.send_backward_button = QPushButton("下移")
        self.send_backward_button.clicked.connect(self.send_backward)
        self.toolbar.addWidget(self.send_backward_button)
        
        # Scroll area for PDF pages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)
        
        # PDF document
        self.pdf_doc = None
        self.current_page = 0
        self.page_widget = None
        self.zoom_scale = 1.0
        
        # Document model integration
        self.document_model = document_model
    
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
        
        # Get page model for current page if available
        page_model = None
        if self.document_model and PageModel:
            # Try to get page model for current page
            for page in self.document_model.pages:
                if page.number == self.current_page:
                    page_model = page
                    break
        
        # Create new page widget with page model
        self.page_widget = PDFPageWidget(self.pdf_doc, self.current_page, page_model=page_model)
        self.page_widget.set_scale(self.zoom_scale)
        self.scroll_area.setWidget(self.page_widget)
        
        # Demo elements are already synced in PDFPageWidget.__init__
        # No need to sync again here
        
        # Update page label
        self.page_label.setText(f"第 {self.current_page + 1} 页，共 {len(self.pdf_doc)} 页")
    
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
    
    def bring_to_front(self):
        """Bring selected element to front"""
        if self.page_widget:
            self.page_widget.bring_to_front()
    
    def send_to_back(self):
        """Send selected element to back"""
        if self.page_widget:
            self.page_widget.send_to_back()
    
    def bring_forward(self):
        """Bring selected element forward"""
        if self.page_widget:
            self.page_widget.bring_forward()
    
    def send_backward(self):
        """Send selected element backward"""
        if self.page_widget:
            self.page_widget.send_backward()
    
    def copy_element(self):
        """Copy selected element"""
        if self.page_widget:
            return self.page_widget.copy_element()
        return None
    
    def paste_element(self, copied_element):
        """Paste copied element"""
        if self.page_widget:
            return self.page_widget.paste_element(copied_element)
    
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
    
    def export_pdf(self):
        """Export current PDF to a file"""
        from PyQt6.QtWidgets import QMessageBox
        import shutil
        
        if not self.pdf_doc:
            QMessageBox.warning(self, "导出 PDF", "没有可导出的 PDF 文档")
            return False
        
        # Determine current PDF path
        current_pdf_path = os.path.join(os.path.dirname(__file__), '..', '..', 'temp', 'guiLaTeX_edit.pdf')
        current_pdf_path = os.path.abspath(current_pdf_path)
        
        if not os.path.exists(current_pdf_path):
            QMessageBox.warning(self, "导出 PDF", "找不到当前 PDF 文件")
            return False
        
        # Export to a new file
        export_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
        os.makedirs(export_dir, exist_ok=True)
        export_path = os.path.join(export_dir, 'guiLaTeX_export.pdf')
        
        try:
            shutil.copy2(current_pdf_path, export_path)
            print(f"PDF exported to: {export_path}")
            
            QMessageBox.information(self, "导出 PDF", 
                f"PDF 已成功导出到:\n{export_path}")
            return True
        except Exception as e:
            QMessageBox.warning(self, "导出 PDF", f"导出失败:\n{str(e)}")
            return False
    
    def export_model(self):
        """Export model to JSON file"""
        import json
        import os
        
        # Ensure model is synced
        if self.page_widget:
            self.page_widget._sync_to_model()
        
        # Prepare export data
        export_data = []
        if self.document_model:
            for page in self.document_model.pages:
                for element in page.elements:
                    export_data.append({
                        'id': element.id,
                        'content': element.content,
                        'x': element.x,
                        'y': element.y,
                        'fontSize': element.font_size,
                        'selected': False  # Selected status not tracked in model
                    })
        elif self.page_widget and self.page_widget.memory_elements:
            # Fallback: export from memory elements if model not available
            for element in self.page_widget.memory_elements:
                export_data.append({
                    'id': element['id'],
                    'content': element['text'],
                    'x': element['x'],
                    'y': element['y'],
                    'fontSize': element['font_size'],
                    'selected': element == self.page_widget.selected_element
                })
        
        # Save to file (使用相对路径)
        export_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
        os.makedirs(export_dir, exist_ok=True)
        export_path = os.path.join(export_dir, 'guiLaTeX_model_export.json')
        export_path = os.path.abspath(export_path)
        
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"Model exported successfully to: {export_path}")
            
            # Also save a copy to screenshots directory for evidence (使用相对路径)
            screenshots_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'contest_evidence', 'screenshots')
            screenshots_dir = os.path.abspath(screenshots_dir)
            os.makedirs(screenshots_dir, exist_ok=True)
            evidence_path = os.path.join(screenshots_dir, '18_qt_demo_model_export.json')
            
            with open(evidence_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"Evidence saved to: {evidence_path}")
            
            # Show message box for user feedback
            from PyQt6.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("模型导出成功")
            msg.setInformativeText(f"模型数据已导出到:\n{export_path}")
            msg.setWindowTitle("导出成功")
            msg.exec()
            
        except Exception as e:
            print(f"Error exporting model: {e}")
    
    def export_model_to_ir(self):
        """Export Qt model to Export IR format (对齐 ExportCore 设计)
        
        Returns:
            dict: Export IR data structure
        """
        import json
        import os
        
        # Ensure model is synced
        if self.page_widget:
            self.page_widget._sync_to_model()
        
        # Prepare IR data
        ir_data = {
            "elements": []
        }
        
        # Current page number (从1开始)
        page_number = self.current_page + 1
        
        # Collect elements from memory_elements (优先使用内存元素)
        if self.page_widget and self.page_widget.memory_elements:
            for element in self.page_widget.memory_elements:
                # Map Qt element type to IR type
                element_type = element.get('type', 'text')
                # 根据ID推断类型
                ir_type = 'textbox'
                if 'demo_title' in element.get('id', ''):
                    ir_type = 'title'
                elif 'demo_author' in element.get('id', ''):
                    ir_type = 'author'
                elif 'demo_body' in element.get('id', ''):
                    ir_type = 'paragraph'
                elif 'demo_formula' in element.get('id', '') or 'formula' in element.get('id', ''):
                    ir_type = 'equation'
                elif 'demo_image' in element.get('id', ''):
                    ir_type = 'image'
                
                # Get layer information
                layer_id = element.get('layer_id', 'layer_1')
                # 从layer_id提取layer编号
                layer_number = 1
                if layer_id.startswith('layer_'):
                    try:
                        layer_number = int(layer_id.split('_')[1])
                    except (IndexError, ValueError):
                        pass
                
                # 层级规则：数值越大，层级越高
                ir_layer = 10 - layer_number
                
                # Get font family and split into zh/en
                font_family = element.get('font_family', 'Noto Sans SC')
                font_family_zh = None
                font_family_en = None
                
                # 简单规则：中文字体优先给 zh，英文优先给 en
                if 'SC' in font_family or 'Han' in font_family or 'Noto Sans SC' in font_family:
                    font_family_zh = font_family
                    font_family_en = 'Inter'
                else:
                    font_family_en = font_family
                    font_family_zh = 'Noto Sans SC'
                
                # Build IR element
                ir_element = {
                    "id": element.get('id', ''),
                    "type": ir_type,
                    "content": element.get('text', ''),
                    "page": page_number,
                    "x": element.get('x', 0),
                    "y": element.get('y', 0),
                    "width": element.get('width', 0),
                    "height": element.get('height', 0),
                    "rotation": element.get('rotation', 0),
                    "layer": ir_layer,
                    "font_family_zh": font_family_zh,
                    "font_family_en": font_family_en,
                    "font_size": element.get('font_size', 12),
                    "color": "#000000",
                    "alignment": "left",
                    "visible": True
                }
                
                ir_data["elements"].append(ir_element)
        
        # Save IR to file
        export_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
        os.makedirs(export_dir, exist_ok=True)
        ir_path = os.path.join(export_dir, 'guiLaTeX_export_ir.json')
        ir_path = os.path.abspath(ir_path)
        
        try:
            with open(ir_path, 'w', encoding='utf-8') as f:
                json.dump(ir_data, f, indent=2, ensure_ascii=False)
            
            print(f"Export IR saved successfully to: {ir_path}")
            return ir_data
            
        except Exception as e:
            print(f"Error exporting IR: {e}")
            return None

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
