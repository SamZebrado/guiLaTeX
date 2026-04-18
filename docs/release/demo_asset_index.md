# guiLaTeX 总演示资产索引

**编制**：外务大臣
**日期**：2026-04-13

---

## 一、Web 端资产

### 1.1 截图证据

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `web_demo_screenshot.png` | `docs/contest_evidence/screenshots/` | Web 端基本界面（Hello guiLaTeX + JSON 预览） | 浏览器级 | ✅ 适合 | 论坛贴 / README |
| `web_regression_v4_initial_page.png` | `docs/contest_evidence/screenshots/` | v4 统一 UI 初始页面 | 浏览器级 | ✅ 适合 | README / 展示页 |
| `web_regression_v4_click_teleportation.png` | `docs/contest_evidence/screenshots/` | 点击元素后光标正确定位 | 浏览器级 | ✅ 适合 | 论坛贴 / 截图 |
| `web_regression_v4_multi_select_rotation.png` | `docs/contest_evidence/screenshots/` | 多选元素旋转 45° | 浏览器级 | ✅ 适合 | 论坛贴 / 视频 |
| `web_regression_v4_export_ir_result.json` | `docs/contest_evidence/screenshots/` | 导出 IR 字段列表 | 浏览器级 | ✅ 适合 | 交接 / 技术展示 |
| `page_screenshot_20260412_172210.png` | `docs/contest_evidence/web_to_core_bridge_real_20260412_172210/` | Bridge 真实运行截图 | 浏览器级 | ✅ 适合 | 论坛贴 / 视频 |
| `page_screenshot_20260412_172747.png` | `docs/contest_evidence/web_to_core_bridge_real_20260412_172747/` | Bridge 真实运行截图（第二次） | 浏览器级 | ⚠️ 与上条重复，选一即可 | 技术展示 |

### 1.2 JSON 证据

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `web_regression_v4_click_teleportation_result.json` | `docs/contest_evidence/screenshots/` | 点击坐标精确匹配 | 浏览器级 | ✅ 适合 | 交接 |
| `web_regression_v4_multi_select_rotation_result.json` | `docs/contest_evidence/screenshots/` | 旋转角度精确匹配 | 浏览器级 | ✅ 适合 | 交接 |
| `web_real_exported_ir_20260412_163536.json` | `docs/contest_evidence/web_to_core_bridge_20260412_163536/` | 浏览器导出 IR 结构 | 浏览器级 | ✅ 适合 | 技术展示 |
| `web_real_exported_ir_20260412_172210.json` | `docs/contest_evidence/web_to_core_bridge_real_20260412_172210/` | 真实运行导出 IR | 浏览器级 | ✅ 适合 | 交接 |
| `web_real_exported_ir_20260412_172747.json` | `docs/contest_evidence/web_to_core_bridge_real_20260412_172747/` | 真实运行导出 IR（第二次） | 浏览器级 | ⚠️ 与上条重复 | 交接 |

### 1.3 LaTeX 证据

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `web_real_export_output.tex` | `docs/contest_evidence/web_to_core_bridge/` | Bridge 导出 LaTeX 输出 | 脚本级 | ✅ 适合 | 论坛贴 / 技术展示 |
| `web_to_core_output.tex` | `docs/contest_evidence/web_to_core_bridge/` | Web IR → Core → LaTeX 转换 | 脚本级 | ✅ 适合 | 技术展示 |
| `web_real_export_output_20260412_172210.tex` | `docs/contest_evidence/web_to_core_bridge_real_20260412_172210/` | 真实运行 LaTeX 输出 | 脚本级 | ✅ 适合 | 交接 |
| `web_import_from_qt_diff.json` | `docs/release/` | Qt tex → Web 导回差异分析 | 脚本级 | ✅ 适合 | 跨端验证展示 |

### 1.4 测试日志

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `regression_test_log.txt` | `docs/contest_evidence/web_to_core_bridge_real_20260412_172210/` | Playwright 回归测试通过 | 浏览器级 | ✅ 适合 | 技术展示 |

---

## 二、Qt 端资产

### 2.1 Canonical Pack（核心证据链）

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `qt_canonical_source_model.json` | `docs/contest_evidence/qt_canonical_pack/` | Qt 原始数据模型 | 桌面级 | ✅ 适合 | 交接 / 技术展示 |
| `qt_canonical_normalized_ir.json` | `docs/contest_evidence/qt_canonical_pack/` | Core normalize 输出 | 桌面级 | ✅ 适合 | 交接 |
| `qt_canonical_exported.tex` | `docs/contest_evidence/qt_canonical_pack/` | Core 导出 LaTeX | 桌面级 | ✅ 适合 | 论坛贴 / 技术展示 |
| `qt_canonical_imported_ir.json` | `docs/contest_evidence/qt_canonical_pack/` | 重新导入后的 IR | 桌面级 | ✅ 适合 | 交接 |
| `qt_canonical_roundtrip_diff_report.json` | `docs/contest_evidence/qt_canonical_pack/` | Roundtrip 字段级差异 | 桌面级 | ✅ 适合（需脱敏） | 交接 / 技术展示 |
| `qt_canonical_final_caliber.json` | `docs/contest_evidence/qt_canonical_pack/` | 最终校准数据 | 桌面级 | ✅ 适合 | 交接 |

