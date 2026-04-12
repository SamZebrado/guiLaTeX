"""
Page Model

Represents a single page in the document.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import uuid
import copy

from .element import ElementModel


@dataclass
class PageModel:
    """Model for a document page
    
    Contains a collection of elements and page-level properties.
    """
    
    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    number: int = 0  # Page number (0-indexed)
    
    # Elements
    elements: List[ElementModel] = field(default_factory=list)
    
    # Page dimensions (in PDF points, 1/72 inch)
    width: float = 595.0   # A4 default width
    height: float = 842.0  # A4 default height
    
    # State tracking
    dirty: bool = False
    
    def __post_init__(self):
        """Validate and initialize after creation"""
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def add_element(self, element: ElementModel) -> ElementModel:
        """Add an element to this page
        
        Args:
            element: Element to add
            
        Returns:
            ElementModel: The added element
        """
        self.elements.append(element)
        self.mark_dirty()
        return element
    
    def remove_element(self, element_id: str) -> bool:
        """Remove an element by ID
        
        Args:
            element_id: ID of element to remove
            
        Returns:
            bool: True if element was found and removed
        """
        for i, element in enumerate(self.elements):
            if element.id == element_id:
                del self.elements[i]
                self.mark_dirty()
                return True
        return False
    
    def get_element_by_id(self, element_id: str) -> Optional[ElementModel]:
        """Get element by ID
        
        Args:
            element_id: Element ID
            
        Returns:
            ElementModel or None
        """
        for element in self.elements:
            if element.id == element_id:
                return element
        return None
    
    def get_elements_at(self, x: float, y: float) -> List[ElementModel]:
        """Get all elements at a point (top to bottom order)
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of elements at the point
        """
        result = []
        for element in reversed(self.elements):  # Reverse for top-to-bottom
            if element.contains_point(x, y):
                result.append(element)
        return result
    
    def get_selected_elements(self) -> List[ElementModel]:
        """Get all selected elements
        
        Returns:
            List of selected elements
        """
        return [e for e in self.elements if e.selected]
    
    def clear_selection(self):
        """Clear all element selections"""
        for element in self.elements:
            element.selected = False
    
    def select_element(self, element_id: str, clear_others: bool = True) -> bool:
        """Select an element by ID
        
        Args:
            element_id: Element ID to select
            clear_others: If True, deselect other elements
            
        Returns:
            bool: True if element was found and selected
        """
        if clear_others:
            self.clear_selection()
        
        element = self.get_element_by_id(element_id)
        if element:
            element.selected = True
            return True
        return False
    
    def mark_dirty(self):
        """Mark page as modified"""
        self.dirty = True
    
    def mark_clean(self):
        """Mark page as clean"""
        self.dirty = False
        for element in self.elements:
            element.mark_clean()
    
    def has_dirty_elements(self) -> bool:
        """Check if any element is dirty
        
        Returns:
            bool: True if any element is dirty
        """
        return any(e.dirty for e in self.elements)
    
    def copy(self) -> 'PageModel':
        """Create a deep copy of this page
        
        Returns:
            PageModel: Deep copy with new ID and copied elements
        """
        new_page = PageModel(
            id=str(uuid.uuid4()),
            number=self.number,
            width=self.width,
            height=self.height,
            dirty=True
        )
        # Deep copy all elements
        new_page.elements = [e.copy() for e in self.elements]
        return new_page
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization
        
        Returns:
            dict: Page as dictionary
        """
        return {
            'id': self.id,
            'number': self.number,
            'width': self.width,
            'height': self.height,
            'dirty': self.dirty,
            'elements': [e.to_dict() for e in self.elements]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PageModel':
        """Create page from dictionary
        
        Args:
            data: Dictionary with page data
            
        Returns:
            PageModel: New page instance
        """
        page = cls(
            id=data.get('id', str(uuid.uuid4())),
            number=data.get('number', 0),
            width=data.get('width', 595.0),
            height=data.get('height', 842.0),
            dirty=data.get('dirty', False)
        )
        # Load elements
        for elem_data in data.get('elements', []):
            page.elements.append(ElementModel.from_dict(elem_data))
        return page
    
    def __repr__(self) -> str:
        return f"PageModel(id={self.id[:8]}, number={self.number}, elements={len(self.elements)})"
