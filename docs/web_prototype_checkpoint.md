# Web v1-candidate 规范工作流

## 1. 浏览器内已完成的部分

### 1.1 核心功能
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

### 1.2 浏览器级证据
- ✅ 页面加载成功
- ✅ 所有按钮存在且可点击
- ✅ 属性面板可滚动
- ✅ 导出 IR 功能正常
- ✅ PDF 导出路径稳定
- ✅ 点击瞬移问题已修复
- ✅ 多选旋转功能正常

## 2. 依赖 bridge 的部分

### 2.1 LaTeX 导出
**工作流：**
1. 点击 "导出 LaTeX" 按钮
2. 系统自动导出 IR 文件
3. 运行 Python bridge 脚本：`python3 web_to_core_bridge.py <input_ir.json> <output.tex>`
4. 生成的 LaTeX 文件保存在 `temp/web_to_core/` 目录中

### 2.2 LaTeX 导入
**工作流：**
1. 准备 conforming LaTeX 文件（如 Qt 导出的 tex 文件）
2. 运行 Python bridge 脚本：`python3 core_to_web_bridge.py <latex_file> <output_json>`
3. 点击 "打开项目" 按钮，选择生成的 JSON 文件
4. Web 加载并显示导入的内容

## 3. Blocked 的部分

### 3.1 浏览器内原生功能
- ❌ 浏览器内原生 LaTeX 导出（依赖 Python bridge）
- ❌ 浏览器内原生 LaTeX 导入（依赖 Python bridge）
- ❌ 部分高级字段支持（颜色、对齐等）

### 3.2 跨端限制
- ❌ 直接从浏览器打开 LaTeX 文件（需要先通过 bridge 转换）

## 4. 功能处理流程

### 4.1 导出 IR
1. 点击 "导出 IR" 按钮
2. 浏览器内生成 IR JSON 文件
3. 自动下载到本地

### 4.2 导出 PDF
1. 点击 "导出 PDF" 按钮
2. 触发浏览器打印功能
3. 用户选择保存为 PDF

### 4.3 导出自家风格 LaTeX
1. 点击 "导出 LaTeX" 按钮
2. 自动导出 IR 文件
3. 使用 bridge 脚本转换为 LaTeX
4. 生成 conforming LaTeX 文件

### 4.4 导入 conforming LaTeX
1. 使用 bridge 脚本将 LaTeX 转换为 JSON
2. 点击 "打开项目" 按钮
3. 选择生成的 JSON 文件
4. Web 加载并显示内容

## 5. 技术依赖

### 5.1 浏览器端
- 纯 HTML/CSS/JavaScript
- 无外部依赖

### 5.2 Bridge 依赖
- Python 3
- ExportCore 模块
- JSON 处理

## 6. 证据文件

### 6.1 测试结果
- [regression_test_output_v2.txt](<repo-root>/web_prototype/regression_test_output_v2.txt)
- [regression_test_results_v2.json](<repo-root>/web_prototype/regression_test_results_v2.json)

### 6.2 跨端验证
- [web_import_from_qt.json](<repo-root>/web_prototype/web_import_from_qt.json)
- [web_import_from_qt_diff.json](<repo-root>/web_prototype/web_import_from_qt_diff.json)
- [web_import_from_qt_log.txt](<repo-root>/web_prototype/web_import_from_qt_log.txt)

## 7. 版本说明

### 7.1 Web 版本
- v1-candidate（独立应用候选版）
- 统一 UI 模式 v1 稳定
- Playwright regression 稳定
- LaTeX 闭环依赖 bridge

### 7.2 里程碑
Web 已经是独立应用候选版，统一 UI 模式 v1 稳定，Playwright regression 稳定，LaTeX 闭环已支持“Qt tex → Web 导回”的跨端路径（依赖 bridge）。