### 2.2 截图

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `16_gui_screenshot.png` | `docs/contest_evidence/screenshots/` | Qt 桌面端界面（guiLaTeX 编辑器） | 桌面级 | ✅ 适合 | README / 展示页 |
| `qt_rotation_test_text_0.png` | `docs/contest_evidence/screenshots/` | 文本旋转 0° 基线 | 桌面级 | ✅ 适合 | 论坛贴 |
| `qt_rotation_test_text_45.png` | `docs/contest_evidence/screenshots/` | 文本旋转 45° | 桌面级 | ✅ 适合 | 论坛贴 / 视频 |
| `qt_rotation_test_image_0.png` | `docs/contest_evidence/screenshots/` | 图片旋转 0° 基线 | 桌面级 | ⚠️ 可选 | 技术展示 |
| `qt_rotation_test_image_30.png` | `docs/contest_evidence/screenshots/` | 图片旋转 ~15-20° | 桌面级 | ⚠️ 可选 | 技术展示 |

---

## 三、Core / 共享资产

### 3.1 回归样本

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `golden_sample_ir.tex` | `export_core/samples/` | Golden sample LaTeX 输出 | 脚本级 | ✅ 适合 | 交接 |
| `regression_sample_1_rotation.tex` | `export_core/samples/` | 旋转场景 LaTeX 输出 | 脚本级 | ✅ 适合 | 交接 |
| `regression_sample_2_layers.tex` | `export_core/samples/` | 图层场景 LaTeX 输出 | 脚本级 | ✅ 适合 | 交接 |
| `regression_sample_3_same_layer.json` | `export_core/samples/` | 同层多元素 IR 数据 | 脚本级 | ✅ 适合 | 交接 |

### 3.2 Bridge 脚本

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `web_to_core_bridge.py` | `docs/contest_evidence/web_to_core_bridge/` | Web IR → Core LaTeX 桥接 | 脚本级 | ✅ 适合 | 交接 |
| `core_to_web_bridge.py` | `docs/contest_evidence/web_to_core_bridge/` | Core LaTeX → Web JSON 桥接 | 脚本级 | ✅ 适合 | 交接 |

---

## 四、Showcase / 叙事资产

| 文件名 | 相对路径 | 证明了什么 | 证据等级 | 公开展示 | 推荐用途 |
|--------|----------|-----------|----------|----------|----------|
| `showcase/index.html` | `release_public/showcase/` | 宫廷风开发展示页 | — | ✅ 适合 | GitHub Pages / 论坛贴 |
| `showcase/assets/court-1-chancellor.jpg` | `release_public/showcase/assets/` | 丞相奏报画像 | — | ✅ 适合 | 展示页 |
| `showcase/assets/court-2-princes.jpg` | `release_public/showcase/assets/` | 四皇子争储画像 | — | ✅ 适合 | 展示页 |
| `showcase/assets/court-3-retire.jpg` | `release_public/showcase/assets/` | 退朝保重龙体画像 | — | ✅ 适合 | 展示页 |
| `整活_争储朝堂/丞相批红_代陛下阅今日朝报.md` | `整活_争储朝堂/` | 完整宫廷叙事 | — | ✅ 适合 | 展示页 / 项目文化 |
| `docs/contest_evidence/lessons_learned.md` | `docs/contest_evidence/` | 开发经验总结 | 文档级 | ✅ 适合 | 论坛贴 / 技术展示 |
| `docs/contest_evidence/dev_journal.md` | `docs/contest_evidence/` | 开发日志 | 文档级 | ✅ 适合 | 项目文化 |

---

## 五、不适合公开的资产

| 文件/目录 | 原因 | 处理建议 |
|-----------|------|----------|
| `*_bridge_fresh_*/execution_log_*.txt` (3个) | 含 `/Users/.../` 路径 | 脱敏后可公开，或只公开 tex/json |
| `*_bridge_synthetic_*/execution_log_*.txt` | 含路径 + 合成证据不宜作真实证据 | 内部留档 |
| `*_bridge_real_*/execution_log_*.txt` (2个) | 含 `/Users/.../` 路径 | 脱敏后可公开，或只公开 tex/json/png |
| `qt_canonical_roundtrip_diff_report.json` | 含 4 处本地路径 | 脱敏后可公开 |
