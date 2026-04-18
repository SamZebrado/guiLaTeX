# Qt GIF 录制最终说明

日期：2026-04-18

## 说明

由于当前环境没有图形界面，无法直接录制 Qt GIF。本文件提供了详细的录制指南，供真人录屏时使用。

---

## 一、Qt 主 GIF（10–15 秒）

### 目标文件
- `release_public/assets/qt_demo.gif`

### 推荐链路（10–15 秒）

1. **启动 Qt 应用**（1 秒）
   - 点击应用图标启动
   - 等待窗口完全加载

2. **展示界面**（1 秒）
   - 让观众看清整体布局
   - 左侧画布 + 右侧属性面板
   - 顶部工具栏分组清晰可见

3. **选中一个元素**（0.5 秒）
   - 点击画布上的标题元素
   - 高亮显示选中状态

4. **修改属性**（2 秒）
   - 点击右侧属性面板的旋转输入框
   - 输入 45 度
   - 按回车或点击其他地方确认

5. **展示画布变化**（1 秒）
   - 停顿让观众看清旋转效果
   - 元素确实旋转了 45 度

6. **复制/粘贴**（3 秒）
   - 点击编辑菜单 → 复制
   - 点击编辑菜单 → 粘贴
   - 观察新元素出现并偏移

7. **停顿展示结果**（2–3 秒）
   - 让观众看清最终效果
   - 两个元素，一个旋转 45 度，一个是新复制的

### 第二优先链路（如果主 GIF 太短）

在上述第 7 步之后添加：

8. **导出 LaTeX**（1.5 秒）
   - 点击文件菜单 → 导出 LaTeX
   - 选择保存位置（快速点击确定）
   - 停顿 0.5 秒

### 录制要求
- 录制区域只包含 Qt 窗口
- 窗口大小建议：1200x800
- 右侧属性面板必须清楚可见
- 鼠标动作慢一点，每步之间停顿 0.5–1 秒
- GIF 时长控制在 10–15 秒
- 不要录到桌面其他隐私信息

### 不要录这些内容
1. 不要把 PDF 导出当主卖点
2. 不要把 blocked 功能录进去
3. 不要把"还没实现的菜单项"录得像已完成
4. 不要录一堆内部证据文件列表
5. 不要暗示"最终桌面版已完成"

---

## 二、可选补充 GIF：roundtrip

### 目标文件
- `release_public/assets/qt_roundtrip.gif`

### 推荐内容（15–20 秒）

1. **选中元素**（0.5 秒）
   - 点击标题元素

2. **改属性**（1.5 秒）
   - 修改旋转角度为 30 度
   - 停顿 0.5 秒

3. **导出 conforming tex**（2 秒）
   - 点击文件菜单 → 导出 LaTeX
   - 保存为 "demo_roundtrip.tex"
   - 打开文件，快速展示包含 IR 元数据

4. **导入刚才导出的 tex**（3 秒）
   - 点击文件菜单 → 导入 LaTeX
   - 选择刚才导出的 "demo_roundtrip.tex"
   - 停顿观察元素被导入

5. **展示恢复结果**（2 秒）
   - 选择导入的元素
   - 在属性面板验证属性正确

### 注意事项
- 这里要诚实
- 不要暗示 PDF 主路径已经完成
- 不要暗示 font family gap 已解决
- 不要说所有字段完全保住
- 如果字体确实不对，可以快速指出来

---

## 三、推荐录制工具

### macOS
- **QuickTime Player**：内置，简单易用
- **OBS Studio**：免费，功能强大
- **Kap**：轻量级 GIF 录制工具

### Windows
- **OBS Studio**：免费，功能强大
- **LICEcap**：轻量级 GIF 录制
- **ShareX**：免费，功能全面

### Linux
- **OBS Studio**：免费，功能强大
- **Peek**：轻量级 GIF 录制
- **SimpleScreenRecorder**：简单易用

---

## 四、Storyboard 备选方案

如果 GIF 录制困难，可以制作故事板（storyboard）。

### 目标目录
- `release_public/assets/qt_demo_storyboard/`

### 截图列表
1. `01_startup.png` - Qt 应用启动，界面完整展示
2. `02_select_element.png` - 选中标题元素
3. `03_modify_rotation.png` - 在属性面板修改旋转角度为 45 度
4. `04_rotation_result.png` - 元素旋转后的效果
5. `05_copy.png` - 点击复制菜单
6. `06_paste.png` - 点击粘贴菜单
7. `07_final_result.png` - 最终效果展示

### Storyboard README
创建 `release_public/assets/qt_demo_storyboard/README.md`：

```markdown
# Qt Demo Storyboard

这个目录包含 Qt 演示的故事板截图，可以用于制作 GIF 或视频。

## 截图说明

1. 01_startup.png - Qt 应用启动，界面完整展示
2. 02_select_element.png - 选中标题元素
3. 03_modify_rotation.png - 在属性面板修改旋转角度为 45 度
4. 04_rotation_result.png - 元素旋转后的效果
5. 05_copy.png - 点击复制菜单
6. 06_paste.png - 点击粘贴菜单
7. 07_final_result.png - 最终效果展示

## 推荐流程

按照截图顺序依次展示，每个截图停留 0.5–1 秒，可配合简单的文字说明。
```

---

## 五、注意事项

### 要诚实
- 不要说 UI 是最终版
- 不要说所有功能都已实现
- 不要说没有任何问题
- 不要暗示 v1 已经完成

### 要留有余地
- 可以说"已进入 v1-candidate 阶段"
- 可以说"核心功能已验证"
- 可以说"支持基本的编辑和导出"

### 技术细节
- 导出使用：normalize_qt_model_to_ir + export_ir_to_latex
- 导入使用：import_own_exported_tex_to_ir
- IR 元数据：包含 BEGIN_IR_METADATA 和 END_IR_METADATA
- Canonical Pack：所有验证材料固定在 docs/contest_evidence/qt_canonical_pack/ 目录

---

## 六、资源文件位置

### Canonical Pack（已准备好）
- `docs/contest_evidence/qt_canonical_pack/qt_canonical_source_model.json`
- `docs/contest_evidence/qt_canonical_pack/qt_canonical_normalized_ir.json`
- `docs/contest_evidence/qt_canonical_pack/qt_canonical_exported.tex`
- `docs/contest_evidence/qt_canonical_pack/qt_canonical_imported_ir.json`
- `docs/contest_evidence/qt_canonical_pack/qt_canonical_roundtrip_diff_report.json`
- `docs/contest_evidence/qt_canonical_pack/qt_canonical_handoff_readme.md`
- `docs/contest_evidence/qt_canonical_pack/qt_canonical_final_caliber.json`

### 演示准备文档
- `docs/release/qt_demo_ready_list.md`
- `docs/release/qt_demo_shot_list.md`
- `docs/release/qt_public_status.md`
- `docs/release/qt_gif_recording_final.md`（本文件）
