# guiLaTeX 项目计划

## 打包时发现的开发意见

> 脱敏打包过程中发现的代码问题和改进建议，详见：
> **[DEV_SUGGESTIONS_2026-04-12.md](DEV_SUGGESTIONS_2026-04-12.md)**
>
> 涵盖：依赖声明修复、DocumentModel 架构问题、失败测试修复、功能重叠整理、开源预备配置等。

---

## 当前迭代: Phase 5 完善

### 迭代目标
完成 PDF-as-Canvas 架构的核心功能，实现可用的可视化编辑器基础版本。

---

## 任务清单

### 🔴 P0: 修复视觉元素更新问题

**任务ID**: TASK-001  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 问题描述
当前调整元素大小后，视觉更新不及时，选中元素存在双重绘制问题。

#### 技术方案

1. **统一元素存储**
   ```python
   # 合并 text_elements 和 memory_elements
   self.elements = self.extract_text_elements()  # 单一数据源
   ```

2. **修复绘制逻辑**
   ```python
   def paintEvent(self, event):
       # 1. 渲染PDF背景
       # 2. 绘制所有元素（包括选中的）
       # 3. 在元素上方绘制选择框（不跳过选中元素）
   ```

3. **确保更新触发**
   ```python
   def mouseMoveEvent(self, event):
       # ... 调整大小逻辑 ...
       self.update()  # 强制重绘
       self.drag_start_pos = event.pos()
   ```

#### 验收标准
- [ ] 调整元素大小后视觉立即更新
- [ ] 选中元素不再出现双重绘制
- [ ] 缩放时元素大小正确变化

---

### 🟠 P1: 实现元素移动功能

**任务ID**: TASK-002  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 功能描述
支持拖动选中的PDF元素改变位置。

#### 技术方案

1. **添加拖动模式识别**
   ```python
   self.drag_mode = None  # None, 'move', 'resize'
   ```

2. **修改鼠标事件处理**
   ```python
   def mousePressEvent(self, event):
       handle = self.get_handle_at(event.pos())
       if handle:
           self.drag_mode = 'resize'
           self.drag_handle = handle
       elif element:
           self.drag_mode = 'move'
           self.selected_element = element
           self.drag_start_pos = event.pos()
   ```

3. **实现移动逻辑**
   ```python
   def mouseMoveEvent(self, event):
       if self.drag_mode == 'move' and self.selected_element:
           dx = (event.pos().x() - self.drag_start_pos.x()) / self.scale
           dy = (event.pos().y() - self.drag_start_pos.y()) / self.scale
           
           self.selected_element['x'] += dx
           self.selected_element['y'] += dy
           
           self.update()
           self.drag_start_pos = event.pos()
   ```

#### 验收标准
- [ ] 可以拖动选中元素改变位置
- [ ] 移动时有视觉反馈（如半透明效果）
- [ ] 移动后元素位置正确保存

---

### 🟡 P2: 实现PDF文本更新

**任务ID**: TASK-003  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 6-8 小时

#### 功能描述
将内存中的编辑结果保存回PDF文件。

#### 技术方案

1. **使用 PyMuPDF 文本编辑**
   ```python
   def update_pdf_element(self, element):
       page = self.pdf_doc.load_page(self.page_num)
       
       # 1. 标记旧文本区域为 redaction
       rect = fitz.Rect(element['x'], element['y'], 
                       element['x'] + element['original_width'],
                       element['y'] + element['original_height'])
       page.add_redact_annot(rect)
       
       # 2. 应用 redaction
       page.apply_redactions()
       
       # 3. 插入新文本
       new_rect = fitz.Rect(element['x'], element['y'],
                           element['x'] + element['width'],
                           element['y'] + element['height'])
       page.insert_textbox(new_rect, element['text'], 
                          fontsize=element['font_size'])
   ```

2. **实现保存功能**
   ```python
   def save_changes(self):
       if not self.is_dirty:
           return True
       
       try:
           for element in self.memory_elements:
               if self.is_element_modified(element):
                   self.update_pdf_element(element)
           
           self.pdf_doc.saveIncr()
           self.is_dirty = False
           return True
       except Exception as e:
           print(f"保存失败: {e}")
           return False
   ```

#### 验收标准
- [ ] 可以保存元素大小修改到PDF
- [ ] 可以保存元素位置修改到PDF
- [ ] 保存后PDF可以正常打开
- [ ] 有保存成功/失败的反馈

