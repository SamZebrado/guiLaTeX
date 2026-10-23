"""Letter export regression and shared legacy A4 compatibility."""
import unittest
import re

from export_core import normalize_web_model_to_ir, normalize_qt_model_to_ir
from export_core import export_ir_to_latex, import_own_exported_tex_to_ir
from export_core.latex_exporter import LatexExporter
from export_core import COORDINATE_SYSTEM
from export_core.page_contract import WEB_CANVAS_PX, web_geometry_to_mm
from web_prototype.core_to_web_bridge import ir_to_web_model
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
        position = re.search(r"at \(([0-9.]+)mm, ([0-9.]+)mm\)", tex)
        self.assertIsNotNone(position)
        self.assertAlmostEqual(float(position.group(1)), 12 * 215.9 / 816)
        self.assertAlmostEqual(float(position.group(2)), 279.4 - 34 * 279.4 / 1056)
        self.assertEqual(import_own_exported_tex_to_ir(tex), ir)
        restored = import_conforming_tex_to_web(tex)["elements"][0]
        for field in ("id", "content", "x", "y", "width", "height", "rotation"):
            if field in ("x", "y", "width", "height"):
                self.assertAlmostEqual(restored[field], self.model["elements"][0][field], places=9)
            else:
                self.assertEqual(restored[field], self.model["elements"][0][field])

    def test_legacy_and_qt_keep_a4(self):
        qt = normalize_qt_model_to_ir(self.model)
        self.assertNotIn("page_contract", qt)
        for ir in (qt, {"elements": qt["elements"]}):
            tex = export_ir_to_latex(ir)
            self.assertIn("a4paper,margin=0mm", tex)
            self.assertIn("A4 (210mm × 297mm)", tex)
            self.assertIn("263", tex)
            self.assertEqual(import_own_exported_tex_to_ir(tex), ir)

    def test_reused_exporter_resolves_each_document(self):
        exporter = LatexExporter()
        self.assertIn("letterpaper", exporter.export(normalize_web_model_to_ir(self.model)))
        self.assertIn("a4paper", exporter.export(normalize_qt_model_to_ir(self.model)))
        self.assertIn("letterpaper", exporter.export(normalize_web_model_to_ir(self.model)))

    def test_canvas_origin_edges_and_representative_object(self):
        self.assertEqual(WEB_CANVAS_PX, (816, 1056))
        for x, y, expected_x, expected_y in ((0, 0, 0, 0), (816, 1056, 215.9, 279.4)):
            model = {"elements": [{**self.model["elements"][0], "x": x, "y": y,
                                   "width": 816, "height": 1056}]}
            ir = normalize_web_model_to_ir(model)
            element = ir["elements"][0]
            self.assertAlmostEqual(element["x"], expected_x)
            self.assertAlmostEqual(element["y"], expected_y)
            self.assertAlmostEqual(element["width"], 215.9)
            self.assertAlmostEqual(element["height"], 279.4)
            restored = ir_to_web_model(ir)["elements"][0]
            for field in ("x", "y", "width", "height"):
                self.assertAlmostEqual(restored[field], model["elements"][0][field], places=9)
        default = web_geometry_to_mm({"x": 100, "y": 280, "width": 400, "height": 50})
        self.assertAlmostEqual(default["width"], 105.83333333333333)
        self.assertGreater(279.4 - default["y"], 0)

    def test_already_canonical_browser_ir_is_not_converted_twice(self):
        ir = normalize_web_model_to_ir(self.model)
        self.assertEqual(normalize_web_model_to_ir(ir), ir)

    def test_coordinate_authority_is_page_neutral(self):
        self.assertEqual(COORDINATE_SYSTEM["unit"], "millimeters (mm)")
        self.assertIn("page_contract", COORDINATE_SYSTEM["page_size"])
        self.assertNotIn("210mm", COORDINATE_SYSTEM["page_size"])
        self.assertEqual(COORDINATE_SYSTEM["rotation_direction"], "clockwise")

    def test_legacy_ir_is_mm_when_imported_to_web(self):
        qt = normalize_qt_model_to_ir(self.model)
        restored = ir_to_web_model(qt)["elements"][0]
        self.assertAlmostEqual(restored["x"], 12 * 816 / 215.9)

    def test_unknown_page_contract_fails_explicitly(self):
        with self.assertRaisesRegex(ValueError, "page_contract"):
            export_ir_to_latex({"elements": [], "page_contract": {"format": "unknown"}})
        with self.assertRaisesRegex(ValueError, "geometry_unit"):
            normalize_web_model_to_ir({"elements": [], "geometry_unit": "inches"})
