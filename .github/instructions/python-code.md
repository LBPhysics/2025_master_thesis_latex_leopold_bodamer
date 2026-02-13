# Python Code Guidelines

Single source of truth for all Python code in this workspace.
**Always check this file before writing or editing any Python code.**

## Scope
Apply to all Python code, scripts, and notebooks in this workspace.

## Voice & Tone (Comments, Docstrings, Output)
- **Clarity first:** every comment, docstring, and log message must be 100 % clear. If unsure about any detail — ask the user. Better to ask than to guess.
- Style: clear, structured, professional. Short sentences. No waffle.
- Language: British English.
- Avoid: vague descriptions, exaggerated claims about performance or accuracy.
- Prefer: concrete wording, specific technical terms, measurable outcomes.

## Things to Ask the User If Unclear
Do **not** guess. Ask about:
- Any physical constant, parameter value, or model assumption that cannot be verified from existing code or documents.
- Whether to add or remove dependencies.
- Which approach to take when multiple valid implementations exist.
- Any fact, figure, or claim you cannot verify from existing workspace files.

## Style & Structure
- Follow PEP 8 for formatting and naming.
- Prefer small, testable functions with clear responsibilities.
- Use type hints for public functions and complex data structures.
- Keep modules cohesive; avoid circular imports.

## Reliability & Performance
- Validate inputs and raise clear exceptions.
- Avoid premature optimisation; use vectorised NumPy operations when appropriate.
- Log long-running steps; avoid print in library code.

## Tooling
- Prefer existing utilities in the workspace before adding new dependencies.
- If a new package is required, document it in environment.yml or pyproject.toml.
- Avoid modifying generated files and outputs.

## Notebooks
- Keep notebook cells deterministic and ordered.
- Move reusable code into modules under packages/ or scripts/.
- Clear temporary debugging cells before finalising changes.

## Documentation
- Add concise docstrings to public functions/classes.
- Include usage examples for non-trivial workflows.