---

### 🟢 P3: 实现LaTeX同步 (简化版)

**任务ID**: TASK-004  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 16-20 小时

#### 功能描述
建立PDF元素与LaTeX源代码的映射关系，支持简单元素的双向同步。

#### 技术方案

1. **元素标识系统**
   ```python
   # 在LaTeX中添加特殊注释
   %%guiLaTeX:element:id=text_001:type=text%%
   Hello World
   %%guiLaTeX:end:text_001%%
   ```

2. **编译时注入标记**
   ```python
   class LaTeXGenerator:
       def add_element_markers(self, latex_code):
           # 解析LaTeX并添加标记
           # 返回带标记的代码
   ```

3. **建立反向映射**
   ```python
   self.element_to_latex_map = {
       'text_001': {
           'line_start': 10,
           'line_end': 12,
           'content': 'Hello World'
       }
   }
   ```

4. **同步更新**
   ```python
   def sync_to_latex(self, element):
       # 根据元素ID找到对应LaTeX代码位置
       # 更新LaTeX代码
       # 重新编译生成PDF
   ```

#### 验收标准
- [ ] 可以识别带标记的LaTeX元素
- [ ] 简单文本修改可以同步回LaTeX
- [ ] 同步后重新编译PDF正确

---

### 🔵 P4: PDF-to-LaTeX重建引擎 (长期)

**任务ID**: TASK-005  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 40+ 小时

#### 功能描述
从任意PDF文件重建可编辑的LaTeX代码。

#### 技术方案

1. **内容分析**
   - 文本块识别
   - 字体特征分析
   - 布局结构检测

2. **元素分类**
   - 标题 (字体大、加粗)
   - 段落 (连续文本块)
   - 公式 (特殊字体、数学符号)
   - 图片 (图像区域)

3. **代码生成**
   ```python
   def generate_latex(self, elements):
       latex_parts = []
       for element in elements:
           if element['type'] == 'heading':
               latex_parts.append(f"\\section{{{element['text']}}}")
           elif element['type'] == 'math':
               latex_parts.append(f"${element['text']}$")
           # ...
       return '\\n'.join(latex_parts)
   ```

#### 验收标准
- [ ] 可以识别PDF中的基本结构
- [ ] 生成的LaTeX代码可编译
- [ ] 支持常见文档类型

---

## 实施路线图

```
Week 1-2:
├── TASK-001: 修复视觉更新问题 [2-3h]
├── TASK-002: 实现元素移动功能 [3-4h]
└── 集成测试

Week 3-4:
├── TASK-003: 实现PDF文本更新 [6-8h]
└── 完善错误处理和用户反馈

Month 2:
├── TASK-004: LaTeX同步简化版 [16-20h]
├── 属性面板增强
└── 支持更多元素类型

Month 3+:
├── TASK-005: PDF重建引擎 [40+h]
├── 性能优化
└── 插件系统
```

---

## 决策记录

### 2026-04-04: 采用保守路线
**决策**: 先完成任务1-3，实现可用的PDF编辑器  
**原因**: 
- 降低项目风险
- 快速获得用户反馈
- 任务4-5复杂度高，需要更多调研

### 技术选型
- **PDF编辑**: PyMuPDF (fitz) - 功能全面，文档完善
- **GUI框架**: PyQt6 - 跨平台，功能强大
- **LaTeX编译**: TeX Live 2022 - 标准发行版

---

## 待决策事项

1. **是否支持多页同时编辑？**
   - 选项A: 单页编辑（简单）
   - 选项B: 多页缩略图导航（复杂）

2. **PDF重建引擎的准确度目标？**
   - 选项A: 80% 常见文档（现实）
   - 选项B: 95% 所有文档（困难）

3. **是否支持协作编辑？**
   - 选项A: 单用户（当前）
   - 选项B: 多用户实时协作（未来）

---

**最后更新**: 2026-04-11  
**更新者**: Builder Agent

## 新添加的未完成项

### 🟡 P2: 实现更完善的图层管理界面
**任务ID**: TASK-006  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 4-6 小时

#### 功能描述
实现图层管理的可视化界面，包括图层列表、显示/隐藏控制、图层重命名等功能。

### 🟡 P2: 添加字体预览功能
**任务ID**: TASK-007  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 功能描述
在字体选择下拉框中添加字体预览功能，让用户可以直观地看到字体效果。

