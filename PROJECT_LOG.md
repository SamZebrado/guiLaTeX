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

## 2026-04-11 - Qt 对接 Core 的预接入准备
- What changed: 完成 Qt -> Core 最小 smoke test，真实调用 ExportCore 函数，生成完整证据文件，明确 font_family_zh / font_family_en 映射策略
- Why: 用户要求做 Qt 对接 Core 的准备工作，把 Qt 推进到"已具备接 Core 的最小适配能力"
- Verified by: 创建完整 smoke test 框架，生成 5 个证据文件，真实调用 normalize_qt_model_to_ir() 和 export_ir_to_latex()
- Files / commands: 
  - docs/contest_evidence/screenshots/qt_to_core_input_model.json
  - docs/contest_evidence/screenshots/qt_to_core_ir_data.json
  - docs/contest_evidence/screenshots/qt_to_core_output.tex
  - docs/contest_evidence/screenshots/qt_to_core_field_mapping.txt
  - docs/contest_evidence/screenshots/qt_to_core_smoke_test_log.txt
  - docs/agent_runs/2026-04-11_dual_agent_runs.md (追加 Round 8)
  - STATUS.md, PROJECT_LOG.md, PLAN.md
- Follow-up: 准备下一轮正式接入 Core 链路

## 2026-04-12 - Qt 线测试正式化轮
- What changed: 把 Qt -> Core smoke test、rotation 证据、IR 导出证据从"临时脚本 + 临时结果"推进到"正式测试材料 + 正式证据链"，压实了 font_family_zh / font_family_en 字段映射，保留并整理了 rotation 证据链，完成了文档和计划收口
- Why: 用户要求只做"测试正式化轮"，不要继续扩 UI、不要先 commit
- Verified by: 创建正式测试文件 tests/test_qt_to_core_smoke.py，更新了字段映射文档 qt_to_core_field_mapping.txt，创建了 rotation 证据链文档 qt_rotation_evidence_chain.txt，更新了所有 dev-workflow 文档
- Files / commands:
  - tests/test_qt_to_core_smoke.py
  - docs/contest_evidence/screenshots/qt_to_core_field_mapping.txt
  - docs/contest_evidence/screenshots/qt_rotation_evidence_chain.txt
  - docs/audits/2026-04-11_qt_demo_checkpoint.md
  - docs/agent_runs/2026-04-11_dual_agent_runs.md (追加 Round 9)
  - STATUS.md, PROJECT_LOG.md
- Follow-up: 准备下一轮正式接入 Core 链路或等待用户进一步指示
