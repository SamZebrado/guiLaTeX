# Qt PDFCanvas 崩溃定位报告

## 生成时间
2026-04-12 21:00:00

## 问题背景
- 在 clean venv 环境中，`QApplication([])` 已能正常创建
- Qt UI smoke 已至少部分通过
- `tests/test_qt_core_smoke.py::test_qt_to_core` 会在 `src/gui/pdf_canvas.py` line 1114 in __init__ 触发 Fatal Python error: Aborted

## 定位过程

### 1. 阅读 PDFCanvas.__init__ 代码
`PDFCanvas.__init__` 的初始化步骤如下：
1. 调用 `super().__init__(parent)`
2. 创建布局 `QVBoxLayout(self)`
3. 创建工具栏 `QHBoxLayout()`
4. 添加导航按钮（上一页、下一页、页码标签）
5. 添加缩放控件（放大、缩小）
6. 添加保存项目按钮
7. 添加导出 PDF 按钮
8. 添加导出模型 JSON 按钮
9. 添加 Z-order 按钮（移到顶部、移到底部、上移、下移）
10. 添加滚动区域 `QScrollArea()`
11. 初始化 PDF 文档相关变量
12. 初始化文档模型集成

### 2. 运行探针脚本

| 探针脚本 | 结果 | 说明 |
|---------|------|------|
| probe_import_pdf_canvas.py | ✅ 通过 | 成功导入 PDFCanvas 模块 |
| probe_instantiate_pdf_canvas.py | ❌ 崩溃 | 尝试实例化 PDFCanvas 时崩溃 |
| probe_pdf_canvas_stepwise.py | ❌ 崩溃 | 尝试逐步初始化时崩溃 |
| probe_qt_basic.py | ✅ 通过 | 成功导入基本 Qt 模块 |
| probe_qt_components.py | ❌ 崩溃 | 尝试导入多个 Qt 组件时崩溃 |
| probe_qt_components_stepwise.py | ❌ 崩溃 | 逐步导入 Qt 组件时崩溃 |
| probe_qapp_only.py | ❌ 崩溃 | 只创建 QApplication 时崩溃 |

### 3. 关键发现
- **PDFCanvas 导入成功**：`probe_import_pdf_canvas.py` 成功通过，说明 PDFCanvas 模块本身可以正常导入
- **基本 Qt 导入成功**：`probe_qt_basic.py` 成功通过，说明基本的 Qt 模块可以正常导入
- **QApplication 创建崩溃**：所有尝试创建 QApplication 的探针都崩溃了，说明问题出在 QApplication 创建阶段

## 崩溃原因分析

### 候选原因 1：QApplication 创建时的平台/插件问题
- 现象：在 clean venv 环境中，虽然可以导入 PyQt6，但创建 QApplication 时会崩溃
- 可能性：高
- 解释：QApplication 创建时会初始化 Qt 平台插件，可能在 headless 环境下存在兼容性问题

### 候选原因 2：PyQt6 版本与系统兼容性问题
- 现象：clean venv 中安装的 PyQt6 版本可能与系统环境不兼容
- 可能性：中
- 解释：不同版本的 PyQt6 在处理 headless 环境时可能有不同的行为

### 候选原因 3：环境变量配置问题
- 现象：缺少必要的环境变量配置导致 QApplication 创建失败
- 可能性：中
- 解释：Qt 需要某些环境变量来正确初始化平台插件

## 最后一条成功执行的初始化步骤
- 在 `probe_qt_components_stepwise.py` 中，最后一条成功执行的步骤是：
  ```
  Step 2: Import QApplication
  ✓ Step 2 passed
  ```
- 崩溃发生在尝试执行：
  ```
  Step 3: Create QApplication
  ```

## 结论
- 问题不是 PDFCanvas 内部的初始化步骤问题，而是 QApplication 创建本身的问题
- 在 clean venv 环境中，虽然可以导入 PyQt6 和基本的 Qt 模块，但尝试创建 QApplication 时会崩溃
- 这与之前在 Anaconda 环境中观察到的现象一致，说明这可能是一个更广泛的 Qt/headless 环境问题

## 建议后续步骤
1. 尝试设置不同的 `QT_QPA_PLATFORM` 环境变量值
2. 检查 PyQt6 版本与系统的兼容性
3. 尝试安装不同版本的 PyQt6
4. 检查系统是否缺少必要的 Qt 依赖
