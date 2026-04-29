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

### Fixed labels vs variables (GLOBAL)
- If a symbol denotes a fixed, named object, set the label upright with `\mathrm{...}`.
- Keep true variables, indices, and dummy summation labels italic.
- This rule applies both in subscripts and inside state notation.
- Examples:
  - fixed labeEls: `\omega_{\mathrm{A}}`, `\omega_{\mathrm{eg}}`, `\omega_{\mathrm{L}}`, `\mu_{\mathrm{ge}}`, `\ket{\mathrm{g}}`, `\bra{\mathrm{e}}`, `\ket{\mathrm{AB}}`
  - variables/indices: `\omega_n`, `J_{mn}`, `\ket{n}`, `\ket{ij}`, `\rho_{ab}`
  - mixed cases: `\mu_{\mathrm{g}n}`, `\mu_{n\mathrm{g}}`
- For the dimer, do not use `f` for the one concrete doubly excited state. Write `\ket{\mathrm{AB}}`, `\bra{\mathrm{AB}}`, `\mu_{n\mathrm{AB}}`, etc.
- Reserve italic `f` only for a genuinely generic final-state label, e.g. a family such as `\{\ket{f}\}`.

### Repo-specific dimer note
- For dimer work (`n_atoms > 1`, especially `n_atoms = 2`), ignore `deph_rate_fs`, `down_rate_fs`, and `up_rate_fs` in YAML/config files.
- These fields are a monomer-only artefact that currently appears in shared configs for all `n_atoms`.
- Do not present those rates as physically relevant dimer parameters in captions, summaries, or parameter lists unless the user explicitly asks about the config artefact itself.
- For `n_atoms: 1`, these rates may still be relevant.

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

---

## 10) Reference-framing in results chapters

- If a results chapter rebuilds figures or analyses from literature, state that once in the chapter introduction.
- Make clear there that the reproduced results are generated with the thesis' own workflow and that the later discussion may extend the published argument.
- Do not keep repeating throughout the chapter that figures are based on, adapted from, or oriented towards the reference papers.
- Mention the reference papers again in the running text only when the present setup, figure, numerical choice, or interpretation differs from the published version, or when a concrete paper-vs-present comparison is the point of the paragraph.

---

## 11) Supervisor-note learnings from chapter revisions

- If an annotated correction flags a local style, notation, or exposition problem, check the whole thesis for the same pattern and fix analogous cases consistently.
- Introduce notation before first use. In particular, define thermal quantities such as `\beta` immediately when they appear, and keep one notation style throughout a chapter.
- Keep trace notation consistent. Prefer one form globally within a chapter, e.g. `\mathrm{Tr}[...]`, instead of mixing bracket styles.
- Do not use vague filler sentences such as forward references without content (`will be shown later`, `will be concretised later`, etc.). Every sentence must add concrete information or be removed.
- When explaining decoherence or reduced states, prefer physically precise wording over broad phrases such as `statistical mixture` unless that statement is exactly justified.
- Do not reintroduce notation conventions that are already defined globally elsewhere in the thesis unless the local context genuinely requires a reminder.
- Avoid standalone `Units.` digressions inside derivations. Either integrate unit information into the surrounding explanation or place it in a more natural setup/implementation context.
- Keep software and package names out of formal derivations and core scientific narrative unless the software itself is the topic. Put concrete implementation details in the implementation appendix or equivalent dedicated sections.
- When working from handwritten supervisor annotations, treat the annotated PDF as the authority if the source has drifted, and record any genuinely unreadable note explicitly instead of guessing.



Safely compile my LaTeX thesis project. Before building, check for and stop any running `latexmk`, `lualatex`, `biber`, or `perl` processes in this repo so there are no overlapping builds. Never run clean and compile in parallel. If stale or corrupted generated files block the build, delete only generated artifacts (`latex/main.*`, chapter/appendix `.aux`, `.bcf`, `.bbl`, `.blg`, `.toc`, `.out`, `.synctex*`, `.fls`, `.fdb_latexmk`, `.run.xml`) and never touch source `.tex` files or figure assets. Then compile from `latex/` with `latexmk -g -lualatex -interaction=nonstopmode -file-line-error -halt-on-error main.tex`, wait for it to finish, and report the real remaining errors or warnings briefly.


The goal is to have the largest improvement in: - logical flow, - reader orientation, - clarity, - unambiguous scientific wording, - grammar and syntax. Rules: - Use simple, clear, scientifically appropriate language. - Avoid ambiguity completely. - Prefer positive formulations wherever possible.. - Only restructure if the benefit is significant. - Apply the Pareto principle: focus first on the few changes with the greatest impact a superivsor cares about (clarity, then scientific value). - Do not add physical interpretation, scientific content, or new claims unless explicitly requested. - Do not change the meaning. Source reliability rule: - All physical statements must agree with the underlying sources of this project. - In particular, check consistency with: 1. Paper I by Mančal et al., 2. Paper II by Pisliakov et al., 3. the lecture notes by Tomáš Mančal. - If a physical statement in my text is unsupported, unclear, too strong, or in tension with these sources, point this out explicitly. - Do not invent physics explanations, interpretations, or justifications. - When in doubt, prefer caution and mark the passage as needing verification. Output now: 1. Short diagnosis 2. Top changes by impact For the top changes: - separate structural/logical issues from minor language/syntax issues, - order them by expected benefit, - keep the comments brief and concrete. Do not provide the revised text yet. Only after my start signal: 3. Provide one final revised version in a single LaTeX code block. Text: