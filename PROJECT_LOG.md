# PROJECT_LOG

## 2026-04-03 14:30 - Project Initialization
- What changed: Created guiLaTeX project structure
- Why: User requested development of visual LaTeX editor with drag-and-drop functionality
- Verified by: Directory creation confirmed
- Files / commands: mkdir -p guiLaTeX
- Follow-up: Initialize STATUS.md, PROJECT_LOG.md, PLAN.md

## 2026-04-03 14:35 - Technology Research
- What changed: Researched existing LaTeX editors and their capabilities
- Why: To understand current landscape and identify gaps
- Verified by: Web search results
- Files / commands: WebSearch queries
- Follow-up: Document findings in architecture design

### Key Findings:
1. **Overleaf**: Visual Editor + Code Editor, but web-based and limited drag-and-drop
2. **TeXpen**: Qt/C++ based, visual editing but still code-centric
3. **LyX**: WYSIWYM approach, structure-focused not visual manipulation
4. **TeXstudio**: Code editor with PDF preview
5. **No existing tool**: Supports Photoshop-like element drag-and-drop

## 2026-04-03 14:40 - Skill Setup
- What changed: Created dev-workflow skill for structured development
- Why: Need disciplined workflow for medium-to-large project
- Verified by: Skill file creation
- Files / commands: .trae/skills/dev-workflow/SKILL.md
- Follow-up: Apply workflow to guiLaTeX development

# PROJECT_LOG

## 2026-04-11 - Qt 线核心功能验证
- What changed: 完成 Qt 线核心功能的真实路径测试验证，更新 dev-workflow 文档
- Why: 用户要求压实旋转功能，不要把"有控件/分支"写成"功能已完成"；要求优先加强单元测试和真实路径测试
- Verified by: 运行 temp/test_qt_real_path.py，所有 5 项测试通过
- Files / commands: temp/test_qt_real_path.py, STATUS.md, PROJECT_LOG.md
- Follow-up: 准备 git 提交，仅提交 Qt 相关文件

### 验证结果
1. ✅ 初始化元素数量: 保持为 5 个对象，无重复
2. ✅ rotation 字段: 已正确进入模型并保存
3. ✅ 旋转绘制链: 绘制函数正确读取 rotation 字段
4. ✅ copy/paste: 生成新 UUID 且位置轻微偏移 (20, 20)
5. ✅ 字体安全: 只保留开源/免费可商用字体

## 2026-04-03 15:00 - Technology Stack Decision
- What changed: Chose Qt 6 (Python/PyQt6) for MVP development
- Why: Balance of rapid development and performance
- Verified by: Technology evaluation complete
- Files / commands: Updated STATUS.md, PLAN.md
- Follow-up: Begin setting up PyQt6 development environment
