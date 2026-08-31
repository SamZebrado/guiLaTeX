# guiLaTeX

guiLaTeX is a Web-first visual editor for a bounded, single-page LaTeX layout format. The current Web v1 lets you place text, images, and a supported subset of equations on a Letter-size canvas, edit them visually, save the project, and export the result.

## Run the Web editor

Python 3.8 or newer is sufficient; the Web v1 runtime has no third-party Python dependency.

```bash
python3 web_prototype/server.py
```

Open `http://127.0.0.1:8000/` in a Chromium-based browser. The loopback server provides the editor and the same-origin LaTeX import/export endpoints.

## Web v1 capabilities

- Single Letter-size page with drag, resize, rotation, coordinate, size, font-size, and layer controls.
- Multi-selection and persistent groups. Group move and rotation, ungroup, undo/redo, and project reopen preserve the supported group contract.
- Project save/open using guiLaTeX JSON.
- Raster image insertion and replacement (PNG, JPEG, GIF, or WebP; up to 2 MB each).
- Offline equation insertion from a bounded TeX-like subset rendered as safe local MathML.
- Export of the internal representation (IR) as JSON.
- Export of conforming LaTeX and import of guiLaTeX-generated conforming `.tex` through the normal Web UI.
- PDF output through the browser print dialog, with a print layout matched to the editor page.

For operating instructions, see [docs/user-guide.md](docs/user-guide.md).

## Showcase

- [朝堂风云录 / Project showcase](https://samzebrado.github.io/guiLaTeX/showcase/)
- [Web v1 demo landing page](https://samzebrado.github.io/guiLaTeX/showcase/demo_index.html)

GitHub Pages hosts the project story and release overview. The full Web v1 editor remains a local application because its conforming LaTeX workflow uses the bundled Python loopback server and ExportCore.

## Deliberate v1 boundaries

- The LaTeX importer is for guiLaTeX's conforming single-page output, not arbitrary LaTeX documents.
- Project JSON is the lossless persistence format. Persistent group metadata and embedded image bytes are not represented by the conforming LaTeX format.
- Equation support is intentionally limited to the documented offline TeX-like subset; it is not a general TeX or MathML parser.
- PDF export uses Chromium's print pipeline. It is not native TeX compilation and does not promise identical font metrics to an external TeX engine.
- The server binds to loopback by default and is intended for local use. Collaboration, multi-page documents, tables, templates, and plugins are outside this Web v1.
- The Qt application is a secondary desktop validation route and is not the Web v1 completion criterion.

## Tests

Run the Web contract suite from the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_web_*.py'
```

Real Chromium evidence is also required for release acceptance; unit tests alone do not prove browser interaction or downloaded artifacts.

## Repository layout

- `web_prototype/` — Web v1 editor and local loopback server.
- `export_core/` — shared IR validation and LaTeX conversion code.
- `tests/test_web_*.py` — Web product and protocol contract tests.
- `src/` — secondary Qt desktop implementation.

## License

guiLaTeX Web v1 is released under the [Apache License 2.0](LICENSE).
