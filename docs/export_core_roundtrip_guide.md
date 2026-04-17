# ExportCore Roundtrip 接入指南

## 概述

本文档为 Web 和 Qt 提供 ExportCore roundtrip 功能的工程化接入说明。

## 接入准备

### 1. 安装依赖

确保项目中包含 ExportCore 模块：

```bash
# 确保 export_core 目录在 Python 路径中
```

### 2. 导入必要的函数

```python
from export_core import (
    export_ir_to_latex,
    import_own_exported_tex_to_ir,
    validate_tex_profile,
    validate_ir_roundtripability
)
```

## Web 接入指南

### 1. 导出流程

```python
# 1. 从 Web 模型转换为 IR
from export_core import normalize_web_model_to_ir

web_model = {
    "elements": [
        # Web 元素数据
    ]
}

ir_data = normalize_web_model_to_ir(web_model)

# 2. 验证 IR
validation_result = validate_ir_roundtripability(ir_data)
if not validation_result["ok"]:
    # 处理验证失败
    print(f"IR 验证失败: {validation_result['message']}")
    # 采取相应措施

# 3. 导出为 LaTeX
latex_content = export_ir_to_latex(ir_data)

# 4. 保存或返回 LaTeX 内容
with open("exported_document.tex", "w", encoding="utf-8") as f:
    f.write(latex_content)
```

### 2. 导回流程

```python
# 1. 读取 LaTeX 文件
with open("exported_document.tex", "r", encoding="utf-8") as f:
    latex_content = f.read()

# 2. 验证 LaTeX 符合规范
profile_validation = validate_tex_profile(latex_content)
if not profile_validation["ok"]:
    # 处理不符合规范的情况
    print(f"LaTeX 不符合规范: {profile_validation['message']}")
    # 采取相应措施

# 3. 导回为 IR
imported_ir = import_own_exported_tex_to_ir(latex_content)

# 4. 使用导回的 IR 数据
# 例如：更新 Web 模型
```

## Qt 接入指南

### 1. 导出流程

```python
# 1. 从 Qt 模型转换为 IR
from export_core import normalize_qt_model_to_ir

qt_model = {
    "elements": [
        # Qt 元素数据
    ]
}

ir_data = normalize_qt_model_to_ir(qt_model)

# 2. 验证 IR
validation_result = validate_ir_roundtripability(ir_data)
if not validation_result["ok"]:
    # 处理验证失败
    print(f"IR 验证失败: {validation_result['message']}")
    # 采取相应措施

# 3. 导出为 LaTeX
latex_content = export_ir_to_latex(ir_data)

# 4. 保存或返回 LaTeX 内容
with open("exported_document.tex", "w", encoding="utf-8") as f:
    f.write(latex_content)
```

### 2. 导回流程

```python
# 1. 读取 LaTeX 文件
with open("exported_document.tex", "r", encoding="utf-8") as f:
    latex_content = f.read()

# 2. 验证 LaTeX 符合规范
profile_validation = validate_tex_profile(latex_content)
if not profile_validation["ok"]:
    # 处理不符合规范的情况
    print(f"LaTeX 不符合规范: {profile_validation['message']}")
    # 采取相应措施

# 3. 导回为 IR
imported_ir = import_own_exported_tex_to_ir(latex_content)

# 4. 使用导回的 IR 数据
# 例如：更新 Qt 模型
```

## 最小 Smoke Test

### 测试代码

```python
# test_roundtrip_smoke.py
from export_core import (
    export_ir_to_latex,
    import_own_exported_tex_to_ir,
    validate_tex_profile
)

# 最小测试 IR
minimal_ir = {
    "elements": [
        {
            "id": "test-1",
            "type": "paragraph",
            "content": "Test",
            "page": 1,
            "x": 0,
            "y": 0,
            "width": 100,
            "height": 20,
            "rotation": 0,
            "layer": 0,
            "visible": True
        }
    ]
}

# 测试导出
try:
    latex = export_ir_to_latex(minimal_ir)
    print("✓ 导出成功")
    
    # 测试验证
    validation = validate_tex_profile(latex)
    if validation["ok"]:
        print("✓ LaTeX 符合规范")
    else:
        print(f"✗ LaTeX 不符合规范: {validation['issues']}")
    
    # 测试导回
    imported = import_own_exported_tex_to_ir(latex)
    print("✓ 导回成功")
    
    # 验证导回结果
    if imported["elements"][0]["id"] == "test-1":
        print("✓ 导回数据正确")
    else:
        print("✗ 导回数据错误")
        
except Exception as e:
    print(f"✗ 测试失败: {str(e)}")
```

