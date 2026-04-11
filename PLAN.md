# guiLaTeX 项目计划

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

**最后更新**: 2026-04-04  
**更新者**: Planner Agent
