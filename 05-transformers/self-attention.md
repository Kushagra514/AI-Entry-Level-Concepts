# Self-Attention

## 1. Definition
Self-Attention is a sequence-to-sequence operation where each token computes a new representation for itself by taking a weighted sum of the representations of all other tokens in the same sequence. The weights are determined dynamically by the compatibility between the tokens.

## 2. Intuition
Imagine a group of specialists trying to decipher a cryptic sentence. Each specialist holds one word. To understand their own word, they ask questions (Queries) to the group. The other specialists hold descriptions of what they can offer (Keys). When a Query matches a Key, the specialist offering the Key passes their actual information (Value) to the asker. The asker mixes all the received information to form a complete understanding of their word in context.

## 3. Why It Exists
Static embeddings (like Word2Vec) map the word "bank" to a single vector, meaning "river bank" and "bank account" have the exact same representation. RNNs process context sequentially, suffering from information bottleneck and vanishing gradients over long distances. Self-attention was created to allow *direct, parallel interaction* between any two tokens in a sequence, creating highly contextual embeddings without sequential bottlenecks.

## 4. Core Mechanics
1. **Projections:** Project the input sequence into three sets of vectors: Queries (Q), Keys (K), and Values (V) using learned weight matrices.
2. **Scores:** Compute the dot product between every Q and every K. This results in an $N \times N$ matrix indicating how much attention every token should pay to every other token.
3. **Scaling:** Divide the scores by $\sqrt{d_k}$ (where $d_k$ is the dimension of the keys). This prevents the dot products from growing too large and pushing the Softmax function into regions with near-zero gradients.
4. **Softmax:** Apply Softmax along the Key dimension so that the weights for each Query sum to 1.
5. **Output:** Multiply the resulting attention matrix by the V vectors.

## 5. Mathematical View
For packed matrices $Q, K, V$:

$$ \text{Attention}(Q, K, V) = \text{softmax}\left( \frac{Q K^T}{\sqrt{d_k}} \right) V $$

## 6. Shape / Dimension Tracking
Assume Batch size $B$, Sequence length $N$, and Head dimension $d_k$ (for $Q, K$) and $d_v$ (for $V$).
```text
Q: (B, N, d_k)
K: (B, N, d_k)
V: (B, N, d_v)

1. Q @ K^T
   (B, N, d_k) @ (B, d_k, N)  -> (B, N, N)
   (This is the unnormalized attention score matrix)

2. Scale and Softmax
   Softmax( (B, N, N) / sqrt(d_k) ) -> (B, N, N)
   (These are the attention weights)

3. Weights @ V
   (B, N, N) @ (B, N, d_v) -> (B, N, d_v)
   (This is the final contextualized output)
```

## 7. Tiny Worked Example
Sequence: `["apple", "is", "tasty"]` (Length 3).
The Q vector for "apple" dot-products with the K vectors of all three words.
Unscaled scores: `[10, 2, 8]`.
Let's assume $d_k = 1$, so scaling by $\sqrt{1} = 1$.
Softmax(`[10, 2, 8]`) $\approx$ `[0.88, 0.00, 0.12]`.
The new representation for "apple" is:
$0.88 \times V_{\text{apple}} + 0.00 \times V_{\text{is}} + 0.12 \times V_{\text{tasty}}$.
The vector for "apple" now mathematically contains a strong hint of "tasty".

## 8. Minimal Implementation
```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
    # Q, K shape: (B, N, d_k)
    # V shape: (B, N, d_v)
    d_k = Q.size(-1)
    
    # 1. Scores: (B, N, N)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    
    if mask is not None:
        # Masking out future tokens (for autoregressive generation) or padding
        scores = scores.masked_fill(mask == 0, float('-inf'))
        
    # 2. Weights: (B, N, N)
    attention_weights = F.softmax(scores, dim=-1)
    
    # 3. Output: (B, N, d_v)
    output = torch.matmul(attention_weights, V)
    
    return output
```

