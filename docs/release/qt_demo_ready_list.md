# Qt 演示准备清单

日期：2026-04-18

## 最适合录制的 Qt 功能

### 1. 元素选择与属性编辑
**功能说明**：选择元素后在右侧属性面板编辑属性
**对应证据文件**：
- [qt_canonical_source_model.json](docs/contest_evidence/qt_canonical_pack/qt_canonical_source_model.json)
- [properties.py](src/gui/properties.py)

**建议录制方式**：
1. 启动 Qt 应用
2. 点击画布上的元素
3. 在右侧属性面板修改文本内容
4. 修改字体大小
5. 观察属性实时更新

**不该说满的地方**：
- 不要说所有属性都已实现
- 不要说属性面板是最终版

### 2. 旋转功能
**功能说明**：对元素进行旋转操作
**对应证据文件**：
- [qt_canonical_source_model.json](docs/contest_evidence/qt_canonical_pack/qt_canonical_source_model.json)
- [qt_canonical_exported.tex](docs/contest_evidence/qt_canonical_pack/qt_canonical_exported.tex)

**建议录制方式**：
1. 选择一个元素
2. 在属性面板修改旋转角度为 45 度
3. 观察元素旋转效果
4. 导出为 LaTeX 并展示旋转效果

**不该说满的地方**：
- 不要说旋转支持任意角度
- 不要说旋转是完美无误差的

### 3. 复制/粘贴功能
**功能说明**：复制元素并生成新 ID 和偏移
**对应证据文件**：
- [qt_canonical_source_model.json](docs/contest_evidence/qt_canonical_pack/qt_canonical_source_model.json)

**建议录制方式**：
1. 选择一个元素
2. 使用编辑菜单的复制功能
3. 使用编辑菜单的粘贴功能
4. 观察新元素的位置偏移
5. 查看新元素的 ID

**不该说满的地方**：
- 不要说复制/粘贴支持复杂对象
- 不要说复制/粘贴速度很快

### 4. 导出 LaTeX 功能
**功能说明**：导出为 conforming LaTeX 文件
**对应证据文件**：
- [qt_canonical_exported.tex](docs/contest_evidence/qt_canonical_pack/qt_canonical_exported.tex)
- [qt_canonical_roundtrip_diff_report.json](docs/contest_evidence/qt_canonical_pack/qt_canonical_roundtrip_diff_report.json)

**建议录制方式**：
1. 点击文件菜单的"导出 LaTeX"
2. 选择保存位置
3. 打开生成的 .tex 文件
4. 展示文件包含 IR 元数据

**不该说满的地方**：
- 不要说导出的 LaTeX 支持所有复杂元素
- 不要说字体选择完全保住

### 5. 导入 LaTeX 功能
**功能说明**：导入 conforming LaTeX 文件
**对应证据文件**：
- [qt_canonical_imported_ir.json](docs/contest_evidence/qt_canonical_pack/qt_canonical_imported_ir.json)
- [qt_canonical_roundtrip_diff_report.json](docs/contest_evidence/qt_canonical_pack/qt_canonical_roundtrip_diff_report.json)

**建议录制方式**：
1. 点击文件菜单的"导入 LaTeX"
2. 选择之前导出的 .tex 文件
3. 观察元素被正确导入
4. 验证元素属性

**不该说满的地方**：
- 不要说导入支持任意 LaTeX 文件
- 不要说所有字段都完全保住

## 演示准备检查

### 环境准备
- 确保 PyQt6 环境正常
- 确保 ExportCore 模块可导入
- 准备一个干净的测试项目

### 证据文件准备
- 确保 [qt_canonical_pack](docs/contest_evidence/qt_canonical_pack/) 目录下所有文件都存在
- 确保 [qt_canonical_exported.tex](docs/contest_evidence/qt_canonical_pack/qt_canonical_exported.tex) 包含 IR 元数据
- 准备好截图和视频录制工具

### 演示流程
1. 展示 UI 布局（左侧画布 + 右侧属性面板）
2. 演示元素选择与属性编辑
3. 演示旋转功能
4. 演示复制/粘贴功能
5. 演示导出 LaTeX 功能
6. 演示导入 LaTeX 功能
7. 总结 Qt 当前状态
