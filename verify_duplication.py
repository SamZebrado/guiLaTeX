#!/usr/bin/env python3
"""
Simple script to verify duplication detection
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Test 1: Basic duplication detection
def test_basic_duplication():
    print("=== Test 1: Basic duplication detection ===")
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
    
    print(f"Elements: {len(memory_elements)}")
    print(f"Unique IDs: {len(unique_ids)}")
    print(f"Duplicate found: {duplicate_found}")
    print()

# Test 2: Demo scene elements
def test_demo_scene():
    print("=== Test 2: Demo scene elements ===")
    # Demo elements
    demo_elements = [
        {'id': 'demo_title', 'text': '可视化编辑 LaTeX 文档'},
        {'id': 'demo_author', 'text': '作者：某某 / 博士生原型测试'},
        {'id': 'demo_body', 'text': '这是一段用于演示正文对象的内容'},
        {'id': 'demo_formula', 'text': 'E = mc²'},
        {'id': 'demo_image', 'text': '图片示例 / 占位图'}
    ]
    
    # Detect duplicates
    unique_ids = set()
    duplicate_found = False
    for elem in demo_elements:
        if elem['id'] in unique_ids:
            duplicate_found = True
            break
        unique_ids.add(elem['id'])
    
    print(f"Elements: {len(demo_elements)}")
    print(f"Unique IDs: {len(unique_ids)}")
    print(f"Duplicate found: {duplicate_found}")
    print()

# Test 3: Simulate model elements
def test_model_elements():
    print("=== Test 3: Model elements ===")
    try:
        from model import DocumentModel, PageModel, ElementModel
        
        # Create document model
        doc_model = DocumentModel(title="Test Document")
        page_model = PageModel(number=0)
        doc_model.add_page(page_model)
        
        # Add demo elements
        demo_elements = [
            {'id': 'demo_title', 'text': '可视化编辑 LaTeX 文档'},
            {'id': 'demo_author', 'text': '作者：某某 / 博士生原型测试'},
            {'id': 'demo_body', 'text': '这是一段用于演示正文对象的内容'},
            {'id': 'demo_formula', 'text': 'E = mc²'},
            {'id': 'demo_image', 'text': '图片示例 / 占位图'}
        ]
        
        # Add elements to model
        for elem in demo_elements:
            new_elem = ElementModel(
                id=elem['id'],
                type='text',
                content=elem['text'],
                x=100,
                y=100,
                width=200,
                height=50,
                font_size=12,
                dirty=True
            )
            page_model.add_element(new_elem)
        
        # Check for duplicates
        element_ids = [elem.id for elem in page_model.elements]
        unique_ids = set(element_ids)
        
        print(f"Elements: {len(element_ids)}")
        print(f"Unique IDs: {len(unique_ids)}")
        print(f"Duplicate found: {len(element_ids) != len(unique_ids)}")
        print(f"IDs: {sorted(list(unique_ids))}")
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("Duplication detection verification")
    print("=" * 50)
    test_basic_duplication()
    test_demo_scene()
    test_model_elements()
    print("Verification complete")
