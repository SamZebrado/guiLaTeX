# Qt 对外口径摘要

日期：2026-04-18

## 已验证

### 核心功能
- **元素选择与属性编辑**：支持选择元素并在右侧属性面板编辑属性
- **旋转功能**：支持对元素进行任意角度的旋转
- **复制/粘贴功能**：支持元素复制，自动生成新 ID 并偏移位置
- **导出 LaTeX**：成功生成 conforming LaTeX 文件，包含 IR 元数据
- **导入 LaTeX**：成功从 conforming LaTeX 文件导回元素

### 技术实现
- **roundtrip 主闭环**：Qt -> Core -> tex -> Core -> Qt 流程已跑通
- **IR 元数据**：导出的 LaTeX 文件包含完整的 IR 元数据
- **Core 集成**：正确调用 normalize_qt_model_to_ir 和 export_ir_to_latex
- **UI 布局**：左侧画布 + 右侧属性面板，布局稳定
- **属性面板滚动**：支持鼠标滚轮滚动

## Core gap

### 已知问题
- **font_family_zh**：normalize_qt_model_to_ir 中硬编码为 'SimSun'，忽略 Qt 模型值
- **font_family_en**：normalize_qt_model_to_ir 中硬编码为 'Times New Roman'，忽略 Qt 模型值

### 原因说明
这些问题出现在 Core 层的映射逻辑中，不是 Qt 层的问题。

## Blocked

### 未实现功能
- **PDF 主路径**：PDF 导出不是通过 Core->tex->编译路径，而是直接复制现有 PDF
- **保存项目**：保存项目功能未实现
- **打开项目**：打开项目功能未实现
- **变换菜单功能**：变换菜单下的具体功能仅添加了菜单项，功能尚未实现

## 最准确的一句话里程碑表述

**Qt 已完成 v1-candidate canonical pack 整理，主闭环已跑通，核心功能已验证，但仍存在 font_family 相关的 Core gap 和部分功能 blocked，已进入可交接、可对外说明的稳定状态。**

## 适合对外展示的功能

1. **元素选择与属性编辑**：展示基本的编辑能力
2. **旋转功能**：展示 45 度旋转效果
3. **复制/粘贴功能**：展示生成新 ID 和偏移
4. **导出 LaTeX 功能**：展示完整的导出流程
5. **导入 LaTeX 功能**：展示从 conforming tex 导回的能力

## 不该说满的地方

- 不要说 PDF 导出是通过 Core->tex->编译路径
- 不要说字体选择完全保住
- 不要说打开/保存项目已实现
- 不要说所有字段都完全保住
- 不要说 UI 是最终版
- 不要说所有功能都已实现

## 技术细节

- **导出使用**：normalize_qt_model_to_ir + export_ir_to_latex
- **导入使用**：import_own_exported_tex_to_ir
- **IR 元数据**：包含 BEGIN_IR_METADATA 和 END_IR_METADATA
- **Canonical Pack**：所有验证材料固定在 docs/contest_evidence/qt_canonical_pack/ 目录
