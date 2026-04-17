#!/usr/bin/env python3
"""
Qt Roundtrip Test

Test the complete roundtrip: Qt -> Core -> LaTeX -> Core -> Qt
"""

import os
import sys
import json
import tempfile

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from export_core import normalize_qt_model_to_ir, export_ir_to_latex, import_own_exported_tex_to_ir


def test_roundtrip():
    """Test the complete roundtrip process"""
    # Create a simple test model that mimics Qt's memory elements
    test_model = {
        "elements": [
            {
                "id": "test_title",
                "type": "text",
                "text": "测试标题",
                "x": 100,
                "y": 50,
                "width": 400,
                "height": 40,
                "font_size": 24,
                "font_family": "Noto Sans SC",
                "rotation": 0
            },
            {
                "id": "test_paragraph",
                "type": "text",
                "text": "这是一段测试文本",
                "x": 100,
                "y": 100,
                "width": 400,
                "height": 80,
                "font_size": 12,
                "font_family": "Noto Sans SC",
                "rotation": 0
            }
        ]
    }
    
    print("=== 开始 Roundtrip 测试 ===")
    
    # Step 1: Normalize Qt model to IR
    print("1. 标准化 Qt 模型到 IR...")
    normalized_ir = normalize_qt_model_to_ir(test_model)
    print(f"   成功标准化 {len(normalized_ir['elements'])} 个元素")
    
    # Step 2: Export IR to LaTeX
    print("2. 导出 IR 到 LaTeX...")
    latex_code = export_ir_to_latex(normalized_ir)
    print(f"   成功生成 LaTeX 代码，长度: {len(latex_code)} 字符")
    
    # Step 3: Save LaTeX to file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write(latex_code)
        temp_tex_path = f.name
    
    print(f"   保存 LaTeX 到: {temp_tex_path}")
    
    # Step 4: Import LaTeX back to IR
    print("3. 从 LaTeX 导回 IR...")
    with open(temp_tex_path, 'r', encoding='utf-8') as f:
        imported_ir = import_own_exported_tex_to_ir(f.read())
    
    print(f"   成功导回 {len(imported_ir['elements'])} 个元素")
    
    # Step 5: Compare original and imported models
    print("4. 比较原始模型和导入模型...")
    
    # Clean up temporary file
    os.unlink(temp_tex_path)
    
    # Verify elements count
    assert len(test_model['elements']) == len(imported_ir['elements']), \
        f"元素数量不匹配: {len(test_model['elements'])} != {len(imported_ir['elements'])}"
    
    # Verify key properties
    for i, (original, imported) in enumerate(zip(test_model['elements'], imported_ir['elements'])):
        assert original['id'] == imported['id'], f"元素 {i} ID 不匹配"
        assert original['text'] == imported['content'], f"元素 {i} 内容不匹配"
        assert abs(original['x'] - imported['x']) < 0.01, f"元素 {i} X 坐标不匹配"
        assert abs(original['y'] - imported['y']) < 0.01, f"元素 {i} Y 坐标不匹配"
        assert abs(original['width'] - imported['width']) < 0.01, f"元素 {i} 宽度不匹配"
        assert abs(original['height'] - imported['height']) < 0.01, f"元素 {i} 高度不匹配"
        assert abs(original['font_size'] - imported['font_size']) < 0.01, f"元素 {i} 字体大小不匹配"
        assert abs(original['rotation'] - imported['rotation']) < 0.01, f"元素 {i} 旋转角度不匹配"
    
    print("   所有元素属性匹配成功！")
    print("=== Roundtrip 测试通过 ===")
    
    return True


if __name__ == "__main__":
    test_roundtrip()
