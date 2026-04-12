# Qt Agent Guard - Qt 线开发规范

## 版本信息
- **版本**: 1.0
- **最后更新**: 2026-04-12
- **更新者**: Qt Agent

## 核心规则

### 1. 最新用户反馈优先原则
**规则ID**: `latest-user-feedback-overrides`
- 最新用户手测结果高于上一轮的判断
- 用户明确说"还在/不对"，就不能继续沿用"已修复"
- 必须以用户实际测试结果为准，而非代码层面的修改

### 2. 证据优先修复原则
**规则ID**: `evidence-first-fix`
- 代码修改不等于问题修复
- 测试路径不对，测试通过也不等于用户问题消失
- 结论必须明确区分：
  - `code-level changed`: 代码已修改，但未验证
  - `executed and verified`: 已执行并验证通过
  - `still needs user verification`: 仍需用户手动验证

### 3. GUI 端到端验证保障
**规则ID**: `gui-e2e-guard`
- import 成功、启动成功、日志打印、单元测试通过，不等于用户级 GUI 问题已解决
- Qt 线要尽量靠近真实用户路径，做不到就明确 blocked
- 必须进行真实用户操作路径的测试

### 4. 真实路径测试原则
**规则ID**: `real-path-test-only`
- 测试优先覆盖真实问题链路
- 尤其优先覆盖 MainWindow / create_initial_pdf / startup path 等真实入口
- 不要用绕开的简化路径宣布 duplication 已解决
- 测试必须模拟用户实际使用场景

### 5. 手动操作需求声明
**规则ID**: `manual-action-needed`
- 需要用户启动 GUI、手动拖动、查看日志、确认字体、确认颜色选择器、确认旋转入口时，最后必须单列 `MANUAL ACTION NEEDED`
- 明确列出需要用户操作的步骤和预期结果

### 6. UI 语义契约
**规则ID**: `ui-semantic-contract`
- 保存 / 导出 PDF / 导出模型 JSON / 预览 的语义必须明确
- 按钮名字与真实行为必须一致
- 功能未实现前，按钮应禁用或隐藏

### 7. 字体安全默认原则
**规则ID**: `font-safety-default`
- 默认字体列表只保留开源 / 免费可商用字体
- 系统字体 / 付费字体不应默认出现在列表里
- 若未来保留，需要标注"需用户自行确认授权"
- 推荐默认字体：
  - Noto Sans SC
  - Source Han Sans SC
  - Inter
  - Noto Sans
  - Sans Serif

### 8. 阻塞后打包原则
**规则ID**: `blocked-then-pack`
- 如果 duplication 或其它核心 GUI bug 连续多轮仍未压实，就切换到 blocked 模式
- 必须真实生成 zip，而不是只在总结里说"已准备"
- 准备清晰的问题描述、复现步骤和当前状态

## 核心功能验证标准

### 9.1 启动与初始化
- ⚠️ 程序正常启动（当前重点验证）
- ⚠️ 初始场景正确加载
- ⚠️ 无 console 错误或警告

### 9.2 Duplication 检测
- ⚠️ 启动后只有 5 个唯一对象
- ⚠️ 拖动一次后 object_count 仍为 5
- ⚠️ duplicate_found 为 False

### 9.3 颜色选择器
- ⚠️ 初始打开时圆色盘不是黑色
- ⚠️ 切换颜色选择方式后功能正常
- ⚠️ 颜色选择器 UI 完整可用

### 9.4 旋转功能
- ⚠️ 旋转入口明确可见
- ⚠️ 旋转手柄或按钮可交互
- ⚠️ 旋转后对象位置和大小正确

### 9.5 复制/粘贴
- ⚠️ 复制功能可用
- ⚠️ 粘贴出的对象有新 id
- ⚠️ 粘贴位置轻微偏移
- ⚠️ 保留大部分原属性

### 9.6 字体设置
- ⚠️ 默认字体列表只包含开源/免费可商用字体
- ⚠️ requested_font_stack 明确
- ⚠️ actual_font_family 正确
- ⚠️ fallback_used / exact_match 明确

## 验证流程

### 10.1 自动测试（如果可用）
1. 启动程序
2. 检查初始对象数量
3. 验证 duplication 检测
4. 测试复制/粘贴功能
5. 保存测试结果

### 10.2 手动测试路径
1. 启动程序：`python src/gui/main.py`
2. 检查初始场景是否有 5 个唯一对象
3. 拖动一个对象，检查是否有 duplication
4. 打开字体颜色选择器，检查初始状态
5. 查找旋转入口，确认是否可见
6. 测试复制/粘贴功能
7. 检查字体列表，确认只包含开源字体

## 证据收集
- 保存程序日志
- 保存测试结果
- 保存屏幕截图到 `docs/contest_evidence/screenshots/`
- 如果 blocked，生成 zip 包到明确路径

## 结论输出格式
- 明确区分已修复、部分缓解、未修复、已确认但 blocked
- 提供具体证据支持
- 列出需要用户手动验证的项目
- 提供 MANUAL ACTION NEEDED 部分
- 如果生成 zip，明确指出路径

## 适用范围
- 本规范适用于 Qt 线所有开发和测试活动
- 所有 Qt 相关的修复和功能实现必须遵循本规范
- 验证结果必须符合本规范的要求
