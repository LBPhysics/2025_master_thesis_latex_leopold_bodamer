# Copilot Instructions

- Follow `.github/instructions/latex-use.md` for thesis LaTeX editing conventions.
- Repo-specific physics note: for dimer jobs (`n_atoms > 1`, especially `n_atoms = 2`), `deph_rate_fs`, `down_rate_fs`, and `up_rate_fs` are legacy monomer-only fields that accidentally remain in shared config files.
- Treat those rates as irrelevant for dimer interpretation, captions, parameter summaries, and figure descriptions unless the user explicitly asks about the config artefact itself.
- For `n_atoms: 1`, those phenomenological rates may still be relevant.