### 🟡 P2: 实现更高级的对象选择和编辑功能
**任务ID**: TASK-008  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 6-8 小时

#### 功能描述
实现多选、框选、批量编辑等高级对象选择和编辑功能。

### 🟡 P2: 优化 PDF 导出功能
**任务ID**: TASK-009  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 4-6 小时

#### 功能描述
优化 PDF 导出功能，支持更多导出选项和格式。

### 🟢 P3: 添加更多的自动测试用例
**任务ID**: TASK-010  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 5-7 小时

#### 功能描述
添加更多的自动测试用例，包括边界情况测试、性能测试等。

---

### 🟡 P2: 完善 Web 线的段落（paragraph）resize 功能
**任务ID**: TASK-032  
**负责人**: Web  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 功能描述
实现段落（paragraph）元素的 resize 功能，与文本框（textbox）类似，支持通过选择框手柄调整大小。

#### 技术方案
- 在 renderElements 函数中为 paragraph 元素添加 resize 手柄
- 实现 paragraph 元素的 resize 逻辑
- 确保 resize 后模型中的 width 和 height 值正确更新

#### 验收标准
- [ ] 段落元素可以通过选择框手柄调整大小
- [ ] 调整大小后模型中的 width 和 height 值正确更新
- [ ] 调整大小后元素显示正常

---

### 🟡 P2: 优化 Web 线的旋转功能
**任务ID**: TASK-033  
**负责人**: Web  
**状态**: 待分配  
**预估工时**: 4-5 小时

#### 功能描述
优化 Web 线的旋转功能，包括：
- 旋转时的视觉反馈
- 旋转后的边界框计算
- 旋转状态的持久化

#### 技术方案
- 增强旋转手柄的交互体验
- 实现旋转后的边界框计算
- 确保旋转状态在模型中正确记录
- 优化旋转时的性能

#### 验收标准
- [ ] 旋转时有流畅的视觉反馈
- [ ] 旋转后的元素边界框计算正确
- [ ] 旋转状态在模型中正确记录
- [ ] 旋转功能性能良好

---

### 🟡 P2: 完善 Web 端 font_family_zh 和 font_family_en 字段
**任务ID**: TASK-034  
**负责人**: Web  
**状态**: 待分配  
**预估工时**: 1-2 小时

#### 功能描述
在 Web 模型中添加 font_family_zh 和 font_family_en 字段，替代当前单一的 fontFamily 字段，实现中英文分离的字体选择。

#### 技术方案
- 在 Web 模型的元素数据结构中添加 font_family_zh 和 font_family_en 字段
- 更新字体选择 UI，支持中英文分别选择
- 确保字体信息正确传递到 Export IR

#### 验收标准
- [ ] Web 模型中包含 font_family_zh 和 font_family_en 字段
- [ ] 字体选择 UI 支持中英文分别选择
- [ ] 字体信息正确导出到 Export IR

---

### 🟡 P2: 为 Web 端添加 page 字段支持
**任务ID**: TASK-035  
**负责人**: Web  
**状态**: 待分配  
**预估工时**: 1-2 小时

#### 功能描述
在 Web 模型中添加 page 字段，当前固定为 1，为未来多页支持做准备。

#### 技术方案
- 在 Web 模型的元素数据结构中添加 page 字段
- 默认值设为 1
- 确保 page 字段正确导出到 Export IR

#### 验收标准
- [ ] Web 模型中包含 page 字段
- [ ] page 字段默认值为 1
- [ ] page 字段正确导出到 Export IR

---

### 🟡 P2: 完善 normalize_web_model_to_ir 函数
**任务ID**: TASK-036  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 功能描述
根据 Web 模型的最新字段结构，完善 normalize_web_model_to_ir 函数，确保所有字段正确转换。

#### 技术方案
- 分析最新 Web 模型结构
- 更新字段映射逻辑
- 处理缺失字段的 fallback 值
- 添加单元测试

#### 验收标准
- [ ] normalize_web_model_to_ir 能正确处理 Web 模型
- [ ] 所有字段正确映射到 Export IR
- [ ] 缺失字段有合理的 fallback 值
- [ ] 单元测试通过

---

