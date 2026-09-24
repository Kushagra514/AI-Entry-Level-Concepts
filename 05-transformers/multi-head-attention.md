# Multi-Head Attention

## 1. Definition
Multi-Head Attention (MHA) is the process of running multiple Self-Attention mechanisms (heads) in parallel within the same Transformer layer, then concatenating their outputs.

## 2. Intuition
Imagine analyzing a painting. If you only have one "head," you might focus entirely on the colors. By having multiple "heads," Head 1 focuses on colors, Head 2 analyzes the brush strokes, Head 3 identifies the objects, and Head 4 infers the historical context. They all look at the same painting simultaneously but extract different representations.

## 3. Why it exists
A single attention mechanism might average out complex relationships, forcing a token to pick one primary thing to attend to. MHA allows the model to jointly attend to information from different representation subspaces at different positions. (e.g., one head tracks grammar, another tracks pronoun references).

## 4. Mechanics
1. Instead of projecting the input embedding $X$ (size $d_{model}$) into one massive Q, K, and V, we project it into $H$ smaller sets of Q, K, V, each of size $d_{head} = d_{model} / H$.
2. Run standard Scaled Dot-Product Attention on all $H$ heads in parallel.
3. Concatenate the $H$ output matrices back together (resulting back in $d_{model}$ size).
4. Apply a final linear projection ($W_O$) to mix the information.

## 5. Complexity (Time & Space)
- **Time Complexity:** Same as single-head attention: $O(N^2 	imes d_{model})$. Splitting the dimension size divides the work by $H$, but doing it $H$ times balances it out perfectly.
- **Space Complexity:** $O(N^2 	imes H)$ to store the attention maps for all heads (though often optimized).

## 6. Tiny worked example
Model dim = 512, Heads = 8.
- Each head gets a subspace of $512 / 8 = 64$ dimensions.
- Head 1 does attention on 64 dims. Head 8 does attention on 64 dims.
- Outputs are $8 	imes 64 = 512$ dims concatenated.
- Projected through a $512 	imes 512$ matrix.

## 7. Code (Python, with type hints)
```python
import torch
import torch.nn as nn

# Conceptual block of MHA
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Fused projection for efficiency
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        
    def forward(self, x):
        batch, seq_len, d_model = x.size()
        
        # Project and reshape: (B, S, 3 * d_model) -> (B, S, 3, H, d_k)
        qkv = self.qkv(x).view(batch, seq_len, 3, self.num_heads, self.d_k)
        
        # Split into Q, K, V
        q, k, v = qkv[:, :, 0], qkv[:, :, 1], qkv[:, :, 2]
        
        # (Self-attention logic here on multiple heads...)
        # Concatenate and project
        # out = self.out_proj(concatenated_heads)
```

## 8. Common mistakes
- Thinking MHA increases the parameter count compared to single-head attention. It doesn't; the projection matrices are just sliced into smaller pieces ($H 	imes d_k = d_{model}$).
- Not realizing that the multiple heads are processed concurrently in a single massive tensor operation, not a python `for` loop.

## 9. 30-second interview answer
"Multi-Head Attention runs multiple independent self-attention mechanisms in parallel. By splitting the embedding dimension into smaller subspaces, the model can simultaneously attend to different semantic and syntactic relationships (like grammar vs. subject matter) without increasing overall computational complexity."

## 10. 2-minute interview answer
"Multi-Head Attention is what gives the Transformer its expressive power. If we used a single attention head, a token's updated representation would be a blunt weighted average of its neighbors, potentially losing distinct linguistic features. By projecting the Queries, Keys, and Values into $H$ lower-dimensional subspaces and computing attention independently, the model can track multiple distinct relationships. For instance, in 'The cat sat on its mat', one head might focus heavily on 'its' mapping to 'cat' for coreference resolution, while another head maps 'sat' to 'mat' for spatial tracking. These independent insights are then concatenated and linearly projected back to the original dimension. Elegantly, because $d_{head} = d_{model} / H$, the parameter count and FLOPs are virtually identical to a single massive attention head."

## 11. Follow-ups
- "What happens if you use too many heads?" (The dimensionality of each head $d_k$ becomes too small to capture meaningful vector relationships).

## 12. Deeper questions
- "Do we actually need all these heads?" (Research like 'Are Sixteen Heads Really Better than One?' shows that at inference time, many heads can be pruned away without performance loss, as they often learn redundant patterns).

## 13. Related concepts
- **Grouped Query Attention (GQA)**: A modern variant used in Llama 2/3 that reduces the number of K and V heads to save memory, while keeping multiple Q heads.

## 14. When it breaks / Edge cases
- MHA creates significant memory pressure during autoregressive decoding because you must cache the K and V matrices for *every* head across the sequence length (the KV-cache problem).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The primary workhorse layer in all Transformer models.
