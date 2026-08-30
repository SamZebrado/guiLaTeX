# ExportCore - 共享导出内核

from .ir_schema import ExportIR, ElementIR, SUPPORTED_TYPES, COORDINATE_SYSTEM
from .latex_exporter import LatexExporter

__all__ = [
    'ExportIR',
    'ElementIR',
    'SUPPORTED_TYPES',
    'COORDINATE_SYSTEM',
    'LatexExporter',
    'normalize_web_model_to_ir',
    'normalize_qt_model_to_ir',
    'export_ir_to_latex',
    'import_own_exported_tex_to_ir',
    'validate_tex_profile',
    'extract_embedded_ir_from_tex',
    'validate_ir_roundtripability'
]

def normalize_web_model_to_ir(web_model: dict) -> dict:
    """
    将 Web 模型标准化为 Export IR 格式
    
    Args:
        web_model: Web JSON 模型
    
    Returns:
        标准化后的 Export IR 格式
    """
    # 从 Web 模型中提取元素并转换为标准格式
    ir_elements = []
    
    if 'elements' in web_model:
        for web_element in web_model['elements']:
            ir_element = _convert_web_element(web_element)
            ir_elements.append(ir_element)
    
    return {
        'elements': ir_elements
    }

def _convert_web_element(web_element: dict) -> dict:
    """
    将单个 Web 元素转换为 IR 元素
    """
    # 类型映射：Web 类型 -> Core canonical 类型
    type_mapping = {
        'body': 'paragraph',
        'formula': 'equation'
    }
    
    element_type = web_element.get('type', 'textbox')
    canonical_type = type_mapping.get(element_type, element_type)
    
    return {
        'id': web_element.get('id', ''),
        'type': canonical_type,
        'content': web_element.get('text', web_element.get('content', '')),
        'page': web_element.get('page', 1),
        'x': web_element.get('x', 0),
        'y': web_element.get('y', 0),
        'width': web_element.get('width', 0),
        'height': web_element.get('height', 0),
        'rotation': web_element.get('rotation', 0),
        'layer': web_element.get('layerId', web_element.get('layer', 0)),
        'font_family_zh': web_element.get(
            'font_family_zh', web_element.get('chineseFont', 'SimSun')
        ),
        'font_family_en': web_element.get(
            'font_family_en', web_element.get('englishFont', 'Times New Roman')
        ),
        'font_size': web_element.get('fontSize', web_element.get('font_size', 12)),
        'color': web_element.get('color', '#000000'),
        'alignment': web_element.get('textAlign', web_element.get('alignment', 'left')),
        'visible': web_element.get('visible', True)
    }

def normalize_qt_model_to_ir(qt_model: dict) -> dict:
    """
    将 Qt 模型标准化为 Export IR 格式
    
    Args:
        qt_model: Qt 模型字典
    
    Returns:
        标准化后的 Export IR 格式
    """
    ir_elements = []
    
    if 'elements' in qt_model:
        for qt_element in qt_model['elements']:
            ir_element = _convert_qt_element(qt_element)
            ir_elements.append(ir_element)
    
    return {
        'elements': ir_elements
    }

def _convert_qt_element(qt_element: dict) -> dict:
    """
    将单个 Qt 元素转换为 IR 元素
    """
    return {
        'id': qt_element.get('id', ''),
        'type': _map_qt_type(qt_element.get('type', 'text')),
        'content': qt_element.get('text', qt_element.get('content', '')),
        'page': qt_element.get('page', 1),
        'x': qt_element.get('x', 0),
        'y': qt_element.get('y', 0),
        'width': qt_element.get('width', 0),
        'height': qt_element.get('height', 0),
        'rotation': qt_element.get('rotation', 0),
        'layer': qt_element.get('layer', 0),
        'font_family_zh': 'SimSun',
        'font_family_en': 'Times New Roman',
        'font_size': qt_element.get('font_size', 12),
        'color': _convert_qt_color(qt_element.get('color', '#000000')),
        'alignment': qt_element.get('alignment', 'left'),
        'visible': qt_element.get('visible', True)
    }

def _map_qt_type(qt_type: str) -> str:
    """
    映射 Qt 元素类型到 IR 元素类型
    """
    type_map = {
        '标题': 'title',
        '作者': 'author',
        '文本': 'paragraph',
        'text': 'paragraph',
        '公式': 'equation',
        'equation': 'equation',
        '图片': 'image',
        'image': 'image',
        'textbox': 'textbox'
    }
    return type_map.get(qt_type, 'paragraph')

