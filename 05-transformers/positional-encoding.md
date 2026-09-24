# Positional Encoding

## 1. Definition
Positional Encoding adds position-dependent signals to token embeddings in Transformers, giving the model information about where each token appears in the sequence — since Self-Attention itself is permutation-invariant.

## 2. Intuition
Imagine giving 10 identical red boxes to 10 people in a line. You can't tell who is first and who is last — the boxes are identical. Positional Encoding is like writing the person's queue number on each box before they receive it, so the model can tell "token at position 3" from "token at position 7."

## 3. Why it exists
Self-Attention computes pairwise scores between all tokens simultaneously — it has no inherent notion of sequence order. If you shuffled the tokens, the attention output would be the same (just permuted). Positional encodings inject order.

## 4. Mechanics
- **Sinusoidal PE (Original "Attention Is All You Need"):** For position $pos$ and dimension $i$:
  $PE_{(pos,2i)} = \sin(pos/10000^{2i/d})$
  $PE_{(pos,2i+1)} = \cos(pos/10000^{2i/d})$
  Added (not concatenated) to the token embedding.
- **Learned PE (GPT, BERT):** A trainable embedding matrix where position index is looked up, like a word embedding. More flexible, but doesn't generalize to unseen positions.
- **Rotary PE (RoPE — used in Llama):** Encodes position via rotation of the Q and K vectors before the dot product, enabling relative position awareness and better length generalization.
- **ALiBi:** Instead of adding to embeddings, adds a position-based penalty to attention scores.

## 5. Complexity (Time & Space)
- **Time:** $O(1)$ additional computation per token (simple lookup or sin/cos).
- **Space:** $O(L \times d)$ for learned PE (L = max sequence length, d = embedding dim).

## 6. Tiny worked example
Token "cat" has embedding $[0.5, 0.3]$. At position 4 with $d=2$:
$PE_{(4,0)} = \sin(4/10000^0) = \sin(4) \approx -0.757$
$PE_{(4,1)} = \cos(4/10000^0) = \cos(4) \approx -0.654$
Final input: $[0.5 + (-0.757), 0.3 + (-0.654)] = [-0.257, -0.354]$.

## 7. Code (Python)
```python
import torch
import numpy as np

def sinusoidal_pe(max_len: int, d_model: int) -> torch.Tensor:
    pe = torch.zeros(max_len, d_model)
    position = torch.arange(0, max_len).unsqueeze(1).float()
    div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                         -(np.log(10000.0) / d_model))
    pe[:, 0::2] = torch.sin(position * div_term)  # Even dims
    pe[:, 1::2] = torch.cos(position * div_term)  # Odd dims
    return pe  # Shape: (max_len, d_model)
```

## 8. Common mistakes
- Confusing Absolute PE (original paper) with Relative PE (RoPE, ALiBi). Absolute PE assigns a fixed vector to each position. Relative PE encodes the distance between positions, making it more robust to sequence lengths unseen during training.
- Forgetting to add PE before the first Transformer block, not after.

## 9. 30-second interview answer
"Positional Encoding injects sequence-order information into the Transformer because Self-Attention is permutation-invariant. The original paper used fixed sinusoidal encodings added to embeddings. Modern LLMs (Llama) use Rotary PE (RoPE), which encodes relative positions via Q/K vector rotation, offering better length generalization."

## 10. 2-minute interview answer
"The Transformer's permutation invariance is a design feature (parallelism) that requires a workaround: positional encodings. The original Transformer uses sinusoids with different frequencies for each embedding dimension. Lower dimensions encode coarse position; higher dimensions encode fine-grained position. The frequencies were chosen so that any offset $k$ corresponds to a linear transformation, enabling the model to attend to relative positions via linear combination. Modern LLMs like Llama use RoPE (Rotary Position Embedding), which encodes position by rotating Q and K vectors. The dot product of RoPE-encoded Q and K vectors depends only on their relative position, not absolute positions, enabling better generalization beyond the training context length."

## 11. Follow-ups
- "Why do models struggle with context lengths beyond their training length?" (Learned PEs produce out-of-distribution embeddings for unseen positions. Sinusoidal PEs theoretically extrapolate, but attention patterns still shift. RoPE + ALiBi generalize somewhat better).

## 12. Deeper questions
- "What is context window extension (e.g., RoPE scaling / YaRN)?" (By scaling the position indices in RoPE's rotation formula, you can extend a model trained on 4K context to 128K context without full retraining, with some fine-tuning to adapt).

## 13. Related concepts
- **Self-Attention**: Becomes position-aware only via PE.
- **RoPE**: The dominant PE in open-source LLMs.

## 14. When it breaks / Edge cases
- Learned PE fails completely at positions > the training max length. Sinusoidal PE degrades gracefully. RoPE with scaling handles it best.

## 15. Comparison with alternative approaches
- **Sinusoidal vs Learned vs RoPE vs ALiBi:** Sinusoidal = no parameters, good extrapolation theory. Learned = more flexible, poor extrapolation. RoPE = relative, good generalization. ALiBi = minimal parameters, strong length generalization via attention bias.

---
*Where this shows up in ML:*
Every Transformer model. Llama uses RoPE. GPT-2/3 uses learned PE. The original Transformer uses sinusoidal. Context length extension techniques (YaRN, LongRoPE) are active research areas.
