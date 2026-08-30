from pathlib import Path
import unittest


INDEX_HTML = Path(__file__).resolve().parents[1] / "web_prototype" / "index.html"


class WebUndoRedoContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX_HTML.read_text(encoding="utf-8")

    def test_history_controls_and_shortcuts_are_present(self):
        for contract in (
            'id="undo-button"',
            'id="redo-button"',
            "function undoModelChange()",
            "function redoModelChange()",
            "event.metaKey || event.ctrlKey",
            "key === 'z'",
            "key === 'y'",
        ):
            self.assertIn(contract, self.source)

    def test_history_is_bounded_and_redo_is_invalidated(self):
        self.assertIn("const HISTORY_LIMIT = 100;", self.source)
        self.assertIn("if (undoStack.length > HISTORY_LIMIT) undoStack.shift();", self.source)
        self.assertIn("redoStack.length = 0;", self.source)

    def test_continuous_pointer_edits_use_transactions(self):
        for label in ("移动对象", "调整对象大小", "旋转对象"):
            self.assertIn(f"beginHistoryTransaction('{label}')", self.source)
        for stop_handler in ("function stopDrag()", "function stopResize()", "function stopRotate()"):
            start = self.source.index(stop_handler)
            self.assertIn("commitHistoryTransaction();", self.source[start:start + 180])


if __name__ == "__main__":
    unittest.main()
