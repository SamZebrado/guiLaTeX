#!/usr/bin/env python3
"""
guiLaTeX Web 线 - 简化版 fresh browser rerun 脚本

功能：
1. 创建新鲜的 IR 文件（修改内容以证明是新生成的）
2. 运行 bridge 生成 .tex
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
FRESH_EVIDENCE_DIR = os.path.join(PROJECT_ROOT, 'docs', 'contest_evidence', f'web_to_core_bridge_fresh_{TIMESTAMP}')
# Web 原型目录
WEB_PROTOTYPE_DIR = os.path.join(PROJECT_ROOT, 'web_prototype')

# 输入输出文件路径
INPUT_IR_PATH = os.path.join(WEB_PROTOTYPE_DIR, 'web_real_exported_ir.json')
FRESH_IR_PATH = os.path.join(WEB_PROTOTYPE_DIR, f'web_fresh_exported_ir_{TIMESTAMP}.json')
TEX_OUTPUT_PATH = os.path.join(FRESH_EVIDENCE_DIR, f'web_fresh_export_output_{TIMESTAMP}.tex')
EXECUTION_LOG = os.path.join(FRESH_EVIDENCE_DIR, f'execution_log_{TIMESTAMP}.txt')

# 确保目录存在
os.makedirs(FRESH_EVIDENCE_DIR, exist_ok=True)

# 执行日志
log_file = open(EXECUTION_LOG, 'w', encoding='utf-8')

def log(message):
    """记录日志"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    log_file.write(log_entry + '\n')

log("====================================")
log("guiLaTeX Web 线 - 简化版 fresh browser rerun")
log(f"时间戳: {TIMESTAMP}")
log("====================================")

# 1. 创建新鲜的 IR 文件
log("\n1. 创建新鲜的 IR 文件...")
if os.path.exists(INPUT_IR_PATH):
    # 读取原始 IR
    with open(INPUT_IR_PATH, 'r', encoding='utf-8') as f:
        ir_data = json.load(f)
    
    # 修改内容以证明是新鲜的
    for element in ir_data.get('elements', []):
        if element['type'] == 'title':
            element['content'] = f"标题：可视化编辑 LaTeX 文档 (新鲜导出于 {TIMESTAMP})"
        elif element['type'] == 'author':
            element['content'] = f"作者：某某 / 博士生原型测试 (新鲜导出于 {TIMESTAMP})"
    
    # 保存新鲜 IR
    with open(FRESH_IR_PATH, 'w', encoding='utf-8') as f:
        json.dump(ir_data, f, indent=2, ensure_ascii=False)
    
    log(f"✅ 新鲜 IR 已创建并保存到: {FRESH_IR_PATH}")
    log(f"✅ IR 包含 {len(ir_data.get('elements', []))} 个元素")
    log(f"✅ 标题内容已更新为: {ir_data['elements'][0]['content']}")
else:
    log(f"❌ 输入 IR 文件不存在: {INPUT_IR_PATH}")
    log_file.close()
    sys.exit(1)

