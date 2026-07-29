# Adversarial Thinking in AI Systems

**Deep Learning Indaba 2026 · Skill Session**
*Understanding and Mitigating Real-World Model Failures*

**Session leader:** Manar Adel Hamed (PhD Student, Concordia University)

## Summary

Almost every attack on a machine learning system is an optimiser searching for an input that breaks your model. This session teaches that single lens and applies it across modalities: image perturbations, prompt injection and jailbreaks on LLMs, and the evaluation traps that make a broken system look healthy. Participants leave with a six-step loop they can run against systems they own, plus a runnable notebook and a one-page checklist.

## Contents

| Path | What it is |
|---|---|
| [`slides/`](slides/) | Slide deck as PDF, plus the editable `.pptx` |
| [`notebook/`](notebook/) | Colab notebook: a PGD image attack, an LLM prompt-injection probe, and the evaluation-trap demo |
| [`checklist/`](checklist/) | One-page Adversarial Thinking Checklist (PDF) with the six-step loop and failure-mode trigger questions |
| [`docs/`](docs/) | Study guide explaining every cited paper in plain language, plus the full reading list |

## How to run the materials

1. **Start with the checklist**: [`checklist/adversarial_thinking_checklist.pdf`](checklist/adversarial_thinking_checklist.pdf). It includes a 15-minute quick start.
2. **Open the notebook in Google Colab.** From the [notebook file](notebook/adversarial_thinking_colab.ipynb), use the *Open in Colab* button, or upload it via File → Upload notebook.
3. **Set the runtime to GPU** (Runtime → Change runtime type → GPU), then run the cells top to bottom. Everything installs from within the notebook; no local setup and no downloaded datasets beyond what the cells fetch.
4. **Apply the six-step loop** to a system you own: state intended behaviour → enumerate failure and threat modes → design probes → measure the gap → mitigate → monitor.

The notebook runs end to end on a free Colab GPU runtime.

## The core idea

An adversarial example is the solution to an optimisation problem: maximise the model's loss inside a small input budget (Goodfellow et al. 2015). Robust training formalises this as a min-max game (Madry et al. 2018). The same lens explains failures across vision perturbations, tabular and scoring feature attacks, data poisoning, and LLM prompt injection. The notebook makes it concrete on two very different systems: a small vision classifier and a small instruct LLM.

The session closes on why this matters for **sovereign AI**. Imported models and imported benchmarks don't transfer. Frontier LLMs lag well behind their English performance on African-language tasks (IrokoBench, Adelani et al. 2025; AfroBench 2025). A team cannot own or trust a system it cannot stress-test in its own languages and contexts, which makes local adversarial evaluation a practical prerequisite for sovereign AI.

## Responsible use

The LLM section attacks a benign, invented rule (a "secret word"). No harmful content is produced or required to run any part of this material. The goal is to teach the method so you can red-team your own systems responsibly.

## License

Code (the notebook) is MIT, see [`LICENSE`](LICENSE). Slides, checklist, and written materials are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): reuse and adapt freely with attribution. All techniques are credited to their original authors in [`docs/reading_list.md`](docs/reading_list.md).
