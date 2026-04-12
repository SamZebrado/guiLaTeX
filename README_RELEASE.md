# guiLaTeX

> 🏆 本项目为 [TRAE 创意编程大赛](https://forum.trae.cn/t/topic/7939/12) 参赛作品，目前仍在活跃开发中。
> 如果你觉得这个项目有意思，欢迎去[论坛帖子](https://forum.trae.cn/t/topic/7939/12)投票加油！❤️
>
> 🏆 This project is a submission for the [TRAE Creative Coding Contest](https://forum.trae.cn/t/topic/7939/12) and is still under active development.
> If you find this project interesting, please visit the [forum post](https://forum.trae.cn/t/topic/7939/12) to vote and cheer us on! ❤️

## 关于本项目 / About

guiLaTeX 是一个可视化 LaTeX 编辑器，支持 PDF 文档的加载、元素级编辑和 LaTeX 代码导出。

guiLaTeX is a visual LaTeX editor that supports PDF document loading, element-level editing, and LaTeX code export.

项目采用 Python + PyQt6 构建 GUI，使用 PyMuPDF 进行 PDF 渲染，并通过 Export IR 中间层实现 LaTeX 代码生成。

Built with Python + PyQt6 for the GUI, PyMuPDF for PDF rendering, and an Export IR intermediate layer for LaTeX code generation.

## 界面预览 / Screenshots

### Qt 桌面端 / Qt Desktop

![Qt Desktop Screenshot](assets/qt_screenshot.png)

基于 PyQt6 的桌面应用，支持 PDF 可视化编辑、属性面板、LaTeX 源码预览。

A PyQt6 desktop application supporting visual PDF editing, property panels, and LaTeX source preview.

### Web 端原型 / Web Prototype

![Web Prototype Screenshot](assets/web_screenshot.png)

基于 HTML/JS 的浏览器端原型，支持元素拖拽、多选旋转、IR 导出。

An HTML/JS browser prototype supporting element dragging, multi-select rotation, and IR export.

## 项目结构 / Project Structure

- **核心源代码 / Core source**: `src/`（GUI、LaTeX 引擎、数据模型 / GUI, LaTeX engine, data model）
- **导出核心 / Export core**: `export_core/`（IR Schema、LaTeX 导出器、回归测试样本 / IR Schema, LaTeX exporter, regression samples）
- **测试套件 / Test suite**: `tests/`（模型层测试、集成测试、smoke test）
- **Web 原型 / Web prototype**: `web_prototype/`（浏览器端 PDF 编辑原型 / Browser-based PDF editing prototype）
- **技术文档 / Documentation**: `docs/`（架构设计、API 文档、用户指南 / Architecture, API docs, user guide）
- **开发经验 / Dev experience**: 多 Agent 协作经验、审计记录、教训总结 / Multi-agent collaboration lessons, audit records

## 技术栈 / Tech Stack

- Python 3.10+
- PyQt6 — GUI 框架 / GUI framework
- PyMuPDF (fitz) — PDF 渲染 / PDF rendering
- LaTeX — 文档编译 / Document compilation
- Playwright — Web 端自动化测试 / Web automation testing

## 许可 / License

[Apache License 2.0](LICENSE)
