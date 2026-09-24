# Query, Key, Value (QKV)

## 1. Definition
Query, Key, and Value (QKV) are three distinct vectors generated for every token in a Transformer layer via learned linear projections. They form the basis of the Self-Attention mechanism, where Queries search for Keys, and matching pairs aggregate their corresponding Values.

## 2. Intuition
Think of searching a database or a library. 
- **Query (Q):** What you type into the search bar ("Action movies").
- **Key (K):** The metadata/tags on the items ("Genre: Action", "Genre: Romance").
- **Value (V):** The actual content of the item you retrieve.
Attention compares your Query to all Keys. Where they match strongly, you extract a large portion of that Value.

## 3. Why It Exists
If we computed the dot product of raw word embeddings to find token similarity, the relationship would be perfectly symmetric (Dot(A,B) = Dot(B,A)). Furthermore, a token's identity would be conflated with its role in a sentence. By generating three distinct projections ($W_Q, W_K, W_V$), the model learns asymmetrical relationships. The word "it" (Query) might seek out nouns (Keys), while the noun outputs its grammatical features (Values).

## 4. Core Mechanics
1. We have three learned weight matrices: $W_Q, W_K, W_V$.
2. The input embedding sequence $X$ is multiplied by these matrices to produce:
   - $Q = X W_Q$
   - $K = X W_K$
   - $V = X W_V$
3. These representations are fed into the scaled dot-product attention formula: $\text{Attention}(Q, K, V) = \text{softmax}(QK^T / \sqrt{d_k}) V$.

## 5. Mathematical View
Let $X \in \mathbb{R}^{N \times d_{\text{model}}}$.
$W_Q \in \mathbb{R}^{d_{\text{model}} \times d_k}$
$W_K \in \mathbb{R}^{d_{\text{model}} \times d_k}$
$W_V \in \mathbb{R}^{d_{\text{model}} \times d_v}$

$$ Q = X W_Q \quad K = X W_K \quad V = X W_V $$

## 6. Shape / Dimension Tracking
Assume Batch size $B$, Sequence length $N$, Model dimension $d_{\text{model}}$, and Head dimensions $d_k, d_v$.
```text
X: (B, N, d_model)
W_Q: (d_model, d_k)
W_K: (d_model, d_k)
W_V: (d_model, d_v)

Q = X @ W_Q -> (B, N, d_k)
K = X @ W_K -> (B, N, d_k)
V = X @ W_V -> (B, N, d_v)
```
*(Note: In Multi-Head Attention, $d_k$ is usually $d_{\text{model}} / \text{num\_heads}$, and the matrices are partitioned across heads).*

## 7. Tiny Worked Example
Input embedding $X$ for "He".
$W_Q, W_K, W_V$ are learned matrices.
"He" generates $Q_{\text{he}}$ (encoding: "I am looking for a verb").
"Ran" generates $K_{\text{ran}}$ (encoding: "I am a verb").
$Q_{\text{he}} \cdot K_{\text{ran}}$ yields a high dot product score.
"He" pulls in $V_{\text{ran}}$ to update its meaning.

## 8. Minimal Implementation
```python
import torch
import torch.nn as nn

class QKVProjection(nn.Module):
    def __init__(self, embed_dim: int, head_dim: int):
        super().__init__()
        # In practice, usually fused into one linear layer for speed:
        # self.qkv_proj = nn.Linear(embed_dim, 3 * head_dim)
        
        self.q_proj = nn.Linear(embed_dim, head_dim, bias=False)
        self.k_proj = nn.Linear(embed_dim, head_dim, bias=False)
        self.v_proj = nn.Linear(embed_dim, head_dim, bias=False)
        
    def forward(self, x: torch.Tensor):
        # x shape: (B, N, embed_dim)
        Q = self.q_proj(x) # (B, N, head_dim)
        K = self.k_proj(x) # (B, N, head_dim)
        V = self.v_proj(x) # (B, N, head_dim)
        return Q, K, V
```

## 9. Common Misconceptions
- **"Q, K, and V must have the same dimension as the input."** In Multi-Head Attention, they are typically projected down to $d_{\text{model}} / \text{num\_heads}$.
- **"Q and K must have the same dimension as V."** Q and K must have the same dimension ($d_k$) to perform the dot product, but V can technically be any dimension ($d_v$), though they are usually kept the same in standard Transformers.

## 10. 30-Second Interview Answer
"QKV is the abstraction used in Self-Attention, inspired by database retrieval. Input tokens are projected via learned weights into Queries (what the token is looking for), Keys (what the token contains), and Values (the semantic payload). The dot product of Queries and Keys determines the attention weights applied to aggregate the Values."

## 11. 2-Minute Interview Answer
"The QKV mechanism is how Transformers achieve asymmetric, dynamic routing of information. If we used raw embeddings to compute attention, the relationship between token A and token B would be perfectly symmetric. By applying three separate learned linear transformations—$W_Q$, $W_K$, and $W_V$—the model learns specialized roles. A token's Query vector encodes what context it needs. Its Key vector encodes what context it offers. The dot product $Q K^T$ yields the relevance score. Finally, the Value vector contains the semantic payload that gets aggregated and passed to the next layer. In modern implementations, these three projections are fused into a single dense matrix multiplication for maximum GPU efficiency."

## 12. Follow-Up Questions
- **"What happens in Cross-Attention (e.g., Encoder-Decoder models)?"** 
  The Queries come from the Decoder's current sequence, but the Keys and Values are projected from the Encoder's final output sequence. This allows the decoder to "search" the encoded input.
- **"What are the complexities of this projection?"**
  $O(N \cdot d_{\text{model}} \cdot d_k)$ time complexity per sequence. Space complexity is $O(d_{\text{model}} \cdot d_k)$ to store the weights.

## 13. Deeper Questions
- **"What is Multi-Query Attention (MQA) or Grouped-Query Attention (GQA)?"** 
  To save memory during LLM inference, MQA shares a single K and V head across all Q heads. GQA shares K and V heads across groups of Q heads. This drastically reduces the size of the KV-cache.

## 14. Failure Modes / Edge Cases
- **Autoregressive Memory Constraints:** During text generation, the K and V matrices of past tokens must be kept in GPU memory (the KV Cache) to avoid recomputing them. This cache grows linearly with sequence length and batch size, often becoming the primary bottleneck that limits context windows.

## 15. Comparison
- **QKV vs. Raw Dot Product:** Raw dot product is symmetric and inflexible. QKV allows $A \to B$ to have high attention while $B \to A$ has low attention.

## 16. What To Remember
- Q, K, V are derived from the *same* input $X$ in self-attention via distinct linear layers.
- Q and K must have the same dimension to dot-product.
- Modern implementations fuse the three linear layers into one.

## 17. Interview Trap
> **Q:** "Does the Transformer use the original input embedding matrix as the Value?"
> **A:** No. The Value is a learned linear projection of the input embedding ($V = X W_V$). The attention weights are applied to this Value projection, not the raw input.

---
*Connected Concepts:* [Self-Attention](self-attention.md), [Multi-Head Attention](multi-head-attention.md), [Transformers](transformer-overview.md)
