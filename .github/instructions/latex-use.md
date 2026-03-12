# LaTeX Copilot Instructions (Thesis Workspace)

Single source of truth for all thesis LaTeX content. Apply to **all** `.tex` files and the bibliography file.

---

## 1) Non-negotiables

### Clarity
- Every sentence must be unambiguous.
- If a statement could be interpreted in more than one way, rewrite.

### Language & style
- **British English** only.
- Scientific, structured, compact.
- Prefer short sentences. No filler.

### Truth & sourcing (STRICT)
- Write **only** statements you can support with a real, verifiable source.
- Any definition, scientific claim, or non-trivial statement **must** have a citation.
- Never invent or approximate references.
- If a citation is needed but not known: **do not write the sentence**. Ask the user for the relevant source/section.

---

## 2) What to ask the user (instead of guessing)

Ask when any of the following is unclear:
- The correct citation for a claim/definition.
- A number/metric, quantitative comparison, or “better/worse” statement.
- Notation choices not already fixed in the thesis (symbols, subscripts, picture conventions).
- Intended emphasis (what should be highlighted vs. kept minimal).

---

## 3) Structure & file hygiene

- Edit only source files (`.tex`, `.bib`, class/style files). Never edit build artefacts (`.aux`, `.bbl`, `.bcf`, `.toc`, …).
- Keep content in the appropriate chapter/appendix file.
- Use consistent sectioning (`\chapter`, `\section`, `\subsection`); do not invent new hierarchies.

### Macros
- Prefer semantic macros over hard-coded formatting.
- Define new macros centrally (main or class/style), not inline.

---

## 4) Cross-references (mandatory conventions)

### Commands
- Use `\autoref{...}` for general references.
- Use `\cref{...}` / `\Cref{...}` for compact/mid-sentence or sentence-start variants as appropriate.

### Non-breaking spaces
- Use `~` before references when grammatically attached:
  - `see~\autoref{...}`, `from~\cref{...}`, `in~\autoref{...}`

### Multiple references
- Use `\cref{a,b,c}` for lists.
- Use `\crefrange{start}{end}` for ranges.

### Equation labels and numbering
- Only assign a `\label{...}` to a displayed equation if that equation is referenced somewhere in the thesis.
- If a displayed equation is not referenced, use the unnumbered form:
  - `equation*` instead of `equation`
  - `align*` instead of `align`
- For multi-line `align` environments that contain at least one referenced line:
  - keep numbering only on the referenced lines
  - add `\notag` to every unreferenced line
- Do not leave numbered display equations in the thesis without a purpose.

---

## 5) Notation rules

### Descriptive subscripts (GLOBAL)
- Any descriptive subscript must be upright:
  - `_{\mathrm{S}}`, `_{\mathrm{E}}`, `_{\mathrm{int}}`, `_{\mathrm{T}}`, `_{\mathrm{I}}`, …
- Do not use italic descriptive subscripts.
- If the meaning/choice is ambiguous, ask.

---

## 6) Figures & tables

### Placement
- First introduce the figure/table in text, then place it **immediately after** (or next page if needed).
- Use flexible placement by default: `\begin{figure}[htbp]`.
- Use `[H]` only when strict placement is essential.

### Captions (STRICT: description only)
Captions may contain **only**:
- What is visibly present (panels, axes, labels, markers, colour coding, arrows).
- Parameters/variables that are explicitly shown or required to read the figure.

Captions must **not** contain:
- Interpretation (“this shows…”), theory background, or causal explanation.
- Methodology unless it is explicitly depicted/labeled in the figure.

All interpretation belongs in the surrounding main text.

---

## 7) Appendix vs supplementary material (decision rule)

### Appendix (in thesis PDF)
Use for material that is not needed for first-pass reading but is needed for scientific transparency:
- Derivations, extended formulas/definitions, extra supporting figures.

### Supplementary (separate from thesis PDF)
Use for bulky items required for full reproducibility but unsuitable for the thesis document:
- Large datasets, full code, long parameter tables, extensive raw outputs, large convergence sweeps.

---

## 8) Bibliography

- Add/edit references **only** in `bib/my_bibliography.bib`.
- Every citation must correspond to a real publication (verifiable).
- Do not add “placeholder” entries.

---

## 9) Editing discipline (to keep diffs clean)

- Keep line lengths reasonable.
- Prefer small, local changes over reflowing entire files.
- Do not change notation/style conventions unless explicitly requested.