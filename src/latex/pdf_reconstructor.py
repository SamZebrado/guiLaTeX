#!/usr/bin/env python3
"""
guiLaTeX - PDF-to-LaTeX Reconstruction Engine

This module reconstructs LaTeX code from PDF elements,
enabling bidirectional editing between PDF and LaTeX.
"""

import re
from typing import List, Dict, Any, Optional


class PDFElement:
    """Represents a single element extracted from PDF"""
    
    def __init__(self, element_type: str, text: str, x: float, y: float,
                 width: float, height: float, font_size: float = 12,
                 font_name: str = "", is_math: bool = False):
        self.type = element_type  # 'text', 'math', 'image', etc.
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font_name = font_name
        self.is_math = is_math
        self.latex_code = ""  # Generated LaTeX code
    
    def to_latex(self) -> str:
        """Convert element to LaTeX code"""
        if self.is_math:
            return f"${self.text}$"
        return self.text


class PDFPage:
    """Represents a page in the PDF document"""
    
    def __init__(self, page_num: int, width: float, height: float):
        self.page_num = page_num
        self.width = width
        self.height = height
        self.elements: List[PDFElement] = []
    
    def add_element(self, element: PDFElement):
        """Add an element to the page"""
        self.elements.append(element)
    
    def sort_elements_by_position(self):
        """Sort elements by vertical position (top to bottom)"""
        self.elements.sort(key=lambda e: e.y)


class PDFDocument:
    """Represents the entire PDF document"""
    
    def __init__(self):
        self.pages: List[PDFPage] = []
        self.title = ""
        self.author = ""
        self.metadata = {}
    
    def add_page(self, page: PDFPage):
        """Add a page to the document"""
        self.pages.append(page)
    
    def get_all_elements(self) -> List[PDFElement]:
        """Get all elements from all pages"""
        elements = []
        for page in self.pages:
            elements.extend(page.elements)
        return elements


