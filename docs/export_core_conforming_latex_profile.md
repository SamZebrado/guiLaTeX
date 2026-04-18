# Conforming LaTeX Profile v1

## 概述

本文档定义了 guiLaTeX ExportCore 支持的 **Conforming LaTeX Profile v1**，用于实现"自家导出的 LaTeX 可导回"的最小闭环协议。

## 目标

- **只支持本项目自己导出的 conforming tex**，不承诺任意第三方 tex
- 保证 Core 自己导出的 tex 能稳定导回 IR
- 为 Web / Qt 提供稳定的接入 contract

## Conforming LaTeX 的结构

### 1. 必需的结构

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
% IR Metadata for roundtrip:
% BEGIN_IR_METADATA
% {
%   "export_date": "YYYY-MM-DD HH:MM:SS",
%   "page_size": "A4 (210mm × 297mm)",
%   "exporter": "guiLaTeX ExportCore",
%   "version": "1.0",
%   "ir": {
%     "elements": [
%       ... 完整的 IR 数据 ...
%     ]
%   }
% }
% END_IR_METADATA

% Optional semantic summary 区
% Title: ...
% Author: ...

% Absolute positioned objects 区
\begin{tikzpicture}[remember picture, overlay]
  % 元素节点定义
  \node[anchor=north west, rotate=0, text width=100mm, font=\fontsize{12}{14.4}\selectfont, color={rgb,1:red,0;green,0;blue,0}, visible on layer=0]
    at (0mm, 297mm) {文本内容};
  % 更多元素...
\end{tikzpicture}

\end{document}
```

### 2. 元数据区

- **必须**包含 `% BEGIN_IR_METADATA` 和 `% END_IR_METADATA` 标记
- **必须**在标记之间嵌入完整的 IR 数据（JSON 格式）
- 每行 JSON 前必须加 `%` 前缀

### 3. 可导回的元素类型

- title
- author
- paragraph
- textbox
- equation
- image

## 支持的字段

### 必须保留的字段

- **id**: 元素唯一标识
- **type**: 元素类型（canonical 类型）
- **content**: 元素内容
- **page**: 页面编号
- **x**: X 坐标
- **y**: Y 坐标
- **width**: 宽度
- **height**: 高度
- **rotation**: 旋转角度
- **layer**: 图层
- **visible**: 可见性

### 可选字段

- **font_family_zh**: 中文字体
- **font_family_en**: 英文字体
- **font_size**: 字体大小
- **color**: 颜色（HEX 格式）
- **alignment**: 对齐方式（left/center/right）

## 不支持的内容

- 任意第三方 LaTeX 格式
- 非 guiLaTeX 导出的 LaTeX
- 手动修改的 LaTeX（可能导致导回失败）
- 不包含 IR 元数据的 LaTeX

## 第三方 Agent 指南

如果第三方 Agent 想生成"可导回"的 tex，必须：

1. **严格遵循**上述结构
2. **必须**在元数据区嵌入完整的 IR 数据
3. **必须**使用标准的 canonical 类型
4. **不要**修改元数据格式
5. **不要**移除必需的标记

## 验证方法

使用 ExportCore 提供的 `validate_tex_profile()` 函数验证 tex 是否符合规范。

## 导回流程

1. 使用 `extract_embedded_ir_from_tex()` 从 tex 中提取 IR 元数据
2. 使用 `validate_ir_roundtripability()` 验证提取的 IR
3. 使用 `import_own_exported_tex_to_ir()` 完成导回

## 版本管理

- **v1**: 初始版本，支持基本元素的 roundtrip