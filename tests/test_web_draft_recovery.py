"""Source contract guards; real browser behavior is covered by the Chromium test."""
from pathlib import Path
import unittest


class WebDraftRecoveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (Path(__file__).resolve().parents[1] / 'web_prototype/index.html').read_text()

    def test_checkpoint_excludes_only_transient_selection(self):
        self.assertIn('snapshot.elements.forEach(element => delete element.selected)', self.source)
        self.assertIn('return editableSnapshot() !== cleanCheckpoint', self.source)
        self.assertIn('cleanCheckpoint = null; // Import creates a new, unsaved editable project.', self.source)

    def test_single_versioned_full_model_draft_and_explicit_recovery(self):
        for token in ("const DRAFT_KEY = 'guilatex.web.draft.v1'", 'version: 1, model: cloneModel()',
                      "'recover-draft-button'", "'discard-draft-button'", 'dialog.showModal()',
                      "dialog.addEventListener('cancel', event => event.preventDefault())"):
            self.assertIn(token, self.source)

    def test_dirty_unload_and_replacement_protected(self):
        self.assertIn("window.addEventListener('beforeunload', event =>", self.source)
        self.assertIn("event.returnValue = ''", self.source)
        self.assertEqual(self.source.count('if (!confirmProjectReplacement()) return;'), 3)

    def test_draft_accepts_actual_conforming_import_text_types(self):
        self.assertIn("['textbox', 'title', 'author', 'paragraph', 'image', 'equation'].includes(element.type)", self.source)

    def test_storage_failure_visible_and_save_schema_unchanged(self):
        self.assertIn('本地草稿不可用', self.source)
        self.assertIn("draftStatus.setAttribute('role', 'status')", self.source)
        self.assertIn('const dataStr = JSON.stringify(model, null, 2);', self.source)
        self.assertIn('URL.revokeObjectURL(url);\n            markProjectClean();', self.source)


if __name__ == '__main__':
    unittest.main()
