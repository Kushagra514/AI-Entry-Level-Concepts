# Transformers in NLP

## 1. Definition
The Transformer is a sequence-to-sequence architecture introduced in "Attention Is All You Need" (2017) that replaced recurrent architectures with purely attention-based mechanisms, becoming the foundation of all modern NLP models.

## 2. Intuition
Unlike RNNs that read text like a human — word by word, trying to remember — the Transformer reads the entire sentence simultaneously, like a photograph, and directly draws connections between any word and any other word in a single computation step.

## 3. Why it exists
RNNs were slow to train (sequential processing prevented GPU parallelization) and forgot distant context despite LSTM's improvements. The Transformer exists to parallelize sequence processing and provide direct (non-sequential) connectivity between all positions.

## 4. Mechanics
The full Transformer architecture:
1. **Tokenize** input → integer IDs.
2. **Embed** tokens → dense vectors.
3. **Add Positional Encodings** — since there's no recurrence, inject position information explicitly.
4. **Encoder** (in seq2seq models): $N$ stacks of [Multi-Head Self-Attention → Add & Norm → Feed-Forward → Add & Norm].
5. **Decoder** (in seq2seq models): Same, plus Masked Self-Attention (prevents looking at future tokens) and Cross-Attention (attends to encoder output).
6. **Output projection** → softmax over vocabulary → probabilities.

## 5. Complexity (Time & Space)
- **Time:** $O(N^2 d)$ per layer due to the attention matrix computation.
- **Space:** $O(N^2)$ for the attention matrix per head.

## 6. Tiny worked example
English → French translation: "The cat sat" → "Le chat s'est assis."
The decoder, when generating "chat", attends heavily to "cat" in the encoder output (Cross-Attention). The decoder's own Masked Self-Attention allows "chat" to attend to "Le" but NOT to future tokens "s'est assis."

## 7. Code (Python)
```python
import torch
import torch.nn as nn

# PyTorch's built-in Transformer
transformer = nn.Transformer(
    d_model=512,
    nhead=8,
    num_encoder_layers=6,
    num_decoder_layers=6,
    dim_feedforward=2048,
    dropout=0.1
)

src = torch.rand(10, 32, 512)  # (seq_len, batch, d_model)
tgt = torch.rand(20, 32, 512)
out = transformer(src, tgt)  # (20, 32, 512)
```

## 8. Common mistakes
- Thinking all modern LLMs use the full encoder-decoder Transformer. GPT-series uses decoder-only. BERT uses encoder-only. Only T5, BART, and translation models use full encoder-decoder.
- Forgetting that the Positional Encoding is added (not concatenated) to the token embedding.

## 9. 30-second interview answer
"The Transformer replaced RNNs with Multi-Head Self-Attention, enabling fully parallel sequence processing. Its $O(N^2)$ attention complexity is a tradeoff for direct, length-independent connectivity between all tokens. Modern LLMs are either encoder-only (BERT), decoder-only (GPT), or full encoder-decoder (T5)."

## 10. 2-minute interview answer
"The Transformer's key insight was that you don't need recurrence to model sequences — you need attention. By computing pairwise attention between all tokens simultaneously, it achieves what LSTMs struggled with: direct connections over arbitrarily long distances. The architecture is modular: 6 encoder layers of Self-Attention + FFN, each with Residual Connections and Layer Normalization to stabilize training. The decoder adds Masked Self-Attention (causal masking) to prevent the model from 'cheating' by looking at future target tokens, plus Cross-Attention to incorporate the encoded source context. This architecture scaled to become the foundation of BERT, GPT, T5, and every modern LLM by simply scaling up depth, width, heads, and training data."

## 11. Follow-ups
- "Why is Masked Self-Attention necessary in the decoder?" (During training, the entire target sequence is fed in parallel. Masking prevents the model from attending to future target tokens — this would make next-token prediction trivial and the model would learn nothing).

## 12. Deeper questions
- "How does Cross-Attention differ from Self-Attention?" (In Cross-Attention: $Q$ comes from the decoder's current state, $K$ and $V$ come from the encoder's output. This lets the decoder query the full source context at every generation step).

## 13. Related concepts
- **BERT**: Encoder-only Transformer, pretrained with Masked Language Modeling.
- **GPT**: Decoder-only Transformer, pretrained with causal next-token prediction.

## 14. When it breaks / Edge cases
- $O(N^2)$ attention breaks for very long sequences (>4096 tokens naively). Addressed by Sparse Attention, Sliding Window, or linear attention approximations.

## 15. Comparison with alternative approaches
- **vs LSTM:** LSTM is $O(N)$ inference (sequential), handles long sequences with less memory, but can't be parallelized during training. Transformer is $O(N^2)$ in sequence but $O(1)$ parallel training depth.

---
*Where this shows up in ML:*
Every state-of-the-art NLP model: GPT-4, Claude, Llama, Gemini, BERT, T5.
