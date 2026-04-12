# guiLaTeX Architecture Design

## Overview

guiLaTeX is a visual LaTeX editor that bridges the gap between traditional code-based LaTeX editing and modern visual document editing. This document outlines the technical architecture and design decisions.

## Design Goals

1. **True WYSIWYG**: What you see is what you get - visual editing matches final output
2. **Intuitive Interaction**: Drag-and-drop, direct manipulation like Photoshop/Word
3. **LaTeX Quality**: Professional typesetting powered by LaTeX engine
4. **Performance**: Smooth interaction even with complex documents
5. **Cross-Platform**: Consistent experience across Windows, macOS, Linux

## Technology Stack Options

### Option 1: Qt 6 (C++)

**Architecture**:
```
┌─────────────────────────────────────┐
│         Qt GUI Application          │
├─────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────────┐ │
│  │  Canvas  │  │  Property Panel  │ │
│  └──────────┘  └──────────────────┘ │
├─────────────────────────────────────┤
│         Business Logic Layer        │
│  ┌──────────┐  ┌──────────────────┐ │
│  │ Element  │  │   LaTeX Bridge   │ │
│  │ Manager  │  │  (Visual ↔ TeX)  │ │
│  └──────────┘  └──────────────────┘ │
├─────────────────────────────────────┤
│         LaTeX Engine Layer          │
│  ┌──────────┐  ┌──────────────────┐ │
│  │TeX Live  │  │   PDF Renderer   │ │
│  │  Engine  │  │   (Poppler)      │ │
│  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────┘
```

**Pros**:
- Native performance
- Mature cross-platform framework
- Direct access to system resources
- Smaller binary size
- Better for complex graphics

**Cons**:
- Steeper learning curve
- Longer development time
- Requires C++ expertise
- Build complexity

### Option 2: Qt 6 (Python/PyQt6)

**Architecture**: Same as C++ but with Python bindings

**Pros**:
- Rapid development
- Easier to learn and prototype
- Large Python ecosystem
- Good for MVP

**Cons**:
- Slower performance
- Larger memory footprint
- Distribution complexity
- Dependency management

### Option 3: Electron + React/Vue

**Architecture**:
```
┌─────────────────────────────────────┐
│      Electron Application           │
├─────────────────────────────────────┤
│  ┌────────────────────────────────┐ │
│  │     React/Vue Frontend         │ │
│  │  ┌──────────┐  ┌─────────────┐ │ │
│  │  │  Canvas  │  │  Property   │ │ │
│  │  │(HTML5/   │  │    Panel    │ │ │
│  │  │ SVG)     │  │             │ │ │
│  │  └──────────┘  └─────────────┘ │ │
│  └────────────────────────────────┘ │
├─────────────────────────────────────┤
│      Node.js Backend                │
│  ┌──────────┐  ┌──────────────────┐ │
│  │ LaTeX    │  │   File System    │ │
│  │ Bridge   │  │   Access         │ │
│  └──────────┘  └──────────────────┘ │
├─────────────────────────────────────┤
│      LaTeX Engine (External)        │
│  ┌──────────┐  ┌──────────────────┐ │
│  │TeX Live  │  │   PDF Renderer   │ │
│  │  Engine  │  │   (pdf.js)       │ │
│  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────┘
```

**Pros**:
- Web technologies (familiar to many developers)
- Rapid prototyping
- Large ecosystem of libraries
- Easy to create modern UI
- Hot reload for development

**Cons**:
- Larger memory footprint
- Performance overhead
- Larger distribution size
- Less native feel

## Recommended Approach

### For MVP: Qt 6 (Python/PyQt6)
- Rapid development
- Easy to prototype and iterate
- Good enough performance for initial version
- Can port to C++ later if needed

### For Production: Qt 6 (C++)
- Best performance
- Native feel
- Smaller distribution
- Better for complex features

## Core Architecture Components

### 1. Visual Canvas (Frontend)
**Responsibilities**:
- Render LaTeX elements visually
- Handle user interactions (click, drag, drop)
- Manage element selection
- Provide visual feedback

**Key Classes**:
```cpp
class Canvas : public QGraphicsView {
    // Main visual editing area
}

class LaTeXElement : public QGraphicsItem {
    // Base class for all LaTeX elements
    // Text, Image, Table, Formula, etc.
}

class SelectionManager {
    // Handle element selection and manipulation
}
```

