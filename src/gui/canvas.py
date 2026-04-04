#!/usr/bin/env python3
"""
guiLaTeX - Canvas Component

Visual canvas for LaTeX element rendering and manipulation
"""

from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsLineItem
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt6.QtCore import Qt, QRectF, QPointF


class LaTeXElement(QGraphicsItem):
    """Base class for all LaTeX elements"""
    
    def __init__(self, x=0, y=0, width=100, height=50):
        super().__init__()
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
                     QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
                     QGraphicsItem.GraphicsItemFlag.ItemIsFocusable |
                     QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges |
                     QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges)
        self.setPos(x, y)
        self.width = width
        self.height = height
        self.text = "LaTeX Element"
        self.font = QFont("Arial", 12)
        self.color = QColor(0, 0, 0)
        self.rotation = 0
        self.scale = 1.0
        
        # Resize and rotation handles
        self.handle_size = 8
        self.resize_handles = [
            (0, 0), (0.5, 0), (1, 0),  # Top left, top center, top right
            (1, 0.5),  # Right center
            (1, 1), (0.5, 1), (0, 1),  # Bottom right, bottom center, bottom left
            (0, 0.5)   # Left center
        ]
        self.rotation_handle = (0.5, -0.1)  # Above the top center
        
        # Mouse interaction
        self.drag_start_pos = None
        self.drag_handle = None
    
    def boundingRect(self):
        """Return bounding rectangle"""
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter, option, widget):
        """Paint the element"""
        # Draw background
        painter.setBrush(QBrush(QColor(240, 240, 240, 100)))
        painter.drawRect(self.boundingRect())
        
        # Draw border
        if self.isSelected():
            painter.setPen(QPen(QColor(0, 120, 215), 2, Qt.PenStyle.DashLine))
        else:
            painter.setPen(QPen(QColor(200, 200, 200), 1))
        painter.drawRect(self.boundingRect())
        
        # Draw text
        painter.setPen(QPen(self.color))
        painter.setFont(self.font)
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter, self.text)
        
        # Draw resize and rotation handles if selected
        if self.isSelected():
            self.draw_handles(painter)
    
    def draw_handles(self, painter):
        """Draw resize and rotation handles"""
        painter.setBrush(QBrush(QColor(0, 120, 215)))
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        
        # Draw resize handles
        for handle in self.resize_handles:
            x = handle[0] * self.width
            y = handle[1] * self.height
            rect = QRectF(
                x - self.handle_size / 2, 
                y - self.handle_size / 2, 
                self.handle_size, 
                self.handle_size
            )
            painter.drawRect(rect)
        
        # Draw rotation handle
        x = self.rotation_handle[0] * self.width
        y = self.rotation_handle[1] * self.height
        rect = QRectF(
            x - self.handle_size / 2, 
            y - self.handle_size / 2, 
            self.handle_size, 
            self.handle_size
        )
        painter.setBrush(QBrush(QColor(255, 165, 0)))
        painter.drawRect(rect)
    
    def get_handle_at(self, pos):
        """Get handle at position"""
        # Check resize handles
        for i, handle in enumerate(self.resize_handles):
            x = handle[0] * self.width
            y = handle[1] * self.height
            rect = QRectF(
                x - self.handle_size / 2, 
                y - self.handle_size / 2, 
                self.handle_size, 
                self.handle_size
            )
            if rect.contains(pos):
                return f"resize_{i}"
        
        # Check rotation handle
        x = self.rotation_handle[0] * self.width
        y = self.rotation_handle[1] * self.height
        rect = QRectF(
            x - self.handle_size / 2, 
            y - self.handle_size / 2, 
            self.handle_size, 
            self.handle_size
        )
        if rect.contains(pos):
            return "rotate"
        
        return None
    
    def hoverEnterEvent(self, event):
        """Handle hover enter event"""
        pos = event.pos()
        handle = self.get_handle_at(pos)
        if handle:
            if handle == "rotate":
                self.setCursor(Qt.CursorShape.SizeAllCursor)
            elif handle.startswith("resize_"):
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
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverEnterEvent(event)
    
    def hoverMoveEvent(self, event):
        """Handle hover move event"""
        pos = event.pos()
        handle = self.get_handle_at(pos)
        if handle:
            if handle == "rotate":
                self.setCursor(Qt.CursorShape.SizeAllCursor)
            elif handle.startswith("resize_"):
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
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverMoveEvent(event)
    
    def hoverLeaveEvent(self, event):
        """Handle hover leave event"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverLeaveEvent(event)
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        pos = event.pos()
        self.drag_handle = self.get_handle_at(pos)
        if self.drag_handle:
            self.drag_start_pos = pos
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move event"""
        if self.drag_handle:
            pos = event.pos()
            if self.drag_start_pos:
                dx = pos.x() - self.drag_start_pos.x()
                dy = pos.y() - self.drag_start_pos.y()
                
                if self.drag_handle == "rotate":
                    # Calculate rotation angle
                    center = QPointF(self.width / 2, self.height / 2)
                    start_vector = self.drag_start_pos - center
                    current_vector = pos - center
                    
                    # Calculate angle difference in degrees
                    start_angle = start_vector.angle()
                    current_angle = current_vector.angle()
                    angle_diff = (current_angle - start_angle) % 360
                    
                    # Update rotation
                    self.rotation = (self.rotation + angle_diff) % 360
                    self.setRotation(self.rotation)
                    self.update()
                    self.scene().update()  # Force scene update
                elif self.drag_handle.startswith("resize_"):
                    # Handle resize
                    handle_idx = int(self.drag_handle.split("_")[1])
                    handle = self.resize_handles[handle_idx]
                    
                    # Get current position and size
                    current_pos = self.pos()
                    
                    # Calculate new width and height based on mouse position
                    if handle[0] == 1:  # Right side
                        new_width = max(20, pos.x())
                    elif handle[0] == 0:  # Left side
                        new_width = max(20, self.width - (pos.x() - self.drag_start_pos.x()))
                        # Adjust position when resizing from left
                        new_x = current_pos.x() + (pos.x() - self.drag_start_pos.x())
                        self.setPos(new_x, current_pos.y())
                    else:
                        new_width = self.width
                    
                    if handle[1] == 1:  # Bottom side
                        new_height = max(20, pos.y())
                    elif handle[1] == 0:  # Top side
                        new_height = max(20, self.height - (pos.y() - self.drag_start_pos.y()))
                        # Adjust position when resizing from top
                        new_y = current_pos.y() + (pos.y() - self.drag_start_pos.y())
                        self.setPos(current_pos.x(), new_y)
                    else:
                        new_height = self.height
                    
                    # Update size
                    self.width = new_width
                    self.height = new_height
                    self.update()
                    self.scene().update()  # Force scene update
                    
            self.drag_start_pos = pos
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release event"""
        self.drag_handle = None
        self.drag_start_pos = None
        super().mouseReleaseEvent(event)


class TextElement(LaTeXElement):
    """Text element"""
    
    def __init__(self, x=0, y=0, width=200, height=60):
        super().__init__(x, y, width, height)
        self.text = "Sample Text"
        self.font = QFont("Times New Roman", 14)


class MathElement(LaTeXElement):
    """Math formula element"""
    
    def __init__(self, x=0, y=0, width=150, height=80):
        super().__init__(x, y, width, height)
        self.text = "$E = mc^2$"
        self.font = QFont("Cambria Math", 16)


class Canvas(QGraphicsView):
    """Visual canvas for LaTeX elements"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Page settings
        self.page_width = 800
        self.page_height = 600
        self.current_page = 0
        self.pages = []  # List of scenes for each page
        
        # Create first page
        self.add_page()
        
        # Set view properties
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        # Add sample elements to first page
        self.add_sample_elements()
        
        # Selection state
        self.selected_items = []
        
        # Enable rubber band selection
        self.rubber_band = None
        self.rubber_band_start = None
    
    def add_page(self):
        """Add a new page"""
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, self.page_width, self.page_height)
        self.pages.append(scene)
        self.setScene(scene)
        self.current_page = len(self.pages) - 1
        self.draw_grid()
    
    def switch_page(self, page_index):
        """Switch to a specific page"""
        if 0 <= page_index < len(self.pages):
            self.setScene(self.pages[page_index])
            self.current_page = page_index
    
    def get_current_page(self):
        """Get current page scene"""
        return self.pages[self.current_page]
    
    def get_page_count(self):
        """Get number of pages"""
        return len(self.pages)
    
    def draw_grid(self):
        """Draw grid background"""
        grid_size = 20
        scene = self.get_current_page()
        scene_rect = scene.sceneRect()
        
        # Clear existing grid lines
        for item in scene.items():
            if hasattr(item, 'type') and item.type() == QGraphicsLineItem.Type:
                scene.removeItem(item)
        
        # Draw horizontal lines
        for y in range(0, int(scene_rect.height()), grid_size):
            scene.addLine(0, y, scene_rect.width(), y, QPen(QColor(220, 220, 220), 0.5, Qt.PenStyle.DashLine))
        
        # Draw vertical lines
        for x in range(0, int(scene_rect.width()), grid_size):
            scene.addLine(x, 0, x, scene_rect.height(), QPen(QColor(220, 220, 220), 0.5, Qt.PenStyle.DashLine))
    
    def add_sample_elements(self):
        """Add sample elements to canvas"""
        scene = self.get_current_page()
        # Add text element
        text_element = TextElement(100, 100)
        scene.addItem(text_element)
        
        # Add math element
        math_element = MathElement(350, 100)
        scene.addItem(math_element)
    
    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        # Adjust scene size based on view size
        view_rect = self.viewport().rect()
        scene = self.get_current_page()
        scene.setSceneRect(0, 0, view_rect.width(), view_rect.height())
        self.draw_grid()
    
    def mousePressEvent(self, event):
        """Handle mouse press event"""
        # Get scene position
        scene_pos = self.mapToScene(event.position().toPoint())
        
        # Handle right click
        if event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.position().toPoint())
            return
        
        # Handle left click
        if event.button() == Qt.MouseButton.LeftButton:
            # Deselect all if clicking on empty space
            item = self.itemAt(event.position().toPoint())
            if not item:
                self.deselect_all()
            
            # Start rubber band selection if Ctrl is pressed
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.rubber_band_start = event.position().toPoint()
                return
        
        super().mousePressEvent(event)
        
        # Update selected items
        self.update_selected_items()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move event"""
        # Handle rubber band selection
        if self.rubber_band_start:
            # TODO: Implement rubber band drawing
            pass
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release event"""
        # End rubber band selection
        if self.rubber_band_start:
            # TODO: Implement rubber band selection
            self.rubber_band_start = None
        
        super().mouseReleaseEvent(event)
        
        # Update selected items
        self.update_selected_items()
    
    def keyPressEvent(self, event):
        """Handle key press event"""
        # Delete selected items
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.delete_selected_items()
            return
        
        # Copy selected items
        elif event.key() == Qt.Key.Key_C and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.copy_selected_items()
            return
        
        # Paste items
        elif event.key() == Qt.Key.Key_V and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.paste_items()
            return
        
        # Select all
        elif event.key() == Qt.Key.Key_A and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.select_all()
            return
        
        # Group selected items
        elif event.key() == Qt.Key.Key_G and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.group_items()
            return
        
        # Ungroup items
        elif event.key() == Qt.Key.Key_U and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.ungroup_items()
            return
        
        super().keyPressEvent(event)
    
    def update_selected_items(self):
        """Update selected items list"""
        scene = self.get_current_page()
        self.selected_items = [item for item in scene.items() if item.isSelected()]
    
    def deselect_all(self):
        """Deselect all items"""
        scene = self.get_current_page()
        for item in scene.items():
            item.setSelected(False)
        self.selected_items = []
    
    def select_all(self):
        """Select all items"""
        scene = self.get_current_page()
        for item in scene.items():
            if isinstance(item, LaTeXElement):
                item.setSelected(True)
        self.update_selected_items()
    
    def delete_selected_items(self):
        """Delete selected items"""
        scene = self.get_current_page()
        for item in self.selected_items[:]:
            scene.removeItem(item)
        self.selected_items = []
    
    def copy_selected_items(self):
        """Copy selected items"""
        # TODO: Implement copy functionality
        pass
    
    def paste_items(self):
        """Paste items"""
        # TODO: Implement paste functionality
        pass
    
    def group_items(self):
        """Group selected items"""
        # TODO: Implement group functionality
        pass
    
    def ungroup_items(self):
        """Ungroup items"""
        # TODO: Implement ungroup functionality
        pass
    
    def show_context_menu(self, pos):
        """Show context menu"""
        # TODO: Implement context menu
        pass
