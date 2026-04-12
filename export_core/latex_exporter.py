# LaTeX Exporter for Export Core

import datetime
from typing import List, Dict, Any

class LatexExporter:
    """LaTeX Exporter for guiLaTeX Export IR"""
    
    def __init__(self):
        self.page_width = 210  # A4 width in mm
        self.page_height = 297  # A4 height in mm
    
    def export(self, ir: Dict[str, Any]) -> str:
        """Export IR to LaTeX"""
        elements = ir.get("elements", [])
        
        # Sort elements by layer (ascending) so that higher layers are rendered on top
        sorted_elements = sorted(elements, key=lambda x: x.get("layer", 0))
        
        # Build LaTeX document
        latex_parts = []
        
        # Preamble / 宏包区
        latex_parts.append(self._generate_preamble())
        
        # Document start
        latex_parts.append("\\begin{document}")
        
        # Metadata / 注释区
        latex_parts.append(self._generate_metadata())
        
        # Optional semantic summary 区
        latex_parts.append(self._generate_semantic_summary(sorted_elements))
        
        # Absolute positioned objects 区
        latex_parts.append(self._generate_absolute_objects(sorted_elements))
        
        # Document end
        latex_parts.append("\\end{document}")
        
        return "\n".join(latex_parts)
    
    def _generate_preamble(self) -> str:
        """Generate LaTeX preamble"""
        return """% Preamble / 宏包区
\\documentclass{article}
\\usepackage[margin=0mm]{geometry}
\\usepackage{xcolor}
\\usepackage{graphicx}
\\usepackage{tikz}
\\usepackage{amsmath}
"""
    
    def _generate_metadata(self) -> str:
        """Generate metadata section"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""% Metadata / 注释区
% Exported by guiLaTeX ExportCore
% Export date: {now}
% Page size: A4 (210mm × 297mm)
"""
    
    def _generate_semantic_summary(self, elements: List[Dict[str, Any]]) -> str:
        """Generate semantic summary section"""
        summary_lines = ["% Optional semantic summary 区"]
        
        # Extract title and author
        title = None
        author = None
        
        for element in elements:
            if element["type"] == "title" and element["visible"]:
                title = element["content"]
            elif element["type"] == "author" and element["visible"]:
                author = element["content"]
        
        if title:
            summary_lines.append(f"% Title: {title}")
        if author:
            summary_lines.append(f"% Author: {author}")
        
        return "\n".join(summary_lines)
    
    def _generate_absolute_objects(self, elements: List[Dict[str, Any]]) -> str:
        """Generate absolute positioned objects section"""
        lines = ["% Absolute positioned objects 区", "\\begin{tikzpicture}[remember picture, overlay]"]
        
        for element in elements:
            if not element.get("visible", True):
                continue
            
            # Calculate y coordinate (LaTeX origin is bottom-left, IR origin is top-left)
            latex_y = self.page_height - element["y"]
            
            # Generate node for element
            node_lines = self._generate_element_node(element, latex_y)
            lines.extend(node_lines)
        
        lines.append("\\end{tikzpicture}")
        return "\n".join(lines)
    
    def _sanitize_content(self, content: str, element_type: str) -> str:
        """Sanitize content based on element type"""
        if element_type == "equation":
            # 验证公式内容
            # 可以添加更严格的验证
            return content
        elif element_type == "image":
            # 验证图片路径
            # 确保路径是相对路径且不包含 ../
            import os
            safe_path = os.path.normpath(content)
            if '..' in safe_path:
                return ""
            return safe_path
        else:
            # 转义特殊字符
            content = content.replace('\\', '\\\\')
            content = content.replace('{', '\\{')
            content = content.replace('}', '\\}')
            return content

    def _generate_element_node(self, element: Dict[str, Any], latex_y: float) -> List[str]:
        """Generate LaTeX node for a single element"""
        lines = []
        
        # Element type and id
        element_type = element["type"]
        element_id = element["id"]
        layer = element.get("layer", 0)
        
        # Common node attributes
        node_attrs = [
            "anchor=north west",
            f"rotate={element.get('rotation', 0)}",
            f"text width={element['width']}mm"
        ]
        
        # Alignment
        alignment = element.get("alignment", "left")
        if alignment == "left":
            node_attrs.append("align=left")
        elif alignment == "center":
            node_attrs.append("align=center")
        elif alignment == "right":
            node_attrs.append("align=right")
        
        # Font properties
        font_size = element.get("font_size", 12)
        font_family_zh = element.get("font_family_zh", "SimSun")
        font_family_en = element.get("font_family_en", "Times New Roman")
        
        # Font command
        if font_size is None:
            font_size = 12  # 默认字体大小
        # 格式化字体大小，避免浮点脏值
        font_size_int = int(font_size)
        line_spacing = round(font_size * 1.2, 1)
        font_cmd = f"\\fontsize{{{font_size_int}}}{{{line_spacing}}}\\selectfont"
        node_attrs.append(f"font={font_cmd}")
        
        # Color
        color = element.get("color", "#000000")
        # Convert HEX to LaTeX color
        latex_color = self._hex_to_latex_color(color)
        node_attrs.append(f"color={latex_color}")
        
        # Layer
        node_attrs.append(f"visible on layer={layer}")
        
        # Position
        x = element["x"]
        y = latex_y
        position = f"at ({x}mm, {y}mm)"
        
        # Content based on element type
        content = element["content"]
        # Sanitize content
        sanitized_content = self._sanitize_content(content, element_type)
        
        if element_type == "equation":
            # Wrap equation in $ for inline math
            content = f"${sanitized_content}$"
        elif element_type == "image":
            # For images, use \includegraphics
            width = element["width"]
            height = element["height"]
            content = f"\\includegraphics[width={width}mm, height={height}mm]{{{sanitized_content}}}"
        else:
            content = sanitized_content
        
        # Build node
        node_attrs_str = ", ".join(node_attrs)
        lines.append(f"  % Layer {layer}: {element_id}")
        lines.append(f"  \\node[{node_attrs_str}]")
        lines.append(f"    {position} {{{content}}};")
        
        return lines
    
    def _hex_to_latex_color(self, hex_color: str) -> str:
        """Convert HEX color to LaTeX color"""
        # Remove # if present
        hex_color = hex_color.lstrip("#")
        
        # Convert to RGB
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        
        # Return LaTeX color definition
        return f"{{rgb,1:red,{r};green,{g};blue,{b}}}"

