# Lessons Learned

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