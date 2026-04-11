"""
Document Model

Represents the entire document containing multiple pages.
This is the root model and source of truth for the document state.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid
import copy

from .page import PageModel
from .element import ElementModel


@dataclass
class DocumentModel:
    """Model for the entire document
    
    This is the root model that contains all pages and elements.
    All document-level operations go through this class.
    """
    
    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Untitled"
    author: str = ""
    
    # Content
    pages: List[PageModel] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    
    # State tracking
    dirty: bool = False
    
    # Document settings
    default_page_width: float = 595.0   # A4 width in points
    default_page_height: float = 842.0  # A4 height in points
    
    def __post_init__(self):
        """Validate and initialize after creation"""
        if not self.id:
            self.id = str(uuid.uuid4())
        
        # Ensure at least one page exists
        if not self.pages:
            self.add_page()
    
    def add_page(self, page: Optional[PageModel] = None) -> PageModel:
        """Add a page to the document
        
        Args:
            page: Page to add (creates new if None)
            
        Returns:
            PageModel: The added page
        """
        if page is None:
            page = PageModel(
                number=len(self.pages),
                width=self.default_page_width,
                height=self.default_page_height
            )
        else:
            page.number = len(self.pages)
        
        self.pages.append(page)
        self.mark_dirty()
        return page
    
    def remove_page(self, page_number: int) -> bool:
        """Remove a page by number
        
        Args:
            page_number: Page number to remove (0-indexed)
            
        Returns:
            bool: True if page was found and removed
        """
        if 0 <= page_number < len(self.pages):
            del self.pages[page_number]
            # Renumber remaining pages
            for i, page in enumerate(self.pages):
                page.number = i
            self.mark_dirty()
            return True
        return False
    
    def get_page(self, page_number: int) -> Optional[PageModel]:
        """Get page by number
        
        Args:
            page_number: Page number (0-indexed)
            
        Returns:
            PageModel or None
        """
        if 0 <= page_number < len(self.pages):
            return self.pages[page_number]
        return None
    
    def get_element_by_id(self, element_id: str) -> Optional[ElementModel]:
        """Get element by ID (searches all pages)
        
        Args:
            element_id: Element ID
            
        Returns:
            ElementModel or None
        """
        for page in self.pages:
            element = page.get_element_by_id(element_id)
            if element:
                return element
        return None
    
    def get_selected_elements(self) -> List[ElementModel]:
        """Get all selected elements across all pages
        
        Returns:
            List of selected elements
        """
        selected = []
        for page in self.pages:
            selected.extend(page.get_selected_elements())
        return selected
    
    def clear_selection(self):
        """Clear all selections across all pages"""
        for page in self.pages:
            page.clear_selection()
    
    def mark_dirty(self):
        """Mark document as modified"""
        self.dirty = True
        self.modified_at = datetime.now()
    
    def mark_clean(self):
        """Mark document as clean (after save/export)"""
        self.dirty = False
        for page in self.pages:
            page.mark_clean()
    
    def has_dirty_pages(self) -> bool:
        """Check if any page is dirty
        
        Returns:
            bool: True if any page is dirty
        """
        return any(p.dirty for p in self.pages)
    
    def has_dirty_elements(self) -> bool:
        """Check if any element is dirty
        
        Returns:
            bool: True if any element is dirty
        """
        for page in self.pages:
            if page.has_dirty_elements():
                return True
        return False
    
    def get_dirty_elements(self) -> List[ElementModel]:
        """Get all dirty elements
        
        Returns:
            List of dirty elements
        """
        dirty = []
        for page in self.pages:
            for element in page.elements:
                if element.dirty:
                    dirty.append(element)
        return dirty
    
    def copy(self) -> 'DocumentModel':
        """Create a deep copy of this document
        
        Returns:
            DocumentModel: Deep copy with new ID and copied pages
        """
        new_doc = DocumentModel(
            id=str(uuid.uuid4()),
            title=self.title + " (Copy)",
            author=self.author,
            created_at=datetime.now(),
            modified_at=datetime.now(),
            dirty=True,
            default_page_width=self.default_page_width,
            default_page_height=self.default_page_height
        )
        # Deep copy all pages
        new_doc.pages = [p.copy() for p in self.pages]
        # Renumber pages
        for i, page in enumerate(new_doc.pages):
            page.number = i
        return new_doc
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization
        
        Returns:
            dict: Document as dictionary
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'dirty': self.dirty,
            'default_page_width': self.default_page_width,
            'default_page_height': self.default_page_height,
            'pages': [p.to_dict() for p in self.pages]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DocumentModel':
        """Create document from dictionary
        
        Args:
            data: Dictionary with document data
            
        Returns:
            DocumentModel: New document instance
        """
        # Create document without auto-creating pages
        doc = object.__new__(cls)
        doc.id = data.get('id', str(uuid.uuid4()))
        doc.title = data.get('title', 'Untitled')
        doc.author = data.get('author', '')
        doc.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        doc.modified_at = datetime.fromisoformat(data.get('modified_at', datetime.now().isoformat()))
        doc.dirty = data.get('dirty', False)
        doc.default_page_width = data.get('default_page_width', 595.0)
        doc.default_page_height = data.get('default_page_height', 842.0)
        doc.pages = []
        
        # Load pages
        for page_data in data.get('pages', []):
            doc.pages.append(PageModel.from_dict(page_data))
        
        # Ensure at least one page if none loaded
        if not doc.pages:
            doc.add_page()
            
        return doc
    
    def __repr__(self) -> str:
        total_elements = sum(len(p.elements) for p in self.pages)
        return f"DocumentModel(id={self.id[:8]}, title='{self.title}', pages={len(self.pages)}, elements={total_elements})"
