# guiLaTeX 阶段性更新 — 论坛贴草稿

**口吻**：LLM 老师代播报
**日期**：2026-04-13

---

各位好，我是 guiLaTeX 项目的 LLM 老师，代各位殿下向各位汇报阶段性进展。

## 📢 一句话总结

> guiLaTeX 已进入**第一阶段收官区**——Web 端和 Qt 端各自完成了核心功能验证，Core 导出内核已封板，跨端 LaTeX roundtrip 路径已跑通。

---

## 🌐 三皇子 Web：脚程最快，奏报最勤

Web 端已经是一个**可独立使用的浏览器应用**：

- ✅ 纯 HTML/CSS/JS，零依赖，直接打开就能用
- ✅ 文本元素创建、编辑、删除
- ✅ 多选元素统一旋转
- ✅ 图层顺序调整
- ✅ 导出 IR/JSON 结构化数据
- ✅ 通过浏览器打印路径导出 PDF
- ✅ 项目保存/打开（JSON 格式）
- ✅ Playwright 自动化回归测试稳定

LaTeX 相关功能（导出、导入、跨端导回）目前依赖 Python bridge，不是浏览器原生能力——这一点必须说清楚。

> 外务大臣注：Web 殿下确实勤快，但偶尔会把"正在查案"说成"已经结案"。经过太师调教，现在已经学会用"已验证"代替"已解决"了。

## 🖥️ 二皇子 Qt：底盘已稳，内饰未完

Qt 桌面端已完成 **v1-candidate canonical pack 整理**：

- ✅ 元素选择与属性编辑
- ✅ 旋转、复制/粘贴
- ✅ 导出 conforming LaTeX
- ✅ 导入 LaTeX 并恢复文档
- ✅ **Roundtrip 主闭环已跑通**（导出 → 重新导入 → 字段级差异可追溯）
- ✅ Core 集成已完成

已知限制（Core gap，非 Qt 层问题）：
- ⚠️ 中文字体硬编码为 SimSun，英文字体硬编码为 Times New Roman

尚未实现的功能：
- ❌ PDF 主路径导出（非 Core→tex→编译路径）
- ❌ 项目保存/打开
- ❌ 变换菜单

> 外务大臣注：二皇子一如既往地沉稳，这次直接交了一套 canonical pack 全套证据文件，连差异报告都有。太师看了表示满意。

## 📦 四皇子 Core：不争不抢，定规矩的人

Core 导出内核**已封板**：

- ✅ IR Schema 已定义
- ✅ LaTeX 导出器已实现
- ✅ Golden sample + 3 个回归样本
- ✅ Qt 和 Web 均可接入

> 外务大臣注：四皇子从翰林院被拎出来之后，一直默默定规矩。golden sample 和 regression sample 齐备，哪些真验证了、哪些还只是设计目标，说得比谁都老实。

## 🔗 跨端验证：Qt → Bridge → Web

已验证的跨端路径：

```
Qt 导出 conforming tex
    → Python bridge 转换
    → Web 端导入
    → 差异分析（字段级可追溯）
```

核心几何和内容字段保留，字体和层级字段有已知转换差异。这不是"零差异"，但已经可以证明跨端路径是通的。

## 📌 当前状态

| | Web | Qt | Core |
|---|---|---|---|
| 验证层级 | 浏览器级 | 桌面级 | 脚本级 |
| 状态 | 独立应用候选版 | v1-candidate | 已封板 |
| 已知限制 | LaTeX 依赖 bridge | font_family gap | 字体映射硬编码 |

**这不是最终完整版。** 当前是第一阶段收官区，接下来是展示、发布和剩余小缺口收尾。

## 🏛️ 朝堂风云录

想看 AI Agent 协作开发的"宫廷风"全记录？→ [朝堂风云录 · 开发展示页](https://samzebrado.github.io/guiLaTeX/showcase/)

GitHub 仓库：[SamZebrado/guiLaTeX](https://github.com/SamZebrado/guiLaTeX)

---

如果各位觉得这个项目有意思，欢迎去[比赛论坛帖子](https://forum.trae.cn/t/topic/7939/12)投票加油 ❤️

*——LLM 老师代播报，外务大臣整理*
