# Next Token Prediction (Causal Language Modeling)

## 1. Definition
Next Token Prediction is the primary pretraining objective for generative LLMs, where the model is trained to predict the probability distribution of the $t$-th token given tokens $1$ through $t-1$.

## 2. Intuition
It's like playing "fill in the blank" repeatedly. Given "The sky is", you predict "blue". Given "The sky is blue and the grass is", you predict "green". By doing this billions of times across all human knowledge, the model is forced to learn facts, logic, and grammar just to make accurate predictions.

## 3. Why it exists
It is the simplest, most scalable self-supervised objective. It requires no human labeling—the text itself provides the labels (the next word is the ground truth). It naturally aligns with autoregressive generation during inference.

## 4. Mechanics
- **Masking:** In a Transformer decoder, causal masking ensures position $i$ can only attend to positions $\le i$. 
- **Teacher Forcing:** During training, we don't feed the model's own predictions back into it. We feed the true sequence and predict the next token at every position simultaneously.
- **Loss:** Cross-Entropy loss between the predicted logits and the actual next token.
- **Loss computation:** $\mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T} \log P_\theta(x_t | x_{<t})$.

## 5. Complexity (Time & Space)
- **Time:** Efficient during training. Because of teacher forcing and causal masking, a sequence of length $N$ computes all $N$ next-token predictions in parallel in one forward pass.
- **Space:** Requires storing logits for $N \times V$ (vocab size) to compute loss, which can be memory intensive.

## 6. Tiny worked example
Sequence: `[A, B, C, D]`
Input to model: `[A, B, C]`
Target labels:  `[B, C, D]`
The model outputs logits at 3 positions.
Loss is avg of CrossEntropy(`logits_0`, `B`), CrossEntropy(`logits_1`, `C`), CrossEntropy(`logits_2`, `D`).

## 7. Code (Python)
```python
import torch
import torch.nn.functional as F

def causal_lm_loss(logits, targets):
    # logits shape: (batch, seq_len, vocab_size)
    # targets shape: (batch, seq_len)
    
    # Flatten everything to (batch*seq_len, vocab_size)
    logits_flat = logits.reshape(-1, logits.size(-1))
    targets_flat = targets.reshape(-1)
    
    # Compute Cross Entropy
    return F.cross_entropy(logits_flat, targets_flat)
```

## 8. Common mistakes
- Thinking the model generates a token, appends it, and does another forward pass *during training*. That only happens during *inference*. Training processes the whole sequence at once.
- Forgetting to shift the targets relative to the inputs (input `[:-1]`, target `[1:]`).

## 9. 30-second interview answer
"Next-token prediction, or Causal Language Modeling, trains a model to predict the next word given the preceding context. It is the core objective of models like GPT. During training, causal masking and teacher forcing allow us to compute the loss for all tokens in a sequence simultaneously, making it highly scalable on GPUs."

## 10. 2-minute interview answer
"Next-token prediction is the engine of emergent intelligence in LLMs. The objective is deceptively simple: minimize the negative log-likelihood of the next token given the history. However, to accurately predict the next token in a complex text, the model must internally develop representations of syntax, semantics, facts, and even reasoning processes. For instance, to predict the last word of a Python function, the model must 'understand' the logic of the code. Architecturally, this is implemented using a decoder-only Transformer with causal masking, ensuring tokens only attend to the past. During training, we use teacher forcing, processing an entire sequence of length $N$ in parallel to predict shifted targets, making GPU utilization highly efficient. At inference, we switch to autoregressive generation, sampling one token at a time."

## 11. Follow-ups
- "Why does next-token prediction lead to reasoning capabilities?" (Because accurately predicting the conclusion of a complex logical argument in the training data requires modeling the logical steps. It forces the model to compress the underlying generative process of the text).

## 12. Deeper questions
- "What is exposure bias in sequence generation?" (During training, the model sees perfect ground-truth history (teacher forcing). During inference, it sees its own generated tokens, which may contain errors. These errors compound because the model was never trained on its own mistakes).

## 13. Related concepts
- **Autoregressive Generation**: The inference counterpart to next-token prediction.
- **Teacher Forcing**: The training strategy used.

## 14. When it breaks / Edge cases
- Models can learn "shortcut" statistics (e.g., repeating phrases) rather than deep semantics if the data is low quality.

## 15. Comparison with alternative approaches
- **Next-Token vs Masked-Token (BERT):** Masked token prediction sees the future context, making it better for representation learning but unsuitable for open-ended generation.

---
*Where this shows up in ML:*
The fundamental training objective for GPT-3, Llama, Claude, etc.
