# Study Guide: Papers and Concepts

**Every paper cited in the session, explained in plain language.**

You do not need to have read any of these to follow the session. This guide exists so that afterwards you can go back to the primary sources and know what you are looking at. Each entry gives you **what it says**, **why it matters**, and **going deeper** for the detail behind the headline result.

Organised by theme, following the arc of the session.

---

## Attacks Are Optimisation

### Szegedy et al., "Intriguing Properties of Neural Networks" (2014)

**What it says:** The first formal demonstration that neural networks can be fooled by small, deliberately computed perturbations that are imperceptible to humans, and that these perturbations transfer across different models trained on the same task.

**Why it matters:** The founding observation that started the field.

**Going deeper:** Transferability, the fact that a perturbation crafted against one model often fools a *different* model too, is exactly why black-box attacks (Papernot, below) are possible even without access to the target's weights.

### Goodfellow, Shlens & Szegedy, "Explaining and Harnessing Adversarial Examples" (ICLR 2015)

**What it says:** Introduces FGSM (Fast Gradient Sign Method): take one step in the direction of the sign of the loss gradient with respect to the input, scaled by epsilon. It also argues that adversarial examples exist because models are *too linear*, not too nonlinear. A linear function is easy to push far in a bad direction with a tiny, coordinated nudge across many input dimensions.

**Why it matters:** The simplest and fastest attack, and the optimisation view of an adversarial example expressed in one line of maths.

**Going deeper:** FGSM is a *single* gradient step, so it is cheap but weak. PGD (below) iterates the same idea and is much stronger. As for why FGSM works at all, the linearity hypothesis is the honest answer: small per-pixel changes summed across thousands of pixels can shift a mostly linear decision boundary a long way.

### Madry et al., "Towards Deep Learning Models Resistant to Adversarial Attacks" (ICLR 2018)

**What it says:** Formalises robustness as a min-max (saddle point) optimisation: minimise, over model weights, the maximum, over allowed perturbations, of the loss. Introduces PGD (Projected Gradient Descent) as the universal first-order attack: iteratively step in the gradient-sign direction, then project back into the allowed epsilon-ball. Proposes adversarial training, meaning training on PGD-perturbed examples.

**Why it matters:** This is the paper the whole session's mental model comes from. The attacker maximises, the defender minimises, and the two are playing a game.

**Going deeper:** Why PGD rather than FGSM repeated many times? PGD adds the projection step, clipping back into the epsilon-ball after each step, and typically starts from a random point inside that ball. Both changes make it a much stronger and more reliable attack than repeated unprojected FGSM steps.

### Korpelevich, "The Extragradient Method for Finding Saddle Points and Other Problems" (1976)

**What it says:** A classical optimisation method for solving saddle-point (min-max) problems. It takes an extra look-ahead gradient step before the real update, which reduces the oscillation that naive alternating gradient descent suffers from in these games.

**Why it matters:** Robust training is a two-player game, and naively alternating between training the defender and training the attacker does not reliably converge. Extragradient-style methods are the principled fix.

**Going deeper:** In a min-max game, plain gradient descent-ascent can circle around the saddle point forever rather than converging to it. Look-ahead and extrapolation steps, meaning extragradient and its modern descendants, dampen that rotation.

### Papernot et al., "Practical Black-Box Attacks against Machine Learning" (ASIACCS 2017)

**What it says:** You can attack a model with zero access to its weights or gradients. Train a substitute model on inputs and outputs queried from the target, craft adversarial examples against your substitute, and thanks to transferability they often fool the real target too.

**Why it matters:** Establishes that "I do not expose my model's internals" is not a security guarantee.

**Going deeper:** This is why API-only deployment is not automatically safe from adversarial attack. Query access alone can be enough.

### Geirhos et al., "Shortcut Learning in Deep Neural Networks" (Nature Machine Intelligence, 2020)

**What it says:** Models often achieve high accuracy by latching onto spurious, dataset-specific cues such as a texture, a background, or a watermark, rather than the concept a human would use. They are right for the wrong reason, and they fail as soon as that shortcut is not present.

**Why it matters:** Complements the adversarial story. Some failures involve no attacker at all, just a model that never learned what we assumed it learned.

**Going deeper:** Distribution shift and shortcut learning are related but distinct. Shortcut learning is about *why* a model generalises poorly even on natural data, while adversarial robustness is about worst-case, deliberately crafted inputs. Both show that accuracy alone hides what the model actually learned.

---

## Attacks on Language Models

### Zou et al., "Universal and Transferable Adversarial Attacks on Aligned Language Models" (2023), known as GCG

**What it says:** An automated, gradient-based discrete search finds a suffix string that, appended to almost any harmful request, gets safety-aligned LLMs to comply. The same suffix often transfers across different models.

**Why it matters:** The LLM-era equivalent of PGD, meaning a systematic automated search rather than a hand-crafted prompt trick.

**Going deeper:** "Universal and transferable" is the key result. One discovered suffix worked broadly, not just against the model it was optimised on, echoing Szegedy's original transferability finding in a new modality.

### Andriushchenko, Croce & Flammarion, "Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks" (ICLR 2025)

