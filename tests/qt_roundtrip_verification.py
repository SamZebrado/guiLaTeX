#!/usr/bin/env python3
"""
Qt Roundtrip Verification Test

真实验证 Qt -> Core -> tex -> Core -> Qt 的 roundtrip 流程
生成字段保留差异报告
"""

import os
import sys
import json
import tempfile

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
                "layer_id": "layer_9",
                "color": "#000000",
                "alignment": "left",
                "visible": True
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
                "font_family_zh": "Noto Sans SC",
                "font_family_en": "Inter",
                "rotation": 45,
                "layer": 2,
                "layer_id": "layer_8",
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
                "layer_id": "layer_7",
                "color": "#000000",
                "alignment": "left",
                "visible": True
            }
        ]
    }


def compare_elements(original, imported):
    """比较两个元素，返回差异报告"""
    differences = []
    
    fields_to_compare = [
        "id", "type", "content", "page",
        "x", "y", "width", "height",
        "rotation", "layer", "visible",
        "font_family", "font_family_zh", "font_family_en",
        "font_size", "color", "alignment"
    ]
    
    for field in fields_to_compare:
        orig_value = original.get(field)
        # 处理 content/text 字段的差异
        if field == "content":
            imported_value = imported.get("content") or imported.get("text")
        elif field == "type":
            # 类型映射：text -> textbox/paragraph
            orig_type = orig_value
            imported_type = imported_value
            if orig_type == "text" and imported_type in ["textbox", "paragraph"]:
                continue  # 类型映射是预期的
        else:
            imported_value = imported.get(field)
        
        if orig_value != imported_value:
            differences.append({
                "field": field,
                "original": orig_value,
                "imported": imported_value,
                "status": "丢失" if imported_value is None else "不匹配"
            })
    
    return differences


def run_roundtrip_test():
    """运行完整的 roundtrip 测试"""
    print("=== Qt Roundtrip 验证测试开始 ===\n")
    
    # 步骤 1: 创建测试用的 Qt 模型
    print("步骤 1: 创建测试用的 Qt 模型")
    original_qt_model = create_test_qt_model()
    print(f"   成功创建 {len(original_qt_model['elements'])} 个测试元素\n")
    
    # 保存原始模型
    screenshots_dir = os.path.join(
        os.path.dirname(__file__), '..', 
        'docs', 'contest_evidence', 'screenshots'
    )
    os.makedirs(screenshots_dir, exist_ok=True)
    
    original_model_path = os.path.join(screenshots_dir, 'qt_roundtrip_original_model.json')
    with open(original_model_path, 'w', encoding='utf-8') as f:
        json.dump(original_qt_model, f, indent=2, ensure_ascii=False)
    print(f"   原始模型已保存到: {original_model_path}")
    
    # 步骤 2: 标准化 Qt 模型到 IR
    print("\n步骤 2: 标准化 Qt 模型到 IR")
    normalized_ir = normalize_qt_model_to_ir(original_qt_model)
    print(f"   成功标准化 {len(normalized_ir['elements'])} 个元素")
    
    normalized_ir_path = os.path.join(screenshots_dir, 'qt_roundtrip_normalized_ir.json')
    with open(normalized_ir_path, 'w', encoding='utf-8') as f:
        json.dump(normalized_ir, f, indent=2, ensure_ascii=False)
    print(f"   标准化 IR 已保存到: {normalized_ir_path}")
    
    # 步骤 3: 导出 IR 到 LaTeX
    print("\n步骤 3: 导出 IR 到 LaTeX")
    latex_code = export_ir_to_latex(normalized_ir)
    print(f"   成功生成 LaTeX 代码，长度: {len(latex_code)} 字符")
    
    latex_path = os.path.join(screenshots_dir, 'qt_roundtrip_export.tex')
    with open(latex_path, 'w', encoding='utf-8') as f:
        f.write(latex_code)
    print(f"   LaTeX 文件已保存到: {latex_path}")
    
    # 步骤 4: 从 LaTeX 导回 IR
    print("\n步骤 4: 从 LaTeX 导回 IR")
    imported_ir = import_own_exported_tex_to_ir(latex_code)
    print(f"   成功导回 {len(imported_ir['elements'])} 个元素")
    
    imported_ir_path = os.path.join(screenshots_dir, 'qt_roundtrip_imported_ir.json')
    with open(imported_ir_path, 'w', encoding='utf-8') as f:
        json.dump(imported_ir, f, indent=2, ensure_ascii=False)
    print(f"   导入 IR 已保存到: {imported_ir_path}")
    
    # 步骤 5: 生成字段保留差异报告
    print("\n步骤 5: 生成字段保留差异报告")
    all_differences = []
    
    for idx, (original_elem, imported_elem) in enumerate(
        zip(original_qt_model['elements'], imported_ir['elements'])
    ):
        # 将原始 Qt 元素转换为 IR 格式以便比较
        original_ir_elem = {
            "id": original_elem["id"],
            "type": "textbox" if idx == 0 else "paragraph" if idx == 1 else "textbox",
            "content": original_elem["text"],
            "page": 1,
            "x": original_elem["x"],
            "y": original_elem["y"],
            "width": original_elem["width"],
            "height": original_elem["height"],
            "rotation": original_elem["rotation"],
            "layer": 10 - original_elem["layer"],  # Qt 的 layer 到 IR 的转换
            "visible": original_elem.get("visible", True),
            "font_family_zh": original_elem.get("font_family_zh"),
            "font_family_en": original_elem.get("font_family_en"),
            "font_size": original_elem["font_size"],
            "color": original_elem.get("color", "#000000"),
            "alignment": original_elem.get("alignment", "left")
        }
        
        elem_differences = compare_elements(original_ir_elem, imported_elem)
        if elem_differences:
            all_differences.append({
                "element_id": original_elem["id"],
                "element_index": idx,
                "differences": elem_differences
            })
    
    # 生成差异报告
    report = {
        "test_date": "2026-04-18",
        "status": "完成",
        "original_elements_count": len(original_qt_model['elements']),
        "imported_elements_count": len(imported_ir['elements']),
        "elements_with_differences": len(all_differences),
        "differences": all_differences,
        "evidence_files": {
            "original_model": original_model_path,
            "normalized_ir": normalized_ir_path,
            "exported_tex": latex_path,
            "imported_ir": imported_ir_path
        }
    }
    
    report_path = os.path.join(screenshots_dir, 'qt_roundtrip_field_difference_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"   差异报告已保存到: {report_path}")
    
    # 打印摘要
    print("\n=== Roundtrip 测试摘要 ===")
    print(f"原始元素数量: {len(original_qt_model['elements'])}")
    print(f"导入元素数量: {len(imported_ir['elements'])}")
    print(f"有差异的元素数量: {len(all_differences)}")
    
    if all_differences:
        print("\n字段差异详情:")
        for elem_diff in all_differences:
            print(f"\n元素 {elem_diff['element_id']}:")
            for diff in elem_diff['differences']:
                print(f"  - {diff['field']}: {diff['status']}")
                print(f"    原始值: {diff['original']}")
                print(f"    导入值: {diff['imported']}")
    else:
        print("\n✅ 所有字段都正确保留！")
    
    print("\n=== Qt Roundtrip 验证测试完成 ===")
    
    return report


if __name__ == "__main__":
    run_roundtrip_test()