### 🟠 P1: 修复颜色选择器初始黑盘问题
**任务ID**: TASK-011  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 问题描述
初始打开 Font 的 Colors 时，圆色盘一开始是黑色的，但可以选颜色；切换几次别的选颜色方法后会恢复彩色。

#### 技术方案
- 调查 QColorDialog.getColor() 原生对话框的初始化问题
- 考虑使用非原生对话框或自定义颜色选择器
- 检查 Qt 平台主题设置

#### 验收标准
- [ ] 初始打开颜色选择器时圆色盘显示正常
- [ ] 颜色选择功能正常工作
- [ ] 切换颜色选择方式时没有异常

---

### 🟠 P1: 添加对象旋转入口
**任务ID**: TASK-012  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 4-6 小时

#### 功能描述
为对象添加可见的旋转入口，包括旋转手柄或旋转按钮/控件。

#### 技术方案
- 在选择框中添加旋转手柄
- 或在属性面板中添加旋转控件
- 实现旋转逻辑，包括旋转角度计算和应用

#### 验收标准
- [ ] 选中对象时有可见的旋转入口
- [ ] 可以通过旋转入口旋转对象
- [ ] 旋转后对象位置和大小正确
- [ ] 旋转角度记录在模型中

---

### 🟢 P3: 实现完整的对象旋转功能
**任务ID**: TASK-013  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 5-7 小时

#### 功能描述
实现完整的对象旋转逻辑，包括：
- 旋转角度的视觉渲染
- 旋转手柄交互
- 旋转后对象边界框计算
- 旋转状态持久化

#### 技术方案
- 在 PDFPageWidget 的 draw_memory_elements 中添加旋转渲染支持
- 实现旋转角度的视觉反馈
- 完善旋转属性的模型同步

#### 验收标准
- [ ] 对象旋转后正确渲染
- [ ] 旋转角度正确保存和加载
- [ ] 旋转后对象交互正常
- [ ] 旋转状态在模型中正确记录

---

### 🟡 P2: 完善颜色选择器与 dict 风格元素的集成
**任务ID**: TASK-014  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 问题描述
当前颜色选择器只支持 QGraphicsItem 风格的元素，需要支持 dict 风格的 PDF 元素。

#### 技术方案
- 在 dict 风格元素数据结构中添加 color 字段
- 在 on_color_clicked 中支持 dict 风格元素
- 在 draw_memory_elements 中渲染元素颜色

#### 验收标准
- [ ] dict 风格元素可以设置颜色
- [ ] 设置的颜色在渲染中正确显示
- [ ] 颜色状态在模型中正确记录

---

### 🟠 P1: 完善 Export IR 模型
**任务ID**: TASK-015  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 4-6 小时

#### 功能描述
完善 Export IR 模型，添加更多元素类型和属性支持，包括 textbox、表格等复杂元素。

#### 技术方案
- 扩展 IR schema，添加更多元素类型
- 完善属性定义，支持更丰富的样式属性
- 添加元素间关系的定义

#### 验收标准
- [ ] 支持 textbox 元素类型
- [ ] 支持表格元素类型
- [ ] 扩展后的 IR 模型向后兼容

---

### 🟠 P1: 增强 LaTeX 导出器
**任务ID**: TASK-016  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 6-8 小时

#### 功能描述
增强 LaTeX 导出器，支持更多元素类型和复杂排版需求。

#### 技术方案
- 支持 textbox 元素的导出
- 支持表格元素的导出
- 优化公式排版
- 改进图片处理

#### 验收标准
- [ ] 正确导出 textbox 元素
- [ ] 正确导出表格元素
- [ ] 公式排版更加美观
- [ ] 图片处理更加灵活

---

### 🟡 P2: 实现 Web JSON -> IR 映射
**任务ID**: TASK-017  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 3-5 小时

#### 功能描述
实现 Web JSON 模型到 Export IR 的映射功能。

#### 技术方案
- 分析 Web JSON 模型结构
- 实现映射函数
- 处理坐标系统转换

#### 验收标准
- [ ] Web JSON 模型正确映射到 Export IR
- [ ] 坐标系统转换准确
- [ ] 所有元素属性正确映射

---

### 🟡 P2: 实现 Qt model -> IR 映射
**任务ID**: TASK-018  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 3-5 小时

#### 功能描述
实现 Qt 模型到 Export IR 的映射功能。

#### 技术方案
- 分析 Qt 模型结构
- 实现映射函数
- 处理坐标系统转换

