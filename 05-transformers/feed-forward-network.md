# Feed-Forward Network (FFN) in Transformers

## 1. Definition
The Feed-Forward Network (FFN) in a Transformer block is a two-layer MLP applied independently to each token position, expanding and then projecting back: $\text{FFN}(x) = \text{GELU}(xW_1 + b_1)W_2 + b_2$.

## 2. Intuition
The Attention layer is like a social mixer — every token gathers information from others. The FFN is like a private thinking room — each token then processes what it gathered independently, reasoning about it with full MLP capacity. No communication between positions happens in the FFN.

## 3. Why it exists
Self-Attention is powerful at routing information but is linear in the embedding dimension (it's just weighted summation of Values). The FFN provides the non-linear, high-capacity computation that actually stores and transforms facts — much of the model's "knowledge" lives in FFN weights.

## 4. Mechanics
- **Architecture:** Linear(d, 4d) → GELU/ReLU → Linear(4d, d).
- **Expansion factor 4x:** Empirically chosen in the original paper; modern models often use 8x/3x for GLU variants.
- **Position-wise:** The same FFN weights are applied to every token independently. No weight sharing across the sequence.
- **GLU variants (SwiGLU, GeGLU):** Replace the simple GELU with a gated mechanism: $\text{FFN}(x) = (\sigma(xW) \odot xV)W'$. Used in Llama, PaLM — provides better performance.

## 5. Complexity (Time & Space)
- **Time:** $O(N \cdot d \cdot 4d) = O(Nd^2)$ per layer. FFN dominates over attention for large $d$ relative to $N$.
- **Parameters:** $2 \times d \times 4d = 8d^2$. Constitutes ~2/3 of total Transformer parameters.

## 6. Tiny worked example
$d=4$, Token embedding $x=[1, 0, -1, 0.5]$.
Layer 1 (Linear → 16): $W_1 \in \mathbb{R}^{4\times16}$, output $h \in \mathbb{R}^{16}$.
GELU(h): element-wise nonlinearity.
Layer 2 (Linear → 4): $W_2 \in \mathbb{R}^{16\times4}$, output $y \in \mathbb{R}^4$.
$y$ is the refined token embedding, injected back via residual.

## 7. Code (Python)
```python
import torch.nn as nn

class TransformerFFN(nn.Module):
    def __init__(self, d_model: int, expansion: int = 4, dropout: float = 0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, expansion * d_model),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(expansion * d_model, d_model),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        return self.net(x)
```

## 8. Common mistakes
- Thinking that FFN layers communicate across tokens. They don't — they are strictly position-wise. All cross-token communication happens in Attention.
- Ignoring that the FFN holds the majority of parameters: For GPT-3 with $d=12288$, each FFN has $8 \times 12288^2 \approx 1.2B$ parameters. Across 96 layers, FFN alone is ~115B of the ~175B total.

## 9. 30-second interview answer
"The FFN in a Transformer applies a 2-layer MLP independently to each token's embedding: expand 4x with GELU, project back. It provides non-linear, per-token computation after Attention's cross-token communication. FFN parameters constitute ~2/3 of total model parameters and are where factual knowledge is believed to be stored."

## 10. 2-minute interview answer
"The FFN sub-layer is often underestimated relative to Attention. Research has shown that the FFN acts as key-value memory: the first linear layer produces 'keys' that match input patterns, the activation function gates relevant memories, and the second linear layer outputs 'values' corresponding to those memories. Factual recall tasks correlate strongly with FFN weight patterns. The choice of activation matters: GELU outperforms ReLU empirically, and modern architectures use SwiGLU (Llama, PaLM) — a Swish-gated linear unit — which multiplies two parallel linear paths element-wise before the final projection. The 4x expansion factor is a hyperparameter; smaller models sometimes use 2.66x with SwiGLU to maintain parameter parity. MoE (Mixture of Experts) models replace the dense FFN with a sparse routing over multiple expert FFNs, routing each token to its top-K FFN experts."

## 11. Follow-ups
- "What is Mixture of Experts (MoE)?" (Replace the FFN with $E$ expert FFNs and a learned router that sends each token to its top-$k$ experts ($k$ typically 2). Only $k$ experts activate per token, reducing FLOPs while maintaining parameters — enabling scale without proportional compute cost. Used in Mixtral, GPT-4 (reported)).

## 12. Deeper questions
- "How does the FFN expand-then-contract architecture relate to bottleneck layers in ResNets?" (The 4x expansion creates a higher-dimensional latent space for the token to reason in, then projects back. The bottleneck (contracting) forces the model to extract the most useful transformation).

## 13. Related concepts
- **MoE (Mixture of Experts)**: Sparse FFN variant for scaling.
- **SwiGLU**: Gated FFN variant in modern LLMs.

## 14. When it breaks / Edge cases
- Very small expansion factors (1x) severely limit model capacity; the FFN becomes a simple linear layer.

## 15. Comparison with alternative approaches
- **vs Attention:** Attention routes information between positions; FFN processes information within each position. Together they are complementary — neither alone is sufficient.

---
*Where this shows up in ML:*
Every Transformer block: Attention handles communication, FFN handles computation. The FFN parameters in GPT-2 are the focus of many interpretability studies.
