# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "huggingface-hub[hf-transfer]==1.20.0",
#     "matplotlib==3.11.0",
#     "pandas==3.0.3",
# ]
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


app._unparsable_cell(
    r"""
    # @title 1. Install & Compile llama.cpp
    # !pip install huggingface_hub[hf_transfer] matplotlib pandas

    # Install build tools
    !apt-get update && apt-get install -y cmake build-essential

    # Clone the repository
    !git clone https://github.com

    # Install Python dependencies for the conversion scripts
    !pip install -r llama.cpp/requirements.txt huggingface_hub[hf_transfer]

    # ---------------------------------------------------------
    # CRITICAL: Modern CMake Build Step
    # ---------------------------------------------------------
    # -B build: Creates a 'build' directory (keeps source clean)
    # -DGGML_CUDA=ON:  Enable if you have a GPU (remove if CPU only)
    # ---------------------------------------------------------
    !cmake -B build -S llama.cpp -DGGML_CUDA=ON

    # Compile the binaries
    # --config Release: Optimizes for speed
    # -j: Uses all CPU cores for faster compilation
    !cmake --build build --config Release -j
    """,
    name="_"
)


@app.cell
def _():
    import numpy
    import pandas

    print(numpy.__version__)
    print(pandas.__version__)
    return


@app.cell
def _():
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
    # os.environ["HF_TOKEN"] = "YOUR_HF_TOKEN_HERE" # Required for Gemma 3n. You can also add this to a .env file

    # Qwen 3.5 0.8B
    snapshot_download(repo_id="Qwen/Qwen3.5-0.8B", local_dir="./qwen-hf")

    # Gemma 3n E2B Instruct
    snapshot_download(repo_id="google/gemma-3n-E2B-it", local_dir="./gemma-hf")

    print("Downloads Complete")
    return (os,)


app._unparsable_cell(
    r"""
    # @title 3. Convert to FP16 &

    # Convert Qwen
    !python llama.cpp/convert_hf_to_gguf.py ./qwen-hf --outfile qwen-f16.gguf

    # Convert Gemma 3n
    # Note: Gemma 3n uses a complex architecture. The script handles it,
    # but ensure you are on the very latest llama.cpp commit.
    !python llama.cpp/convert_hf_to_gguf.py ./gemma-hf --outfile gemma-f16.gguf
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    # Generating the Importance Matrix
    # This step runs inference on the wiki text to learn weight importance.
    # It takes a few minutes but creates a "Smart" quantization map.
    # Run the commands from inside llama.cpp

    # Calculate Qwen Matrix
    !./build/bin/llama-imatrix \
        -m ../qwen-f16.gguf \
        -f ../wiki.train.raw \
        -o ../qwen-imatrix.dat \
        --chunks 32 # Higher chunks = better data, slower generation

    # Calculate Gemma Matrix
    !./build/bin/llama-imatrix \
        -m ../gemma-f16.gguf \
        -f ../wiki.train.raw \
        -o ../gemma-imatrix.dat \
        --chunks 32

    print("Calibration Data (IMatrix) Generated")
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will create two versions of the Qwen model to prove the difference:
    1. Q4_K_M: The standard "safe" choice.
    2. IQ3_M: The calibrated "aggressive" choice (smaller, often same quality).
    """)
    return


app._unparsable_cell(
    r"""
    # 1. Standard Quantization (No Matrix needed)
    !./build/bin/llama-quantize qwen-f16.gguf qwen-Q4_K_M.gguf Q4_K_M

    # 2. Calibrated Quantization (Uses qwen-imatrix.dat)
    !./build/bin/llama-quantize \
        --imatrix qwen-imatrix.dat \
        qwen-f16.gguf \
        qwen-IQ3_M.gguf \
        IQ3_M
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    Now, we will do the same for Gemma:
    1. Q4_K_M: The standard "safe" choice.
    2. IQ3_M: The calibrated "aggressive" choice (smaller, often same quality).
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    # 1. Standard Quantization (No Matrix needed)
    !./build/bin/llama-quantize gemma-f16.gguf gemma-Q4_K_M.gguf Q4_K_M

    # 2. Calibrated Quantization (Uses qwen-imatrix.dat)
    !./build/bin/llama-quantize \
        --imatrix gemma-imatrix.dat \
        gemma-f16.gguf \
        gemma-IQ3_M.gguf \
        IQ3_M
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's benchmark and visualise

    We'll run `llama-cli` on each model, parses the performance logs, and generates a visual report
    """)
    return


@app.cell
def _(os):
    # @title 4. Benchmark & Separate Line Graphs (Qwen vs Gemma)

    import subprocess
    import re
    import matplotlib.pyplot as plt
    import pandas as pd

    # =========================
    # Models
    # =========================
    models = [
        {"name": "Qwen F16 (Base)", "path": "qwen-f16.gguf"},
        {"name": "Qwen Q4_K_M",     "path": "qwen-Q4_K_M.gguf"},
        {"name": "Qwen IQ3_M",      "path": "qwen-IQ3_M.gguf"},
        {"name": "Gemma F16 (Base)", "path": "gemma-f16.gguf"},
        {"name": "Gemma Q4_K_M",    "path": "gemma-Q4_K_M.gguf"},
        {"name": "Gemma IQ3_M",     "path": "gemma-IQ3_M.gguf"},
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
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
