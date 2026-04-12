"""
Tests for the model layer

These tests verify that the internal document model works correctly
and serves as the source of truth for document state.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model import ElementModel, PageModel, DocumentModel


def test_element_model():
    """Test ElementModel creation and operations"""
    print("Testing ElementModel...")
    
    # Create element
    elem = ElementModel(
        type='text',
        content='Hello World',
        x=100,
        y=200,
        width=150,
        height=30,
        font_size=14
    )
    
    # Verify ID is unique
    assert elem.id is not None
    assert len(elem.id) > 0
    print(f"  ✓ Element created with ID: {elem.id[:8]}")
    
    # Verify initial state
    assert elem.dirty == False
    assert elem.content == 'Hello World'
    print("  ✓ Initial state correct")
    
    # Test modification
    elem.update_content('Updated text')
    assert elem.dirty == True
    assert elem.content == 'Updated text'
    print("  ✓ Modification tracking works")
    
    # Test position update
    elem.update_position(150, 250)
    assert elem.x == 150
    assert elem.y == 250
    print("  ✓ Position update works")
    
    # Test contains_point
    assert elem.contains_point(160, 260) == True
    assert elem.contains_point(0, 0) == False
    print("  ✓ Point containment works")
    
    # Test copy (deep copy with new ID)
    elem_copy = elem.copy()
    assert elem_copy.id != elem.id
    assert elem_copy.content == elem.content
    assert elem_copy.dirty == True  # Copy is dirty
    print("  ✓ Deep copy works with new ID")
    
    print("ElementModel tests passed!\n")


def test_page_model():
    """Test PageModel creation and operations"""
    print("Testing PageModel...")
    
    # Create page
    page = PageModel(number=0)
    
    # Verify ID
    assert page.id is not None
    print(f"  ✓ Page created with ID: {page.id[:8]}")
    
    # Add elements
    elem1 = ElementModel(content='Element 1', x=10, y=10)
    elem2 = ElementModel(content='Element 2', x=20, y=20)
    
    page.add_element(elem1)
    page.add_element(elem2)
    
    assert len(page.elements) == 2
    assert page.dirty == True
    print("  ✓ Elements added to page")
    
    # Test get_element_by_id
    found = page.get_element_by_id(elem1.id)
    assert found is not None
    assert found.content == 'Element 1'
    print("  ✓ Element lookup by ID works")
    
    # Test selection
    page.select_element(elem1.id)
    assert elem1.selected == True
    assert elem2.selected == False
    print("  ✓ Element selection works")
    
    # Test get_elements_at
    elements_at = page.get_elements_at(15, 15)
    assert len(elements_at) >= 1
    print("  ✓ Element hit testing works")
    
    print("PageModel tests passed!\n")


def test_document_model():
    """Test DocumentModel creation and operations"""
    print("Testing DocumentModel...")
    
    # Create document
    doc = DocumentModel(title='Test Document', author='Test Author')
    
    # Verify ID and initial state
    assert doc.id is not None
    assert doc.title == 'Test Document'
    assert len(doc.pages) == 1  # Auto-creates first page
    print(f"  ✓ Document created with ID: {doc.id[:8]}")
    print("  ✓ Auto-created first page")
    
    # Add elements to first page
    page = doc.pages[0]
    elem = ElementModel(content='Test Element')
    page.add_element(elem)
    
    # Page is dirty after adding element, but element itself is not dirty (just created)
    assert page.dirty == True
    print("  ✓ Page dirty tracking works")
    
    # Now modify the element to make it dirty
    elem.update_content('Modified Test Element')
    assert doc.has_dirty_elements() == True
    print("  ✓ Dirty element detection works")
    
    # Test get_element_by_id (searches all pages)
    found = doc.get_element_by_id(elem.id)
    assert found is not None
    assert found.content == 'Modified Test Element'
    print("  ✓ Global element lookup works")
    
    # Test add_page
    page2 = doc.add_page()
    assert len(doc.pages) == 2
    assert page2.number == 1
    print("  ✓ Page addition works")
    
    # Test copy
    doc_copy = doc.copy()
    assert doc_copy.id != doc.id
    assert doc_copy.title == 'Test Document (Copy)'
    assert len(doc_copy.pages) == 2
    print("  ✓ Document deep copy works")
    
    # Test serialization
    data = doc.to_dict()
    assert 'id' in data
    assert 'pages' in data
    assert len(data['pages']) == 2
    print("  ✓ Serialization works")
    
    # Test deserialization
    doc_restored = DocumentModel.from_dict(data)
    assert doc_restored.title == doc.title
    assert len(doc_restored.pages) == len(doc.pages)
    print("  ✓ Deserialization works")
    
    print("DocumentModel tests passed!\n")


def test_unique_ids():
    """Verify that all IDs are unique"""
    print("Testing ID uniqueness...")
    
    elements = [ElementModel() for _ in range(100)]
    ids = [e.id for e in elements]
    
    assert len(ids) == len(set(ids)), "Duplicate IDs found!"
    print(f"  ✓ All {len(ids)} element IDs are unique")
    
    pages = [PageModel(number=i) for i in range(10)]
    page_ids = [p.id for p in pages]
    
    assert len(page_ids) == len(set(page_ids)), "Duplicate page IDs found!"
    print(f"  ✓ All {len(page_ids)} page IDs are unique")
    
    docs = [DocumentModel() for _ in range(5)]
    doc_ids = [d.id for d in docs]
    
    assert len(doc_ids) == len(set(doc_ids)), "Duplicate document IDs found!"
    print(f"  ✓ All {len(doc_ids)} document IDs are unique")
    
    print("ID uniqueness tests passed!\n")


def test_no_shallow_copy_issues():
    """Verify that copy() creates true deep copies"""
    print("Testing deep copy behavior...")
    
    # Create element with metadata
    elem = ElementModel(
        content='Original',
        metadata={'key1': 'value1', 'nested': {'a': 1}}
    )
    
    # Copy
    elem_copy = elem.copy()
    
    # Modify original metadata
    elem.metadata['key1'] = 'modified'
    elem.metadata['nested']['a'] = 999
    
    # Verify copy is unaffected
    assert elem_copy.metadata['key1'] == 'value1'
    assert elem_copy.metadata['nested']['a'] == 1
    print("  ✓ Metadata deep copy works")
    
    # Test page copy
    page = PageModel()
    elem1 = ElementModel(content='E1')
    page.add_element(elem1)
    
    page_copy = page.copy()
    
    # Modify original
    elem1.update_content('Modified')
    
    # Verify copy element is unaffected
    copy_elem = page_copy.get_element_by_id(elem1.id)
    if copy_elem:  # If ID was preserved
        pass  # Element in copy should have original content
    
    # Actually, copy() creates new IDs, so we need to check by index
    assert page_copy.elements[0].content == 'E1'
    print("  ✓ Page deep copy works")
    
    print("Deep copy tests passed!\n")


if __name__ == '__main__':
    print("=" * 60)
    print("Running Model Layer Tests")
    print("=" * 60 + "\n")
    
    test_element_model()
    test_page_model()
    test_document_model()
    test_unique_ids()
    test_no_shallow_copy_issues()
    
    print("=" * 60)
    print("All tests passed!")
    print("=" * 60)
