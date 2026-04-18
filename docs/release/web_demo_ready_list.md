# Web 演示准备清单

## 1. 最适合录制的 Web 功能

### 1.1 统一 UI 模式展示
- **功能说明**：展示 Web 应用的统一 UI 布局，包括顶部主工具栏、左/中画布和右侧固定属性面板
- **证据文件**：
  - [regression_initial_page.png](web_prototype/regression_initial_page.png)
  - [regression_test_output_v2.txt](web_prototype/regression_test_output_v2.txt)
- **录制建议**：
  - 打开 Web 应用，展示整体布局
  - 演示响应式设计（调整浏览器窗口大小）
  - 展示右侧属性面板的滚动功能
- **能力层级**：浏览器级
- **注意事项**：
  - 可以说："Web 应用采用统一 UI 模式 v1，布局清晰，操作直观"
  - 不该说满：无需特别说明限制

### 1.2 文本元素操作
- **功能说明**：演示文本元素的创建、编辑、拖动和调整大小
- **证据文件**：
  - [regression_click_teleportation.png](web_prototype/regression_click_teleportation.png)
  - [regression_click_teleportation.json](web_prototype/regression_click_teleportation.json)
- **录制建议**：
  - 选择一个文本元素
  - 编辑文本内容
  - 拖动元素到新位置
  - 调整元素大小
- **能力层级**：浏览器级
- **注意事项**：
  - 可以说："文本元素操作流畅，支持实时编辑和调整"
  - 不该说满：无需特别说明限制

### 1.3 多选与旋转功能
- **功能说明**：演示选择多个元素并进行批量旋转操作
- **证据文件**：
  - [regression_multi_select_rotation.png](web_prototype/regression_multi_select_rotation.png)
  - [regression_multi_select_rotation.json](web_prototype/regression_multi_select_rotation.json)
- **录制建议**：
  - 启用多选模式
  - 选择多个元素
  - 使用旋转滑块调整旋转角度
  - 展示所有选中元素同时旋转
- **能力层级**：浏览器级
- **注意事项**：
  - 可以说："支持多选模式，可对多个元素进行批量旋转操作"
  - 不该说满：无需特别说明限制

### 1.4 图层管理
- **功能说明**：演示元素的图层管理功能，包括上下移动、置顶、置底
- **证据文件**：
  - [regression_test_output_v2.txt](web_prototype/regression_test_output_v2.txt)
- **录制建议**：
  - 创建多个重叠元素
  - 使用图层管理按钮调整元素层级
  - 展示元素前后顺序的变化
- **能力层级**：浏览器级
- **注意事项**：
  - 可以说："支持完整的图层管理功能，可调整元素的前后顺序"
  - 不该说满：无需特别说明限制

### 1.5 导出功能
- **功能说明**：演示导出 IR 和 PDF 功能
- **证据文件**：
  - [regression_export_ir.json](web_prototype/regression_export_ir.json)
  - [regression_test_output_v2.txt](web_prototype/regression_test_output_v2.txt)
- **录制建议**：
  - 点击 "导出 IR" 按钮，展示生成的 JSON 文件
  - 点击 "导出 PDF" 按钮，展示浏览器打印功能
- **能力层级**：浏览器级
- **注意事项**：
  - 可以说："支持导出 IR 中间格式和 PDF 格式"
  - 不该说满：无需特别说明限制

## 2. LaTeX 功能（作为补充演示）

### 2.1 LaTeX 导出
- **功能说明**：演示 LaTeX 导出流程
- **证据文件**：
  - [web_real_export_output.tex](temp/web_to_core/web_real_export_output.tex)
- **录制建议**：
  - 点击 "导出 LaTeX" 按钮
  - 展示自动导出的 IR 文件
  - 简要说明需要运行 bridge 脚本生成 LaTeX
- **能力层级**：bridge 级
- **注意事项**：
  - 可以说："支持导出自家风格的 LaTeX 文件"
  - 不该说满："需要通过 Python bridge 脚本完成转换"

### 2.2 LaTeX 导入
- **功能说明**：演示 LaTeX 导入流程
- **证据文件**：
  - [web_import_from_qt.json](web_prototype/web_import_from_qt.json)
  - [web_import_from_qt_diff.json](web_prototype/web_import_from_qt_diff.json)
- **录制建议**：
  - 简要说明需要运行 bridge 脚本将 LaTeX 转换为 JSON
  - 点击 "打开项目" 按钮，选择生成的 JSON 文件
  - 展示导入的内容
- **能力层级**：bridge 级
- **注意事项**：
  - 可以说："支持导入 conforming LaTeX 文件"
  - 不该说满："需要通过 Python bridge 脚本完成转换"

## 3. 演示注意事项

### 3.1 浏览器级能力
- ✅ 统一 UI 模式 v1
- ✅ 文本元素操作
- ✅ 多选与旋转
- ✅ 图层管理
- ✅ 导出 IR
- ✅ PDF 导出（通过浏览器打印）
- ✅ 项目保存和打开（JSON）
- ✅ 复制粘贴功能

### 3.2 Bridge 级能力
- ✅ LaTeX 导出（依赖 Python bridge）
- ✅ LaTeX 导入（依赖 Python bridge）
- ✅ 跨端导回（Qt tex → Web）

### 3.3 Blocked 能力
- ❌ 浏览器内原生 LaTeX 导出
- ❌ 浏览器内原生 LaTeX 导入
- ❌ 部分高级字段支持（颜色、对齐等）
- ❌ 直接从浏览器打开 LaTeX 文件

## 4. 演示环境准备

### 4.1 本地运行
- 直接打开 `web_prototype/index.html` 文件
- 无需安装任何依赖

### 4.2 测试验证
- Playwright 回归测试：`node playwright_regression_test_v2.js`
- 跨端验证：使用 `qt_fidelity_export.tex` 测试导回功能

### 4.3 Bridge 脚本准备
- LaTeX 导出：`python3 web_to_core_bridge.py <input_ir.json> <output.tex>`
- LaTeX 导入：`python3 core_to_web_bridge.py <latex_file> <output_json>`