### 2. Property Panel (Frontend)
**Responsibilities**:
- Display selected element properties
- Allow property editing
- Update visual elements in real-time

**Key Features**:
- Font family, size, color
- Alignment, spacing
- LaTeX-specific properties
- Custom properties per element type

### 3. LaTeX Bridge (Core)
**Responsibilities**:
- Convert visual elements to LaTeX code
- Parse LaTeX code to visual elements
- Maintain synchronization
- Handle LaTeX compilation

**Key Classes**:
```cpp
class LaTeXGenerator {
    // Generate LaTeX from visual elements
    QString generateLaTeX(Document* doc);
}

class LaTeXParser {
    // Parse LaTeX to visual elements
    Document* parseLaTeX(QString latex);
}

class LaTeXCompiler {
    // Compile LaTeX using TeX Live
    PDF* compile(QString latex);
}
```

### 4. Document Model (Core)
**Responsibilities**:
- Represent document structure
- Manage elements and their relationships
- Handle undo/redo
- Serialize/deserialize document

**Key Classes**:
```cpp
class Document {
    // Main document model
    QList<LaTeXElement*> elements;
}

class ElementFactory {
    // Create elements from LaTeX code
}
```

### 5. Preview System (Frontend)
**Responsibilities**:
- Render PDF preview
- Synchronize with canvas
- Handle zoom and navigation

**Implementation**:
- Use Poppler (Qt) or pdf.js (Electron)
- Real-time updates on changes
- Side-by-side or overlay preview

## Data Flow

### User Editing Flow
```
User Action
    ↓
Canvas (Visual Change)
    ↓
Document Model (Update)
    ↓
LaTeX Generator (Generate Code)
    ↓
LaTeX Compiler (Compile)
    ↓
PDF Preview (Render)
```

### Import Flow
```
LaTeX File
    ↓
LaTeX Parser (Parse)
    ↓
Document Model (Create Elements)
    ↓
Canvas (Render Visual)
    ↓
User can edit visually
```

## Key Challenges and Solutions

### Challenge 1: Visual ↔ LaTeX Synchronization
**Problem**: Maintaining bidirectional sync between visual elements and LaTeX code

**Solution**:
- Use internal representation that maps to both
- Incremental updates instead of full regeneration
- Conflict resolution strategy

### Challenge 2: Complex LaTeX Structures
**Problem**: Some LaTeX structures (tables, matrices) are complex to visualize

**Solution**:
- Specialized visual editors for complex structures
- Hybrid approach: visual + code editing
- Template-based approach

### Challenge 3: Performance with Large Documents
**Problem**: Real-time preview can be slow with large documents

**Solution**:
- Incremental compilation
- Background compilation thread
- Smart caching
- Lazy rendering

### Challenge 4: Cross-Platform LaTeX Integration
**Problem**: Different LaTeX distributions on different platforms

**Solution**:
- Detect and use system LaTeX (TeX Live, MiKTeX)
- Bundle minimal LaTeX distribution
- Provide download helper

## File Format

### Native Format (.glx)
```json
{
  "version": "1.0",
  "metadata": {
    "created": "2026-04-03T14:30:00Z",
    "modified": "2026-04-03T14:35:00Z"
  },
  "elements": [
    {
      "id": "elem_1",
      "type": "text",
      "position": {"x": 100, "y": 100},
      "properties": {
        "text": "Hello World",
        "font": "Arial",
        "size": 12,
        "color": "#000000"
      },
      "latex": "\\text{Hello World}"
    }
  ],
  "latex_preamble": "\\documentclass{article}\n..."
}
```

### Export Formats
- LaTeX source (.tex)
- PDF (.pdf)
- HTML (future)
- DOCX (future, via Pandoc)

## Development Phases

See [PLAN.md](../PLAN.md) for detailed development roadmap.

## Next Steps

1. **Technology Decision**: Choose between Qt (C++/Python) vs Electron
2. **Prototype**: Create basic canvas with element rendering
3. **LaTeX Integration**: Integrate TeX Live compilation
4. **Iterate**: Add features based on user feedback

## References

- [Qt Documentation](https://doc.qt.io/)
- [LaTeX Project](https://www.latex-project.org/)
- [TeX Live](https://www.tug.org/texlive/)
- [Poppler (PDF rendering)](https://poppler.freedesktop.org/)
