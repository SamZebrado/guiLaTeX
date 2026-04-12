# Group Transform Semantics v0.1

## 1. Single Object Rotation 定义

**Single Object Rotation**：单个对象独立旋转，每个对象都有自己独立的 `rotation` 字段。

- **IR 字段**：每个元素的 `rotation` 属性
- **单位**：度（degree）
- **正方向**：顺时针
- **旋转中心**：元素的左上角（由 x, y 定义）

## 2. Multi-select / Group Rotation 与 Independent Rotation 的区分

### 2.1 Group Rotation（组旋转）
- **定义**：多个对象作为一个整体围绕某个共同中心点旋转
- **语义**：旋转后，对象之间的相对位置关系保持不变
- **当前 IR 支持**：❌ **不支持**
- **原因**：当前 IR 没有 `group_id` 或 `group_rotation` 等字段，无法表达组关系和组旋转

### 2.2 Independent Rotation（独立旋转）
- **定义**：多个对象各自独立旋转，每个对象有自己的 `rotation` 值
- **语义**：旋转后，对象之间的相对位置关系可能改变
- **当前 IR 支持**：✅ **支持**
- **方式**：每个元素独立设置 `rotation` 字段

## 3. 当前 IR 能表达什么，不能表达什么

### 3.1 当前 IR 能表达
- ✅ 单个对象的独立旋转
- ✅ 多个对象各自独立旋转（每个对象有自己的 rotation）
- ✅ 图层顺序（通过 layer 字段）
- ✅ 基本几何属性（x, y, width, height）
- ✅ 基本字体和颜色属性

### 3.2 当前 IR 不能表达
- ❌ 组关系（没有 group_id 字段）
- ❌ 组旋转（没有 group_rotation 或 pivot 字段）
- ❌ 旋转中心点自定义（固定为元素左上角）
- ❌ 变换矩阵（没有 transform_matrix 字段）
- ❌ 剪切/斜切变换
- ❌ 缩放变换（没有 scale 字段）

## 4. 当前如果前端只支持"多个对象各自旋转"，应如何表述

如果前端实现的是"多个对象各自独立旋转"（Independent Rotation），而不是"组旋转"（Group Rotation），应该明确表述为：

- **前端表述**："多选后独立旋转" 或 "每个对象独立设置旋转角度"
- **不要表述**："组旋转"、"整体旋转"、"围绕共同中心点旋转"
- **用户期望管理**：明确告知用户，多选后旋转是每个对象各自旋转，不是作为一个整体围绕某个点旋转

## 5. 哪些情况 roundtripability 需要降级为 partial / unsupported

### 5.1 完全支持（full）
- 单个对象独立旋转
- 多个对象各自独立旋转
- 图层顺序
- 基本几何属性
- 基本字体和颜色属性

### 5.2 部分支持（partial）
- 文本布局：文本换行、行间距、字间距可能与原设计有差异
- 字体 fallback：字体不可用时可能导致布局变化
- 旋转精度：旋转角度可能存在微小误差

### 5.3 不支持（unsupported）
- 组旋转（group rotation）
- 自定义旋转中心点
- 变换矩阵
- 剪切/斜切变换
- 缩放变换
- 多页文档（当前 page 字段固定为 1）

## 6. 类型词表策略

### 6.1 Core Canonical 类型表
**仅支持以下类型**：
- `title`、`author`、`paragraph`、`textbox`、`equation`、`image`

### 6.2 Web 兼容别名
**仅支持以下别名**：
- `body` → `paragraph`
- `formula` → `equation`

### 6.3 实现策略
- **第一层**：`normalize_web_model_to_ir` 自动映射别名到 canonical 类型
- **第二层**：`validate_ir_roundtripability` 只接受 canonical 类型
- **第三层**：`export_ir_to_latex` 只处理 canonical 类型

### 6.4 未知别名处理
- 未知别名 **不会** 被静默归一化
- 未知别名会在验证阶段返回 `partial` 支持
- 未知别名 **不能** 穿透到 exporter，exporter 会明确报错
- 必须使用 canonical 类型或已定义的别名

### 6.5 防漂移措施
- 禁止新增别名
- 所有别名映射必须在 `_convert_web_element` 中明确定义
- 必须通过回归测试验证

## 7. 版本历史

- **v0.1 (2026-04-12)**：初始版本，定义基本语义
- **v0.1.1 (2026-04-12)**：添加类型词表策略和 Web 兼容别名映射
