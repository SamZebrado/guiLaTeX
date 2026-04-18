#!/usr/bin/env python3
"""
Qt 跨端验证材料生成

生成固定的跨端验证材料，供 Web 直接使用
"""

import os
import sys
import json

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from export_core import (
    normalize_qt_model_to_ir,
    export_ir_to_latex,
    import_own_exported_tex_to_ir
)


def create_test_qt_model():
    """创建测试用的 Qt 模型"""
    return {
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
                "font_family_zh": "Noto Sans SC",
                "font_family_en": "Inter",
                "rotation": 0,
                "layer": 1,
                "layer_id": "layer_1",
                "color": "#000000",
                "alignment": "left",
                "visible": True
            },
            {
                "id": "test_paragraph",
                "type": "text",
                "text": "这是一段测试文本，包含中英文混合内容：Hello World",
                "x": 100,
                "y": 100,
                "width": 400,
                "height": 80,
                "font_size": 12,
                "font_family": "Noto Sans SC",
                "font_family_zh": "Noto Sans SC",
                "font_family_en": "Inter",
                "rotation": 45,
                "layer": 2,
                "layer_id": "layer_2",
                "color": "#000000",
                "alignment": "left",
                "visible": True
            },
            {
                "id": "test_formula",
                "type": "text",
                "text": "E = mc²",
                "x": 100,
                "y": 200,
                "width": 200,
                "height": 30,
                "font_size": 16,
                "font_family": "Noto Sans",
                "font_family_zh": "Noto Sans SC",
                "font_family_en": "Noto Sans",
                "rotation": 0,
                "layer": 3,
                "layer_id": "layer_3",
                "color": "#000000",
                "alignment": "left",
                "visible": True
            }
        ]
    }


