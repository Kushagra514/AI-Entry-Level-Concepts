# Full Mock Interview — Session 1: ML Engineer (Entry Level)

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
