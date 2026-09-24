import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch F)"')

# Create 12-interview-questions directory files
wc("12-interview-questions/ml-interview-questions.md", r"""# ML Interview Questions

Each question includes: Expected Answer • Key Concepts • Likely Follow-Up • Common Wrong Answer • What Strong Candidates Add

---

## Q1. What is the bias-variance tradeoff?

**Expected Answer:** Every model's test error decomposes as: $\text{Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise}$. Bias is error from wrong assumptions (underfitting); variance is sensitivity to training data fluctuations (overfitting). Simpler models have high bias, low variance; complex models have low bias, high variance. Regularization, ensemble methods, and cross-validation manage this tradeoff.

**Key Concepts:** Decomposition formula, underfitting vs overfitting, regularization, ensemble methods.

**Likely Follow-Up:** "How does ensemble learning (Random Forest) reduce variance without increasing bias?" — Averaging independent high-variance models reduces their combined variance by factor $1/N$ (assuming independence).

**Common Wrong Answer:** "Bias is when the model is biased toward certain predictions" — this conflates statistical bias with fairness bias.

**Strong Candidates Add:** The mathematical derivation $E[(y-\hat{f})^2] = \text{Bias}[\hat{f}]^2 + \text{Var}[\hat{f}] + \sigma^2$; how dropout addresses variance; that irreducible noise sets a hard floor on achievable performance.

---

## Q2. Explain gradient descent and its variants.

**Expected Answer:** Gradient Descent minimizes loss by iteratively moving parameters in the opposite direction of the gradient: $\theta \leftarrow \theta - \alpha\nabla_\theta\mathcal{L}$. Variants: Batch GD (full dataset per step, slow), SGD (one sample, noisy), Mini-batch SGD (practical default). Adaptive optimizers: Adam (momentum + per-parameter LR via first and second moment estimates), RMSProp, AdaGrad.

**Key Concepts:** Gradient, learning rate, SGD, momentum, Adam, convergence.

**Likely Follow-Up:** "Why does SGD sometimes generalize better than Adam?" — SGD's noise acts as implicit regularization, finding flatter minima that generalize better. Adam converges faster but can find sharp, less generalizable minima.

**Common Wrong Answer:** Describing Adam as "always better than SGD" — several papers show SGD + momentum outperforms Adam on image classification when properly tuned.

**Strong Candidates Add:** Adam hyperparameters ($\beta_1=0.9$, $\beta_2=0.999$, $\epsilon=10^{-8}$), learning rate scheduling (warmup + cosine decay), gradient clipping for RNN/Transformer training stability.

---

## Q3. What is cross-entropy loss and why is it used for classification?

**Expected Answer:** Cross-entropy loss: $\mathcal{L} = -\sum_k y_k \log \hat{p}_k$. For binary classification: $\mathcal{L} = -[y\log\hat{p} + (1-y)\log(1-\hat{p})]$. It is derived from Maximum Likelihood Estimation: minimizing cross-entropy is equivalent to maximizing the likelihood of the training data under a Categorical distribution. It penalizes confident wrong predictions logarithmically (infinite penalty for predicting 0 probability for the correct class).

**Key Concepts:** MLE, log-likelihood, softmax, probability calibration.

**Likely Follow-Up:** "Why not use MSE for classification?" — MSE doesn't penalize confident wrong predictions sufficiently and produces very small gradients when the sigmoid output is near 0 or 1 (vanishing gradient in output layer).

**Common Wrong Answer:** "Cross-entropy just measures how close the predictions are to labels" — misses the MLE/information-theoretic grounding.

**Strong Candidates Add:** The connection $H(P,Q) = H(P) + D_{KL}(P||Q)$ — minimizing cross-entropy is minimizing KL divergence from the true distribution; label smoothing as a regularization that prevents overconfident predictions.

---

## Q4. How does a Random Forest differ from Gradient Boosting?

**Expected Answer:** Random Forest grows many independent decision trees in parallel using bootstrap samples and random feature subsets (bagging + feature randomization). It reduces variance by averaging predictions. Gradient Boosting grows trees sequentially, each fitting the residuals of the previous ensemble, reducing bias. RF is harder to overfit; XGBoost/LightGBM (GBT implementations) achieve higher accuracy but require more careful regularization.

**Key Concepts:** Bagging vs boosting, variance reduction vs bias reduction, parallel vs sequential.

**Likely Follow-Up:** "When would you choose Random Forest over XGBoost?" — RF is preferred when training speed matters, when data is very noisy (boosting can overfit noise), or when interpretability of individual trees is needed.

**Common Wrong Answer:** Confusing bagging and boosting. Bagging = parallel, independent. Boosting = sequential, dependent.

**Strong Candidates Add:** Gradient Boosting's update rule: $F_m(x) = F_{m-1}(x) + \gamma_m h_m(x)$ where $h_m$ fits negative gradients (pseudo-residuals); LightGBM's leaf-wise growth vs XGBoost's level-wise growth; SHAP values for both.

---

## Q5. What is overfitting and how do you prevent it?

**Expected Answer:** Overfitting occurs when a model learns the training data noise rather than the underlying signal, achieving high training accuracy but poor generalization. Prevention: more training data, regularization (L1/L2/dropout), early stopping, cross-validation, reducing model complexity, data augmentation, batch normalization.

**Key Concepts:** Generalization, train/val/test split, regularization, model complexity.

**Likely Follow-Up:** "How does dropout prevent overfitting?" — Randomly zeroing activations forces the network to learn redundant representations. No single unit can rely on specific co-activations, preventing complex co-adaptations. Equivalent to training an ensemble of $2^N$ thinned networks.

**Common Wrong Answer:** Treating overfitting as "model is too big" — model size alone isn't the issue; the ratio of parameters to training samples is.

**Strong Candidates Add:** Double descent phenomenon — as model size grows beyond interpolation threshold, test error can decrease again; early stopping implicitly bounds model complexity by the optimization path; weight decay (L2) is equivalent to Gaussian prior MAP estimation.
""")

