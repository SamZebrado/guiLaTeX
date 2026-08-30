from pathlib import Path
import unittest

from web_prototype.server import (
    MAX_REQUEST_BYTES,
    export_web_model_to_tex,
    import_conforming_tex_to_web,
)


INDEX_HTML = Path(__file__).resolve().parents[1] / "web_prototype" / "index.html"


class WebLatexApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX_HTML.read_text(encoding="utf-8")

    def test_web_ui_uses_same_origin_core_routes(self):
        for contract in (
            "fetch('/api/export-latex'",
            "fetch('/api/import-latex'",
            "link.download = 'guilatex_export.tex'",
            "model = payload.model",
            "clearModelHistory();",
            "syncPropertyPanelFromSelection();",
        ):
            self.assertIn(contract, self.source)

    def test_old_manual_shell_instruction_is_removed_from_product_buttons(self):
        self.assertNotIn("python3 web_to_core_bridge.py <input_ir.json> <output.tex>", self.source)
        self.assertNotIn("python3 core_to_web_bridge.py <latex_file> <output_json>", self.source)

    def test_api_roundtrip_reuses_export_core_and_web_adapter(self):
        model = {
            "elements": [{
                "id": "api-equation",
                "type": "equation",
                "content": r"\frac{x}{2}",
                "page": 1,
                "x": 12,
                "y": 34,
                "width": 80,
                "height": 30,
                "rotation": 5,
                "layer": 2,
                "font_size": 18,
                "visible": True,
            }]
        }
        tex = export_web_model_to_tex(model)
        restored = import_conforming_tex_to_web(tex)
        equation = restored["elements"][0]
        self.assertIn(r"$\frac{x}{2}$", tex)
        self.assertEqual(equation["type"], "equation")
        self.assertEqual(equation["content"], r"\frac{x}{2}")
        self.assertEqual(equation["rotation"], 5)

    def test_import_rejects_nonconforming_tex(self):
        with self.assertRaisesRegex(ValueError, "不符合"):
            import_conforming_tex_to_web(r"\documentclass{article}\begin{document}x\end{document}")

    def test_server_request_limit_is_bounded(self):
        self.assertEqual(MAX_REQUEST_BYTES, 5 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
