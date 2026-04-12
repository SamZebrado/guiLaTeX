#!/usr/bin/env python3
"""
Test cases for Canvas component
"""

import pytest
import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui import canvas


@pytest.fixture
def qapp():
    """Fixture for QApplication"""
    app = QApplication([])
    yield app
    app.quit()


class TestCanvas:
    """Test Canvas component"""
    
    def test_canvas_initialization(self, qapp):
        """Test Canvas initialization"""
        canvas_widget = canvas.Canvas()
        assert canvas_widget is not None
        assert canvas_widget.scene is not None
    
    def test_add_sample_elements(self, qapp):
        """Test adding sample elements"""
        canvas_widget = canvas.Canvas()
        # Count elements (excluding grid lines)
        elements = [item for item in canvas_widget.scene.items() 
                   if hasattr(item, 'text')]
        assert len(elements) >= 2  # Should have at least text and math elements
    
    def test_element_selection(self, qapp):
        """Test element selection"""
        canvas_widget = canvas.Canvas()
        
        # Get first element
        elements = [item for item in canvas_widget.scene.items() 
                   if hasattr(item, 'text')]
        if elements:
            element = elements[0]
            # Select element
            element.setSelected(True)
            canvas_widget.update_selected_items()
            assert len(canvas_widget.selected_items) == 1
            assert canvas_widget.selected_items[0] == element
    
    def test_deselect_all(self, qapp):
        """Test deselect all"""
        canvas_widget = canvas.Canvas()
        
        # Select all elements
        canvas_widget.select_all()
        assert len(canvas_widget.selected_items) > 0
        
        # Deselect all
        canvas_widget.deselect_all()
        assert len(canvas_widget.selected_items) == 0
    
    def test_delete_selected_items(self, qapp):
        """Test delete selected items"""
        canvas_widget = canvas.Canvas()
        
        # Select first element
        elements = [item for item in canvas_widget.scene.items() 
                   if hasattr(item, 'text')]
        if elements:
            element = elements[0]
            element.setSelected(True)
            canvas_widget.update_selected_items()
            assert len(canvas_widget.selected_items) == 1
            
            # Delete selected
            canvas_widget.delete_selected_items()
            assert len(canvas_widget.selected_items) == 0
            # Element should no longer be in scene
            elements_after = [item for item in canvas_widget.scene.items() 
                           if hasattr(item, 'text')]
            assert element not in elements_after


if __name__ == "__main__":
    pytest.main([__file__])
