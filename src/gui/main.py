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

# Add project root and src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules
from latex.engine import LaTeXEngine, LaTeXGenerator
from latex.pdf_reconstructor import PDFToLaTeXConverter
from gui.properties import PropertyPanel
from gui.pdf_canvas import PDFCanvas

# Import model layer
try:
    from model import DocumentModel, PageModel, ElementModel
except ImportError:
    # Fallback: model layer not available
    DocumentModel = None
    PageModel = None
    ElementModel = None


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
        
        # Create document model (source of truth)
        self.document_model = None
        if DocumentModel:
            self.document_model = DocumentModel(title='guiLaTeX Document')
            print("DocumentModel created successfully")
        else:
            print("Warning: DocumentModel not available, falling back to old path")
        
        # Create PDF canvas (now the main visual editor)
        self.pdf_canvas = PDFCanvas(document_model=self.document_model)
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
        self.pdf_to_latex_converter = PDFToLaTeXConverter()
        
        # Create initial PDF document
        self.create_initial_pdf()
        
        # Connect PDF canvas events to property panel
        self.connect_pdf_canvas_events()
        
    def create_menu_bar(self):
        """Create menu bar"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        open_project_action = QAction("打开项目", self)
        open_project_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_project_action)
        
        save_project_action = QAction("保存项目", self)
        save_project_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_project_action)
        
        file_menu.addSeparator()
        
        export_pdf_action = QAction("导出 PDF", self)
        export_pdf_action.setShortcut("Ctrl+E")
        export_pdf_action.triggered.connect(self.export_document)
        file_menu.addAction(export_pdf_action)
        
        export_model_json_action = QAction("导出模型 JSON", self)
        file_menu.addAction(export_model_json_action)
        
        export_ir_action = QAction("导出 IR", self)
        export_ir_action.setShortcut("Ctrl+Shift+E")
        export_ir_action.triggered.connect(self.export_ir)
        file_menu.addAction(export_ir_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        copy_action = QAction("复制", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_element)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("粘贴", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste_element)
        edit_menu.addAction(paste_action)
        
        delete_action = QAction("删除", self)
        delete_action.setShortcut("Del")
        edit_menu.addAction(delete_action)
        
        # 排列菜单
        arrange_menu = menu_bar.addMenu("排列")
        
        move_up_action = QAction("上移", self)
        arrange_menu.addAction(move_up_action)
        
        move_down_action = QAction("下移", self)
        arrange_menu.addAction(move_down_action)
        
        move_to_top_action = QAction("移到顶部", self)
        arrange_menu.addAction(move_to_top_action)
        
        move_to_bottom_action = QAction("移到底部", self)
        arrange_menu.addAction(move_to_bottom_action)
        
        layer_to_integer_action = QAction("图层编号变整数", self)
        arrange_menu.addAction(layer_to_integer_action)
        
        # 变换菜单
        transform_menu = menu_bar.addMenu("变换")
        
        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        
        zoom_in_action = QAction("放大", self)
        zoom_in_action.setShortcut("Ctrl++")
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("缩小", self)
        zoom_out_action.setShortcut("Ctrl+-")
        view_menu.addAction(zoom_out_action)
        
        reset_view_action = QAction("重置视图", self)
        view_menu.addAction(reset_view_action)
        
        show_debug_action = QAction("显示调试", self)
        view_menu.addAction(show_debug_action)
    

    
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

\section{Introduction}

This is a test document created with guiLaTeX.

You can select this text and edit it in the property panel.

\section{Math Example}

$E = mc^2$

This is another paragraph that you can edit.

\section{Instructions}

1. Click on any text to select it
2. Edit the text in the property panel
3. Watch the changes update immediately
4. The changes are synchronized to the model
\end{document}
"""
        
        # Create PDF
        success = self.pdf_canvas.create_pdf(initial_latex)
        if success:
            # Update LaTeX view
            self.latex_view.setText(initial_latex)
            print("Initial PDF created successfully")
            # 模型同步已在 pdf_canvas.create_pdf -> update_page_display -> PDFPageWidget.__init__ 中完成
            # 不再需要手动添加元素，避免 duplication 问题
        else:
            print("Failed to create initial PDF")
    
    def connect_pdf_canvas_events(self):
        """Connect PDF canvas events to property panel"""
        if self.pdf_canvas.page_widget:
            # Connect element selection to property panel
            self.pdf_canvas.page_widget.element_selected.connect(self.on_element_selected)
            
            # Connect property changes back to PDF canvas
            self.property_panel.element_changed.connect(self.on_property_changed)
    
    def on_element_selected(self, element):
        """Handle element selection from PDF canvas"""
        self.property_panel.set_element(element)
        print(f"Element selected: {element.get('text', 'Unknown')}")
    
    def on_property_changed(self, element_id, property_name, value):
        """Handle property changes from property panel"""
        if self.pdf_canvas.page_widget:
            # Update text content
            if property_name == 'text':
                self.pdf_canvas.page_widget.update_element_text(element_id, value)
            # Update font size
            elif property_name == 'font_size':
                self.pdf_canvas.page_widget.update_element_font_size(element_id, value)
            # Update font family zh
            elif property_name == 'font_family_zh':
                element = self.pdf_canvas.page_widget.get_element_by_id(element_id)
                if element:
                    element['font_family_zh'] = value
                    self.pdf_canvas.page_widget.is_dirty = True
                    self.pdf_canvas.page_widget.update()
                    self.pdf_canvas.page_widget._sync_to_model()
                    print(f"Updated element font family zh: {value}")
            # Update font family en
            elif property_name == 'font_family_en':
                element = self.pdf_canvas.page_widget.get_element_by_id(element_id)
                if element:
                    element['font_family_en'] = value
                    self.pdf_canvas.page_widget.is_dirty = True
                    self.pdf_canvas.page_widget.update()
                    self.pdf_canvas.page_widget._sync_to_model()
                    print(f"Updated element font family en: {value}")
            # Update position
            elif property_name == 'position':
                x, y = value
                element = self.pdf_canvas.page_widget.get_element_by_id(element_id)
                if element:
                    element['x'] = x
                    element['y'] = y
                    self.pdf_canvas.page_widget.update()
            # Update geometry
            elif property_name == 'geometry':
                width, height = value
                element = self.pdf_canvas.page_widget.get_element_by_id(element_id)
                if element:
                    element['width'] = width
                    element['height'] = height
                    self.pdf_canvas.page_widget.is_dirty = True
                    self.pdf_canvas.page_widget.update()
                    self.pdf_canvas.page_widget._sync_to_model()
                    print(f"Updated element geometry: {width}x{height}")
            # Update rotation
            elif property_name == 'rotation':
                element = self.pdf_canvas.page_widget.get_element_by_id(element_id)
                if element:
                    element['rotation'] = value
                    self.pdf_canvas.page_widget.is_dirty = True
                    self.pdf_canvas.page_widget.update()
                    self.pdf_canvas.page_widget._sync_to_model()
                    print(f"Updated element rotation: {value}")
            # Update layer
            elif property_name == 'layer':
                element = self.pdf_canvas.page_widget.get_element_by_id(element_id)
                if element:
                    element['layer'] = value
                    self.pdf_canvas.page_widget.is_dirty = True
                    self.pdf_canvas.page_widget.update()
                    self.pdf_canvas.page_widget._sync_to_model()
                    print(f"Updated element layer: {value}")
            
            # Sync changes to LaTeX view
            self.sync_to_latex()
    
    def sync_to_latex(self):
        """Sync PDF canvas changes to LaTeX code view"""
        if self.pdf_canvas.page_widget and self.pdf_to_latex_converter:
            # Get memory elements from PDF canvas
            memory_elements = self.pdf_canvas.page_widget.memory_elements
            
            # Convert to LaTeX
            latex_code = self.pdf_to_latex_converter.convert_memory_elements(memory_elements)
            
            # Update LaTeX view
            self.latex_view.setText(latex_code)
            print("Synced changes to LaTeX view")
    
    def export_document(self):
        """Export document"""
        if not self.pdf_canvas.page_widget:
            QMessageBox.warning(self, "Export", "No document to export")
            return
        
        # Get LaTeX code from current state
        memory_elements = self.pdf_canvas.page_widget.memory_elements
        latex_code = self.pdf_to_latex_converter.convert_memory_elements(memory_elements)
        
        # Save LaTeX code to file
        export_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
        os.makedirs(export_dir, exist_ok=True)
        latex_path = os.path.join(export_dir, 'guiLaTeX_export.tex')
        
        try:
            with open(latex_path, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            
            # Show success message
            QMessageBox.information(self, "Export", 
                f"Document exported successfully to:\n{latex_path}")
            print(f"Exported LaTeX to: {latex_path}")
        except Exception as e:
            QMessageBox.warning(self, "Export", f"Failed to export document:\n{str(e)}")
    
    def preview_document(self):
        """Preview document as PDF"""
        # Check if LaTeX engine is available
        if not self.latex_engine.is_available():
            QMessageBox.warning(self, "Preview", "LaTeX engine not found")
            return
        
        # Get PDF path from PDF canvas (使用相对路径)
        pdf_path = os.path.join(os.path.dirname(__file__), '..', '..', 'temp', 'guiLaTeX_edit.pdf')
        pdf_path = os.path.abspath(pdf_path)
        
        if os.path.exists(pdf_path):
            # View PDF
            success = self.latex_engine.view_pdf(pdf_path)
            if success:
                print(f"Previewing PDF: {pdf_path}")
            else:
                QMessageBox.warning(self, "Preview", "Failed to open PDF viewer")
        else:
            QMessageBox.warning(self, "Preview", "No document to preview")
    
    def copy_element(self):
        """Copy selected element"""
        if self.pdf_canvas:
            self.copied_element = self.pdf_canvas.copy_element()
            print("元素已复制到剪贴板")
    
    def paste_element(self):
        """Paste copied element"""
        if self.pdf_canvas and hasattr(self, 'copied_element') and self.copied_element:
            self.pdf_canvas.paste_element(self.copied_element)
            print("元素已粘贴到文档")
    
    def export_ir(self):
        """Export model to Export IR format"""
        if self.pdf_canvas:
            ir_data = self.pdf_canvas.export_model_to_ir()
            if ir_data:
                from PyQt6.QtWidgets import QMessageBox
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("导出 IR 成功")
                msg.setInformativeText("模型已成功导出为 Export IR 格式")
                msg.setWindowTitle("导出成功")
                msg.exec()
            else:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "导出 IR", "导出 IR 失败")


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
