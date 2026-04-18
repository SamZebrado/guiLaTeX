#!/usr/bin/env python3
"""
ExportCore to Web 最小桥接脚本

功能：
1. 读取项目自己导出的 conforming LaTeX 文件
2. 解析其中的 IR 元数据
3. 转换为 Web 可编辑的模型格式
4. 保存为 JSON 文件
"""

import json
import os
import sys
import re

# 添加项目根目录到路径，以便导入 export_core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def parse_latex_ir_metadata(latex_content):
    """
    解析 LaTeX 文件中的 IR 元数据
    
    Args:
        latex_content: LaTeX 文件内容
    
    Returns:
        解析后的 IR 数据
    """
    # 查找 IR 元数据部分
    metadata_pattern = r'% BEGIN_IR_METADATA(.*?)% END_IR_METADATA'
    match = re.search(metadata_pattern, latex_content, re.DOTALL)
    
    if not match:
        raise ValueError("LaTeX 文件中未找到 IR 元数据")
    
    metadata_str = match.group(1)
    # 移除每行开头的 % 符号和空格
    metadata_str = re.sub(r'^%\s*', '', metadata_str, flags=re.MULTILINE)
    
    try:
        metadata = json.loads(metadata_str)
        return metadata.get('ir', {})
    except json.JSONDecodeError as e:
        raise ValueError(f"解析 IR 元数据失败: {e}")

def ir_to_web_model(ir_data):
    """
    将 IR 数据转换为 Web 模型格式
    
    Args:
        ir_data: 解析后的 IR 数据
    
    Returns:
        Web 模型数据
    """
    elements = []
    
    # 计算最大 layer 值，用于转换为 Web 模型的 layerId
    max_layer = max([el.get('layer', 0) for el in ir_data.get('elements', [])], default=0)
    
    for element in ir_data.get('elements', []):
        # 转换 layer：IR 中 layer 越大层级越高，Web 模型中 layerId 越小层级越高
        layer_id = max_layer - element.get('layer', 0) + 1
        
        web_element = {
            'id': element.get('id', str(len(elements) + 1)),
            'type': element.get('type', 'textbox'),
            'role': element.get('type', 'textbox'),  # 使用 type 作为 role
            'content': element.get('content', ''),
            'x': element.get('x', 0),
            'y': element.get('y', 0),
            'width': element.get('width', 100),
            'height': element.get('height', 50),
            'rotation': element.get('rotation', 0),
            'layerId': layer_id,
            'zIndex': layer_id,
            'selected': False
        }
        
        # 添加字体相关属性
        if element.get('font_family_zh'):
            web_element['chineseFont'] = element['font_family_zh']
        else:
            web_element['chineseFont'] = 'Noto Sans SC'
        
        if element.get('font_family_en'):
            web_element['englishFont'] = element['font_family_en']
        else:
            web_element['englishFont'] = 'Inter'
        
        if element.get('font_size'):
            web_element['fontSize'] = element['font_size']
        else:
            web_element['fontSize'] = 16
        
        elements.append(web_element)
    
    return {'elements': elements}

def core_to_web_bridge(latex_path, output_json_path):
    """
    执行 ExportCore 到 Web 的桥接
    
    Args:
        latex_path: LaTeX 文件路径
        output_json_path: 输出的 JSON 文件路径
    """
    try:
        # 1. 读取 LaTeX 文件
        print(f"读取 LaTeX 文件: {latex_path}")
        with open(latex_path, 'r', encoding='utf-8') as f:
            latex_content = f.read()
        
        # 2. 解析 IR 元数据
        print("解析 IR 元数据...")
        ir_data = parse_latex_ir_metadata(latex_content)
        print(f"解析到 {len(ir_data.get('elements', []))} 个元素")
        
        # 3. 转换为 Web 模型
        print("转换为 Web 模型...")
        web_model = ir_to_web_model(ir_data)
        print(f"转换后包含 {len(web_model.get('elements', []))} 个元素")
        
        # 4. 保存 JSON 文件
        print(f"保存 Web 模型文件: {output_json_path}")
        # 确保输出目录存在
        output_dir = os.path.dirname(output_json_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(web_model, f, indent=2, ensure_ascii=False)
        
        print("\n✅ 桥接成功！")
        print(f"输入: {latex_path}")
        print(f"输出: {output_json_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 桥接失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # 输入输出路径 - 使用命令行参数或默认值
    if len(sys.argv) == 3:
        latex_path = sys.argv[1]
        output_json_path = sys.argv[2]
    else:
        # 默认路径 - 使用之前导出的 LaTeX 文件
        latex_path = os.path.join(os.path.dirname(__file__), '..', 'temp', 'web_to_core', 'web_real_export_output.tex')
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'temp', 'core_to_web')
        output_json_path = os.path.join(output_dir, 'core_to_web_import_output.json')
    
    # 执行桥接
    success = core_to_web_bridge(latex_path, output_json_path)
    
    if success:
        print("\n🎉 桥接完成！")
        print(f"Web 模型文件已保存到: {output_json_path}")
        return 0
    else:
        print("\n💥 桥接失败！")
        return 1

if __name__ == "__main__":
    sys.exit(main())