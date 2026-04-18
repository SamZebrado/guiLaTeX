# guiLaTeX 公开候选材料最终筛查清单

**编制**：外务大臣
**日期**：2026-04-13

---

## 一、docs/release/ 下本轮新增文档

| 文件 | 敏感信息 | 适合公开 | 处理建议 |
|------|----------|----------|----------|
| `web_demo_ready_list.md` | 无 | ✅ 适合 | 直接公开 |
| `web_demo_shot_list.md` | 无 | ✅ 适合 | 直接公开 |
| `web_public_status.md` | 无 | ✅ 适合 | 直接公开 |
| `qt_demo_ready_list.md` | 无 | ✅ 适合 | 直接公开 |
| `qt_demo_shot_list.md` | 无 | ✅ 适合 | 直接公开 |
| `qt_public_status.md` | 无 | ✅ 适合 | 直接公开 |
| `public_project_overview.md` | 无 | ✅ 适合 | 直接公开（本轮新增） |
| `demo_asset_index.md` | 无 | ✅ 适合 | 直接公开（本轮新增） |
| `demo_master_shot_list.md` | 无 | ✅ 适合 | 直接公开（本轮新增） |
| `forum_update_draft.md` | 无 | ✅ 适合 | 直接公开（本轮新增） |
| `public_sanitization_checklist.md` | 无 | ✅ 适合 | 直接公开（本轮新增） |

## 二、Web/Qt 演示文档中的内部口径

| 文件 | 内部痕迹 | 适合公开 | 处理建议 |
|------|----------|----------|----------|
| `qt_demo_ready_list.md` | 含"最不该说满的点"内部策略节 | ⚠️ 需摘要化 | 公开时删除该节，或替换为通用"注意事项" |
| `qt_demo_shot_list.md` | 含"不该说满的话"内部口径 | ⚠️ 需摘要化 | 公开时保留"对外可说"，删除"不该说满" |
| `web_demo_shot_list.md` | 同上 | ⚠️ 需摘要化 | 同上 |
| `web_public_status.md` | 无内部痕迹 | ✅ 适合 | 直接公开（已是最精炼的口径文件） |
| `qt_public_status.md` | 无内部痕迹 | ✅ 适合 | 直接公开（已是最精炼的口径文件） |

## 三、Canonical Pack

| 文件 | 敏感信息 | 适合公开 | 处理建议 |
|------|----------|----------|----------|
| `qt_canonical_source_model.json` | 无 | ✅ 适合 | 直接公开 |
| `qt_canonical_normalized_ir.json` | 无 | ✅ 适合 | 直接公开 |
| `qt_canonical_exported.tex` | 无 | ✅ 适合 | 直接公开 |
| `qt_canonical_imported_ir.json` | 无 | ✅ 适合 | 直接公开 |
| `qt_canonical_final_caliber.json` | 无 | ✅ 适合 | 直接公开 |
| `qt_canonical_roundtrip_diff_report.json` | **含 4 处 `/Users/samzebrado/` 路径** | ⚠️ 需脱敏 | 替换路径后公开 |
| `qt_canonical_handoff_readme.md` | 含"最不该说满的点"内部策略 | ⚠️ 需摘要化 | 公开时删除内部策略节 |

## 四、Web-to-Core Bridge 目录

| 目录 | 敏感信息 | 证据性质 | 适合公开 | 处理建议 |
|------|----------|----------|----------|----------|
| `web_to_core_bridge/` | 无 | 合成/测试 | ✅ 适合 | 直接公开 |
| `web_to_core_bridge_20260412_163536/` | 无 | 真实 | ✅ 适合 | 直接公开 |
| `web_to_core_bridge_fresh_20260412_164438/` | **execution_log 含路径** | 真实 | ⚠️ 需脱敏 | 脱敏 execution_log，其余直接公开 |
| `web_to_core_bridge_fresh_20260412_164500/` | **execution_log 含路径** | 真实 | ⚠️ 需脱敏 | 同上 |
| `web_to_core_bridge_synthetic_20260412_165000/` | **execution_log 含路径** | 合成/模拟 | ❌ 不建议 | 内部留档（合成证据不宜作真实证据） |
| `web_to_core_bridge_real_20260412_172210/` | **execution_log 含路径** | 真实 | ⚠️ 需脱敏 | 脱敏 execution_log，tex/json/png 直接公开 |
| `web_to_core_bridge_real_20260412_172747/` | **execution_log 含路径** | 真实 | ⚠️ 需脱敏 | 同上（与上条选一即可，内容重复） |

## 五、已有截图目录

| 文件 | 适合公开 | 处理建议 |
|------|----------|----------|
| `web_regression_v4_*.png/json` (6个) | ✅ 适合 | 直接公开（最终版证据） |
| `web_regression_v3_*.png/json` (4个) | ✅ 适合 | 可公开（历史中间版本） |
| `web_regression_*.png/json` (v1, 4个) | ✅ 适合 | 可公开（历史中间版本） |
| `web_test_*.png/json` (4个) | ✅ 适合 | 可公开（早期测试） |
| `16_gui_screenshot.png` | ✅ 适合 | 直接公开（Qt 界面截图） |
| `qt_rotation_test_*.png` (4个) | ✅ 适合 | 直接公开 |
| `18_qt_demo_model_export.json` | ✅ 适合 | 直接公开 |
| `qt_to_core_*.json` (2个) | ✅ 适合 | 直接公开 |

## 六、汇总

### 已适合公开（无需处理）
- docs/release/ 全部 11 个文档（除内部策略节外）
- web_to_core_bridge/ 和 web_to_core_bridge_20260412_163536/ 全部文件
- qt_canonical_pack/ 中 6 个文件（除 roundtrip_diff_report.json）
- 全部已有截图和 JSON 证据
- showcase/ 展示页

### 需脱敏后公开（6 个文件）
1. `qt_canonical_roundtrip_diff_report.json` — 4 处路径
2. `web_to_core_bridge_fresh_20260412_164438/execution_log_*.txt` — 3 处路径
3. `web_to_core_bridge_fresh_20260412_164500/execution_log_*.txt` — 6+ 处路径
4. `web_to_core_bridge_real_20260412_172210/execution_log_*.txt` — 8+ 处路径
5. `web_to_core_bridge_real_20260412_172747/execution_log_*.txt` — 8+ 处路径
6. `web_to_core_bridge_synthetic_20260412_165000/execution_log_*.txt` — 10+ 处路径

### 需摘要化后公开（3 个文件）
1. `qt_demo_ready_list.md` — 删除"最不该说满的点"节
2. `qt_demo_shot_list.md` — 删除"不该说满的话"列
3. `qt_canonical_handoff_readme.md` — 删除内部策略节

### 不建议公开（1 个目录）
1. `web_to_core_bridge_synthetic_20260412_165000/` — 合成证据，不宜作真实证据

### 内部留档（无需公开）
- `web_to_core_bridge_fresh_*/` 和 `web_to_core_bridge_real_*/` 中的 execution_log 原件（脱敏后公开摘要版即可）
