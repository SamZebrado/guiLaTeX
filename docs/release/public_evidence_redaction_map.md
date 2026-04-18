# guiLaTeX 公开证据脱敏映射表

**编制**：外务大臣
**日期**：2026-04-13

---

## 一、直接公开（无需处理）

| 原始文件 | 状态 | 说明 |
|----------|------|------|
| `web_to_core_bridge/` 全部 7 个文件 | ✅ 直接公开 | 无敏感信息 |
| `web_to_core_bridge_20260412_163536/` 全部 4 个文件 | ✅ 直接公开 | 无敏感信息 |
| `qt_canonical_pack/qt_canonical_source_model.json` | ✅ 直接公开 | 无敏感信息 |
| `qt_canonical_pack/qt_canonical_normalized_ir.json` | ✅ 直接公开 | 无敏感信息 |
| `qt_canonical_pack/qt_canonical_exported.tex` | ✅ 直接公开 | 无敏感信息 |
| `qt_canonical_pack/qt_canonical_imported_ir.json` | ✅ 直接公开 | 无敏感信息 |
| `qt_canonical_pack/qt_canonical_final_caliber.json` | ✅ 直接公开 | 无敏感信息 |
| `docs/contest_evidence/screenshots/` 全部 PNG/JSON | ✅ 直接公开 | 无敏感信息 |
| `docs/release/web_public_status.md` | ✅ 直接公开 | 最精炼口径文件 |
| `docs/release/qt_public_status.md` | ✅ 直接公开 | 最精炼口径文件 |
| `docs/release/public_project_overview.md` | ✅ 直接公开 | 总装版总览 |
| `docs/release/demo_asset_index.md` | ✅ 直接公开 | 演示资产索引 |
| `docs/release/demo_master_shot_list.md` | ✅ 直接公开 | 总录制脚本 |
| `docs/release/forum_update_draft.md` | ✅ 直接公开 | 论坛贴草稿 |

## 二、脱敏后公开

| 原始文件 | 敏感内容 | 脱敏副本路径 | 处理方式 |
|----------|----------|-------------|----------|
| `web_to_core_bridge_fresh_20260412_164438/execution_log_20260412_164438.txt` | 3 处 `/Users/samzebrado/...` | `docs/release/redacted_evidence/execution_log_20260412_164438.redacted.txt` | 路径 → `<project_root>/` |
| `web_to_core_bridge_fresh_20260412_164500/execution_log_20260412_164500.txt` | 6+ 处 `/Users/samzebrado/...` | `docs/release/redacted_evidence/execution_log_20260412_164500.redacted.txt` | 路径 → `<project_root>/` |
| `web_to_core_bridge_real_20260412_172210/execution_log_20260412_172210.txt` | 8+ 处 `/Users/samzebrado/...` | `docs/release/redacted_evidence/execution_log_20260412_172210.redacted.txt` | 路径 → `<project_root>/` |
| `web_to_core_bridge_real_20260412_172747/execution_log_20260412_172747.txt` | 8+ 处 `/Users/samzebrado/...` | `docs/release/redacted_evidence/execution_log_20260412_172747.redacted.txt` | 路径 → `<project_root>/` |
| `qt_canonical_pack/qt_canonical_roundtrip_diff_report.json` | 4 处 `/Users/samzebrado/...` | `docs/release/redacted_evidence/qt_canonical_roundtrip_diff_report.redacted.json` | 路径 → `<project_root>/` |

> 注：以上目录中的 .tex、.json（非 diff report）、.png 文件均无敏感信息，可直接公开。只有 execution_log 和 diff report 需要脱敏。

## 三、仅摘要公开

| 原始文件 | 原因 | 处理方式 |
|----------|------|----------|
| `web_to_core_bridge_synthetic_20260412_165000/` 全部 | 合成/模拟证据，不宜作真实证据公开 | 内部留档，公开时标注"存在合成测试验证"即可 |
| `qt_canonical_handoff_readme.md` | 含"最不该说满的点"内部策略节 | 摘要版见下方 |
| `qt_demo_ready_list.md` | 含内部策略节 | 公开版删除"最不该说满的点"节，保留功能清单 |
| `qt_demo_shot_list.md` | 含"不该说满的话"列 | 公开版删除"不该说满的话"列，保留"对外可说"列 |
| `web_demo_shot_list.md` | 含"不该说满的话"列 | 同上 |

### qt_canonical_handoff_readme.md 摘要公开版

> **Qt Canonical Pack 交接说明（公开版）**
>
> 本目录包含 Qt 端 roundtrip 验证的完整证据链：
> 1. `qt_canonical_source_model.json` — Qt 原始数据模型
> 2. `qt_canonical_normalized_ir.json` — Core normalize 输出
> 3. `qt_canonical_exported.tex` — Core 导出 LaTeX
> 4. `qt_canonical_imported_ir.json` — 重新导入后的 IR
> 5. `qt_canonical_roundtrip_diff_report.json` — Roundtrip 字段级差异
>
> **Web 端验证**：将 `qt_canonical_exported.tex` 通过 bridge 转换后导入 Web 端，可验证跨端一致性。
>
> **已知限制**：font_family_zh 硬编码为 SimSun、font_family_en 硬编码为 Times New Roman（Core 层问题）。

## 四、内部留档

| 原始文件 | 原因 |
|----------|------|
| `web_to_core_bridge_synthetic_20260412_165000/execution_log_*.txt` | 合成证据 + 含敏感路径 |
| 全部原始 execution_log 原件 | 含敏感路径，脱敏副本已生成 |
| `qt_canonical_roundtrip_diff_report.json` 原件 | 含敏感路径，脱敏副本已生成 |