## 9. Common Misconceptions
- **"Attention solves long-term dependencies"**: This is an oversimplification. Attention *allows* direct interaction between any two tokens, but it has no inherent sense of sequence order (hence Positional Encoding is required), and standard attention scales quadratically, making it difficult to process truly infinite sequences compared to linear state-space models.
- **Cross-Attention vs. Self-Attention**: In Self-Attention, Q, K, and V all originate from the same sequence. In Cross-Attention (e.g., Decoder attending to Encoder), Q comes from the target sequence, while K and V come from the source sequence.
- **Why $\sqrt{d_k}$?**: People often think the scaling factor is arbitrary. It is derived from the variance of the dot product of two vectors with independent features. Scaling keeps the variance at 1.

## 10. 30-Second Interview Answer
"Self-attention allows tokens in a sequence to dynamically route information among themselves. It calculates an $N \times N$ matrix by taking the dot product of Query and Key matrices, scaling by the square root of the key dimension, applying Softmax, and using the resulting weights to combine the Value vectors. This operation transforms static embeddings into highly contextualized representations."

## 11. 2-Minute Interview Answer
"Self-attention is the core mechanism of the Transformer architecture. Mathematically, it operates as a differentiable dictionary retrieval system. We project input embeddings into Queries, Keys, and Values. The attention scores are the dot products of $Q$ and $K^T$, representing how much 'focus' token A should put on token B. We scale this by $\sqrt{d_k}$ to prevent the dot products from growing too large, which would push the softmax function into regions with vanishing gradients. After applying softmax, we multiply the $N \times N$ weight matrix by $V$. This allows every token to directly interact with every other token in $O(1)$ sequential operations. The fundamental tradeoff is its time and space complexity, which scales quadratically $O(N^2)$ with the sequence length $N$, necessitating hardware-aware optimizations like FlashAttention for long contexts."

## 12. Follow-Up Questions
- **"What does Masked Self-Attention do?"**
  In decoder-only models like GPT, a causal mask forces the upper triangle of the $Q \times K^T$ matrix to $-\infty$ before Softmax. This prevents tokens from looking at future tokens during training, preserving the autoregressive property.
- **"What is the complexity of Self-Attention?"**
  $O(N^2 \cdot d)$ time complexity and $O(N^2)$ space complexity, where $N$ is sequence length and $d$ is the embedding dimension.

## 13. Deeper Questions
- **"Why is the $Q \times K^T$ matrix size independent of the model dimension $d$?"**
  Because the dot product reduces the $d_k$ dimension. `(N, d_k) @ (d_k, N)` results in `(N, N)`. The resulting matrix size depends purely on sequence length.

## 14. Failure Modes / Edge Cases
- **Context Limit:** Because memory scales quadratically $O(N^2)$, standard self-attention runs out of GPU memory quickly on long documents.

## 15. Comparison
- **vs Recurrent Neural Networks (RNNs):** RNNs process tokens sequentially, creating an $O(N)$ sequential path length where early information degrades. Self-attention processes all tokens in parallel, providing an $O(1)$ path length between any two tokens, but at the cost of losing inherent sequence order.

## 16. What To Remember
- The formula: $\text{softmax}(Q K^T / \sqrt{d_k}) V$.
- Complexity is $O(N^2)$ for sequence length $N$.
- Scaling by $\sqrt{d_k}$ prevents vanishing gradients in the Softmax.
- Q, K, V shapes and the intermediate $N \times N$ attention matrix shape.

## 17. Interview Trap
> **Q:** "How does Self-Attention know the order of the words?"
> **A:** It doesn't! Self-attention is fundamentally permutation invariant. If you shuffle the input words, the output vectors will simply be shuffled in the exact same way. It strictly requires Positional Encodings added to the input embeddings to understand word order.

---
*Connected Concepts:* [Query, Key, Value (QKV)](query-key-value.md), [Multi-Head Attention](multi-head-attention.md), [Positional Encoding](positional-encoding.md)
