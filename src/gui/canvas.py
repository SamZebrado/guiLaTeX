#!/usr/bin/env python3
"""
guiLaTeX - Canvas Component

Visual canvas for LaTeX element rendering and manipulation
"""

from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
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
        
        # Create scene
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 600)
        self.setScene(self.scene)
        
        # Set view properties
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        # Add grid background
        self.draw_grid()
        
        # Add sample elements
        self.add_sample_elements()
        
        # Selection state
        self.selected_items = []
        
        # Enable rubber band selection
        self.rubber_band = None
        self.rubber_band_start = None
    
    def draw_grid(self):
        """Draw grid background"""
        grid_size = 20
        scene_rect = self.scene.sceneRect()
        
        # Draw horizontal lines
        for y in range(0, int(scene_rect.height()), grid_size):
            self.scene.addLine(0, y, scene_rect.width(), y, QPen(QColor(220, 220, 220), 0.5))
        
        # Draw vertical lines
        for x in range(0, int(scene_rect.width()), grid_size):
            self.scene.addLine(x, 0, x, scene_rect.height(), QPen(QColor(220, 220, 220), 0.5))
    
    def add_sample_elements(self):
        """Add sample elements to canvas"""
        # Add text element
        text_element = TextElement(100, 100)
        self.scene.addItem(text_element)
        
        # Add math element
        math_element = MathElement(350, 100)
        self.scene.addItem(math_element)
    
    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        # Adjust scene size based on view size
        view_rect = self.viewport().rect()
        self.scene.setSceneRect(0, 0, view_rect.width(), view_rect.height())
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
        self.selected_items = [item for item in self.scene.items() if item.isSelected()]
    
    def deselect_all(self):
        """Deselect all items"""
        for item in self.scene.items():
            item.setSelected(False)
        self.selected_items = []
    
    def select_all(self):
        """Select all items"""
        for item in self.scene.items():
            if isinstance(item, LaTeXElement):
                item.setSelected(True)
        self.update_selected_items()
    
    def delete_selected_items(self):
        """Delete selected items"""
        for item in self.selected_items[:]:
            self.scene.removeItem(item)
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
