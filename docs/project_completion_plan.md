# guiLaTeX 项目完成定义与阶段规划（当前收口版）

## 0. 这份文档是干什么的

这份文档用于把项目从"边开发边想"切换到"分阶段完成"的状态，避免目标无限抬高，导致一直觉得"还没做完"。

它主要回答四个问题：

1. **什么叫"基本能用"**
2. **什么叫"终极完成"**
3. **Web / Qt / Core 三条线接下来各自做什么**
4. **哪些东西现在该做，哪些东西应该延后**

---

## 1. 项目的真实长期目标

这个项目的长期目标，不只是"做一个自己的 LaTeX 编辑器"，而是：

> 做一套**人类与 agent 可以共同操作的 LaTeX 可视化编辑协作协议**。

换句话说，最终希望做到：

- 人可以通过可视化界面编辑对象
- agent 可以通过结构化格式或符合规范的 LaTeX 参与编辑
- 系统能在对象模型、IR、LaTeX、PDF 之间尽量稳定地转换
- 对于符合规范的 LaTeX，系统能检测其是否"可编辑回读"
- 如果不符合规范，系统能通过检测接口给出结构化反馈，提示 agent 修正

这意味着最终项目的重心不是"某一个 GUI"，而是：

1. **对象编辑层**
2. **共享 IR / 导出内核**
3. **符合规范的 LaTeX 风格与校验机制**
4. **回读与可编辑性检测**

---

## 2. 不要再把"完成"定义得太大：分成两个版本

### 2.1 完成定义 v1：自家闭环"基本能用"版

#### v1 的目标

这个版本只追求：

- Web / Qt 至少有一个前端达到**基本能用**
- 用户可以通过 GUI 对对象进行基本编辑
- 对象可导出到共享 IR
- 共享 IR 可导出到 LaTeX / PDF
- 系统能够重新读取**本工具自己导出的、符合规范的 LaTeX**，并恢复为可编辑对象
- 几何关系尽量一致，不追求任意第三方 LaTeX 的完美兼容

#### v1 必须包含的能力

**编辑器基础能力**

- 实时更新与查看
- 选择对象
- 拖动对象
- 旋转对象
- 基本多选
- 基本分组
- 复制 / 粘贴
- 删除
- 撤销 / 重做（至少单步到多步基本可用）

**对象类型**

- 文本 / 文本框
- 段落
- 公式
- 图片

**导出能力**

- 导出 IR
- 导出 LaTeX
- 导出 PDF

**回读能力**

- 至少支持"本工具自己导出的符合规范的 LaTeX"回读
- 回读后恢复成基本一致的可编辑对象

**证据要求**

- Web 至少有浏览器级自动测试覆盖关键交互
- Qt 至少有 ui_smoke / core_smoke / render_evidence 三层证据
- Core 至少有 golden sample + regression sample + validation status

#### v1 不强求的内容

- 任意第三方 LaTeX 完整可编辑导入
- 像素级一模一样的 PDF
- 高级复杂排版的完美 roundtrip
- 任意宏包与任意自定义命令的可靠支持

#### 对 v1 的现实判断

只要收紧目标到这里，项目是**可做完**的，而且不是研究级不可能任务。

---

### 2.2 完成定义 v2：增强版 / 终极版

#### v2 的目标

在 v1 基础上，继续追求：

- 第三方 agent 能根据本项目规范直接产出"可编辑 LaTeX"
- 系统能检测一份 LaTeX 是否符合本项目的可编辑风格
- 系统能对不符合规范的地方给出结构化反馈
- 支持部分第三方 LaTeX 导入
- 进一步提高 PDF 视觉一致性与 roundtrip 稳定性

#### v2 可能包含的能力

- Conforming LaTeX Profile（符合本项目风格的 LaTeX 子集）
- Profile Validator / Validation API
- 组级变换语义（整体旋转 / 各自旋转）
- 受限子集的第三方 LaTeX 导入
- 更强的文本布局与字体一致性策略

#### 对 v2 的现实判断

v2 不是"顺手加一点"，而是项目的第二阶段，应该单独规划。

---

## 3. 当前三条线的角色定位

### 3.1 Web：测试前线 + UI 样板 + 外部兼容试验场

#### 当前定位

Web 现在最适合承担：

1. **统一 UI 模式的样板**
2. **浏览器级自动测试主阵地**
3. **Core 导出链接入的第一实验场**
4. **将来用于测试第三方 agent 产物的外勤站**

#### 当前已经具备的基础

- 顶部工具栏 + 右侧属性面板的统一模式
- Playwright 级回归
- Export IR
- 基本对象编辑
- 已有 commit 和证据链

#### Web 下一步最重要的事

