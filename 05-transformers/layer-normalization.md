# Layer Normalization

## 1. Definition
Layer Normalization normalizes the activations within a single sample across the feature dimension, computing mean and variance per-sample rather than per-batch.

## 2. Intuition
Imagine everyone on a team speaks different languages with wildly different volumes. You apply noise-cancelling headphones (normalization) to each person individually, bringing everyone to the same volume level. Unlike Batch Norm, which adjusts all people in the room at once, Layer Norm adjusts each person independently.

## 3. Why it exists
Batch Normalization (normalizing across the batch) works poorly for variable-length sequences in NLP: batch statistics become meaningless when sequence lengths vary, and small batches on GPU produce noisy estimates. Layer Normalization normalizes per-sample, making it batch-size independent and suitable for Transformers and RNNs.

## 4. Mechanics
Given input $x \in \mathbb{R}^d$:
1. Compute mean: $\mu = \frac{1}{d}\sum_{i=1}^d x_i$.
2. Compute variance: $\sigma^2 = \frac{1}{d}\sum_{i=1}^d (x_i - \mu)^2$.
3. Normalize: $\hat{x}_i = (x_i - \mu)/\sqrt{\sigma^2 + \epsilon}$.
4. Scale & shift: $y_i = \gamma \hat{x}_i + \beta$ where $\gamma, \beta$ are learnable parameters.

Applied in Transformers as **Pre-LN** (before sub-layer) for stability:
$x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$.

## 5. Complexity (Time & Space)
- **Time:** $O(d)$ per token — two passes over the feature vector.
- **Space:** $O(d)$ for $\gamma$ and $\beta$ parameters; $O(1)$ auxiliary per-sample.

## 6. Tiny worked example
$x = [3, 5, 7]$. $d=3$.
$\mu = 5$. $\sigma^2 = \frac{(3-5)^2+(5-5)^2+(7-5)^2}{3} = \frac{8}{3} \approx 2.67$.
$\hat{x} = [-1.22, 0, 1.22]$.
With $\gamma=1$, $\beta=0$: $y = [-1.22, 0, 1.22]$.

## 7. Code (Python)
```python
import torch
import torch.nn as nn

# PyTorch's built-in LayerNorm
layer_norm = nn.LayerNorm(normalized_shape=512)  # Normalizes last 512 dims

# Manual implementation
def layer_norm_manual(x, gamma, beta, eps=1e-5):
    mu = x.mean(dim=-1, keepdim=True)
    sigma = x.var(dim=-1, keepdim=True, unbiased=False)
    x_hat = (x - mu) / (sigma + eps).sqrt()
    return gamma * x_hat + beta
```

## 8. Common mistakes
- Confusing Layer Norm (normalize across features for one sample) with Batch Norm (normalize across batch for one feature). In NLP: LayerNorm is almost always used; BatchNorm is rare because sequence lengths vary.
- Not using learnable $\gamma$ and $\beta$ (scale and shift). Without them, the normalization is too restrictive — it cannot learn to scale activations back up if needed.

## 9. 30-second interview answer
"Layer Normalization normalizes activations within each token's feature vector independently, computing per-sample statistics. Unlike Batch Norm (which fails on variable-length NLP sequences), LayerNorm is batch-size invariant and is used in every Transformer architecture alongside residual connections to stabilize training."

## 10. 2-minute interview answer
"Layer Normalization is critical for training deep Transformers. When activations grow large or small across layers, gradients either explode or vanish. LayerNorm constrains the magnitude of each token's embedding to have unit variance, making the activation landscape smooth and the gradients well-behaved. The learnable $\gamma$ and $\beta$ parameters allow the model to rescale the normalized activations appropriately for each layer. The placement matters: Post-LN (original Transformer) places LayerNorm after the residual, which works but requires very careful learning rate warmup. Pre-LN (modern standard, used in GPT-2+, Llama) places LayerNorm before each sub-layer, providing more stable training and often better final performance without warmup constraints. RMSNorm (used in Llama) further simplifies LayerNorm by only computing the RMS (no mean centering), reducing compute by ~30% with negligible accuracy impact."

## 11. Follow-ups
- "What is RMSNorm and why is it used in Llama?" (Simplified LayerNorm that skips mean subtraction. Only normalizes by RMS $\sqrt{(1/d)\sum x_i^2}$. Faster and empirically performs as well as full LayerNorm).

## 12. Deeper questions
- "How does LayerNorm interact with residual connections?" (Pre-LN: $x \leftarrow x + F(\text{LayerNorm}(x))$. The residual path carries unnormalized activations, while the learning path sees normalized input. This allows each layer's contribution to be well-conditioned while the residual stream can grow).

## 13. Related concepts
- **Batch Normalization**: The counterpart for vision models and CNNs.
- **Residual Connections**: Always paired with LayerNorm in Transformers.

## 14. When it breaks / Edge cases
- Very small feature dimensions (d=1 or d=2) make variance estimation noisy. LayerNorm assumes enough dimensions for stable statistics.

## 15. Comparison with alternative approaches
- **vs Batch Norm:** BatchNorm normalizes across the batch — dependent on batch size and sequence length. LayerNorm is batch-independent — normalizes across features — perfect for variable-length sequences.

---
*Where this shows up in ML:*
Every Transformer block: `x = x + Attention(LayerNorm(x))`, then `x = x + FFN(LayerNorm(x))`.
