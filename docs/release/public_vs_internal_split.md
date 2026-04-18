# guiLaTeX 公开版 / 内部版分层

**编制**：外务大臣
**日期**：2026-04-13

---

## A. 公开战报版

适合：论坛更新、GitHub Pages、showcase、对外介绍

### 文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 公开总览 | `docs/release/public_project_overview.md` | 项目状态、证据层级、红线清单 |
| 论坛战报草稿 | `docs/release/forum_update_draft.md` | 可直接发帖 |
| Web 公开口径 | `docs/release/web_public_status.md` | Web 端最精炼口径 |
| Qt 公开口径 | `docs/release/qt_public_status.md` | Qt 端最精炼口径 |
| 人类阅读说明 | `docs/README_FOR_HUMANS.md` | 文档分层导引 |
| README | `README.md` | 项目介绍（双语） |
| 展示页 | `showcase/index.html` | 朝堂风云录 |
| 演示入口 | `showcase/demo_index.html` | GitHub Pages 小入口 |

### 证据

| 证据 | 路径 | 说明 |
|------|------|------|
| Web v4 截图 + JSON | `docs/contest_evidence/screenshots/web_regression_v4_*` | 最终版证据 |
| Qt 界面截图 | `docs/contest_evidence/screenshots/16_gui_screenshot.png` | Qt 桌面端 |
| Qt 旋转截图 | `docs/contest_evidence/screenshots/qt_rotation_test_*.png` | 旋转验证 |
| Canonical Pack（5 文件） | `docs/contest_evidence/qt_canonical_pack/` | 除 diff report 外全部 |
| Canonical diff report（脱敏版） | `docs/release/redacted_evidence/qt_canonical_roundtrip_diff_report.redacted.json` | 脱敏副本 |
| Bridge 脚本 + 样本 | `docs/contest_evidence/web_to_core_bridge/` | 无敏感信息 |
| Bridge 真实证据（脱敏日志） | `docs/release/redacted_evidence/execution_log_*.redacted.txt` | 4 个脱敏副本 |
| Core 回归样本 | `export_core/samples/` | 4 个样本文件 |

### 不公开（仅摘要提及）

| 内容 | 公开时如何提及 |
|------|---------------|
| 合成 bridge 测试 | "存在合成测试验证"（不公开原件） |
| 内部策略口径（"不该说满"） | 不公开，公开版只保留"对外可说"部分 |

---

## B. 内部完整版

适合：交接、复核、证据留档、继续开发参考

### 文档

| 文档 | 路径 | 说明 |
|------|------|------|
| Web 演示准备清单（完整版） | `docs/release/web_demo_ready_list.md` | 含内部策略节 |
| Web 录制脚本（完整版） | `docs/release/web_demo_shot_list.md` | 含"不该说满"列 |
| Qt 演示准备清单（完整版） | `docs/release/qt_demo_ready_list.md` | 含内部策略节 |
| Qt 录制脚本（完整版） | `docs/release/qt_demo_shot_list.md` | 含"不该说满"列 |
| Qt Canonical 交接说明（完整版） | `docs/contest_evidence/qt_canonical_pack/qt_canonical_handoff_readme.md` | 含内部策略 |
| 证据脱敏映射表 | `docs/release/public_evidence_redaction_map.md` | 完整脱敏记录 |
| 公开/内部分层说明 | `docs/release/public_vs_internal_split.md` | 本文档 |
| 筛查清单 | `docs/release/public_sanitization_checklist.md` | 逐项筛查结果 |

### 证据

| 证据 | 路径 | 说明 |
|------|------|------|
| 全部 execution_log 原件 | `docs/contest_evidence/web_to_core_bridge_*/` | 含敏感路径，仅内部 |
| 合成 bridge 测试 | `docs/contest_evidence/web_to_core_bridge_synthetic_*/` | 合成证据，仅内部 |
| Canonical diff report 原件 | `docs/contest_evidence/qt_canonical_pack/qt_canonical_roundtrip_diff_report.json` | 含敏感路径 |
| 全部历史中间截图 | `docs/contest_evidence/screenshots/web_test_*`, `web_regression_*` (v1/v3) | 历史留档 |
| Bridge 真实运行截图 | `docs/contest_evidence/web_to_core_bridge_real_*/page_screenshot_*.png` | 内部留档 |
| 全部开发日志 | `PLAN.md`, `PROJECT_LOG.md`, `RUN_LEDGER.md` | 内部留档 |
| Agent 规范 | `docs/skills/`, `docs/audits/` | 内部留档 |

---

## C. 双版本并存的文档

以下文档需要"公开版"和"内部版"两个版本：

| 文档 | 公开版 | 内部版 |
|------|--------|--------|
| Qt demo ready list | 删除"最不该说满的点"节 | 完整版 |
| Qt demo shot list | 删除"不该说满的话"列 | 完整版 |
| Web demo shot list | 删除"不该说满的话"列 | 完整版 |
| Qt canonical handoff readme | 摘要版（见 redaction_map） | 完整版 |
| Canonical diff report | 脱敏版（`redacted_evidence/`） | 原件 |

---

## D. 仅摘要公开、不适合原件公开

| 内容 | 摘要说明 | 原件处理 |
|------|----------|----------|
| `web_to_core_bridge_synthetic_20260412_165000/` | "存在合成测试验证" | 内部留档 |
| 各 execution_log 原件 | "运行日志已脱敏公开" | 内部留档，脱敏版在 `redacted_evidence/` |
| 内部策略口径 | 不公开 | 仅内部版文档中保留 |
