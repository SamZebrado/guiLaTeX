# Dual Agent Runs (2026-04-11 起)

## Web 侧新 Round

### 完成情况

1. **右侧属性面板滚动**：已落实
   - 属性面板内容过多时可滚动
   - 鼠标滚轮可以上下滚动
   - 窄宽度下仍可访问
   - Playwright 测试通过

2. **Playwright 回归测试**：全部通过
   - 点击对象中心后位置不变
   - 点击对象偏右下后位置不变
   - 多选两个对象后执行旋转，两个对象的 rotation 都变化
   - 导出 IR 按钮存在且结果包含关键字段
   - PDF 导出按钮存在且 print 路径仍可触发
   - 右侧属性面板可滚动

3. **Web 导出自己风格的 LaTeX**：已实现
   - Web model -> IR
   - 再走 Core 规定的 conforming profile / contract
   - 真实生成项目自己风格的 `.tex`

4. **Web 导入自己导出的 conforming LaTeX**：已实现基础功能
   - 实现了 `core_to_web_bridge.py` 脚本
   - 可解析项目自己导出的 conforming LaTeX 文件中的 IR 元数据
   - 转换为 Web 可编辑的模型格式
   - 保存为 JSON 文件后可通过 "打开项目" 功能导入

### 技术实现

- **右侧属性面板滚动**：通过 CSS `max-height: calc(100vh - 80px)` 和 `overflow-y: auto` 实现
- **LaTeX 导出**：通过 `web_to_core_bridge.py` 脚本调用 ExportCore 函数生成 LaTeX
- **LaTeX 导入**：通过 `core_to_web_bridge.py` 脚本解析 LaTeX 文件中的 IR 元数据并转换为 Web 模型
- **Playwright 测试**：增强了测试脚本，添加了属性面板滚动测试

### 验证结果

- **Playwright 测试**：所有 5 个测试用例全部通过
- **LaTeX 导出**：成功生成符合项目风格的 `.tex` 文件，包含完整的 IR 元数据
- **LaTeX 导入**：成功解析 LaTeX 文件并转换为 Web 模型
- **UI 一致性**：保持统一 UI 模式 v1

### 保存的证据文件

- `web_prototype/regression_test_output_v2.txt`
- `web_prototype/regression_test_results_v2.json`
- `web_prototype/regression_initial_page.png`
- `temp/web_to_core/web_real_export_output.tex`
- `temp/core_to_web/core_to_web_import_output.json`

### 下一步计划

1. 优化 LaTeX 导入体验，实现浏览器内直接导入
2. 增强 LaTeX 导出/导入的功能完整性
3. 进一步完善 UI 响应式设计
4. 增加更多 Playwright 测试用例