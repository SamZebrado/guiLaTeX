from pathlib import Path
import unittest

from export_core import export_ir_to_latex, import_own_exported_tex_to_ir, normalize_web_model_to_ir


INDEX_HTML = Path(__file__).resolve().parents[1] / "web_prototype" / "index.html"


class WebEquationWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX_HTML.read_text(encoding="utf-8")

    def test_equation_insert_control_and_model_object_exist(self):
        for contract in (
            'id="insert-equation-button"',
            "beginHistoryTransaction('插入公式')",
            "type: 'equation'",
            "content: 'E = mc^2'",
            "id: `equation-${Date.now()}-${++equationSequence}`",
        ):
            self.assertIn(contract, self.source)

    def test_renderer_is_local_safe_mathml_not_remote_or_inner_html(self):
        for contract in (
            "const MATHML_NS = 'http://www.w3.org/1998/Math/MathML';",
            "function renderEquationMathML(source)",
            "document.createElementNS(MATHML_NS, tag)",
            "preview.dataset.renderState = 'mathml'",
            "fallback.textContent = source || '空公式'",
        ):
            self.assertIn(contract, self.source)
        renderer_start = self.source.index("function renderEquationMathML(source)")
        renderer_end = self.source.index("function createSelectionBox", renderer_start)
        renderer = self.source[renderer_start:renderer_end]
        self.assertNotIn("innerHTML", renderer)
        self.assertNotIn("https://", renderer)

    def test_bounded_tex_subset_includes_fraction_root_scripts_and_symbols(self):
        for contract in (
            "command === 'frac'",
            "command === 'sqrt'",
            "mathNode('msubsup')",
            "mathNode('msub')",
            "mathNode('msup')",
            "alpha: ['mi', 'α']",
        ):
            self.assertIn(contract, self.source)

    def test_existing_formula_alias_and_new_equation_share_render_path(self):
        self.assertIn("element.type === 'equation' || element.role === 'formula'", self.source)
        self.assertIn("div.appendChild(renderEquationMathML(element.content));", self.source)

    def test_equation_remains_raw_latex_in_conforming_ir(self):
        export_start = self.source.index("function exportToIR()")
        export_end = self.source.index("function preparePrintLayout()", export_start)
        export_source = self.source[export_start:export_end]
        self.assertIn("type: element.role || element.type", export_source)
        self.assertIn("content: element.content", export_source)

    def test_complex_equation_content_survives_core_export_roundtrip(self):
        content = r"\frac{a_1+b^2}{\sqrt{\alpha}}"
        web_model = {
            "elements": [{
                "id": "equation-e2e",
                "type": "equation",
                "content": content,
                "page": 1,
                "x": 10,
                "y": 20,
                "width": 80,
                "height": 30,
                "rotation": 0,
                "layer": 1,
            }]
        }
        normalized = normalize_web_model_to_ir(web_model)
        tex = export_ir_to_latex(normalized)
        restored = import_own_exported_tex_to_ir(tex)
        self.assertIn(f"${content}$", tex)
        self.assertEqual(restored["elements"][0]["content"], content)


if __name__ == "__main__":
    unittest.main()
