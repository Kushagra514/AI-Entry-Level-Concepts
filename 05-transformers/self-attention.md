# Self-Attention

## 1. Definition
Self-Attention is a sequence-to-sequence operation where each token in a sequence dynamically updates its own representation by computing a weighted sum of all other tokens in the same sequence, based on how "relevant" they are to it.

## 2. Intuition
You are at a cocktail party. You are talking to someone, but you hear your name across the room. Your brain instantly lowers the "attention weight" on the person in front of you and raises the "attention weight" on the distant conversation. Self-attention does this for words: the word "it" looks across the sentence to figure out what noun it refers to.

## 3. Why it exists
Static embeddings (Word2Vec) map "bank" to a single vector. But "river bank" and "bank account" mean different things. Self-attention exists to create *contextual* embeddings, allowing words to alter their mathematical meaning based on their neighbors.

## 4. Mechanics
1. Every token generates three vectors via learned linear projections: Query (Q), Key (K), and Value (V).
2. **Score:** Compute the dot product between a token's Q and all other tokens' K. (High dot product = high relevance).
3. **Scale:** Divide by $\sqrt{d_k}$ (dimension size) to stabilize gradients.
4. **Softmax:** Apply Softmax to the scores to get weights that sum to 1.
5. **Output:** Multiply these weights by the V vectors and sum them up.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N^2 	imes d)$ where $N$ is sequence length. The $Q \times K^T$ multiplication creates an $N \times N$ matrix.
- **Space Complexity:** $O(N^2)$ to store the attention score matrix.

## 6. Tiny worked example
"Apple is tasty."
- "Apple" (Query) checks Keys of "Apple", "is", "tasty".
- Dot products: `[Apple=10, is=2, tasty=8]`.
- Softmax weights: `[Apple=0.8, is=0.01, tasty=0.19]`.
- Output for "Apple": `0.8*V(Apple) + 0.01*V(is) + 0.19*V(tasty)`. The vector for "Apple" now mathematically contains a hint of "tasty".

## 7. Code (Python, with type hints)
```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
    d_k = Q.size(-1)
    # 1. Dot product of Q and K^T
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
        
    # 2. Softmax to get probabilities
    attention_weights = F.softmax(scores, dim=-1)
    
    # 3. Multiply by Values
    output = torch.matmul(attention_weights, V)
    return output
```

## 8. Common mistakes
- Forgetting the scaling factor $\sqrt{d_k}$. Without it, large dimensions cause large dot products, pushing Softmax into regions with vanishing gradients.
- Confusing Cross-Attention (Q comes from decoder, K/V from encoder) with Self-Attention (Q, K, V all come from the same sequence).

## 9. 30-second interview answer
"Self-attention allows tokens in a sequence to dynamically route information among themselves. It calculates an $N \times N$ attention matrix by taking the dot product of Query and Key vectors, scaling and applying Softmax, and using the resulting weights to combine Value vectors. This yields highly contextualized embeddings."

## 10. 2-minute interview answer
"Self-attention is the mechanism that solves the long-term dependency problem in NLP. Unlike RNNs, it provides an $O(1)$ path length between any two words in a text. Mathematically, it operates as a differentiable dictionary retrieval system. We project input embeddings into Queries, Keys, and Values. The attention scores are the dot products of $Q$ and $K^T$, representing how much 'focus' word A should put on word B. We scale this by $\sqrt{d_k}$ to prevent softmax saturation, apply softmax to normalize the scores, and multiply by $V$. The result is a new representation for each token that has absorbed relevant context from the entire sequence. The fundamental tradeoff is its $O(N^2)$ complexity, which makes processing massive contexts computationally prohibitive without hardware optimization."

## 11. Follow-ups
- "What does Masked Self-Attention do?" (Used in decoders like GPT. It forces the upper triangle of the $Q \times K^T$ matrix to $-\infty$ before Softmax, preventing tokens from looking at future tokens during training).

## 12. Deeper questions
- "What is FlashAttention?" (A hardware-aware algorithm that fuses the Q, K, V operations, avoiding writing the massive $N \times N$ intermediate attention matrix to slow GPU HBM memory, keeping it in fast SRAM).

## 13. Related concepts
- **Transformer**: The architecture built around this mechanism.
- **QKV**: The specific projections used.

## 14. When it breaks / Edge cases
- Memory blows up quadratically with $N$. A 100k context window requires gigabytes of VRAM just for the attention matrix.

## 15. Comparison with alternative approaches
- **vs Convolutions:** CNNs only look at local neighbors (fixed receptive field). Self-attention has a global receptive field at layer 1.

---
*Where this shows up in ML:* 
The defining operation in all Transformers.
