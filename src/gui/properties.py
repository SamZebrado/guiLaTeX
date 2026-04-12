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
        self.create_selection_info_group()
        self.create_content_group()
        self.create_geometry_group()
        self.create_font_group()
        self.create_object_specific_group()
        self.create_debug_info_group()
        
        # Add stretch
        self.layout.addStretch()
    
    def create_selection_info_group(self):
        """创建选中信息分组"""
        selection_group = QGroupBox("选中信息")
        selection_layout = QFormLayout()
        
        # 元素类型
        self.type_label = QLabel("无")
        selection_layout.addRow("类型:", self.type_label)
        
        # 元素ID
        self.id_label = QLabel("无")
        selection_layout.addRow("ID:", self.id_label)
        
        selection_group.setLayout(selection_layout)
        self.layout.addWidget(selection_group)
    
    def create_content_group(self):
        """创建内容分组"""
        content_group = QGroupBox("内容")
        content_layout = QFormLayout()
        
        # 文本内容
        self.text_edit = QLineEdit()
        self.text_edit.textChanged.connect(self.on_text_changed)
        content_layout.addRow("正文:", self.text_edit)
        
        content_group.setLayout(content_layout)
        self.layout.addWidget(content_group)
    
    def create_geometry_group(self):
        """创建几何分组"""
        geometry_group = QGroupBox("几何")
        geometry_layout = QFormLayout()
        
        # X 位置
        self.x_spin = QSpinBox()
        self.x_spin.setRange(-1000, 10000)
        self.x_spin.valueChanged.connect(self.on_position_changed)
        geometry_layout.addRow("X:", self.x_spin)
        
        # Y 位置
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-1000, 10000)
        self.y_spin.valueChanged.connect(self.on_position_changed)
        geometry_layout.addRow("Y:", self.y_spin)
        
        # 宽度
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.valueChanged.connect(self.on_geometry_changed)
        geometry_layout.addRow("宽:", self.width_spin)
        
        # 高度
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.valueChanged.connect(self.on_geometry_changed)
        geometry_layout.addRow("高:", self.height_spin)
        
        # 旋转角度
        self.rotation_spin = QSpinBox()
        self.rotation_spin.setRange(-360, 360)
        self.rotation_spin.setSuffix("°")
        self.rotation_spin.valueChanged.connect(self.on_rotation_changed)
        geometry_layout.addRow("旋转:", self.rotation_spin)
        
        # 图层编号
        self.layer_spin = QSpinBox()
        self.layer_spin.setRange(1, 100)
        self.layer_spin.valueChanged.connect(self.on_layer_changed)
        geometry_layout.addRow("图层:", self.layer_spin)
        
        geometry_group.setLayout(geometry_layout)
        self.layout.addWidget(geometry_group)
    
    def create_font_group(self):
        """创建字体分组"""
        font_group = QGroupBox("字体")
        font_layout = QFormLayout()
        
        # 中文字体
        self.font_family_zh_combo = QComboBox()
        self.font_family_zh_combo.addItems([
            "Noto Sans SC",      # Google Noto Sans 简体中文（开源，可商用）
            "Source Han Sans SC", # Adobe 思源黑体（开源，可商用）
            "Sans Serif"        # 系统无衬线字体（安全备选）
        ])
        self.font_family_zh_combo.currentTextChanged.connect(self.on_font_family_zh_changed)
        font_layout.addRow("中文字体:", self.font_family_zh_combo)
        
        # 英文字体
        self.font_family_en_combo = QComboBox()
        self.font_family_en_combo.addItems([
            "Inter",            # Inter 字体（开源，可商用）
            "Noto Sans",        # Google Noto Sans（开源，可商用）
            "Sans Serif"        # 系统无衬线字体（安全备选）
        ])
        self.font_family_en_combo.currentTextChanged.connect(self.on_font_family_en_changed)
        font_layout.addRow("英文字体:", self.font_family_en_combo)
        
        # 字号
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.valueChanged.connect(self.on_font_size_changed)
        font_layout.addRow("字号:", self.font_size_spin)
        
        # 颜色
        self.color_button = QPushButton("颜色")
        self.color_button.clicked.connect(self.on_color_clicked)
        font_layout.addRow("颜色:", self.color_button)
        
        font_group.setLayout(font_layout)
        self.layout.addWidget(font_group)
    
    def create_object_specific_group(self):
        """创建对象专属属性分组"""
        object_group = QGroupBox("对象专属属性")
        object_layout = QFormLayout()
        
        # 这里可以根据不同对象类型添加专属属性
        self.object_specific_label = QLabel("无专属属性")
        object_layout.addRow("", self.object_specific_label)
        
        object_group.setLayout(object_layout)
        self.layout.addWidget(object_group)
    
    def create_debug_info_group(self):
        """创建调试信息分组"""
        debug_group = QGroupBox("调试信息")
        debug_layout = QFormLayout()
        
        # 调试信息
        self.debug_label = QLabel("无调试信息")
        debug_layout.addRow("", self.debug_label)
        
        debug_group.setLayout(debug_layout)
        self.layout.addWidget(debug_group)
    
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
            self.type_label.setText("无")
            self.id_label.setText("无")
            self.text_edit.setText("")
            self.x_spin.setValue(0)
            self.y_spin.setValue(0)
            self.width_spin.setValue(100)
            self.height_spin.setValue(50)
            self.rotation_spin.setValue(0)
            self.layer_spin.setValue(1)
            self.font_family_zh_combo.setCurrentText("Noto Sans SC")
            self.font_family_en_combo.setCurrentText("Inter")
            self.font_size_spin.setValue(12)
            self.object_specific_label.setText("无专属属性")
            self.debug_label.setText("无调试信息")
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            # Update selection info
            element_type = self.current_element.get('type', 'text')
            self.type_label.setText(element_type)
            
            element_id = self.current_element.get('id', '无')
            self.id_label.setText(element_id)
            
            # Update content
            text = self.current_element.get('text', '')
            self.text_edit.setText(text)
            
            # Update geometry
            x = self.current_element.get('x', 0)
            y = self.current_element.get('y', 0)
            width = self.current_element.get('width', 100)
            height = self.current_element.get('height', 50)
            rotation = self.current_element.get('rotation', 0)
            layer = self.current_element.get('layer', 1)
            
            self.x_spin.setValue(int(x))
            self.y_spin.setValue(int(y))
            self.width_spin.setValue(int(width))
            self.height_spin.setValue(int(height))
            self.rotation_spin.setValue(int(rotation))
            self.layer_spin.setValue(int(layer))
            
            # Update font properties
            font_size = self.current_element.get('font_size', 12)
            self.font_size_spin.setValue(int(font_size))
            
            # Update font families
            font_family_zh = self.current_element.get('font_family_zh', 'Noto Sans SC')
            index = self.font_family_zh_combo.findText(font_family_zh)
            if index != -1:
                self.font_family_zh_combo.setCurrentIndex(index)
            else:
                self.font_family_zh_combo.setCurrentIndex(0)
            
            font_family_en = self.current_element.get('font_family_en', 'Inter')
            index = self.font_family_en_combo.findText(font_family_en)
            if index != -1:
                self.font_family_en_combo.setCurrentIndex(index)
            else:
                self.font_family_en_combo.setCurrentIndex(0)
            
            # Update debug info
            debug_info = f"ID: {element_id}\n类型: {element_type}\n位置: ({x}, {y})\n大小: {width}x{height}\n旋转: {rotation}°\n图层: {layer}"
            self.debug_label.setText(debug_info)
        else:
            # Handle QGraphicsItem-style elements (legacy)
            # Update selection info
            self.type_label.setText("图形元素")
            self.id_label.setText("无ID")
            
            # Update content
            if hasattr(self.current_element, 'text'):
                self.text_edit.setText(self.current_element.text)
            else:
                self.text_edit.setText("")
            
            # Update geometry
            pos = self.current_element.pos()
            self.x_spin.setValue(int(pos.x()))
            self.y_spin.setValue(int(pos.y()))
            self.width_spin.setValue(100)
            self.height_spin.setValue(50)
            
            if hasattr(self.current_element, 'rotation'):
                rotation = self.current_element.rotation()
                self.rotation_spin.setValue(int(rotation))
            else:
                self.rotation_spin.setValue(0)
            
            self.layer_spin.setValue(1)
            
            # Update font properties
            if hasattr(self.current_element, 'font'):
                font_family = self.current_element.font.family()
                # Set font families based on detected language
                if 'SC' in font_family or 'Han' in font_family:
                    self.font_family_zh_combo.setCurrentText(font_family)
                    self.font_family_en_combo.setCurrentText("Inter")
                else:
                    self.font_family_zh_combo.setCurrentText("Noto Sans SC")
                    self.font_family_en_combo.setCurrentText(font_family)
                self.font_size_spin.setValue(int(self.current_element.font.pointSize()))
            else:
                self.font_family_zh_combo.setCurrentText("Noto Sans SC")
                self.font_family_en_combo.setCurrentText("Inter")
                self.font_size_spin.setValue(12)
            
            # Update debug info
            debug_info = "图形元素 (传统样式)"
            self.debug_label.setText(debug_info)
    
    def on_font_family_zh_changed(self, family):
        """处理中文字体变化"""
        if not self.current_element:
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                # Add font family to element data
                self.current_element['font_family_zh'] = family
                self.element_changed.emit(element_id, 'font_family_zh', family)
        elif hasattr(self.current_element, 'font'):
            # For legacy elements, update the font family directly
            self.current_element.font.setFamily(family)
            self.current_element.update()
    
    def on_font_family_en_changed(self, family):
        """处理英文字体变化"""
        if not self.current_element:
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                # Add font family to element data
                self.current_element['font_family_en'] = family
                self.element_changed.emit(element_id, 'font_family_en', family)
    
    def on_geometry_changed(self, value):
        """处理几何属性变化"""
        if not self.current_element:
            return
        
        # Get new geometry
        width = self.width_spin.value()
        height = self.height_spin.value()
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                self.current_element['width'] = width
                self.current_element['height'] = height
                self.element_changed.emit(element_id, 'geometry', (width, height))
    
    def on_layer_changed(self, value):
        """处理图层变化"""
        if not self.current_element:
            return
        
        # Handle dict-style PDF elements
        if isinstance(self.current_element, dict):
            element_id = self.current_element.get('id')
            if element_id:
                self.current_element['layer'] = value
                self.element_changed.emit(element_id, 'layer', value)
    
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
