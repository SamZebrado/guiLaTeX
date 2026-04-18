# Qt 跨端验证材料说明

## 材料列表
- qt_to_web_conforming.tex：Qt 导出的 conforming LaTeX 文件
- qt_to_web_source_model.json：Qt 原始模型
- qt_to_web_expected_ir.json：标准化后的 IR

## Web 验证指南
1. 使用 Web 端的导入 LaTeX 功能
2. 选择 qt_to_web_conforming.tex 文件
3. 验证元素是否正确导入

## 必须保住的字段
- id
- content
- page
- x, y, width, height
- rotation
- visible
- font_size
- color
- alignment
- layer

## 当前允许差异的字段
- type：Qt 'text' → IR 'paragraph'（这是预期的映射策略）
- font_family_zh：当前 Core 硬编码为 'SimSun'（Core gap）
- font_family_en：当前 Core 硬编码为 'Times New Roman'（Core gap）

## Core gap 说明
- font_family_zh：normalize_qt_model_to_ir 中硬编码为 'SimSun'，忽略 Qt 模型值
- font_family_en：normalize_qt_model_to_ir 中硬编码为 'Times New Roman'，忽略 Qt 模型值

## 预期元素
1. 标题元素：id="test_title"
2. 段落元素：id="test_paragraph"
3. 公式元素：id="test_formula"

## 字段口径
| 字段 | Qt 原始值 | 预期 IR 值 | 说明 |
|------|-----------|------------|------|
| type | "text" | "paragraph" | 映射策略 |
| layer | 1/2/3 | 1/2/3 | 必须保住 |
| font_family_zh | "Noto Sans SC" | "SimSun" | Core gap |
| font_family_en | "Inter"/"Noto Sans" | "Times New Roman" | Core gap |
