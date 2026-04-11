# 共享导出内核设计文档

## 1. 概述

本设计文档定义了 guiLaTeX 项目的共享导出内核，旨在为 Web JSON 和 Qt model 提供一个统一的导出中间表示（Export IR），并通过同一个 exporter 生成 LaTeX。

## 2. Export IR 定义

### 2.1 核心字段

| 字段名 | 类型 | 描述 | 必需 |
|-------|------|------|------|
| id | string | 元素唯一标识符 | 是 |
| type | string | 元素类型（title / author / paragraph / textbox / equation / image） | 是 |
| content | string | 元素内容 | 是 |
| page | number | 元素所在页码（从1开始） | 是 |
| x | number | x 坐标 | 是 |
| y | number | y 坐标 | 是 |
| width | number | 宽度 | 是 |
| height | number | 高度 | 是 |
| rotation | number | 旋转角度（度） | 是 |
| layer | number | 层级（数值越大，层级越高） | 是 |
| font_family_zh | string | 中文字体 | 否 |
| font_family_en | string | 英文字体 | 否 |
| font_size | number | 字体大小（pt） | 否 |
| color | string | 颜色（HEX 格式） | 否 |
| alignment | string | 对齐方式（left / center / right） | 否 |
| visible | boolean | 是否可见 | 是 |

### 2.2 坐标系统

- **原点**：页面左上角
- **单位**：毫米（mm）
- **页面宽高**：A4 纸张默认尺寸（210mm × 297mm）
- **rotation 正方向**：顺时针
- **layer 排序规则**：数值越大，层级越高，渲染时会覆盖在数值较小的元素之上

## 3. 映射规范

### 3.1 Web JSON -> IR 映射

Web 前端需要将其 JSON 模型映射到 Export IR 格式。具体映射规则：

1. 提取 Web 模型中的元素属性
2. 按照 Export IR 字段进行转换
3. 确保坐标系统转换正确（如果 Web 前端使用不同的单位或坐标系统）

### 3.2 Qt model -> IR 映射

Qt 模型需要将其内部表示映射到 Export IR 格式。具体映射规则：

1. 提取 Qt 模型中的元素属性
2. 按照 Export IR 字段进行转换
3. 确保坐标系统转换正确（如果 Qt 模型使用不同的单位或坐标系统）

## 4. LaTeX 导出器设计

### 4.1 导出结构

生成的 LaTeX 文件至少分为以下几个部分：

1. **Preamble / 宏包区**：包含必要的宏包和设置
2. **Metadata / 注释区**：包含导出信息和元数据
3. **Optional semantic summary 区**：可选的语义摘要
4. **Absolute positioned objects 区**：主区，包含所有绝对定位的对象

### 4.2 支持的对象类型

第一版导出器支持以下 5 类对象：

1. **title**：标题
2. **author**：作者
3. **paragraph**：段落
4. **equation**：公式
5. **image**：图片

### 4.3 实现策略

- 优先保证几何位置、尺寸、旋转、层级和基本字体/字号/颜色
- 对 paragraph / textbox 不强行做"文档流还原"
- 允许使用绝对定位导出
- 定位命令集中放在单独 section / block 中，维持可读性

## 5. 示例

### 5.1 示例 IR

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
    },
    {
      "id": "author-1",
      "type": "author",
      "content": "张三",
      "page": 1,
      "x": 95,
      "y": 55,
      "width": 20,
      "height": 10,
      "rotation": 0,
      "layer": 9,
      "font_family_zh": "SimSun",
      "font_family_en": "Times New Roman",
      "font_size": 12,
      "color": "#000000",
      "alignment": "center",
      "visible": true
    },
    {
      "id": "paragraph-1",
      "type": "paragraph",
      "content": "这是一段示例文本。",
      "page": 1,
      "x": 30,
      "y": 80,
      "width": 150,
      "height": 30,
      "rotation": 0,
      "layer": 8,
      "font_family_zh": "SimSun",
      "font_family_en": "Times New Roman",
      "font_size": 12,
      "color": "#000000",
      "alignment": "left",
      "visible": true
    },
    {
      "id": "equation-1",
      "type": "equation",
      "content": "E = mc^2",
      "page": 1,
      "x": 80,
      "y": 120,
      "width": 50,
      "height": 20,
      "rotation": 0,
      "layer": 7,
      "font_family_zh": "SimSun",
      "font_family_en": "Times New Roman",
      "font_size": 14,
      "color": "#000000",
      "alignment": "center",
      "visible": true
    },
    {
      "id": "image-1",
      "type": "image",
      "content": "example.jpg",
      "page": 1,
      "x": 60,
      "y": 150,
      "width": 90,
      "height": 60,
      "rotation": 0,
      "layer": 6,
      "visible": true
    }
  ]
}
```

### 5.2 生成的 LaTeX

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
% Export date: YYYY-MM-DD HH:MM:SS
% Page size: A4 (210mm × 297mm)

% Optional semantic summary 区
% Title: 示例文档
% Author: 张三

% Absolute positioned objects 区
\begin{tikzpicture}[remember picture, overlay]
  % Layer 10: title-1
  \node[anchor=north west, rotate=0, text width=110mm, align=center, font=\fontsize{24}{28}\selectfont, color=black, visible on layer=10]
    at (50mm, 297mm-30mm) {示例文档};
  
  % Layer 9: author-1
  \node[anchor=north west, rotate=0, text width=20mm, align=center, font=\fontsize{12}{14}\selectfont, color=black, visible on layer=9]
    at (95mm, 297mm-55mm) {张三};
  
  % Layer 8: paragraph-1
  \node[anchor=north west, rotate=0, text width=150mm, align=left, font=\fontsize{12}{14}\selectfont, color=black, visible on layer=8]
    at (30mm, 297mm-80mm) {这是一段示例文本。};
  
  % Layer 7: equation-1
  \node[anchor=north west, rotate=0, text width=50mm, align=center, font=\fontsize{14}{16}\selectfont, color=black, visible on layer=7]
    at (80mm, 297mm-120mm) {$E = mc^2$};
  
  % Layer 6: image-1
  \node[anchor=north west, rotate=0, visible on layer=6]
    at (60mm, 297mm-150mm) {
      \includegraphics[width=90mm, height=60mm]{example.jpg}
    };
\end{tikzpicture}

\end{document}
```

