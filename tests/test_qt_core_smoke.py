#!/usr/bin/env python3
"""
Qt Core Smoke Test

验证 Qt -> Core 链路是否正常工作
"""

import sys
import os
import json

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入必要的模块
try:
    from gui.pdf_canvas import PDFCanvas
    from model import DocumentModel, PageModel, ElementModel
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)


def test_qt_to_core():
    """测试 Qt -> Core 链路"""
    print("=== Qt Core Smoke Test ===")
    
    # 创建文档模型
    print("\n1. 创建测试模型:")
    document_model = DocumentModel(title='Test Document')
    page = PageModel(number=1)
    document_model.add_page(page)
    
    # 创建测试元素
    element1 = ElementModel(
        type='text',
        content='测试文本 1',
        x=100,
        y=100,
        width=200,
        height=50,
        font_size=12,
        rotation=45,
        layer=1,
        font_family_zh='Noto Sans SC',
        font_family_en='Inter'
    )
    
    element2 = ElementModel(
        type='text',
        content='Test Text 2',
        x=200,
        y=200,
        width=150,
        height=40,
        font_size=14,
        rotation=90,
        layer=2,
        font_family_zh='Source Han Sans SC',
        font_family_en='Noto Sans'
    )
    
    page.add_element(element1)
    page.add_element(element2)
    
    print(f"  ✓ 创建了 {len(page.elements)} 个测试元素")
    print(f"  ✓ 元素 1: 旋转={element1.rotation}, 图层={element1.layer}")
    print(f"  ✓ 元素 2: 旋转={element2.rotation}, 图层={element2.layer}")
    
    # 创建 PDFCanvas 实例
    print("\n2. 测试 IR 导出:")
    pdf_canvas = PDFCanvas(document_model=document_model)
    
    # 导出模型到 IR
    ir_data = pdf_canvas.export_model_to_ir()
    
    if ir_data:
        print("  ✓ IR 导出成功")
        
        # 验证关键字段
        print("\n3. 验证关键字段:")
        for i, element in enumerate(ir_data.get('elements', [])):
            print(f"  元素 {i+1}:")
            
            # 检查 rotation 字段
            if 'rotation' in element:
                print(f"    ✓ rotation: {element['rotation']}")
            else:
                print("    ✗ rotation 字段缺失")
            
            # 检查 layer 字段
            if 'layer' in element:
                print(f"    ✓ layer: {element['layer']}")
            else:
                print("    ✗ layer 字段缺失")
            
            # 检查 font 字段
            if 'font' in element:
                print(f"    ✓ font 字段存在")
                font = element['font']
                if 'font_family_zh' in font:
                    print(f"    ✓ font_family_zh: {font['font_family_zh']}")
                else:
                    print("    ✗ font_family_zh 字段缺失")
                if 'font_family_en' in font:
                    print(f"    ✓ font_family_en: {font['font_family_en']}")
                else:
                    print("    ✗ font_family_en 字段缺失")
            else:
                print("    ✗ font 字段缺失")
        
        # 保存 IR 到文件
        ir_path = os.path.join(os.path.dirname(__file__), '..', 'temp', 'qt_ir_test.json')
        os.makedirs(os.path.dirname(ir_path), exist_ok=True)
        
        with open(ir_path, 'w', encoding='utf-8') as f:
            json.dump(ir_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n4. IR 数据已保存到: {ir_path}")
    else:
        print("  ✗ IR 导出失败")
    
    # 测试 LaTeX 导出（如果可用）
    print("\n5. 测试 LaTeX 导出:")
    try:
        from latex.pdf_reconstructor import PDFToLaTeXConverter
        converter = PDFToLaTeXConverter()
        
        # 模拟 memory_elements
        memory_elements = []
        for element in page.elements:
            memory_elements.append({
                'id': element.id,
                'text': element.content,
                'x': element.x,
                'y': element.y,
                'width': element.width,
                'height': element.height,
                'font_size': element.font_size,
                'rotation': element.rotation,
                'layer': element.layer,
                'font_family_zh': element.font_family_zh,
                'font_family_en': element.font_family_en
            })
        
        latex_code = converter.convert_memory_elements(memory_elements)
        if latex_code:
            print("  ✓ LaTeX 导出成功")
            
            # 保存 LaTeX 到文件
            latex_path = os.path.join(os.path.dirname(__file__), '..', 'temp', 'qt_latex_test.tex')
            with open(latex_path, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            
            print(f"  LaTeX 代码已保存到: {latex_path}")
        else:
            print("  ✗ LaTeX 导出失败")
    except ImportError:
        print("  ⚠️  LaTeX 转换器不可用，跳过测试")
    except Exception as e:
        print(f"  ✗ LaTeX 导出出错: {e}")
    
    print("\n=== Core Smoke Test 完成 ===")


if __name__ == "__main__":
    test_qt_to_core()