def _convert_qt_color(qt_color) -> str:
    """
    转换 Qt 颜色格式为 HEX 格式
    """
    if isinstance(qt_color, str):
        return qt_color
    # TODO: 处理 QColor 转换为 HEX
    return '#000000'

def export_ir_to_latex(ir: dict) -> str:
    """
    将 Export IR 导出为 LaTeX
    
    Args:
        ir: Export IR 格式数据
    
    Returns:
        LaTeX 字符串
    
    Raises:
        ValueError: 如果发现未知类型
    """
    # 支持的 canonical 类型
    supported_types = {"title", "author", "paragraph", "textbox", "equation", "image"}
    
    # 类型 preflight 检查
    elements = ir.get("elements", [])
    for element in elements:
        element_type = element.get("type")
        if element_type not in supported_types:
            raise ValueError(f"Unknown element type: '{element_type}'. Only canonical types are supported: {supported_types}")
    
    exporter = LatexExporter()
    return exporter.export(ir)

def validate_ir_roundtripability(ir_data: dict) -> dict:
    """
    验证 IR 的 roundtripability（往返能力）
    
    Args:
        ir_data: Export IR 格式数据
    
    Returns:
        验证结果字典，包含 ok / supported / issues / severity / message
    """
    result = {
        "ok": True,
        "supported": "full",
        "issues": [],
        "severity": "low",
        "message": "IR 验证通过"
    }
    
    # 必需字段检查
    required_root_fields = ["elements"]
    for field in required_root_fields:
        if field not in ir_data:
            result["ok"] = False
            result["supported"] = "unsupported"
            result["issues"].append({
                "field": field,
                "severity": "critical",
                "message": f"缺少必需的根字段: {field}"
            })
            result["severity"] = "critical"
            result["message"] = "IR 缺少必需字段"
            return result
    
    elements = ir_data.get("elements", [])
    
    if not elements:
        result["ok"] = False
        result["supported"] = "partial"
        result["issues"].append({
            "field": "elements",
            "severity": "warning",
            "message": "elements 列表为空"
        })
        result["severity"] = "warning"
        result["message"] = "IR 包含空元素列表"
        return result
    
    # 支持的元素类型
    supported_types = {"title", "author", "paragraph", "textbox", "equation", "image"}
    
    # 每个元素的必需字段
    required_element_fields = [
        "id", "type", "content", "page", 
        "x", "y", "width", "height", 
        "rotation", "layer", "visible"
    ]
    
    for idx, element in enumerate(elements):
        element_id = element.get("id", f"element_{idx}")
        
        # 检查必需字段
        for field in required_element_fields:
            if field not in element:
                result["ok"] = False
                result["supported"] = "partial"
                result["issues"].append({
                    "element": element_id,
                    "field": field,
                    "severity": "error",
                    "message": f"元素 {element_id} 缺少必需字段: {field}"
                })
                if result["severity"] != "critical":
                    result["severity"] = "error"
        
        # 检查字段值的有效性
        # font_size 不能为 None
        if "font_size" in element and element["font_size"] is None:
            result["ok"] = False
            result["supported"] = "partial"
            result["issues"].append({
                "element": element_id,
                "field": "font_size",
                "severity": "error",
                "message": f"元素 {element_id} 的 font_size 不能为 None"
            })
            if result["severity"] != "critical":
                result["severity"] = "error"
        
        # 数值字段必须是数字
        numeric_fields = ["page", "x", "y", "width", "height", "rotation", "layer", "font_size"]
        for field in numeric_fields:
            if field in element and element[field] is not None:
                if not isinstance(element[field], (int, float)):
                    result["ok"] = False
                    result["supported"] = "partial"
                    result["issues"].append({
                        "element": element_id,
                        "field": field,
                        "severity": "error",
                        "message": f"元素 {element_id} 的 {field} 必须是数字"
                    })
                    if result["severity"] != "critical":
                        result["severity"] = "error"
        
        # 检查元素类型是否支持
        element_type = element.get("type")
        if element_type and element_type not in supported_types:
            result["ok"] = False
            result["supported"] = "partial"
            result["issues"].append({
                "element": element_id,
                "field": "type",
                "severity": "warning",
                "message": f"元素 {element_id} 使用了不支持的类型: {element_type}"
            })
            if result["severity"] not in ["critical", "error"]:
                result["severity"] = "warning"
        
        # 检查 group transform 语义相关的不支持字段
        unsupported_group_fields = ["group_id", "group_rotation", "pivot", "transform_matrix", "scale", "skew"]
        for field in unsupported_group_fields:
            if field in element:
                result["ok"] = False
                result["supported"] = "unsupported"
                result["issues"].append({
                    "element": element_id,
                    "field": field,
                    "severity": "critical",
                    "message": f"元素 {element_id} 包含不支持的 group transform 字段: {field}"
                })
                result["severity"] = "critical"
                result["message"] = "IR 包含不支持的 group transform 语义"
                return result
    
    # 检查是否有多页
    pages = set()
    for element in elements:
        page = element.get("page", 1)
        pages.add(page)
    
    if len(pages) > 1:
        result["ok"] = False
        result["supported"] = "partial"
        result["issues"].append({
            "field": "page",
            "severity": "warning",
            "message": f"检测到 {len(pages)} 页，当前仅支持单页"
        })
        if result["severity"] not in ["critical", "error"]:
            result["severity"] = "warning"
    
    # 更新最终消息
    if result["severity"] == "critical":
        result["message"] = "IR 包含不支持的特性，无法 roundtrip"
    elif result["severity"] == "error":
        result["message"] = "IR 存在错误，但可部分 roundtrip"
    elif result["severity"] == "warning":
        result["message"] = "IR 验证通过，但存在部分支持限制"
    elif result["ok"] and result["supported"] == "full":
        result["message"] = "IR 验证完全通过，支持完整 roundtrip"
    
    return result

