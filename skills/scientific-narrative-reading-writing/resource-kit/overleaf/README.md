# overleaf/

The shared LaTeX/Overleaf template used during Part 5 of the session (the
hands-on 3-sentence abstract exercise).

- `indaba-narrative-template.zip` — the full Overleaf project: `main.tex`,
  `indaba_narrative.sty` (the `[draft]`/`[final]` coaching-box package),
  `references.bib`, `README.md`, `LICENSE`. Upload this zip directly to
  Overleaf, or unzip it locally and compile `main.tex`.
- `latex-template-preview.pdf` — a compiled preview of that template (the
  "CropGuard" cassava-disease-detector walkthrough), showing the coaching
  boxes, reviewer's-lens callouts, and dataset card as they render.
- `Abstract_Template.tex` — a small, dependency-free extract of just the
  3-sentence abstract scaffold from `main.tex`, for anyone who wants the
  exercise without the full paper skeleton or the custom `.sty` package.

Switching `\usepackage[draft]{indaba_narrative}` to `[final]` in `main.tex`
hides every coaching box, leaving a clean paper skeleton ready for
submission.
