import json
from pathlib import Path
import unittest
from export_core import normalize_qt_model_to_ir, export_ir_to_latex
from web_prototype.server import import_conforming_tex_to_web

class LegacyGeometryTests(unittest.TestCase):
    def test_baseline_web_fixture_requires_explicit_origin_and_preserves_px(self):
        root=Path(__file__).parent/'fixtures'
        tex=(root/'pre_r1_web_baseline.tex').read_text()
        with self.assertRaisesRegex(ValueError,'LEGACY_GEOMETRY_AMBIGUOUS'):
            import_conforming_tex_to_web(tex)
        model=import_conforming_tex_to_web(tex,'web-px')
        expected=json.loads((root/'pre_r1_web_baseline.json').read_text())['web_geometry']
        for actual,original in zip(model['elements'],expected):
            for field in ('x','y','width','height'):
                self.assertAlmostEqual(actual[field],original[field],places=9)

    def test_legacy_qt_mm_is_not_guessed_as_web_px(self):
        ir=normalize_qt_model_to_ir({'elements':[{'id':'qt','type':'textbox','x':12,'y':34,'width':80,'height':20}]})
        tex=export_ir_to_latex(ir)
        self.assertIn('a4paper',tex)
        with self.assertRaisesRegex(ValueError,'LEGACY_GEOMETRY_AMBIGUOUS'):
            import_conforming_tex_to_web(tex)
        model=import_conforming_tex_to_web(tex,'ir-mm')
        self.assertAlmostEqual(model['elements'][0]['x'],12*816/215.9)
