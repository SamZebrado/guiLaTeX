from pathlib import Path
import unittest


INDEX_HTML = Path(__file__).resolve().parents[1] / "web_prototype" / "index.html"


class WebPersistentGroupingContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX_HTML.read_text(encoding="utf-8")

    def test_group_and_ungroup_controls_mutate_project_model(self):
        for contract in (
            'id="group-button"',
            'id="ungroup-button"',
            "function createGroupFromSelection()",
            "function ungroupSelection()",
            "element.groupId = groupId",
            "delete element.groupId",
            "beginHistoryTransaction('成组')",
            "beginHistoryTransaction('解组')",
        ):
            self.assertIn(contract, self.source)

    def test_persistent_group_is_an_atomic_selection_and_move_target(self):
        for contract in (
            "function getPersistentGroupId(elements)",
            "candidate.groupId === element.groupId",
            "element.groupId === clickedElement.groupId",
            "elementsToDrag = persistentGroup || [clickedElement]",
            "draggedElements = selectedElements.map(element => ({",
        ):
            self.assertIn(contract, self.source)

    def test_group_rotation_uses_common_center_and_preserves_member_rotation(self):
        for contract in (
            "rotateAsPersistentGroup = Boolean(getPersistentGroupId(selectedElements))",
            "function getGroupRotationCenter(elements)",
            "elements.reduce((sum, element) => sum + element.x + element.width / 2",
            "? getGroupRotationCenter(selectedElements)",
            "rotationCenter.modelX",
            "rotationCenter.modelY",
            "rotatedCenterX",
            "rotatedCenterY",
            "element.rotation = Math.round(newRotation)",
        ):
            self.assertIn(contract, self.source)

    def test_group_selection_bounds_use_rotated_visual_extents(self):
        for contract in (
            "const rect = elementDiv.getBoundingClientRect();",
            "left: (rect.left - paperRect.left) / scaleX",
            "right: (rect.right - paperRect.left) / scaleX",
            "selectionBox.dataset.pivotX",
            "selectionBox.dataset.pivotY",
        ):
            self.assertIn(contract, self.source)

    def test_project_save_preserves_group_but_conforming_ir_does_not_claim_it(self):
        self.assertIn("const dataStr = JSON.stringify(model, null, 2);", self.source)
        export_start = self.source.index("function exportToIR()")
        export_end = self.source.index("function preparePrintLayout()", export_start)
        self.assertNotIn("groupId", self.source[export_start:export_end])

    def test_copy_paste_remaps_group_identity(self):
        for contract in (
            "const pastedGroupIds = new Map();",
            "pastedGroupIds.set(newElement.groupId",
            "newElement.groupId = pastedGroupIds.get(newElement.groupId)",
        ):
            self.assertIn(contract, self.source)


if __name__ == "__main__":
    unittest.main()