**What it says:** A simple adaptive attack, using random search over a suffix that maximises the probability the model's response starts with something like "Sure, here is", reliably jailbreaks essentially every major safety-aligned model tested, often more effectively than far more complex methods.

**Why it matters:** It is the paper behind the session's core evaluation lesson. No single fixed attack generalises, so evaluation must be adaptive.

**Going deeper:** Why does forcing the start of the reply work so well? Autoregressive LLMs generate token by token, conditioned on everything so far. Once the model has "said" the first few compliant tokens, continuing in that direction is far more likely than reversing course to refuse.

### Greshake et al., "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (2023)

**What it says:** LLM applications that read external content such as web pages, documents, or emails in order to answer questions can be hijacked by instructions hidden inside that content. The attacker never talks to the model directly.

**Why it matters:** The most practically dangerous class of prompt injection for RAG and agentic systems, because the untrusted content does not look like user input.

---

## Defence

### Shafahi et al., "Adversarial Training for Free!" (NeurIPS 2019)

**What it says:** Standard adversarial training in the style of Madry is expensive, because it multiplies training cost by the number of attack steps per batch. This paper recycles gradient computations across the model-update and attack-generation steps, so adversarial training costs roughly the same as normal training.

**Why it matters:** Answers the obvious objection that adversarial training sounds too expensive to be practical.

### Wong, Rice & Kolter, "Fast is Better than Free: Revisiting Adversarial Training" (ICLR 2020)

**What it says:** Even simple FGSM-based adversarial training, done carefully with random initialisation to avoid a failure mode called catastrophic overfitting, can match multi-step PGD training at a fraction of the cost.

**Why it matters:** Reinforces that robustness does not have to mean prohibitively expensive training. Cheap and practical variants exist.

---

## The Evaluation Trap

### Athalye, Carlini & Wagner, "Obfuscated Gradients Give a False Sense of Security" (ICML 2018)

**What it says:** Surveyed several published defences that looked robust against standard attacks, and showed most of them worked only because they broke gradient-based attacks, through non-differentiable steps, randomisation, or vanishing and exploding gradients, rather than because the underlying model was actually harder to fool. Once evaluated with attacks adapted to bypass the obfuscation, most of these robust defences collapsed.

**Why it matters:** This is the paper behind the keyword-filter demo in the notebook, and behind the whole idea that a robustness number can lie.

**Going deeper:** What exactly is a masked or obfuscated gradient? Any defence mechanism that makes gradient computation uninformative, such as a non-differentiable preprocessing step or randomised inputs, will make gradient-based attacks report artificially low success rates. Not because the model resists the perturbation, but because the *attack itself* can no longer find the way through. The keyword filter in the notebook is a crude, non-gradient analogue: it blocks the literal attack it was tested against, not the underlying capability to elicit disallowed content.

### Carlini et al., "On Evaluating Adversarial Robustness" (2019)

**What it says:** A methodological checklist for evaluating robustness claims properly: attack adaptively, report against the strongest attack you can construct for the specific defence, and be suspicious of very high claimed robustness numbers.

**Why it matters:** The practical companion to the obfuscated-gradients paper. If you take one operational habit away from this session, take this one.

---

## Evaluation and Sovereignty

### Adelani et al., "IrokoBench: A New Benchmark for African Languages in the Age of LLMs" (NAACL 2025)

**What it says:** Introduces a benchmark spanning multiple African languages and tasks, evaluates frontier LLMs, and finds a large and consistent performance gap relative to English.

**Why it matters:** Concrete evidence that imported benchmarks and imported models do not transfer.

### AfroBench (ACL Findings 2025)

**What it says:** A broader benchmark evaluating LLMs across African languages and tasks. It corroborates the IrokoBench finding that even top proprietary models underperform substantially compared to English.

**Why it matters:** A second independent source for the same conclusion, which strengthens the claim beyond a single benchmark.

*A note on the figures:* the percentages quoted in the session are approximate and are drawn from these papers as published. Benchmark numbers move as models and evaluation suites are updated, so check the current abstracts before quoting a precise figure in your own work.

---

## Quick reference

| Concept | One-liner |
|---|---|
| Adversarial example | Solution to "maximise loss within a small input budget" (Goodfellow 2015) |
| Robust training | Min-max game: attacker maximises, defender minimises (Madry 2018) |
| FGSM | One gradient-sign step |
| PGD | Iterated, projected FGSM, and much stronger |
| Black-box attack | No weights needed: query, substitute model, transferability (Papernot 2017) |
| GCG | Automated discrete token search jailbreak (Zou 2023) |
| Adaptive random search | Simple suffix search breaks nearly every safety-aligned model (Andriushchenko 2025) |
| Indirect prompt injection | Malicious instructions hidden in retrieved or third-party content (Greshake 2023) |
| Adversarial training, cheap | Free (Shafahi 2019), Fast (Wong 2020) |
| Obfuscated gradients | A defence can look robust by breaking the *attack*, not the *vulnerability* (Athalye, Carlini & Wagner 2018) |
| Evaluate honestly | Attack adaptively, never trust a single fixed-attack number (Carlini 2019) |
| IrokoBench / AfroBench | Frontier LLMs lag substantially behind English on African languages |

---

All techniques described here are credited to their original authors. Full citations with links are in [`reading_list.md`](reading_list.md).
