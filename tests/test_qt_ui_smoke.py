#!/usr/bin/env python3
"""
Qt UI Smoke Test

验证 Qt 界面结构是否符合统一 UI 模式 v1
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui.main import MainWindow


def test_ui_structure():
    """测试 UI 结构是否符合统一 UI 模式 v1"""
    print("=== Qt UI Smoke Test ===")
    
    # 创建应用实例
    app = QApplication([])
    
    # 创建主窗口
    window = MainWindow()
    
    # 测试 1: 顶部工具栏是否按分组存在
    print("\n1. 测试顶部工具栏分组:")
    menu_bar = window.menuBar()
    menu_titles = [menu.title() for menu in menu_bar.actions()]
    
    expected_menus = ["文件", "编辑", "排列", "变换", "视图"]
    for menu in expected_menus:
        if menu in menu_titles:
            print(f"  ✓ {menu} 菜单存在")
        else:
            print(f"  ✗ {menu} 菜单缺失")
    
    # 测试 2: 左画布 / 右面板是否成立
    print("\n2. 测试主区布局:")
    central_widget = window.centralWidget()
    layout = central_widget.layout()
    
    # 检查主分割器
    main_splitter = layout.itemAt(0).widget()
    top_splitter = main_splitter.widget(0)
    
    if top_splitter:
        print("  ✓ 主分割器存在")
        
        # 检查 PDF 画布和属性面板
        pdf_canvas = top_splitter.widget(0)
        property_panel = top_splitter.widget(1)
        
        if pdf_canvas:
            print("  ✓ PDF 画布存在")
        else:
            print("  ✗ PDF 画布缺失")
        
        if property_panel:
            print("  ✓ 属性面板存在")
        else:
            print("  ✗ 属性面板缺失")
    else:
        print("  ✗ 主分割器缺失")
    
    # 测试 3: 中文标签是否对齐 Web 模式
    print("\n3. 测试中文标签:")
    # 检查文件菜单
    file_menu = menu_bar.actions()[0].menu()
    file_actions = [action.text() for action in file_menu.actions() if action.text()]
    expected_file_actions = ["打开项目", "保存项目", "导出 PDF", "导出模型 JSON", "导出 IR", "退出"]
    
    for action in expected_file_actions:
        if action in file_actions:
            print(f"  ✓ 文件菜单: {action}")
        else:
            print(f"  ✗ 文件菜单: {action} 缺失")
    
    # 检查编辑菜单
    edit_menu = menu_bar.actions()[1].menu()
    edit_actions = [action.text() for action in edit_menu.actions() if action.text()]
    expected_edit_actions = ["复制", "粘贴", "删除"]
    
    for action in expected_edit_actions:
        if action in edit_actions:
            print(f"  ✓ 编辑菜单: {action}")
        else:
            print(f"  ✗ 编辑菜单: {action} 缺失")
    
    # 检查排列菜单
    arrange_menu = menu_bar.actions()[2].menu()
    arrange_actions = [action.text() for action in arrange_menu.actions() if action.text()]
    expected_arrange_actions = ["上移", "下移", "移到顶部", "移到底部", "图层编号变整数"]
    
    for action in expected_arrange_actions:
        if action in arrange_actions:
            print(f"  ✓ 排列菜单: {action}")
        else:
            print(f"  ✗ 排列菜单: {action} 缺失")
    
    # 检查视图菜单
    view_menu = menu_bar.actions()[4].menu()
    view_actions = [action.text() for action in view_menu.actions() if action.text()]
    expected_view_actions = ["放大", "缩小", "重置视图", "显示调试"]
    
    for action in expected_view_actions:
        if action in view_actions:
            print(f"  ✓ 视图菜单: {action}")
        else:
            print(f"  ✗ 视图菜单: {action} 缺失")
    
    # 测试 4: 属性面板分组
    print("\n4. 测试属性面板分组:")
    if hasattr(window, 'property_panel'):
        property_layout = window.property_panel.layout()
        group_boxes = []
        
        for i in range(property_layout.count()):
            widget = property_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'title'):
                group_boxes.append(widget.title())
        
        expected_groups = ["选中信息", "内容", "几何", "字体", "对象专属属性", "调试信息"]
        for group in expected_groups:
            if group in group_boxes:
                print(f"  ✓ 属性面板: {group}")
            else:
                print(f"  ✗ 属性面板: {group} 缺失")
    else:
        print("  ✗ 属性面板未找到")
    
    print("\n=== UI Smoke Test 完成 ===")
    
    # 清理
    window.close()
    del window
    del app


if __name__ == "__main__":
    test_ui_structure()
