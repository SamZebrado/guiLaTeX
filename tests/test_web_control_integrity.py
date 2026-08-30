from pathlib import Path
import unittest


INDEX_HTML = Path(__file__).resolve().parents[1] / "web_prototype" / "index.html"


class WebControlIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX_HTML.read_text(encoding="utf-8")

    def test_visible_geometry_inputs_mutate_one_selected_object(self):
        for contract in (
            "function updateSelectedGeometry()",
            "selectedElements.length !== 1",
            "element.x = values.x",
            "element.y = values.y",
            "element.width = Math.max(1, values.width)",
            "element.height = Math.max(1, values.height)",
            "beginHistoryTransaction('修改几何')",
            "control.addEventListener('input', updateSelectedGeometry)",
            "control.addEventListener('change', commitHistoryTransaction)",
        ):
            self.assertIn(contract, self.source)

    def test_fake_screenshot_export_action_is_not_advertised(self):
        self.assertNotIn('id="export-screenshot-button"', self.source)
        self.assertNotIn("请使用浏览器截图功能手动截图", self.source)


if __name__ == "__main__":
    unittest.main()
