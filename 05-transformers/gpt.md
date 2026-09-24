# GPT (Generative Pretrained Transformer)

## 1. Definition
GPT is a family of decoder-only Transformer models pretrained on Causal Language Modeling (next-token prediction) on large text corpora, producing generalist language models capable of in-context learning and instruction following.

## 2. Intuition
A very well-read person who has read essentially the entire internet. Give them a prompt and they will continue it in the most plausible way given everything they've read. They complete text — they don't just encode it. That is GPT.

## 3. Why it exists
BERT is powerful for understanding but cannot generate text. GPT showed that the simpler pretraining objective — predict the next token — scales massively and produces emergent capabilities: reasoning, translation, code generation, without task-specific training. GPT-3 demonstrated few-shot in-context learning at scale.

## 4. Mechanics
**Architecture:** Decoder-only. No encoder. No Cross-Attention.
- $N$ stacked Transformer decoder blocks, each with:
  - Masked (Causal) Self-Attention — each token attends only to previous tokens.
  - FFN.
  - Residual + LayerNorm (Pre-LN in GPT-2+).

**Pretraining Objective:** $\mathcal{L} = -\sum_{i} \log P(x_i | x_1, ..., x_{i-1})$. Standard left-to-right next-token prediction.

**Inference:** Autoregressive — sample one token at a time, append it, and re-run.

**In-Context Learning:** At inference, examples in the prompt act as implicit fine-tuning without weight updates. GPT-3 demonstrated this emergently at scale.

## 5. Complexity (Time & Space)
- **Training:** Efficiently parallelized — all positions computed simultaneously with causal masking.
- **Inference:** Sequential — each new token requires a full forward pass. KV-cache reduces this to $O(N \cdot d)$ per step after the first.

## 6. Tiny worked example
Prompt: "The capital of France is"
- GPT computes hidden states for all tokens in parallel.
- Final token's logits over vocabulary.
- Highest probability token: "Paris". Generate it, append, continue.

## 7. Code (Python)
```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

inputs = tokenizer("The capital of France is", return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_new_tokens=5,
    do_sample=True,
    temperature=0.7,
    top_p=0.9
)
print(tokenizer.decode(outputs[0]))
```

## 8. Common mistakes
- Thinking GPT processes text bidirectionally like BERT. It is strictly left-to-right (causal) at both train and inference time.
- Not using KV-cache during inference, causing $O(N^2)$ generation complexity instead of near-linear.

## 9. 30-second interview answer
"GPT is a decoder-only Transformer pretrained with causal next-token prediction. It attends only to previous tokens (causal masking), enabling autoregressive text generation. At scale, it develops emergent capabilities including in-context learning (GPT-3) and instruction following (InstructGPT/ChatGPT via RLHF). Modern LLMs (Llama, Claude, Gemini) all follow the GPT decoder-only architecture."

## 10. 2-minute interview answer
"GPT's key insight was simplicity at scale: a decoder-only Transformer with a single pretraining objective (next-token prediction) trained on increasingly large corpora produces increasingly capable models. GPT-1 showed transfer learning. GPT-2 showed zero-shot generalization. GPT-3 showed few-shot in-context learning — capabilities that emerged from scale without task-specific training. InstructGPT (2022) added RLHF (Reinforcement Learning from Human Feedback): supervised fine-tuning on human demonstrations, then reward model training, then PPO optimization to align the model to human preferences — creating ChatGPT. Modern open-source LLMs like Llama 3, Mistral, and Qwen are all GPT-style decoder-only Transformers differing in specific architectural choices (RoPE, GQA, SwiGLU, RMSNorm) and training data."

## 11. Follow-ups
- "What is RLHF?" (Reinforcement Learning from Human Feedback: fine-tune the LLM on human preference data using a learned reward model, then apply PPO to maximize the reward while a KL penalty prevents too much deviation from the base model).

## 12. Deeper questions
- "Why does the KV-cache grow with context length and what are the implications?" (Each new token appends K and V vectors to the cache. For a 70B model with 8K context, the KV-cache alone requires ~16GB VRAM. This is why context window length and number of KV heads (GQA/MQA) are critical deployment parameters).

## 13. Related concepts
- **BERT**: The encoder-only counterpart.
- **RLHF**: The alignment technique used to create ChatGPT from GPT.

## 14. When it breaks / Edge cases
- Catastrophic hallucination: GPT models generate fluent, confident text that is factually wrong because they predict plausible tokens, not truthful ones.

## 15. Comparison with alternative approaches
- **vs BERT:** BERT is better at understanding (classification, extraction). GPT is better at generation. GPT at instruction-following scale (ChatGPT) has largely superseded BERT-based systems.

---
*Where this shows up in ML:*
ChatGPT, GPT-4, Claude, Gemini, Llama 3, Mistral — all are GPT-style decoder-only Transformers.
