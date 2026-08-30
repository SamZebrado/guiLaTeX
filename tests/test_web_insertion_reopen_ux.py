from pathlib import Path
import unittest


INDEX_HTML = Path(__file__).resolve().parents[1] / "web_prototype" / "index.html"


class WebInsertionReopenUxContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX_HTML.read_text(encoding="utf-8")

    def test_image_and_equation_share_available_placement_search(self):
        for contract in (
            "function boxesOverlap(first, second, padding = 12)",
            "function findAvailablePlacement(width, height)",
            "!occupied.some(box => boxesOverlap(candidate, box))",
            "const placement = findAvailablePlacement(width, height);",
            "const placement = findAvailablePlacement(240, 60);",
            "x: placement.x",
            "y: placement.y",
        ):
            self.assertIn(contract, self.source)

    def test_empty_document_layer_assignment_is_finite(self):
        self.assertGreaterEqual(self.source.count("const minLayerId = model.elements.length"), 2)
        self.assertGreaterEqual(self.source.count("layerId: minLayerId - 1"), 2)

    def test_property_panel_has_one_complete_selection_sync_entrypoint(self):
        for contract in (
            "function syncPropertyPanelFromSelection()",
            "contentInput.value = element.content || ''",
            "fontSizeSlider.value = element.fontSize || 16",
            "rotationSlider.value = element.rotation || 0",
            "layerInput.value = element.layerId ?? ''",
        ):
            self.assertIn(contract, self.source)

    def test_open_project_syncs_selected_object_controls(self):
        open_start = self.source.index("fileInput.addEventListener('change'")
        open_end = self.source.index("// Import LaTeX", open_start)
        open_source = self.source[open_start:open_end]
        self.assertIn("clearModelHistory();", open_source)
        self.assertIn("syncPropertyPanelFromSelection();", open_source)


if __name__ == "__main__":
    unittest.main()