wc("12-interview-questions/deep-learning-questions.md", r"""# Deep Learning Interview Questions

---

## Q1. How does backpropagation work?

**Expected Answer:** Backpropagation applies the chain rule to compute gradients of the loss with respect to all parameters. For a composition $L = f(g(h(x)))$: $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial f}\cdot\frac{\partial f}{\partial g}\cdot\frac{\partial g}{\partial h}\cdot\frac{\partial h}{\partial x}$. Starting from the output, we propagate error signals backward through each layer, computing local Jacobians and multiplying them. PyTorch builds a dynamic computation graph (DAG) and traverses it in reverse topological order.

**Key Concepts:** Chain rule, computation graph, local gradients, vanishing/exploding gradients.

**Likely Follow-Up:** "What is the vanishing gradient problem and how do residual connections fix it?" — Multiplying many Jacobians (each < 1 for saturating activations) approaches zero. Residual connections add an identity path: gradient = $F'(x) + I$, so even if $F'(x) \to 0$, gradient is still $\approx 1$.

**Common Wrong Answer:** "Backprop just adjusts weights toward the correct answer" — misses the calculus derivation and chain rule.

**Strong Candidates Add:** Gradient checkpointing for memory efficiency; mixed-precision training accumulates gradients in FP32 to avoid underflow; gradient accumulation simulates larger batches.

---

## Q2. What are activation functions and why do we need non-linear ones?

**Expected Answer:** Activation functions introduce non-linearity. Without them, any stack of linear layers collapses to a single linear transformation (matrix product is closed under composition). Non-linear activations enable the Universal Approximation Theorem: a two-layer network with enough units can approximate any continuous function. Common activations: ReLU ($\max(0,x)$, fast, sparse), GELU ($x\Phi(x)$, smooth, used in transformers), Sigmoid (saturates, used in gates), Tanh (zero-centered sigmoid).

**Key Concepts:** Non-linearity, UAT, dying ReLU, vanishing gradients, GELU vs ReLU.

**Likely Follow-Up:** "What is the dying ReLU problem?" — Neurons with consistently negative pre-activation receive zero gradient and never recover. Leaky ReLU and ELU address this with a small negative slope.

**Common Wrong Answer:** "We need non-linear activations so the network is more complex" — misses the mathematical reason (composition of linear functions is linear).

**Strong Candidates Add:** GELU's probabilistic interpretation (Gaussian CDF gating); SwiGLU's gating mechanism in modern LLMs; BatchNorm/LayerNorm as "activation normalization" that keeps activations in the non-saturated regime.

---

## Q3. Explain the transformer attention mechanism mathematically.

**Expected Answer:** $\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$. Q, K, V are linear projections of the input. The dot product $QK^T$ computes pairwise similarities between queries and keys; dividing by $\sqrt{d_k}$ prevents softmax saturation from large dot products in high dimensions; softmax normalizes to attention weights; weighted sum of V produces the output. Multi-head attention applies this in $h$ parallel subspaces and concatenates.

**Key Concepts:** QKV projections, scaling, softmax, multi-head, $O(N^2)$ complexity.

**Likely Follow-Up:** "Why scale by $\sqrt{d_k}$?" — When $d_k$ is large, random initialization causes dot products to have magnitude $\sqrt{d_k}$. Without scaling, softmax receives very large inputs and becomes nearly one-hot, losing gradient signal.

**Common Wrong Answer:** Dividing by $d_k$ instead of $\sqrt{d_k}$.

**Strong Candidates Add:** Flash Attention's IO-aware implementation that fuses operations to avoid writing the $N\times N$ attention matrix to HBM; GQA (Grouped Query Attention) in Llama which reduces KV-cache by sharing K,V across multiple Q heads.

---

## Q4. What is batch normalization and when should you use it?

**Expected Answer:** BatchNorm normalizes each feature across the batch: $\hat{x} = (x-\mu_B)/\sqrt{\sigma_B^2+\epsilon}$, then rescales with learnable $\gamma, \beta$. Benefits: reduces internal covariate shift, allows higher learning rates, acts as regularizer (different for each batch's noise). Drawbacks: depends on batch size (fails for small batches), problematic for sequential data and variable-length sequences. Use LayerNorm for Transformers/RNNs; BatchNorm for CNNs/MLPs with adequate batch size.

**Key Concepts:** Internal covariate shift, batch statistics, learnable scale/shift, train vs inference mode.

**Likely Follow-Up:** "What changes at inference time for BatchNorm?" — Uses running mean/variance accumulated during training (via exponential moving average), not batch statistics. Important to call `model.eval()` in PyTorch.

**Common Wrong Answer:** "BatchNorm prevents overfitting" — it reduces internal covariate shift primarily; regularization effect is a side benefit.

**Strong Candidates Add:** GroupNorm as a compromise between BatchNorm and LayerNorm; Instance Normalization for style transfer; the failure mode of BatchNorm with batch size 1.
""")

