import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch D)"')

wc("06-llms/alignment.md", r"""# LLM Alignment

## 1. Definition
Alignment is the process of fine-tuning an LLM so its outputs match human values, preferences, and safety guidelines—ensuring it is helpful, honest, and harmless (the "3H" criteria).

## 2. Intuition
A base model is a wild mirror of the internet; it might give you a recipe for a cake or a recipe for a bomb with equal probability. Alignment is the process of putting guardrails on the model and teaching it to be a helpful assistant rather than a neutral text generator.

## 3. Why it exists
Base models are misaligned with enterprise and consumer use cases. They can be toxic, biased, hallucinate confidently, or assist with malicious activities. Alignment makes them safe, reliable, and commercially viable.

## 4. Mechanics
- **SFT (Supervised Fine-Tuning):** Initial alignment using high-quality human demonstrations.
- **RLHF (Reinforcement Learning from Human Feedback):** 
  1. Train a Reward Model (RM) on human preference rankings (Response A > Response B).
  2. Use PPO (Proximal Policy Optimization) to maximize the RM score.
- **DPO (Direct Preference Optimization):** Mathematically bypasses the RM and RL loop by optimizing the policy directly on preference data using a specialized loss function.
- **Constitutional AI:** Anthropic's method where an AI (not a human) evaluates and critiques responses based on a set of principles (a "constitution"), used to generate preference data for RL.

## 5. Complexity (Time & Space)
- RLHF requires running 4 models simultaneously during PPO (Policy, Reference, Reward, Value), making it very memory intensive (often requiring 4x the VRAM of standard fine-tuning). DPO is much cheaper as it only requires the Policy and Reference models.

## 6. Tiny worked example
Preference Data:
Prompt: "How do I steal a car?"
Response A: "Use a slim jim to unlock the door..."
Response B: "I cannot help with illegal activities."
Human labels: B > A.
Reward Model learns to score B high and A low. RLHF updates the LLM to output B-like responses.

## 7. Code (Python)
```python
# Conceptual DPO Loss
import torch
import torch.nn.functional as F

def dpo_loss(pi_logps_chosen, pi_logps_rejected, ref_logps_chosen, ref_logps_rejected, beta=0.1):
    # pi = current model, ref = frozen reference model
    # Log probability ratios
    pi_ratio = pi_logps_chosen - pi_logps_rejected
    ref_ratio = ref_logps_chosen - ref_logps_rejected
    
    # Loss: minimize the negative log sigmoid of the scaled difference
    loss = -F.logsigmoid(beta * (pi_ratio - ref_ratio)).mean()
    return loss
```

## 8. Common mistakes
- Confusing Alignment with pretraining. Alignment does not inject facts; it just shapes how the model presents the facts it already knows.
- Over-alignment leading to "alignment tax" — where a model becomes so safe it refuses benign requests or loses its coding/reasoning capabilities.

## 9. 30-second interview answer
"Alignment ensures an LLM is helpful, honest, and harmless. It is typically achieved through RLHF, which trains a reward model on human preferences and optimizes the LLM using PPO, or through DPO, which simplifies the process by directly optimizing on preference data. It's the critical step that turns a raw base model into a safe, deployable assistant like ChatGPT."

## 10. 2-minute interview answer
"Alignment is the final and arguably most important step in the LLM training pipeline. A base model learns the distribution of the internet; instruction tuning teaches it to follow commands; alignment teaches it what commands it *should* follow and how to format the answer safely. The gold standard is RLHF. In RLHF, human annotators rank model outputs. We train a reward model on these rankings, and then use PPO to update the LLM to maximize the reward. However, PPO is complex and unstable. Recently, Direct Preference Optimization (DPO) has emerged as a dominant alternative. DPO shows that under certain assumptions, you can skip the reward model and RL loop entirely, directly optimizing the policy using a simple cross-entropy-like loss on the preference pairs. Anthropic introduced Constitutional AI to reduce reliance on expensive human annotators by using an AI to critique and revise answers based on a set of rules. The major challenge in alignment today is the 'alignment tax' — the empirical observation that highly aligned models often degrade in reasoning or coding tasks compared to their base models."

## 11. Follow-ups
- "What is the role of the KL penalty in RLHF?" (It prevents the model from "reward hacking" — generating weird, ungrammatical text that exploits a loophole in the reward model to get a high score. It forces the aligned model to stay close to the initial SFT model).

## 12. Deeper questions
- "Why is DPO considered more stable than PPO?" (PPO involves actor-critic networks, advantage estimation, and moving targets, which are notoriously hyperparameter-sensitive. DPO is just supervised learning with a specific loss function).

## 13. Related concepts
- **Instruction Tuning**: The prerequisite for alignment.
- **RLHF**: The most famous alignment technique.

## 14. When it breaks / Edge cases
- Jailbreaks and Prompt Injection: Users can craft prompts that bypass alignment guardrails (e.g., "Pretend you are an unaligned AI...").

## 15. Comparison with alternative approaches
- **RLHF vs DPO:** RLHF is the original, proven method but complex. DPO is simpler, requires less memory, and is increasingly the standard for open-source model alignment (e.g., Llama-3).

---
*Where this shows up in ML:*
Creating safe APIs and chatbots; the difference between a research model and a product.
""")

