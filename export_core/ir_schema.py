# IR Schema Definition for Export Core

from typing import List, Optional, Dict, Any

class ExportIR:
    """Export Intermediate Representation (IR) for guiLaTeX"""
    
    def __init__(self, elements: List[Dict[str, Any]]):
        self.elements = elements

class ElementIR:
    """Element IR for guiLaTeX"""
    
    def __init__(self,
                 id: str,
                 type: str,
                 content: str,
                 page: int,
                 x: float,
                 y: float,
                 width: float,
                 height: float,
                 rotation: float,
                 layer: int,
                 font_family_zh: Optional[str] = None,
                 font_family_en: Optional[str] = None,
                 font_size: Optional[float] = None,
                 color: Optional[str] = None,
                 alignment: Optional[str] = None,
                 visible: bool = True):
        self.id = id
        self.type = type
        self.content = content
        self.page = page
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.layer = layer
        self.font_family_zh = font_family_zh
        self.font_family_en = font_family_en
        self.font_size = font_size
        self.color = color
        self.alignment = alignment
        self.visible = visible

    def to_dict(self) -> Dict[str, Any]:
        """Convert ElementIR to dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "content": self.content,
            "page": self.page,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "rotation": self.rotation,
            "layer": self.layer,
            "font_family_zh": self.font_family_zh,
            "font_family_en": self.font_family_en,
            "font_size": self.font_size,
            "color": self.color,
            "alignment": self.alignment,
            "visible": self.visible
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ElementIR':
        """Create ElementIR from dictionary"""
        return cls(
            id=data["id"],
            type=data["type"],
            content=data["content"],
            page=data["page"],
            x=data["x"],
            y=data["y"],
            width=data["width"],
            height=data["height"],
            rotation=data["rotation"],
            layer=data["layer"],
            font_family_zh=data.get("font_family_zh"),
            font_family_en=data.get("font_family_en"),
            font_size=data.get("font_size"),
            color=data.get("color"),
            alignment=data.get("alignment"),
            visible=data.get("visible", True)
        )

# Supported element types
SUPPORTED_TYPES = ["title", "author", "paragraph", "textbox", "equation", "image"]

# Coordinate system definition
COORDINATE_SYSTEM = {
    "origin": "top-left corner of the page",
    "unit": "millimeters (mm)",
    "page_size": "A4 (210mm × 297mm)",
    "rotation_direction": "clockwise",
    "layer_order": "higher number means higher layer (appears on top)"
}