### 运行测试

```bash
python test_roundtrip_smoke.py
```

## 输入输出示例

### 输入 IR

```json
{
  "elements": [
    {
      "id": "title-1",
      "type": "title",
      "content": "示例文档",
      "page": 1,
      "x": 50,
      "y": 30,
      "width": 110,
      "height": 20,
      "rotation": 0,
      "layer": 10,
      "font_family_zh": "SimSun",
      "font_family_en": "Times New Roman",
      "font_size": 24,
      "color": "#000000",
      "alignment": "center",
      "visible": true
    }
  ]
}
```

### 输出 LaTeX

```latex
% Preamble / 宏包区
\documentclass{article}
\usepackage[margin=0mm]{geometry}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{amsmath}

\begin{document}

% Metadata / 注释区
% Exported by guiLaTeX ExportCore
% Export date: 2026-04-17 12:00:00
% Page size: A4 (210mm × 297mm)
% IR Metadata for roundtrip:
% BEGIN_IR_METADATA
% {
%   "export_date": "2026-04-17 12:00:00",
%   "page_size": "A4 (210mm × 297mm)",
%   "exporter": "guiLaTeX ExportCore",
%   "version": "1.0",
%   "ir": {
%     "elements": [
%       {
%         "id": "title-1",
%         "type": "title",
%         "content": "示例文档",
%         "page": 1,
%         "x": 50,
%         "y": 30,
%         "width": 110,
%         "height": 20,
%         "rotation": 0,
%         "layer": 10,
%         "font_family_zh": "SimSun",
%         "font_family_en": "Times New Roman",
%         "font_size": 24,
%         "color": "#000000",
%         "alignment": "center",
%         "visible": true
%       }
%     ]
%   }
% }
% END_IR_METADATA

% Optional semantic summary 区
% Title: 示例文档

% Absolute positioned objects 区
\begin{tikzpicture}[remember picture, overlay]
  % Layer 10: title-1
  \node[anchor=north west, rotate=0, text width=110mm, align=center, font=\fontsize{24}{28.8}\selectfont, color={rgb,1:red,0;green,0;blue,0}, visible on layer=10]
    at (50mm, 267mm) {示例文档};
\end{tikzpicture}

\end{document}
```

### 再导回 IR

```json
{
  "elements": [
    {
      "id": "title-1",
      "type": "title",
      "content": "示例文档",
      "page": 1,
      "x": 50,
      "y": 30,
      "width": 110,
      "height": 20,
      "rotation": 0,
      "layer": 10,
      "font_family_zh": "SimSun",
      "font_family_en": "Times New Roman",
      "font_size": 24,
      "color": "#000000",
      "alignment": "center",
      "visible": true
    }
  ]
}
```

## 注意事项

1. **只支持自家导出的 LaTeX**：不要尝试导回非 guiLaTeX 导出的 LaTeX
2. **保持 LaTeX 结构完整**：不要手动修改导出的 LaTeX，可能导致导回失败
3. **验证是必要步骤**：在导出和导回前都应该进行验证
4. **错误处理**：实现时应添加适当的错误处理
5. **性能考虑**：对于大型文档，可能需要考虑性能优化

## 故障排除

### 常见问题

1. **导回失败**：检查 LaTeX 文件是否完整，特别是 IR 元数据部分
2. **验证失败**：确保 IR 数据符合规范，所有必需字段都存在
3. **字段丢失**：检查 IR 数据是否包含所有必要字段

### 调试方法

1. 使用 `validate_ir_roundtripability()` 检查 IR 数据
2. 使用 `validate_tex_profile()` 检查 LaTeX 文件
3. 检查导出的 LaTeX 文件中的 IR 元数据是否正确嵌入