#### 验收标准
- [ ] Qt 模型正确映射到 Export IR
- [ ] 坐标系统转换准确
- [ ] 所有元素属性正确映射

---

### 🟢 P3: 实现多页导出支持
**任务ID**: TASK-019  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 4-6 小时

#### 功能描述
支持多页文档的导出，处理跨页元素和页面布局。

#### 技术方案
- 扩展 IR 模型以支持多页
- 修改 LaTeX 导出器以处理多页
- 实现页面布局和跨页元素处理

#### 验收标准
- [ ] 正确导出多页文档
- [ ] 跨页元素处理正确
- [ ] 页面布局符合预期

### 🟡 P2: 完善元素选择与旋转后的交互
**任务ID**: TASK-015  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 问题描述
元素旋转后，鼠标选择和交互可能需要考虑旋转后的边界框计算。

#### 技术方案
- 在 get_element_at 和 get_handle_at 方法中考虑旋转
- 实现旋转后的边界框计算
- 确保旋转后的元素仍然可以正确选择和交互

#### 验收标准
- [ ] 旋转后的元素可以正确选择
- [ ] 旋转后的元素可以正确调整大小
- [ ] 旋转后的元素交互体验正常

---

### 🟢 P3: 完善颜色选择器与 dict 风格元素的集成
**任务ID**: TASK-016  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 问题描述
当前颜色选择器只支持 QGraphicsItem 风格的元素，需要支持 dict 风格的 PDF 元素，并在渲染中显示颜色。

#### 技术方案
- 在 dict 风格元素数据结构中添加 color 字段
- 在 on_color_clicked 中支持 dict 风格元素
- 在 draw_memory_elements 中渲染元素颜色

#### 验收标准
- [ ] dict 风格元素可以设置颜色
- [ ] 设置的颜色在渲染中正确显示
- [ ] 颜色状态在模型中正确记录
- [ ] 颜色字段正确导出到 IR

---

### 🟡 P2: 实现 Web 线的段落（paragraph）resize 功能
**任务ID**: TASK-020  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 功能描述
实现段落（paragraph）元素的 resize 功能，与文本框（textbox）类似，支持通过选择框手柄调整大小。

#### 技术方案
- 在 renderElements 函数中为 paragraph 元素添加 resize 手柄
- 实现 paragraph 元素的 resize 逻辑
- 确保 resize 后模型中的 width 和 height 值正确更新

#### 验收标准
- [ ] 段落元素可以通过选择框手柄调整大小
- [ ] 调整大小后模型中的 width 和 height 值正确更新
- [ ] 调整大小后元素显示正常

---

### 🟡 P2: 优化 Web 线的旋转功能
**任务ID**: TASK-021  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 4-5 小时

#### 功能描述
优化 Web 线的旋转功能，包括：
- 旋转时的视觉反馈
- 旋转后的边界框计算
- 旋转状态的持久化

#### 技术方案
- 增强旋转手柄的交互体验
- 实现旋转后的边界框计算
- 确保旋转状态在模型中正确记录
- 优化旋转时的性能

#### 验收标准
- [ ] 旋转时有流畅的视觉反馈
- [ ] 旋转后的元素边界框计算正确
- [ ] 旋转状态在模型中正确记录
- [ ] 旋转功能性能良好

---

### 🟠 P1: 完成 Web 线核心交互功能的可信验证
**任务ID**: TASK-022  
**负责人**: Builder  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 功能描述
完成点击瞬移和多选旋转功能的可信验证，包括：
- 浏览器级自动化测试
- 手动测试验证
- 测试结果文档化

#### 技术方案
- 配置 Playwright 环境
- 运行浏览器自动化测试
- 执行手动测试
- 记录测试结果

#### 验收标准
- [ ] 浏览器级自动化测试通过
- [ ] 手动测试验证通过
- [ ] 测试结果文档化
- [ ] 核心交互功能确认已修复

---

### 🟡 P2: 完善 Web 端 font_family_zh 和 font_family_en 字段
**任务ID**: TASK-023  
**负责人**: Web  
**状态**: 待分配  
**预估工时**: 1-2 小时

#### 功能描述
在 Web 模型中添加 font_family_zh 和 font_family_en 字段，替代当前单一的 fontFamily 字段，实现中英文分离的字体选择。

