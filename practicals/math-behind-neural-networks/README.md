# The Math Behind Neural Networks

**Deep Learning Indaba 2026 — Lagos, Nigeria**

**Session leaders:** Pelumi Victor, Catherine Essuman

**Overseen by:** Claire David

## Summary

This tutorial walks participants through the core mathematics powering neural networks — from linear regression and gradient descent, through logistic regression, to fully connected feedforward networks with backpropagation. We implement everything from scratch in NumPy to build deep intuition, then see how PyTorch automates the same steps with automatic differentiation.

## Materials

| Material | Description |
|:--|:--|
| [`The_Math_Behind_Neural_Networks_Tutorial.ipynb`](The_Math_Behind_Neural_Networks_Tutorial.ipynb) | Follow-along tutorial notebook (used during the session) |
| [`Neural_Network_By_Hand_Exercise.ipynb`](Neural_Network_By_Hand_Exercise.ipynb) | DIY exercise — code a neural network from scratch yourself! |
| [`slides/`](slides/) | Presentation slides (PDF) |

## How to run

Both notebooks are designed to run on **Google Colab** with no local setup required. Dependencies are installed in the first cell of each notebook.

| Notebook | Open in Colab |
|:--|:--|
| Tutorial (follow-along) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/15CPNugK4Uj49ePu2gUyEArG6SWdZ2Ol8) |
| Exercise (DIY) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1DMYdXx7mCOxoReOi9GbSd0TH06fLsh9n) |

**Prerequisites:** Basic Python, some familiarity with calculus and linear algebra.

## Notebook descriptions

### Tutorial notebook (follow-along)

Used during the live session. The instructors walk through each section while participants run the cells alongside the slides. Covers:

1. Linear Regression & Gradient Descent
2. Logistic Regression & Classification
3. Neural Network Building Blocks (Neurons, Activations, Loss Functions)
4. Forward Propagation — from scratch
5. Backpropagation — from scratch
6. Putting It All Together: Training a Neural Network
7. Bonus: The Same Thing in PyTorch

### Exercise notebook (DIY)

A fill-in-the-blanks exercise adapted from [Claire David's T5 tutorial](https://clairedavid.github.io/intro_to_ml/tutorials/t05_nn_by_hand.html). Participants code a neural network from scratch to solve the classic XOR problem. Includes:

- Part I: Guided implementation (weighted sum, activations, feedforward, backprop, training loop)
- Part II: Generalize to dynamic depth and multiple output nodes (bonus)
- Part III: Double spiral challenge (bonus)

## Reference material

- [Claire David's Intro to ML — Neural Networks](https://clairedavid.github.io/intro_to_ml/nn/nn_0_intro.html)
- [TensorFlow Playground](https://playground.tensorflow.org) — interactive visualization
- [Google Slides version of the presentation](https://docs.google.com/presentation/d/10m61ipGlTce7AMhK5Qa9zXQRDO5VTdXXsv_29kJSIPo/edit?usp=sharing)
