"""
Element Model

Represents a single element in the document (text, image, formula, etc.)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import uuid
import copy


@dataclass
class ElementModel:
    """Model for a document element
    
    This is the source of truth for element state.
    All visual editing operations modify this model.
    """
    
    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = 'text'  # 'text', 'image', 'formula', 'line', etc.
    
    # Content
    content: str = ''  # Text content or LaTeX code
    
    # Geometry (in PDF points, 1/72 inch)
    x: float = 0.0
    y: float = 0.0
    width: float = 100.0
    height: float = 20.0
    
    # Typography
    font_size: float = 12.0
    font_family: str = 'default'
    
    # State tracking
    dirty: bool = False  # True if modified since last save/export
    selected: bool = False  # True if currently selected in UI
    
    # Source tracking
    original_source: Optional[str] = None  # 'pdf_extraction', 'user_created', etc.
    source_element_id: Optional[str] = None  # Original ID if imported from PDF
    
    # Metadata for extensibility
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate and initialize after creation"""
        # Ensure ID is set
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def mark_dirty(self):
        """Mark element as modified"""
        self.dirty = True
    
    def mark_clean(self):
        """Mark element as clean (after save/export)"""
        self.dirty = False
    
    def update_position(self, x: float, y: float):
        """Update element position
        
        Args:
            x: New x coordinate
            y: New y coordinate
        """
        self.x = x
        self.y = y
        self.mark_dirty()
    
    def update_size(self, width: float, height: float):
        """Update element size
        
        Args:
            width: New width
            height: New height
        """
        self.width = width
        self.height = height
        self.mark_dirty()
    
    def update_content(self, content: str):
        """Update element content
        
        Args:
            content: New content
        """
        self.content = content
        self.mark_dirty()
    
    def update_font(self, font_size: Optional[float] = None, font_family: Optional[str] = None):
        """Update font properties
        
        Args:
            font_size: New font size
            font_family: New font family
        """
        if font_size is not None:
            self.font_size = font_size
        if font_family is not None:
            self.font_family = font_family
        self.mark_dirty()
    
    def get_bbox(self) -> tuple:
        """Get bounding box as (x, y, width, height)
        
        Returns:
            tuple: (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)
    
    def contains_point(self, px: float, py: float) -> bool:
        """Check if point is inside element
        
        Args:
            px: Point x coordinate
            py: Point y coordinate
            
        Returns:
            bool: True if point is inside
        """
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)
    
    def copy(self) -> 'ElementModel':
        """Create a deep copy of this element
        
        Returns:
            ElementModel: Deep copy with new ID
        """
        # Use dataclass's built-in copy with new ID
        new_element = ElementModel(
            id=str(uuid.uuid4()),  # New unique ID
            type=self.type,
            content=self.content,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            font_size=self.font_size,
            font_family=self.font_family,
            dirty=True,  # New copy is dirty
            selected=False,
            original_source=self.original_source,
            source_element_id=self.id,  # Reference to original
            metadata=copy.deepcopy(self.metadata)
        )
        return new_element
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization
        
        Returns:
            dict: Element as dictionary
        """
        return {
            'id': self.id,
            'type': self.type,
            'content': self.content,
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height,
            'font_size': self.font_size,
            'font_family': self.font_family,
            'dirty': self.dirty,
            'original_source': self.original_source,
            'source_element_id': self.source_element_id,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ElementModel':
        """Create element from dictionary
        
        Args:
            data: Dictionary with element data
            
        Returns:
            ElementModel: New element instance
        """
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            type=data.get('type', 'text'),
            content=data.get('content', ''),
            x=data.get('x', 0.0),
            y=data.get('y', 0.0),
            width=data.get('width', 100.0),
            height=data.get('height', 20.0),
            font_size=data.get('font_size', 12.0),
            font_family=data.get('font_family', 'default'),
            dirty=data.get('dirty', False),
            original_source=data.get('original_source'),
            source_element_id=data.get('source_element_id'),
            metadata=data.get('metadata', {})
        )
    
    def __repr__(self) -> str:
        return f"ElementModel(id={self.id[:8]}, type={self.type}, content='{self.content[:30]}...')"
