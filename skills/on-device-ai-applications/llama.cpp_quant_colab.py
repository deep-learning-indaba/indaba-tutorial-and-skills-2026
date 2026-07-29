# %% [markdown]
# # Building efficient on-device LLMs with llama.cpp
#
# Quantise Gemma 3n and Qwen 3.5 down to GGUF formats that run on phones and
# laptops, then benchmark size vs. speed.
#
# This is the Jupytext "percent" (`# %%`) companion to on-device-ai-colab.ipynb,
# with the same cells in plain-Python form for diffing and editing in
# Jupyter/VS Code. To run it in Colab, convert it back to a notebook first:
#   pip install jupytext
#   jupytext --to notebook llama.cpp_quant_colab.py
# then upload the resulting .ipynb, or just use on-device-ai-colab.ipynb
# directly. Runtime: GPU recommended (Runtime > Change runtime type > T4 GPU)
# for faster imatrix calibration.

# %%
# @title 0. Install Python dependencies
get_ipython().system('pip install -q huggingface_hub[hf_transfer] matplotlib pandas datasets')

# %%
# @title 1. Install & Compile llama.cpp

# Install build tools
get_ipython().system('apt-get update && apt-get install -y cmake build-essential')

# Clone the repository
get_ipython().system('git clone https://github.com/ggml-org/llama.cpp.git')

# Install Python dependencies for the conversion scripts
get_ipython().system('pip install -r llama.cpp/requirements.txt huggingface_hub[hf_transfer]')

# ---------------------------------------------------------
# CRITICAL: Modern CMake Build Step
# ---------------------------------------------------------
# -B build: Creates a 'build' directory (keeps source clean)
# -DGGML_CUDA=ON:  Enable if you have a GPU (remove if CPU only)
# ---------------------------------------------------------
get_ipython().system('cmake -B build -S llama.cpp -DGGML_CUDA=ON')

# Compile the binaries
# --config Release: Optimizes for speed
# -j: Uses all CPU cores for faster compilation
get_ipython().system('cmake --build build --config Release -j')

# %%
import numpy
import pandas

print(numpy.__version__)
print(pandas.__version__)

# %%
# @title 2. Download Models & Calibration Data
import os
from huggingface_hub import snapshot_download
from datasets import load_dataset

# 1. Download Calibration Dataset (WikiText)
dataset = load_dataset("Salesforce/wikitext", "wikitext-2-raw-v1")
train_text = "\n".join(dataset["train"]["text"])

with open("wiki.train.raw", "w", encoding="utf-8") as f:
    f.write(train_text)

print(f"Wrote {len(train_text):,} characters.")

# 2. Download Models (High Speed)
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
# os.environ["HF_TOKEN"] = "YOUR_HF_TOKEN_HERE" # Required for Gemma 3n.
# In Colab, prefer the "Secrets" tab (key icon) to store HF_TOKEN instead of hardcoding it here.

# Qwen 3.5 0.8B
snapshot_download(repo_id="Qwen/Qwen3.5-0.8B", local_dir="./qwen-hf")

# Gemma 3n E2B Instruct
snapshot_download(repo_id="google/gemma-3n-E2B-it", local_dir="./gemma-hf")

print("Downloads Complete")

# %%
# @title 3. Convert to FP16 &

# Convert Qwen
get_ipython().system('python llama.cpp/convert_hf_to_gguf.py ./qwen-hf --outfile ./outputs/qwen/qwen-f16.gguf')

# Convert Gemma 3n
# Note: Gemma 3n uses a complex architecture. The script handles it,
# but ensure you are on the very latest llama.cpp commit.
get_ipython().system('python llama.cpp/convert_hf_to_gguf.py ./gemma-hf --outfile ./outputs/gemma/gemma-f16.gguf')

# %%
# Generating the Importance Matrix
# This step runs inference on the wiki text to learn weight importance.
# It takes a few minutes but creates a "Smart" quantization map.
# Run the commands from inside llama.cpp

# Calculate Qwen Matrix
get_ipython().system('./build/bin/llama-imatrix -m ./outputs/qwen/qwen-f16.gguf -f ./wiki.train.raw -o ./outputs/qwen/qwen-imatrix.dat --chunks 32')  # Higher chunks = better data, slower generation

