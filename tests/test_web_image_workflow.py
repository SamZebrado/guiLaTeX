from pathlib import Path
import unittest


INDEX_HTML = Path(__file__).resolve().parents[1] / "web_prototype" / "index.html"


class WebImageWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX_HTML.read_text(encoding="utf-8")

    def test_insert_and_replace_controls_use_a_bounded_raster_picker(self):
        for contract in (
            'id="insert-image-button"',
            'id="replace-image-button"',
            'id="image-file-input"',
            'accept="image/png,image/jpeg,image/webp,image/gif"',
            "const MAX_IMAGE_BYTES = 2 * 1024 * 1024;",
            "SUPPORTED_IMAGE_TYPES.has(file.type)",
        ):
            self.assertIn(contract, self.source)

    def test_image_file_is_decoded_before_model_mutation(self):
        for contract in (
            "function readImageFile(file)",
            "function decodeImage(dataUrl)",
            "await readImageFile(file)",
            "await decodeImage(dataUrl)",
            "imageNaturalWidth: dimensions.width",
            "imageNaturalHeight: dimensions.height",
        ):
            self.assertIn(contract, self.source)

    def test_insert_and_replace_are_history_transactions(self):
        self.assertIn("beginHistoryTransaction('插入图片')", self.source)
        self.assertIn("beginHistoryTransaction('替换图片')", self.source)
        self.assertIn("commitHistoryTransaction();", self.source)

    def test_raster_data_is_rendered_and_project_serialized(self):
        for contract in (
            "element.imageDataUrl",
            "document.createElement('img')",
            "image.style.objectFit = 'contain'",
            "const dataStr = JSON.stringify(model, null, 2);",
        ):
            self.assertIn(contract, self.source)

    def test_conforming_ir_uses_filename_without_embedding_data_url(self):
        export_start = self.source.index("function exportToIR()")
        export_end = self.source.index("function preparePrintLayout()", export_start)
        export_source = self.source[export_start:export_end]
        self.assertIn("content: element.content", export_source)
        self.assertNotIn("imageDataUrl", export_source)


if __name__ == "__main__":
    unittest.main()
