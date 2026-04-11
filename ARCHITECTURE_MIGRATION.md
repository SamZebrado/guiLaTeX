# guiLaTeX 架构迁移方案

## 当前架构问题清单

### 1. 数据模型问题
- **memory_elements 浅拷贝**: `self.memory_elements = self.text_elements.copy()` 只是浅拷贝，修改时可能产生别名问题
- **ID 不唯一**: `extract_text_elements()` 使用 `f'text_{i}'` 作为ID，跨页或重新加载时可能重复
- **缺少 dirty flag**: 虽然有 `is_dirty`，但没有细粒度的元素级 dirty 标记
- **缺少 original_source**: 无法追踪元素来源，不利于同步

### 2. 保存语义混乱
- **save_changes() 误导性**: 方法名暗示保存到PDF，实际只是打印日志
- **update_pdf_element() 空实现**: 有方法但无实际功能，造成误解
- **直接PDF编辑思维**: 代码仍倾向于直接修改PDF，而非内部模型驱动

### 3. 架构方向偏差
- **PDF-as-Canvas 过度依赖**: 把PDF作为实时编辑真相源，导致频繁磁盘操作
- **缺少内部模型层**: 没有清晰的 DocumentModel/PageModel/ElementModel 分层
- **PDF-to-LaTeX 过早实现**: 只有基础框架，不应作为近期主干

### 4. 代码质量问题
- **双轨制混乱**: `text_elements` 和 `memory_elements` 并存，逻辑复杂
- **选中状态管理**: 页面切换时属性面板/选中状态同步有问题
- **预览/导出语义不清**: 用户不清楚何时会触发PDF重新编译

## 最小迁移方案

### 阶段1: 建立内部模型 (核心)

#### 1.1 创建模型层
```
src/
├── model/
│   ├── __init__.py
│   ├── document.py    # DocumentModel
│   ├── page.py        # PageModel
│   └── element.py     # ElementModel
```

#### 1.2 ElementModel 设计
```python
@dataclass
class ElementModel:
    id: str                    # UUID，保证唯一
    type: str                  # 'text', 'image', 'formula', etc.
    content: str               # 文本内容或LaTeX代码
    x: float
    y: float
    width: float
    height: float
    font_size: float
    font_family: str = 'default'
    dirty: bool = False        # 是否被修改
    original_source: Optional[str] = None  # 来源追踪
    metadata: Dict = field(default_factory=dict)
```

#### 1.3 PageModel 设计
```python
@dataclass
class PageModel:
    id: str
    number: int
    elements: List[ElementModel] = field(default_factory=list)
    width: float = 595.0       # A4默认宽度 (points)
    height: float = 842.0      # A4默认高度 (points)
    dirty: bool = False
```

#### 1.4 DocumentModel 设计
```python
@dataclass
class DocumentModel:
    id: str
    title: str = "Untitled"
    author: str = ""
    pages: List[PageModel] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    dirty: bool = False
```

### 阶段2: 调整编辑逻辑

#### 2.1 修改 PDFPageWidget
- **移除**: `text_elements` 和 `memory_elements` 双轨制
- **使用**: 单一的 `page_model: PageModel` 
- **编辑操作**: 只修改 `page_model.elements`，不再直接操作PDF

#### 2.2 渲染流程调整
```python
def paintEvent(self, event):
    # 1. 渲染原始PDF背景（只读）
    painter.drawPixmap(0, 0, self.render_pdf_background())
    
    # 2. 渲染内部模型覆盖层
    self.render_model_overlay(painter)
    
    # 3. 渲染选中状态
    self.render_selection(painter)
```

### 阶段3: 明确保存语义

#### 3.1 重命名方法
- `save_changes()` → `apply_to_model()` 或移除
- `update_pdf_element()` → 移除或改为内部方法
- 新增: `generate_latex()` - 从模型生成LaTeX
- 新增: `preview_pdf()` - 编译并预览PDF
- 新增: `export_pdf()` - 导出最终PDF

#### 3.2 UI 调整
- "Save" 按钮 → "Apply" 或移除（实时应用到模型）
- "Preview" 按钮 → 明确触发LaTeX编译
- "Export" 按钮 → 导出最终文档

### 阶段4: 低磁盘开销预览

#### 4.1 策略
- **平时编辑**: 只更新内部模型和界面覆盖层，不触碰磁盘
- **预览时**: 调用 `generate_latex()` → `LaTeXEngine.compile()` → 显示PDF
- **缓存**: 使用临时目录，不写入项目目录

#### 4.2 临时文件管理
```python
# 使用系统临时目录，自动清理
with tempfile.TemporaryDirectory() as tmpdir:
    pdf_path = os.path.join(tmpdir, 'preview.pdf')
    engine.compile(latex_code, output_path=pdf_path)
    view_pdf(pdf_path)
```

### 阶段5: 暂缓PDF-to-LaTeX

#### 5.1 近期支持范围
- ✅ 从PDF提取简单文本元素 → 创建内部模型
- ✅ 从内部模型生成简化LaTeX
- ✅ LaTeX编译预览PDF

#### 5.2 不支持（本轮）
- ❌ 任意PDF的高质量逆向重建
- ❌ 复杂布局的精确还原
- ❌ 嵌入字体的处理

## 实施步骤

### Step 1: 创建模型层
1. 创建 `src/model/` 目录
2. 实现 `ElementModel`, `PageModel`, `DocumentModel`
3. 添加 UUID 生成和深拷贝支持

### Step 2: 修改 PDFPageWidget
1. 替换 `memory_elements` 为 `page_model`
2. 修改所有编辑方法，只操作模型
3. 调整渲染流程

### Step 3: 调整 MainWindow
1. 创建 `DocumentModel` 实例
2. 连接模型到PDFCanvas
3. 重命名保存相关方法

### Step 4: 更新 LaTeX Engine
1. 添加 `generate_from_model()` 方法
2. 优化临时文件处理
3. 移除直接PDF修改相关代码

### Step 5: 测试与文档
1. 添加模型层单元测试
2. 更新 STATUS.md
3. 更新 PLAN.md

## 预期改动文件

### 主要修改
- `src/model/` (新增目录)
- `src/gui/pdf_canvas.py` (大幅修改)
- `src/gui/main.py` (中等修改)
- `src/gui/properties.py` (轻度修改)
- `src/latex/engine.py` (轻度修改)
- `src/latex/pdf_reconstructor.py` (移除或简化)

### 文档更新
- `STATUS.md`
- `PLAN.md`
- `docs/architecture.md`

## 验证标准

### 模型层
- [ ] ElementModel 有唯一ID
- [ ] 深拷贝不会导致别名问题
- [ ] dirty flag 正常工作

### 编辑流程
- [ ] 选中、移动、缩放只改模型
- [ ] PDF背景只读，不修改
- [ ] 覆盖层正确显示模型状态

### 保存语义
- [ ] 没有误导性的 save_changes 命名
- [ ] Preview 明确触发编译
- [ ] Export 生成最终文件

### 磁盘开销
- [ ] 平时编辑不写磁盘
- [ ] 预览使用临时目录
- [ ] 临时文件自动清理

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 模型层引入复杂度 | 保持最小可用设计，不过度抽象 |
| 渲染性能下降 | 优化覆盖层绘制，必要时使用缓存 |
| 用户习惯改变 | 更新UI文案，提供清晰反馈 |
| 数据迁移问题 | 保留旧代码路径作为fallback |