class LaTeXReconstructor:
    """Reconstructs LaTeX code from PDF document"""
    
    def __init__(self):
        self.document = PDFDocument()
        self.preamble_lines = []
        self.document_class = "article"
        self.packages = [
            "[utf8]{inputenc}",
            "{amsmath}",
            "{amssymb}",
            "{graphicx}",
            "{geometry}"
        ]
    
    def load_from_memory_elements(self, memory_elements: List[Dict[str, Any]], 
                                   page_width: float = 595, 
                                   page_height: float = 842):
        """Load elements from PDF canvas memory elements
        
        Args:
            memory_elements: List of element dictionaries from PDF canvas
            page_width: Page width in points
            page_height: Page height in points
        """
        page = PDFPage(0, page_width, page_height)
        
        for elem_data in memory_elements:
            element = PDFElement(
                element_type=elem_data.get('type', 'text'),
                text=elem_data.get('text', ''),
                x=elem_data.get('x', 0),
                y=elem_data.get('y', 0),
                width=elem_data.get('width', 0),
                height=elem_data.get('height', 0),
                font_size=elem_data.get('font_size', 12),
                font_name=elem_data.get('font_name', ''),
                is_math=self._is_math_text(elem_data.get('text', ''))
            )
            page.add_element(element)
        
        page.sort_elements_by_position()
        self.document.add_page(page)
    
    def _is_math_text(self, text: str) -> bool:
        """Check if text is a math formula"""
        math_patterns = [
            r'\$.*?\$',  # Inline math $...$
            r'\\\[.*?\\\]',  # Display math \[...\]
            r'\\begin\{equation\}',  # Equation environment
            r'\\begin\{align\}',  # Align environment
            r'[_\^]',  # Subscript or superscript
            r'\\[a-zA-Z]+',  # LaTeX commands
        ]
        for pattern in math_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def generate_latex(self) -> str:
        """Generate complete LaTeX document from PDF elements"""
        lines = []
        
        # Document class
        lines.append(f"\\documentclass{{{self.document_class}}}")
        lines.append("")
        
        # Packages
        for package in self.packages:
            lines.append(f"\\usepackage{package}")
        lines.append("")
        
        # Geometry settings
        lines.append(r"\geometry{a4paper, margin=2cm}")
        lines.append("")
        
        # Custom preamble
        for line in self.preamble_lines:
            lines.append(line)
        if self.preamble_lines:
            lines.append("")
        
        # Document begin
        lines.append(r"\begin{document}")
        lines.append("")
        
        # Generate content for each page
        for page in self.document.pages:
            lines.extend(self._generate_page_content(page))
            lines.append("")
        
        # Document end
        lines.append(r"\end{document}")
        
        return "\n".join(lines)
    
    def _generate_page_content(self, page: PDFPage) -> List[str]:
        """Generate LaTeX content for a single page"""
        lines = []
        
        # Group elements by vertical position (paragraphs)
        paragraphs = self._group_elements_into_paragraphs(page.elements)
        
        for paragraph in paragraphs:
            if len(paragraph) == 1:
                # Single element paragraph
                element = paragraph[0]
                latex_code = self._convert_element_to_latex(element)
                lines.append(latex_code)
            else:
                # Multiple elements - join them
                texts = []
                for element in paragraph:
                    latex_code = self._convert_element_to_latex(element)
                    texts.append(latex_code)
                lines.append(" ".join(texts))
        
        return lines
    
    def _group_elements_into_paragraphs(self, elements: List[PDFElement]) -> List[List[PDFElement]]:
        """Group elements into paragraphs based on vertical spacing"""
        if not elements:
            return []
        
        paragraphs = []
        current_paragraph = [elements[0]]
        
        for i in range(1, len(elements)):
            prev_element = elements[i - 1]
            curr_element = elements[i]
            
            # Check vertical gap (if gap > 1.5 * line height, start new paragraph)
            vertical_gap = curr_element.y - (prev_element.y + prev_element.height)
            line_height = prev_element.height
            
            if vertical_gap > line_height * 0.5:
                # Start new paragraph
                paragraphs.append(current_paragraph)
                current_paragraph = [curr_element]
            else:
                # Continue current paragraph
                current_paragraph.append(curr_element)
        
        # Add last paragraph
        if current_paragraph:
            paragraphs.append(current_paragraph)
        
        return paragraphs
    
    def _convert_element_to_latex(self, element: PDFElement) -> str:
        """Convert a single element to LaTeX code"""
        text = element.text
        
        # Handle math formulas
        if element.is_math:
            return text
        
        # Escape special LaTeX characters
        text = self._escape_latex(text)
        
        # Handle font size changes
        if element.font_size and element.font_size != 12:
            size_commands = {
                8: r"\scriptsize",
                9: r"\footnotesize",
                10: r"\small",
                11: r"\normalsize",
                12: r"\normalsize",
                14: r"\large",
                17: r"\Large",
                20: r"\LARGE",
                25: r"\huge",
                30: r"\Huge"
            }
            # Find closest size
            closest_size = min(size_commands.keys(), key=lambda x: abs(x - element.font_size))
            if closest_size != 12:
                text = f"{size_commands[closest_size]} {{{text}}}"
        
        return text
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters"""
        # Characters that need escaping in LaTeX
        escape_chars = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        
        for char, escaped in escape_chars.items():
            text = text.replace(char, escaped)
        
        return text
    
    def add_package(self, package: str):
        """Add a package to the preamble"""
        if package not in self.packages:
            self.packages.append(package)
    
    def set_document_class(self, doc_class: str):
        """Set the document class"""
        self.document_class = doc_class
    
    def add_preamble_line(self, line: str):
        """Add a custom line to the preamble"""
        self.preamble_lines.append(line)


class PDFToLaTeXConverter:
    """High-level converter from PDF to LaTeX"""
    
    def __init__(self):
        self.reconstructor = LaTeXReconstructor()
    
    def convert_memory_elements(self, memory_elements: List[Dict[str, Any]]) -> str:
        """Convert memory elements to LaTeX code
        
        Args:
            memory_elements: List of element dictionaries from PDF canvas
            
        Returns:
            str: Generated LaTeX code
        """
        self.reconstructor.load_from_memory_elements(memory_elements)
        return self.reconstructor.generate_latex()
    
    def convert_with_changes(self, original_latex: str, 
                            memory_elements: List[Dict[str, Any]]) -> str:
        """Convert PDF elements to LaTeX, preserving original structure where possible
        
        Args:
            original_latex: Original LaTeX code
            memory_elements: Modified elements from PDF canvas
            
        Returns:
            str: Updated LaTeX code
        """
        # TODO: Implement intelligent merging of changes
        # For now, just generate from elements
        return self.convert_memory_elements(memory_elements)


if __name__ == "__main__":
    # Test PDF to LaTeX reconstruction
    test_elements = [
        {
            'id': 'text_0',
            'type': 'text',
            'text': 'Hello World!',
            'x': 100,
            'y': 100,
            'width': 100,
            'height': 12,
            'font_size': 12
        },
        {
            'id': 'text_1',
            'type': 'text',
            'text': '$E = mc^2$',
            'x': 100,
            'y': 130,
            'width': 80,
            'height': 14,
            'font_size': 14
        },
        {
            'id': 'text_2',
            'type': 'text',
            'text': 'This is a test document.',
            'x': 100,
            'y': 160,
            'width': 150,
            'height': 12,
            'font_size': 12
        }
    ]
    
    converter = PDFToLaTeXConverter()
    latex_code = converter.convert_memory_elements(test_elements)
    
    print("Generated LaTeX code:")
    print("=" * 50)
    print(latex_code)
    print("=" * 50)