## 6. 几何关系保证

### 6.1 当前能保证的几何关系

- 元素的位置（x, y）
- 元素的尺寸（width, height）
- 元素的旋转角度（rotation）
- 元素的层级关系（layer）
- 基本字体属性（font_family, font_size）
- 颜色（color）
- 对齐方式（alignment）

### 6.2 暂时不能保证的几何关系

- 复杂的文本布局和换行
- 精确的行间距和字间距
- 某些特殊字体效果
- 复杂的公式排版
- 图片的精确缩放和裁剪

## 7. 字段映射契约

### 7.1 Web 当前模型 -> Export IR 映射表

| Web 字段 | Export IR 字段 | 转换规则 | 缺失/默认值 |
|---------|---------------|---------|-------------|
| id | id | 直接映射 | 无 |
| type | type | 直接映射（textbox -> textbox, image -> image） | 无 |
| text/content | content | 直接映射 | 空字符串 |
| x | x | 直接映射（单位：mm） | 0 |
| y | y | 直接映射（单位：mm） | 0 |
| width | width | 直接映射（单位：mm） | 0 |
| height | height | 直接映射（单位：mm） | 0 |
| rotation | rotation | 直接映射（度） | 0 |
| layerId | layer | 直接映射 | 0 |
| fontFamily | font_family_zh / font_family_en | 根据字体名称判断语言 | SimSun / Times New Roman |
| fontSize | font_size | 直接映射（pt） | 12 |
| color | color | 直接映射（HEX） | #000000 |
| textAlign | alignment | left/center/right 映射 | left |
| visible | visible | 直接映射 | true |
| page | page | 固定为 1（Web 暂不支持多页） | 1 |

### 7.2 Qt 当前模型 -> Export IR 映射表

| Qt 字段 | Export IR 字段 | 转换规则 | 缺失/默认值 |
|--------|---------------|---------|-------------|
| id | id | 直接映射 | 无 |
| type | type | 映射规则：标题 -> title, 作者 -> author, 文本 -> paragraph, 公式 -> equation, 图片 -> image | 无 |
| text/content | content | 直接映射 | 空字符串 |
| x | x | 直接映射（单位：mm） | 0 |
| y | y | 直接映射（单位：mm） | 0 |
| width | width | 直接映射（单位：mm） | 0 |
| height | height | 直接映射（单位：mm） | 0 |
| rotation | rotation | 直接映射（度） | 0 |
| layer | layer | 直接映射 | 0 |
| font_family | font_family_zh / font_family_en | 根据字体名称判断语言 | SimSun / Times New Roman |
| font_size | font_size | 直接映射（pt） | 12 |
| color | color | 转换为 HEX 格式 | #000000 |
| alignment | alignment | left/center/right 映射 | left |
| visible | visible | 直接映射 | true |
| page | page | 直接映射 | 1 |

## 8. 几何保真声明（细化）

### 8.1 位置保真

- **描述**：元素左上角位置（x, y）
- **承诺精度**：误差 < 1mm
- **实现方式**：直接使用 IR 中的 x, y 坐标，单位为 mm，转换为 LaTeX 的绝对坐标系统
- **注意事项**：LaTeX 坐标原点在左下角，IR 坐标原点在左上角，需要转换为已正确转换
- **当前状态**：✅ 完全实现并验证

### 8.2 尺寸保真

