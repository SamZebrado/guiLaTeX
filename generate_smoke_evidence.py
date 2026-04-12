#!/usr/bin/env python3
"""生成 Qt -> Core smoke test 证据文件"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# 准备输出目录
output_dir = Path(__file__).parent / 'docs' / 'contest_evidence' / 'screenshots'
output_dir.mkdir(parents=True, exist_ok=True)

# 1. 读取 Qt 输入模型
qt_model_path = output_dir / 'qt_to_core_input_model.json'
with open(qt_model_path, 'r', encoding='utf-8') as f:
    qt_model = json.load(f)

# 2. 导入 ExportCore 函数
from export_core import normalize_qt_model_to_ir, export_ir_to_latex

# 3. 调用 normalize_qt_model_to_ir
ir_data = normalize_qt_model_to_ir(qt_model)

# 4. 保存 IR 数据
ir_data_path = output_dir / 'qt_to_core_ir_data.json'
with open(ir_data_path, 'w', encoding='utf-8') as f:
    json.dump(ir_data, f, indent=2, ensure_ascii=False)

print(f"✅ IR 数据已保存: {ir_data_path}")

# 5. 调用 export_ir_to_latex
latex_content = export_ir_to_latex(ir_data)

# 6. 保存 LaTeX 输出
latex_output_path = output_dir / 'qt_to_core_output.tex'
with open(latex_output_path, 'w', encoding='utf-8') as f:
    f.write(latex_content)

print(f"✅ LaTeX 输出已保存: {latex_output_path}")

# 7. 创建字段对照说明
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

print(f"✅ 字段对照说明已保存: {field_mapping_path}")

# 8. 创建测试日志
log_path = output_dir / 'qt_to_core_smoke_test_log.txt'
with open(log_path, 'w', encoding='utf-8') as f:
    f.write(f"测试开始时间: {datetime.now().isoformat()}\n")
    f.write("=" * 60 + "\n\n")
    f.write("步骤 1: 准备 Qt 模型数据\n")
    f.write(f"✅ Qt 输入模型已保存: {qt_model_path}\n")
    f.write(f"   元素数量: {len(qt_model['elements'])}\n\n")
    f.write("步骤 2: 导入 ExportCore\n")
    f.write("✅ export_core 模块导入成功\n")
    f.write("   可用函数: normalize_qt_model_to_ir, export_ir_to_latex\n\n")
    f.write("步骤 3: 调用 normalize_qt_model_to_ir(qt_model)\n")
    f.write("✅ normalize_qt_model_to_ir 调用成功\n")
    f.write(f"✅ IR 数据已保存: {ir_data_path}\n")
    f.write(f"   元素数量: {len(ir_data['elements'])}\n\n")
    f.write("步骤 4: 调用 export_ir_to_latex(ir_data)\n")
    f.write("✅ export_ir_to_latex 调用成功\n")
    f.write(f"✅ LaTeX 输出已保存: {latex_output_path}\n")
    f.write(f"   输出大小: {len(latex_content)} 字符\n\n")
    f.write("步骤 5: 验证 LaTeX 内容\n")
    checks = [
        ('documentclass', '\\documentclass'),
        ('begin{document}', '\\begin{document}'),
        ('tikz', 'tikzpicture'),
        ('end{document}', '\\end{document}'),
    ]
    all_checks_passed = True
    for check_name, check_text in checks:
        if check_text in latex_content:
            f.write(f"   ✅ {check_name} 存在\n")
        else:
            f.write(f"   ❌ {check_name} 不存在\n")
            all_checks_passed = False
    f.write("\n")
    f.write("=" * 60 + "\n")
    f.write("Smoke Test 总结\n")
    f.write("=" * 60 + "\n\n")
    f.write("真实调用的 ExportCore 函数:\n")
    f.write("  1. normalize_qt_model_to_ir(qt_model)\n")
    f.write("  2. export_ir_to_latex(ir_data)\n\n")
    f.write("保存的文件:\n")
    f.write(f"  1. Qt 输入模型: {qt_model_path}\n")
    f.write(f"  2. IR 中间数据: {ir_data_path}\n")
    f.write(f"  3. LaTeX 输出: {latex_output_path}\n")
    f.write(f"  4. 字段对照说明: {field_mapping_path}\n")
    f.write(f"  5. 测试日志: {log_path}\n\n")
    f.write("字体映射当前状态:\n")
    f.write("  - normalize_qt_model_to_ir 目前使用默认值\n")
    f.write("  - font_family_zh = 'SimSun'\n")
    f.write("  - font_family_en = 'Times New Roman'\n\n")
    f.write("当前 Qt 还差的最小动作:\n")
    f.write("  1. 修改 normalize_qt_model_to_ir 中的字体映射逻辑，从 Qt 的 font_family 分离\n")
    f.write("  2. 正式添加 font_family_zh 字段到 Qt 模型（可选）\n")
    f.write("  3. 正式添加 font_family_en 字段到 Qt 模型（可选）\n")
    f.write("  4. 将正式导出按钮切换到 Core 路径\n\n")
    f.write(f"测试结束时间: {datetime.now().isoformat()}\n\n")
    f.write("=== Smoke Test 完成 ===\n")

print(f"✅ 测试日志已保存: {log_path}")
print("\n✅ 所有证据文件生成完成！")
