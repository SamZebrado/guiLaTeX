# guiLaTeX Web v1 User Guide

## Start the editor

From the repository root, run:

```bash
python3 web_prototype/server.py
```

Then open `http://127.0.0.1:8000/` in a Chromium-based browser. Keep the server running while importing or exporting LaTeX.

## Create and edit objects

Use the toolbar to insert text, an image, or an equation. Click an object to select it, then:

- Drag it on the canvas to move it.
- Drag its resize handle to change its size.
- Drag its rotation handle to rotate it.
- Use the property panel to edit position, size, rotation, layer, and applicable text properties.

Property edits, dragging, grouping, insertion, deletion, and supported image/equation changes participate in the bounded undo/redo history. Use the Undo and Redo buttons.

## Multi-select and groups

Enable **Multi-select**, then click each object that should be included. Select **Group** to create a persistent group.

- Moving or rotating one selected grouped member applies the group transform.
- **Ungroup** removes the persistent relationship without deleting its members.
- Saving and reopening a project preserves group membership and the supported group transform behavior.

The same object cannot belong to two groups at once.

## Images

Choose **Insert Image** and select a PNG, JPEG, GIF, or WebP file. Each image must be 2 MB or smaller. With an image selected, **Replace Image** changes its content while retaining its layout properties.

Image bytes are embedded in project JSON so project save/open is lossless for the supported workflow. Conforming LaTeX export preserves image placement metadata but not the embedded image binary; keep project JSON as the editable source of truth.

## Equations

Choose **Insert Equation** to add the default formula. With the equation selected, edit its source in the **Content** field. The editor renders the supported TeX-like source as safe local MathML without a network dependency.

The supported subset covers common symbols, `\\frac`, `\\sqrt`, superscripts, subscripts, grouped expressions, and `\\text`. Unsupported syntax is shown as a visible fallback rather than executed. This is not an arbitrary TeX or MathML parser.

## Save and reopen a project

Choose **Save Project** to download a guiLaTeX JSON file. Choose **Open Project** to restore it. Project JSON is the lossless format for all supported Web v1 fields, including groups and embedded images.

## LaTeX workflow

Choose **Export LaTeX** to download conforming `.tex`. Choose **Import LaTeX** to reopen guiLaTeX-generated conforming output through the same Web UI.

This roundtrip is intentionally bounded to the single-page, ungrouped conforming subset. It is not a general-purpose importer for arbitrary LaTeX. Fields outside that format, including persistent groups and embedded image bytes, require project JSON.

## IR export

Choose **Export IR** to download the validated intermediate representation as JSON. This artifact is intended for diagnostics and integration; project JSON remains the normal editable-project format.

## PDF output

Choose **Export PDF**, then select **Save as PDF** in Chromium's print dialog. The editor applies a Letter-size print layout and hides editor chrome before printing.

PDF output uses the browser print engine, not native TeX compilation. Browser font availability and print settings can affect metrics. Confirm Letter paper, 100% scale, and disabled headers/footers if the print dialog has changed those settings.

## Current limits

- One Letter-size page per project.
- Local loopback use; no collaboration service.
- No general LaTeX import, multi-page layout, tables, templates, or plugin system.
- Equation input is limited to the supported offline TeX-like subset.
- PDF is browser-print output, not a TeX-compiled preview.
- Qt desktop behavior is separate from the Web v1 contract.

If an import is rejected, keep the original file, verify that it was exported by this Web version, and use project JSON when lossless editing is required.