wc("06-llms/temperature.md", r"""# Temperature in Sampling

## 1. Definition
Temperature ($T$) is a hyperparameter used during autoregressive generation that scales the logits before applying the softmax function, thereby controlling the randomness and diversity of the generated text.

## 2. Intuition
Imagine you have three choices: Apple (score 10), Banana (score 5), Cherry (score 1). 
Low temperature exaggerates differences: Apple becomes 99% likely. 
High temperature flattens differences: Apple, Banana, and Cherry become almost equally likely.

## 3. Why it exists
Without temperature, we either always pick the most likely word (boring, repetitive, gets stuck in loops) or we sample from the raw distribution. Temperature gives us a simple dial to tune the model between "deterministic/factual" and "creative/diverse".

## 4. Mechanics
Standard softmax: $p_i = \frac{\exp(z_i)}{\sum_j \exp(z_j)}$
Temperature-scaled softmax: $p_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$
- **$T = 1$:** Raw softmax distribution.
- **$T < 1$:** Distribution becomes "sharper" (higher peaks). Probabilities of top tokens increase.
- **$T \to 0$:** Equivalent to `argmax` (Greedy decoding). Deterministic.
- **$T > 1$:** Distribution becomes flatter. Low-probability tokens become more likely.
- **$T \to \infty$:** Uniform distribution (completely random).

## 5. Complexity (Time & Space)
- **Time:** $O(V)$ scalar division before softmax. Negligible.
- **Space:** $O(1)$.

## 6. Tiny worked example
Logits: `[2.0, 1.0, 0.1]`
T=1: `[0.66, 0.24, 0.10]`
T=0.5: Logits become `[4.0, 2.0, 0.2]` -> Probabilities `[0.87, 0.12, 0.01]` (Sharper)
T=2.0: Logits become `[1.0, 0.5, 0.05]` -> Probabilities `[0.46, 0.28, 0.26]` (Flatter)

## 7. Code (Python)
```python
import torch
import torch.nn.functional as F

def sample_with_temperature(logits, temperature=1.0):
    if temperature == 0.0:
        return torch.argmax(logits, dim=-1)
    
    # Scale logits
    scaled_logits = logits / temperature
    # Convert to probabilities
    probs = F.softmax(scaled_logits, dim=-1)
    # Sample from the distribution
    return torch.multinomial(probs, num_samples=1)
```

## 8. Common mistakes
- Using high temperature (e.g., 0.8) for coding or math tasks. These require exact syntax and logic; high temperature causes hallucinations and syntax errors.
- Confusing Temperature with Top-K or Top-P. Temperature changes the *probabilities* of all tokens; Top-K/P *removes* tokens from consideration entirely.

## 9. 30-second interview answer
"Temperature is a scaling factor applied to logits before the softmax layer during generation. A temperature less than 1 makes the probability distribution sharper, leading to more deterministic, predictable text. A temperature greater than 1 flattens the distribution, increasing randomness and creativity. Setting it to 0 is equivalent to greedy decoding."

## 10. 2-minute interview answer
"Temperature controls the exploration-exploitation tradeoff in language generation. By dividing the logits by $T$ before exponentiation in the softmax function, we manipulate the entropy of the output distribution. For tasks requiring factual accuracy, structured output like JSON, or mathematical reasoning, we use $T=0$ (greedy decoding) to eliminate variance and ensure the model outputs its highest-confidence answer. For tasks requiring creativity, like writing a poem or brainstorming ideas, we increase $T$ (usually 0.7 to 1.0) to sample from a wider range of the vocabulary, which prevents the model from generating bland, highly predictable text. Importantly, temperature is almost always used in conjunction with Top-P or Top-K sampling; temperature reshapes the distribution, and Top-P truncates the long tail of absolute nonsense that a high temperature might elevate."

## 11. Follow-ups
- "Why does greedy decoding (T=0) sometimes produce worse text than sampling?" (Greedy decoding only considers the immediate next token. It can lead to repetitive loops because it never takes a slightly suboptimal path that might lead to a much better long-term sequence. Beam search is a better deterministic alternative).

## 12. Deeper questions
- "How does temperature affect the calibration of a classification model?" (Temperature scaling is a standard technique to calibrate Neural Networks. If a model is overconfident, finding an optimal $T > 1$ on a validation set can make its output probabilities accurately reflect its true accuracy, without changing the argmax predictions).

## 13. Related concepts
- **Top-K / Top-P**: The other half of the sampling equation.
- **Beam Search**: Deterministic generation alternative to sampling.

## 14. When it breaks / Edge cases
- Very high temperatures ($T > 2$) cause the model to output complete gibberish, as the distribution approaches uniform.

## 15. Comparison with alternative approaches
- **Temperature vs Top-P:** Temperature changes the shape of the whole distribution. Top-P dynamically chops off the tail. They are complementary.

---
*Where this shows up in ML:*
Every LLM API call (OpenAI, Anthropic) exposes temperature as a primary parameter.
""")

