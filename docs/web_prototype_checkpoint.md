# Web 原型检查点 - 2026-04-11

## 目标
验证 "web 是否更适合 guiLaTeX 这类可视化微调编辑器" 的可行性，通过一个最小、可运行、可截图、可手动演示的 Web 原型。

## 当前状态：收口提交轮 - 2026-04-11

### 本轮唯一目标
把已跑通的 Playwright regression、统一 UI 模式 v1、Export IR 导出能力，整理成可重复执行、可留证、可提交的稳定基线。

---

## 已完成的最小闭环

### 1. 统一 UI 模式 v1
- ✅ 顶部主工具栏，中文标签，分组清晰：
  - 文件：打开项目 / 保存项目 / 导出截图 / 导出 IR
  - 编辑：复制 / 粘贴 / 删除
  - 排列：上移 / 下移 / 移到顶部 / 移到底部 / 图层编号变整数
  - 视图：重置演示 / 显示调试
- ✅ 主区：中间为画布，右侧固定属性面板
- ✅ 右侧属性面板分组：
  - 选中信息
  - 内容（仅单选时正文可编辑）
  - 几何（x/y/宽/高/旋转/图层编号）
  - 字体（中文字体 / 英文字体 / 字号）
  - 对象专属属性
  - 模型预览
  - 调试信息（默认折叠）
- ✅ 面向用户界面全部中文
- ✅ 窄宽度下仍能访问关键按钮（1200px 以下垂直布局，700px 以下画布缩小）

### 2. 用户交互
- ✅ 可以选中所有类型的元素
- ✅ 可以拖动所有类型的元素改变位置
- ✅ 可以修改文本类元素的内容
- ✅ 可以修改文本类元素的字号
- ✅ 可以重置演示到初始状态
- ✅ 文本框（textbox）支持 resize 功能
- ✅ 图片元素支持 resize 功能
- ✅ 旋转手柄已添加（视觉占位）
- ✅ 删除按钮已添加
- ✅ 选中信息显示已添加
- ✅ 几何输入框已添加（x/y/宽/高）

### 3. 内部模型
- ✅ 内部模型作为 source of truth
- ✅ 画布显示来自模型
- ✅ 文本/字号/位置的变化都先改模型，再反映到界面
- ✅ 模型包含所需字段：id, type, content, x, y, fontSize, selected
- ✅ 图片和文本框元素包含 width 和 height 字段
- ✅ 暴露到 window 供 Playwright 测试

### 4. 实时更新
- ✅ 画布立即更新
- ✅ 内部模型同步更新
- ✅ 模型 JSON 预览实时更新

### 5. 点击瞬移问题 - 已回归通过
- ✅ Playwright 验证通过
- ✅ 点击前位置: (152, 420)
- ✅ 点击对象中心后: (152, 420)
- ✅ 点击对象偏右下后: (152, 420)
- ✅ 三次点击位置完全一致，无瞬移
- ✅ 证据文件：web_regression_v4_click_teleportation_result.json, web_regression_v4_click_teleportation.png

### 6. 多选旋转功能 - 已回归通过
- ✅ Playwright 验证通过
- ✅ 旋转前: [ { id: '1', rotation: 0 }, { id: '2', rotation: 0 } ]
- ✅ 旋转后: [ { id: '1', rotation: 45 }, { id: '2', rotation: 45 } ]
- ✅ 两个对象都从 0° 旋转到 45°
- ✅ 证据文件：web_regression_v4_multi_select_rotation_result.json, web_regression_v4_multi_select_rotation.png

### 7. 字体栈
- ✅ 已更新为开源/免费可商用字体栈
- ✅ 优先支持中文显示：Noto Sans SC, Source Han Sans SC, Inter, Noto Sans, sans-serif
- ✅ 页面和控制台输出字体信息，包括请求的字体栈和实际使用的字体
- ✅ 支持中文字体和英文字体分别设置
- ✅ 移除了授权状态不稳妥的字体（PingFang SC, Microsoft YaHei, Arial）
- ✅ 默认字体列表只包含开源/免费可商用字体

### 8. 旋转功能
- ✅ textbox 和 image 都支持旋转功能
- ✅ 旋转入口明确可见（蓝色圆形旋转手柄，大小增大，添加阴影效果）
- ✅ 可以通过旋转手柄拖动旋转
- ✅ 可以通过旋转滑块调整角度
- ✅ 模型中有 rotation 字段记录角度
- ✅ 旋转角度范围限制在 -180° 到 180°
- ✅ 支持多选对象同时旋转（统一角度赋值）：已实现
  - 实现方案：更新了 startRotate 和 rotate 函数，使其作用于所有选中的元素
  - 验证状态：Playwright 回归通过

### 9. 对象上下顺序（z-order）
- ✅ 支持移到顶部、移到底部、上移、下移
- ✅ 统一使用 layerId 字段控制层级（数字越小越靠上）
- ✅ 渲染时按 layerId 排序
- ✅ 支持多选元素的层级操作

### 10. 图层雏形
- ✅ 对象有 layerId 字段
- ✅ 已初步建立文本层和图片层的结构
- ✅ 支持图层编号数值化输入
- ✅ 支持图层编号整数化功能