1. **右侧工具栏 / 属性面板支持滚轮滚动**
2. **开始真实接 Core，导出 `.tex`**
3. **把 Web -> IR -> Core -> tex 路径做成回归链**
4. **为未来的 Profile Validator 测试预留接口**
5. **继续补分组整体旋转的真实交互与自动测试**

#### Web 不应再优先做的事

- 再发明一套新 UI
- 继续做与 Core 无关的功能花活
- 继续扩大量纯前端功能，但不推进导出链

---

### 3.2 Qt：桌面原型 + 相对完整的对象编辑端

#### 当前定位

Qt 更适合承担：

1. **更完整的桌面对象编辑原型**
2. **更像"正式编辑器"的交互骨架**
3. **Core 接入前的本地工作站版本**

#### 当前已经具备的基础

- duplication 解决并留档
- rotation 有离屏证据
- Qt -> Core smoke test 已正式化
- IR / tex 输入输出证据已落地
- 复制 / 粘贴可用
- 字体列表已安全化

#### Qt 下一步最重要的事

1. **跟进 Web 的统一 UI 模式 v1**
2. **把 Qt 的 ui_smoke / core_smoke / render_evidence 三层正式化**
3. **继续准备正式接 Core**
4. **补最小可用编辑器体验，而不是继续盲目扩功能**

#### Qt 不应再优先做的事

- 大量继续发明独立于 Web 的 UI 模式
- 继续大规模扩新功能
- 抢着定义导出协议
- 再单独搞一套和 Core 脱节的导出格式

---

### 3.3 Core：共享导出内核 + 规范中心 + 检测官

#### 当前定位

Core 现在不应该只被看成"导出器"，而应该被看成：

1. **共享导出内核**
2. **Conforming LaTeX 风格规范中心**
3. **验证 / 反馈接口的提供者**

#### 当前已经具备的基础

- Export IR
- LaTeX 导出器
- golden sample
- regression sample
- quickstart / sample index / validation status
- normalize / export API

#### Core 下一步最重要的事

1. **继续写 Conforming LaTeX Profile**
2. **定义 group transform semantics**
3. **提供 validate_tex_profile / validate_roundtripability 级别的检测接口**
4. **继续补 regression sample**
5. **让 Web 可以拿第三方或 agent 生成的 `.tex` 来跑兼容性检查**

#### Core 不应再优先做的事

- 无限增加抽象设计文档而不落到 validator
- 再发明新字段但不服务实际接入
- 抢着做 UI

---

## 4. 目前距离"真正完成"的判断

### 4.1 如果按 v1（自家闭环基本能用）算

#### 判断

项目已经**不算离得很远**。

#### 还差的大头

1. Web 或 Qt 至少一端把"编辑器体验"推进到更稳
2. 真正打通：
   - model -> IR
   - IR -> tex
   - tex -> 本项目规范回读
3. 分组 / 整体旋转 / 撤销重做做成稳定主链
4. Core 的 Profile 与 Validator 起步

#### 粗略判断

如果周末推进、目标不继续膨胀，v1 是现实可达的。

---

### 4.2 如果按 v2（包含第三方 LaTeX 导入）算

#### 判断

还很远。

#### 最远的不是 GUI，而是：

1. 第三方 LaTeX 导入
2. 导出的 PDF 与原设计一比一
3. 回读任意 LaTeX 时恢复可编辑对象
4. 字体 / 换行 / 公式 / 旋转 / 图层在 LaTeX 里的高度一致性

#### 关键认知

"支持导入第三方 LaTeX"不是小功能，而是一个单独的大主题。

---

## 5. 当前最推荐的路线：先彻底打通"自家闭环"

### 5.1 最近目标

优先打通这条链：

> GUI 对象编辑 -> 导出 IR -> Core 导出 tex / pdf -> 回读本工具自己导出的 conforming tex -> 恢复可编辑对象

只要这条链通了，项目就真的成立了。

### 5.2 为什么这条链最关键

因为这条链一旦通了：

- 项目不是"能画界面"
- 也不是"能导出一点 tex"
- 而是变成了**真正能工作的编辑闭环**

---

## 6. 关于"分组整体旋转"的当前结论

你特别提到这点，这个判断是对的：

> 目前"分组功能"还没看到真正的"整体旋转"。

这不是小问题，因为它关系到：

- 组语义是否明确
- 几何关系是否稳定
- 将来 IR / Core 是否能表达组变换

### 建议

Core 需要尽快定义两种语义之一，或者两者都支持：

1. **group rotation** — 围绕组中心旋转
2. **independent rotation** — 多个对象各自绕自己中心旋转

如果 IR 不先定，Web 和 Qt 后面容易各写各的。

---

## 7. Conforming LaTeX Profile：为什么必须做

