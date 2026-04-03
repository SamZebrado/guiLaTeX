# guiLaTeX

A visual LaTeX editor with drag-and-drop functionality, enabling users to visually manipulate LaTeX elements without writing code.

## Vision

guiLaTeX aims to be:
- A visual LaTeX editor with true WYSIWYG experience
- Support drag-and-drop editing of LaTeX elements (like Photoshop)
- Allow direct formatting changes (font, size, color, layout) like Word
- Generate high-quality LaTeX output in the background
- Cross-platform (Windows, macOS, Linux)

## Why guiLaTeX?

Existing LaTeX editors fall into two categories:
1. **Code editors** (TeXstudio, Texmaker): Require knowledge of LaTeX syntax
2. **Structure editors** (LyX): Focus on document structure, not visual manipulation

guiLaTeX fills the gap by providing:
- **True visual editing**: Drag and drop elements like in Photoshop
- **Direct formatting**: Change fonts, colors, sizes like in Word
- **LaTeX quality**: Professional output powered by LaTeX engine
- **No code required**: Users don't need to write LaTeX code

## Features (Planned)

### Core Features
- Visual canvas with drag-and-drop support
- Element selection and manipulation
- Property panel for formatting (font, size, color, alignment)
- Real-time PDF preview
- Math formula visual editor
- Table and figure support

### Advanced Features
- Import existing LaTeX documents
- Export to LaTeX source code
- Template library
- Custom themes
- Plugin system (future)

## Technology Stack

### Under Evaluation
- **Option 1**: Qt 6 (C++ or Python)
  - Pros: Native performance, cross-platform, mature
  - Cons: Steeper learning curve, larger binaries

- **Option 2**: Electron + React/Vue
  - Pros: Web technologies, rapid development, large ecosystem
  - Cons: Larger memory footprint, performance overhead

### Core Components
1. **Visual Editor Canvas**: Element rendering and manipulation
2. **Property Editor**: Formatting controls
3. **LaTeX Bridge**: Visual ↔ LaTeX conversion
4. **Preview System**: Real-time PDF rendering

## Project Status

**Current Phase**: Initialization and Planning

See [STATUS.md](STATUS.md) for current state, [PLAN.md](PLAN.md) for development roadmap, and [PROJECT_LOG.md](PROJECT_LOG.md) for development history.

## Development

This project uses a structured development workflow with STATUS + LOG + PLAN pattern. See [dev-workflow skill](../.trae/skills/dev-workflow/SKILL.md) for details.

### Getting Started

1. Read [STATUS.md](STATUS.md) to understand current state
2. Read [PLAN.md](PLAN.md) to see active tasks
3. Review recent [PROJECT_LOG.md](PROJECT_LOG.md) entries
4. Choose a task from PLAN.md
5. Implement with verification
6. Update STATUS.md and PROJECT_LOG.md

## Requirements

### System Requirements
- TeX Live 2022 or later (or MiKTeX)
- C++17 compiler (if using Qt/C++)
- Python 3.8+ (if using Qt/Python)
- Node.js 16+ (if using Electron)

### Platform Support
- macOS 10.15+ (Intel and Apple Silicon)
- Windows 10+
- Linux (Ubuntu 20.04+, Fedora, etc.)

## License

To be determined (considering MIT, Apache 2.0, or GPL v3)

## Contributing

Contributions are welcome! Please read the development workflow documentation before contributing.

## Contact

Project repository: `guiLaTeX/`

---

**Note**: This project is in early development phase. Features and architecture are subject to change.
