#!/usr/bin/env bash
# Agent Watchdog - 监控Agent状态并自动恢复
set -euo pipefail

RAM_DISK_PATH="${COMMS_RAM_ROOT:-/tmp/trae_multi_agent_ram}"
LOG_FILE="$RAM_DISK_PATH/logs/watchdog.log"
STATE_FILE="$RAM_DISK_PATH/state/CURRENT_RUN_STATE.json"
ALERT_FILE="$RAM_DISK_PATH/state/RECOVERY_NEEDED.txt"

log() {
    local level="$1"
    shift
    local msg="$*"
    local ts
    ts=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$ts] [WATCHDOG] [$level] $msg" | tee -a "$LOG_FILE"
}

check_agent_alive() {
    local agent_name="$1"
    local pid
    pid=$(pgrep -f "AGENT_NAME=$agent_name" | head -1 || true)
    
    if [ -z "$pid" ]; then
        return 1
    fi
    
    if ! ps -p "$pid" > /dev/null 2>&1; then
        return 1
    fi
    
    return 0
}

check_agent_activity() {
    local agent_name="$1"
    local log_file="$RAM_DISK_PATH/logs/agent_${agent_name}.log"
    local max_idle_seconds="${2:-300}"  # 默认5分钟无活动视为停滞
    
    if [ ! -f "$log_file" ]; then
        return 1
    fi
    
    local last_modified
    last_modified=$(stat -f %m "$log_file" 2>/dev/null || stat -c %Y "$log_file" 2>/dev/null || echo "0")
    local current_time
    current_time=$(date +%s)
    local idle_time=$((current_time - last_modified))
    
    if [ "$idle_time" -gt "$max_idle_seconds" ]; then
        return 2  # 停滞
    fi
    
    return 0
}

check_pending_messages() {
    local agent_name="$1"
    local inbox_dir="$RAM_DISK_PATH/inbox/$agent_name"
    
    if [ ! -d "$inbox_dir" ]; then
        return 0
    fi
    
    local pending_count
    pending_count=$(find "$inbox_dir" -maxdepth 1 -name "*.json" -type f 2>/dev/null | wc -l | tr -d ' ')
    
    echo "$pending_count"
}

generate_recovery_script() {
    local dead_agents="$1"
    
    cat > "$ALERT_FILE" << EOF
# Agent Recovery Required

## Time: $(date)

## Dead Agents:
$dead_agents

## Recovery Commands:

# Restart all dead agents:
EOF

    for agent in $dead_agents; do
        local role
        role=$(echo "$agent" | tr '[:upper:]' '[:lower:]')
        local interval=60
        case "$role" in
            manager) interval=30 ;;
            documenter) interval=120 ;;
        esac
        
        cat >> "$ALERT_FILE" << EOF
export COMMS_RAM_ROOT="$RAM_DISK_PATH"
export AGENT_NAME="$agent"
export AGENT_ROLE="$role"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=$interval
export AGENT_POLL_JITTER_SEC=10
bash .trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh &

EOF
    done
    
    log "WARN" "Generated recovery script: $ALERT_FILE"
}

update_current_state() {
    local status="$1"
    local details="$2"
    
    local ts
    ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    
    cat > "$STATE_FILE" << EOF
{
  "timestamp": "$ts",
  "status": "$status",
  "details": "$details",
  "agents": {
EOF

    local first=true
    for agent in Manager Planner Builder Reviewer Documenter; do
        local alive="false"
        local pending=0
        
        if check_agent_alive "$agent"; then
            alive="true"
        fi
        
        pending=$(check_pending_messages "$agent")
        
        if [ "$first" = true ]; then
            first=false
        else
            echo "," >> "$STATE_FILE"
        fi
        
        cat >> "$STATE_FILE" << EOF
    "$agent": {
      "alive": $alive,
      "pending_messages": $pending
    }
EOF
    done
    
    cat >> "$STATE_FILE" << EOF
  }
}
EOF
}

main() {
    log "INFO" "Watchdog started"
    
    mkdir -p "$RAM_DISK_PATH/logs" "$RAM_DISK_PATH/state"
    
    local dead_agents=""
    local stalled_agents=""
    local all_healthy=true
    
    for agent in Manager Planner Builder Reviewer Documenter; do
        if ! check_agent_alive "$agent"; then
            dead_agents="$dead_agents $agent"
            all_healthy=false
            log "ERROR" "Agent $agent is not running"
        else
            local activity_status
            activity_status=$(check_agent_activity "$agent")
            case $? in
                0)
                    log "INFO" "Agent $agent is healthy"
                    ;;
                1)
                    log "WARN" "Agent $agent has no log file"
                    ;;
                2)
                    stalled_agents="$stalled_agents $agent"
                    all_healthy=false
                    log "WARN" "Agent $agent appears stalled (no activity for 5+ minutes)"
                    ;;
            esac
        fi
        
        local pending
        pending=$(check_pending_messages "$agent")
        if [ "$pending" -gt 0 ]; then
            log "INFO" "Agent $agent has $pending pending messages"
        fi
    done
    
    if [ "$all_healthy" = true ]; then
        update_current_state "healthy" "All agents running normally"
        log "INFO" "All agents healthy"
    else
        if [ -n "$dead_agents" ]; then
            update_current_state "degraded" "Dead agents:$dead_agents Stalled:$stalled_agents"
            generate_recovery_script "$dead_agents"
        else
            update_current_state "stalled" "Stalled agents:$stalled_agents"
        fi
    fi
    
    log "INFO" "Watchdog check completed"
}

main "$@"