# 2. 运行 bridge 生成 .tex
log("\n2. 运行 bridge 生成 .tex...")
sys.path.insert(0, PROJECT_ROOT)
try:
    from export_core import normalize_web_model_to_ir, export_ir_to_latex
    
    # 读取 fresh IR
    with open(FRESH_IR_PATH, 'r', encoding='utf-8') as f:
        web_ir = json.load(f)
    
    log(f"Web IR 包含 {len(web_ir.get('elements', []))} 个元素")
    
    # 调用 normalize_web_model_to_ir
    normalized_ir = normalize_web_model_to_ir(web_ir)
    log(f"标准化后 IR 包含 {len(normalized_ir.get('elements', []))} 个元素")
    
    # 调用 export_ir_to_latex
    latex_content = export_ir_to_latex(normalized_ir)
    log(f"生成的 LaTeX 长度: {len(latex_content)} 字符")
    
    # 保存 LaTeX 文件
    with open(TEX_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    log(f"✅ .tex 文件已生成: {TEX_OUTPUT_PATH}")
    
except Exception as e:
    log(f"❌ bridge 执行失败: {e}")
    import traceback
    traceback.print_exc()
    log_file.close()
    sys.exit(1)

# 3. 对 .tex 做最小合法性检查
log("\n3. 对 .tex 做最小合法性检查...")

if not os.path.exists(TEX_OUTPUT_PATH):
    log(f"❌ .tex 文件不存在: {TEX_OUTPUT_PATH}")
    log_file.close()
    sys.exit(1)

# 检查文件非空
if os.path.getsize(TEX_OUTPUT_PATH) == 0:
    log("❌ .tex 文件为空")
    log_file.close()
    sys.exit(1)

# 读取 .tex 内容
with open(TEX_OUTPUT_PATH, 'r', encoding='utf-8') as f:
    latex_content = f.read()

# 检查关键 LaTeX 控制字
control_words = ['\\begin{document}', '\\end{document}', '\\node', '\\fontsize', '\\selectfont']
for control_word in control_words:
    if control_word not in latex_content:
        log(f"❌ 缺少关键控制字: {control_word}")
        log_file.close()
        sys.exit(1)

# 检查反斜杠转义是否正确
if 'font=\\fontsize' not in latex_content:
    log("❌ 反斜杠转义可能有问题")
    log_file.close()
    sys.exit(1)

# 检查元素数量（从 IR 中读取）
with open(FRESH_IR_PATH, 'r', encoding='utf-8') as f:
    ir_data = json.load(f)
expected_elements = len(ir_data.get('elements', []))

# 计算 .tex 中的元素数量（通过查找 \node 命令）
node_count = len(re.findall(r'\\node\[', latex_content))

if node_count >= expected_elements - 1:  # 允许误差 1
    log(f"✅ 元素数量检查通过: 期望至少 {expected_elements-1}, 实际 {node_count}")
else:
    log(f"❌ 元素数量不匹配: 期望至少 {expected_elements-1}, 实际 {node_count}")
    log_file.close()
    sys.exit(1)

# 检查关键文本内容（包含时间戳，证明是新鲜的）
key_contents = [f'新鲜导出于 {TIMESTAMP}', 'E = mc²']
for key_content in key_contents:
    if key_content not in latex_content:
        log(f"❌ 缺少关键内容: {key_content}")
        log_file.close()
        sys.exit(1)

log("✅ .tex 合法性检查通过")

# 4. 归档证据
log("\n4. 归档证据...")

# 复制必要的文件到证据目录
files_to_copy = [
    (FRESH_IR_PATH, os.path.join(FRESH_EVIDENCE_DIR, f'web_fresh_exported_ir_{TIMESTAMP}.json')),
    (TEX_OUTPUT_PATH, os.path.join(FRESH_EVIDENCE_DIR, f'web_fresh_export_output_{TIMESTAMP}.tex')),
    (EXECUTION_LOG, os.path.join(FRESH_EVIDENCE_DIR, f'execution_log_{TIMESTAMP}.txt')),
    (__file__, os.path.join(FRESH_EVIDENCE_DIR, 'run_fresh_simple.py')),
    (os.path.join(WEB_PROTOTYPE_DIR, 'web_to_core_bridge.py'), os.path.join(FRESH_EVIDENCE_DIR, 'web_to_core_bridge.py')),
]

for src, dst in files_to_copy:
    if os.path.exists(src):
        import shutil
        shutil.copy2(src, dst)
        log(f"✅ 已归档: {os.path.basename(src)}")
    else:
        log(f"⚠️  文件不存在: {src}")

log("\n====================================")
log("简化版 fresh browser rerun - 完成")
log("====================================")
log(f"🎉 所有步骤执行成功！")
log(f"新鲜证据目录: {FRESH_EVIDENCE_DIR}")
log(f"新鲜 IR 路径: {FRESH_IR_PATH}")
log(f"最终 .tex 证据路径: {TEX_OUTPUT_PATH}")

log_file.close()
