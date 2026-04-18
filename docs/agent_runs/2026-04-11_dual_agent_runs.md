# Dual Agent Runs (2026-04-11 起)

## Web 侧新 Round

### 一、已浏览器级验证

| 功能 | 验证状态 | 证据文件 |
|------|----------|----------|
| 右侧属性面板滚动 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 点击对象中心后位置不变 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 点击对象偏右下后位置不变 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 多选两个对象后执行旋转 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 导出 IR 按钮存在且结果包含关键字段 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| PDF 导出按钮存在且 print 路径可触发 | ✅ 已验证 | [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt) |
| 统一 UI 模式 v1 保持 | ✅ 已验证 | [index.html](<repo-root>/web_prototype/index.html) |

### 二、仅逻辑层/脚本层验证

| 功能 | 验证状态 | 证据文件 |
|------|----------|----------|
| Web model → IR | ✅ 已验证 | [exportToIR函数](<repo-root>/web_prototype/index.html#L1559-L1586) |
| IR → 项目风格 LaTeX（通过 bridge） | ✅ 已验证 | [web_to_core_bridge.py](<repo-root>/web_prototype/web_to_core_bridge.py) |
| 项目风格 LaTeX → Web 模型（通过 bridge） | ✅ 已验证 | [core_to_web_bridge.py](<repo-root>/web_prototype/core_to_web_bridge.py) |

### 三、Blocked

| 功能 | 阻塞原因 | 阻塞点 |
|------|----------|--------|
| 浏览器内直接导入 LaTeX | 缺少浏览器与 Python 脚本的交互机制 | 需要实现 Web 与本地 Python 脚本的通信 |

### 四、Bridge 依赖项

| 功能 | 依赖 Bridge | Bridge 文件 |
|------|-------------|-------------|
| Web 导出项目风格 LaTeX | 是 | [web_to_core_bridge.py](<repo-root>/web_prototype/web_to_core_bridge.py) |
| 导入项目风格 LaTeX 到 Web | 是 | [core_to_web_bridge.py](<repo-root>/web_prototype/core_to_web_bridge.py) |

### 五、Web 导出/导入闭环链路说明

#### 已打通链路
1. **Web 模型 → IR**：浏览器内完成，无需 bridge
   - 入口：`exportToIR()` 函数
   - 文件：[index.html](<repo-root>/web_prototype/index.html#L1559-L1586)

#### 仍依赖 Bridge 的链路
2. **IR → 项目风格 LaTeX**：需要 Python bridge
   - 脚本：[web_to_core_bridge.py](<repo-root>/web_prototype/web_to_core_bridge.py)
   - 执行命令：`python3 web_to_core_bridge.py <input_ir.json> <output.tex>`
   - 输出：`temp/web_to_core/web_real_export_output.tex`

3. **项目风格 LaTeX → Web 模型**：需要 Python bridge
   - 脚本：[core_to_web_bridge.py](<repo-root>/web_prototype/core_to_web_bridge.py)
   - 执行命令：`python3 core_to_web_bridge.py <input.tex> <output.json>`
   - 输出：`temp/core_to_web/core_to_web_import_output.json`

#### 完全 Blocked 的链路
4. **浏览器内直接导入 LaTeX**：无实现
   - 原因：当前浏览器无法直接运行 Python 脚本
   - 备选方案：先通过 bridge 转换为 JSON，再用"打开项目"功能导入

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
4. 探索浏览器内直接导入 LaTeX 的方案（如需）

## Qt 侧新 Round

### 一、已验证

| 功能 | 验证状态 | 证据文件 |
|------|----------|----------|
| 顶部主工具栏分组 | ✅ 已验证 | [main.py](<repo-root>/src/gui/main.py#L96-L195) |
| 右侧属性面板滚动 | ✅ 已验证 | [properties.py](<repo-root>/src/gui/properties.py#L28-L53) |
| 导出 LaTeX 走 Core | ✅ 已验证 | [main.py](<repo-root>/src/gui/main.py#L439-L483) |
| 导入 LaTeX 走 Core | ✅ 已验证 | [main.py](<repo-root>/src/gui/main.py#L485-L541) |
| Roundtrip 测试 | ✅ 已验证 | [qt_roundtrip_test.py](<repo-root>/tests/qt_roundtrip_test.py) |
| 变换菜单 | ✅ 已验证 | [main.py](<repo-root>/src/gui/main.py#L177-L186) |

### 二、Blocked

| 功能 | 阻塞原因 | 阻塞点 |
|------|----------|--------|
| PDF 导出 | 不是通过 Core->tex->编译 | 直接复制现有 PDF |
| 打开/保存项目 | 未实现 | 需要实现文件读写功能 |
| 图层编号变整数 | 未实现 | 需要修改图层编号逻辑 |
| 变换菜单功能 | 仅添加菜单项 | 需要实现具体变换操作 |

### 三、Qt 导出/导入闭环链路

1. **Qt 模型 → IR**：[export_model_to_ir](<repo-root>/src/gui/pdf_canvas.py#L1475-L1577)
2. **IR → 项目风格 LaTeX**：[export_latex](<repo-root>/src/gui/main.py#L439-L483)
3. **项目风格 LaTeX → Qt 模型**：[import_latex](<repo-root>/src/gui/main.py#L485-L541)

### 四、技术实现详情

#### 顶部主工具栏
- 分组：文件、编辑、排列、变换、视图
- 中文标签：全部使用中文
- 快捷键：为常用操作添加了快捷键

#### 右侧属性面板
- 分组：选中信息、内容、几何、字体、对象专属属性、调试信息
- 滚动：使用 QScrollArea 实现
- 字体列表：只保留安全字体

#### Core 集成
- 导出：使用 `normalize_qt_model_to_ir` 和 `export_ir_to_latex`
- 导入：使用 `import_own_exported_tex_to_ir`

### 五、保存的证据文件

| 文件 | 说明 |
|------|------|
| [qt_latex_export.tex](<repo-root>/docs/contest_evidence/screenshots/qt_latex_export.tex) | 导出的 LaTeX 文件 |
| [18_qt_demo_model_export.json](<repo-root>/docs/contest_evidence/screenshots/18_qt_demo_model_export.json) | 导出的模型 JSON |
| [qt_roundtrip_test.py](<repo-root>/tests/qt_roundtrip_test.py) | Roundtrip 测试脚本 |

### 六、下一步计划

1. 继续跟进 Web 的统一 UI 模式 v1
2. 压实正式导出按钮功能
3. 完善变换菜单的具体功能
4. 探索 PDF 导出通过 Core->tex->编译的方案
5. 实现打开/保存项目功能