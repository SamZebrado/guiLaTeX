"""Letter export regression and shared legacy A4 compatibility."""
import unittest
import re

from export_core import normalize_web_model_to_ir, normalize_qt_model_to_ir
from export_core import export_ir_to_latex, import_own_exported_tex_to_ir
from export_core.latex_exporter import LatexExporter
from web_prototype.server import export_web_model_to_tex, import_conforming_tex_to_web


class WebPageContractTests(unittest.TestCase):
    def setUp(self):
        self.model = {"elements": [{"id": "position", "type": "textbox",
            "content": "Letter", "x": 12, "y": 34, "width": 80,
            "height": 20, "rotation": 17, "layer": 3, "visible": True}]}

    def test_web_geometry_metadata_and_y_use_letter(self):
        ir = normalize_web_model_to_ir(self.model)
        self.assertEqual(ir["page_contract"], {"format": "letter"})
        tex = export_web_model_to_tex(self.model)
        self.assertIn(r"\usepackage[letterpaper,margin=0mm]{geometry}", tex)
        self.assertIn("Letter (215.9mm × 279.4mm)", tex)
        self.assertNotIn("A4", tex)
        position = re.search(r"at \(12mm, ([0-9.]+)mm\)", tex)
        self.assertIsNotNone(position)
        self.assertAlmostEqual(float(position.group(1)), 279.4 - 34)
        self.assertEqual(import_own_exported_tex_to_ir(tex), ir)
        restored = import_conforming_tex_to_web(tex)["elements"][0]
        for field in ("id", "content", "x", "y", "width", "height", "rotation"):
            self.assertEqual(restored[field], self.model["elements"][0][field])

    def test_legacy_and_qt_keep_a4(self):
        qt = normalize_qt_model_to_ir(self.model)
        self.assertNotIn("page_contract", qt)
        for ir in (qt, normalize_web_model_to_ir(self.model)):
            if "page_contract" in ir:
                ir.pop("page_contract")
            tex = export_ir_to_latex(ir)
            self.assertIn("a4paper,margin=0mm", tex)
            self.assertIn("A4 (210mm × 297mm)", tex)
            self.assertIn("263", tex)
            self.assertEqual(import_own_exported_tex_to_ir(tex), ir)

    def test_reused_exporter_resolves_each_document(self):
        exporter = LatexExporter()
        self.assertIn("letterpaper", exporter.export(normalize_web_model_to_ir(self.model)))
        self.assertIn("a4paper", exporter.export(normalize_qt_model_to_ir(self.model)))

    def test_unknown_page_contract_fails_explicitly(self):
        with self.assertRaisesRegex(ValueError, "page_contract"):
            export_ir_to_latex({"elements": [], "page_contract": {"format": "unknown"}})
