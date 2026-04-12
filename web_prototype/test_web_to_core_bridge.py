#!/usr/bin/env python3
"""
Web to ExportCore 桥接的最小 smoke test

功能：
1. 验证 Web IR 样例文件存在
2. 验证桥接脚本可以运行
3. 验证生成的 LaTeX 文件存在
4. 验证生成的 LaTeX 文件包含关键内容
"""

import os
import sys

def test_web_to_core_bridge():
    """
    运行 Web to ExportCore 桥接的 smoke test
    """
    print("=== Web to ExportCore Bridge Smoke Test ===")
    
    # 检查 Web IR 样例文件
    web_ir_path = os.path.join(os.path.dirname(__file__), 'web_ir_sample.json')
    if not os.path.exists(web_ir_path):
        print(f"❌ Web IR 样例文件不存在: {web_ir_path}")
        return False
    print(f"✅ Web IR 样例文件存在: {web_ir_path}")
    
    # 运行桥接脚本
    print("\n运行桥接脚本...")
    bridge_script = os.path.join(os.path.dirname(__file__), 'web_to_core_bridge.py')
    try:
        result = os.system(f'python3 "{bridge_script}"')
        if result != 0:
            print(f"❌ 桥接脚本运行失败，返回码: {result}")
            return False
        print("✅ 桥接脚本运行成功")
    except Exception as e:
        print(f"❌ 桥接脚本运行异常: {e}")
        return False
    
    # 检查生成的 LaTeX 文件
    output_tex_path = os.path.join(os.path.dirname(__file__), '..', 'temp', 'web_to_core', 'web_to_core_output.tex')
    if not os.path.exists(output_tex_path):
        print(f"❌ 生成的 LaTeX 文件不存在: {output_tex_path}")
        return False
    print(f"✅ 生成的 LaTeX 文件存在: {output_tex_path}")
    
    # 检查 LaTeX 文件内容
    try:
        with open(output_tex_path, 'r', encoding='utf-8') as f:
            latex_content = f.read()
        
        # 检查关键内容
        check_points = [
            '\\documentclass{article}',
            '标题：可视化编辑 LaTeX 文档',
            '作者：某某',
            '这是一段用于演示段落对象的正文内容',
            'E = mc²',
            '\\includegraphics',
            '\\end{document}'
        ]
        
        all_found = True
        for check in check_points:
            if check in latex_content:
                print(f"  ✅ 找到: {check}")
            else:
                print(f"  ❌ 未找到: {check}")
                all_found = False
        
        if all_found:
            print("✅ LaTeX 文件包含所有关键内容")
        else:
            print("❌ LaTeX 文件缺少关键内容")
            return False
            
    except Exception as e:
        print(f"❌ 检查 LaTeX 文件内容失败: {e}")
        return False
    
    print("\n🎉 所有测试通过！Web to ExportCore 桥接链路正常。")
    return True

def main():
    success = test_web_to_core_bridge()
    if success:
        print("\n✅ Smoke test 通过！")
        return 0
    else:
        print("\n❌ Smoke test 失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())
