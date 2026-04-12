# 给人类读者的阅读说明 / Guide for Human Readers

> 本项目保留了完整的开发过程痕迹，包括 AI Agent 协作记录、内部审计文档和历史证据。
> This project preserves its full development history, including AI agent collaboration records, internal audit docs, and historical evidence.

---

## 📖 先读这些 / Start Here

| 文档 | 说明 |
|------|------|
| [README.md](../README.md) | 项目介绍、界面截图、技术栈 |
| [docs/architecture.md](architecture.md) | 系统架构设计 |
| [docs/export_core_design.md](export_core_design.md) | Export IR 中间层设计（核心架构） |
| [docs/export_core_quickstart.md](export_core_quickstart.md) | Export Core 快速上手 |
| [docs/user-guide.md](user-guide.md) | 用户指南（部分功能仍在开发中） |

## 🤖 Agent / 自动化流程相关 / Agent & Automation Docs

这些文档主要面向 AI Agent 或自动化流程，普通读者可以跳过：

| 文档 | 说明 |
|------|------|
| [PLAN.md](../PLAN.md) | 当前开发计划和里程碑（Agent 任务清单） |
| [PROJECT_LOG.md](../PROJECT_LOG.md) | 开发日志（决策记录、修正历史） |
| [RUN_LEDGER.md](../RUN_LEDGER.md) | Agent 运行状态记录 |
| [MULTI_AGENT_PLAN.md](../MULTI_AGENT_PLAN.md) | 多 Agent 协作方案设计 |
| [docs/skills/qt_agent_guard.md](skills/qt_agent_guard.md) | Qt 开发 Agent 行为规范 |
| [docs/skills/web_agent_guard.md](skills/web_agent_guard.md) | Web 开发 Agent 行为规范 |

## 📋 审计与复盘 / Audits & Retrospectives

这些文档记录了开发过程中的审计、复盘和经验总结：

| 文档 | 说明 |
|------|------|
| [docs/audits/2026-04-11_post-trae-cn-audit.md](audits/2026-04-11_post-trae-cn-audit.md) | TRAE CN 辅助后的代码审计 |
| [docs/audits/handoff_mtc_to_code.md](audits/handoff_mtc_to_code.md) | MTC → Code 模式交接记录 |
| [docs/contest_evidence/lessons_learned.md](../lessons_learned.md) | 开发经验与教训总结 |
| [docs/contest_evidence/dev_journal.md](dev_journal.md) | 开发日志（Web 原型开发过程） |
| [security_best_practices_report.md](../security_best_practices_report.md) | 安全审计报告 |

## 🧪 测试证据 / Test Evidence

### 证据目录：`docs/contest_evidence/screenshots/`

| 类别 | 文件 | 性质 |
|------|------|------|
| **Web 最终版证据** ✅ | `web_regression_v4_*.png/json` | 真实回归测试结果（v4 最终版） |
| **Web 历史中间版本** | `web_test_*`, `web_regression_*` (v1), `web_regression_v3_*` | 迭代过程中的中间产物，供参考 |
| **Qt 截图** | `16_gui_screenshot.png` | Qt 桌面端界面截图 |
| **Qt 测试数据** | `qt_rotation_test_*.png`, `qt_to_core_*.json` | Qt 线验证数据（headless 环境生成） |

> ⚠️ Qt 线目前仍在 probe/headless 诊断阶段，Qt 截图展示的是界面原型，不代表完整可用状态。

## 🎭 项目文化 / Project Culture

| 目录/文件 | 说明 |
|-----------|------|
| `整活_争储朝堂/` | 项目文化材料（宫廷风开发叙事），非核心文档 |

## 🔬 研究文档 / Research

| 文档 | 说明 |
|------|------|
| [docs/research/pdf-editing-standards.md](research/pdf-editing-standards.md) | PDF 编辑技术标准调研 |
| [docs/research/selection-box-patents.md](research/selection-box-patents.md) | 选择框专利调研 |

## 📌 当前版本状态

- **Web + Core** 是当前主可用路径
- **Qt 桌面端**仍在 probe/headless 诊断阶段，不作为当前 v1 完成判据
- 当前版本是 Web-first 的中间版本 / v1 里程碑版
- 以内部导入导出闭环、单页优先为主

## 🛠️ 工具脚本 / Utility Scripts

根目录下的 `*_smoke.py`、`verify_*.py`、`create_zip_package.py` 等是开发和验证过程中使用的工具脚本，普通用户不需要直接运行。
