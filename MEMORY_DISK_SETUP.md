# 内存盘设置指南

## 为什么使用内存盘

内存盘（RAM disk）可以显著提升多Agent系统的性能，因为：
- **速度快**：内存访问速度远快于硬盘
- **减少I/O**：避免频繁的硬盘读写操作
- **临时存储**：适合Agent间的消息传递

## 在沙箱外部设置内存盘

### macOS 系统

1. **打开终端**（在沙箱外部）

2. **创建内存盘挂载点**：
   ```bash
   mkdir -p ~/trae_multi_agent_ram
   ```

3. **创建内存盘**（256MB）：
   ```bash
   diskutil erasevolume HFS+ "TraeRAM" $(hdiutil attach -nomount ram://524288)
   ```

4. **验证内存盘**：
   ```bash
   ls -la /Volumes/TraeRAM/
   ```

### Linux 系统

1. **打开终端**（在沙箱外部）

2. **创建内存盘挂载点**：
   ```bash
   mkdir -p ~/trae_multi_agent_ram
   ```

3. **创建内存盘**（256MB）：
   ```bash
   sudo mount -t tmpfs -o size=256M tmpfs ~/trae_multi_agent_ram
   ```

4. **验证内存盘**：
   ```bash
   ls -la ~/trae_multi_agent_ram/
   ```

## 配置多Agent环境使用内存盘

### 1. 复制目录结构到内存盘

1. **在内存盘中创建目录结构**：
   ```bash
   mkdir -p /Volumes/TraeRAM/logs /Volumes/TraeRAM/state /Volumes/TraeRAM/inbox /Volumes/TraeRAM/processed
   ```

2. **复制Agent注册表**：
   ```bash
   cp <repo-root>/trae_multi_agent_ram/state/agents.tsv /Volumes/TraeRAM/state/
   ```

3. **复制初始化Prompt**：
   ```bash
   cp <repo-root>/trae_multi_agent_ram/init_*_prompt.txt /Volumes/TraeRAM/
   ```

### 2. 更新环境变量配置

在每个Agent的终端中，使用以下环境变量配置：

#### Manager Agent
```bash
export COMMS_RAM_ROOT="/Volumes/TraeRAM"
export AGENT_NAME="Manager"
export AGENT_ROLE="manager"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=30
export AGENT_POLL_JITTER_SEC=10
```

#### Planner Agent
```bash
export COMMS_RAM_ROOT="/Volumes/TraeRAM"
export AGENT_NAME="Planner"
export AGENT_ROLE="planner"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=60
export AGENT_POLL_JITTER_SEC=10
```

#### Builder Agent
```bash
export COMMS_RAM_ROOT="/Volumes/TraeRAM"
export AGENT_NAME="Builder"
export AGENT_ROLE="builder"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=60
export AGENT_POLL_JITTER_SEC=10
```

#### Reviewer Agent
```bash
export COMMS_RAM_ROOT="/Volumes/TraeRAM"
export AGENT_NAME="Reviewer"
export AGENT_ROLE="reviewer"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=60
export AGENT_POLL_JITTER_SEC=10
```

#### Documenter Agent
```bash
export COMMS_RAM_ROOT="/Volumes/TraeRAM"
export AGENT_NAME="Documenter"
export AGENT_ROLE="documenter"
export AGENT_DEFAULT_POLL_INTERVAL_SEC=120
export AGENT_POLL_JITTER_SEC=10
```

## 启动多Agent系统

### 1. 启动Agent控制器

在沙箱外部的终端中，为每个Agent启动控制器：

```bash
# 启动Manager Agent
bash .trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh manager

# 启动Planner Agent
bash .trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh planner

# 启动Builder Agent
bash .trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh builder

# 启动Reviewer Agent
bash .trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh reviewer

# 启动Documenter Agent
bash .trae/skills/trae-cn-multi-agent-orchestration/scripts/agent_controller.sh documenter
```

### 2. 验证Agent状态

检查内存盘中的日志文件，确认所有Agent都正常运行：

```bash
ls -la /Volumes/TraeRAM/logs/
tail -f /Volumes/TraeRAM/logs/agent_Manager.log
```

## 测试多Agent通信

1. **创建测试消息**：
   ```bash
   cat > /Volumes/TraeRAM/inbox/test_message.json << EOF
   {
     "id": "test-001",
     "ts": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
     "from": "User",
     "to": "Manager",
     "type": "TASK_REQUEST",
     "thread_id": "test-thread-001",
     "body": "测试多Agent通信机制",
     "meta": {
       "test": true,
       "priority": "low"
     }
   }
   EOF
   ```

2. **检查消息处理**：
   ```bash
   # 检查Manager是否处理了消息
   tail -f /Volumes/TraeRAM/logs/agent_Manager.log
   
   # 检查消息是否被移动到processed目录
   ls -la /Volumes/TraeRAM/processed/
   ```

## 故障排除

### 常见问题

1. **内存盘挂载失败**：
   - 检查权限
   - 确保没有其他进程占用内存盘
   - 尝试使用不同的内存大小

2. **Agent无法启动**：
   - 检查环境变量设置
   - 检查内存盘权限
   - 查看日志文件了解具体错误

3. **消息未处理**：
   - 检查Agent是否正在运行
   - 检查消息格式是否正确
   - 检查内存盘权限

### 日志位置

所有Agent的日志文件都存储在：
```
/Volumes/TraeRAM/logs/
├── agent_Manager.log
├── agent_Planner.log
├── agent_Builder.log
├── agent_Reviewer.log
└── agent_Documenter.log
```

## 性能优化

1. **调整内存盘大小**：
   - 根据项目规模调整内存盘大小
   - 大型项目建议使用512MB或1GB

2. **优化轮询间隔**：
   - 根据系统性能调整轮询间隔
   - 性能较好的系统可以缩短轮询间隔

3. **定期清理**：
   - 定期清理processed目录中的旧消息
   - 避免内存盘空间不足

## 总结

使用内存盘可以显著提升多Agent系统的性能和响应速度。通过以上步骤，您可以在沙箱外部设置内存盘并配置多Agent环境，为guiLaTeX项目的开发提供高效的协作平台。

如果遇到任何问题，请查看日志文件或参考多Agent协作技能的文档。