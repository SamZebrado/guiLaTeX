# ExportCore 接入速查表

## 快速接入

### Web 接入

**调用函数**：
```python
from export_core import normalize_web_model_to_ir, export_ir_to_latex
```

**最短接入路径**：
1. 准备 Web 模型
2. `ir_data = normalize_web_model_to_ir(web_model)`
3. `latex_content = export_ir_to_latex(ir_data)`
4. 保存结果

**输入样例文件路径**：
- Web 模型参考：`export_core/samples/golden_sample_ir.json`

**输出样例文件路径**：
- 生成的 LaTeX：`export_core/samples/golden_sample_ir.tex`

**最小 Smoke Test**：
```python
from export_core import normalize_web_model_to_ir, export_ir_to_latex

web_model = {
    "elements": [
        {
            "id": "test-1",
            "type": "textbox",
            "text": "测试文本",
            "x": 50,
            "y": 50,
            "width": 100,
            "height": 30,
            "rotation": 0,
            "layerId": 1,
            "fontSize": 12,
            "color": "#000000",
            "textAlign": "left",
            "visible": True
        }
    ]
}

try:
    ir_data = normalize_web_model_to_ir(web_model)
    latex_content = export_ir_to_latex(ir_data)
    print("✓ 成功")
except Exception as e:
    print("✗ 失败:", e)
```

**当前最关键的字段缺口**：
- `font_family_zh` 和 `font_family_en` 字段分离
- `page` 字段支持

---

### Qt 接入

**调用函数**：
```python
from export_core import normalize_qt_model_to_ir, export_ir_to_latex
```

**最短接入路径**：
1. 准备 Qt 模型
2. `ir_data = normalize_qt_model_to_ir(qt_model)`
3. `latex_content = export_ir_to_latex(ir_data)`
4. 保存结果

**输入样例文件路径**：
- Qt 模型参考：`export_core/samples/golden_sample_ir.json`

**输出样例文件路径**：
- 生成的 LaTeX：`export_core/samples/golden_sample_ir.tex`

**最小 Smoke Test**：
```python
from export_core import normalize_qt_model_to_ir, export_ir_to_latex

qt_model = {
    "elements": [
        {
            "id": "test-1",
            "type": "文本",
            "text": "测试文本",
            "x": 50,
            "y": 50,
            "width": 100,
            "height": 30,
            "rotation": 0,
            "layer": 1,
            "font_size": 12,
            "color": "#000000",
            "alignment": "left",
            "visible": True,
            "page": 1
        }
    ]
}

try:
    ir_data = normalize_qt_model_to_ir(qt_model)
    latex_content = export_ir_to_latex(ir_data)
    print("✓ 成功")
except Exception as e:
    print("✗ 失败:", e)
```

**当前最关键的字段缺口**：
- `font_family_zh` 和 `font_family_en` 字段分离

---

### 直接导出 IR

**调用函数**：
```python
from export_core import export_ir_to_latex
```

**输入样例文件路径**：
- IR JSON：`export_core/samples/golden_sample_ir.json`

**输出样例文件路径**：
- LaTeX 输出：`export_core/samples/golden_sample_ir.tex`
