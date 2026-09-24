# Transformer One-Page Revision

## The Flow (QKV -> MHA -> Block -> LLM)
1. **Tokenization:** Split text to subwords $\to$ lookup Embedding $(B, N, d_{\text{model}})$.
2. **Positional Encoding:** Add sinusoids or learned vectors so model knows order.
3. **Q, K, V Projections:** $Q = X W_Q$, $K = X W_K$, $V = X W_V$.
4. **Attention:** $\text{Softmax}(Q K^T / \sqrt{d_k}) V$.
   - $Q \times K^T$: How much does Token A care about Token B? (Shape: $B, N, N$)
   - Scale by $\sqrt{d_k}$ to stop Softmax from saturating (vanishing gradients).
   - Multiply by $V$ to aggregate the actual information.
5. **Multi-Head Attention (MHA):** Run attention in $H$ parallel subspaces. Concatenate results and project back to $d_{\text{model}}$.
6. **Residual & Norm:** $x = \text{LayerNorm}(x + \text{MHA}(x))$. Solves vanishing gradients.
7. **Feed-Forward Network (FFN):** Expands to $4 \times d_{\text{model}}$, applies GELU, projects back. *Stores factual knowledge.*
8. **Residual & Norm:** $x = \text{LayerNorm}(x + \text{FFN}(x))$.

## Encoder vs Decoder
- **Encoder (BERT):** Bidirectional. Sees the whole sequence at once. Good for classification/understanding.
- **Decoder (GPT):** Causal Masking. Upper triangle of $N \times N$ attention matrix is set to $-\infty$. Tokens can only attend to past tokens. Good for autoregressive generation.

## Complexities
- **Time per layer:** $O(N^2 \cdot d)$. Bottleneck is $N^2$ sequence length.
- **Space:** $O(N^2)$ for the attention matrix (limits context window).

## Interview Traps
- *Does attention store facts?* No, the FFN stores facts. Attention routes information.
- *How does it know word order?* It doesn't. Without Positional Encodings, it's permutation invariant.
