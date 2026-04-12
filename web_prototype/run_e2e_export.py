#!/usr/bin/env python3
"""
guiLaTeX Web 线 - 一键真实导出证据链脚本

功能：
1. 启动 Playwright 从浏览器真实导出 IR
2. 运行 web_to_core_bridge 生成 .tex
3. 对 .tex 做最小合法性检查
4. 保存证据到 repo-relative 目录
5. 运行旧的 Playwright regression 测试
"""

import os
import sys
import json
import subprocess
import re

# 项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 证据目录
EVIDENCE_DIR = os.path.join(PROJECT_ROOT, 'docs', 'contest_evidence', 'web_to_core_bridge')
# Web 原型目录
WEB_PROTOTYPE_DIR = os.path.join(PROJECT_ROOT, 'web_prototype')

# 输出文件路径
REAL_IR_PATH = os.path.join(WEB_PROTOTYPE_DIR, 'web_real_exported_ir.json')
TEX_OUTPUT_PATH = os.path.join(EVIDENCE_DIR, 'web_real_export_output.tex')
BRIDGE_SCRIPT = os.path.join(WEB_PROTOTYPE_DIR, 'web_to_core_bridge.py')
PLAYWRIGHT_IR_SCRIPT = os.path.join(WEB_PROTOTYPE_DIR, 'playwright_export_real_ir.js')
PLAYWRIGHT_REGRESSION_SCRIPT = os.path.join(WEB_PROTOTYPE_DIR, 'playwright_regression_test.js')

# 中间输出路径（temp）
TEMP_DIR = os.path.join(PROJECT_ROOT, 'temp', 'web_to_core')
TEMP_TEX_PATH = os.path.join(TEMP_DIR, 'web_real_export_output.tex')


def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"运行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        print("✅ 命令执行成功")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None


def export_real_ir():
    """从浏览器真实导出 IR"""
    print("\n====================================")
    print("1. 从浏览器真实导出 IR")
    print("====================================")
    
    result = run_command('node playwright_export_real_ir.js', cwd=WEB_PROTOTYPE_DIR)
    if result:
        print(f"✅ 真实 IR 已导出到: {REAL_IR_PATH}")
        return True
    else:
        print("❌ 真实 IR 导出失败")
        return False


def run_bridge():
    """运行 bridge 生成 .tex"""
    print("\n====================================")
    print("2. 运行 bridge 生成 .tex")
    print("====================================")
    
    # 确保 temp 目录存在
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    result = run_command('python3 web_to_core_bridge.py', cwd=WEB_PROTOTYPE_DIR)
    if result:
        # 复制到证据目录
        os.makedirs(EVIDENCE_DIR, exist_ok=True)
        if os.path.exists(TEMP_TEX_PATH):
            import shutil
            shutil.copy2(TEMP_TEX_PATH, TEX_OUTPUT_PATH)
            print(f"✅ .tex 文件已生成并复制到: {TEX_OUTPUT_PATH}")
            return True
        else:
            print(f"❌ 生成的 .tex 文件不存在: {TEMP_TEX_PATH}")
            return False
    else:
        print("❌ bridge 执行失败")
        return False


def check_latex_validity():
    """对 .tex 做最小合法性检查"""
    print("\n====================================")
    print("3. 对 .tex 做最小合法性检查")
    print("====================================")
    
    if not os.path.exists(TEX_OUTPUT_PATH):
        print(f"❌ .tex 文件不存在: {TEX_OUTPUT_PATH}")
        return False
    
    # 检查文件非空
    if os.path.getsize(TEX_OUTPUT_PATH) == 0:
        print("❌ .tex 文件为空")
        return False
    
    # 读取 .tex 内容
    with open(TEX_OUTPUT_PATH, 'r', encoding='utf-8') as f:
        latex_content = f.read()
    
    # 检查关键 LaTeX 控制字
    control_words = ['\\fontsize', '\\selectfont', '\\begin{document}', '\\end{document}']
    for control_word in control_words:
        if control_word not in latex_content:
            print(f"❌ 缺少关键控制字: {control_word}")
            return False
    
    # 检查反斜杠转义是否正确
    if 'font=\\fontsize' not in latex_content:
        print("❌ 反斜杠转义可能有问题")
        return False
    
    # 检查元素数量（从 IR 中读取）
    if os.path.exists(REAL_IR_PATH):
        with open(REAL_IR_PATH, 'r', encoding='utf-8') as f:
            ir_data = json.load(f)
        expected_elements = len(ir_data.get('elements', []))
        
        # 计算 .tex 中的元素数量（通过查找 \node 命令）
        node_count = len(re.findall(r'\\node\[', latex_content))
        
        if node_count >= expected_elements - 1:  # 允许误差 1
            print(f"✅ 元素数量检查通过: 期望至少 {expected_elements-1}, 实际 {node_count}")
        else:
            print(f"❌ 元素数量不匹配: 期望至少 {expected_elements-1}, 实际 {node_count}")
            return False
    
    # 检查关键文本内容
    key_contents = ['可视化编辑 LaTeX 文档', 'E = mc²']
    for key_content in key_contents:
        if key_content not in latex_content:
            print(f"❌ 缺少关键内容: {key_content}")
            return False
    
    print("✅ .tex 合法性检查通过")
    return True


def run_regression_tests():
    """运行旧的 Playwright regression 测试"""
    print("\n====================================")
    print("4. 运行旧的 Playwright regression 测试")
    print("====================================")
    
    result = run_command('node playwright_regression_test.js', cwd=WEB_PROTOTYPE_DIR)
    if result:
        # 复制回归测试日志到证据目录
        regression_log = os.path.join(WEB_PROTOTYPE_DIR, 'regression_test_log.txt')
        if os.path.exists(regression_log):
            import shutil
            shutil.copy2(regression_log, os.path.join(EVIDENCE_DIR, 'regression_test_log.txt'))
        print("✅ 回归测试通过")
        return True
    else:
        print("❌ 回归测试失败")
        return False


def archive_evidence():
    """归档证据"""
    print("\n====================================")
    print("5. 归档证据")
    print("====================================")
    
    # 确保证据目录存在
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    
    # 复制必要的文件到证据目录
    files_to_copy = [
        (REAL_IR_PATH, os.path.join(EVIDENCE_DIR, 'web_real_exported_ir.json')),
        (BRIDGE_SCRIPT, os.path.join(EVIDENCE_DIR, 'web_to_core_bridge.py')),
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            import shutil
            shutil.copy2(src, dst)
            print(f"✅ 已归档: {os.path.basename(src)}")
        else:
            print(f"⚠️  文件不存在: {src}")
    
    print("✅ 证据归档完成")
    return True


def main():
    """主函数"""
    print("====================================")
    print("guiLaTeX Web 线 - 一键真实导出证据链")
    print("====================================")
    
    # 执行流程
    steps = [
        ("导出真实 IR", export_real_ir),
        ("运行 bridge", run_bridge),
        ("检查 .tex 合法性", check_latex_validity),
        ("运行回归测试", run_regression_tests),
        ("归档证据", archive_evidence),
    ]
    
    all_success = True
    for step_name, step_func in steps:
        if not step_func():
            all_success = False
    
    print("\n====================================")
    print("一键真实导出证据链 - 总结")
    print("====================================")
    
    if all_success:
        print("🎉 所有步骤执行成功！")
        print(f"真实 IR 路径: {REAL_IR_PATH}")
        print(f"最终 .tex 证据路径: {TEX_OUTPUT_PATH}")
        return 0
    else:
        print("💥 部分步骤执行失败！")
        return 1


if __name__ == "__main__":
    sys.exit(main())