wc("12-interview-questions/llm-rag-questions.md", r"""# LLM & RAG Interview Questions

---

## Q1. What is RAG and when would you use it instead of fine-tuning?

**Expected Answer:** RAG (Retrieval-Augmented Generation) retrieves relevant documents at inference time and injects them into the LLM's context. Use RAG when: knowledge is frequently updated (news, docs), you need source attribution, data is proprietary/confidential (can't expose to training), or you need to handle very large knowledge bases (>what fits in context). Use fine-tuning when: you need the model to learn a new style/format/behavior, the domain has very specific terminology, or you need inference latency improvement from fewer context tokens.

**Key Concepts:** Retrieval, chunking, embedding, in-context learning, knowledge freshness.

**Likely Follow-Up:** "What are the failure modes of RAG?" — Retrieval failure (relevant doc not retrieved), context faithfulness (LLM ignores retrieved context), chunking artifacts (answer splits across chunks), semantic gap (query and document use different vocabulary).

**Common Wrong Answer:** "RAG is always better because you don't need to retrain" — RAG adds retrieval latency and fails when the answer requires synthesizing across many documents or understanding domain-specific reasoning patterns not in the retrieved text.

**Strong Candidates Add:** RAGAS evaluation framework (faithfulness, answer relevancy, context recall); hybrid retrieval (BM25 + dense); HyDE (generate hypothetical document, then retrieve); reranking with cross-encoders.

---

## Q2. Explain RLHF. What is the reward model and why is it needed?

**Expected Answer:** RLHF (Reinforcement Learning from Human Feedback) has three stages: (1) Supervised Fine-Tuning (SFT) on high-quality human demonstrations; (2) Reward Model (RM) training: annotators rank model outputs, train a regression model to score outputs; (3) RL optimization: use PPO to maximize the reward model's score while a KL-divergence penalty prevents the policy from drifting too far from the SFT model. The reward model is needed because "good response" isn't easily defined by a differentiable loss — human preferences require a learned proxy.

**Key Concepts:** SFT, reward model, PPO, KL penalty, preference data.

**Likely Follow-Up:** "What is DPO and how does it differ from RLHF?" — DPO (Direct Preference Optimization) eliminates the separate RM and RL loop. It directly optimizes the policy using preference pairs, mathematically equivalent to RLHF under certain assumptions but simpler, more stable, and cheaper to implement.

**Common Wrong Answer:** "RLHF just means training the model to follow instructions" — SFT alone is instruction tuning; RLHF specifically adds the preference-based reward loop.

**Strong Candidates Add:** Constitutional AI (Anthropic's approach using AI feedback instead of human feedback for some stages); reward hacking (RM can be gamed, leading to degenerate outputs that score high but are poor); the tension between helpfulness and harmlessness.

---

## Q3. What is hallucination in LLMs and how do you mitigate it?

**Expected Answer:** Hallucination is when LLMs generate fluent, confident text that is factually incorrect. Types: intrinsic (contradicts the provided context), extrinsic (makes up external facts). Causes: models predict plausible next tokens, not truthful statements; training data noise; lack of explicit "I don't know" training. Mitigations: RAG (ground answers in retrieved documents), sampling with temperature 0 for factual tasks, chain-of-thought prompting, self-consistency (sample multiple answers), factual consistency training, tool use (search, calculator), output verification.

**Key Concepts:** Types of hallucination, RAG grounding, temperature, self-consistency.

**Likely Follow-Up:** "How would you build a system to detect hallucinations?" — Use a separate verifier model, compare claims to retrieved sources using NLI (Natural Language Inference), or use LLM-as-judge to score faithfulness.

**Common Wrong Answer:** "Just lower the temperature to 0" — greedy decoding reduces diversity but doesn't eliminate hallucination; models can confidently generate wrong facts.

**Strong Candidates Add:** SelfCheckGPT (sample multiple times, inconsistency across samples indicates hallucination); FACTSCORE for biography generation; citation-based generation where every claim is tied to a retrieved source.

---

## Q4. What is quantization and what are the tradeoffs?

**Expected Answer:** Quantization represents model weights/activations in lower-precision data types (FP16, INT8, INT4) to reduce memory and improve inference speed. PTQ (Post-Training Quantization): quantize after training, fast but accuracy loss. QAT (Quantization-Aware Training): simulate quantization during training, better accuracy. NF4 (NormalFloat4) used in QLoRA: designed for normally-distributed weights, minimal quality loss at 4-bit. Tradeoffs: 4-bit reduces model size 8x (FP32→INT4) but loses some accuracy, requires careful outlier handling (absmax/zeropoint scaling).

**Key Concepts:** PTQ vs QAT, INT8/INT4/NF4, accuracy tradeoff, bitsandbytes.

**Likely Follow-Up:** "What is GPTQ?" — A PTQ algorithm that computes quantization errors layer-by-layer using second-order information, achieving near-lossless INT4 quantization for large LLMs.

**Common Wrong Answer:** "Quantization always significantly degrades accuracy" — with modern methods (GPTQ, AWQ, NF4), 4-bit quantization of large LLMs often loses only 0-2% performance.

**Strong Candidates Add:** The outlier problem in LLM quantization: a few outlier weights/activations have very large magnitudes, making naive quantization poor. LLM.int8() and SmoothQuant address this by mixed-precision or migrating outlier difficulty from activations to weights.
""")