def generate_web_verification_material():
    """生成跨端验证材料"""
    print("=== Qt 跨端验证材料生成开始 ===\n")
    
    screenshots_dir = os.path.join(
        os.path.dirname(__file__), '..', 
        'docs', 'contest_evidence', 'screenshots'
    )
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # 步骤 1: 创建测试用的 Qt 模型
    print("步骤 1: 创建测试用的 Qt 模型")
    original_qt_model = create_test_qt_model()
    
    source_model_path = os.path.join(screenshots_dir, 'qt_to_web_source_model.json')
    with open(source_model_path, 'w', encoding='utf-8') as f:
        json.dump(original_qt_model, f, indent=2, ensure_ascii=False)
    print(f"   原始模型已保存到: {source_model_path}")
    
    # 步骤 2: 标准化 Qt 模型到 IR
    print("\n步骤 2: 标准化 Qt 模型到 IR")
    normalized_ir = normalize_qt_model_to_ir(original_qt_model)
    
    expected_ir_path = os.path.join(screenshots_dir, 'qt_to_web_expected_ir.json')
    with open(expected_ir_path, 'w', encoding='utf-8') as f:
        json.dump(normalized_ir, f, indent=2, ensure_ascii=False)
    print(f"   标准化 IR 已保存到: {expected_ir_path}")
    
    # 步骤 3: 导出 IR 到 LaTeX
    print("\n步骤 3: 导出 IR 到 LaTeX")
    latex_code = export_ir_to_latex(normalized_ir)
    
    conforming_tex_path = os.path.join(screenshots_dir, 'qt_to_web_conforming.tex')
    with open(conforming_tex_path, 'w', encoding='utf-8') as f:
        f.write(latex_code)
    print(f"   LaTeX 文件已保存到: {conforming_tex_path}")
    
    # 步骤 4: 检查是否包含 IR 元数据
    print("\n步骤 4: 检查是否包含 IR 元数据")
    has_metadata = False
    has_begin_marker = "BEGIN_IR_METADATA" in latex_code
    has_end_marker = "END_IR_METADATA" in latex_code
    
    if has_begin_marker and has_end_marker:
        has_metadata = True
        print("   ✅ 包含 IR 元数据标记")
    else:
        print("   ❌ 缺少 IR 元数据标记")
        if not has_begin_marker:
            print("   - 缺少 BEGIN_IR_METADATA")
        if not has_end_marker:
            print("   - 缺少 END_IR_METADATA")
    
    # 步骤 5: 生成说明文件
    print("\n步骤 5: 生成说明文件")
    readme_content = """# Qt 跨端验证材料说明

## 材料列表
- qt_to_web_conforming.tex：Qt 导出的 conforming LaTeX 文件
- qt_to_web_source_model.json：Qt 原始模型
- qt_to_web_expected_ir.json：标准化后的 IR

## Web 验证指南
1. 使用 Web 端的导入 LaTeX 功能
2. 选择 qt_to_web_conforming.tex 文件
3. 验证元素是否正确导入

## 必须保住的字段
- id
- content
- page
- x, y, width, height
- rotation
- visible
- font_size
- color
- alignment
- layer

## 当前允许差异的字段
- type：Qt 'text' → IR 'paragraph'（这是预期的映射策略）
- font_family_zh：当前 Core 硬编码为 'SimSun'（Core gap）
- font_family_en：当前 Core 硬编码为 'Times New Roman'（Core gap）

## Core gap 说明
- font_family_zh：normalize_qt_model_to_ir 中硬编码为 'SimSun'，忽略 Qt 模型值
- font_family_en：normalize_qt_model_to_ir 中硬编码为 'Times New Roman'，忽略 Qt 模型值

## 预期元素
1. 标题元素：id="test_title"
2. 段落元素：id="test_paragraph"
3. 公式元素：id="test_formula"

## 字段口径
| 字段 | Qt 原始值 | 预期 IR 值 | 说明 |
|------|-----------|------------|------|
| type | "text" | "paragraph" | 映射策略 |
| layer | 1/2/3 | 1/2/3 | 必须保住 |
| font_family_zh | "Noto Sans SC" | "SimSun" | Core gap |
| font_family_en | "Inter"/"Noto Sans" | "Times New Roman" | Core gap |
"""
    
    readme_path = os.path.join(screenshots_dir, 'qt_to_web_readme.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"   说明文件已保存到: {readme_path}")
    
    # 步骤 6: 生成差异口径文件
    print("\n步骤 6: 生成差异口径文件")
    field_caliber = {
        "test_date": "2026-04-18",
        "fields": [
            {
                "field": "type",
                "qt_value": "text",
                "ir_value": "paragraph",
                "expected_value": "paragraph",
                "status": "可接受",
                "attribution": "映射策略",
                "note": "Qt 'text' → IR 'paragraph' 是预期的映射行为"
            },
            {
                "field": "layer",
                "qt_value": [1, 2, 3],
                "ir_value": [1, 2, 3],
                "expected_value": [1, 2, 3],
                "status": "必须保住",
                "attribution": "直接映射",
                "note": "layer 字段应该完整保住"
            },
            {
                "field": "font_family_zh",
                "qt_value": "Noto Sans SC",
                "ir_value": "SimSun",
                "expected_value": "Noto Sans SC",
                "status": "不可接受",
                "attribution": "Core gap",
                "note": "normalize_qt_model_to_ir 中硬编码为 'SimSun'"
            },
            {
                "field": "font_family_en",
                "qt_value": ["Inter", "Noto Sans"],
                "ir_value": "Times New Roman",
                "expected_value": ["Inter", "Noto Sans"],
                "status": "不可接受",
                "attribution": "Core gap",
                "note": "normalize_qt_model_to_ir 中硬编码为 'Times New Roman'"
            }
        ],
        "evidence_files": {
            "source_model": source_model_path,
            "expected_ir": expected_ir_path,
            "conforming_tex": conforming_tex_path,
            "readme": readme_path
        }
    }
    
    caliber_path = os.path.join(screenshots_dir, 'qt_to_web_field_caliber.json')
    with open(caliber_path, 'w', encoding='utf-8') as f:
        json.dump(field_caliber, f, indent=2, ensure_ascii=False)
    print(f"   差异口径文件已保存到: {caliber_path}")
    
    # 打印摘要
    print("\n=== 跨端验证材料生成摘要 ===")
    print(f"生成的文件:")
    print(f"  - {source_model_path}")
    print(f"  - {expected_ir_path}")
    print(f"  - {conforming_tex_path}")
    print(f"  - {readme_path}")
    print(f"  - {caliber_path}")
    
    print(f"\nIR 元数据检查:")
    if has_metadata:
        print("  ✅ 包含 BEGIN_IR_METADATA 和 END_IR_METADATA")
    else:
        print("  ❌ 缺少 IR 元数据标记")
    
    print("\n=== Qt 跨端验证材料生成完成 ===")
    
    return {
        "has_metadata": has_metadata,
        "files": {
            "source_model": source_model_path,
            "expected_ir": expected_ir_path,
            "conforming_tex": conforming_tex_path,
            "readme": readme_path,
            "caliber": caliber_path
        }
    }


if __name__ == "__main__":
    generate_web_verification_material()
