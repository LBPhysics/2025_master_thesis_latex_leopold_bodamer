# LaTeX Usage Guidelines

## Scope
Apply to all LaTeX files in this workspace, including chapters, appendices, and bibliography.

## Structure & Organization
- Keep content in chapter/appendix files; avoid editing generated .aux/.bbl/.bcf files.
- Use consistent sectioning levels (\chapter, \section, \subsection).
- Prefer semantic macros and reuse existing commands in style_thesis.cls.

## Consistency
- Use consistent notation for symbols and units across the document.
- Define new macros in a central place (main.tex or class/style files), not inline.
- Avoid hard-coded formatting; use predefined styles and environments.

## Figures & Tables
- Store figures under latex/figures with clear names.
- Always add captions and labels; reference with \ref/\autoref.
- Keep table formatting simple and consistent.

## Bibliography
- Add sources only in bib/my_bibliography.bib.
- Use consistent citation commands and styles as defined by the thesis class.

## Build Hygiene
- Do not edit compiled artifacts (main.aux, main.bbl, main.toc, etc.).
- Keep line lengths reasonable to improve diffs and reviews.