wc("13-project-defense/NEXEN.md", r"""# NEXEN Project Defense — Rainfall Regime-Aware Bias Correction

## Project Overview

**Project:** NEXEN (SIH26080) — A Rainfall Regime-Aware Statistical Bias Correction System for Climate Model Outputs  
**Problem:** Climate models systematically over- or under-predict rainfall compared to observed data. The bias is not uniform — it varies by rainfall regime (dry, moderate, extreme).  
**Goal:** Build a bias correction pipeline that is regime-aware, outperforms standard methods (quantile mapping, delta method) on extreme precipitation events.

---

## Architecture Q&A

### Q1. Why did you choose a regime-aware approach over standard quantile mapping?

**Answer:** Standard Quantile Mapping (QM) maps the entire distribution uniformly. It performs well on median precipitation but poorly on extremes — the tails have too few samples for robust quantile estimation. By first classifying days into rainfall regimes (Dry: <1mm, Light: 1-10mm, Moderate: 10-50mm, Extreme: >50mm), we build separate correction models per regime. This allows the extreme regime correction to be calibrated on extreme events specifically, improving Extreme Value Index (EVI) by ~18% compared to global QM.

**Key Architecture Choice:** DBSCAN clustering on precipitation PDFs for regime identification, followed by regime-conditioned QM with LOWESS smoothing for the extreme tail.

---

### Q2. What was your model selection process?

**Answer:** We evaluated: (1) Delta Method (baseline — simplest, just shift mean), (2) Standard Quantile Mapping, (3) Quantile Delta Mapping (QDM — preserves trends), (4) EDCDF (equidistant CDF matching), and (5) our Regime-Aware QM (RAQM).

Evaluated on: Monthly precipitation totals, 95th percentile exceedance (extreme events), wet-day frequency (drizzle bias), spatial coherence (correlation fields).

RAQM outperformed on extremes and wet-day frequency. QDM outperformed on trend preservation. Final system: RAQM for short-term application, QDM blend for long-term trend-preserving scenarios.

---

### Q3. How did you evaluate the system?

**Answer:** 
- **Cross-validation:** Leave-one-year-out (LOYO) CV on the historical period (1990-2020). Cannot use random k-fold — temporal autocorrelation in climate data means random splits leak future information.
- **Metrics used:** RMSE (overall), 95th percentile error (extreme bias), Wet-day Frequency Error (WFE), Spatial Correlation Score, Perkins Skill Score (PSS — area between PDFs).
- **Baselines:** Compared against raw model output, delta method, standard QM, and QDM.
- **Statistical significance:** Wilcoxon signed-rank test on paired daily errors (non-parametric, since precip distributions are skewed).

---

### Q4. What failed and what did you learn?

**Answer:** 
1. **K-means for regime clustering failed** — assumed spherical clusters in high-dimensional PDF space. Replaced with DBSCAN, which handles irregular cluster shapes and identifies noise points (ambiguous regime days).
2. **LOWESS smoothing over-smoothed the extreme tail** — applying LOWESS across the full range lost the sharp increase in the extreme tail. Fixed by applying piecewise LOWESS separately per regime, with tighter bandwidth in the extreme regime.
3. **Spatial consistency was not initially enforced** — correcting each gridpoint independently produced checkerboard artifacts. Added spatial regularization by interpolating quantile maps from neighboring gridpoints.
4. **The drizzle problem** — GCMs produce too many very light rain days. Our regime boundary at 1mm was too generous. Iterative calibration of regime boundaries using WFE metric improved this significantly.

---

### Q5. What would you change with more data / compute?

**Answer:**
- **More data:** Use ERA5 reanalysis as the "reference truth" instead of station-interpolated data. Station data has sparse coverage in mountainous regions; ERA5 provides consistent 30km gridded estimates.
- **More compute:** Replace statistical RAQM with a deep learning bias corrector — a U-Net trained on GCM→ERA5 paired data, which can capture non-stationary biases and spatial relationships simultaneously. Reference: DeepSD (Pan et al., 2021).
- **Uncertainty quantification:** Add ensemble-based correction to estimate correction uncertainty, not just point estimates. Important for climate risk assessment — decision-makers need confidence intervals on extreme event probability.
- **Transfer learning:** Fine-tune the regime classifier for different geographic regions (the rainfall regime definitions differ between tropical and temperate climates).

---

### Q6. How does this relate to ML concepts?

**Answer:**
- **Regime classification:** Unsupervised clustering (DBSCAN) on distribution features — this is a real-world application of clustering.
- **Quantile mapping:** Statistical function approximation — a non-parametric form of regression that maps one CDF to another.
- **Cross-validation design:** Temporal data requires time-series-aware splits — a real-world example of why data leakage must be considered carefully.
- **Domain shift / distribution mismatch:** The core problem — the model output distribution differs from the observed distribution. Our correction is essentially a domain adaptation approach using historical paired data.
- **Evaluation design:** Defining task-specific metrics (PSS, EVI, WFE) rather than generic MSE, because the downstream decision (flood risk assessment) cares about extremes, not averages.

---

## Rapid-Fire Defense Q&A

| Question | Answer |
|---|---|
| What is the training data period? | 1990–2020 (30 years of historical paired GCM+observation data) |
| What climate model (GCM) did you use? | [Specify your actual GCM, e.g., CMIP6 ensemble or regional model] |
| What is Perkins Skill Score? | Area between two PDFs: $PSS = \sum \min(z_o, z_m)$. Range [0,1]; 1 = identical distributions |
| Why not use a neural network directly? | Limited paired training data (~10,000 data points per gridpoint), high interpretability requirement for climate science applications |
| How does your method handle non-stationarity? | QDM blend preserves climate change signals; limitation is that the correction is calibrated on historical data and may not perfectly transfer to future climate states |
| What is the computational cost? | Training (historical period): ~2 minutes per gridpoint. Inference: <1 second per day per gridpoint. Fully parallelizable across gridpoints. |
""")

