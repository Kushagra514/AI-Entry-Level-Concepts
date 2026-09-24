# LLM Pretraining

## 1. Definition
Pretraining is the initial, compute-intensive phase where a Large Language Model trains on a massive, unlabeled text corpus using a self-supervised objective (usually next-token prediction). The model learns grammar, facts, and statistical relationships in language, establishing a general-purpose foundation.

## 2. Intuition
Pretraining is like a human spending their first 18 years reading every book, article, and website in the world. They aren't explicitly taught specific tasks (like "how to summarize an email"); they just absorb the structure of language and the general knowledge of the world. At the end of this phase, they know a lot, but they just want to continue completing sentences, not necessarily answer questions helpfully.

## 3. Why It Exists
Supervised learning requires labeled data, which is expensive and scarce. Pretraining leverages the near-infinite supply of raw text on the internet to learn a powerful general-purpose representation. This "Foundation Model" can later be adapted (fine-tuned) to specific tasks with very little labeled data.

## 4. Core Mechanics
1. **Data Pipeline:** Scrape web data, filter low-quality text, strictly deduplicate, and tokenize into subwords.
2. **Objective:**
   - **Causal Language Modeling (CLM):** Predict the next token given all previous tokens (e.g., GPT, Llama).
   - **Masked Language Modeling (MLM):** Predict missing/masked tokens given surrounding context (e.g., BERT).
3. **Training:** Requires massive GPU clusters running for months.
4. **Optimization:** Typically uses AdamW, gradient clipping, learning rate warmup, and cosine decay.

## 5. Mathematical View
For Causal Language Modeling, the objective is to maximize the probability of the sequence of tokens $x_{1:T}$:

$$ \mathcal{L} = - \sum_{t=1}^{T} \log P(x_t \mid x_{1}, x_2, \dots, x_{t-1}; \Theta) $$

This is the standard Cross-Entropy Loss applied over the sequence.

## 6. Shape / Dimension Tracking
During a pretraining step with batch size $B$, sequence length $S$, vocabulary size $V$:
```text
Inputs: (B, S)
Labels: (B, S)  <-- Inputs shifted left by 1 token

Logits: (B, S, V)
Target: (B, S)

Cross-Entropy computes loss by comparing (B*S, V) logits against (B*S) targets.
```

## 7. Tiny Worked Example
Given the text: "The cat sat on the mat."
CLM Objective creates these training examples instantly by shifting:
Input: `"The"`, Target: `"cat"`
Input: `"The cat"`, Target: `"sat"`
Input: `"The cat sat"`, Target: `"on"`

## 8. Minimal Implementation
```python
import torch
import torch.nn as nn

def pretrain_step(model, inputs: torch.Tensor, optimizer):
    # inputs shape: (B, S+1)
    # Shift inputs for next-token prediction
    x = inputs[:, :-1]     # (B, S)
    y_true = inputs[:, 1:] # (B, S)
    
    logits = model(x) # (B, S, V)
    
    loss_fn = nn.CrossEntropyLoss()
    # Flatten spatial dimensions to match standard CrossEntropy input
    loss = loss_fn(logits.view(-1, logits.size(-1)), y_true.view(-1))
    
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    
    return loss.item()
```

## 9. Common Misconceptions
- **"Pretraining embeds explicit reasoning rules."** Pretraining strictly learns a statistical representation (a probability distribution over sequences). It does not learn explicit, symbolic reasoning rules. What appears as "reasoning" is an emergent property of modeling extremely complex statistical relationships in data.
- **"More data is always better."** Low-quality data actively degrades a model. Severe deduplication and quality filtering are often more important than sheer volume.
- **"Pretrained models are chat bots."** A raw pretrained model (Base Model) is just a document completer. If you ask it a question, it might answer with another question, mimicking a forum post.

## 10. 30-Second Interview Answer
"Pretraining is the unsupervised phase where an LLM learns general language representations from massive web corpora. For models like GPT, the objective is Causal Language Modeling—predicting the next token. This phase consumes the vast majority of the compute budget and embeds factual knowledge and syntax into the model's weights, creating a Base Model that is later aligned for specific tasks."

## 11. 2-Minute Interview Answer
"Pretraining is the engine of the modern LLM paradigm. By using a self-supervised objective like next-token prediction on trillions of tokens, the model is forced to learn a highly compressed statistical representation of human knowledge. The scaling laws for neural language models demonstrate that cross-entropy loss predictably decreases as a power-law with increases in compute, dataset size, and parameter count. In practice, pretraining is a massive distributed engineering challenge involving data curation, Tensor and Pipeline Parallelism, and training stability techniques like gradient clipping. The end result is a foundation model that understands language but is merely a text-continuation engine, which must subsequently undergo instruction tuning and alignment to become a useful AI assistant."

## 12. Follow-Up Questions
- **"What are Scaling Laws in LLMs?"**
  Empirical observations (e.g., the Chinchilla paper) showing how model performance improves predictably as you scale parameters and training tokens. Chinchilla scaling suggests an optimal ratio of roughly 20 tokens per parameter.
- **"How do you handle the massive memory requirements during pretraining?"**
  Using DeepSpeed ZeRO to partition optimizer states, gradients, and parameters across GPUs, alongside 3D Parallelism (Tensor, Pipeline, and Data parallelism) and activation checkpointing.

## 13. Comparison
- **CLM (GPT) vs MLM (BERT):** CLM predicts the next token, forcing an autoregressive constraint, which makes it perfect for text generation. MLM randomly masks tokens and predicts them using bidirectional context, making it excellent for understanding and classification tasks, but poor at generation.

## 14. What To Remember
- The objective is usually next-token prediction (Cross-Entropy Loss).
- It produces a Base Model, not a chatbot.
- Scaling laws dictate the compute/data/parameter tradeoff.

## 15. Interview Trap
> **Q:** "If we want a model to be better at answering medical questions, should we modify the pretraining objective?"
> **A:** No. Modifying the base architecture or objective is rarely the right approach. You should either include high-quality medical text in the pretraining corpus, or apply supervised fine-tuning / RAG to a standard pretrained foundation model.

---
*Connected Concepts:* [Instruction Tuning](instruction-tuning.md), [Alignment (RLHF)](alignment.md), [Next Token Prediction](next-token-prediction.md)
