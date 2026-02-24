# LaTeX Usage Guidelines

Single source of truth for all thesis LaTeX content.
**Always check this file before drafting or editing any LaTeX document.**

## Scope
Apply to all LaTeX files in this workspace, including chapters, appendices, and bibliography.

## Voice & Tone
- **Clarity first:** every statement must be 100 % clear. If unsure about any fact, figure, or claim — ask the user. Better to ask than to guess.
- Style: clear, structured, scientific. Short sentences. No waffle.
- Tone: precise, evidence-based, appropriately cautious.
- Language: British English throughout.
- Avoid: vague claims, exaggerated impact, unsupported assertions, filler phrases.
- Prefer: concrete wording, measurable outcomes, specific technical terms.

## Factual Accuracy & Sources (STRICT)
- **Only generate statements that are verifiably true and backed by an actual source.**
- Every scientific claim, definition, or non-trivial statement must have a citation.
- Do **not** fabricate, hallucinate, or approximate references. If a proper source is not known, **do not write the sentence**.
- If a citation is needed but unavailable, **ask the user** to provide the relevant section of a book, paper, or resource so the sentence can be drafted with a proper citation.
- Metrics, numbers, and quantitative claims only if accurate and sourced.
- Specific statements > broad impact claims.

## Things to Ask the User If Unclear
Do **not** guess. Ask about:
- Any fact, figure, or claim that cannot be verified from existing documents in the workspace.
- The correct source / citation for a statement.
- Whether a particular phrasing or emphasis is intended.
- Notation choices or symbol conventions not already established in the thesis.

## Structure & Organisation
- Keep content in chapter/appendix files; avoid editing generated .aux/.bbl/.bcf files.
- Use consistent sectioning levels (\chapter, \section, \subsection).
- Prefer semantic macros and reuse existing commands in style_thesis.cls.

## Appendices vs. Supplementary Material

**Appendix (part of the thesis PDF)**
- Physically included at the end of the thesis document.
- Examined and archived together with the thesis.
- Needed for completeness or reproducibility.
- Can be referenced in the main text ("see Appendix A").
- Typically includes:
  - Technical derivations
  - Extended formulas
  - Detailed definitions
  - Additional figures that support the argument
- **Purpose:** "Not needed for first-pass reading, but essential for full scientific transparency."

**Supplementary Material (separate document or data)**
- Not part of the main thesis PDF.
- Often stored separately (data repository, GitHub, university archive).
- Usually not printed.
- Contains material too long, too technical, or too data-heavy for the thesis.
- Typically includes:
  - Large datasets
  - Full simulation code
  - Parameter tables
  - Extra spectra not discussed in detail
  - Extended numerical convergence studies
  - Raw outputs
- **Purpose:** "Everything required for full reproducibility, but too bulky for the thesis itself."

## Cross-References and Citations

**Reference commands:**
- Use `\autoref{label}` for automatic reference names (e.g., "Equation (2.5)", "Figure 3.1")
- Use `\cref{label}` for abbreviated forms mid-sentence (e.g., "Eq. (2.5)")
- Use `\Cref{label}` for full forms at sentence start (e.g., "Equation (2.5)")

**Non-breaking spaces before references:**
Always use a non-breaking space `~` before reference commands when the reference is grammatically attached to the preceding word. This prevents line breaks between the word and the reference.

Correct usage:
- `derived in~\autoref{sec:derivation}` → "derived in Eq. (2.5)"
- `from~\autoref{eq:master}` → "from Eq. (1.1)"
- `to~\autoref{sec:methods}` → "to Section 2.3"
- `see~\autoref{app:derivation}` → "see Appendix A"

Incorrect usage (missing `~`):
- `derived in \autoref{sec:derivation}` ❌ (allows unwanted line break)

**Sentence-start references:**
At the beginning of a sentence, `\autoref` automatically produces full names (e.g., "Equation", "Figure"). No `~` is needed when starting a sentence:
- `\Autoref{eq:master} shows that...` → "Equation (1.1) shows that..."

**Multiple references:**
Use `\cref{label1,label2,label3}` for ranges or lists:
- `\cref{eq:a,eq:b,eq:c}` → "Eqs. (1), (2), and (3)"
- `\crefrange{eq:start}{eq:end}` → "Eqs. (1.1)–(1.5)"

## Consistency
- Use consistent notation for symbols and units across the document.
- Define new macros in a central place (main.tex or class/style files), not inline.
- Avoid hard-coded formatting; use predefined styles and environments.

## Figures & Tables
- Store figures under latex/figures with clear names.
- Always add captions and labels; reference with \ref/\autoref.
- Keep table formatting simple and consistent.
- First mention comes first: introduce the figure in the text, then place the figure immediately after that paragraph (or on the next page if layout forces it).
- Do not preview figures: avoid placing a figure earlier than its first callout, since the reader has not been told why it is there yet.
- Keep the callout and the figure close: ideally on the same page; if not possible, ensure it is within the next page or so.
- Full-page or large figures may land on the next page; ensure the first callout is not pages later than the figure.
- Prefer flexible placement for figures: use `\begin{figure}[tbp]` to avoid blank space and allow the figure to move to the top of the next page if needed. Reserve `\begin{figure}[H]` for rare cases where strict placement is essential.

## Bibliography
- Add sources only in bib/my_bibliography.bib.
- Use consistent citation commands and styles as defined by the thesis class.
- Every new citation must correspond to a real, verifiable publication.

## Build Hygiene
- Do not edit compiled artifacts (main.aux, main.bbl, main.toc, etc.).
- Keep line lengths reasonable to improve diffs and reviews.