# Example usage
if __name__ == "__main__":
    # Sample IR
    sample_ir = {
        "elements": [
            {
                "id": "title-1",
                "type": "title",
                "content": "示例文档",
                "page": 1,
                "x": 50,
                "y": 30,
                "width": 110,
                "height": 20,
                "rotation": 0,
                "layer": 10,
                "font_family_zh": "SimSun",
                "font_family_en": "Times New Roman",
                "font_size": 24,
                "color": "#000000",
                "alignment": "center",
                "visible": True
            },
            {
                "id": "author-1",
                "type": "author",
                "content": "张三",
                "page": 1,
                "x": 95,
                "y": 55,
                "width": 20,
                "height": 10,
                "rotation": 0,
                "layer": 9,
                "font_family_zh": "SimSun",
                "font_family_en": "Times New Roman",
                "font_size": 12,
                "color": "#000000",
                "alignment": "center",
                "visible": True
            },
            {
                "id": "paragraph-1",
                "type": "paragraph",
                "content": "这是一段示例文本。",
                "page": 1,
                "x": 30,
                "y": 80,
                "width": 150,
                "height": 30,
                "rotation": 0,
                "layer": 8,
                "font_family_zh": "SimSun",
                "font_family_en": "Times New Roman",
                "font_size": 12,
                "color": "#000000",
                "alignment": "left",
                "visible": True
            },
            {
                "id": "equation-1",
                "type": "equation",
                "content": "E = mc^2",
                "page": 1,
                "x": 80,
                "y": 120,
                "width": 50,
                "height": 20,
                "rotation": 0,
                "layer": 7,
                "font_family_zh": "SimSun",
                "font_family_en": "Times New Roman",
                "font_size": 14,
                "color": "#000000",
                "alignment": "center",
                "visible": True
            },
            {
                "id": "image-1",
                "type": "image",
                "content": "example.jpg",
                "page": 1,
                "x": 60,
                "y": 150,
                "width": 90,
                "height": 60,
                "rotation": 0,
                "layer": 6,
                "visible": True
            }
        ]
    }
    
    # Create exporter and generate LaTeX
    exporter = LatexExporter()
    latex_output = exporter.export(sample_ir)
    
    # Print LaTeX output
    print(latex_output)
