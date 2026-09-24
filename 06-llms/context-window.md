# Context Window

## 1. Definition
The context window is the maximum number of tokens an LLM can process simultaneously in a single forward pass. It dictates how much history, prompt text, and retrieved data the model can "see" at once.

## 2. Intuition
The context window is the model's short-term working memory. If the window is 4,000 tokens (about 10 pages of text), and you feed it a 20-page document, it literally cannot see the first 10 pages when generating its answer.

## 3. Why it exists
Transformers scale quadratically $O(N^2)$ in time and memory with sequence length $N$ due to the Self-Attention mechanism (every token must compute a dot product with every other token). We cannot make context windows infinite without running out of VRAM and compute time.

## 4. Mechanics
- **Attention Matrix:** An $N \times N$ matrix is computed per head, per layer. If $N=100,000$, the matrix alone requires massive memory.
- **KV-Cache:** During generation, we must store the Key and Value vectors for all $N$ tokens in the context window. This memory grows linearly with $N$.
- **Positional Encodings:** The model is pre-trained to recognize positions $0$ to $N_{max}$. It often fails if fed positions $> N_{max}$ because it has never seen them.

## 5. Complexity (Time & Space)
- **Time (Prefill):** $O(N^2 \cdot d)$ to process the initial prompt.
- **Space (KV Cache):** $O(N \cdot L \cdot d)$ to store the cache during generation.

## 6. Tiny worked example
Model Context: 4096 tokens.
System Prompt: 100 tokens.
User History: 2000 tokens.
RAG Retrieved Docs: 1500 tokens.
Total used: 3600.
Tokens left for model to generate answer: 496. If the answer requires 500 tokens, it will abruptly cut off.

## 7. Code (Python)
```python
# Calculating KV Cache memory for Llama-2-7B
# 32 layers, 32 KV heads, head_dim 128, FP16 (2 bytes)
# Memory = 2 (K & V) * batch_size * seq_len * num_layers * num_heads * head_dim * 2 bytes

batch_size = 1
seq_len = 4096
layers = 32
heads = 32
head_dim = 128
bytes_per_param = 2

kv_cache_bytes = 2 * batch_size * seq_len * layers * heads * head_dim * bytes_per_param
print(f"KV Cache Size: {kv_cache_bytes / (1024**2):.2f} MB") # ~2048 MB (2GB) per sequence!
```

## 8. Common mistakes
- Thinking a 1M token context window (like Gemini 1.5) solves all RAG problems. Massive context windows are slow, expensive, and suffer from the "Lost in the Middle" phenomenon where models ignore information in the middle of long contexts.
- Confusing Context Window with Model Parameters (weights). Weights represent long-term memory; context window is short-term memory.

## 9. 30-second interview answer
"The context window is the maximum sequence length an LLM can process. It is limited primarily by the $O(N^2)$ compute and memory complexity of the Self-Attention mechanism, as well as the linear growth of the KV-cache. Techniques to extend it include RoPE scaling, sparse attention, and Ring Attention, which allow modern models to reach 100k+ token windows."

## 10. 2-minute interview answer
"The context window defines the upper bound on an LLM's working memory, dictating how much text can be processed in one pass. The hard limit exists for two reasons: computationally, the dense self-attention matrix scales at $O(N^2)$; memory-wise, storing the KV-cache during generation scales at $O(N)$ but has a huge constant factor, often consuming gigabytes of VRAM for a single request. Historically, extending context meant training from scratch, but modern techniques like RoPE (Rotary Position Embedding) scaling allow us to stretch a model trained on 4K context to 32K or 128K by interpolating the position indices. Even with hardware optimizations like FlashAttention, which avoids materializing the $N \times N$ matrix in HBM, very long contexts suffer from the 'Lost in the Middle' problem — models tend to rely heavily on the beginning and end of the prompt and degrade at retrieving facts from the middle. Therefore, RAG remains essential even with large context windows."

## 11. Follow-ups
- "What is FlashAttention?" (An IO-aware exact attention algorithm. It computes the $O(N^2)$ attention matrix in blocks in the fast SRAM, avoiding reading/writing the massive intermediate matrix to the slow HBM. It speeds up attention 2-4x and reduces memory to $O(N)$).

## 12. Deeper questions
- "How does RoPE scaling work?" (Instead of extrapolating to unseen positions $N+1$, it interpolates by dividing the position index by a scale factor. The model still sees position values within its training range $[0, N]$, just compressed, allowing it to handle longer sequences with minimal fine-tuning).

## 13. Related concepts
- **KV-Cache**: The memory bottleneck of long contexts.
- **RAG**: The architectural alternative to just dumping everything into a massive context window.

## 14. When it breaks / Edge cases
- "Lost in the Middle": Accuracy of fact retrieval drops significantly if the fact is located in the middle 50% of a massive context window.

## 15. Comparison with alternative approaches
- **Long Context vs RAG:** Long context sees the whole document but is expensive per token and slow. RAG is cheap and fast but might fail to retrieve the right chunk. The industry trend is using both together.

---
*Where this shows up in ML:*
Deciding whether to use RAG vs feeding the whole document; calculating GPU requirements for serving.