def import_own_exported_tex_to_ir(tex_content: str) -> dict:
    """
    从自家导出的 LaTeX 导回 IR
    
    Args:
        tex_content: LaTeX 内容
    
    Returns:
        导回的 IR 数据
    
    Raises:
        ValueError: 如果无法从 tex 中提取 IR
    """
    # 提取嵌入的 IR 元数据
    ir_data = extract_embedded_ir_from_tex(tex_content)
    
    # 验证提取的 IR
    validation_result = validate_ir_roundtripability(ir_data)
    if not validation_result["ok"]:
        raise ValueError(f"Extracted IR validation failed: {validation_result['message']}")
    
    return ir_data

def validate_tex_profile(tex_content: str) -> dict:
    """
    验证 LaTeX 是否符合 Conforming LaTeX Profile v1
    
    Args:
        tex_content: LaTeX 内容
    
    Returns:
        验证结果字典，包含 ok / issues / message
    """
    result = {
        "ok": True,
        "issues": [],
        "message": "Tex 符合 Conforming LaTeX Profile v1"
    }
    
    # 检查必要的结构
    required_sections = [
        "% Preamble / 宏包区",
        "% Metadata / 注释区",
        "% IR Metadata for roundtrip:",
        "% BEGIN_IR_METADATA",
        "% END_IR_METADATA",
        "\\begin{document}",
        "\\end{document}"
    ]
    
    for section in required_sections:
        if section not in tex_content:
            result["ok"] = False
            result["issues"].append(f"Missing required section: {section}")
    
    # 检查嵌入的 IR 元数据
    try:
        ir_data = extract_embedded_ir_from_tex(tex_content)
    except Exception as e:
        result["ok"] = False
        result["issues"].append(f"Failed to extract IR metadata: {str(e)}")
    
    if not result["ok"]:
        result["message"] = "Tex 不符合 Conforming LaTeX Profile v1"
    
    return result

def extract_embedded_ir_from_tex(tex_content: str) -> dict:
    """
    从 LaTeX 中提取嵌入的 IR 元数据
    
    Args:
        tex_content: LaTeX 内容
    
    Returns:
        提取的 IR 数据
    
    Raises:
        ValueError: 如果无法提取 IR 元数据
    """
    import json
    
    # 查找 IR 元数据的开始和结束标记
    start_marker = "% BEGIN_IR_METADATA"
    end_marker = "% END_IR_METADATA"
    
    start_idx = tex_content.find(start_marker)
    if start_idx == -1:
        raise ValueError("No IR metadata found in tex content")
    
    end_idx = tex_content.find(end_marker, start_idx)
    if end_idx == -1:
        raise ValueError("Incomplete IR metadata in tex content")
    
    # 提取元数据部分
    metadata_section = tex_content[start_idx + len(start_marker):end_idx].strip()
    
    # 移除每行的 % 前缀
    lines = metadata_section.split('\n')
    json_lines = []
    for line in lines:
        if line.startswith('%'):
            json_line = line[1:].strip()
            if json_line:
                json_lines.append(json_line)
    
    # 重建 JSON 字符串
    json_str = '\n'.join(json_lines)
    
    try:
        metadata = json.loads(json_str)
        ir_data = metadata.get('ir')
        if not ir_data:
            raise ValueError("No IR data found in metadata")
        return ir_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse IR metadata: {str(e)}")
