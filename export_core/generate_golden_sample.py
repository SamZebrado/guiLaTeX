#!/usr/bin/env python3

import json
import os
from latex_exporter import LatexExporter

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 读取 IR JSON 文件
ir_path = os.path.join(script_dir, 'samples', 'golden_sample_ir.json')
with open(ir_path, 'r', encoding='utf-8') as f:
    ir_data = json.load(f)

# 创建导出器并生成 LaTeX
exporter = LatexExporter()
latex_output = exporter.export(ir_data)

# 保存 LaTeX 输出到文件
latex_path = os.path.join(script_dir, 'samples', 'golden_sample_latex.tex')
with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(latex_output)

print("Golden sample LaTeX generated successfully!")
print(f"IR JSON: {ir_path}")
print(f"LaTeX output: {latex_path}")
