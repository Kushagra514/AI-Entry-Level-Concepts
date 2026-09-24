# Transformer Overview

## 1. Definition
The Transformer is a neural network architecture introduced in the 2017 paper "Attention Is All You Need". It dispenses with recurrence and convolutions entirely, relying instead on Self-Attention mechanisms to compute representations of its input and output.

## 2. Intuition
Imagine a reading group trying to understand a complex document. An RNN works like a single person reading word-by-word; by the end of page 5, they've forgotten page 1. A Transformer works like a room of 1,000 people looking at the document simultaneously. Each person holds one word and shouts to everyone else to figure out how their word connects to the others. They instantly grasp the full context of the entire document at once. 

## 3. Why It Exists
Before 2017, NLP relied on RNNs and LSTMs, which process data sequentially ($O(N)$ sequential steps). This created a severe bottleneck: you couldn't parallelize the training across modern GPUs, and gradients vanished over long sequences, meaning models forgot early context. The Transformer exists to solve both: it processes the entire sequence in parallel (massive GPU utilization) and directly connects any two words with an $O(1)$ path length (solving long-term dependencies).

## 4. Core Mechanics & The Transformer Learning Path
To truly understand the Transformer, you must understand the data pipeline from input to output:
1. **Tokenization:** Text is split into subwords.
2. **Embeddings:** Tokens are converted into dense vectors.
3. **Positional Encoding:** Because processing is parallel, vectors are injected with position information so the model knows word order.
4. **Q/K/V Projections:** Tokens are projected into Queries, Keys, and Values.
5. **Scaled Dot-Product Attention:** Tokens score relevance against all other tokens.
6. **Masking:** (If decoder) Future tokens are hidden to preserve autoregressive generation.
7. **Multi-Head Attention (MHA):** Attention is performed in parallel subspaces.
8. **Residual Connections:** The input to the MHA is added to its output to prevent vanishing gradients.
9. **Layer Normalization:** Stabilizes the activations.
10. **Feed-Forward Network (FFN):** A two-layer MLP expands and contracts the dimension to process the aggregated information.
11. **Transformer Block:** Steps 4-10 combined. Models stack dozens of these blocks.

## 5. Mathematical View
A single pass of a generic Transformer block:
$$ x' = \text{LayerNorm}(x + \text{MultiHeadAttention}(x)) $$
$$ x'' = \text{LayerNorm}(x' + \text{FFN}(x')) $$

## 6. Shape / Dimension Tracking
Assume Sequence Length $N$, Model Dimension $d_{\text{model}}$:
```text
Input: (B, N)
Embeddings: (B, N, d_model)
After Positional Encoding: (B, N, d_model)

Attention Output: (B, N, d_model)
Residual + Norm: (B, N, d_model)

FFN Hidden Layer: (B, N, 4 * d_model)
FFN Output Layer: (B, N, d_model)
Residual + Norm: (B, N, d_model)
```
Notice how the tensor shape $(B, N, d_{\text{model}})$ is flawlessly preserved throughout the entire block. This is what allows stacking 96 layers in GPT-4.

## 7. Tiny Worked Example
Input: `"The bank of the river"`
- Token `bank` enters the Transformer.
- In Layer 1 Attention, `bank` attends heavily to `river`.
- The FFN processes this new vector.
- In Layer 2 Attention, the heavily contextualized `bank` vector now confidently signals to the rest of the network: "I am a geographic feature, not a financial institution."

## 8. Minimal Implementation
```python
import torch.nn as nn

class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        # 1. Multi-Head Attention
        self.attention = nn.MultiheadAttention(d_model, num_heads, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        
        # 2. Feed-Forward Network (MLP)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model)
        )
        self.norm2 = nn.LayerNorm(d_model)
        
    def forward(self, x):
        # x shape: (B, N, d_model)
        
        # Sub-layer 1: Attention + Residual + Norm
        attn_out, _ = self.attention(x, x, x)
        x = self.norm1(x + attn_out)
        
        # Sub-layer 2: FFN + Residual + Norm
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)
        
        return x # shape: (B, N, d_model)
```

## 9. Common Misconceptions
- **"Transformers process text sequentially."** They don't. All tokens enter the first layer simultaneously in parallel.
- **"The attention mechanism is the only important part."** The Feed-Forward Network (FFN) actually contains ~2/3 of the model's parameters and acts as the key-value memory of facts the model has learned, while attention just routes the information.

## 10. 30-Second Interview Answer
"The Transformer is an architecture that replaced RNNs by using purely Self-Attention. It processes sequences entirely in parallel, enabling massive GPU scaling. Its core block consists of Multi-Head Attention to route information between tokens, followed by a Feed-Forward Network to process that information, wrapped in Residual connections and Layer Normalization. It forms the basis of all modern LLMs."

## 11. 2-Minute Interview Answer
"The Transformer revolutionized AI by abandoning recurrence in favor of pure Attention. Because RNNs process tokens sequentially, they create a computational bottleneck that prevents scaling. The Transformer takes an entire sequence of tokens simultaneously, relying on Positional Encodings to inject order. In the core Multi-Head Attention layers, every token computes a dot product with every other token, creating an $N \times N$ attention matrix. This allows the model to form rich, contextualized representations with an $O(1)$ path length between any two words, solving long-term dependencies. The aggregated data is then passed through an FFN, which contains the bulk of the model's factual memory. While this $O(N^2)$ attention mechanism is computationally heavy for long contexts, its highly parallelizable matrix math maps perfectly to GPU hardware, which is the singular reason why the massive scaling laws of modern LLMs were possible."

## 12. Follow-Up Questions
- **"What is the difference between Encoder-only and Decoder-only models?"**
  Encoder-only models (BERT) allow bidirectional attention (every token sees every token) and are used for understanding tasks. Decoder-only models (GPT) use a causal mask (tokens can only see past tokens) and are used for autoregressive generation.
- **"How does the model know word order?"**
  Through Positional Encodings. Without them, the Transformer is completely permutation invariant (a bag of words).

## 13. Deeper Questions
- **"Why is the FFN dimension usually 4x the model dimension?"**
  The FFN projects $d_{\text{model}}$ up to a higher-dimensional space to learn complex, non-linear feature combinations, then projects back down to $d_{\text{model}}$ to allow residual connections. The 4x multiplier was chosen empirically in the original paper and became standard.

## 14. Failure Modes / Edge Cases
- **Quadratic Memory Blowup:** Because the attention matrix is $N \times N$, memory requirements grow quadratically with sequence length $N$. A 1M context window requires extreme architectural modifications (like Ring Attention or Sparse Attention) to fit in VRAM.

## 15. Comparison
- **vs RNN/LSTM:** RNNs have $O(N)$ inference complexity (great for memory) but are slow to train (no parallelization) and suffer from vanishing gradients over long sequences. Transformers are fast to train but memory hungry during inference.

## 16. What To Remember
- No recurrence, no convolutions.
- Parallel processing requires positional encoding.
- The block: MHA -> Add/Norm -> FFN -> Add/Norm.
- $O(N^2)$ complexity with respect to sequence length.

## 17. Interview Trap
> **Q:** "Which component of the Transformer stores the factual knowledge of the world?"
> **A:** Most people say "Attention". Attention is merely a routing mechanism. The actual factual knowledge (e.g., "Paris is the capital of France") is overwhelmingly stored in the weights of the Feed-Forward Networks (FFN) located after the attention mechanism in each block.

---
*Connected Concepts:* [Self-Attention](self-attention.md), [Multi-Head Attention](multi-head-attention.md), [Encoder vs Decoder](encoder-decoder.md), [Positional Encoding](positional-encoding.md)
