#!/usr/bin/env bash
# 状态同步脚本 - 确保所有状态文件与单一真相源保持一致
set -euo pipefail

RAM_DISK_PATH="${COMMS_RAM_ROOT:-/tmp/trae_multi_agent_ram}"
STATE_FILE="$RAM_DISK_PATH/state/CURRENT_RUN_STATE.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[SYNC]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 检查状态文件是否存在
if [ ! -f "$STATE_FILE" ]; then
    warn "状态文件不存在: $STATE_FILE"
    exit 1
fi

# 从CURRENT_RUN_STATE.json同步到STATUS.md
sync_status_md() {
    local status_file="STATUS.md"
    
    if [ ! -f "$status_file" ]; then
        warn "STATUS.md 不存在，跳过同步"
        return
    fi
    
    log "同步 STATUS.md..."
    
    python3 - "$STATE_FILE" "$status_file" << 'PYEOF'
import json, sys, re
from datetime import datetime

state_file, status_file = sys.argv[1:3]

with open(state_file, 'r') as f:
    state = json.load(f)

# 读取现有STATUS.md
with open(status_file, 'r') as f:
    content = f.read()

# 更新Current goal部分
run_status = state['run']['status']
current_phase = state['run']['current_phase']
current_task = state['current_task']

# 生成新的状态内容
new_content = f"""# STATUS

## Current goal
- 运行状态: {run_status}
- 当前阶段: {current_phase}
- 当前任务: {current_task.get('objective', 'None') if current_task.get('id') else 'None'}

## What is currently true
"""

# 添加Agent状态
for agent, info in state['agents'].items():
    status = "✅ 运行中" if info['alive'] else "❌ 已停止"
    pending = info.get('pending_messages', 0)
    new_content += f"- {agent}: {status}, 待处理消息: {pending}\n"

# 添加完成层级
tiers = state.get('completion_tiers', {})
new_content += f"""
## Completion Tiers
- scaffold_done: {'✅' if tiers.get('scaffold_done') else '❌'}
- code_done: {'✅' if tiers.get('code_done') else '❌'}
- test_done: {'✅' if tiers.get('test_done') else '❌'}
- verified_done: {'✅' if tiers.get('verified_done') else '❌'}

## Current blockers
- None

## Current risks
- None

## Source-of-truth files
- CURRENT_RUN_STATE.json (单一真相源)
- RUN_LEDGER.md (任务记录)
- STATUS.md (本文件)

## Last updated
- {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""

# 写回文件
with open(status_file, 'w') as f:
    f.write(new_content)

print("STATUS.md 已更新")
PYEOF
}

# 从CURRENT_RUN_STATE.json同步到PLAN.md
sync_plan_md() {
    local plan_file="PLAN.md"
    
    if [ ! -f "$plan_file" ]; then
        warn "PLAN.md 不存在，跳过同步"
        return
    fi
    
    log "同步 PLAN.md..."
    
    python3 - "$STATE_FILE" "$plan_file" << 'PYEOF'
import json, sys
from datetime import datetime

state_file, plan_file = sys.argv[1:3]

with open(state_file, 'r') as f:
    state = json.load(f)

# 读取现有PLAN.md
with open(plan_file, 'r') as f:
    content = f.read()

# 更新Active tasks部分
current_task = state['current_task']

if current_task.get('id'):
    # 在文件开头添加当前任务信息
    task_info = f"""
## Current Active Task (from CURRENT_RUN_STATE.json)

### {current_task.get('id', 'Unknown')}
- **Objective**: {current_task.get('objective', 'N/A')}
- **Owner**: {current_task.get('owner', 'N/A')}
- **Status**: {current_task.get('status', 'N/A')}
- **Started**: {current_task.get('started_at', 'N/A')}

---

"""
    
    # 在第一个## Active tasks之前插入
    if '## Active tasks' in content:
        content = content.replace('## Active tasks', task_info + '## Active tasks', 1)
    else:
        content = task_info + content

# 写回文件
with open(plan_file, 'w') as f:
    f.write(content)

print("PLAN.md 已更新")
PYEOF
}

# 更新RUN_LEDGER.md
sync_run_ledger() {
    local ledger_file="RUN_LEDGER.md"
    
    if [ ! -f "$ledger_file" ]; then
        warn "RUN_LEDGER.md 不存在，跳过同步"
        return
    fi
    
    log "同步 RUN_LEDGER.md..."
    
    python3 - "$STATE_FILE" "$ledger_file" << 'PYEOF'
import json, sys
from datetime import datetime

state_file, ledger_file = sys.argv[1:3]

with open(state_file, 'r') as f:
    state = json.load(f)

# 读取现有RUN_LEDGER.md
with open(ledger_file, 'r') as f:
    content = f.read()

# 更新Agent状态摘要部分
agent_summary = "\n## Agent状态摘要\n\n"
agent_summary += "| Agent | 状态 | 当前任务 | 待处理消息 |\n"
agent_summary += "|-------|------|----------|-----------|\n"

for agent, info in state['agents'].items():
    status = "✅ 活跃" if info['alive'] else "❌ 停止"
    job = info.get('current_job', '空闲') or '空闲'
    pending = info.get('pending_messages', 0)
    agent_summary += f"| {agent} | {status} | {job} | {pending} |\n"

# 替换Agent状态摘要部分
if '## Agent状态摘要' in content:
    # 找到下一个##之前的内容并替换
    import re
    pattern = r'## Agent状态摘要.*?(?=\n## |\Z)'
    content = re.sub(pattern, agent_summary.rstrip(), content, flags=re.DOTALL)
else:
    # 在文件末尾添加
    content += "\n" + agent_summary

# 写回文件
with open(ledger_file, 'w') as f:
    f.write(content)

print("RUN_LEDGER.md 已更新")
PYEOF
}

# 主函数
main() {
    log "开始状态同步..."
    
    sync_status_md
    sync_plan_md
    sync_run_ledger
    
    log "状态同步完成"
}

main "$@"
