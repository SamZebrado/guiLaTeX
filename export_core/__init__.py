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
    'export_ir_to_latex'
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
    return {
        'id': web_element.get('id', ''),
        'type': web_element.get('type', 'textbox'),
        'content': web_element.get('text', web_element.get('content', '')),
        'page': 1,
        'x': web_element.get('x', 0),
        'y': web_element.get('y', 0),
        'width': web_element.get('width', 0),
        'height': web_element.get('height', 0),
        'rotation': web_element.get('rotation', 0),
        'layer': web_element.get('layerId', web_element.get('layer', 0)),
        'font_family_zh': 'SimSun',
        'font_family_en': 'Times New Roman',
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
    """
    exporter = LatexExporter()
    return exporter.export(ir)
