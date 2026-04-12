# guiLaTeX — SOLO MTC → Code 模式交接文档

**日期**：2026-04-11
**来源**：SOLO MTC 模式（Linux VM）
**目标**：Code 模式（Mac 本机）

---

## 1. 本轮做了什么（MTC 模式下）

1. 对 TRAE CN 最新一轮操作后的代码进行了基于证据的审计
2. 创建了安全快照 commit `645a217`
3. 尝试修复 VM 运行环境（创建 `.venv_solo`），发现 PyQt6 被 libEGL.so.1 阻塞
4. 确认 SOLO MTC 模式无法运行 GUI 应用（VM 限制）
5. 完成了非 GUI 部分的测试验证（14 passed, 3 failed）
6. 完成了 5 个关键文件的静态审计
7. 清理了 `.venv_solo`（VM 内创建的 venv，已无用）

## 2. Code 模式下需要优先做的事

### 优先级 1：GUI 验证（只有 Code 模式能做）

```bash
# 激活 Mac 环境
source .venv_local_gui/bin/activate

# 验证 GUI 模块 import
python -c "from src.gui.main import MainWindow; print('OK')"
python -c "from src.gui.pdf_canvas import PDFCanvas; print('OK')"

# 启动 GUI（如果能显示）
python src/gui/main.py
```

### 优先级 2：修复 3 个失败测试

| 测试 | 问题 | 修复方式 |
|------|------|----------|
| test_integration.py::test_no_integration_yet | 过时断言：断言 main.py 不应使用 DocumentModel | 删除或更新断言 |
| test_main_model_integration_no_qt.py (2个) | MockPDFCanvas 缺少 `element_selected` 属性 | 添加 mock 属性 |

### 优先级 3：更新 requirements.txt

```
# 当前问题：
# - 缺少 PyMuPDF 声明
# - PyQt6==6.11.0 版本锁定过严
# - numpy==1.26.0 与 numpy>=2.0 冲突

# 建议修改为：
PyQt6>=6.5
PyMuPDF>=1.20
numpy>=2.0
pytest>=7.0
pytest-qt>=4.0
latex>=0.7.0
Pillow
build
wheel
```

## 3. 关键审计结论（带入 Code 模式）

### 已验证（executed）
- model 层数据结构正确（6 个测试通过）
- PDFToLaTeXConverter 基本转换可用
- 非 GUI 模块 import 正常

### 仅静态可见（static only，需在 Code 模式中动态验证）
- main.py 创建 DocumentModel 并传递给 PDFCanvas
- pdf_canvas.py 的 _sync_from_model / _sync_to_model
- 信号连接（element_selected → on_element_selected → property_panel）
- create_initial_pdf() 中的 model 填充逻辑

### 重要架构发现
- **DocumentModel 目前是"附加层"而非 source of truth**
- 实际数据流仍走 `PDF → fitz → memory_elements → GUI`
- model 层只在初始化时从 memory_elements 复制数据
- 后续修改（拖拽、编辑）走 memory_elements，不一定同步回 PageModel

### 代码问题
- main.py `preview_document()` 硬编码了 Mac 路径 `/Users/...`
- export_document() 仍从 memory_elements 而非 DocumentModel 导出

## 4. 文件索引（所有产出物）

### 审计与证据

| 文件 | 内容 |
|------|------|
| `docs/audits/2026-04-11_post-trae-cn-audit.md` | 完整审计记录（3 轮追加） |
| `docs/contest_evidence/dev_journal.md` | 开发日志（3 轮追加） |
| `docs/contest_evidence/lessons_learned.md` | 经验总结（含 SOLO 平台限制） |

### 截图证据

| 文件 | 内容 |
|------|------|
| `docs/contest_evidence/screenshots/01_git_log.txt` | git log + status |
| `docs/contest_evidence/screenshots/02_test_model_result.txt` | model 层测试结果 |
| `docs/contest_evidence/screenshots/03_test_no_qt_failure.txt` | mock 测试失败 |
| `docs/contest_evidence/screenshots/03b_test_integration_failure.txt` | 过时断言失败 |
| `docs/contest_evidence/screenshots/04_blocked_dependencies.txt` | VM 依赖阻塞证据 |
| `docs/contest_evidence/screenshots/05_snapshot_commit_diff.txt` | 快照 commit diff |
| `docs/contest_evidence/screenshots/06_venv_python_deps.txt` | venv 信息（已清理） |
| `docs/contest_evidence/screenshots/07_import_checks.txt` | import 检查结果 |
| `docs/contest_evidence/screenshots/08_pytest_results.txt` | pytest 10 passed |
| `docs/contest_evidence/screenshots/09_test_failures_rerun.txt` | 失败测试重跑 |
| `docs/contest_evidence/screenshots/10_libegl_blocked.txt` | libEGL 阻塞证据 |
| `docs/contest_evidence/screenshots/11_full_test_coverage.txt` | 完整测试 14p/3f |
| `docs/contest_evidence/screenshots/12_nongui_smoke_test.txt` | 非 GUI smoke test |

## 5. SOLO MTC 模式限制（已记录到 lessons_learned.md）

- MTC 模式 = Linux VM，无法运行 GUI 应用
- Mac venv 在 VM 中不可用（broken symlink）
- 需要 GUI 验证时切 Code 模式
- 详见 `docs/contest_evidence/lessons_learned.md` 最后一个小节
