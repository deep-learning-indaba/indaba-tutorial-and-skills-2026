# Contributing — for session leaders

Thanks for leading a session! 🙌 This guide keeps everyone's work isolated so we
avoid stepping on each other's toes.

## The one rule

> **You own exactly one folder. Only ever edit files inside your own folder.**

Do not edit another session's folder, and do not edit shared files at the repo
root (`README.md`, `LICENSE`, `.gitignore`, `.github/`). If a shared file needs
changing, ask Annie or Joscha.

## Folder convention

Put your material under `practicals/` **or** `skills/`, in a folder named after
your session (lowercase, hyphens instead of spaces):

```
practicals/
  your-session-name/
    README.md          <- short description + how to run
    Your_Notebook.ipynb
    slides/            <- your slides (PDF preferred, or a link in README.md)
    data/              <- small sample data only (see limits below)
```

Your folder already exists (named after your session in the schedule) — put
your material inside it.

## What to include

Please add **everything a participant needs to follow your session and revisit
it afterwards**:

- **Notebook(s)** — Colab-ready (for tutorials; optional for skills sessions).
- **Slides** — export as **PDF** into a `slides/` subfolder. If you prefer to
  keep them in Google Slides / Canva, add the (publicly viewable) link to your
  folder's `README.md` instead.
- **Any other materials** — handouts, cheat sheets, reading lists, links to
  datasets or demos. Small files go in your folder; anything large gets linked
  from your `README.md`.
- **A `README.md`** in your folder with: session title, leaders, a short
  summary, and how to run / use the materials.

📣 **Please add your slides and materials even if your session is
presentation-only** — participants consistently ask for them afterwards, and
this repo is the one place they'll look.

## Workflow (fork & pull request — no direct pushes)

You do **not** need write access to this repo. Work in your own fork and open a
pull request:

1. **Fork** this repository (top-right "Fork" button on GitHub).
2. Clone your fork and create a branch:
   ```bash
   git clone git@github.com:<your-username>/indaba-tutorial-and-skills-2026.git
   cd indaba-tutorial-and-skills-2026
   git checkout -b my-session
   ```
3. Add your folder and commit **only files inside it**.
4. Push and open a Pull Request against `main` of this repo.
5. An organiser reviews and merges. Because you only touched your own folder,
   there will be no conflicts. ✅

To pull in later updates from the main repo, add it as a remote once:
```bash
git remote add upstream git@github.com:deep-learning-indaba/indaba-tutorial-and-skills-2026.git
git fetch upstream && git rebase upstream/main
```

## Notebook hygiene (please!)

- **Clear all outputs before committing.** Saved outputs (images, plots) bloat
  the repo and cause ugly diffs. In Jupyter: *Kernel → Restart & Clear Output*,
  or run `jupyter nbconvert --clear-output --inplace your_notebook.ipynb`.
- **No large files.** Keep anything over ~10 MB out of git. Host datasets/model
  weights externally (Google Drive, HF Hub) and download them from the notebook.
- Make notebooks **Colab-ready** — pin/install dependencies in the first cell.

## Questions?

Open an issue or ping Annie and Joscha. 🌍
