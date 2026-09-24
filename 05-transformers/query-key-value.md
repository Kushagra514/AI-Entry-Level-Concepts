# Query, Key, Value (QKV)

## 1. Definition
Query, Key, and Value (QKV) are three distinct vectors generated for every token in a Transformer, used by the Self-Attention mechanism to calculate contextual relationships. 

## 2. Intuition
Think of a database search or a library. 
- **Query (Q):** What you type into the search bar ("Action movies").
- **Key (K):** The metadata/tags on the books on the shelf ("Genre: Action", "Genre: Romance").
- **Value (V):** The actual content of the book.
Attention compares your Query to all Keys. Where they match, you extract that Value.

## 3. Why it exists
If we just computed the dot product of the raw word embeddings with themselves, we'd lack flexibility. Generating three distinct projections (Q, K, V) allows the model to learn asymmetrical relationships. E.g., the word "it" (Query) might seek out nouns (Keys), while the noun outputs its grammatical features (Values).

## 4. Mechanics
1. We have three learned weight matrices: $W_Q, W_K, W_V$.
2. The input embedding $X$ is multiplied by these matrices to produce $Q = X W_Q$, $K = X W_K$, $V = X W_V$.
3. These representations are fed into the scaled dot-product attention formula: $Attention(Q, K, V) = Softmax(QK^T / \sqrt{d_k}) V$.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N 	imes d^2)$ to project a sequence of $N$ tokens from dimension $d$ to Q, K, V.
- **Space Complexity:** $O(N 	imes d)$ to store the Q, K, V matrices.

## 6. Tiny worked example
Input embedding $X$ for "He".
$W_Q, W_K, W_V$ are learned matrices.
"He" generates $Q_{he}$ (looking for verbs).
"Ran" generates $K_{ran}$ (identifies as a verb).
$Q_{he} \cdot K_{ran}$ is high.
"He" pulls in $V_{ran}$ to update its meaning.

## 7. Code (Python, with type hints)
```python
import torch
import torch.nn as nn

class QKVProjection(nn.Module):
    def __init__(self, embed_dim: int, head_dim: int):
        super().__init__()
        # In practice, usually fused into one linear layer for speed
        self.q_proj = nn.Linear(embed_dim, head_dim)
        self.k_proj = nn.Linear(embed_dim, head_dim)
        self.v_proj = nn.Linear(embed_dim, head_dim)
        
    def forward(self, x: torch.Tensor):
        Q = self.q_proj(x)
        K = self.k_proj(x)
        V = self.v_proj(x)
        return Q, K, V
```

## 8. Common mistakes
- Assuming Q, K, and V must have the same dimensions as the input. (In Multi-Head Attention, they are projected down to $d_{model} / num\_heads$).
- Thinking Q and K must have the same dimension as V. (Q and K must match to do the dot product, but V can technically be any dimension, though they are usually kept the same).

## 9. 30-second interview answer
"QKV is the abstraction used in Self-Attention, inspired by database retrieval. Input tokens are projected into Queries (what the token is looking for), Keys (what the token contains), and Values (the actual information it provides). The dot product of Queries and Keys determines the attention weights applied to the Values."

## 10. 2-minute interview answer
"The QKV mechanism is how Transformers achieve asymmetric, dynamic routing of information. If we used raw embeddings to compute attention, the relationship between token A and token B would be perfectly symmetric. By applying three separate learned linear transformations—$W_Q$, $W_K$, and $W_V$—the model learns specialized roles. A token's Query vector encodes what context it needs to disambiguate itself. Its Key vector encodes what context it can offer to others. The dot product $Q \times K^T$ yields the relevance score. Finally, the Value vector contains the actual semantic payload that gets aggregated and passed to the next layer. In modern implementations, these three projections are often fused into a single dense matrix multiplication for maximum GPU efficiency."

## 11. Follow-ups
- "What happens in Cross-Attention (e.g., Encoder-Decoder)?" (The Queries come from the Decoder's current state, but the Keys and Values come from the Encoder's final output).

## 12. Deeper questions
- "What is Grouped Query Attention (GQA) / Multi-Query Attention (MQA)?" (To save memory during LLM inference, MQA shares a single K and V head across multiple Q heads, drastically reducing the KV-cache size).

## 13. Related concepts
- **Self-Attention**: Consumes QKV.
- **KV-Cache**: In LLM generation, we cache the K and V matrices of past tokens to avoid recomputing them.

## 14. When it breaks / Edge cases
- Memory constraints in autoregressive generation (the KV-cache grows linearly with sequence length, eventually causing Out Of Memory).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The first step of every Attention block.
