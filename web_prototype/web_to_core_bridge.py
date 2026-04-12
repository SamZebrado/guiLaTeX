#!/usr/bin/env python3
"""
Web to ExportCore 最小桥接脚本

功能：
1. 从 Web 导出的 IR 文件读取数据
2. 调用 ExportCore 的 normalize_web_model_to_ir 函数
3. 调用 ExportCore 的 export_ir_to_latex 函数
4. 生成 .tex 文件
5. 保存结果到明确位置
"""

import json
import os
import sys

# 添加项目根目录到路径，以便导入 export_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from export_core import normalize_web_model_to_ir, export_ir_to_latex

def web_to_core_bridge(web_ir_path, output_tex_path):
    """
    执行 Web 到 ExportCore 的桥接
    
    Args:
        web_ir_path: Web 导出的 IR 文件路径
        output_tex_path: 输出的 LaTeX 文件路径
    """
    try:
        # 1. 读取 Web 导出的 IR 文件
        print(f"读取 Web IR 文件: {web_ir_path}")
        with open(web_ir_path, 'r', encoding='utf-8') as f:
            web_ir = json.load(f)
        
        print(f"Web IR 包含 {len(web_ir.get('elements', []))} 个元素")
        
        # 2. 调用 normalize_web_model_to_ir
        print("调用 normalize_web_model_to_ir...")
        normalized_ir = normalize_web_model_to_ir(web_ir)
        print(f"标准化后 IR 包含 {len(normalized_ir.get('elements', []))} 个元素")
        
        # 3. 调用 export_ir_to_latex
        print("调用 export_ir_to_latex...")
        latex_content = export_ir_to_latex(normalized_ir)
        print(f"生成的 LaTeX 长度: {len(latex_content)} 字符")
        
        # 4. 保存 LaTeX 文件
        print(f"保存 LaTeX 文件: {output_tex_path}")
        os.makedirs(os.path.dirname(output_tex_path), exist_ok=True)
        with open(output_tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print("\n✅ 桥接成功！")
        print(f"输入: {web_ir_path}")
        print(f"输出: {output_tex_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 桥接失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # 输入输出路径 - 使用真实浏览器导出的 IR
    web_ir_path = os.path.join(os.path.dirname(__file__), 'web_real_exported_ir.json')
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'temp', 'web_to_core')
    output_tex_path = os.path.join(output_dir, 'web_real_export_output.tex')
    
    # 执行桥接
    success = web_to_core_bridge(web_ir_path, output_tex_path)
    
    if success:
        print("\n🎉 桥接完成！")
        print(f"LaTeX 文件已保存到: {output_tex_path}")
        return 0
    else:
        print("\n💥 桥接失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())
