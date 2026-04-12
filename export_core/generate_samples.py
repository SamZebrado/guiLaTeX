#!/usr/bin/env python3

import json
import os
from latex_exporter import LatexExporter

def _validate_path(path: str, base_dir: str) -> str:
    """Validate that path is within base_dir"""
    abs_path = os.path.abspath(path)
    abs_base = os.path.abspath(base_dir)
    if not abs_path.startswith(abs_base):
        raise ValueError(f"Path {path} is outside base directory {base_dir}")
    return abs_path

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
samples_dir = os.path.join(script_dir, 'samples')

# 样例文件列表
samples = [
    'golden_sample_ir',
    'regression_sample_1_rotation',
    'regression_sample_2_layers',
    'regression_sample_3_same_layer',
    'regression_sample_4_fonts',
    'regression_sample_5_rotation_layer'
]

# 创建导出器
exporter = LatexExporter()

# 处理每个样例
for sample_name in samples:
    json_path = os.path.join(samples_dir, f'{sample_name}.json')
    tex_path = os.path.join(samples_dir, f'{sample_name}.tex')
    
    try:
        # 验证路径
        json_path = _validate_path(json_path, samples_dir)
        tex_path = _validate_path(tex_path, samples_dir)
        
        # 读取 IR JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            ir_data = json.load(f)
        
        # 生成 LaTeX
        latex_output = exporter.export(ir_data)
        
        # 保存 LaTeX 输出到文件
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_output)
        
        print(f"✓ 成功生成: {tex_path}")
    except Exception as e:
        print(f"✗ 生成失败 {sample_name}: 处理过程中出现错误")
        # 可以添加日志记录
        # import logging
        # logging.error(f"Error processing {sample_name}: {e}")

print("\n所有样例处理完成！")
