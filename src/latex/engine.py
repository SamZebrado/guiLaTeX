#!/usr/bin/env python3
"""
guiLaTeX - LaTeX Engine Integration

Integration with LaTeX engine for compilation and preview
"""

import os
import subprocess
import tempfile
import shutil


class LaTeXEngine:
    """LaTeX engine integration"""
    
    def __init__(self):
        self.latex_cmd = self._find_latex_command()
        self.pdf_viewer = self._find_pdf_viewer()
    
    def _find_latex_command(self):
        """Find LaTeX command in system path"""
        commands = ['pdflatex', 'xelatex', 'lualatex']
        for cmd in commands:
            if shutil.which(cmd):
                return cmd
        return None
    
    def _find_pdf_viewer(self):
        """Find PDF viewer in system path"""
        viewers = ['open', 'evince', 'okular', 'acroread']
        for viewer in viewers:
            if shutil.which(viewer):
                return viewer
        return None
    
    def is_available(self):
        """Check if LaTeX is available"""
        return self.latex_cmd is not None
    
    def compile(self, latex_code, output_dir=None, output_path=None, keep_temp=False):
        """Compile LaTeX code to PDF
        
        Args:
            latex_code (str): LaTeX code to compile
            output_dir (str, optional): Output directory
            output_path (str, optional): Exact output PDF path
            keep_temp (bool): Whether to keep temporary directory after compilation
            
        Returns:
            tuple: (success, pdf_path, log, temp_dir)
        """
        if not self.is_available():
            return False, None, "LaTeX engine not found", None
        
        # Create temporary directory if no output directory provided
        if output_dir is None and output_path is None:
            temp_dir = tempfile.mkdtemp()
        elif output_path:
            # Use directory from output_path
            temp_dir = os.path.dirname(output_path)
            os.makedirs(temp_dir, exist_ok=True)
        else:
            temp_dir = output_dir
            os.makedirs(temp_dir, exist_ok=True)
        
        # Write LaTeX code to file
        tex_file = os.path.join(temp_dir, 'document.tex')
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_code)
        
        # Determine PDF output path
        if output_path:
            pdf_file = output_path
        else:
            pdf_file = os.path.join(temp_dir, 'document.pdf')
        
        log_file = os.path.join(temp_dir, 'document.log')
        
        try:
            # Run LaTeX compilation
            result = subprocess.run(
                [self.latex_cmd, '-interaction=nonstopmode', 'document.tex'],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            # Check if compilation succeeded
            success = os.path.exists(pdf_file)
            
            # Read log
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    log = f.read()
            else:
                log = result.stdout + '\n' + result.stderr
            
            # Clean up temporary directory if not keeping it
            if not keep_temp and output_dir is None and output_path is None and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                temp_dir = None
            
            return success, pdf_file if success else None, log, temp_dir
            
        except Exception as e:
            # Clean up on error
            if output_dir is None and output_path is None and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return False, None, f"Error compiling LaTeX: {str(e)}", None
    
    def generate_basic_latex(self, elements):
        """Generate basic LaTeX code from elements
        
        Args:
            elements (list): List of LaTeXElement objects
            
        Returns:
            str: Generated LaTeX code
        """
        latex_code = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{a4paper, margin=2cm}
\begin{document}

"""
        
        for element in elements:
            if hasattr(element, 'text'):
                # Handle text elements
                if '$' in element.text:
                    # Math formula
                    latex_code += element.text + '\\\\\n\n'
                else:
                    # Regular text
                    latex_code += element.text + '\\\\\n\n'
        
        latex_code += r"""
\end{document}
"""
        
        return latex_code
    
    def view_pdf(self, pdf_path):
        """View PDF file
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            bool: Success
        """
        if not self.pdf_viewer or not os.path.exists(pdf_path):
            return False
        
        try:
            subprocess.run([self.pdf_viewer, pdf_path], check=False)
            return True
        except Exception:
            return False


class LaTeXGenerator:
    """Generate LaTeX code from visual elements"""
    
    def generate(self, elements):
        """Generate LaTeX code from elements
        
        Args:
            elements (list): List of LaTeXElement objects
            
        Returns:
            str: Generated LaTeX code
        """
        engine = LaTeXEngine()
        return engine.generate_basic_latex(elements)


class LaTeXParser:
    """Parse LaTeX code to visual elements"""
    
    def parse(self, latex_code):
        """Parse LaTeX code to elements
        
        Args:
            latex_code (str): LaTeX code
            
        Returns:
            list: List of LaTeXElement objects
        """
        # TODO: Implement LaTeX parsing
        # This is a complex task that would require a proper LaTeX parser
        return []


if __name__ == "__main__":
    # Test LaTeX engine
    engine = LaTeXEngine()
    print(f"LaTeX engine found: {engine.latex_cmd}")
    print(f"PDF viewer found: {engine.pdf_viewer}")
    
    # Test basic compilation
    if engine.is_available():
        test_latex = r"""\documentclass{article}
\begin{document}
Hello World!
$E = mc^2$
\end{document}
"""
        
        success, pdf_path, log, temp_dir = engine.compile(test_latex)
        print(f"Compilation success: {success}")
        if success:
            print(f"PDF generated at: {pdf_path}")
            engine.view_pdf(pdf_path)
            # Clean up temp directory
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"Cleaned up temp directory: {temp_dir}")
        else:
            print(f"Compilation log:\n{log}")
