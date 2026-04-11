#!/usr/bin/env bash
set -euo pipefail

# 启动多Agent系统的脚本

# 内存盘路径（默认使用/Volumes/TraeRAM，如果不存在则使用/tmp）
RAM_DISK_PATH="/Volumes/TraeRAM"
if [ ! -d "$RAM_DISK_PATH" ]; then
    RAM_DISK_PATH="/tmp/trae_multi_agent_ram"
    echo "警告: 内存盘不存在，使用 $RAM_DISK_PATH 作为备选"
    mkdir -p "$RAM_DISK_PATH"
fi

# 创建必要的目录结构
mkdir -p "$RAM_DISK_PATH/logs" "$RAM_DISK_PATH/state" "$RAM_DISK_PATH/inbox" "$RAM_DISK_PATH/processed" "$RAM_DISK_PATH/outbox" "$RAM_DISK_PATH/threads"

# 复制Agent注册表
if [ -f "trae_multi_agent_ram/state/agents.tsv" ]; then
    cp "trae_multi_agent_ram/state/agents.tsv" "$RAM_DISK_PATH/state/"
    echo "已复制Agent注册表"
else
    echo "创建默认Agent注册表"
    cat > "$RAM_DISK_PATH/state/agents.tsv" << EOF
Agent名称	角色	轮询间隔(秒)
Manager	manager	30
Planner	planner	60
Builder	builder	60
Reviewer	reviewer	60
Documenter	documenter	120
EOF
fi

# 启动Manager Agent
echo "启动Manager Agent..."
export COMMS_RAM_ROOT="$RAM_DISK_PATH"
export AGENT_NAME="Manager"
export AGENT_ROLE="manager"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=30
export AGENT_POLL_JITTER_SEC=10

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 在后台启动Manager Agent
bash "$PROJECT_ROOT/.trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh" &
MANAGER_PID=$!
echo "Manager Agent 已启动 (PID: $MANAGER_PID)"

# 等待1秒
sleep 1

# 启动Planner Agent
echo "启动Planner Agent..."
export COMMS_RAM_ROOT="$RAM_DISK_PATH"
export AGENT_NAME="Planner"
export AGENT_ROLE="planner"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=60
export AGENT_POLL_JITTER_SEC=10

# 在后台启动Planner Agent
bash "$PROJECT_ROOT/.trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh" &
PLANNER_PID=$!
echo "Planner Agent 已启动 (PID: $PLANNER_PID)"

# 等待1秒
sleep 1

# 启动Builder Agent
echo "启动Builder Agent..."
export COMMS_RAM_ROOT="$RAM_DISK_PATH"
export AGENT_NAME="Builder"
export AGENT_ROLE="builder"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=60
export AGENT_POLL_JITTER_SEC=10

# 在后台启动Builder Agent
bash "$PROJECT_ROOT/.trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh" &
BUILDER_PID=$!
echo "Builder Agent 已启动 (PID: $BUILDER_PID)"

# 等待1秒
sleep 1

# 启动Reviewer Agent
echo "启动Reviewer Agent..."
export COMMS_RAM_ROOT="$RAM_DISK_PATH"
export AGENT_NAME="Reviewer"
export AGENT_ROLE="reviewer"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=60
export AGENT_POLL_JITTER_SEC=10

# 在后台启动Reviewer Agent
bash "$PROJECT_ROOT/.trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh" &
REVIEWER_PID=$!
echo "Reviewer Agent 已启动 (PID: $REVIEWER_PID)"

# 等待1秒
sleep 1

# 启动Documenter Agent
echo "启动Documenter Agent..."
export COMMS_RAM_ROOT="$RAM_DISK_PATH"
export AGENT_NAME="Documenter"
export AGENT_ROLE="documenter"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=120
export AGENT_POLL_JITTER_SEC=10

# 在后台启动Documenter Agent
bash "$PROJECT_ROOT/.trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh" &
DOCUMENTER_PID=$!
echo "Documenter Agent 已启动 (PID: $DOCUMENTER_PID)"

# 等待2秒，让所有Agent都启动完成
sleep 2

# 显示状态
echo ""
echo "===== 多Agent系统启动完成 ====="
echo "内存盘路径: $RAM_DISK_PATH"
echo ""
echo "运行中的Agent:"
echo "- Manager (PID: $MANAGER_PID)"
echo "- Planner (PID: $PLANNER_PID)"
echo "- Builder (PID: $BUILDER_PID)"
echo "- Reviewer (PID: $REVIEWER_PID)"
echo "- Documenter (PID: $DOCUMENTER_PID)"
echo ""
echo "日志文件位置: $RAM_DISK_PATH/logs/"
echo ""
echo "测试多Agent通信..."

# 创建测试消息
test_message=$(cat << EOF
{
  "id": "test-$(date +%s)",
  "ts": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "from": "User",
  "to": "Manager",
  "type": "TASK_REQUEST",
  "thread_id": "test-thread-$(date +%s)",
  "body": "测试多Agent通信机制",
  "meta": {
    "test": true,
    "priority": "low"
  }
}
EOF
)

# 保存测试消息
mkdir -p "$RAM_DISK_PATH/inbox/Manager"
echo "$test_message" > "$RAM_DISK_PATH/inbox/Manager/test_message.json"
echo "已发送测试消息到Manager"
echo ""
echo "等待3秒后检查日志..."
sleep 3

# 检查Manager日志
if [ -f "$RAM_DISK_PATH/logs/agent_Manager.log" ]; then
    echo "Manager日志（最后10行）:"
    tail -10 "$RAM_DISK_PATH/logs/agent_Manager.log"
    echo ""
else
    echo "Manager日志文件不存在，可能Agent尚未完全启动"
fi

echo "===== 启动脚本完成 ====="
echo ""
echo "使用以下命令停止所有Agent:"
echo "kill $MANAGER_PID $PLANNER_PID $BUILDER_PID $REVIEWER_PID $DOCUMENTER_PID"
echo ""
echo "或使用 ./stop_agents.sh 脚本"
