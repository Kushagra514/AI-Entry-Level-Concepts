# Top-K and Top-P (Nucleus) Sampling

## 1. Definition
Top-K and Top-P are truncation strategies used during text generation to restrict the vocabulary from which the model samples the next token, preventing the selection of highly unlikely (and often nonsensical) tokens.

## 2. Intuition
Imagine a model predicts the next word is: 
"apple" (80%), "banana" (15%), "cherry" (4%), and 30,000 other words (total 1%).
Without truncation, there's a 1% chance the model picks a bizarre word like "bulldozer," which derails the sentence. Top-K and Top-P act as bouncers, throwing out the 30,000 bad options before you roll the dice.

## 3. Why it exists
Language models have large vocabularies (30k-100k tokens). Even if the long tail of tokens has tiny individual probabilities, the *sum* of the tail can be significant. Sampling from the unmodified distribution occasionally selects a terrible token, causing a cascading failure in generation.

## 4. Mechanics
- **Top-K:** Sort the vocabulary by probability. Keep only the top $K$ tokens. Re-normalize their probabilities to sum to 1, and sample. (Fixed size).
- **Top-P (Nucleus Sampling):** Sort the vocabulary by probability. Compute the cumulative sum. Keep tokens until the cumulative sum exceeds $P$ (e.g., 0.9). Re-normalize and sample. (Dynamic size).

## 5. Complexity (Time & Space)
- **Time:** $O(V \log V)$ to sort the logits, though Top-K can be optimized to $O(V \log K)$ using a min-heap or QuickSelect.
- **Space:** $O(V)$ to store logits/probabilities.

## 6. Tiny worked example
Probs: `A: 0.5, B: 0.3, C: 0.15, D: 0.04, E: 0.01`
- **Top-K (K=2):** Keep A and B. Re-normalize: A = 0.5/0.8 = 62.5%, B = 0.3/0.8 = 37.5%.
- **Top-P (P=0.9):** Cumulative: A(0.5) -> B(0.8) -> C(0.95). 0.95 > 0.9, so stop. Keep A, B, C. Re-normalize among those three.

## 7. Code (Python)
```python
import torch

def top_p_sampling(logits, p=0.9):
    # Sort logits descending
    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
    cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
    
    # Identify tokens to remove (cumulative prob > p)
    # Shift by 1 to keep the token that crosses the threshold
    sorted_indices_to_remove = cumulative_probs > p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = 0
    
    # Scatter back to original indices and set to -infinity
    indices_to_remove = sorted_indices_to_remove.scatter(
        dim=-1, index=sorted_indices, src=sorted_indices_to_remove
    )
    logits[indices_to_remove] = float('-inf')
    return logits # Ready for softmax and sampling
```

## 8. Common mistakes
- Setting both Top-K and Top-P to very restrictive values simultaneously (e.g., K=5, P=0.5). Usually, you rely primarily on Top-P and leave K large (e.g., 50) as a fallback.
- Applying Top-P *before* Temperature. Temperature scales logits, which changes the probabilities, which changes which tokens make it into the Top-P nucleus. Always apply Temperature first.

## 9. 30-second interview answer
"Top-K and Top-P are sampling techniques that truncate the probability distribution to prevent generating nonsensical tokens. Top-K restricts sampling to the K most likely tokens. Top-P, or Nucleus Sampling, dynamically restricts sampling to the smallest set of tokens whose cumulative probability exceeds P. Top-P is generally preferred because it adapts to how confident the model is."

## 10. 2-minute interview answer
"To generate fluent text, we must manage the long tail of the vocabulary distribution. Top-K is a hard cutoff; if K=10, we only consider 10 tokens. The flaw with Top-K is that in flat distributions (model is unsure), 10 tokens isn't enough variety; in sharp distributions (model is confident), 10 tokens is too many and includes bad options. Top-P solves this dynamically. If $P=0.9$, and the top token has 95% probability, the nucleus contains only 1 token. If the top 50 tokens have 1% probability each, the nucleus expands to 90 tokens. This allows the model to be deterministic when confident and creative when uncertain. In practice, production systems apply Temperature first to shape the distribution, then Top-K (e.g., K=50) as a safety net, then Top-P (e.g., P=0.9) for the final dynamic truncation."

## 11. Follow-ups
- "Why does text degenerate without truncation?" (The long tail sums up. Even if $P(\text{gibberish}) = 10^{-5}$, across a 30,000 token vocabulary, the cumulative chance of picking *some* gibberish token becomes significant over a long generation).

## 12. Deeper questions
- "What is Min-P sampling?" (A newer alternative where you keep tokens whose probability is at least $P$ percent of the top token's probability. It handles dynamic ranges better than Top-P in some edge cases).

## 13. Related concepts
- **Temperature**: Applied before Top-K/P.
- **Beam Search**: Deterministic alternative to sampling.

## 14. When it breaks / Edge cases
- If $P$ is too close to 1.0, the tail is not truncated enough. If $P$ is too small (e.g., 0.1), it degenerates into greedy decoding.

## 15. Comparison with alternative approaches
- **Top-K vs Top-P:** Top-P is strictly superior because it dynamically adjusts the candidate pool size based on the model's confidence.

---
*Where this shows up in ML:*
OpenAI API parameters, HuggingFace `generate()` method.
