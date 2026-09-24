# Language Models

## 1. Definition
A Language Model computes the probability of a sequence of words (or tokens) $P(w_1, w_2, ..., w_n)$ or the probability of the next word given the history $P(w_n | w_1, ..., w_{n-1})$. 

## 2. Intuition
Imagine a smartphone keyboard's autocomplete. If you type "I am going to the", the model predicts "store" is more likely than "moon". It does this by understanding the statistical patterns of language from vast amounts of text.

## 3. Why it exists
Language Models are the fundamental building blocks of NLP. They allow machines to generate fluent text, assess the fluency of text (useful for translation and speech recognition), and, as recently discovered, perform complex reasoning by predicting the most probable continuation of a prompt.

## 4. Mechanics
- **n-gram Models:** Calculate probabilities based on the frequency of word sequences of length $n$ in a corpus. Uses Markov assumption (next word depends only on previous $n-1$ words). Fails on long-range dependencies and out-of-vocabulary words.
- **Neural LMs (RNNs/LSTMs):** Use hidden states to summarize the entire history. Better at long-term context but sequential processing is slow.
- **Transformer LMs:** Use self-attention to process all past tokens simultaneously. Extremely parallelizable and capable of capturing very long-range dependencies. The current state-of-the-art.

## 5. Complexity (Time & Space)
- **Time:** $O(V)$ at the final layer to output probabilities over vocabulary $V$. Transformer attention is $O(N^2)$ for sequence length $N$.
- **Space:** $O(V \times d)$ for embedding matrix.

## 6. Tiny worked example
Bigram model (n=2). Sentence: "the cat sat".
$P(\text{"the cat sat"}) = P(\text{"the"}) \times P(\text{"cat" | "the"}) \times P(\text{"sat" | "cat"})$.
If "cat" follows "the" in 10% of cases, $P(\text{"cat" | "the"}) = 0.1$.

## 7. Code (Python)
```python
import math

# Simple bigram probability calculation
corpus = ["the cat sat", "the dog barked"]
# Assume we counted frequencies
prob_cat_given_the = 1 / 2  # "the" is followed by "cat" once, "dog" once
prob_sat_given_cat = 1 / 1

p_sequence = (2/6) * prob_cat_given_the * prob_sat_given_cat
print(f"P(sequence) = {p_sequence:.4f}")
```

## 8. Common mistakes
- Confusing a Language Model (generates text based on probability) with a text classifier (assigns a single label to text).
- Assuming n-gram models are entirely obsolete; they are still used in constrained environments or as baselines.

## 9. 30-second interview answer
"A Language Model assigns probabilities to sequences of words. While traditional n-gram models rely on local frequency counts and the Markov assumption, modern Neural LMs, especially Transformers, use self-attention to model long-range dependencies and predict the next token given the entire preceding context."

## 10. 2-minute interview answer
"Language modeling is the core task of NLP, defined as predicting the probability distribution of the next token given previous tokens. Historically, n-gram models dominated, but they suffer from sparsity and cannot capture long-range dependencies. Recurrent Neural Networks solved the context length issue but couldn't be trained in parallel. Transformers solved both by using self-attention over the entire sequence. The standard metric for LMs is Perplexity, which exponentiates the cross-entropy loss; a lower perplexity means the model is less surprised by unseen text. Modern Large Language Models (LLMs) like GPT-4 are essentially massive Transformer-based language models trained on web-scale data, which emergently learn world knowledge and reasoning just by optimizing the next-token prediction objective."

## 11. Follow-ups
- "What is Perplexity?" (It is $e^{\text{CrossEntropyLoss}}$. It represents the effective vocabulary size the model is guessing between. Lower is better.)

## 12. Deeper questions
- "How does smoothing (like Laplace smoothing) help n-gram models?" (It prevents zero probabilities for unseen n-grams by adding a small count to all possible n-grams).

## 13. Related concepts
- **Transformers**: The architecture behind modern LMs.
- **Next-Token Prediction**: The training objective for generative LMs.

## 14. When it breaks / Edge cases
- Neural LMs can "hallucinate" by predicting highly probable but factually incorrect sequences.

## 15. Comparison with alternative approaches
- **N-grams vs Transformers:** N-grams are fast and simple but limited in context. Transformers capture deep context but require massive compute.

---
*Where this shows up in ML:*
Foundation of all generative AI, autocomplete, machine translation scoring.
