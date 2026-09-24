# Transformer Key Equations

## 1. Definition
A consolidated reference of the core mathematical formulas underlying the Transformer architecture, suitable for interview derivation and exam-style questions.

## 2. Intuition
These equations are not abstract — each one is a computational step you can trace through the architecture. Understanding each equation operationally (what goes in, what comes out, why it's this form) is essential for deep interviews.

## 3. Why it exists
Interviewers often ask "derive the attention formula" or "what is the softmax over?". Having these formulas memorized and internalized avoids black-box answers.

## 4. Mechanics

### Token Embedding
$x_i = \text{Embedding}(t_i) + \text{PE}(i) \in \mathbb{R}^d$

### Sinusoidal Positional Encoding
$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right)$, $PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)$

### QKV Projections
$Q = XW_Q,\quad K = XW_K,\quad V = XW_V \quad (W_Q, W_K, W_V \in \mathbb{R}^{d \times d_k})$

### Scaled Dot-Product Attention
$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

- Scaling by $\sqrt{d_k}$ prevents softmax saturation.
- Output shape: $(N, d_v)$ where $N$ is sequence length.

### Multi-Head Attention
$$\text{MHA}(Q,K,V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W_O$$
$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$
where $d_k = d_v = d_{model}/h$.

### Causal Mask (Decoder)
Replace $QK^T/\sqrt{d_k}$ with $QK^T/\sqrt{d_k} + M$ where $M_{ij} = 0$ if $i \geq j$ else $-\infty$.

### Feed-Forward Network
$$\text{FFN}(x) = \text{GELU}(xW_1 + b_1)W_2 + b_2$$
$W_1 \in \mathbb{R}^{d \times 4d}$, $W_2 \in \mathbb{R}^{4d \times d}$.

### Layer Normalization
$$\text{LayerNorm}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \cdot \gamma + \beta$$

### Pre-LN Residual Wrapper
$$x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$$

### Softmax
$$\text{softmax}(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$$
Numerically stable: subtract $\max(z)$ before exponentiating.

### Cross-Entropy Loss (Language Model)
$$\mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T} \log P_\theta(x_t | x_{<t})$$

### Perplexity
$$\text{PPL} = \exp\!\left(\mathcal{L}\right) = \exp\!\left(-\frac{1}{T}\sum_t \log P_\theta(x_t|x_{<t})\right)$$
Lower is better. PPL = 10 means the model is as uncertain as uniformly over 10 choices at each step.

## 5. Complexity (Time & Space)
| Component | Time per layer | Parameters |
|---|---|---|
| Attention | $O(N^2 d)$ | $4d^2$ (Q,K,V,O projections) |
| FFN | $O(N d^2)$ | $8d^2$ |
| LayerNorm | $O(Nd)$ | $2d$ |
| Total per layer | $O(N^2 d + Nd^2)$ | $12d^2$ |

## 6. Tiny worked example
$d_k = 64$. Dot product of Q and K vectors of magnitude ~1: expected magnitude $\approx \sqrt{64} = 8$. Without scaling, softmax saturates. With $\sqrt{d_k}=8$ scaling, scores are $O(1)$ — gradients stay healthy.

## 7. Code (Python)
```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    attn = F.softmax(scores, dim=-1)
    return attn @ V, attn
```

## 8. Common mistakes
- Dividing by $d_k$ instead of $\sqrt{d_k}$ — a common slip in interviews.
- Applying softmax over the wrong dimension (should be the key dimension, `dim=-1` over sequence positions).

## 9. 30-second interview answer
"The core Transformer equation is $\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$. The scaling by $\sqrt{d_k}$ prevents softmax saturation from large dot products. Multi-head attention applies this independently in $h$ subspaces and concatenates. Every sub-layer is wrapped in $x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$."

## 10. 2-minute interview answer
"Walking through the Transformer equations: input tokens become embeddings plus sinusoidal positional encodings. These pass through $L$ identical encoder blocks. Each block first applies Multi-Head Attention: input is linearly projected into $h$ sets of Q, K, V matrices, scaled dot-product attention is computed in each head's subspace, and the outputs are concatenated and projected through $W_O$. A residual connection adds the pre-attention input back, and LayerNorm stabilizes the scale. The FFN then applies two linear layers with GELU, again wrapped in residual + LayerNorm. The final output of the last encoder layer represents each token as a contextual, high-dimensional vector."

## 11. Follow-ups
- "What does perplexity measure and what is a good value?" (PPL measures how surprised the model is by each next token on average. GPT-3 achieves ~20 on Penn Treebank. A PPL of 1 means perfect prediction; PPL = vocabulary size means random guessing).

## 12. Deeper questions
- "Why is the attention score matrix's diagonal dominant?" (Tokens often find themselves most relevant — especially early in training before the model learns richer dependencies. This is known as the 'attention sink' phenomenon, exploited by StreamingLLM).

## 13. Related concepts
- **All Transformer files**: These equations underpin every component.

## 14. When it breaks / Edge cases
- Numerical instability in softmax with very large logits. Always subtract `max(scores)` before `exp`.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:*
Every interview question about how Transformers work. Derivable directly from the architecture.
