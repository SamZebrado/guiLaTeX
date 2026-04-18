# Qt v1-candidate Canonical Pack 说明

## 材料列表
- qt_canonical_source_model.json：Canonical 源模型
- qt_canonical_normalized_ir.json：标准化后的 IR
- qt_canonical_exported.tex：导出的 conforming LaTeX 文件
- qt_canonical_imported_ir.json：导回的 IR
- qt_canonical_roundtrip_diff_report.json：Roundtrip 差异报告

## 验证指南
1. 使用 Web 端的导入 LaTeX 功能
2. 选择 qt_canonical_exported.tex 文件
3. 验证元素是否正确导入

## 最终口径

### 已验证
- **type**：Qt 'text' → IR 'paragraph'（映射策略）
- **layer**：完整保住
- **export_tex**：成功生成 conforming tex 并包含 IR 元数据
- **import_conforming_tex**：成功从 conforming tex 导回 IR

### Core gap
- **font_family_zh**：normalize_qt_model_to_ir 中硬编码为 'SimSun'
- **font_family_en**：normalize_qt_model_to_ir 中硬编码为 'Times New Roman'

### Blocked
- **pdf_main_path**：PDF 导出不是通过 Core->tex->编译路径
- **save_project**：保存项目功能未实现
- **open_project**：打开项目功能未实现

## 适合录制的功能
1. 元素选择与属性编辑
2. 旋转功能
3. 复制/粘贴功能
4. 导出 LaTeX 功能
5. 导入 LaTeX 功能

## 最不该说满的点
- 不要说 PDF 导出是通过 Core->tex->编译路径
- 不要说字体选择完全保住
- 不要说打开/保存项目已实现
- 不要说所有字段都完全保住

## 证据文件
- 截图：右侧属性面板滚动
- 截图：工具栏分组
- 视频：导出/导入 LaTeX 流程
- 视频：旋转功能

## 技术细节
- 导出使用：normalize_qt_model_to_ir + export_ir_to_latex
- 导入使用：import_own_exported_tex_to_ir
- IR 元数据：包含 BEGIN_IR_METADATA 和 END_IR_METADATA
