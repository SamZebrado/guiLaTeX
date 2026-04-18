#!/usr/bin/env python3
"""
Qt 字段保真验证与跨端准备

重点验证：type、layer、font_family_zh、font_family_en 字段
生成跨端验证材料
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


def analyze_core_gaps():
    """分析 Core 中的已知 gap"""
    return {
        "font_family_zh": {
            "status": "Core gap",
            "description": "normalize_qt_model_to_ir 中硬编码为 'SimSun'",
            "code_location": "export_core/__init__.py:111",
            "current_behavior": "忽略 Qt 模型中的 font_family_zh 字段",
            "expected_behavior": "应该保留 Qt 模型中的 font_family_zh 字段"
        },
        "font_family_en": {
            "status": "Core gap",
            "description": "normalize_qt_model_to_ir 中硬编码为 'Times New Roman'",
            "code_location": "export_core/__init__.py:112",
            "current_behavior": "忽略 Qt 模型中的 font_family_en 字段",
            "expected_behavior": "应该保留 Qt 模型中的 font_family_en 字段"
        },
        "type": {
            "status": "映射策略",
            "description": "Qt 类型到 IR 类型的映射",
            "code_location": "export_core/__init__.py:119-134",
            "current_behavior": "text -> paragraph, textbox -> textbox",
            "note": "这是预期的映射行为"
        },
        "layer": {
            "status": "直接映射",
            "description": "直接使用 Qt 模型的 layer 字段",
            "code_location": "export_core/__init__.py:110",
            "current_behavior": "layer: qt_element.get('layer', 0)",
            "note": "这是预期的直接映射"
        }
    }


def run_field_fidelity_verification():
    """运行字段保真验证"""
    print("=== Qt 字段保真验证开始 ===\n")
    
    screenshots_dir = os.path.join(
        os.path.dirname(__file__), '..', 
        'docs', 'contest_evidence', 'screenshots'
    )
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # 步骤 1: 创建测试用的 Qt 模型
    print("步骤 1: 创建测试用的 Qt 模型")
    original_qt_model = create_test_qt_model()
    
    original_model_path = os.path.join(screenshots_dir, 'qt_fidelity_original_model.json')
    with open(original_model_path, 'w', encoding='utf-8') as f:
        json.dump(original_qt_model, f, indent=2, ensure_ascii=False)
    print(f"   原始模型已保存到: {original_model_path}")
    
    # 步骤 2: 标准化 Qt 模型到 IR
    print("\n步骤 2: 标准化 Qt 模型到 IR")
    normalized_ir = normalize_qt_model_to_ir(original_qt_model)
    
    normalized_ir_path = os.path.join(screenshots_dir, 'qt_fidelity_normalized_ir.json')
    with open(normalized_ir_path, 'w', encoding='utf-8') as f:
        json.dump(normalized_ir, f, indent=2, ensure_ascii=False)
    print(f"   标准化 IR 已保存到: {normalized_ir_path}")
    
    # 步骤 3: 导出 IR 到 LaTeX
    print("\n步骤 3: 导出 IR 到 LaTeX")
    latex_code = export_ir_to_latex(normalized_ir)
    
    latex_path = os.path.join(screenshots_dir, 'qt_fidelity_export.tex')
    with open(latex_path, 'w', encoding='utf-8') as f:
        f.write(latex_code)
    print(f"   LaTeX 文件已保存到: {latex_path}")
    
    # 步骤 4: 从 LaTeX 导回 IR
    print("\n步骤 4: 从 LaTeX 导回 IR")
    imported_ir = import_own_exported_tex_to_ir(latex_code)
    
    imported_ir_path = os.path.join(screenshots_dir, 'qt_fidelity_imported_ir.json')
    with open(imported_ir_path, 'w', encoding='utf-8') as f:
        json.dump(imported_ir, f, indent=2, ensure_ascii=False)
    print(f"   导入 IR 已保存到: {imported_ir_path}")
    
    # 步骤 5: 分析字段差异
    print("\n步骤 5: 分析字段差异")
    field_analysis = []
    
    focus_fields = ["type", "layer", "font_family_zh", "font_family_en"]
    
    for idx, (original_elem, normalized_elem, imported_elem) in enumerate(
        zip(original_qt_model['elements'], normalized_ir['elements'], imported_ir['elements'])
    ):
        elem_analysis = {
            "element_id": original_elem["id"],
            "element_index": idx,
            "fields": {}
        }
        
        for field in focus_fields:
            orig_value = original_elem.get(field)
            norm_value = normalized_elem.get(field)
            imp_value = imported_elem.get(field)
            
            elem_analysis["fields"][field] = {
                "original_qt": orig_value,
                "normalized_ir": norm_value,
                "imported_ir": imp_value,
                "qt_to_norm_match": orig_value == norm_value,
                "norm_to_imp_match": norm_value == imp_value,
                "full_roundtrip_match": orig_value == imp_value
            }
        
        field_analysis.append(elem_analysis)
    
    # 步骤 6: 生成字段保真报告
    print("\n步骤 6: 生成字段保真报告")
    core_gaps = analyze_core_gaps()
    
    fidelity_report = {
        "test_date": "2026-04-18",
        "status": "完成",
        "focus_fields": focus_fields,
        "core_gaps": core_gaps,
        "field_analysis": field_analysis,
        "summary": {
            "qt_to_norm_match_count": sum(
                1 for elem in field_analysis 
                for field in focus_fields 
                if elem["fields"][field]["qt_to_norm_match"]
            ),
            "norm_to_imp_match_count": sum(
                1 for elem in field_analysis 
                for field in focus_fields 
                if elem["fields"][field]["norm_to_imp_match"]
            ),
            "full_roundtrip_match_count": sum(
                1 for elem in field_analysis 
                for field in focus_fields 
                if elem["fields"][field]["full_roundtrip_match"]
            ),
            "total_possible": len(field_analysis) * len(focus_fields)
        },
        "evidence_files": {
            "original_model": original_model_path,
            "normalized_ir": normalized_ir_path,
            "exported_tex": latex_path,
            "imported_ir": imported_ir_path
        }
    }
    
    report_path = os.path.join(screenshots_dir, 'qt_fidelity_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(fidelity_report, f, indent=2, ensure_ascii=False)
    print(f"   字段保真报告已保存到: {report_path}")
    
    # 步骤 7: 生成跨端验证材料
    print("\n步骤 7: 生成跨端验证材料")
    cross_end_material = {
        "purpose": "为 Web 端导回 Qt 导出的 conforming tex 准备的验证材料",
        "qt_exported_tex_path": latex_path,
        "qt_exported_ir_path": normalized_ir_path,
        "field_mapping_notes": {
            "type": "Qt 'text' 映射为 IR 'paragraph'",
            "layer": "直接使用 Qt layer 值",
            "font_family_zh": "当前 Core 硬编码为 'SimSun'",
            "font_family_en": "当前 Core 硬编码为 'Times New Roman'"
        },
        "web_import_instructions": """
