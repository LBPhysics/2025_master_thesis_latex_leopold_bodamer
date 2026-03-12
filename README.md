# Master Thesis – LaTeX Manuscript

This repository now focuses exclusively on the written thesis: LaTeX sources, bibliography, and curated figures. The numerical codes and Python tooling previously bundled here have moved to dedicated project under: 
https://github.com/LBPhysics/2025_master_thesis_python_leopold_bodamer.git

## Repository layout
```
Master_thesis/
├── figures/                 # hand-drawn and exported graphics
├── latex/
│   ├── main.tex            # main document (LuaLaTeX)
│   ├── style_thesis.cls    # custom class file (formatting)
│   ├── chapters/           # thesis chapters
│   ├── appendices/         # appendices
│   ├── bib/                # bibliography database & style
│   └── figures/            # figure files
├── .vscode/                # editor helpers for LaTeX workflows
├── .gitignore              # LaTeX- and figure-specific ignores
└── README.md               # this document
```

## Building the thesis

**Compiler:** LuaLaTeX (specified in `latex/main.tex`)  
**Bibliography:** Biber backend with BibLaTeX

### Option 1: Using latexmk (recommended)
From the repository root:
```bash
latexmk -lualatex -interaction=nonstopmode -halt-on-error -cd latex/main.tex
```
Clean up auxiliary files: `latexmk -c -cd latex/main.tex`

### Option 2: Manual compilation
From the `latex/` directory:
```bash
lualatex main.tex
biber main
lualatex main.tex
lualatex main.tex
```

The output PDF is generated as `latex/main.pdf`.

## Custom LaTeX Commands

### Todo Notes
- `\todoimp{text}` - Red, for important items
- `\todoidea{text}` - Green, for ideas
- `\todoeq{text}` - Blue, for equations to check
- `\todoref{text}` - Purple, for references needed
- `\todofix{text}` - Orange, for fixes required

### References (Smart Auto-Capitalization)
- `\autoref{label}` - **Use by default**. Auto-capitalizes at sentence start
  - Mid-sentence: `\autoref{fig:x}` → "Fig. 1"
  - Sentence start: `\autoref{eq:y}` → "Equation 2"
- `\cref{label1,label2}` - Multiple refs: "Eqs. 1, 2, and 3"
- `\Cref{label}` - Force full form: "Equation 1"

**Naming conventions:** Eq./Fig./Tab./Sec./Ch./App. (short) | Equation/Figure/Table/Section/Chapter/Appendix (full)

## Class Options

Available options in `\documentclass[...]{style_thesis}`:
- `draft` - Fast compile, show overfull boxes
- `liststotoc` - Add list of figures/tables to TOC
- `nolistspacing` - Single spacing in lists
- `parskip` - Space between paragraphs
- `headsepline` - Line under header

## Selective Compilation

Uncomment in `main.tex` to compile only specific chapters:
```latex
\includeonly{chapters/c10_introduction}
```

## Figures
- `figures/` contains editable SVG drafts.

## Version control tips
- Commit generated PDFs sparingly—`latex/main.pdf` is ignored so that the history stays light.
- Keep auxiliary logs out of source control; `latexmk -c` is your friend before pushing.
- Use branches for major chapter rewrites to keep reviews focused.