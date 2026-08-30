from pathlib import Path
import unittest


INDEX_HTML = Path(__file__).resolve().parents[1] / "web_prototype" / "index.html"


class WebPdfLayoutContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX_HTML.read_text(encoding="utf-8")

    def test_print_css_uses_model_box_without_editor_chrome(self):
        for contract in (
            "box-sizing: border-box;",
            "padding: 0 !important;",
            "border: none !important;",
            "overflow: hidden;",
            "size: letter;",
        ):
            self.assertIn(contract, self.source)

    def test_print_lifecycle_fits_then_restores_text(self):
        for contract in (
            "function preparePrintLayout()",
            "function restorePrintLayout()",
            "window.addEventListener('beforeprint', preparePrintLayout);",
            "window.addEventListener('afterprint', restorePrintLayout);",
            "elementDiv.scrollWidth <= elementDiv.clientWidth",
            "elementDiv.scrollHeight <= elementDiv.clientHeight",
            "printStyleSnapshots.set(element.id",
            "if (!preparePrintLayout())",
            "部分文字无法在当前文本框内完整打印",
        ):
            self.assertIn(contract, self.source)


if __name__ == "__main__":
    unittest.main()