- **描述**：元素宽度和高度（width, height）
- **承诺精度**：误差 < 1mm
- **实现方式**：直接使用 IR 中的 width, height，单位为 mm
- **当前状态**：✅ 完全实现并验证

### 8.3 旋转保真

- **描述**：元素旋转角度（rotation）
- **承诺精度**：误差 < 1度
- **实现方式**：直接使用 IR 中的 rotation，单位为度，正方向为顺时针
- **当前状态**：✅ 完全实现并验证

### 8.4 图层顺序保真

- **描述**：元素层叠顺序（layer）
- **承诺精度**：完全保真
- **实现方式**：按 layer 值升序渲染，数值越大层级越高，越在上面
- **当前状态**：✅ 完全实现并验证

### 8.5 文本框与文本内容的关系

- **描述**：文本在文本框内的布局
- **当前状态**：⚠️ 部分实现
- **已知问题**：
  - 文本换行可能与原设计有差异
  - 行间距和字间距由 LaTeX 自动控制
  - 文本超出文本框时不会自动裁剪

### 8.6 字体 fallback 后的差异风险

- **描述**：指定字体不可用时的 fallback 行为
- **当前状态**：⚠️ 需要注意
- **风险**：
  - 字体 fallback 后可能导致文本尺寸变化
  - 不同字体的字符宽度不同，可能影响整体布局
  - 建议**：尽量使用跨平台通用字体

## 9. 接入缺口表

| IR 字段 | Web 当前是否已具备 | Qt 当前是否已具备 | 若未具备，最小补齐动作是什么
|---------|-----------------|----------------|------------------------
| id | ✅ 是 | ✅ 是 | 无
| type | ✅ 是 | ✅ 是 | 无
| content | ✅ 是 | ✅ 是 | 无
| page | ⚠️ 固定为 1 | ✅ 是 | Web：需要在 Web 模型中添加 page 字段，当前固定为 1
| x | ✅ 是 | ✅ 是 | 无
| y | ✅ 是 | ✅ 是 | 无
| width | ✅ 是 | ✅ 是 | 无
| height | ✅ 是 | ✅ 是 | 无
| rotation | ✅ 是 | ✅ 是 | 无
| layer | ✅ 是 | ✅ 是 | 无
| font_family_zh | ⚠️ 部分 | ⚠️ 部分 | Web：需要区分中英文分离，默认SimSun
| font_family_en | ⚠️ 部分 | ⚠️ 部分 | Web：需要区分中英文分离，默认Times New Roman
| font_size | ✅ 是 | ✅ 是 | 无
| color | ✅ 是 | ✅ 是 | 无
| alignment | ✅ 是 | ✅ 是 | 无
| visible | ✅ 是 | ✅ 是 | 无

### 9.1 Web 端最小补齐动作

1. **page 字段：在 Web 模型中添加 page 字段，当前固定为 1
2. **font_family_zh / font_family_en**：将现有 fontFamily 字段拆分为中英文分离的两个字段
3. **确保所有字段都正确传递给 normalize_web_model_to_ir 函数能正确处理

### 9.2 Qt 端最小补齐动作

1. **font_family_zh / font_family_en**：将现有 font_family 字段拆分为中英文分离的两个字段
2. **确保所有字段都正确传递给 normalize_qt_model_to_ir 函数能正确处理

## 10. 接入 API

### 10.1 Web 接入函数

```python
from export_core import normalize_web_model_to_ir, export_ir_to_latex

# 1. 准备 Web 模型标准化为 IR
ir_data = normalize_web_model_to_ir(web_model)

# 2. 导出 IR 为 LaTeX
latex_content = export_ir_to_latex(ir_data)

# 3. 保存或显示 LaTeX
```

### 10.2 Qt 接入函数

```python
from export_core import normalize_qt_model_to_ir, export_ir_to_latex

# 1. 准备 Qt 模型标准化为 IR
ir_data = normalize_qt_model_to_ir(qt_model)

# 2. 导出 IR 为 LaTeX
latex_content = export_ir_to_latex(ir_data)

# 3. 保存或显示 LaTeX
```

### 10.3 直接导出 IR 为 LaTeX

```python
from export_core import export_ir_to_latex

# 如果你已经有标准 IR 数据
latex_content = export_ir_to_latex(ir_data)
```

## 11. 差异原因分析

### 11.1 LaTeX backend 本身导致

- LaTeX 的文本布局算法与 GUI 不同
- LaTeX 的字体渲染机制与 GUI 不同
- LaTeX 的页面处理方式与 GUI 不同

### 11.2 当前 exporter 尚未实现

- 复杂文本布局算法
- 高级字体效果支持
- 复杂公式排版优化
- 图片精确处理

## 12. 实现路径

- `export_core/`：导出内核目录
- `export_core/ir_schema.py`：IR schema 定义
- `export_core/latex_exporter.py`：LaTeX 导出器实现
- `export_core/__init__.py`：导出 API 入口
- `export_core/samples/`：样例文件目录