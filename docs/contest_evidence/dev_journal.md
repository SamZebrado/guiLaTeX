# Development Journal

## 2026-04-11: Dependency Fix Round

### Summary

Fixed dependency declarations in requirements.txt to improve platform compatibility and resolve missing dependencies.

### Changes Made

**File: requirements.txt**
- Added PyMuPDF>=1.20 to fix missing fitz dependency
- Changed PyQt6==6.11.0 to PyQt6>=6.5,<6.8 for better platform compatibility
- Changed pytest-qt==4.2.0 to pytest-qt>=4.0 for better pytest 9 compatibility
- Changed numpy==1.26.0 to numpy>=2.0 for Python 3.14 compatibility

### Verification

**Local Code / Mac + venv Environment:**
- Python version: 3.14.2
- `pip install -r requirements.txt`: SUCCESS
- `import fitz`: SUCCESS
- `from PyQt6.QtWidgets import QApplication`: SUCCESS

### Notes

The dependency fixes ensure that the project can be installed and basic imports work in the local environment. The version ranges were chosen to provide better platform compatibility while maintaining compatibility with the current codebase.

## 2026-04-11: Test Fix Round

### Summary

Fixed failing tests by updating mock structures and test assertions to reflect current code state.

### Changes Made

**File: tests/test_main_model_integration_no_qt.py**
- Added MockSignal class to simulate Qt signals
- Updated MockPDFCanvas to include element_selected and element_modified signals
- Updated MockQWidget to include element_changed signal property
- Fixed model import path to match main.py

**File: tests/test_integration.py**
- Renamed test_current_pdf_canvas_uses_old_path to test_current_pdf_canvas_has_backward_compatibility
- Renamed test_no_integration_yet to test_model_integration_exists
- Updated assertions to reflect current code state

### Verification

**Local Code / Mac + venv Environment:**
- Non-GUI tests: All passing
- Test discovery: SUCCESS

### Notes

The test fixes ensure that non-GUI tests pass in the local environment, providing a solid foundation for future development. Mock objects were updated to properly simulate Qt signals, and test assertions were updated to reflect the current codebase structure.