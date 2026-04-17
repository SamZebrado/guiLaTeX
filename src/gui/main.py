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
        
        export_ir_action = QAction("导出 IR", self)
        export_ir_action.setShortcut("Ctrl+Shift+E")
        export_ir_action.triggered.connect(self.export_ir)
        file_menu.addAction(export_ir_action)
        
        export_latex_action = QAction("导出 LaTeX", self)
        export_latex_action.setShortcut("Ctrl+L")
        export_latex_action.triggered.connect(self.export_latex)
        file_menu.addAction(export_latex_action)
        
        import_latex_action = QAction("导入 LaTeX", self)
        import_latex_action.setShortcut("Ctrl+I")
        import_latex_action.triggered.connect(self.import_latex)
        file_menu.addAction(import_latex_action)
        
        export_pdf_action = QAction("导出 PDF", self)
        export_pdf_action.setShortcut("Ctrl+E")
        export_pdf_action.triggered.connect(self.export_document)
        file_menu.addAction(export_pdf_action)
        
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
        delete_action.triggered.connect(self.delete_element)
        edit_menu.addAction(delete_action)
        
        # 排列菜单
        arrange_menu = menu_bar.addMenu("排列")
        
        move_up_action = QAction("上移", self)
        move_up_action.triggered.connect(self.move_element_up)
        arrange_menu.addAction(move_up_action)
        
        move_down_action = QAction("下移", self)
        move_down_action.triggered.connect(self.move_element_down)
        arrange_menu.addAction(move_down_action)
        
        move_to_top_action = QAction("移到顶部", self)
        move_to_top_action.triggered.connect(self.move_element_to_top)
        arrange_menu.addAction(move_to_top_action)
        
        move_to_bottom_action = QAction("移到底部", self)
        move_to_bottom_action.triggered.connect(self.move_element_to_bottom)
        arrange_menu.addAction(move_to_bottom_action)
        
        # 变换菜单
        transform_menu = menu_bar.addMenu("变换")
        
        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        
        zoom_in_action = QAction("放大", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("缩小", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        reset_view_action = QAction("重置视图", self)
        reset_view_action.triggered.connect(self.reset_view)
        view_menu.addAction(reset_view_action)
    

    
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
    
    def delete_element(self):
        """Delete selected element"""
        if self.pdf_canvas and self.pdf_canvas.page_widget and self.pdf_canvas.page_widget.selected_element:
            element_id = self.pdf_canvas.page_widget.selected_element['id']
            # Remove element from memory_elements
            for i, elem in enumerate(self.pdf_canvas.page_widget.memory_elements):
                if elem['id'] == element_id:
                    self.pdf_canvas.page_widget.memory_elements.pop(i)
                    break
            # Remove from layer
            for layer in self.pdf_canvas.page_widget.layers:
                if element_id in layer['elements']:
                    layer['elements'].remove(element_id)
                    break
            # Clear selection
            self.pdf_canvas.page_widget.selected_element = None
            # Mark as dirty
            self.pdf_canvas.page_widget.is_dirty = True
            # Update view
            self.pdf_canvas.page_widget.update()
            # Sync to model
            self.pdf_canvas.page_widget._sync_to_model()
            print(f"元素 {element_id} 已删除")
    
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
    
    def export_latex(self):
        """Export model to LaTeX via Core"""
        try:
            # Import Core functions
            from export_core import normalize_qt_model_to_ir, export_ir_to_latex
            
            # Get IR data from PDF canvas
            if self.pdf_canvas:
                ir_data = self.pdf_canvas.export_model_to_ir()
                if ir_data:
                    # Normalize Qt model to IR
                    normalized_ir = normalize_qt_model_to_ir(ir_data)
                    
                    # Export IR to LaTeX
                    latex_code = export_ir_to_latex(normalized_ir)
                    
                    # Save LaTeX to file
                    export_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
                    os.makedirs(export_dir, exist_ok=True)
                    latex_path = os.path.join(export_dir, 'guiLaTeX_export.tex')
                    
                    with open(latex_path, 'w', encoding='utf-8') as f:
                        f.write(latex_code)
                    
                    # Also save a copy to screenshots directory for evidence
                    screenshots_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'contest_evidence', 'screenshots')
                    os.makedirs(screenshots_dir, exist_ok=True)
                    evidence_path = os.path.join(screenshots_dir, 'qt_latex_export.tex')
                    
                    with open(evidence_path, 'w', encoding='utf-8') as f:
                        f.write(latex_code)
                    
                    # Show success message
                    from PyQt6.QtWidgets import QMessageBox
                    QMessageBox.information(self, "导出 LaTeX", 
                        f"LaTeX 已成功导出到:\n{latex_path}")
                    print(f"Exported LaTeX to: {latex_path}")
                    print(f"Evidence saved to: {evidence_path}")
                else:
                    from PyQt6.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "导出 LaTeX", "获取 IR 数据失败")
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "导出 LaTeX", f"导出失败:\n{str(e)}")
            print(f"Error exporting LaTeX: {e}")
    
    def import_latex(self):
        """Import LaTeX via Core"""
        try:
            # Import Core functions
            from export_core import import_own_exported_tex_to_ir
            
            # Open file dialog to select LaTeX file
            from PyQt6.QtWidgets import QFileDialog, QMessageBox
            options = QFileDialog.Options()
            options |= QFileDialog.Option.ReadOnly
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择 LaTeX 文件", "", "LaTeX Files (*.tex);;All Files (*)", options=options
            )
            
            if file_path:
                # Read LaTeX content
                with open(file_path, 'r', encoding='utf-8') as f:
                    latex_content = f.read()
                
                # Import LaTeX to IR
                ir_data = import_own_exported_tex_to_ir(latex_content)
                
                # Update PDF canvas with imported elements
                if self.pdf_canvas and self.pdf_canvas.page_widget:
                    # Clear existing elements
                    self.pdf_canvas.page_widget.memory_elements = []
                    
                    # Convert IR elements to memory elements
                    for ir_element in ir_data.get('elements', []):
                        memory_element = {
                            'id': ir_element.get('id', ''),
                            'type': ir_element.get('type', 'text'),
                            'text': ir_element.get('content', ''),
                            'x': ir_element.get('x', 0),
                            'y': ir_element.get('y', 0),
                            'width': ir_element.get('width', 0),
                            'height': ir_element.get('height', 0),
                            'font_size': ir_element.get('font_size', 12),
                            'font_family': ir_element.get('font_family_zh', 'Noto Sans SC'),
                            'font_family_zh': ir_element.get('font_family_zh', 'Noto Sans SC'),
                            'font_family_en': ir_element.get('font_family_en', 'Inter'),
                            'rotation': ir_element.get('rotation', 0),
                            'layer': ir_element.get('layer', 1),
                            'layer_id': f'layer_{10 - ir_element.get("layer", 1)}',
                            'original_width': ir_element.get('width', 0),
                            'original_height': ir_element.get('height', 0)
                        }
                        self.pdf_canvas.page_widget.memory_elements.append(memory_element)
                    
                    # Sync to model
                    self.pdf_canvas.page_widget._sync_to_model()
                    
                    # Update view
                    self.pdf_canvas.page_widget.is_dirty = True
                    self.pdf_canvas.page_widget.update()
                    
                    # Show success message
                    QMessageBox.information(self, "导入 LaTeX", 
                        f"LaTeX 已成功导入，共 {len(ir_data.get('elements', []))} 个元素")
                    print(f"Imported LaTeX from: {file_path}")
                else:
                    QMessageBox.warning(self, "导入 LaTeX", "PDF 画布未初始化")
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "导入 LaTeX", f"导入失败:\n{str(e)}")
            print(f"Error importing LaTeX: {e}")
    
    def move_element_up(self):
        """Move selected element up"""
        if self.pdf_canvas:
            self.pdf_canvas.bring_forward()
    
    def move_element_down(self):
        """Move selected element down"""
        if self.pdf_canvas:
            self.pdf_canvas.send_backward()
    
    def move_element_to_top(self):
        """Move selected element to top"""
        if self.pdf_canvas:
            self.pdf_canvas.bring_to_front()
    
    def move_element_to_bottom(self):
        """Move selected element to bottom"""
        if self.pdf_canvas:
            self.pdf_canvas.send_to_back()
    
    def zoom_in(self):
        """Zoom in"""
        if self.pdf_canvas:
            self.pdf_canvas.zoom_in()
    
    def zoom_out(self):
        """Zoom out"""
        if self.pdf_canvas:
            self.pdf_canvas.zoom_out()
    
    def reset_view(self):
        """Reset view to default zoom"""
        if self.pdf_canvas:
            self.pdf_canvas.zoom_scale = 1.0
            if self.pdf_canvas.page_widget:
                self.pdf_canvas.page_widget.set_scale(1.0)


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
