#!/usr/bin/env python3
"""
Test cases for LaTeX engine
"""

import pytest
import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from latex.engine import LaTeXEngine, LaTeXGenerator


class TestLaTeXEngine:
    """Test LaTeX engine functionality"""
    
    def test_latex_engine_initialization(self):
        """Test LaTeX engine initialization"""
        engine = LaTeXEngine()
        assert engine is not None
    
    def test_latex_engine_availability(self):
        """Test if LaTeX engine is available"""
        engine = LaTeXEngine()
        # This should return True on systems with LaTeX installed
        # For CI environments, this might return False
        assert isinstance(engine.is_available(), bool)
    
    def test_generate_basic_latex(self):
        """Test basic LaTeX generation"""
        engine = LaTeXEngine()
        
        # Create mock elements
        class MockElement:
            def __init__(self, text):
                self.text = text
        
        elements = [
            MockElement("Hello World"),
            MockElement("$E = mc^2$")
        ]
        
        latex_code = engine.generate_basic_latex(elements)
        assert isinstance(latex_code, str)
        assert "Hello World" in latex_code
        assert "$E = mc^2$" in latex_code
        assert "\\documentclass{article}" in latex_code
        assert "\\end{document}" in latex_code
    
    @pytest.mark.skipif(not LaTeXEngine().is_available(), reason="LaTeX not available")
    def test_compile_basic_latex(self):
        """Test basic LaTeX compilation"""
        engine = LaTeXEngine()
        
        test_latex = r"""\documentclass{article}
\begin{document}
Hello World!
$E = mc^2$
\end{document}
"""
        
        success, pdf_path, log, temp_dir = engine.compile(test_latex, keep_temp=True)
        assert success is True
        assert pdf_path is not None
        assert os.path.exists(pdf_path)
        # Clean up temp directory
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)


class TestLaTeXGenerator:
    """Test LaTeX generator functionality"""
    
    def test_generator_initialization(self):
        """Test LaTeX generator initialization"""
        generator = LaTeXGenerator()
        assert generator is not None
    
    def test_generate_latex(self):
        """Test LaTeX generation"""
        generator = LaTeXGenerator()
        
        # Create mock elements
        class MockElement:
            def __init__(self, text):
                self.text = text
        
        elements = [
            MockElement("Test Text"),
            MockElement("$x^2 + y^2 = z^2$")
        ]
        
        latex_code = generator.generate(elements)
        assert isinstance(latex_code, str)
        assert "Test Text" in latex_code
        assert "$x^2 + y^2 = z^2$" in latex_code


if __name__ == "__main__":
    pytest.main([__file__])
