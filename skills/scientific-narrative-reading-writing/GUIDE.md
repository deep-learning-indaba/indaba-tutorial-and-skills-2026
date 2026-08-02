# Guide — How to Use This Repository

This is a walkthrough of the repository in the order it's meant to be used,
whether you attended the live Skill Session or are working through the
material on your own.

## 1. Watch / read the session

- [`slides/PDF/Livrable3_Slides_Scientific_Narrative_v3.pdf`](slides/PDF/Livrable3_Slides_Scientific_Narrative_v3.pdf) — the 40-slide deck, print-ready.
- [`slides/PPTX/Livrable3_Slides_Scientific_Narrative_v3.pptx`](slides/PPTX/Livrable3_Slides_Scientific_Narrative_v3.pptx) — the same deck, editable (e.g. to reuse slides in your own talk).

## 2. Read the long-form material

- [`docs/Indaba2026_Participant_Handbook_PREMIUM.docx`](docs/Indaba2026_Participant_Handbook_PREMIUM.docx) — the condensed, 20-point handbook: fastest way to review the session after attending.
- [`docs/Indaba2026_ScientificNarrative_Handbook_v2.0.docx`](docs/Indaba2026_ScientificNarrative_Handbook_v2.0.docx) — the full multi-chapter handbook, for going deeper on any one step (reading method, writing blueprint, FAIR data, reviewer psychology, etc.), with worked examples and exercises per chapter.

Both cover the same two methods — Keshav's 3-Pass reading method and the
four-step Writing Blueprint (Frame · Core · Impact · Honesty) — at different
depths.

## 3. Do the hands-on exercise

- [`resource-kit/exercises/Exercise_3-Sentence_Abstract.docx`](resource-kit/exercises/Exercise_3-Sentence_Abstract.docx) or [`.pdf`](resource-kit/exercises/Exercise_3-Sentence_Abstract.pdf) — pick one of the four scenario cards (climate, agriculture, health, or local languages) and write your abstract in exactly 3 sentences: Context+Gap → Method → Results+Impact.
- Self-check against [`resource-kit/checklist/Scientific_Writing_Checklist.pdf`](resource-kit/checklist/Scientific_Writing_Checklist.pdf) before you consider it done.

## 4. Write your own paper

Two templates exist, for two different moments:

| Template | When to use it |
|---|---|
| [`resource-kit/overleaf/`](resource-kit/overleaf/) — `indaba-narrative-template.zip` | **During/right after the session.** Includes the coaching boxes (`[draft]` mode) that walk you through the same 3-sentence abstract exercise inside a full paper skeleton. Switch to `[final]` mode in `main.tex` to hide the boxes once you're ready to submit. |
| [`templates/overleaf/`](templates/overleaf/) — `main.tex` + `references.bib` | **Once you're writing for real, for a specific venue.** Plain LaTeX, no custom package, with links to the *official* NeurIPS/ICLR/ACL style files and notation-shortcut conventions. See [`templates/overleaf/bonus-figures/`](templates/overleaf/bonus-figures/) for example result figures (Pareto, box plot, confusion matrix, convergence curves). |

**To compile either one:**
1. Create a free account on [Overleaf](https://www.overleaf.com).
2. **New Project → Upload Project**, and upload the folder (or the `.zip`, for `resource-kit/overleaf/`).
3. It compiles out of the box with pdfLaTeX — no local install needed.

(Or locally: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`, from inside the template folder, with a TeX distribution installed.)

## 5. Keep reading

- [`resource-kit/reading-list/READING_LIST.md`](resource-kit/reading-list/READING_LIST.md) — 14 annotated references (reading method, writing craft, figures/data/reproducibility, scientific integrity, African AI community) with a suggested 4-week starter plan.
- [`references/bibliography.bib`](references/bibliography.bib) — the same core references in BibTeX, ready to drop into your own paper.

## 6. No power, no Wi-Fi?

[`resource-kit/offline-pack/`](resource-kit/offline-pack/) has the repository
URL written out in full (`Resource_Kit_URL.txt`) as a fallback for the QR
code shown on the slides, plus printable versions of the slides and exercise
sheet.

## Everything else

- [`resource-kit/README.md`](resource-kit/README.md) — full index of the resource kit if you just want to browse.
- [`README.md`](README.md#repository-structure) — full repository map.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — several folders (`examples/`, `templates/neurips/`, `templates/iclr/`, `templates/ieee/`, `assets/`, `resource-kit/demo-paper/`, `resource-kit/reference-managers/`) are scaffolded but still pending real content — see their `README.md` for what's expected, and open a PR if you'd like to help fill one in.
- [`CITATION.cff`](CITATION.cff) — how to cite this work.