wc("15-mock-interviews/full-mock-1.md", r"""# Full Mock Interview — Session 1: ML Engineer (Entry Level)

**Duration:** 45 minutes  
**Format:** 15 min DSA + 20 min ML Theory + 10 min Project Defense

---

## Part 1: DSA (15 minutes)

### Problem: Two Sum (Warm-up)
**Interviewer:** "Given an array of integers and a target, return indices of two numbers that add to the target."

**Step 1 — Restate:** "Return any two indices `[i, j]` such that `nums[i] + nums[j] == target`, where `i != j`."

**Step 2 — Clarify:** 
- "Can I assume exactly one solution exists?" → Yes.
- "Can I use the same element twice?" → No.
- "Negative numbers?" → Yes.

**Step 3 — Brute Force:** Nested loops, $O(N^2)$ time, $O(1)$ space. "I'll mention this but not implement it."

**Step 4 — Insight:** "If I see `nums[i]`, I need `target - nums[i]`. I can store every number I've seen so far in a Hash Map mapping value → index."

**Step 5 — Optimized Approach:** Single pass. For each number, check if complement is in hash map. If yes, return. If no, add current number to map.

**Step 6 — Justification:** $O(N)$ time (one pass), $O(N)$ space (hash map).

**Step 7 — Code:**
```python
from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    seen = {}  # value -> index
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []
```

**Step 8 — Dry Run:** `nums=[2,7,11,15]`, `target=9`.
- i=0, n=2, complement=7. 7 not in seen. seen={2:0}.
- i=1, n=7, complement=2. 2 in seen! Return [0, 1]. ✓

**Step 9 — Edge Cases:** Empty array → return []. Single element → return []. Target = 2*num → ensure `i != j` (handled since we add AFTER check).

**Step 10 — Follow-ups:** 
- "What if the array is sorted?" → Use Two Pointers instead, $O(1)$ space.
- "What if multiple solutions?" → Collect all pairs.

---

### Problem: Valid Parentheses (Core DSA)
**Interviewer:** "Determine if a string of brackets is valid."

**Key Insight:** Stack. Open brackets push; close brackets must match the top. If stack is empty at end, valid.

```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in mapping:
            top = stack.pop() if stack else '#'
            if mapping[c] != top: return False
        else:
            stack.append(c)
    return len(stack) == 0
```

**Edge Cases:** Empty string (valid), only open brackets (invalid), mismatched types.

---

## Part 2: ML Theory (20 minutes)

### Q1: "Walk me through the forward pass of a Transformer block."

**Strong Answer:** "Input is a sequence of token embeddings $X \in \mathbb{R}^{N \times d}$. First, we apply Multi-Head Self-Attention: project $X$ to $Q$, $K$, $V$ via learned matrices. Compute $\text{softmax}(QK^T/\sqrt{d_k})V$ independently for each of $h$ heads, concatenate, project with $W_O$. Add the attention output to the original $X$ via a residual connection, then apply Layer Normalization. Second, pass through the Feed-Forward Network: two linear layers with GELU activation and 4x expansion. Add via residual + LayerNorm again. Output is another $\mathbb{R}^{N \times d}$ tensor with enriched contextual representations."

**Follow-up: "Why scale by $\sqrt{d_k}$?"**
"In high dimensions, dot products of random vectors have expected magnitude $\sqrt{d_k}$. Without scaling, softmax inputs are $O(\sqrt{d_k})$, pushing softmax into the saturation region where gradients are near zero. Dividing by $\sqrt{d_k}$ normalizes the scores to $O(1)$."

---

### Q2: "What's the difference between overfitting and distribution shift?"

**Strong Answer:** "Overfitting means the model memorizes training noise and fails on data from the same distribution. Distribution shift means train and test data come from different distributions entirely — the model can be well-fitted and still fail. Distribution shift types: covariate shift (input distribution $P(X)$ changes but $P(Y|X)$ stays same), label shift (class proportions change), concept drift (the relationship $P(Y|X)$ itself changes). In ML deployment, distribution shift is often the dominant failure mode — the real world differs from the training distribution in ways we didn't anticipate."

---

### Q3: "How would you decide between RAG and fine-tuning for a customer support chatbot?"

**Strong Answer:** "I'd analyze several dimensions: (1) Data freshness — if product info changes frequently, RAG avoids retraining cycles. (2) Data volume — fine-tuning needs ~100+ high-quality examples to be effective; RAG can work with a document corpus immediately. (3) Latency — RAG adds retrieval latency (50-200ms); fine-tuning has no additional inference cost. (4) Interpretability — RAG can show sources; fine-tuning is opaque. (5) Privacy — RAG keeps data outside model weights. For a customer support chatbot with a large, frequently-updated knowledge base: RAG first, fine-tune the response style with a small SFT dataset on top."

---

## Part 3: Project Defense (10 minutes)

### "Tell me about your NEXEN project."

**2-Minute Pitch:** "NEXEN is a rainfall bias correction system submitted to Smart India Hackathon 2024. Climate models systematically mispredict rainfall — for example, the ERA5 model may overestimate rainfall in mountainous regions and underestimate extremes during monsoon. Standard bias correction applies a uniform quantile mapping across all precipitation intensities, which works for typical days but fails on extreme events that are critical for flood risk assessment. We built a regime-aware correction system: first classify each day into Dry, Light, Moderate, or Extreme rainfall regimes using DBSCAN clustering on precipitation distribution features, then apply separate, calibrated quantile maps per regime. This improved the Extreme Value Index by 18% over standard quantile mapping when evaluated with Leave-One-Year-Out cross-validation."

**Follow-up: "Why DBSCAN over K-means for regime clustering?"**
"K-means assumes spherical clusters in feature space and requires specifying K upfront. Precipitation distribution features (PDFs over 0-200mm range) form non-spherical clusters — the dry regime is very compact (spike at 0), moderate is more spread, extreme has heavy tails. DBSCAN identifies arbitrarily-shaped clusters and, importantly, marks ambiguous days as noise, which we exclude from calibration rather than forcing them into incorrect regimes."

**Follow-up: "What would you do with 10x more compute?"**
"Replace the statistical RAQM with a convolutional neural network trained on GCM→observation pairs. The key advantage is capturing spatial correlations — standard QM corrects each grid point independently, creating spatial inconsistencies. A U-Net architecture would learn to correct while preserving spatial rainfall patterns. We'd need ERA5 as ground truth (30km coverage) instead of interpolated station data."
""")

