from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WebReleaseDocsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.guide = (ROOT / "docs" / "user-guide.md").read_text(encoding="utf-8")

    def test_readme_describes_the_runnable_web_product(self):
        for fact in (
            "python3 web_prototype/server.py",
            "http://127.0.0.1:8000/",
            "Web v1 capabilities",
            "Project save/open",
            "Export of conforming LaTeX",
            "PDF output through the browser print dialog",
        ):
            self.assertIn(fact, self.readme)

    def test_readme_does_not_present_stale_planning_claims(self):
        for stale_claim in (
            "Features (Planned)",
            "Under Evaluation",
            "Current Phase**: Initialization and Planning",
            "real-time PDF preview",
        ):
            self.assertNotIn(stale_claim, self.readme)

    def test_user_guide_matches_current_web_controls(self):
        for workflow in (
            "Enable **Multi-select**",
            "**Replace Image**",
            "edit its source in the **Content** field",
            "**Save Project**",
            "**Export LaTeX**",
            "**Import LaTeX**",
            "**Export PDF**",
        ):
            self.assertIn(workflow, self.guide)

        for stale_instruction in (
            "Ctrl+Click",
            "Compile to PDF with a single click",
            "TODO:",
            "python src/gui/main.py",
        ):
            self.assertNotIn(stale_instruction, self.guide)

    def test_documented_boundaries_are_explicit(self):
        for boundary in (
            "not arbitrary LaTeX documents",
            "not represented by the conforming LaTeX format",
            "not native TeX compilation",
            "Qt application is a secondary desktop validation route",
        ):
            self.assertIn(boundary, self.readme)


if __name__ == "__main__":
    unittest.main()
