#!/usr/bin/env python3
"""
guiLaTeX - Property Panel Component

Property panel for editing element properties
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QComboBox,
    QSpinBox, QPushButton, QColorDialog, QFormLayout, QLineEdit
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, pyqtSignal


class PropertyPanel(QWidget):
    """Property panel for editing element properties"""
    
    # Signals
    element_changed = pyqtSignal(str, str, object)  # element_id, property_name, value
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(250)
        self.setMaximumWidth(300)
        self.current_element = None
        
        # Create layout
        self.layout = QVBoxLayout(self)
        
        # Create property groups
        self.create_font_group()
        self.create_text_group()
        self.create_position_group()
        
        # Add stretch
        self.layout.addStretch()
    
    def create_font_group(self):
        """Create font property group"""
        font_group = QGroupBox("Font")
        font_layout = QFormLayout()
        
        # Font family - 只保留开源/免费可商用字体
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems([
            "Noto Sans SC",      # Google Noto Sans 简体中文（开源，可商用）
            "Source Han Sans SC", # Adobe 思源黑体（开源，可商用）
            "Inter",            # Inter 字体（开源，可商用）
            "Noto Sans",        # Google Noto Sans（开源，可商用）
            "Sans Serif"        # 系统无衬线字体（安全备选）
        ])
        self.font_family_combo.currentTextChanged.connect(self.on_font_family_changed)
        font_layout.addRow("Family:", self.font_family_combo)
        
        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.valueChanged.connect(self.on_font_size_changed)
        font_layout.addRow("Size:", self.font_size_spin)
        
        # Font color
        self.color_button = QPushButton("Color")
        self.color_button.clicked.connect(self.on_color_clicked)
        font_layout.addRow("Color:", self.color_button)
        
        font_group.setLayout(font_layout)
        self.layout.addWidget(font_group)
    
    def create_text_group(self):
        """Create text property group"""
        text_group = QGroupBox("Text")
        text_layout = QFormLayout()
        
        # Text content
        self.text_edit = QLineEdit()
        self.text_edit.textChanged.connect(self.on_text_changed)
        text_layout.addRow("Content:", self.text_edit)
        
        text_group.setLayout(text_layout)
        self.layout.addWidget(text_group)
    
    def create_position_group(self):
        """Create position property group"""
        position_group = QGroupBox("Position")
        position_layout = QFormLayout()
        
        # X position
        self.x_spin = QSpinBox()
        self.x_spin.setRange(-1000, 10000)
        self.x_spin.valueChanged.connect(self.on_position_changed)
        position_layout.addRow("X:", self.x_spin)
        
        # Y position
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-1000, 10000)
        self.y_spin.valueChanged.connect(self.on_position_changed)
        position_layout.addRow("Y:", self.y_spin)
        
        # Rotation angle
        self.rotation_spin = QSpinBox()
        self.rotation_spin.setRange(-360, 360)
        self.rotation_spin.setSuffix("°")
        self.rotation_spin.valueChanged.connect(self.on_rotation_changed)
        position_layout.addRow("Rotation:", self.rotation_spin)
        
        position_group.setLayout(position_layout)
        self.layout.addWidget(position_group)
    
    def set_element(self, element):
        """Set current element to edit
        
        Args:
            element: LaTeXElement object or dict (for PDF elements)
        """
        self.current_element = element
        self.update_properties()
    
    def update_properties(self):
        """Update property fields based on current element"""
        if not self.current_element:
            # Clear fields if no element selected
            self.font_family_combo.setCurrentText("Noto Sans SC")
            self.font_size_spin.setValue(12)
            self.text_edit.setText("")
            self.x_spin.setValue(0)
            self.y_spin.setValue(0)
            self.rotation_spin.setValue(0)
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            # Update font properties
            font_size = self.current_element.get('font_size', 12)
            self.font_size_spin.setValue(int(font_size))
            
            # Update font family
            font_family = self.current_element.get('font_family', 'Noto Sans SC')
            # Find the index of the font family in the combo box
            index = self.font_family_combo.findText(font_family)
            if index != -1:
                self.font_family_combo.setCurrentIndex(index)
            else:
                # If font family not found, set to first item
                self.font_family_combo.setCurrentIndex(0)
            
            # Update text content
            text = self.current_element.get('text', '')
            self.text_edit.setText(text)
            
            # Update position
            x = self.current_element.get('x', 0)
            y = self.current_element.get('y', 0)
            self.x_spin.setValue(int(x))
            self.y_spin.setValue(int(y))
            
            # Update rotation
            rotation = self.current_element.get('rotation', 0)
            self.rotation_spin.setValue(int(rotation))
        else:
            # Handle QGraphicsItem-style elements (legacy)
            # Update font properties
            if hasattr(self.current_element, 'font'):
                font_family = self.current_element.font.family()
                if font_family in [self.font_family_combo.itemText(i) for i in range(self.font_family_combo.count())]:
                    self.font_family_combo.setCurrentText(font_family)
                self.font_size_spin.setValue(int(self.current_element.font.pointSize()))
            
            # Update text content
            if hasattr(self.current_element, 'text'):
                self.text_edit.setText(self.current_element.text)
            
            # Update position
            pos = self.current_element.pos()
            self.x_spin.setValue(int(pos.x()))
            self.y_spin.setValue(int(pos.y()))
            
            # Update rotation
            if hasattr(self.current_element, 'rotation'):
                rotation = self.current_element.rotation()
                self.rotation_spin.setValue(int(rotation))
            else:
                self.rotation_spin.setValue(0)
    
    def on_font_family_changed(self, family):
        """Handle font family change"""
        if not self.current_element:
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                # Add font family to element data
                self.current_element['font_family'] = family
                self.element_changed.emit(element_id, 'font_family', family)
        elif hasattr(self.current_element, 'font'):
            self.current_element.font.setFamily(family)
            self.current_element.update()
    
    def on_font_size_changed(self, size):
        """Handle font size change"""
        if not self.current_element:
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                self.current_element['font_size'] = size
                self.element_changed.emit(element_id, 'font_size', size)
        elif hasattr(self.current_element, 'font'):
            self.current_element.font.setPointSize(size)
            self.current_element.update()
    
    def on_color_clicked(self):
        """Handle color button click"""
        if not self.current_element:
            return
        
        # Get current color
        if isinstance(self.current_element, dict):
            current_color = QColor(0, 0, 0)
        else:
            current_color = self.current_element.color if hasattr(self.current_element, 'color') else QColor(0, 0, 0)
        
        # Use non-native dialog to avoid initialization issues on macOS
        color_dialog = QColorDialog(current_color, self)
        color_dialog.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
        color_dialog.setWindowTitle("Select Color")
        
        if color_dialog.exec() == QColorDialog.DialogCode.Accepted:
            color = color_dialog.selectedColor()
            if color.isValid():
                if not isinstance(self.current_element, dict):
                    self.current_element.color = color
                    self.current_element.update()
    
    def on_text_changed(self, text):
        """Handle text content change"""
        if not self.current_element:
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                self.current_element['text'] = text
                self.element_changed.emit(element_id, 'text', text)
        elif hasattr(self.current_element, 'text'):
            self.current_element.text = text
            self.current_element.update()
    
    def on_position_changed(self, value):
        """Handle position change"""
        if not self.current_element:
            return
        
        # Get new position
        x = self.x_spin.value()
        y = self.y_spin.value()
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                self.current_element['x'] = x
                self.current_element['y'] = y
                self.element_changed.emit(element_id, 'position', (x, y))
        else:
            # Set position for QGraphicsItem
            self.current_element.setPos(x, y)
    
    def on_rotation_changed(self, value):
        """Handle rotation change"""
        if not self.current_element:
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                self.current_element['rotation'] = value
                self.element_changed.emit(element_id, 'rotation', value)
        else:
            # Set rotation for QGraphicsItem if available
            if hasattr(self.current_element, 'setRotation'):
                self.current_element.setRotation(value)