wc("24-dsa-mock-interviews/dsa-mock-1.md", r"""# DSA Mock Interview — Session 1

**Time:** 45 minutes | **Difficulty:** Medium | **Topics:** Arrays, Trees, DP

---

## Problem 1: Maximum Subarray (20 min)

**Interviewer:** "Given an integer array, find the contiguous subarray with the largest sum."

### Step 1 — Restate
"Find contiguous subarray (at least one element) with maximum sum. Return the sum."

### Step 2 — Clarify
- "Can all elements be negative?" → Yes. Return the maximum single element.
- "Is an empty subarray allowed?" → No. At least one element.

### Step 3 — Brute Force
Try all subarrays: $O(N^2)$ or $O(N^3)$. Too slow.

### Step 4 — Insight (Kadane's Algorithm)
"At each position, I make a binary choice: extend the existing subarray or start fresh. If the existing sum is negative, it only hurts to carry it forward."

### Step 5 — Optimized Approach
Maintain `curr_sum` (sum of best subarray ending here) and `max_sum`. At each element: `curr_sum = max(num, curr_sum + num)`. Update `max_sum`.

### Step 6 — Justification
$O(N)$ time, $O(1)$ space. Single pass, one decision per element.

### Step 7 — Code
```python
from typing import List

def maxSubArray(nums: List[int]) -> int:
    max_sum = curr_sum = nums[0]  # Initialize with first element
    
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)  # Extend or restart
        max_sum = max(max_sum, curr_sum)
    
    return max_sum
```

### Step 8 — Dry Run
`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`
- num=-2: curr=-2, max=-2
- num=1: curr=max(-2+1,1)=1, max=1
- num=-3: curr=max(1-3,-3)=-2, max=1
- num=4: curr=max(-2+4,4)=4, max=4
- num=-1: curr=3, max=4
- num=2: curr=5, max=5
- num=1: curr=6, max=6 ✓

### Step 9 — Edge Cases
- All negative → returns least negative (correctly handled by Kadane's)
- Single element → returns that element

### Step 10 — Follow-ups
"Return the subarray itself?" → Track start/end indices: reset `start = i` when restarting, update end when `max_sum` is updated.
"Circular array?" → `max(Kadane(nums), total_sum - min_subarray_sum)`.

---

## Problem 2: Lowest Common Ancestor of a BST (15 min)

**Interviewer:** "Given a BST and two nodes p and q, find their LCA."

### Key Insight
"In a BST, if both p and q are less than the current node, the LCA is in the left subtree. If both are greater, it's in the right subtree. Otherwise, the current node is the LCA."

### Code
```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = self.right = None

def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left    # Both in left subtree
        elif p.val > root.val and q.val > root.val:
            root = root.right   # Both in right subtree
        else:
            return root         # Split point = LCA
    return None
```

**Complexity:** $O(H)$ time, $O(1)$ space. $H = \log N$ for balanced BST.

**Follow-up:** "General binary tree (not BST)?" → DFS returning LCA: if left and right both return non-None, current is LCA. $O(N)$ time.

---

## Problem 3: Coin Change (10 min)

**Interviewer:** "Given coin denominations and an amount, find minimum coins needed."

### Key Insight
"Optimal substructure: min coins for amount $a$ = 1 + min coins for $a - \text{coin}$, for each coin."

### Code
```python
def coinChange(coins: List[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins for amount 0
    
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Complexity:** $O(\text{amount} \times \text{coins})$ time, $O(\text{amount})$ space.

**Follow-up:** "Why is Greedy wrong?" → Coins [1, 3, 4], amount 6: Greedy picks 4→then two 1s (3 coins). DP finds 3+3 (2 coins). Greedy only works for canonical coin systems like USD.
""")

print("Batch F questions + project defense + mocks complete")
