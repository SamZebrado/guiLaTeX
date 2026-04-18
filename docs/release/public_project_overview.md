# guiLaTeX 总装版公开总览

**编制**：外务大臣
**日期**：2026-04-13
**阶段**：v1-candidate / 第一阶段收官区

---

## 1. 项目一句话简介

guiLaTeX 是一个可视化 LaTeX 编辑器，支持 PDF 元素级编辑，通过 Export IR 中间层实现 LaTeX 代码生成，提供 Web 浏览器端和 Qt 桌面端双端原型。

## 2. 当前阶段

**v1-candidate — 第一阶段收官区**

项目已进入阶段性收官状态：Web 端和 Qt 端各自完成了核心功能的验证，Core 导出内核已稳定，跨端 roundtrip 路径已跑通。当前工作重心是展示、发布和剩余小缺口收尾。

**这不是最终完整版。**

## 3. Web 当前状态

Web 已经是**独立应用候选版**。

| 维度 | 状态 |
|------|------|
| UI 模式 | 统一 UI 模式 v1 稳定 |
| 回归测试 | Playwright regression 稳定 |
| LaTeX 闭环 | 已支持跨端路径（Qt tex → Web 导回），依赖 Python bridge |
| PDF 导出 | 浏览器打印路径（非原生导出） |

**已浏览器级验证**：UI 布局、文本元素 CRUD、多选与旋转、图层管理、IR/JSON 导出、PDF 导出（浏览器打印）、项目保存/打开（JSON）、复制粘贴、点击瞬移修复

**仅 Bridge/脚本层验证**：LaTeX 导出、LaTeX 导入、跨端导回（Qt tex → Web）

**Blocked**：浏览器内原生 LaTeX 处理、部分高级字段（颜色、对齐等）、直接打开 .tex 文件

## 4. Qt 当前状态

Qt 已完成 **v1-candidate canonical pack 整理**。

| 维度 | 状态 |
|------|------|
| 主闭环 | 已跑通（Qt → Core → tex → Core → Qt） |
| 核心功能 | 元素选择、属性编辑、旋转、复制/粘贴、导出/导入 conforming LaTeX |
| 证据链 | canonical pack 全套 JSON/tex 文件 |
| Core 集成 | 已集成，有已知 gap |

**已桌面级验证**：元素选择与属性编辑、旋转、复制/粘贴、导出 conforming LaTeX、导入 conforming LaTeX、roundtrip 主闭环、IR 元数据、Core 集成、UI 布局、属性面板滚动

**Core gap**：font_family_zh 硬编码为 SimSun、font_family_en 硬编码为 Times New Roman（Core 层 normalize 问题，非 Qt 层问题）

**Blocked**：PDF 主路径（非 Core→tex→编译）、保存项目、打开项目、变换菜单功能

## 5. Core 当前状态

Core 导出内核**已封板**。

| 维度 | 状态 |
|------|------|
| IR Schema | 已定义，JSON 格式 |
| LaTeX 导出 | export_ir_to_latex 已实现 |
| 回归样本 | golden sample + 3 个 regression sample |
| 跨端支持 | Qt 和 Web 均可接入 |
| 已知限制 | font_family 映射硬编码（影响中文字体保真度） |

## 6. 当前最适合公开展示的能力

1. **Web 端独立编辑体验**：纯浏览器打开，零依赖，文本 CRUD、多选旋转、图层管理
2. **IR/JSON 导出**：Web 和 Qt 均支持，可查看结构化文档模型
3. **LaTeX roundtrip**：Qt 端完整 roundtrip（导出 → 重新导入 → 差异对比）
4. **跨端导回**：Qt 导出的 conforming tex 可通过 bridge 导入 Web
5. **Playwright 自动化回归**：Web 端有稳定的自动化测试证据链
6. **Canonical Pack 证据链**：Qt 端 5 个 JSON/tex 文件构成完整 roundtrip 证据

## 7. 当前最不适合说满的能力

1. ❌ "浏览器内原生支持 LaTeX 导入/导出" — 实际依赖 Python bridge
2. ❌ "PDF 导出走 Core→tex→编译路径" — Qt 端 PDF 导出 blocked
3. ❌ "字体选择完全保真" — Core gap，中文字体硬编码
4. ❌ "保存/打开项目已实现" — Qt 端 blocked
5. ❌ "所有字段完全保住" — 部分高级字段（颜色、对齐）未支持
6. ❌ "UI 是最终版" — 两端 UI 均为 v1-candidate
7. ❌ "所有功能都已实现" — 两端均有 blocked 项

## 8. 对外统一口径

| 能力 | Web | Qt | Core |
|------|-----|-----|------|
| 已浏览器级验证 | ✅ | — | — |
| 已桌面级验证 | — | ✅ | — |
| 已脚本/bridge 级验证 | LaTeX 导出/导入/跨端 | — | — |
| Blocked | 原生 LaTeX、高级字段 | PDF 主路径、保存/打开 | font_family 映射 |
