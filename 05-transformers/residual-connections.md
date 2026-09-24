# Residual Connections (Skip Connections)

## 1. Definition
A Residual Connection (Skip Connection) adds the input of a layer directly to its output: $\text{output} = F(x) + x$, allowing gradients to flow directly through identity paths during backpropagation.

## 2. Intuition
Imagine teaching a student by asking them to learn only the "delta" — the correction to their current answer, not the entire answer from scratch. Instead of learning $y = F(x)$, the layer learns $\text{residual} = F(x) - x$, which is typically a small correction. This is easier to learn and far easier to train with gradient descent.

## 3. Why it exists
Deep networks (20+ layers) fail to train without residual connections due to the **Vanishing Gradient Problem**. Gradients in the backward pass are products of layer-local derivatives. Even tiny values (0.9) multiplied 100 times become $0.9^{100} \approx 0.00003$, essentially zero. Residual connections create gradient highways that bypass this.

## 4. Mechanics
- **Forward Pass:** $y = F(x, W) + x$ (or with projection $W_s x$ if dimensions differ).
- **Backward Pass:** $\partial L/\partial x = \partial L/\partial y \cdot (F'(x) + I)$. The identity term $I$ ensures gradient flows even if $F'(x) \to 0$.
- In Transformers, every sub-layer (Attention and FFN) has a residual connection: $x \leftarrow x + \text{Attention}(x)$, then $x \leftarrow x + \text{FFN}(x)$.
- **Pre-LN vs Post-LN:** Whether LayerNorm is applied before or after the sub-layer. Modern LLMs use Pre-LN for training stability.

## 5. Complexity (Time & Space)
- **Time:** $O(d)$ per token — just an elementwise addition.
- **Space:** $O(d)$ to keep the residual (input) in memory alongside the layer output.

## 6. Tiny worked example
Without residual: If $F(x)$ has gradient $0.01$ and there are 100 layers: $0.01^{100} \approx 10^{-200}$. Effectively zero. No learning.

With residual: Gradient becomes $0.01 + 1 = 1.01$ through the identity path. $1.01^{100} \approx 2.7$. The gradient is preserved.

## 7. Code (Python)
```python
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, d_model: int):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model)
        )

    def forward(self, x):
        # Pre-LN residual (modern convention)
        return x + self.ff(self.norm(x))
```

## 8. Common mistakes
- Applying residual connections only to some layers and not others, creating bottlenecks.
- Using residual connections when input and output dimensions differ without projecting the residual ($W_s x$) to match dimensions.

## 9. 30-second interview answer
"Residual connections add the input to the layer output: $y = F(x) + x$. They solve the Vanishing Gradient Problem by providing gradient highways through identity paths, enabling training of very deep networks (100+ layers). Every Transformer sub-layer wraps a residual connection around Attention and FFN."

## 10. 2-minute interview answer
"ResNets introduced residual connections in 2015, enabling 152-layer networks where 20-layer plain networks failed. The core insight is reformulating what the layer learns: instead of learning a complete transformation $H(x)$, the layer learns only the residual $F(x) = H(x) - x$, which is small and easy to train. During backpropagation, the identity term in $\partial L/\partial x = \partial L/\partial y \cdot (F'(x)+I)$ ensures a gradient pathway even when the learned transformation's gradient vanishes. In Transformers, residual connections are combined with Layer Normalization in a 'sublayer wrapper': $x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$ (Pre-LN), which provides both gradient flow and activation scale stability. The residual stream in Transformers has been deeply studied — the residual stream can be understood as a communication bus between layers, each layer reading from and writing to this shared state."

## 11. Follow-ups
- "What is the 'residual stream' perspective of Transformers?" (Each attention head and FFN layer reads from the residual stream and adds a vector to it. The stream accumulates information across all layers as an additive process).

## 12. Deeper questions
- "Why are deeper Transformers better? Isn't the residual connection effectively making early layers optional?" (Each additional layer has the *opportunity* to refine the representation. With residual connections, the network can choose to 'skip' a layer by learning near-zero weights in $F(x)$).

## 13. Related concepts
- **Layer Normalization**: Almost always paired with residual connections in Transformers.
- **Highway Networks**: A gated predecessor to ResNets with learned skip weights.

## 14. When it breaks / Edge cases
- Post-LN (original Transformer paper) can be unstable without careful learning rate warmup. Pre-LN is now standard.

## 15. Comparison with alternative approaches
- **vs Dense/DenseNet connections:** DenseNet connects every layer to every subsequent layer ($O(N^2)$ connections). ResNets use simple skip-one connections. Transformers use residual-to-every-layer because the architecture is sequential.

---
*Where this shows up in ML:*
Every modern deep learning architecture: ResNets (vision), Transformers (NLP), U-Nets (segmentation). Without residual connections, models beyond ~20 layers cannot be trained effectively.
