# Lessons Learned

## 2026-04-11: Demo Evidence Compaction

### Key Lessons

1. **Evidence-Driven Development**: When claiming functionality exists, always compact evidence into:
   - Git diffs showing actual code changes
   - Reproducible manual verification steps
   - Screenshot or log evidence
   - Automated test results

2. **Clear Trigger Logic**: Documenting exactly when a fallback mechanism triggers helps avoid confusion:
   - What conditions must be met
   - What happens when triggered
   - How to verify it's working

3. **Transparent Labeling**: Always clearly label demo fallbacks as fallbacks, not complete solutions:
   - Avoids overpromising
   - Sets appropriate expectations
   - Makes it clear what's real vs. demo

4. **Reproducibility**: Step-by-step manual verification should be:
   - Short (4-6 steps maximum)
   - Exact commands
   - Clear expected outcomes
   - Easy to follow

5. **Screenshot Management**: Always:
   - Verify screenshot files actually exist
   - Document what the screenshot shows
   - Note if screenshots are user-provided or auto-generated

---

## 2026-04-11: Minimal Model-Driven Editing Demo

### Key Lessons

1. **Demo Fallback**: Implementing a demo fallback mechanism ensures that users always have something to interact with, even when the primary functionality (PDF element extraction) fails.

2. **Model-View Sync**: Ensuring that changes in the view layer (GUI) are properly synchronized with the model layer is crucial for a consistent editing experience.

3. **Backward Compatibility**: Maintaining compatibility with existing code paths while introducing new model-driven functionality helps reduce risk and allows for a smoother transition.

4. **Test Isolation**: Testing model synchronization logic separately from GUI components can help identify issues early and avoid complex test setups.

5. **Visual Feedback**: Providing immediate visual feedback when users modify elements enhances the user experience and confirms that changes are being applied.

6. **Initial Content**: Providing clear instructions and sample content in the initial document helps users understand how to interact with the application.

## 2026-04-11: Dependency Fix Round

### Key Lessons

1. **Version Constraints Matter**: Exact version constraints can cause installation failures on different platforms. Using version ranges (e.g., >=6.5,<6.8) provides better platform compatibility.

2. **Missing Dependencies**: Always check that all imported modules are declared in requirements.txt. The fitz module from PyMuPDF was missing from the original requirements.

3. **Platform-Specific Issues**: PyQt6 version 6.11.0 had no precompiled wheel for Linux aarch64, highlighting the importance of testing dependencies across platforms.

4. **Python Version Compatibility**: Ensure dependencies are compatible with the Python version being used. numpy==1.26.0 was not available for Python 3.14, requiring an update to numpy>=2.0.

5. **Dependency Verification**: Always verify dependencies after changes by running imports and basic functionality tests.

## 2026-04-11: Test Fix Round

### Key Lessons

1. **Mock Maintenance**: Mock objects need to be updated when the underlying code structure changes. The missing signals in mock objects were causing test failures.

2. **Test Boundaries**: Clearly define test boundaries, especially when dealing with GUI-dependent code. Non-GUI tests should avoid direct Qt dependencies.

3. **Test Naming**: Use descriptive test names that reflect the actual functionality being tested, not the expected state of incomplete code.

4. **Assertion Accuracy**: Test assertions must be updated to reflect the current state of the codebase, not outdated expectations.

5. **Import Paths**: Ensure import paths in tests match the actual project structure to avoid import errors.