# Calculate Gemma Matrix
get_ipython().system('./build/bin/llama-imatrix -m ./outputs/gemma/gemma-f16.gguf -f ./wiki.train.raw -o ./outputs/gemma/gemma-imatrix.dat --chunks 32')

print("Calibration Data (IMatrix) Generated")

# %% [markdown]
# We will create two versions of the Qwen model to prove the difference:
# 1. Q4_K_M: The standard "safe" choice.
# 2. IQ3_M: The calibrated "aggressive" choice (smaller, often same quality).

# %%
# 1. Standard Quantization (No Matrix needed)
get_ipython().system('./build/bin/llama-quantize ./outputs/qwen/qwen-f16.gguf ./outputs/qwen/qwen-Q4_K_M.gguf Q4_K_M')

# 2. Calibrated Quantization (Uses qwen-imatrix.dat)
get_ipython().system('./build/bin/llama-quantize --imatrix ./outputs/qwen/qwen-imatrix.dat ./outputs/qwen/qwen-f16.gguf ./outputs/qwen/qwen-IQ3_M.gguf IQ3_M')

# %% [markdown]
# Now, we will do the same for Gemma:
# 1. Q4_K_M: The standard "safe" choice.
# 2. IQ3_M: The calibrated "aggressive" choice (smaller, often same quality).

# %%
# 1. Standard Quantization (No Matrix needed)
get_ipython().system('./build/bin/llama-quantize ./outputs/gemma/gemma-f16.gguf ./outputs/gemma/gemma-Q4_K_M.gguf Q4_K_M')

# 2. Calibrated Quantization (Uses qwen-imatrix.dat)
get_ipython().system('./build/bin/llama-quantize --imatrix ./outputs/gemma/gemma-imatrix.dat ./outputs/gemma/gemma-f16.gguf ./outputs/gemma/gemma-IQ3_M.gguf IQ3_M')

# %% [markdown]
# Let's benchmark and visualise
#
# We'll run `llama-cli` on each model, parse the performance logs, and generate a visual report

# %%
# @title 4. Benchmark & Separate Line Graphs (Qwen vs Gemma)

import subprocess
import re
import matplotlib.pyplot as plt
import pandas as pd

# =========================
# Models
# =========================
models = [
    {"name": "Qwen F16 (Base)", "path": "./outputs/qwen/qwen-f16.gguf"},
    {"name": "Qwen Q4_K_M",     "path": "./outputs/qwen/qwen-Q4_K_M.gguf"},
    {"name": "Qwen IQ3_M",      "path": "./outputs/qwen/qwen-IQ3_M.gguf"},
    {"name": "Gemma F16 (Base)", "path": "./outputs/gemma/gemma-f16.gguf"},
    {"name": "Gemma Q4_K_M",    "path": "./outputs/gemma/gemma-Q4_K_M.gguf"},
    {"name": "Gemma IQ3_M",     "path": "./outputs/gemma/gemma-IQ3_M.gguf"},
]

results = []

print(f"{'Model':<20} | {'Size (MB)':<10} | {'Speed (t/s)':<10}")
print("-" * 45)

# =========================
# Benchmark Loop
# =========================
for m in models:
    if not os.path.exists(m["path"]):
        print(f"{m['name']:<20} | MISSING")
        continue

    # Size
    size_mb = os.path.getsize(m["path"]) / (1024 * 1024)

    # Run inference benchmark
    cmd = [
        "./llama.cpp/build/bin/llama-cli",
        "-m", m["path"],
        "-n", "128",
        "-p", "User: Hi. AI:",
        "-t", "4",
        "-ngl", "0"
    ]

    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        # Extract tokens/sec
        match = re.search(r"([\d.]+)\s+(?:tokens per second|t/s)", res.stdout + res.stderr)
        speed = float(match.group(1)) if match else 0.0

    except Exception as e:
        print(f"Error: {m['name']} -> {e}")
        speed = 0.0

    results.append({
        "Model": m["name"],
        "Size (MB)": size_mb,
        "Speed (t/s)": speed
    })

    print(f"{m['name']:<20} | {size_mb:<10.1f} | {speed:<10.2f}")

