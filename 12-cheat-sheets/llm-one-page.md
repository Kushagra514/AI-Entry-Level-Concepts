# LLM One-Page Revision

## 1. Pretraining (The Engine)
- **Goal:** Learn general language and facts.
- **Objective:** Causal Language Modeling (predict next token). $\mathcal{L} = -\sum \log P(x_t|x_{<t})$.
- **Data:** Trillions of tokens of raw web text. Requires aggressive deduplication and quality filtering.
- **Compute:** Months on GPU clusters.
- **Result:** A Base Model. It is not an assistant; it is a document completer.

## 2. Supervised Fine-Tuning / Instruction Tuning (SFT)
- **Goal:** Teach the model to follow instructions and answer questions format.
- **Data:** Tens of thousands of high-quality (Prompt, Response) pairs written by humans.
- **Result:** An Instruction-Tuned model (e.g., Llama-3-Instruct).

## 3. Alignment (RLHF / DPO)
- **Goal:** Make the model safe, helpful, and polite. Stop it from generating toxic or dangerous text.
- **RLHF:** Train a Reward Model on human preferences (A is better than B). Use PPO to optimize the LLM to maximize the reward.
- **DPO (Direct Preference Optimization):** Skip the reward model and PPO. Directly optimize the LLM on preference pairs mathematically. Much more stable.

## Inference Concepts
- **KV Cache:** Cache the Keys and Values of past tokens so we don't recompute them for every new token generated. Takes linear memory $O(N)$ and is a massive bottleneck.
- **Temperature:** Scales logits before softmax. $T=0$ (greedy, deterministic), $T=1$ (normal), $T>1$ (flatter distribution, more random).
- **Top-K / Top-P (Nucleus):** Top-K only samples from the $K$ most likely tokens. Top-P samples from the smallest set of tokens whose probabilities sum to $P$.

## Interview Traps
- *Does pretraining embed rules of logic?* No, it learns statistical probabilities over tokens. Reasoning is an emergent property of modeling extremely complex conditional probabilities.
- *Is instruction tuning for adding new knowledge?* No. Fine-tuning/SFT is notoriously bad at memorizing new facts. Use RAG to add knowledge.