#### 技术方案
- 在 Web 模型的元素数据结构中添加 font_family_zh 和 font_family_en 字段
- 更新字体选择 UI，支持中英文分别选择
- 确保字体信息正确传递到 Export IR

#### 验收标准
- [ ] Web 模型中包含 font_family_zh 和 font_family_en 字段
- [ ] 字体选择 UI 支持中英文分别选择
- [ ] 字体信息正确导出到 Export IR

---

### 🟡 P2: 完善 Qt 端 font_family_zh 和 font_family_en 字段
**任务ID**: TASK-024  
**负责人**: Qt  
**状态**: 待分配  
**预估工时**: 1-2 小时

#### 功能描述
在 Qt 模型中添加 font_family_zh 和 font_family_en 字段，替代当前单一的 font_family 字段，实现中英文分离的字体选择。

#### 技术方案
- 在 Qt 模型的元素数据结构中添加 font_family_zh 和 font_family_en 字段
- 更新字体选择 UI，支持中英文分别选择
- 确保字体信息正确传递到 Export IR

#### 验收标准
- [ ] Qt 模型中包含 font_family_zh 和 font_family_en 字段
- [ ] 字体选择 UI 支持中英文分别选择
- [ ] 字体信息正确导出到 Export IR

---

### 🟡 P2: 为 Web 端添加 page 字段支持
**任务ID**: TASK-025  
**负责人**: Web  
**状态**: 待分配  
**预估工时**: 1-2 小时

#### 功能描述
在 Web 模型中添加 page 字段，当前固定为 1，为未来多页支持做准备。

#### 技术方案
- 在 Web 模型的元素数据结构中添加 page 字段
- 默认值设为 1
- 确保 page 字段正确导出到 Export IR

#### 验收标准
- [ ] Web 模型中包含 page 字段
- [ ] page 字段默认值为 1
- [ ] page 字段正确导出到 Export IR

---

### 🟡 P2: 完善 normalize_web_model_to_ir 函数
**任务ID**: TASK-026  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 功能描述
根据 Web 模型的最新字段结构，完善 normalize_web_model_to_ir 函数，确保所有字段正确转换。

#### 技术方案
- 分析最新 Web 模型结构
- 更新字段映射逻辑
- 处理缺失字段的 fallback 值
- 添加单元测试

#### 验收标准
- [ ] normalize_web_model_to_ir 能正确处理 Web 模型
- [ ] 所有字段正确映射到 Export IR
- [ ] 缺失字段有合理的 fallback 值
- [ ] 单元测试通过

---

### 🟡 P2: 完善 normalize_qt_model_to_ir 函数
**任务ID**: TASK-027  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 功能描述
根据 Qt 模型的最新字段结构，完善 normalize_qt_model_to_ir 函数，确保所有字段正确转换。

#### 技术方案
- 分析最新 Qt 模型结构
- 更新字段映射逻辑
- 处理缺失字段的 fallback 值
- 添加单元测试

#### 验收标准
- [ ] normalize_qt_model_to_ir 能正确处理 Qt 模型
- [ ] 所有字段正确映射到 Export IR
- [ ] 缺失字段有合理的 fallback 值
- [ ] 单元测试通过

---

### 🟠 P1: 优化文本布局
**任务ID**: TASK-028  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 4-6 小时

#### 功能描述
优化 LaTeX 导出器的文本布局，减少与原设计的差异。

#### 技术方案
- 改进文本换行算法
- 优化行间距和字间距控制
- 增强文本框边界处理

#### 验收标准
- [ ] 文本换行更接近原设计
- [ ] 行间距和字间距更合理
- [ ] 文本超出文本框时能适当处理

---

### 🟠 P1: 处理字体 fallback
**任务ID**: TASK-029  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 功能描述
实现字体 fallback 机制，减少字体不可用时的布局差异。

#### 技术方案
- 建立字体 fallback 链
- 实现字体可用性检测
- 优化字体切换时的布局调整

#### 验收标准
- [ ] 字体不可用时能自动切换到合适的替代字体
- [ ] 字体切换后布局差异最小化
- [ ] 提供字体 fallback 配置选项

---

### 🟡 P2: 优化旋转精度
**任务ID**: TASK-030  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 功能描述
优化 LaTeX 导出器的旋转实现，提高旋转精度。

#### 技术方案
- 改进旋转角度计算
- 优化旋转中心点处理
- 增强旋转后边界框计算

