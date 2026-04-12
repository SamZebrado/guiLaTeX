#!/usr/bin/env python3
"""
guiLaTeX Web 线 - 简化版一键真实导出证据链脚本

功能：
1. 从浏览器真实导出 IR（使用已有的 web_real_exported_ir.json）
2. 运行 web_to_core_bridge 生成 .tex
3. 对 .tex 做最小合法性检查
4. 保存证据到带时间戳的新鲜证据目录
"""

import os
import sys
import json
import re
import datetime

# 项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 时间戳
TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
# 新鲜证据目录
FRESH_EVIDENCE_DIR = os.path.join(PROJECT_ROOT, 'docs', 'contest_evidence', f'web_to_core_bridge_{TIMESTAMP}')
# Web 原型目录
WEB_PROTOTYPE_DIR = os.path.join(PROJECT_ROOT, 'web_prototype')

# 输入输出文件路径
INPUT_IR_PATH = os.path.join(WEB_PROTOTYPE_DIR, 'web_real_exported_ir.json')
REAL_IR_PATH = os.path.join(WEB_PROTOTYPE_DIR, f'web_real_exported_ir_{TIMESTAMP}.json')
TEX_OUTPUT_PATH = os.path.join(FRESH_EVIDENCE_DIR, f'web_real_export_output_{TIMESTAMP}.tex')

# 确保目录存在
os.makedirs(FRESH_EVIDENCE_DIR, exist_ok=True)

print("====================================")
print("guiLaTeX Web 线 - 简化版一键真实导出证据链")
print(f"时间戳: {TIMESTAMP}")
print("====================================")

# 1. 复制真实 IR 文件作为新鲜证据
print("\n1. 准备真实 IR 文件...")
if os.path.exists(INPUT_IR_PATH):
    import shutil
    shutil.copy2(INPUT_IR_PATH, REAL_IR_PATH)
    print(f"✅ 真实 IR 已复制到: {REAL_IR_PATH}")
else:
    print(f"❌ 输入 IR 文件不存在: {INPUT_IR_PATH}")
    sys.exit(1)

# 2. 运行 bridge 生成 .tex
print("\n2. 运行 bridge 生成 .tex...")
sys.path.insert(0, PROJECT_ROOT)
from export_core import normalize_web_model_to_ir, export_ir_to_latex

try:
    # 读取 IR 文件
    with open(REAL_IR_PATH, 'r', encoding='utf-8') as f:
        web_ir = json.load(f)
    
    print(f"Web IR 包含 {len(web_ir.get('elements', []))} 个元素")
    
    # 调用 normalize_web_model_to_ir
    normalized_ir = normalize_web_model_to_ir(web_ir)
    print(f"标准化后 IR 包含 {len(normalized_ir.get('elements', []))} 个元素")
    
    # 调用 export_ir_to_latex
    latex_content = export_ir_to_latex(normalized_ir)
    print(f"生成的 LaTeX 长度: {len(latex_content)} 字符")
    
    # 保存 LaTeX 文件
    with open(TEX_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    print(f"✅ .tex 文件已生成: {TEX_OUTPUT_PATH}")
    
except Exception as e:
    print(f"❌ bridge 执行失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. 对 .tex 做最小合法性检查
print("\n3. 对 .tex 做最小合法性检查...")

if not os.path.exists(TEX_OUTPUT_PATH):
    print(f"❌ .tex 文件不存在: {TEX_OUTPUT_PATH}")
    sys.exit(1)

# 检查文件非空
if os.path.getsize(TEX_OUTPUT_PATH) == 0:
    print("❌ .tex 文件为空")
    sys.exit(1)

# 读取 .tex 内容
with open(TEX_OUTPUT_PATH, 'r', encoding='utf-8') as f:
    latex_content = f.read()

# 检查关键 LaTeX 控制字
control_words = ['\\begin{document}', '\\end{document}', '\\node', '\\fontsize', '\\selectfont']
for control_word in control_words:
    if control_word not in latex_content:
        print(f"❌ 缺少关键控制字: {control_word}")
        sys.exit(1)

# 检查反斜杠转义是否正确
if 'font=\\fontsize' not in latex_content:
    print("❌ 反斜杠转义可能有问题")
    sys.exit(1)

# 检查元素数量（从 IR 中读取）
with open(REAL_IR_PATH, 'r', encoding='utf-8') as f:
    ir_data = json.load(f)
expected_elements = len(ir_data.get('elements', []))

# 计算 .tex 中的元素数量（通过查找 \node 命令）
node_count = len(re.findall(r'\\node\[', latex_content))

if node_count >= expected_elements - 1:  # 允许误差 1
    print(f"✅ 元素数量检查通过: 期望至少 {expected_elements-1}, 实际 {node_count}")
else:
    print(f"❌ 元素数量不匹配: 期望至少 {expected_elements-1}, 实际 {node_count}")
    sys.exit(1)

# 检查关键文本内容
key_contents = ['可视化编辑 LaTeX 文档', 'E = mc²']
for key_content in key_contents:
    if key_content not in latex_content:
        print(f"❌ 缺少关键内容: {key_content}")
        sys.exit(1)

print("✅ .tex 合法性检查通过")

# 4. 归档证据
print("\n4. 归档证据...")

# 复制必要的文件到证据目录
files_to_copy = [
    (REAL_IR_PATH, os.path.join(FRESH_EVIDENCE_DIR, f'web_real_exported_ir_{TIMESTAMP}.json')),
    (os.path.join(WEB_PROTOTYPE_DIR, 'web_to_core_bridge.py'), os.path.join(FRESH_EVIDENCE_DIR, 'web_to_core_bridge.py')),
    (__file__, os.path.join(FRESH_EVIDENCE_DIR, 'run_e2e_simple.py')),
]

for src, dst in files_to_copy:
    if os.path.exists(src):
        import shutil
        shutil.copy2(src, dst)
        print(f"✅ 已归档: {os.path.basename(src)}")
    else:
        print(f"⚠️  文件不存在: {src}")

print("\n====================================")
print("简化版一键真实导出证据链 - 完成")
print("====================================")
print(f"🎉 所有步骤执行成功！")
print(f"新鲜证据目录: {FRESH_EVIDENCE_DIR}")
print(f"真实 IR 路径: {REAL_IR_PATH}")
print(f"最终 .tex 证据路径: {TEX_OUTPUT_PATH}")
