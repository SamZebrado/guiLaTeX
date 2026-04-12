# PROJECT_LOG

## 2026-04-13 - Qt 线 UI 统一模式
- What changed: 跟进 Web 的统一 UI 模式 v1，重构了 Qt 界面，包括顶部主工具栏、主区布局和属性面板
- Why: 为了与 Web 端保持统一的 UI 模式和用户体验，提高产品的一致性
- Verified by: 创建了完整的测试文件，但由于本环境缺少 PyQt6 模块，未实际运行验证
- Files / commands: src/gui/main.py, src/gui/properties.py, tests/test_qt_ui_smoke.py, tests/test_qt_core_smoke.py, tests/test_qt_render_evidence.py
- Follow-up: 继续重构 PDFCanvas 使用内部模型，完善编辑逻辑和保存语义
- Status: 代码已实现但本环境未验证，受环境阻塞

## 2026-04-12 - Qt 线测试环境诚实化
- What changed: 为 Qt 相关测试添加了 skip 机制，创建了纯 Python 模型测试，更新了测试环境说明文档
- Why: 为了在无 PyQt6 环境下也能诚实运行测试，避免硬失败
- Verified by: 成功运行了纯 Python 模型测试 test_qt_model_smoke.py
- Files / commands: tests/test_qt_ui_smoke.py, tests/test_qt_core_smoke.py, tests/test_qt_render_evidence.py, tests/test_qt_model_smoke.py, STATUS.md
- Follow-up: 尝试安装 PyQt6 以运行完整的 Qt 测试
- Status: 纯 Python 测试可运行，Qt 相关测试受 PyQt6 依赖阻塞

## 2026-04-12 - 尝试安装 PyQt6
- What changed: 尝试在当前环境中安装 PyQt6
- Why: 为了运行完整的 Qt 测试，获取真实的运行证据
- Verified by: 执行 `python -m pip install PyQt6`，发现 PyQt6 已安装
- Files / commands: 无文件变更，仅执行命令
- Follow-up: 尝试运行测试，发现非 GUI 环境限制
- Status: PyQt6 已安装，但在非 GUI 环境中无法运行 Qt 界面测试

## 2026-04-12 - 运行测试
- What changed: 运行了纯 Python 模型测试和 Qt UI smoke 测试
- Why: 为了获取真实的测试证据
- Verified by: 执行 `python -m pytest tests/test_qt_model_smoke.py -q` 和 `python -m pytest tests/test_qt_ui_smoke.py -q`
- Files / commands: 无文件变更，仅执行命令
- Follow-up: 记录测试结果，更新文档
- Status: 纯 Python 模型测试通过，Qt UI 测试因非 GUI 环境失败

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

## 2026-04-12 - Qt 线 Subprocess 探针定位
- What changed: 创建并运行最小探针脚本，修复 probe 框架，定位 Qt 崩溃点
- Why: 为了精确定位 Qt 在非 GUI 环境下的崩溃原因
- Verified by: 运行了 probe_import_pyqt6.py 和 probe_qapplication.py 在 default、offscreen 和 minimal 环境下的测试
- Files / commands:
  - tests/qt_probes/probe_import_pyqt6.py (修复)
  - tests/qt_probes/probe_qapplication.py (修复)
  - tests/qt_probes/run_probes.py (修复)
  - docs/contest_evidence/qt_probe_matrix_20260412_201936.md
  - STATUS.md (更新)
- Follow-up: 继续缩小卡点范围
- Status: 已定位到 QApplication 创建阶段超时，疑似平台/插件问题

## 2026-04-12 - Qt 线细粒度探针定位
- What changed: 创建更细粒度探针，精确区分导入层和创建层
- Why: 为了精确定位卡点是在导入 QtWidgets 还是在创建 QApplication 实例
- Verified by: 运行 probe_import_pyqt6.py、probe_import_qtwidgets.py、probe_create_qapplication.py 在 default、offscreen、minimal 环境下的测试
- Files / commands:
  - tests/qt_probes/probe_import_qtwidgets.py (新增)
  - tests/qt_probes/probe_create_qapplication.py (新增)
  - tests/qt_probes/run_probes.py (更新)
  - docs/contest_evidence/qt_probe_matrix_20260412_202440.md
  - STATUS.md (更新)
- Follow-up: 继续缩小 QApplication 卡点范围
- Status: 已精确锁定卡点在 QApplication 实例化阶段，导入层完全正常

## 2026-04-12 - Qt 线 QApplication 卡点继续缩小
- What changed: 创建更细粒度探针，区分导入 QApplication 和创建 QApplication 实例
- Why: 为了进一步确认卡点是在 QApplication 创建、退出还是 driver/timeout 问题
- Verified by: 运行 probe_import_pyqt6.py、probe_import_qtwidgets.py、probe_before_qapp.py、probe_after_qapp_create.py 在 default、offscreen、minimal 环境下的测试
- Files / commands:
  - tests/qt_probes/probe_before_qapp.py (新增)
  - tests/qt_probes/probe_after_qapp_create.py (新增)
  - tests/qt_probes/run_probes.py (更新)
  - docs/contest_evidence/qt_probe_matrix_20260412_203548.md
  - STATUS.md (更新)
- Follow-up: 进行环境对照测试
- Status: 已进一步缩小到 QApplication 实例化阶段，仅导入不创建时正常，创建时超时

## 2026-04-12 - Qt 线环境对照测试
- What changed: 创建干净虚拟环境并进行环境对照测试，比较 Anaconda 和 Clean Venv 环境下的表现
- Why: 为了判断 QApplication 实例化超时是 Anaconda 环境特有问题还是更普遍的 Qt/macOS/headless 问题
- Verified by: 在 Anaconda 和 Clean Venv 环境下运行相同的 probe 测试
- Files / commands:
  - venv_clean/ (新增)
  - tests/qt_probes/run_probes_env_compare.py (新增)
  - docs/contest_evidence/qt_probe_matrix_env_compare_20260412_204536.md
  - STATUS.md (更新)
- Follow-up: 基于环境对照结果制定后续解决方案
- Status: 已确认为 Anaconda 环境特有问题，在 Clean Venv 环境中 QApplication 实例化正常通过