# =========================
# DataFrame
# =========================
df = pd.DataFrame(results)

# Split into families
qwen_df = df[df["Model"].str.contains("Qwen")]
gemma_df = df[df["Model"].str.contains("Gemma")]

# =========================
# QWEN: Speed Line Graph
# =========================
plt.figure(figsize=(8, 5))
plt.plot(qwen_df["Model"], qwen_df["Speed (t/s)"], marker="o")
plt.title("Qwen Models — Inference Speed")
plt.ylabel("Tokens/sec")
plt.xticks(rotation=30)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# =========================
# GEMMA: Speed Line Graph
# =========================
plt.figure(figsize=(8, 5))
plt.plot(gemma_df["Model"], gemma_df["Speed (t/s)"], marker="o")
plt.title("Gemma Models — Inference Speed")
plt.ylabel("Tokens/sec")
plt.xticks(rotation=30)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# =========================
# QWEN: Size Line Graph
# =========================
plt.figure(figsize=(8, 5))
plt.plot(qwen_df["Model"], qwen_df["Size (MB)"], marker="o")
plt.title("Qwen Models — File Size")
plt.ylabel("MB")
plt.xticks(rotation=30)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# =========================
# GEMMA: Size Line Graph
# =========================
plt.figure(figsize=(8, 5))
plt.plot(gemma_df["Model"], gemma_df["Size (MB)"], marker="o")
plt.title("Gemma Models — File Size")
plt.ylabel("MB")
plt.xticks(rotation=30)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Path to your generated or downloaded GGUF model
from google.colab import files

model_path = "./outputs/gemma/gemma-IQ3_M.gguf"
files.download(model_path)

# %%
# Path to your generated or downloaded GGUF model
from google.colab import files

model_path2 = "./outputs/qwen/qwen-IQ3_M.gguf"
files.download(model_path2)

# %%
# @title Upload Quantized Models to Hugging Face
from huggingface_hub import HfApi, create_repo

# 1. Configuration
# ---------------------------------------------------------
hf_username = "your-huggingface-username"  # <--- Change this to your HF username
repo_name = "your-repo-name" # <--- Name of your new repo
repo_id = f"{hf_username}/{repo_name}"

# 2. Authenticate & Create Repo
# ---------------------------------------------------------
api = HfApi()

# Create the repository (if it doesn't exist)
print(f"Creating repository: {repo_id}...")
create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)

# 3. Generate a Model Card (Critical for Discovery)
# ---------------------------------------------------------
# This README tells Hugging Face these are GGUF files so
# the "Use in llama.cpp" button appears automatically.
readme_content = f"""---
library_name: gguf
tags:
- gguf
- quantization
- llama.cpp
- imatrix
- mobile
---

# Mobile Quantization Demo Models

This repository contains GGUF quantizations optimized for laptop and mobile deployment.

## Models Included
- **Qwen 3.5 0.8B** (Standard Q4_K_M + Calibrated IQ3_M)
- **Gemma 3 E2B IT** (Standard Q4_K_M + Calibrated IQ3_M)

## Calibration
These models were quantized using **Importance Matrix (IMatrix)** calibration with the WikiText dataset to preserve accuracy at low bit-widths (IQ3/IQ2).

## Usage
```bash
llama-cli -m qwen-IQ3_M.gguf -p "Explain quantum physics" -n 128
```

Run this cell in your notebook. It will create a new repository and upload all your work.
"""

with open("./outputs/README.md", "w") as f3:
    f3.write(readme_content)


# 4. Upload Files
# ---------------------------------------------------------
print("Starting upload... (This may take time based on your internet)")

api.upload_folder(
    folder_path="./outputs",
    repo_id=repo_id,
    repo_type="model", # ONLY upload the quant files, calibration data, and the readme. IGNORE the huge raw model folders (qwen-hf, gemma-hf)
    allow_patterns=["*.gguf", "*.dat", "README.md"],
    commit_message="Upload experimental mobile quants"
)

print(f"Upload Complete! View your models at: https://huggingface.co/{repo_id}")
