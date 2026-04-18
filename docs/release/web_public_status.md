# Web 对外口径摘要

## 1. 已浏览器级验证

### 核心功能
- ✅ 统一 UI 模式 v1（顶部主工具栏、左/中画布、右侧固定属性面板）
- ✅ 文本元素的创建、编辑、拖动和调整大小
- ✅ 多选模式和批量操作
- ✅ 元素旋转功能
- ✅ 图层管理（上下移动、置顶、置底）
- ✅ 右侧属性面板滚动
- ✅ 导出 IR（中间表示格式）
- ✅ PDF 导出（通过浏览器打印功能）
- ✅ 项目保存和打开（JSON 格式）
- ✅ 复制粘贴功能

### 技术验证
- ✅ 页面加载成功
- ✅ 所有按钮存在且可点击
- ✅ 属性面板可滚动
- ✅ 导出 IR 功能正常
- ✅ PDF 导出路径稳定
- ✅ 点击瞬移问题已修复
- ✅ 多选旋转功能正常

## 2. 仅 bridge / 脚本层验证

### LaTeX 功能
- ✅ LaTeX 导出（依赖 Python bridge）
- ✅ LaTeX 导入（依赖 Python bridge）
- ✅ 跨端导回（Qt tex → Web）

### 工作流程
- **LaTeX 导出**：点击按钮 → 自动导出 IR → 运行 bridge 脚本 → 生成 LaTeX 文件
- **LaTeX 导入**：准备 LaTeX 文件 → 运行 bridge 脚本 → 生成 JSON → Web 打开 JSON

## 3. Blocked

### 功能限制
- ❌ 浏览器内原生 LaTeX 导出（依赖 Python bridge）
- ❌ 浏览器内原生 LaTeX 导入（依赖 Python bridge）
- ❌ 部分高级字段支持（颜色、对齐等）
- ❌ 直接从浏览器打开 LaTeX 文件（需要先通过 bridge 转换）

### 技术限制
- ❌ 浏览器内无法直接处理 LaTeX 文件
- ❌ 部分高级排版功能暂未支持

## 4. 技术依赖

### 浏览器端
- 纯 HTML/CSS/JavaScript
- 无外部依赖
- 直接打开 `web_prototype/index.html` 即可运行

### Bridge 依赖
- Python 3
- ExportCore 模块
- JSON 处理

## 5. 跨端验证

### 验证结果
- ✅ Qt 导出的 conforming tex 可以通过 bridge 导回 Web
- ✅ 保留了所有核心几何和内容字段
- ✅ 转换了字体相关字段和层级字段
- ✅ 生成了详细的字段差异分析

### 验证文件
- **输入文件**：`docs/contest_evidence/screenshots/qt_fidelity_export.tex`
- **导回结果**：`web_prototype/web_import_from_qt.json`
- **差异分析**：`web_prototype/web_import_from_qt_diff.json`
- **验证日志**：`web_prototype/web_import_from_qt_log.txt`

## 6. 演示建议

### 最佳演示功能
1. **统一 UI 模式**：顶部主工具栏、左/中画布、右侧固定属性面板的布局
2. **文本元素操作**：创建、编辑、拖动、调整大小
3. **多选与旋转**：选择多个元素并批量旋转
4. **图层管理**：元素上下移动、置顶、置底
5. **导出功能**：导出 IR、PDF 导出

### 注意事项
- 强调 Web 是独立应用候选版
- 明确说明 LaTeX 功能依赖 bridge
- 不要宣称浏览器内原生支持 LaTeX 导入/导出
- 突出已实现的核心功能和技术亮点

## 7. 里程碑表述

> Web 已经是独立应用候选版，统一 UI 模式 v1 稳定，Playwright regression 稳定，LaTeX 闭环已支持“Qt tex → Web 导回”的跨端路径（依赖 bridge）。