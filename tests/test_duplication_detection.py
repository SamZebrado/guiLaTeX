#!/usr/bin/env python3
"""
Test for duplication detection in the demo scene
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model import DocumentModel, PageModel, ElementModel

def test_demo_scene_no_duplicates():
    """Test that demo scene has no duplicate objects"""
    # Create document model
    doc_model = DocumentModel(title="Test Document")
    page_model = PageModel(number=0)
    doc_model.add_page(page_model)
    
    # Add demo elements (simulating what happens in PDFPageWidget.__init__)
    demo_elements = [
        # Title
        {
            'id': 'demo_title',
            'type': 'text',
            'text': '可视化编辑 LaTeX 文档',
            'x': 100,
            'y': 50,
            'width': 400,
            'height': 40,
            'font_size': 24,
            'original_width': 400,
            'original_height': 40
        },
        # Author
        {
            'id': 'demo_author',
            'type': 'text',
            'text': '作者：某某 / 博士生原型测试',
            'x': 100,
            'y': 100,
            'width': 300,
            'height': 25,
            'font_size': 14,
            'original_width': 300,
            'original_height': 25
        },
        # Body text
        {
            'id': 'demo_body',
            'type': 'text',
            'text': '这是一段用于演示正文对象的内容，可用于测试拖动、选择和后续选择框能力。',
            'x': 100,
            'y': 150,
            'width': 400,
            'height': 80,
            'font_size': 12,
            'original_width': 400,
            'original_height': 80
        },
        # Formula
        {
            'id': 'demo_formula',
            'type': 'text',
            'text': 'E = mc²',
            'x': 100,
            'y': 240,
            'width': 200,
            'height': 30,
            'font_size': 16,
            'original_width': 200,
            'original_height': 30
        },
        # Image placeholder
        {
            'id': 'demo_image',
            'type': 'text',
            'text': '图片示例 / 占位图',
            'x': 100,
            'y': 280,
            'width': 300,
            'height': 200,
            'font_size': 12,
            'original_width': 300,
            'original_height': 200
        }
    ]
    
    # Add elements to model
    for elem in demo_elements:
        new_elem = ElementModel(
            id=elem['id'],
            type=elem['type'],
            content=elem['text'],
            x=elem['x'],
            y=elem['y'],
            width=elem['width'],
            height=elem['height'],
            font_size=elem['font_size'],
            dirty=True
        )
        page_model.add_element(new_elem)
    
    # Check for duplicates
    element_ids = [elem.id for elem in page_model.elements]
    unique_ids = set(element_ids)
    
    # Verify no duplicates
    assert len(element_ids) == len(unique_ids), f"Duplicate elements found: {len(element_ids)} elements, {len(unique_ids)} unique IDs"
    assert len(element_ids) == 5, f"Expected 5 elements, got {len(element_ids)}"
    print("✓ No duplicates in demo scene")
    print(f"  Total elements: {len(element_ids)}")
    print(f"  Unique IDs: {sorted(list(unique_ids))}")

def test_duplication_detection():
    """Test duplication detection logic"""
    # Simulate memory elements with duplicates
    memory_elements = [
        {'id': 'demo_title', 'text': 'Title 1'},
        {'id': 'demo_author', 'text': 'Author 1'},
        {'id': 'demo_title', 'text': 'Title 2'},  # Duplicate ID
        {'id': 'demo_body', 'text': 'Body 1'}
    ]
    
    # Detect duplicates
    unique_ids = set()
    duplicate_found = False
    for elem in memory_elements:
        if elem['id'] in unique_ids:
            duplicate_found = True
            break
        unique_ids.add(elem['id'])
    
    assert duplicate_found, "Should detect duplicates"
    assert len(unique_ids) == 3, f"Expected 3 unique IDs, got {len(unique_ids)}"
    print("✓ Duplication detection works correctly")

if __name__ == "__main__":
    # Run tests
    test_demo_scene_no_duplicates()
    test_duplication_detection()
    print("All duplication detection tests passed!")
