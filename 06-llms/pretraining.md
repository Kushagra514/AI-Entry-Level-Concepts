# LLM Pretraining

## 1. Definition
Pretraining is the initial, compute-intensive phase where a Large Language Model trains on a massive, unlabeled text corpus using a self-supervised objective (like next-token prediction or masked language modeling) to learn grammar, facts, and reasoning capabilities.

## 2. Intuition
Pretraining is like a human spending their first 18 years reading every book, article, and website in the world. They aren't taught specific tasks (like "how to summarize an email"); they just absorb general knowledge and language structure.

## 3. Why it exists
Supervised learning requires labeled data, which is expensive and scarce. Pretraining leverages the near-infinite supply of raw text on the internet to learn a powerful general-purpose representation of language, which can later be adapted to specific tasks with very little labeled data.

## 4. Mechanics
- **Data Collection & Cleaning:** Scrape web data (Common Crawl), filter out low-quality text, deduplicate, and remove toxic content.
- **Tokenization:** Convert text into subword tokens (e.g., BPE, WordPiece).
- **Objective:** 
  - **Causal Language Modeling (CLM):** Predict next token (GPT).
  - **Masked Language Modeling (MLM):** Predict missing tokens (BERT).
- **Compute:** Requires massive GPU clusters (thousands of GPUs) running for weeks or months. Optimization uses AdamW, gradient clipping, learning rate warmup, and cosine decay.

## 5. Complexity (Time & Space)
- **Time:** $O(\text{Tokens} \times \text{Parameters})$. Typically $10^{21}$ to $10^{24}$ FLOPs.
- **Space:** Requires sharding model weights, optimizer states, and gradients across many GPUs (Zero Redundancy Optimizer / FSDP).

## 6. Tiny worked example
Given the text: "The cat sat on the mat."
CLM Objective creates these training examples:
Input: "The", Target: "cat"
Input: "The cat", Target: "sat"
Input: "The cat sat", Target: "on"...

## 7. Code (Python)
```python
import torch
import torch.nn as nn

# Simplified CLM Pretraining step
def pretrain_step(model, inputs, optimizer):
    # inputs shape: (batch_size, seq_len)
    # Shift inputs for next-token prediction
    x = inputs[:, :-1]
    y_true = inputs[:, 1:]
    
    logits = model(x) # shape: (batch_size, seq_len-1, vocab_size)
    
    loss_fn = nn.CrossEntropyLoss()
    loss = loss_fn(logits.reshape(-1, logits.size(-1)), y_true.reshape(-1))
    
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    return loss.item()
```

## 8. Common mistakes
- Confusing pretraining with fine-tuning. Pretraining takes months and uses terabytes of raw text. Fine-tuning takes hours/days and uses thousands of high-quality conversational pairs.
- Underestimating data quality. "Garbage in, garbage out" heavily applies; filtering and deduplicating pretraining data is crucial for model quality.

## 9. 30-second interview answer
"Pretraining is the unsupervised phase where an LLM learns general language representations from massive web corpora. For models like GPT, the objective is Causal Language Modeling (predicting the next token). This phase consumes 99% of the compute budget and embeds factual knowledge, grammar, and emergent reasoning into the model's weights."

## 10. 2-minute interview answer
"Pretraining is the engine of the modern LLM paradigm. By using a self-supervised objective like next-token prediction on trillions of tokens of text, the model is forced to learn a compressed representation of human knowledge. The scaling laws for neural language models show that cross-entropy loss predictably decreases as a power-law with increases in compute, dataset size, and parameter count. In practice, pretraining involves massive engineering challenges: data curation (filtering Common Crawl, deduplication, toxicity removal), distributed training (Tensor Parallelism, Pipeline Parallelism, ZeRO), and training stability (mixed precision, learning rate schedules). The result is a foundation model that has broad capabilities but isn't yet an AI assistant — it just wants to continue text. We then use fine-tuning and alignment to mold it into a useful assistant."

## 11. Follow-ups
- "What are Scaling Laws in LLMs?" (Empirical observations (e.g., Chinchilla) showing how model performance improves predictably as you scale parameters and training tokens. Chinchilla optimal scaling suggests ~20 tokens per parameter).

## 12. Deeper questions
- "How do you handle the massive memory requirements during pretraining?" (Using DeepSpeed ZeRO stages to partition optimizer states, gradients, and parameters across GPUs, plus activation checkpointing to trade compute for memory).

## 13. Related concepts
- **Fine-Tuning**: The next step after pretraining.
- **Tokenization**: How text is prepared for pretraining.

## 14. When it breaks / Edge cases
- Training instability (loss spikes) is common at scale, often requiring restarting from checkpoints or adjusting learning rates.

## 15. Comparison with alternative approaches
- **CLM (GPT) vs MLM (BERT):** CLM trains the model to generate text autoregressively. MLM provides better bidirectional context for understanding tasks but cannot easily generate text.

---
*Where this shows up in ML:*
Creating foundation models like Llama 3, GPT-4, Mistral.
