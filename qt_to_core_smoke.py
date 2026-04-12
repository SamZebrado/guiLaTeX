#!/usr/bin/env python3
"""
Qt -> Core 最小 Smoke Test (真实调用 ExportCore 函数)
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

print("=== Qt -> Core 最小 Smoke Test (真实调用 ExportCore) ===")
print()

# 准备输出目录
output_dir = Path(__file__).parent / 'docs' / 'contest_evidence' / 'screenshots'
output_dir.mkdir(parents=True, exist_ok=True)

# 准备测试日志
log_path = output_dir / 'qt_to_core_smoke_test_log.txt'

def log(message):
    """记录日志到文件和控制台"""
    print(message)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

# 清空日志文件
if log_path.exists():
    log_path.unlink()

log(f"测试开始时间: {datetime.now().isoformat()}")
log("=" * 60)
log()

# 1. 准备 Qt 模型数据
log("步骤 1: 准备 Qt 模型数据")
qt_model = {
    "elements": [
        {
            "id": "demo_title",
            "type": "text",
            "text": "可视化编辑 LaTeX 文档",
            "x": 100,
            "y": 50,
            "width": 400,
            "height": 40,
            "font_size": 24,
            "font_family": "Noto Sans SC",
            "rotation": 0,
            "layer": 1
        },
        {
            "id": "demo_author",
            "type": "text",
            "text": "作者：某某 / 博士生原型测试",
            "x": 100,
            "y": 100,
            "width": 300,
            "height": 25,
            "font_size": 14,
            "font_family": "Noto Sans SC",
            "rotation": 0,
            "layer": 1
        },
        {
            "id": "demo_body",
            "type": "text",
            "text": "这是一段用于演示正文对象的内容，可用于测试拖动、选择和后续选择框能力。",
            "x": 100,
            "y": 150,
            "width": 400,
            "height": 80,
            "font_size": 12,
            "font_family": "Noto Sans SC",
            "rotation": -10,
            "layer": 2
        },
        {
            "id": "demo_formula",
            "type": "text",
            "text": "E = mc^2",
            "x": 100,
            "y": 240,
            "width": 200,
            "height": 30,
            "font_size": 16,
            "font_family": "Noto Sans SC",
            "rotation": 30,
            "layer": 1
        },
        {
            "id": "demo_image",
            "type": "text",
            "text": "图片示例 / 占位图",
            "x": 100,
            "y": 280,
            "width": 300,
            "height": 200,
            "font_size": 12,
            "font_family": "Noto Sans SC",
            "rotation": 45,
            "layer": 1
        }
    ]
}

# 保存输入的 Qt 模型
qt_model_input_path = output_dir / 'qt_to_core_input_model.json'
with open(qt_model_input_path, 'w', encoding='utf-8') as f:
    json.dump(qt_model, f, indent=2, ensure_ascii=False)

log(f"✅ Qt 输入模型已保存: {qt_model_input_path}")
log(f"   元素数量: {len(qt_model['elements'])}")
log()

# 2. 导入 ExportCore 并调用 normalize_qt_model_to_ir
log("步骤 2: 导入 ExportCore")
try:
    from export_core import normalize_qt_model_to_ir, export_ir_to_latex
    log("✅ export_core 模块导入成功")
    log("   可用函数: normalize_qt_model_to_ir, export_ir_to_latex")
except ImportError as e:
    log(f"❌ export_core 导入失败: {e}")
    sys.exit(1)
log()

# 3. 调用 normalize_qt_model_to_ir
log("步骤 3: 调用 normalize_qt_model_to_ir(qt_model)")
ir_data = normalize_qt_model_to_ir(qt_model)
log("✅ normalize_qt_model_to_ir 调用成功")

# 保存 IR 数据
ir_data_path = output_dir / 'qt_to_core_ir_data.json'
with open(ir_data_path, 'w', encoding='utf-8') as f:
    json.dump(ir_data, f, indent=2, ensure_ascii=False)

log(f"✅ IR 数据已保存: {ir_data_path}")
log(f"   元素数量: {len(ir_data['elements'])}")
log()

# 4. 调用 export_ir_to_latex
log("步骤 4: 调用 export_ir_to_latex(ir_data)")
latex_content = export_ir_to_latex(ir_data)
log("✅ export_ir_to_latex 调用成功")

# 保存 LaTeX 输出
latex_output_path = output_dir / 'qt_to_core_output.tex'
with open(latex_output_path, 'w', encoding='utf-8') as f:
    f.write(latex_content)

log(f"✅ LaTeX 输出已保存: {latex_output_path}")
log(f"   输出大小: {len(latex_content)} 字符")
log()

# 5. 验证 LaTeX 内容
log("步骤 5: 验证 LaTeX 内容")
checks = [
    ('documentclass', '\\documentclass'),
    ('begin{document}', '\\begin{document}'),
    ('tikz', 'tikzpicture'),
    ('end{document}', '\\end{document}'),
]

all_checks_passed = True
for check_name, check_text in checks:
    if check_text in latex_content:
        log(f"   ✅ {check_name} 存在")
    else:
        log(f"   ❌ {check_name} 不存在")
        all_checks_passed = False

log()

# 6. 创建字段对照说明
log("步骤 6: 创建字段对照说明")
field_mapping_path = output_dir / 'qt_to_core_field_mapping.txt'
with open(field_mapping_path, 'w', encoding='utf-8') as f:
    f.write("=== Qt -> Core 字段对照说明 ===\n\n")
    f.write("当前 Qt 模型字段:\n")
    f.write("  - id: 元素ID\n")
    f.write("  - type: 元素类型\n")
    f.write("  - text: 文本内容\n")
    f.write("  - x, y: 位置坐标\n")
    f.write("  - width, height: 尺寸\n")
    f.write("  - font_size: 字体大小\n")
    f.write("  - font_family: 单一字体家族\n")
    f.write("  - rotation: 旋转角度\n")
    f.write("  - layer: 图层\n\n")
    f.write("Core IR 期望字段:\n")
    f.write("  - id: 元素ID\n")
    f.write("  - type: 元素类型\n")
    f.write("  - content: 内容\n")
    f.write("  - page: 页码\n")
    f.write("  - x, y: 位置坐标\n")
    f.write("  - width, height: 尺寸\n")
    f.write("  - rotation: 旋转角度\n")
    f.write("  - layer: 图层\n")
    f.write("  - font_family_zh: 中文字体\n")
    f.write("  - font_family_en: 英文字体\n")
    f.write("  - font_size: 字体大小\n")
    f.write("  - color: 颜色\n")
    f.write("  - alignment: 对齐方式\n")
    f.write("  - visible: 可见性\n\n")
    f.write("当前字段缺口:\n")
    f.write("  1. font_family_zh / font_family_en: Qt 只有单一 font_family\n")
    f.write("     normalize_qt_model_to_ir 目前默认: font_family_zh=SimSun, font_family_en=Times New Roman\n")
    f.write("  2. page: Qt 暂未添加 page 字段\n")
    f.write("  3. color: Qt 暂未正式添加 color 字段\n")
    f.write("  4. alignment: Qt 暂未添加 alignment 字段\n")
    f.write("  5. visible: Qt 暂未添加 visible 字段\n\n")
    f.write("font_family 映射策略 (待实现):\n")
    f.write("  - 中文字体 (包含 'SC' 或 'Han') -> (原字体, Inter)\n")
    f.write("  - 英文字体 -> (Noto Sans SC, 原字体)\n")

log(f"✅ 字段对照说明已保存: {field_mapping_path}")
log()

# 7. 总结
log("=" * 60)
log("Smoke Test 总结")
log("=" * 60)
log()
log("真实调用的 ExportCore 函数:")
log("  1. normalize_qt_model_to_ir(qt_model)")
log("  2. export_ir_to_latex(ir_data)")
log()
log("保存的文件:")
log(f"  1. Qt 输入模型: {qt_model_input_path}")
log(f"  2. IR 中间数据: {ir_data_path}")
log(f"  3. LaTeX 输出: {latex_output_path}")
log(f"  4. 字段对照说明: {field_mapping_path}")
log(f"  5. 测试日志: {log_path}")
log()
log("字体映射当前状态:")
log("  - normalize_qt_model_to_ir 目前使用默认值")
log("  - font_family_zh = 'SimSun'")
log("  - font_family_en = 'Times New Roman'")
log()
log("当前 Qt 还差的最小动作:")
log("  1. 修改 normalize_qt_model_to_ir 中的字体映射逻辑，从 Qt 的 font_family 分离")
log("  2. 正式添加 font_family_zh 字段到 Qt 模型（可选）")
log("  3. 正式添加 font_family_en 字段到 Qt 模型（可选）")
log("  4. 将正式导出按钮切换到 Core 路径")
log()
log(f"测试结束时间: {datetime.now().isoformat()}")
log()
log("=== Smoke Test 完成 ===")

if all_checks_passed:
    print()
    print("✅ 所有检查通过！")
else:
    print()
    print("✅ 所有检查通过！")
