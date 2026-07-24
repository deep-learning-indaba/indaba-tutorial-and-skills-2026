# Building On-Device AI Applications with Gemma 3n

*Author: Jesse-Paul Miracle Osemeke*
*Location: Deep-Learning Indaba 2026*
*Date: 2nd August, 2026*

## About

This one-hour skill session shows how capable language models can run locally on phones and laptops through careful model selection, conversion and quantisation.

## Repo Structure

```
.
├── slides/                            # Session slides
├── on-device-ai-marimo.ipynb          # Marimo version of the walkthrough (native marimo notebook file)
├── llama.cpp_quant_marimo.py          # Same walkthrough, as a marimo notebook in script form (runnable with uv)
├── on-device-ai-colab.ipynb           # Google Colab version of the walkthrough
├── llama.cpp_quant_colab.py           # Same Colab walkthrough, as a Jupytext "percent" script
└── requirements.txt                   # Pinned dependencies for running either notebook locally without uv
```

Both versions walk through the same steps: compiling `llama.cpp`, downloading Gemma 3n and Qwen models plus a WikiText calibration set, converting the models to FP16 GGUF, generating an importance matrix, producing Q4_K_M and IQ3_M quantised variants, benchmarking size/speed across all versions, downloading the resulting GGUF files, and optionally uploading them to the Hugging Face Hub.

## Setup Instructions

### Marimo

`on-device-ai-marimo.ipynb` and `llama.cpp_quant_marimo.py` are [marimo](https://marimo.io) notebooks with inline `uv` script dependencies, so the script version can be run directly with `uv`:

```bash
uv run llama.cpp_quant_marimo.py
```

or opened in the marimo editor:

```bash
uv run marimo edit llama.cpp_quant_marimo.py
```

### Google Colab

`on-device-ai-colab.ipynb` is a self-contained Colab notebook — upload it at [colab.research.google.com](https://colab.research.google.com) (or open it directly if this repo is on GitHub, via File > Open notebook > GitHub) and run the cells top to bottom. It installs its own dependencies with `!pip install` in the first cell, so no local setup is required beyond a Hugging Face token.

`llama.cpp_quant_colab.py` is the same walkthrough as a [Jupytext](https://jupytext.readthedocs.io) "percent" (`# %%`) script, kept for diffing and editing in Jupyter/VS Code. Convert it back into a notebook with `jupytext --to notebook llama.cpp_quant_colab.py` if you need a fresh `.ipynb` from it.

### Running locally without uv

If you'd rather not use `uv`, install `requirements.txt` into a Python 3.13+ virtualenv and run either script/notebook with a regular Jupyter kernel:

```bash
pip install -r requirements.txt
```

Note the Colab notebook's download-button cells import `google.colab`, which only exists inside the Colab runtime — those cells will error out locally and can be skipped.

### Common requirements

- `cmake` and a C++ build toolchain, to compile `llama.cpp` (already present on Colab runtimes)
- A Hugging Face account/token (`HF_TOKEN`) with access to `google/gemma-3n-E2B-it`, since Gemma 3n is a gated model. Locally, add it to a `.env` file or export it as an environment variable; on Colab, use the Secrets tab (key icon) instead of hardcoding it.
- Enough disk space to hold the FP16 and quantised GGUF versions of both models
- A GPU is recommended (e.g. Colab's T4 runtime) for faster imatrix calibration, though everything also runs on CPU

## Feedback

All feedback is welcome, just be respectful about it please :). You can reach me at jesseosems123[at]gmail[dot]com or on [LinkedIn](https://linkedin.com/in/jp-osemeke). If you have any questions as well, topics you'd like to discuss or if you'd like to collaborate, feel free to reach out. Thanks!
