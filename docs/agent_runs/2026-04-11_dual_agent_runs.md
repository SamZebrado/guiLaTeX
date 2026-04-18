# Dual Agent Runs (2026-04-11 起)

## Qt 侧新 Round（desktop closing round）

### 一、已验证的功能（证据充分）

| 功能 | 验证状态 | 证据文件 |
|------|----------|----------|
| Qt roundtrip 主闭环完整验证 | ✅ 已验证 | [qt_roundtrip_verification.py](<repo-root>/tests/qt_roundtrip_verification.py) |
| normalize_qt_model_to_ir(...) 真实调用 | ✅ 已验证 | [qt_roundtrip_verification.py](<repo-root>/tests/qt_roundtrip_verification.py#L47) |
| export_ir_to_latex(...) 真实调用 | ✅ 已验证 | [qt_roundtrip_verification.py](<repo-root>/tests/qt_roundtrip_verification.py#L50) |
| import_own_exported_tex_to_ir(...) 真实调用 | ✅ 已验证 | [qt_roundtrip_verification.py](<repo-root>/tests/qt_roundtrip_verification.py#L59) |
| 真实生成 conforming .tex | ✅ 已验证 | [qt_roundtrip_export.tex](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_export.tex) |
| 字段保留差异报告 | ✅ 已验证 | [qt_roundtrip_field_difference_report.json](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_field_difference_report.json) |
| 右侧属性面板滚动 | ✅ 已验证 | [properties.py](<repo-root>/src/gui/properties.py#L28-L53) |
| 统一 UI 模式 v1 保持 | ✅ 已验证 | [main.py](<repo-root>/src/gui/main.py) |

### 二、Roundtrip 字段保留情况

| 字段 | 保住状态 | 说明 |
|------|----------|------|
| id | ✅ 保住 | |
| content | ✅ 保住 | |
| page | ✅ 保住 | |
| x / y / width / height | ✅ 保住 | |
| rotation | ✅ 保住 | |
| visible | ✅ 保住 | |
| font_size | ✅ 保住 | |
| color | ✅ 保住 | |
| alignment | ✅ 保住 | |
| type | ⚠️ 有差异 | 原始是 "textbox"/"paragraph"，导入变成元素 ID |
| layer | ⚠️ 有差异 | 原始是 9/8/7，导入变成 1/2/3 |
| font_family_zh | ⚠️ 有差异 | 原始是安全字体，导入变成 'SimSun'（ExportCore 硬编码） |
| font_family_en | ⚠️ 有差异 | 原始是安全字体，导入变成 'Times New Roman'（ExportCore 硬编码） |

### 三、Qt 导出/导入闭环链路说明

#### 已打通链路（桌面端完整）
1. **Qt 模型 → IR**
   - 入口：qt_roundtrip_verification.py
   - 调用函数：normalize_qt_model_to_ir(...)
   - 证据：[qt_roundtrip_normalized_ir.json](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_normalized_ir.json)

2. **IR → conforming LaTeX**
   - 入口：qt_roundtrip_verification.py
   - 调用函数：export_ir_to_latex(...)
   - 证据：[qt_roundtrip_export.tex](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_export.tex)

3. **conforming LaTeX → IR**
   - 入口：qt_roundtrip_verification.py
   - 调用函数：import_own_exported_tex_to_ir(...)
   - 证据：[qt_roundtrip_imported_ir.json](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_imported_ir.json)

4. **IR → Qt 可编辑对象**
   - 入口：qt_roundtrip_verification.py
   - 完成验证：字段比较完成
   - 证据：[qt_roundtrip_field_difference_report.json](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_field_difference_report.json)

### 四、导出语义说明

| 功能 | 当前语义 | 说明 |
|------|----------|------|
| 保存项目 | 未实现 | |
| 导出 IR | 导出当前模型为 IR JSON | temp/guiLaTeX_export_ir.json |
| 导出 LaTeX | 通过 Core 导出 conforming LaTeX | temp/guiLaTeX_export.tex |
| 导出 PDF | 直接复制现有 PDF | 不是 Core->tex->编译路径 |

### 五、保存的证据文件

| 文件 | 说明 |
|------|------|
| [qt_roundtrip_original_model.json](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_original_model.json) | 原始测试模型 |
| [qt_roundtrip_normalized_ir.json](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_normalized_ir.json) | 标准化后的 IR |
| [qt_roundtrip_export.tex](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_export.tex) | 导出的 LaTeX 文件 |
| [qt_roundtrip_imported_ir.json](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_imported_ir.json) | 导回的 IR |
| [qt_roundtrip_field_difference_report.json](<repo-root>/docs/contest_evidence/screenshots/qt_roundtrip_field_difference_report.json) | 字段保留差异报告 |

### 六、下一步计划

1. 保持 Qt roundtrip 固化，不要回退
2. 继续稳住统一 UI 模式 v1，不再大扩无关功能
3. 实现打开项目 / 保存项目功能
4. 完善 PDF 导出流程，通过 Core->tex->编译得到
5. 优化 ExportCore 中的字体硬编码问题

## Web 侧新 Round

### 一、已浏览器级验证（Playwright 证据充分）

| 功能 | 验证状态 | 证据文件 |
|------|----------|----------|
| 右侧属性面板滚动 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 点击对象中心后位置不变 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 点击对象偏右下后位置不变 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 多选两个对象后执行旋转，两个对象的 rotation 都变化 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 导出 IR 按钮存在且结果包含关键字段 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| PDF 导出按钮存在且 print 路径仍可触发 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 右侧属性面板可滚动 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 统一 UI 模式 v1 保持 | ✅ 已验证 | [index.html](<repo-root>/web_prototype/index.html) |
| 导出 LaTeX 按钮存在 | ✅ 已验证 | [index.html](<repo-root>/web_prototype/index.html) |
| 导入 LaTeX 按钮存在 | ✅ 已验证 | [index.html](<repo-root>/web_prototype/index.html) |

### 二、仅逻辑层/脚本层验证（无浏览器级证据）

| 功能 | 验证状态 | 证据文件 |
|------|----------|----------|
| Web model → IR | ✅ 已验证 | [exportToIR函数](<repo-root>/web_prototype/index.html#L1559-L1586) |
| IR → 项目风格 LaTeX（通过 bridge） | ✅ 已验证 | [web_to_core_bridge.py](<repo-root>/web_prototype/web_to_core_bridge.py) |
| 项目风格 LaTeX → Web 模型（通过 bridge） | ✅ 已验证 | [core_to_web_bridge.py](<repo-root>/web_prototype/core_to_web_bridge.py) |

### 三、Blocked

| 功能 | 阻塞原因 | 阻塞点 |
|------|----------|--------|
| 浏览器内直接导入 LaTeX | 缺少浏览器与 Python 脚本的交互机制 | 需要实现 Web 与本地 Python 脚本的通信 |
| 浏览器内直接导出 LaTeX | 缺少浏览器与 Python 脚本的交互机制 | 需要实现 Web 与本地 Python 脚本的通信 |

### 四、Bridge 依赖项

| 功能 | 依赖 Bridge | Bridge 文件 |
|------|-------------|-------------|
| Web 导出项目风格 LaTeX | 是 | [web_to_core_bridge.py](<repo-root>/web_prototype/web_to_core_bridge.py) |
| 导入项目风格 LaTeX 到 Web | 是 | [core_to_web_bridge.py](<repo-root>/web_prototype/core_to_web_bridge.py) |

### 五、Web 导出/导入闭环链路说明

#### 已打通链路（浏览器内完成，无需 bridge）
1. **Web 模型 → IR**
   - 入口："导出 IR"按钮
   - 文件：[index.html](<repo-root>/web_prototype/index.html#L1559-L1586)

#### 仍依赖 Bridge 的链路
2. **IR → 项目风格 LaTeX**
   - 入口："导出 LaTeX"按钮（提供操作指导）
   - 脚本：[web_to_core_bridge.py](<repo-root>/web_prototype/web_to_core_bridge.py)
   - 执行命令：`python3 web_to_core_bridge.py <input_ir.json> <output.tex>`

3. **项目风格 LaTeX → Web 模型**
   - 入口："导入 LaTeX"按钮（提供操作指导）
   - 脚本：[core_to_web_bridge.py](<repo-root>/web_prototype/core_to_web_bridge.py)
   - 执行命令：`python3 core_to_web_bridge.py <input.tex> <output.json>`
   - 后续步骤：用"打开项目"功能导入生成的 JSON

#### 完全 Blocked 的链路
4. **浏览器内直接导入/导出 LaTeX**：无实现
   - 原因：当前浏览器无法直接运行 Python 脚本

### 六、技术实现详情

#### 右侧属性面板滚动
- 实现方式：CSS `max-height: calc(100vh - 80px)` 和 `overflow-y: auto`
- 文件：[index.html](<repo-root>/web_prototype/index.html#L147-L155)

#### Web 导出 IR
- 实现方式：[exportToIR](<repo-root>/web_prototype/index.html#L1559-L1586) 函数
- 覆盖字段：id, type, content, page, x, y, width, height, rotation, layer, font_family_zh, font_family_en, font_size, color, visible

#### 统一 UI 模式 v1
- 保持不变：顶部主工具栏、左/中画布+右侧固定属性面板、右侧分组明确、全中文界面
- 默认字体：Noto Sans SC, Source Han Sans SC, Inter, Noto Sans, Sans Serif

### 七、保存的证据文件

| 文件 | 说明 |
|------|------|
| [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) | Playwright 测试结果 |
| [regression_test_results_v2.json](<repo-root>/web_prototype/regression_test_results_v2.json) | Playwright 测试 JSON 结果 |
| [regression_initial_page.png](<repo-root>/web_prototype/regression_initial_page.png) | 初始页面截图 |
| [temp/web_to_core/web_real_export_output.tex](<repo-root>/temp/web_to_core/web_real_export_output.tex) | 导出的 LaTeX 文件 |
| [temp/core_to_web/core_to_web_import_output.json](<repo-root>/temp/core_to_web/core_to_web_import_output.json) | 导入转换的 JSON 文件 |

### 八、下一步计划

1. 保持 Playwright regression 固化，不要回退
2. 继续稳住统一 UI 模式 v1，不再大扩无关功能
3. 为将来与 Core 的正式对接继续留清晰接口，但不自发明第二套不兼容 tex 规范
4. 探索浏览器内直接导入/导出 LaTeX 的方案（如需）