#### 验收标准
- [ ] 旋转角度误差 < 0.5度
- [ ] 旋转中心点正确
- [ ] 旋转后元素位置准确

---

### 🟡 P2: 完善页面边距处理
**任务ID**: TASK-031  
**负责人**: ExportCore  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 功能描述
完善 LaTeX 导出器的页面边距处理，减少与原设计的差异。

#### 技术方案
- 优化页面边距设置
- 支持自定义页面尺寸
- 改进页面布局计算

#### 验收标准
- [ ] 页面边距更接近原设计
- [ ] 支持自定义页面尺寸
- [ ] 页面布局计算准确

---

### 🟠 P1: 完善 Qt 离屏渲染验证的深入测试
**任务ID**: TASK-028  
**负责人**: Qt  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 功能描述
继续完善 Qt 离屏渲染验证，添加更深入的测试用例，验证不同旋转角度的渲染正确性。

#### 技术方案
- 测试更多旋转角度（0°, 30°, 45°, 60°, 90°, 180°, -45°）
- 验证旋转后的文字仍然可读
- 验证旋转后的边界框计算
- 添加更多离屏渲染测试用例

#### 验收标准
- [ ] 多旋转角度测试通过
- [ ] 旋转后的文字渲染正确
- [ ] 边界框计算准确

---

### 🟡 P2: 完善 Qt 端的 rotation 交互
**任务ID**: TASK-029  
**负责人**: Qt  
**状态**: 待分配  
**预估工时**: 3-4 小时

#### 功能描述
完善 Qt 端的 rotation 交互，确保旋转后的元素仍然可以正确选择和调整大小。

#### 技术方案
- 在 get_element_at 和 get_handle_at 方法中考虑旋转
- 实现旋转后的边界框计算
- 确保旋转后的元素仍然可以正确选择和交互

#### 验收标准
- [ ] 旋转后的元素可以正确选择
- [ ] 旋转后的元素可以正确调整大小
- [ ] 旋转后的元素交互体验正常

---

### 🟠 P1: 修改 normalize_qt_model_to_ir 中的字体映射逻辑
**任务ID**: TASK-030  
**负责人**: Qt + ExportCore  
**状态**: 待分配  
**预估工时**: 1-2 小时

#### 功能描述
修改 normalize_qt_model_to_ir 中的字体映射逻辑，从 Qt 的 font_family 分离出 font_family_zh 和 font_family_en。

#### 技术方案
- 分析 Qt 的 font_family 字段值
- 实现字体判断逻辑（包含 'SC' 或 'Han' 的判断为中文字体）
- 实现映射：
  - 中文字体 -> (原字体, Inter)
  - 英文字体 -> (Noto Sans SC, 原字体)

#### 验收标准
- [ ] normalize_qt_model_to_ir 能正确从 Qt 的 font_family 分离出 font_family_zh 和 font_family_en
- [ ] 中文字体正确映射
- [ ] 英文字体正确映射

---

### 🟡 P2: （可选）正式添加 font_family_zh 字段到 Qt 模型
**任务ID**: TASK-031  
**负责人**: Qt  
**状态**: 待分配  
**预估工时**: 2-3 小时

#### 功能描述
正式添加 font_family_zh 字段到 Qt 模型，并在 UI 中提供选择。

#### 技术方案
- 在 Qt 模型的元素数据结构中添加 font_family_zh 字段
- 在属性面板中添加中文字体选择控件
- 确保 font_family_zh 字段正确导出到 IR

#### 验收标准
- [ ] Qt 模型中包含 font_family_zh 字段
- [ ] UI 支持中文字体选择
- [ ] font_family_zh 字段正确导出到 IR

---

### 🟡 P2: 正式添加 font_family_zh 和 font_family_en 字段到 Qt 模型
**任务ID**: TASK-032  
**负责人**: Qt  
**状态**: ✅ 完成  
**预估工时**: 2-3 小时

#### 功能描述
正式添加 font_family_zh 和 font_family_en 字段到 Qt 模型，并在 UI 中提供选择。

#### 技术方案
- 在 Qt 模型的元素数据结构中添加 font_family_zh 和 font_family_en 字段
- 在属性面板中添加中文字体和英文字体选择控件
- 确保字体信息正确导出到 IR