如果未来真的希望"人和 agent 一起写 LaTeX"，那不能指望所有第三方 agent 自由发挥。

必须提供一份明确的风格规范，例如：

- 文档结构怎么写
- 元数据怎么写
- 对象定位命令放在哪个单独小节
- 图层如何表示
- 旋转如何表示
- 图片 / 公式 / 字体推荐怎么写
- 哪些写法保证可编辑回读
- 哪些写法只保证可编译，不保证回读

### 这份文档建议文件名

`docs/export_core_conforming_latex_profile.md`

---

## 8. Validator：为什么这是第三方接入真正的关键

只给风格指南还不够，系统还必须能"检查"。

最小应该有两个函数：

```python
validate_tex_profile(tex_text: str) -> dict
validate_ir_roundtripability(ir_data: dict) -> dict
```

### 它们要能回答的问题

- 这份 tex 是否符合 profile
- 哪些地方不符合
- 严重程度是什么
- 哪些地方会影响回读
- 给 agent 什么修复建议
- 结果最好是机器可读 JSON

这样第三方 agent 才能自动接反馈继续修。

---

## 9. 建议新增的文件

### Core 侧

- `docs/export_core_conforming_latex_profile.md`
- `docs/export_core_group_transform_semantics.md`
- `docs/export_core_validator_api.md`

### Web / 测试侧

- `tests/web_profile_regression/`
- `tests/core_profile_validation/`

---

## 10. 推荐的测试分层

### 10.1 Web 测试分层

| 层级 | 覆盖范围 |
|------|----------|
| **browser_regression** | 点击是否瞬移；多选旋转是否作用于多个对象；导出 IR 是否存在；将来导出 tex 后可继续接 profile validator |
| **profile_regression** | 自家导出的 tex 是否符合 Conforming Profile；第三方 / agent 生成的 tex 是否违反 profile；验证错误是否能结构化返回 |

### 10.2 Qt 测试分层

| 层级 | 覆盖范围 |
|------|----------|
| **ui_smoke** | 顶部工具栏是否完整；左画布 / 右面板是否成立；中文标签是否一致 |
| **core_smoke** | Qt model -> IR；IR -> tex；关键字段是否存在 |
| **render_evidence** | rotation 离屏 before / after / diff；duplication 是否保持为 5；copy/paste 是否新 id + 偏移 |

### 10.3 Core 测试分层

| 层级 | 覆盖范围 |
|------|----------|
| **exporter_regression** | golden sample / regression sample 是否稳定导出 |
| **profile_validation** | conforming tex 是否通过；non-conforming tex 是否给出明确反馈 |
| **roundtrip_regression** | 自家闭环是否稳定 |

---

## 11. 当前建议的开发优先级

| 优先级 | 内容 |
|--------|------|
| **第一优先** | 把"自家闭环"打通：Web / Qt 任一端编辑 -> 导出 IR -> Core 导出 tex / pdf -> 回读 conforming tex |
| **第二优先** | Core 推进：Conforming Profile、Validator、group transform semantics |
| **第三优先** | Web 继续：右侧面板滚轮滚动、接 Core 导出 .tex、作为第三方 / agent 输出测试站 |
| **第四优先** | Qt 跟进：统一 UI 模式、正式接 Core、基本可用编辑器体验 |
| **最后优先** | 第三方任意 LaTeX 导入 |

---

## 12. 当前不建议做的事

- 不要继续把"完成"的定义抬高
- 不要先去啃任意第三方 LaTeX 完整导入
- 不要让 Web / Qt / Core 同时继续无限扩功能
- 不要把"有控件 / 有字段 / 有分支"写成"已经完成"
- 不要忽视自动测试和证据链

---

## 13. 对当前阶段的简短结论

- 项目离 **v1（自家闭环基本能用）**：**不算太远**
- 项目离 **v2（支持第三方 LaTeX 的增强版）**：**还很远**

当前最值得做的事，不是继续把需求无限抬高，而是：

> 把"对象编辑 -> IR -> tex/pdf -> conforming tex 回读"这条链彻底打通。

这条一旦打通，项目就真正有意义了。

---

## 14. 对 Web 的立即新增需求（来自最新手测反馈）

### 14.1 右侧工具栏 / 属性面板要支持滚轮滚动

**要求：**

- 鼠标滚轮可上下滚动
- 选项多时不被截断
- 窄宽度下仍可访问

### 14.2 Web 需要开始与 Core 对接

当前不能停留在只导出 IR，下一步应该推进到：

1. Web model -> IR
2. 调 Core：
   - `normalize_web_model_to_ir(...)`
   - `export_ir_to_latex(...)`
3. 真实导出 `.tex`
4. 保存输出样例与日志
5. 给后续 conforming profile / validator 留接口