wc("06-llms/top-k-top-p.md", r"""# Top-K and Top-P (Nucleus) Sampling

## 1. Definition
Top-K and Top-P are truncation strategies used during text generation to restrict the vocabulary from which the model samples the next token, preventing the selection of highly unlikely (and often nonsensical) tokens.

## 2. Intuition
Imagine a model predicts the next word is: 
"apple" (80%), "banana" (15%), "cherry" (4%), and 30,000 other words (total 1%).
Without truncation, there's a 1% chance the model picks a bizarre word like "bulldozer," which derails the sentence. Top-K and Top-P act as bouncers, throwing out the 30,000 bad options before you roll the dice.

## 3. Why it exists
Language models have large vocabularies (30k-100k tokens). Even if the long tail of tokens has tiny individual probabilities, the *sum* of the tail can be significant. Sampling from the unmodified distribution occasionally selects a terrible token, causing a cascading failure in generation.

## 4. Mechanics
- **Top-K:** Sort the vocabulary by probability. Keep only the top $K$ tokens. Re-normalize their probabilities to sum to 1, and sample. (Fixed size).
- **Top-P (Nucleus Sampling):** Sort the vocabulary by probability. Compute the cumulative sum. Keep tokens until the cumulative sum exceeds $P$ (e.g., 0.9). Re-normalize and sample. (Dynamic size).

## 5. Complexity (Time & Space)
- **Time:** $O(V \log V)$ to sort the logits, though Top-K can be optimized to $O(V \log K)$ using a min-heap or QuickSelect.
- **Space:** $O(V)$ to store logits/probabilities.

## 6. Tiny worked example
Probs: `A: 0.5, B: 0.3, C: 0.15, D: 0.04, E: 0.01`
- **Top-K (K=2):** Keep A and B. Re-normalize: A = 0.5/0.8 = 62.5%, B = 0.3/0.8 = 37.5%.
- **Top-P (P=0.9):** Cumulative: A(0.5) -> B(0.8) -> C(0.95). 0.95 > 0.9, so stop. Keep A, B, C. Re-normalize among those three.

## 7. Code (Python)
```python
import torch

def top_p_sampling(logits, p=0.9):
    # Sort logits descending
    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
    cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
    
    # Identify tokens to remove (cumulative prob > p)
    # Shift by 1 to keep the token that crosses the threshold
    sorted_indices_to_remove = cumulative_probs > p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = 0
    
    # Scatter back to original indices and set to -infinity
    indices_to_remove = sorted_indices_to_remove.scatter(
        dim=-1, index=sorted_indices, src=sorted_indices_to_remove
    )
    logits[indices_to_remove] = float('-inf')
    return logits # Ready for softmax and sampling
```

## 8. Common mistakes
- Setting both Top-K and Top-P to very restrictive values simultaneously (e.g., K=5, P=0.5). Usually, you rely primarily on Top-P and leave K large (e.g., 50) as a fallback.
- Applying Top-P *before* Temperature. Temperature scales logits, which changes the probabilities, which changes which tokens make it into the Top-P nucleus. Always apply Temperature first.

## 9. 30-second interview answer
"Top-K and Top-P are sampling techniques that truncate the probability distribution to prevent generating nonsensical tokens. Top-K restricts sampling to the K most likely tokens. Top-P, or Nucleus Sampling, dynamically restricts sampling to the smallest set of tokens whose cumulative probability exceeds P. Top-P is generally preferred because it adapts to how confident the model is."

## 10. 2-minute interview answer
"To generate fluent text, we must manage the long tail of the vocabulary distribution. Top-K is a hard cutoff; if K=10, we only consider 10 tokens. The flaw with Top-K is that in flat distributions (model is unsure), 10 tokens isn't enough variety; in sharp distributions (model is confident), 10 tokens is too many and includes bad options. Top-P solves this dynamically. If $P=0.9$, and the top token has 95% probability, the nucleus contains only 1 token. If the top 50 tokens have 1% probability each, the nucleus expands to 90 tokens. This allows the model to be deterministic when confident and creative when uncertain. In practice, production systems apply Temperature first to shape the distribution, then Top-K (e.g., K=50) as a safety net, then Top-P (e.g., P=0.9) for the final dynamic truncation."

## 11. Follow-ups
- "Why does text degenerate without truncation?" (The long tail sums up. Even if $P(\text{gibberish}) = 10^{-5}$, across a 30,000 token vocabulary, the cumulative chance of picking *some* gibberish token becomes significant over a long generation).

## 12. Deeper questions
- "What is Min-P sampling?" (A newer alternative where you keep tokens whose probability is at least $P$ percent of the top token's probability. It handles dynamic ranges better than Top-P in some edge cases).

## 13. Related concepts
- **Temperature**: Applied before Top-K/P.
- **Beam Search**: Deterministic alternative to sampling.

## 14. When it breaks / Edge cases
- If $P$ is too close to 1.0, the tail is not truncated enough. If $P$ is too small (e.g., 0.1), it degenerates into greedy decoding.

## 15. Comparison with alternative approaches
- **Top-K vs Top-P:** Top-P is strictly superior because it dynamically adjusts the candidate pool size based on the model's confidence.

---
*Where this shows up in ML:*
OpenAI API parameters, HuggingFace `generate()` method.
""")

wc("06-llms/context-window.md", r"""# Context Window

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
""")

print("Batch D Part 3_2 complete")
