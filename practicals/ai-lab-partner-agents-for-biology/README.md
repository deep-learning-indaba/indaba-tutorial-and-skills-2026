# 🧬 The AI Lab Partner: Agents for Biological Discovery

<a href="https://ibb.co/5WJ92c2C"><img src="https://i.ibb.co/HD92XgXR/Screenshot-2026-07-24-at-14-50-56.png" alt="Screenshot-2026-07-24-at-14-50-56" border="0"></a>

Welcome to the **AI Lab Partner** tutorial, developed for the Deep Learning Indaba 2026 in Lagos, Nigeria! 🇳🇬

This repository contains an interactive Google Colab notebook designed to teach the **agentic workflow** of using Large Language Models (LLMs) like Gemini not just as chatbots, but as active reasoning agents in a computational biology pipeline. 

Instead of getting bogged down in writing complex bioinformatics scripts from scratch, you will learn how to prompt an AI agent to build a **Closed-Loop Multi-Objective Protein Optimization** pipeline.

## 🎯 What You Will Build
In this tutorial, we tackle a real-world challenge: engineering **Single-Chain Insulin** to be highly thermostable. This is a critical step toward eliminating the need for fragile cold-chain storage in regions like West Africa. 

By the end of the notebook, you will have built an automated "AI Scientist" that iteratively designs, tests, and refines protein mutations.

## 📚 Key Concepts Covered
1. **Target Discovery:** Using LLMs to identify high-impact biological targets (e.g., malaria antigens, insulin) based on specific geographic and logistical constraints.
2. **Data Fetching & Visualization:** Programmatically interacting with the UniProt API and rendering 3D protein structures directly in the notebook using `py3Dmol`.
3. **Biological Metrics:** Understanding core concepts like Hydrophobicity, Solvency (SASA), and Immunogenicity.
4. **The Oracle Models:** Setting up state-of-the-art predictive models on a Colab CPU:
   - **ESMFold:** For rapid structural prediction.
   - **ThermoFormer:** For predicting thermal stability (Optimal Growth Temperature).
   - **ESM-2:** For zero-shot evolutionary fitness scoring.
   - **MHCflurry:** For predicting immunogenicity and preventing auto-immune risks.
5. **Multi-Objective Optimization Loop:** Building a closed-loop system where Gemini proposes structurally-sound mutations, tests them against multiple competing constraints, and learns from its failures.

## 🚀 Getting Started
1. **Open the Notebook:** Upload the `.ipynb` file to your Google Colab environment.
2. **Set up your Gemini API Key:** 
   - Get a free API key from Google AI Studio.
   - In your Colab notebook, click the **🔑 Secrets** icon on the left sidebar.
   - Add a new secret named `GEMINI_API_KEY` and paste your key.
3. **Run the Cells:** Follow the prompts and run the code cells sequentially. You do not need a GPU for this tutorial; a standard Colab CPU instance is sufficient.

## ⚠️ Important Security Warning
**NEVER hardcode your API keys directly into the notebook cells!** 
Always use the Colab Secrets manager (`userdata.get('GEMINI_API_KEY')`) to load your keys. If you accidentally hardcode your key and push the notebook to GitHub, your key will be compromised.

## 🤝 Contributing
This is an educational resource. If you find bugs, typos, or have suggestions for improving the agentic workflow prompts, please open an issue or submit a pull request!

## ✏️ Authors
This session was co-written by Natasha Latysheva, Adam Kosiorek, Kyle Taylor, Sebastian Bodenstein, and Alexander Karollus.
