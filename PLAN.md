# PLAN

## Goal
Develop guiLaTeX - a visual LaTeX editor with drag-and-drop functionality similar to Photoshop/Word, enabling users to visually manipulate LaTeX elements without writing code.

## Agent Identity
- **guiLaTeX-Starter**: Core development agent responsible for architecture, PDF editing research, and foundational features
- Collaboration via local files and shared skill protocols

## Milestones

### Phase 1: Foundation (Week 1-2)
1. [x] Technology stack decision
   - Target: Choose between Qt (C++/Python) vs Electron
   - Verification: Document decision rationale
   - Files: docs/architecture.md

2. [x] Project structure setup
   - Target: Create basic project structure
   - Verification: Directory structure exists
   - Files: src/, tests/, docs/, assets/

3. [x] Development environment setup (PyQt6)
   - Target: Install PyQt6 and dependencies
   - Verification: Can import PyQt6 in Python
   - Files: requirements.txt

4. [x] Development environment setup
   - Target: Configure build system and dependencies
   - Verification: Build system works
   - Files: CMakeLists.txt or package.json

### Phase 2: Core Architecture (Week 3-4)
5. [x] Core architecture design
   - Target: Design modular architecture
   - Verification: Architecture document complete
   - Files: docs/architecture.md

6. [x] GUI framework setup
   - Target: Basic window and canvas
   - Verification: Application launches
   - Files: src/gui/main.py

7. [x] LaTeX engine integration
   - Target: Integrate TeX Live for compilation
   - Verification: Can compile basic LaTeX
   - Files: src/latex/engine.py

### Phase 3: Visual Editor (Week 5-8)
8. [x] Visual canvas implementation
   - Target: Canvas that can display LaTeX elements
   - Verification: Can render text and shapes
   - Files: src/gui/canvas.py

9. [x] Element selection and manipulation
   - Target: Click to select, drag to move
   - Verification: Can select and move elements
   - Files: src/gui/canvas.py

10. [x] Drag-and-drop functionality
    - Target: Full drag-and-drop support
    - Verification: Can drag elements freely
    - Files: src/gui/canvas.py

11. [x] Property panel
    - Target: Panel for editing element properties
    - Verification: Can change font, size, color
    - Files: src/gui/properties.py

### Phase 4: LaTeX Integration (Week 9-12)
12. [x] Visual-to-LaTeX code generation
    - Target: Generate LaTeX from visual elements
    - Verification: Visual changes produce correct LaTeX
    - Files: src/latex/generator.py

13. [ ] LaTeX-to-Visual parsing
    - Target: Parse LaTeX to visual elements
    - Verification: Can import existing LaTeX
    - Files: src/latex/parser.py

14. [x] Real-time preview
    - Target: Live PDF preview
    - Verification: Preview updates in real-time
    - Files: src/gui/preview.py

15. [ ] Math formula editor
    - Target: Visual math formula editing
    - Verification: Can create/edit formulas visually
    - Files: src/gui/matheditor.py

### Phase 5: PDF-as-Canvas Architecture (New - 2026-04-04)
**Proposed by guiLaTeX-Starter**

16. [x] Research PDF editing & annotation standards
    - Target: Investigate PDF as editable canvas with metadata annotations
    - Verification: Complete research document on PDF editing feasibility
    - Files: docs/research/pdf-editing-standards.md
    - Key questions:
      - Can PDF elements carry custom metadata for LaTeX reconstruction? ✅ Yes (via annotations)
      - What PDF standards support lossless editing (PDF/A, PDF/X)? ✅ PDF 1.x/2.0
      - Licensing requirements for PDF manipulation libraries ✅ No special license needed
      - Existing solutions (PDF.js, PyMuPDF, pdf-lib) ✅ PyMuPDF recommended

17. [ ] Prototype PDF canvas viewer
    - Target: Display PDF as interactive canvas instead of static preview
    - Verification: Can render PDF pages with selectable elements
    - Files: src/gui/pdf_canvas.py
    - Constraints: WYSIWYG principle - only implement lossless features

18. [ ] PDF-to-LaTeX reconstruction engine
    - Target: Extract annotated PDF elements back to LaTeX source
    - Verification: Round-trip editing (LaTeX → PDF → edit → LaTeX) preserves content
    - Files: src/latex/pdf_reconstructor.py
    - Must handle: text, positioning, basic formatting
    - Skip if lossy: complex layouts, embedded fonts, raster images

### Phase 6: Polish & Distribution (Week 13-16)
19. [ ] Performance optimization
    - Target: Smooth performance with large documents
    - Verification: Performance benchmarks pass
    - Files: src/core/optimization.py

20. [ ] User documentation
    - Target: Complete user guide
    - Verification: Documentation review
    - Files: docs/user-guide.md

21. [ ] Testing and bug fixes
    - Target: Comprehensive test suite
    - Verification: All tests pass
    - Files: tests/

22. [ ] Distribution packaging
    - Target: Installers for Windows, macOS, Linux
    - Verification: Can install and run on all platforms
    - Files: dist/

## Validation
- Build: Compile and run application
- Test: Run unit/integration tests
- Manual: Manual feature testing
- Code Review: Review code quality
- Documentation: Update relevant docs

## Deferred / blocked
- Advanced features (collaboration, cloud sync)
- Plugin system
- Mobile version
- AI-assisted editing

## Design Principles
1. **WYSIWYG (What You See Is What You Get)**: Only implement features that can be losslessly converted between visual and LaTeX representations
2. **Progressive Enhancement**: Start with basic elements (text, positioning), add complexity only when lossless conversion is proven feasible
3. **PDF as Source of Truth**: Explore treating annotated PDF as the primary editable format rather than generated output
