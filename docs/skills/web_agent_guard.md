# Web v1-candidate 交接说明

## 1. Web 当前最适合录制的功能

### 1.1 核心功能展示
1. **统一 UI 模式**：顶部主工具栏、左/中画布、右侧固定属性面板的布局
2. **文本元素操作**：创建、编辑、拖动、调整大小
3. **多选与旋转**：选择多个元素并批量旋转
4. **图层管理**：元素上下移动、置顶、置底
5. **导出功能**：导出 IR、PDF 导出

### 1.2 技术亮点
1. **无外部依赖**：纯 HTML/CSS/JavaScript 实现
2. **响应式设计**：支持不同屏幕尺寸
3. **流畅的用户体验**：元素拖动、旋转等操作流畅
4. **清晰的属性面板**：分类明确，支持滚动

## 2. Web 当前最不该说满的地方

### 2.1 功能限制
- **LaTeX 导入/导出**：依赖 Python bridge，不是浏览器内原生实现
- **高级字段支持**：颜色、对齐等高级属性暂未支持
- **跨端直接操作**：不能直接从浏览器打开 LaTeX 文件

### 2.2 技术限制
- **浏览器兼容性**：建议使用现代浏览器
- **性能限制**：复杂文档可能会影响性能
- **存储限制**：项目数据存储在本地文件系统

## 3. 能力层级说明

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

## 4. 演示建议

### 4.1 最佳演示流程
1. 打开 Web 应用，展示统一 UI 布局
2. 创建和编辑文本元素
3. 演示多选和旋转功能
4. 展示图层管理操作
5. 导出 IR 和 PDF
6. 简要说明 LaTeX 导入/导出流程（提及 bridge 依赖）

### 4.2 注意事项
- 强调 Web 是独立应用候选版
- 明确说明 LaTeX 功能依赖 bridge
- 不要宣称浏览器内原生支持 LaTeX 导入/导出
- 突出已实现的核心功能和技术亮点

## 5. 技术支持

### 5.1 本地运行
- 直接打开 `web_prototype/index.html` 文件
- 无需安装任何依赖

### 5.2 Bridge 脚本使用
- LaTeX 导出：`python3 web_to_core_bridge.py <input_ir.json> <output.tex>`
- LaTeX 导入：`python3 core_to_web_bridge.py <latex_file> <output_json>`

### 5.3 测试验证
- Playwright 回归测试：`node playwright_regression_test_v2.js`
- 跨端验证：使用 `qt_fidelity_export.tex` 测试导回功能

## 6. 版本信息

- **Web 版本**：v1-candidate（独立应用候选版）
- **UI 模式**：统一 UI 模式 v1
- **测试状态**：Playwright regression 稳定
- **跨端能力**：支持 Qt tex → Web 导回（依赖 bridge）

## 7. 里程碑表述

> Web 已经是独立应用候选版，统一 UI 模式 v1 稳定，Playwright regression 稳定，LaTeX 闭环已支持“Qt tex → Web 导回”的跨端路径（依赖 bridge）。