### 11. 多选功能
- ✅ 多选复选框现在真正生效
- ✅ 可以选择多个对象
- ✅ 多选后可以整体移动
- ✅ 多选后可以批量修改属性（旋转、字体大小、字体、图层编号）
- ✅ 多选状态有明确的视觉反馈（红色边框）

### 12. 导出 IR 功能 - 已回归通过
- ✅ 实现了 exportToIR() 函数，将 Web 模型映射到 Export IR 格式
- ✅ 导出按钮已更新，明确显示为"导出 IR"
- ✅ 导出的 IR 文件包含所有必需字段：id, type, content, page, x, y, width, height, rotation, layer, font_family_zh, font_family_en, font_size, color, visible
- ✅ 支持图层映射：Web 模型中 layerId 越小层级越高，Export IR 中 layer 越大层级越高
- ✅ 导出的 IR 文件为 JSON 格式，可直接被 ExportCore 使用
- ✅ 证据文件：web_regression_v4_export_ir_result.json

### 13. Playwright regression 固化
- ✅ 测试脚本路径：web_prototype/playwright_regression_test.js
- ✅ 启动服务器方式：无需服务器，直接打开 index.html
- ✅ 运行命令：cd web_prototype && node playwright_regression_test.js
- ✅ 输出文件路径：docs/contest_evidence/screenshots/
- ✅ 失败日志路径：docs/contest_evidence/screenshots/web_regression_v4_test_log.txt
- ✅ 测试日志：web_regression_v4_test_log.txt
- ✅ 初始页面截图：web_regression_v4_initial_page.png

---

## Web 原型结构

### 目录结构
```
web_prototype/
├── index.html                      # 主页面，包含完整的原型实现
├── playwright_regression_test.js     # Playwright 回归测试脚本
└── docs/contest_evidence/screenshots/  # 证据文件目录
    ├── web_regression_v4_initial_page.png
    ├── web_regression_v4_click_teleportation.png
    ├── web_regression_v4_click_teleportation_result.json
    ├── web_regression_v4_multi_select_rotation.png
    ├── web_regression_v4_multi_select_rotation_result.json
    ├── web_regression_v4_export_ir_result.json
    └── web_regression_v4_test_log.txt
```

### 技术栈
- **前端**: 纯 HTML, CSS, JavaScript
- **无依赖**: 不使用任何框架或库
- **轻量级**: 单文件实现，无需构建过程

---

## 自动化验证

### 状态
✅ 已实现并运行通过

### Playwright 测试内容
1. 点击瞬移问题回归测试：✅ 通过
2. 多选旋转功能回归测试：✅ 通过
3. Export IR 功能检查：✅ 通过

### 证据文件
- web_regression_v4_initial_page.png - 初始页面截图
- web_regression_v4_click_teleportation.png - 点击瞬移测试截图
- web_regression_v4_click_teleportation_result.json - 点击瞬移测试结果
- web_regression_v4_multi_select_rotation.png - 多选旋转测试截图
- web_regression_v4_multi_select_rotation_result.json - 多选旋转测试结果
- web_regression_v4_export_ir_result.json - Export IR 测试结果
- web_regression_v4_test_log.txt - 测试日志

---

## Web 路线优势

### 相比 Qt 路线的优势
1. **快速迭代**: 纯前端实现，无需编译，修改后立即生效
2. **跨平台**: 任何现代浏览器都可以运行，无需为不同平台构建
3. **轻量级**: 无需安装复杂的依赖和运行环境
4. **直观的 DOM 操作**: 对于可视化编辑场景，DOM 操作比 Qt 更直接
5. **丰富的 CSS 能力**: 可以更灵活地实现各种视觉效果和动画
6. **易于部署**: 可以直接部署到静态网站托管服务
7. **易于测试**: Playwright 等浏览器自动化测试工具成熟，易于使用

### 潜在优势
- **协作编辑**: 基于 Web 的架构更容易实现实时协作
- **扩展性**: 可以利用丰富的 Web 生态系统和库
- **移动设备支持**: 响应式设计可以支持平板等设备

---

## 未实现的功能

### 本轮未实现
- 后端服务
- 用户系统
- 数据库存储
- 真正的 PDF 解析
- 真正的 LaTeX 编译
- 完整多页管理
- 复杂样式系统
- 与 Qt 线的大量共享/重构
- 段落（paragraph）的完整 resize 功能

---

## 本轮结论

### 本轮已完成
1. ✅ 统一 UI 模式 v1 已稳定落地
2. ✅ Playwright regression 已固化（可重复执行、可留证、可提交）
3. ✅ 点击瞬移问题：回归通过
4. ✅ 多选旋转功能：回归通过
5. ✅ Export IR 功能：回归通过
6. ✅ 证据文件已完整保存

### 当前 Web 线最准确的里程碑表述
**已稳定落实统一 UI 模式 v1，固化了 Playwright 回归测试（点击瞬移、多选旋转、Export IR 都通过），证据文件已完整保存，达到可提交的稳定基线**。
