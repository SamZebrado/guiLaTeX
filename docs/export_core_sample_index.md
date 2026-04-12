# ExportCore Sample 索引

## 样例列表

### 1. Golden Sample

**文件名**：
- IR: [export_core/samples/golden_sample_ir.json](export_core/samples/golden_sample_ir.json)
- LaTeX: [export_core/samples/golden_sample_ir.tex](export_core/samples/golden_sample_ir.tex)

**作用**：
- 完整功能演示样例
- 包含所有基本元素类型

**重点验证**：
- 标题、作者、段落、公式、图片的基本导出
- 基本几何属性（位置、尺寸）
- 基本字体属性

**适合参考**：
- Web ✅
- Qt ✅

---

### 2. Regression Sample 1 - Rotation

**文件名**：
- IR: [export_core/samples/regression_sample_1_rotation.json](export_core/samples/regression_sample_1_rotation.json)
- LaTeX: [export_core/samples/regression_sample_1_rotation.tex](export_core/samples/regression_sample_1_rotation.tex)

**作用**：
- 验证旋转功能
- 验证不同旋转角度的文本和图片

**重点验证**：
- 0度、15度、45度、90度旋转
- 旋转后的位置和尺寸
- 旋转后的图层顺序

**适合参考**：
- Web ✅
- Qt ✅

---

### 3. Regression Sample 2 - Layers

**文件名**：
- IR: [export_core/samples/regression_sample_2_layers.json](export_core/samples/regression_sample_2_layers.json)
- LaTeX: [export_core/samples/regression_sample_2_layers.tex](export_core/samples/regression_sample_2_layers.tex)

**作用**：
- 验证图层顺序
- 验证图层叠加效果

**重点验证**：
- 不同 layer 值的渲染顺序
- 图层叠加的视觉效果
- 数值越大层级越高

**适合参考**：
- Web ✅
- Qt ✅

---

### 4. Regression Sample 3 - Same Layer

**文件名**：
- IR: [export_core/samples/regression_sample_3_same_layer.json](export_core/samples/regression_sample_3_same_layer.json)
- LaTeX: [export_core/samples/regression_sample_3_same_layer.tex](export_core/samples/regression_sample_3_same_layer.tex)

**作用**：
- 验证同一图层多个元素
- 验证同一图层内的渲染顺序

**重点验证**：
- 多个元素同一 layer 值
- 同一图层内的元素顺序
- 颜色和对齐方式

**适合参考**：
- Web ✅
- Qt ✅

---

### 5. Regression Sample 4 - Fonts

**文件名**：
- IR: [export_core/samples/regression_sample_4_fonts.json](export_core/samples/regression_sample_4_fonts.json)
- LaTeX: [export_core/samples/regression_sample_4_fonts.tex](export_core/samples/regression_sample_4_fonts.tex)

**作用**：
- 验证中英文字体分离
- 验证字体属性导出

**重点验证**：
- font_family_zh 和 font_family_en 字段
- 中文字体和英文字体分别设置
- 混合文本的字体处理

**适合参考**：
- Web ✅
- Qt ✅

---

### 6. Regression Sample 5 - Rotation + Layers

**文件名**：
- IR: [export_core/samples/regression_sample_5_rotation_layer.json](export_core/samples/regression_sample_5_rotation_layer.json)
- LaTeX: [export_core/samples/regression_sample_5_rotation_layer.tex](export_core/samples/regression_sample_5_rotation_layer.tex)

**作用**：
- 验证旋转和图层同时存在的情况
- 验证复杂场景的组合效果

**重点验证**：
- 旋转角度不同，图层不同
- 低图层低旋转、低图层高旋转
- 高图层低旋转、高图层高旋转

**适合参考**：
- Web ✅
- Qt ✅

---

## 使用指南

### Web 开发者
1. 从 golden sample 开始，了解基本格式
2. 然后看 regression sample 1-3，了解基本功能
3. 最后看 regression sample 4-5，了解复杂场景

### Qt 开发者
1. 从 golden sample 开始，了解基本格式
2. 然后看 regression sample 1-3，了解基本功能
3. 最后看 regression sample 4-5，了解复杂场景
