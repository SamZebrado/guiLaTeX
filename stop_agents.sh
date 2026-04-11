#!/usr/bin/env bash
set -euo pipefail

# 停止所有Agent进程的脚本

echo "停止所有Agent进程..."

# 查找所有agent_controller.sh进程
AGENT_PIDS=$(pgrep -f "agent_controller.sh" || true)

if [ -z "$AGENT_PIDS" ]; then
    echo "没有找到运行中的Agent进程"
    exit 0
fi

echo "找到以下Agent进程: $AGENT_PIDS"

# 停止所有Agent进程
for PID in $AGENT_PIDS; do
    echo "停止进程 $PID"
    kill -15 "$PID" 2>/dev/null || true
done

# 等待2秒
sleep 2

# 检查是否还有进程运行
REMAINING_PIDS=$(pgrep -f "agent_controller.sh" || true)
if [ -z "$REMAINING_PIDS" ]; then
    echo "所有Agent进程已停止"
else
    echo "以下进程仍在运行: $REMAINING_PIDS"
    echo "正在强制停止..."
    for PID in $REMAINING_PIDS; do
        kill -9 "$PID" 2>/dev/null || true
    done
    echo "已强制停止所有进程"
fi

echo "停止脚本完成"
