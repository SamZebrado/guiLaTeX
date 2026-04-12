# guiLaTeX — 公开发布说明

> 🏆 本项目为 [TRAE 创意编程大赛](https://forum.trae.cn/t/topic/7939/12) 参赛作品，目前仍在活跃开发中。
> 如果你觉得这个项目有意思，欢迎去[论坛帖子](https://forum.trae.cn/t/topic/7939/12)投票加油！❤️

## 关于本项目

guiLaTeX 是一个可视化 LaTeX 编辑器，支持 PDF 文档的加载、元素级编辑和 LaTeX 代码导出。项目采用 Python + PyQt6 构建 GUI，使用 PyMuPDF 进行 PDF 渲染，并通过 Export IR 中间层实现 LaTeX 代码生成。

## 界面预览

### Qt 桌面端

![Qt Desktop Screenshot](assets/qt_screenshot.png)

基于 PyQt6 的桌面应用，支持 PDF 可视化编辑、属性面板、LaTeX 源码预览。

### Web 端原型

![Web Prototype Screenshot](assets/web_screenshot.png)

基于 HTML/JS 的浏览器端原型，支持元素拖拽、多选旋转、IR 导出。

## 当前发布版本

本版本为**脱敏公开版**，已移除高风险个人信息、运行时敏感目录和内部 Agent 日志，保留了经脱敏的开发审计与方法记录。

### 包含内容

- **核心源代码**：`src/`（GUI、LaTeX 引擎、数据模型）
- **导出核心**：`export_core/`（IR Schema、LaTeX 导出器、回归测试样本）
- **测试套件**：`tests/`（模型层测试、集成测试、smoke test）
- **Web 原型**：`web_prototype/`（浏览器端 PDF 编辑原型）
- **技术文档**：架构设计、API 文档、用户指南
- **开发经验**：多 Agent 协作经验、审计记录、教训总结
- **测试证据**：GUI/Web 测试截图

### 未包含内容

以下内容因包含个人身份信息或内部开发记录，暂不公开：
- Agent 通信记录和运行日志
- 多 Agent RAM Disk 配置的原始路径
- TRAE CN IDE 导出记录
- 内部 checkpoint 文档
- 临时测试文件和归档包

## 开发状态

本项目处于活跃开发中。当前版本展示了：
- 基于 PyQt6 的 PDF 可视化编辑
- 基于 PyMuPDF 的 PDF 渲染和元素提取
- Export IR 中间层架构（JSON → LaTeX）
- 多层回归测试样本
- Web 端原型（Playwright 自动化测试）

## 技术栈

- Python 3.10+
- PyQt6 — GUI 框架
- PyMuPDF (fitz) — PDF 渲染
- LaTeX — 文档编译
- Playwright — Web 端自动化测试

## 许可

[Apache License 2.0](LICENSE)
