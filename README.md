# guiLaTeX

**可视化 LaTeX 编辑器** — 支持 PDF 元素级编辑，通过 Export IR 中间层生成 LaTeX 代码。

> 🏆 [TRAE 创意编程大赛参赛作品](https://forum.trae.cn/t/topic/7939/12) · 欢迎投票加油 ❤️

---

## 界面预览

<table>
<tr>
<td width="50%">

### 🌐 Web 端（当前主展示线）

纯浏览器应用，零依赖，直接打开即用。

<br>

![Web 初始页面](assets/web_screenshot.png)

<br>

<!-- GIF 预留：Web 端操作演示 -->
<!-- ![Web Demo](assets/web_demo.gif) -->

</td>
<td width="50%">

### 🖥️ Qt 桌面端（原型阶段）

PyQt6 桌面应用，核心闭环已验证，但多项功能尚未收口。

<br>

![Qt 桌面端](assets/qt_screenshot.png)

<br>

<!-- GIF 预留：Qt 端操作演示 -->
<!-- ![Qt Demo](assets/qt_demo.gif) -->

</td>
</tr>
</table>

---

## 当前状态

> ⚠️ **这不是最终完整版。**

- 🌐 **Web — 当前主展示线**。独立应用候选版，浏览器级验证。文本 CRUD、多选旋转、图层管理、IR/PDF 导出均已验证。LaTeX 功能依赖 Python bridge。演示录屏由人工完成。
- 🖥️ **Qt — 原型阶段**。Roundtrip 闭环已跑通，但旋转仅能通过配置面板调节（无直接控件）、图层功能未在编辑界面中体现、导出 PDF 会闪退。不作为当前主完成判据。
- 📦 **Core — 支撑层**。IR Schema + LaTeX 导出器 + 回归样本齐备，是 Web 和 Qt 的共享导出内核。不是独立产品线。

---

## 快速体验

- 🌐 [Web 端在线体验](web_prototype/index.html) — 直接在浏览器中打开（推荐）
- 🎬 [录屏演示（B 站）](https://www.bilibili.com/video/BV1L7rzBzEDs/) — 完整操作演示
- 📜 [朝堂风云录 · 开发展示页](https://samzebrado.github.io/guiLaTeX/showcase/) — AI Agent 协作开发全记录
- 📋 [Demo 入口](https://samzebrado.github.io/guiLaTeX/showcase/demo_index.html) — 模块状态与演示导航

---

## 技术栈

Python 3.10+ · PyQt6 · PyMuPDF · HTML/CSS/JS · LaTeX · Playwright

## 许可

[Apache License 2.0](LICENSE)

---

<details>
<summary>📖 更多文档</summary>

**技术文档**

- [架构设计](docs/architecture.md) · [用户指南](docs/user-guide.md)
- [Export Core 设计](docs/export_core_design.md) · [快速上手](docs/export_core_quickstart.md)
- [Conforming LaTeX Profile](docs/export_core_conforming_latex_profile.md) · [Roundtrip 指南](docs/export_core_roundtrip_guide.md)

**发布材料**

- [公开总览](docs/release/public_project_overview.md) — 项目状态、证据层级、红线清单
- [演示资产索引](docs/release/demo_asset_index.md) · [总录制脚本](docs/release/demo_master_shot_list.md)

</details>

---

# English

## guiLaTeX

**A visual LaTeX editor** — supports element-level PDF editing and LaTeX code generation via Export IR.

> 🏆 [TRAE Creative Coding Contest Submission](https://forum.trae.cn/t/topic/7939/12) · Vote for us! ❤️

---

## Screenshots

<table>
<tr>
<td width="50%">

### 🌐 Web (Primary Demo)

A pure browser application, zero dependencies.

<br>

![Web Initial Page](assets/web_screenshot.png)

<br>

<!-- GIF placeholder: Web demo -->
<!-- ![Web Demo](assets/web_demo.gif) -->

</td>
<td width="50%">

### 🖥️ Qt Desktop (Prototype)

A PyQt6 desktop app, core loop validated but several features not yet finalized.

<br>

![Qt Desktop](assets/qt_screenshot.png)

<br>

<!-- GIF placeholder: Qt demo -->
<!-- ![Qt Demo](assets/qt_demo.gif) -->

</td>
</tr>
</table>

---

## Current Status

> ⚠️ **This is not the final version.**

- 🌐 **Web — Primary demo line.** Independent app candidate, browser-level verified. Text CRUD, multi-select rotation, layer management, IR/PDF export. LaTeX depends on Python bridge. Demo recordings done manually.
- 🖥️ **Qt — Prototype stage.** Roundtrip loop validated, but rotation only via config panel (no direct control), layer management not visible in editor, PDF export causes crash. Not a primary completion criterion.
- 📦 **Core — Support layer.** IR Schema + LaTeX exporter + regression samples. Shared export engine for Web and Qt. Not an independent product line.

---

## Quick Start

- 🌐 [Try Web App](web_prototype/index.html) — Open directly in your browser (recommended)
- 🎬 [Demo Recording (Bilibili)](https://www.bilibili.com/video/BV1L7rzBzEDs/) — Full operation demo
- 📜 [Court Chronicles · Showcase](https://samzebrado.github.io/guiLaTeX/showcase/) — AI agent dev journal
- 📋 [Demo Index](https://samzebrado.github.io/guiLaTeX/showcase/demo_index.html) — Module status & demo navigation

---

## Tech Stack

Python 3.10+ · PyQt6 · PyMuPDF · HTML/CSS/JS · LaTeX · Playwright

## License

[Apache License 2.0](LICENSE)

---

<details>
<summary>📖 More Documentation</summary>

**Technical Docs**

- [Architecture](docs/architecture.md) · [User Guide](docs/user-guide.md)
- [Export Core Design](docs/export_core_design.md) · [Quick Start](docs/export_core_quickstart.md)
- [Conforming LaTeX Profile](docs/export_core_conforming_latex_profile.md) · [Roundtrip Guide](docs/export_core_roundtrip_guide.md)

**Release Materials**

- [Public Overview](docs/release/public_project_overview.md) — Status, evidence levels, red lines
- [Demo Asset Index](docs/release/demo_asset_index.md) · [Master Shot List](docs/release/demo_master_shot_list.md)

</details>