#### 验收标准
- [x] Qt 模型中包含 font_family_zh 和 font_family_en 字段
- [x] UI 支持中文字体和英文字体选择
- [x] 字体信息正确导出到 IR

---

### 🟠 P1: 重构PDFCanvas使用内部模型
**任务ID**: TASK-033  
**负责人**: Qt  
**状态**: 🔄 进行中  
**预估工时**: 4-6 小时

#### 功能描述
将 PDFCanvas 重构为使用内部模型驱动，替代当前的直接 PDF 操作。

#### 技术方案
- 修改 PDFCanvas 以使用 DocumentModel 作为数据源
- 移除对 text_elements 和 memory_elements 的直接依赖
- 实现模型驱动的绘制和交互逻辑

#### 验收标准
- [ ] PDFCanvas 完全使用内部模型
- [ ] 绘制和交互逻辑正确
- [ ] 性能和稳定性良好

---

### 🟡 P2: 调整编辑逻辑（只改模型）
**任务ID**: TASK-034  
**负责人**: Qt  
**状态**: ⏳ 待开始  
**预估工时**: 3-4 小时

#### 功能描述
调整编辑逻辑，确保所有编辑操作只修改模型，不直接操作 PDF。

#### 技术方案
- 修改鼠标事件处理，直接更新模型属性
- 实现模型变化的通知机制
- 确保 UI 元素与模型状态同步

#### 验收标准
- [ ] 所有编辑操作只修改模型
- [ ] UI 与模型状态保持同步
- [ ] 编辑操作响应及时

---

### 🟡 P2: 明确保存语义（移除误导性命名）
**任务ID**: TASK-035  
**负责人**: Qt  
**状态**: ⏳ 待开始  
**预估工时**: 2-3 小时

#### 功能描述
明确保存语义，将 save_changes 等误导性命名改为更准确的名称。

#### 技术方案
- 将 save_changes 改为 apply_to_model / export_model
- 明确区分预览和导出操作
- 更新相关文档和注释

#### 验收标准
- [ ] 命名清晰准确
- [ ] 操作语义明确
- [ ] 文档和注释更新完成

---

### 🟠 P1: 实现低磁盘开销预览策略
**任务ID**: TASK-036  
**负责人**: Qt  
**状态**: ⏳ 待开始  
**预估工时**: 3-4 小时

#### 功能描述
实现低磁盘开销的预览策略，避免频繁的 PDF 生成。

#### 技术方案
- 实现内存中的预览渲染
- 优化 PDF 生成时机
- 减少磁盘 I/O 操作

#### 验收标准
- [ ] 预览响应迅速
- [ ] 磁盘开销低
- [ ] 内存使用合理

---

### 🟠 P1: 更新LaTeX Engine支持模型导出
**任务ID**: TASK-037  
**负责人**: Qt  
**状态**: ⏳ 待开始  
**预估工时**: 4-6 小时

#### 功能描述
更新 LaTeX Engine 以支持从模型直接导出 LaTeX。

#### 技术方案
- 修改 LaTeXEngine 以接受模型数据
- 实现模型到 LaTeX 的转换逻辑
- 支持复杂排版需求

#### 验收标准
- [ ] LaTeX Engine 支持模型导出
- [ ] 生成的 LaTeX 代码正确
- [ ] 支持复杂排版

---

### 🟡 P2: 完善图层管理界面
**任务ID**: TASK-038  
**负责人**: Qt  
**状态**: ⏳ 待开始  
**预估工时**: 4-6 小时

#### 功能描述
完善图层管理界面，支持图层的显示/隐藏、重命名、排序等操作。

#### 技术方案
- 添加图层管理面板
- 实现图层操作功能
- 确保图层操作与模型同步

#### 验收标准
- [ ] 图层管理界面完整
- [ ] 图层操作功能正常
- [ ] 与模型状态同步

---

### 🟢 P3: 添加更多测试用例
**任务ID**: TASK-039  
**负责人**: Qt  
**状态**: ⏳ 待开始  
**预估工时**: 5-7 小时

#### 功能描述
添加更多测试用例，包括边界情况测试、性能测试等。

#### 技术方案
- 扩展现有的测试文件
- 添加边界情况测试
- 添加性能测试
- 确保测试覆盖率

#### 验收标准
- [ ] 测试用例完整
- [ ] 边界情况覆盖
- [ ] 性能测试通过
- [ ] 测试覆盖率高