1. 使用 Web 端的导入 LaTeX 功能
2. 选择 qt_fidelity_export.tex 文件
3. 验证元素是否正确导入
4. 检查以下字段：id, content, x, y, width, height, rotation
5. 注意：type/layer/font_family_zh/font_family_en 可能与 Qt 原始模型有差异
        """,
        "expected_elements": [
            {
                "id": "test_title",
                "content": "测试标题",
                "x": 100,
                "y": 50,
                "width": 400,
                "height": 40,
                "rotation": 0
            },
            {
                "id": "test_paragraph",
                "content": "这是一段测试文本",
                "x": 100,
                "y": 100,
                "width": 400,
                "height": 80,
                "rotation": 45
            },
            {
                "id": "test_formula",
                "content": "E = mc²",
                "x": 100,
                "y": 200,
                "width": 200,
                "height": 30,
                "rotation": 0
            }
        ]
    }
    
    cross_end_path = os.path.join(screenshots_dir, 'qt_cross_end_verification_material.json')
    with open(cross_end_path, 'w', encoding='utf-8') as f:
        json.dump(cross_end_material, f, indent=2, ensure_ascii=False)
    print(f"   跨端验证材料已保存到: {cross_end_path}")
    
    # 打印摘要
    print("\n=== 字段保真验证摘要 ===")
    print(f"重点字段: {', '.join(focus_fields)}")
    print(f"\nCore Gap 识别:")
    for field, gap_info in core_gaps.items():
        if gap_info["status"] == "Core gap":
            print(f"  - {field}: {gap_info['description']}")
    
    print(f"\n字段匹配统计:")
    summary = fidelity_report["summary"]
    print(f"  Qt -> IR 匹配: {summary['qt_to_norm_match_count']}/{summary['total_possible']}")
    print(f"  IR -> 导入匹配: {summary['norm_to_imp_match_count']}/{summary['total_possible']}")
    print(f"  完整 roundtrip 匹配: {summary['full_roundtrip_match_count']}/{summary['total_possible']}")
    
    print("\n=== Qt 字段保真验证完成 ===")
    
    return fidelity_report


if __name__ == "__main__":
    run_field_fidelity_verification()
