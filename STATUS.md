# guiLaTeX 项目状态

## 项目概览
- **项目名称**: guiLaTeX
- **项目描述**: 可视化LaTeX编辑器，支持像Photoshop那样选中拖动编辑LaTeX元素，像Word那样改变字体字号颜色排版
- **技术栈**: PyQt6 (Python), PyMuPDF, TeX Live 2022
- **当前阶段**: Phase 5 - 内部模型驱动架构重构

## 当前状态

### 已实现功能 ✅

#### 模型层 (Model Layer) - 已完成 ✅
- **ElementModel**: 元素模型，包含唯一ID、类型、内容、几何属性、字体属性、dirty标记
- **PageModel**: 页面模型，管理元素集合，支持增删改查
- **DocumentModel**: 文档模型，根模型，管理多页面
- **深拷贝支持**: 所有模型支持深拷贝，避免别名问题
- **序列化**: 支持to_dict/from_dict，便于保存和恢复
- **唯一ID**: 使用UUID确保所有元素、页面、文档ID唯一
- **状态追踪**: dirty标记系统，追踪修改状态

| 组件 | 状态 | 说明 |
|------|------|------|
| ElementModel | ✅ 完成 | 元素模型，唯一ID，深拷贝 |
| PageModel | ✅ 完成 | 页面模型，元素管理 |
| DocumentModel | ✅ 完成 | 文档模型，多页面管理 |
| 模型层测试 | ✅ 完成 | 100%测试通过 |

#### UI层 (旧架构，待重构)
- PDF Canvas Viewer | ⚠️ 待重构 | 当前基于PDF直接编辑，需改为模型驱动
- 元素选择 | ⚠️ 待重构 | 需要适配新模型
- 大小调整 | ⚠️ 待重构 | 需要适配新模型
- 内存中编辑 | ⚠️ 待重构 | 将被模型层替代
- 字体等比例变化 | ⚠️ 待重构 | 需要适配新模型
- 缩放控制 | ⚠️ 待重构 | 需要适配新模型
- 页面导航 | ⚠️ 待重构 | 需要适配新模型

### 待完成任务 📋

| 优先级 | 任务 | 状态 | 预估工作量 |
|--------|------|------|-----------|
| P0 | 重构PDFCanvas使用内部模型 | 🔄 进行中 | 4-6 小时 |
| P1 | 调整编辑逻辑（只改模型） | ⏳ 待开始 | 3-4 小时 |
| P2 | 明确保存语义（移除误导性命名） | ⏳ 待开始 | 2-3 小时 |
| P3 | 实现低磁盘开销预览策略 | ⏳ 待开始 | 3-4 小时 |
| P4 | 更新LaTeX Engine支持模型导出 | ⏳ 待开始 | 4-6 小时 |
| P5 | 添加更多模型层测试 | ⏳ 待开始 | 2-3 小时 |

## 技术架构

### 新架构：内部模型驱动

```
guiLaTeX/
├── src/
│   ├── model/              # ✅ 新增：内部模型层（Source of Truth）
│   │   ├── __init__.py
│   │   ├── element.py      # ElementModel
│   │   ├── page.py         # PageModel
│   │   └── document.py     # DocumentModel
│   ├── gui/
│   │   ├── main.py         # 主应用入口（待重构）
│   │   ├── pdf_canvas.py   # PDF画布（待重构为模型驱动）
│   │   ├── properties.py   # 属性面板（待适配）
│   │   └── preview.py      # 预览组件（待适配）
│   └── latex/
│       ├── engine.py       # LaTeX编译引擎（待适配）
│       └── pdf_reconstructor.py  # 暂缓实现
├── tests/
│   └── test_model.py       # ✅ 模型层测试
└── docs/
    └── architecture.md     # 架构文档
```

### 核心原则

1. **内部模型是Source of Truth**: DocumentModel/PageModel/ElementModel 是文档状态的唯一真相源
2. **LaTeX源码由模型生成**: 不再尝试直接编辑PDF，而是从模型生成LaTeX
3. **PDF只是预览产物**: PDF仅作为预览/导出产物，不作为实时编辑真相源
4. **低磁盘开销**: 平时编辑只更新模型，仅在"预览/导出"时编译PDF

### 关键类

#### 模型层 (已完成)
- **ElementModel**: 单个元素（文本、图片等）
  - 属性: id, type, content, x, y, width, height, font_size, dirty
  - 方法: update_position, update_size, update_content, copy
  
- **PageModel**: 单页，包含多个元素
  - 属性: id, number, elements, width, height, dirty
  - 方法: add_element, remove_element, get_element_by_id, select_element
  
- **DocumentModel**: 整个文档，包含多页
  - 属性: id, title, author, pages, dirty
  - 方法: add_page, get_page, get_element_by_id, to_dict, from_dict

#### UI层 (待重构)
- **PDFPageWidget**: 需要改为显示模型覆盖层而非直接编辑PDF
- **PDFCanvas**: 需要连接DocumentModel而非直接操作PDF

## 使用说明

### 启动应用
```bash
cd guiLaTeX
source venv/bin/activate
python src/gui/main.py
```

### 当前限制（架构重构中）
- ⚠️ 正在从"PDF直接编辑"迁移到"模型驱动"
- ⚠️ 部分UI功能暂时不可用
- ⚠️ 保存/预览语义即将调整

## 当前问题

### 架构问题（正在解决）
1. **~~memory_elements 浅拷贝~~** ✅ 已解决：模型层使用深拷贝
2. **~~element id 不唯一~~** ✅ 已解决：使用UUID
3. **save_changes 误导性命名** ⏳ 待解决：将改为 apply_to_model / export_model
4. **直接PDF编辑思维** ⏳ 待解决：改为模型驱动
5. **PDF-to-LaTeX 过早实现** ⏳ 已暂缓：本轮不做

### 代码质量问题
- **双轨制混乱**: `text_elements` 和 `memory_elements` 将被模型层统一替代
- **选中状态管理**: 将由PageModel.select_element管理
- **预览/导出语义不清**: 将明确区分 preview_pdf / export_pdf

## 下一步计划

### 短期目标 (本周)
1. ✅ 建立内部模型层 (已完成)
2. 🔄 重构PDFCanvas使用内部模型 (进行中)
3. ⏳ 调整编辑逻辑（只改模型）
4. ⏳ 明确保存语义

### 中期目标 (下周)
1. 实现低磁盘开销预览策略
2. 更新LaTeX Engine支持模型导出
3. 完善属性面板
4. 添加更多测试

### 长期目标 (本月)
1. 支持更多元素类型
2. 完善撤销/重做
3. 文档格式保存/加载
4. 用户手册

## 风险评估

| 风险 | 级别 | 缓解措施 |
|------|------|----------|
| 架构重构复杂度 | 中 | 保持最小改动，逐步迁移 |
| 用户习惯改变 | 低 | 更新UI文案，提供清晰反馈 |
| 性能下降 | 低 | 模型层轻量，渲染优化 |

## 资源需求

- **开发环境**: Python 3.10+, PyQt6, PyMuPDF, TeX Live
- **测试环境**: macOS (当前), 需要扩展到 Windows/Linux
- **文档**: 需要补充架构文档和用户手册

---

**最后更新**: 2026-04-04  
**更新者**: Builder Agent  
**版本**: 2.0 (架构重构中)
