# guiLaTeX

> **v1-candidate · 第一阶段收官区**
>
> guiLaTeX is a visual LaTeX editor supporting PDF element-level editing, LaTeX code generation via Export IR, and dual-end prototypes (Web + Qt).

> 🏆 本项目为 [TRAE 创意编程大赛](https://forum.trae.cn/t/topic/7939/12) 参赛作品。
> 欢迎去[论坛帖子](https://forum.trae.cn/t/topic/7939/12)投票加油！❤️
>
> 🏆 This project is a submission for the [TRAE Creative Coding Contest](https://forum.trae.cn/t/topic/7939/12).
> If you find it interesting, please visit the [forum post](https://forum.trae.cn/t/topic/7939/12) to vote! ❤️

---

## 当前状态 / Current Status

**这不是最终完整版。** 项目已进入阶段性收官状态，Web 端和 Qt 端各自完成了核心功能验证，Core 导出内核已稳定，跨端 roundtrip 路径已跑通。

**This is not the final complete version.** The project has entered a milestone phase: Web and Qt have each completed core feature verification, the Core export engine is stable, and the cross-end roundtrip path has been validated.

| 模块 | 状态 | 说明 |
|------|------|------|
| 🌐 **Web** | 独立应用候选版 | 纯浏览器应用，零依赖。文本 CRUD、多选旋转、图层管理、IR/PDF 导出、项目保存/打开均已浏览器级验证。LaTeX 导入导出依赖 Python bridge。 |
| 🖥️ **Qt** | v1-candidate | 桌面端主闭环已跑通（Qt → Core → tex → Core → Qt）。已知 font_family Core gap。PDF 主路径 / 保存打开尚未实现。 |
| 📦 **Core** | 已封板 | IR Schema + LaTeX 导出器 + 回归样本齐备。Qt 和 Web 均可接入。 |

详细状态见 → [公开总览](docs/release/public_project_overview.md)

---

## 界面预览 / Screenshots

### Qt 桌面端 / Qt Desktop

![Qt Desktop Screenshot](assets/qt_screenshot.png)

基于 PyQt6 的桌面应用，支持 PDF 可视化编辑、属性面板、LaTeX 源码预览、roundtrip 闭环验证。

A PyQt6 desktop application supporting visual PDF editing, property panels, LaTeX source preview, and roundtrip verification.

### Web 端 / Web Prototype

![Web Prototype Screenshot](assets/web_screenshot.png)

纯 HTML/CSS/JS 浏览器端应用，零依赖。支持文本 CRUD、多选旋转、图层管理、IR/JSON 导出、PDF 打印导出。

A pure HTML/CSS/JS browser application, zero dependencies. Supports text CRUD, multi-select rotation, layer management, IR/JSON export, and PDF print export.

---

## 展示与文档 / Showcase & Docs

### 🎭 朝堂风云录 — AI Agent 协作开发全记录

- [开发展示页](showcase/) / [Showcase Page](showcase/)
- [Demo 入口](showcase/demo_index.html) / [Demo Index](showcase/demo_index.html)

### 📋 发布文档 / Release Documents

| 文档 | 说明 |
|------|------|
| [公开总览](docs/release/public_project_overview.md) | 项目状态、证据层级、红线清单 |
| [演示资产索引](docs/release/demo_asset_index.md) | 全部演示资产清单与推荐用途 |
| [总录制脚本](docs/release/demo_master_shot_list.md) | 建议的演示录制流程（4 幕 16 shot） |
| [论坛战报草稿](docs/release/forum_update_draft.md) | 可直接发布的阶段性更新贴 |
| [证据脱敏映射](docs/release/public_evidence_redaction_map.md) | 脱敏处理记录 |
| [公开/内部分层](docs/release/public_vs_internal_split.md) | 哪些公开、哪些内部留档 |

### 📖 技术文档 / Technical Docs

| 文档 | 说明 |
|------|------|
| [架构设计](docs/architecture.md) | 系统架构 |
| [用户指南](docs/user-guide.md) | 使用说明 |
| [Export Core 设计](docs/export_core_design.md) | IR 中间层设计 |
| [Export Core 快速上手](docs/export_core_quickstart.md) | 导出核心入门 |
| [Conforming LaTeX Profile](docs/export_core_conforming_latex_profile.md) | LaTeX 导出格式规范 |
| [Roundtrip 指南](docs/export_core_roundtrip_guide.md) | 导出-导入闭环指南 |
| [给人类读者的阅读说明](docs/README_FOR_HUMANS.md) | 文档分层导引 |

---

## 项目结构 / Project Structure

```
guiLaTeX/
├── src/                    # 核心源代码（GUI、数据模型）
├── export_core/            # Export IR 中间层（Schema、导出器、回归样本）
├── tests/                  # 测试套件
├── web_prototype/          # Web 端原型（纯浏览器应用）
├── showcase/               # 开发展示页 + Demo 入口
├── docs/
│   ├── release/            # 发布文档、脱敏证据
│   ├── contest_evidence/   # 演示证据（截图、JSON、canonical pack）
│   ├── audits/             # 审计记录
│   └── research/           # 技术调研
├── assets/                 # 截图等静态资源
└── 整活_争储朝堂/           # 项目文化素材
```

## 技术栈 / Tech Stack

- **Python 3.10+** — 核心逻辑 / Core logic
- **PyQt6** — Qt 桌面端 GUI
- **PyMuPDF (fitz)** — PDF 渲染 / PDF rendering
- **HTML/CSS/JS** — Web 端原型 / Web prototype
- **LaTeX** — 文档编译 / Document compilation
- **Playwright** — Web 自动化回归测试 / Web automation regression testing

## 许可 / License

[Apache License 2.0](LICENSE)
