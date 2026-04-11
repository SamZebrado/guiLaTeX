# 多Agent系统稳定性改进指南

> 本文档记录了对guiLaTeX项目多Agent系统的稳定性改进

## 改进概述

### 问题诊断

经过审计，发现以下问题：

1. **缺少Watchdog机制** - 无法检测Agent停止
2. **状态文件不一致** - STATUS.md、PLAN.md、DEVELOPMENT_STATUS.md互相打架
3. **消息体过薄** - 缺少结构化任务上下文
4. **无恢复机制** - 中断后需要人工干预
5. **完成定义模糊** - 没有分层完成标准

### 实施的改进

#### 1. Agent Watchdog (`agent_watchdog.sh`)

**功能**:
- 检测Agent进程是否存活
- 检测Agent是否停滞（5分钟无活动）
- 统计待处理消息数量
- 自动生成恢复脚本
- 更新单一真相文件

**使用**:
```bash
# 手动检查
./agent_watchdog.sh

# 定时检查（每分钟）
watch -n 60 ./agent_watchdog.sh
```

#### 2. 单一真相文件 (`CURRENT_RUN_STATE.json`)

**位置**: `$RAM_DISK_PATH/state/CURRENT_RUN_STATE.json`

**内容**:
- 运行状态（running/stopped/idle）
- 当前任务信息
- 所有Agent状态
- 完成层级（scaffold/code/test/verified）

**原则**:
- 这是唯一的真相源
- 其他所有状态文件都从这里同步
- 不允许各写各的

#### 3. Run Ledger (`RUN_LEDGER.md`)

**功能**:
- 记录所有任务的执行摘要
- 追踪任务生命周期
- 显示Agent状态摘要
- 提供恢复指令

**维护**:
- 自动从CURRENT_RUN_STATE.json同步
- 记录每个任务的完成层级

#### 4. 结构化任务包 (`STRUCTURED_TASK_TEMPLATE.json`)

**改进**:
- 明确objective
- 定义scope（in_scope_files, out_of_scope）
- 列出acceptance_criteria
- 要求evidence_required
- 分层完成定义

**示例**:
```json
{
  "task_id": "TASK-001",
  "objective": "修复视觉元素更新问题",
  "scope": {
    "in_scope_files": ["src/gui/pdf_canvas.py"],
    "out_of_scope": ["其他文件"]
  },
  "acceptance_criteria": [
    {
      "check": "元素移动后能正确更新显示",
      "type": "test",
      "required": true
    }
  ],
  "completion_tiers": {
    "scaffold_done": false,
    "code_done": false,
    "test_done": false,
    "verified_done": false
  }
}
```

#### 5. 状态同步机制 (`sync_state.sh`)

**功能**:
- 从CURRENT_RUN_STATE.json同步到STATUS.md
- 从CURRENT_RUN_STATE.json同步到PLAN.md
- 更新RUN_LEDGER.md

**使用**:
```bash
# 手动同步
./sync_state.sh

# 定时同步（每5分钟）
watch -n 300 ./sync_state.sh
```

#### 6. 增强的启动/停止脚本

**start_agents.sh**:
- 初始化CURRENT_RUN_STATE.json
- 启动Watchdog
- 发送测试消息
- 显示当前状态

**stop_agents.sh**:
- 停止所有Agent
- 更新状态文件
- 生成恢复指令

---

## 使用流程

### 启动系统

```bash
# 1. 启动所有Agent和Watchdog
./start_agents.sh

# 2. 检查状态
cat /tmp/trae_multi_agent_ram/state/CURRENT_RUN_STATE.json

# 3. 查看日志
tail -f /tmp/trae_multi_agent_ram/logs/agent_Manager.log
```

### 监控系统

```bash
# 1. 运行Watchdog检查
./agent_watchdog.sh

# 2. 查看恢复需求（如果有）
cat /tmp/trae_multi_agent_ram/state/RECOVERY_NEEDED.txt

# 3. 同步状态文件
./sync_state.sh

# 4. 查看任务记录
cat RUN_LEDGER.md
```

### 恢复系统

```bash
# 1. 检查恢复指令
cat /tmp/trae_multi_agent_ram/state/RECOVERY_INSTRUCTIONS.txt

# 2. 重新启动
./start_agents.sh

# 3. 验证状态
./agent_watchdog.sh
```

### 停止系统

```bash
# 1. 正常停止
./stop_agents.sh

# 2. 检查恢复指令
cat /tmp/trae_multi_agent_ram/state/RECOVERY_INSTRUCTIONS.txt
```

---

## 完成层级定义

为了避免"已完成"的歧义，定义了四个完成层级：

### 1. scaffold_done（框架完成）
- 代码框架已搭建
- 接口已定义
- 但功能未实现

### 2. code_done（代码完成）
- 功能已实现
- 代码已编写
- 但未测试

### 3. test_done（测试完成）
- 单元测试通过
- 集成测试通过
- 但未验证实际效果

### 4. verified_done（验证完成）
- 在实际环境中验证
- 符合acceptance_criteria
- 证据已记录

**原则**:
- 不允许只因为scaffold_done就标记completed
- 每个层级必须有对应的evidence
- 完成层级在CURRENT_RUN_STATE.json中记录

---

## 文件清单

### 新增文件

1. `agent_watchdog.sh` - Agent监控脚本
2. `sync_state.sh` - 状态同步脚本
3. `RUN_LEDGER.md` - 任务执行记录
4. `trae_multi_agent_ram/state/CURRENT_RUN_STATE.json` - 单一真相文件
5. `trae_multi_agent_ram/state/STRUCTURED_TASK_TEMPLATE.json` - 任务包模板

### 修改文件

1. `start_agents.sh` - 增强启动脚本
2. `stop_agents.sh` - 增强停止脚本

---

## 验证方法

### 1. 验证Watchdog

```bash
# 启动系统
./start_agents.sh

# 手动停止一个Agent
kill <PID>

# 运行Watchdog
./agent_watchdog.sh

# 检查是否生成恢复脚本
cat /tmp/trae_multi_agent_ram/state/RECOVERY_NEEDED.txt
```

### 2. 验证状态一致性

```bash
# 启动系统
./start_agents.sh

# 同步状态
./sync_state.sh

# 检查STATUS.md是否更新
cat STATUS.md

# 检查CURRENT_RUN_STATE.json
cat /tmp/trae_multi_agent_ram/state/CURRENT_RUN_STATE.json

# 确认内容一致
```

### 3. 验证恢复机制

```bash
# 启动系统
./start_agents.sh

# 停止系统
./stop_agents.sh

# 检查恢复指令
cat /tmp/trae_multi_agent_ram/state/RECOVERY_INSTRUCTIONS.txt

# 恢复系统
./start_agents.sh

# 验证状态
./agent_watchdog.sh
```

---

## 未解决的问题

1. **自动重启** - 当前只生成恢复脚本，未实现自动重启
2. **消息持久化** - inbox消息未持久化到磁盘
3. **任务依赖** - 未实现任务依赖关系管理
4. **并发控制** - 多个Builder同时工作时的冲突处理
5. **长时间运行** - 未测试长时间运行的稳定性

---

## 下一步改进建议

1. **实现自动重启** - Watchdog检测到Agent停止后自动重启
2. **添加消息持久化** - 定期将inbox消息备份到磁盘
3. **实现任务依赖** - 在任务包中添加dependencies字段
4. **添加并发控制** - 文件锁或任务队列机制
5. **长时间运行测试** - 运行24小时测试稳定性

---

**最后更新**: 2026-04-04
**版本**: 1.0
