# Temperature in Sampling

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
