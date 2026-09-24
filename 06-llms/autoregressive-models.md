# Autoregressive Generation

## 1. Definition
Autoregressive generation is the process where a model generates a sequence one token at a time, using its own previously generated tokens as input for predicting the next token.

## 2. Intuition
Writing a sentence word by word. You write "The", then based on "The", you decide to write "cat", then based on "The cat", you decide to write "sat". The model feeds its output back into its input in a loop.

## 3. Why it exists
While training can process all tokens in parallel (because we know the ground truth future), inference cannot. To generate novel text, we must wait to see what token is sampled at step $t$ before we can compute the probabilities for step $t+1$.

## 4. Mechanics
1. Feed the prompt tokens into the model.
2. Get the logits for the final token position.
3. Apply a sampling strategy (Greedy, Temperature, Top-K, Top-P) to select the next token.
4. Append the selected token to the input sequence.
5. Repeat until an End-Of-Sequence (EOS) token is generated or max length is reached.
- **KV-Cache:** To avoid recomputing the attention over the entire growing sequence at every step, we cache the Key and Value vectors of past tokens.

## 5. Complexity (Time & Space)
- **Time:** $O(N \cdot d^2 + N^2 \cdot d)$ without KV-cache. $O(N \cdot d^2 + N \cdot d)$ per step with KV-cache. Generating $T$ tokens takes time proportional to $T$.
- **Space:** KV-cache grows linearly with sequence length: $O(N \cdot L \cdot d)$ where $L$ is number of layers.

## 6. Tiny worked example
Prompt: "I am"
Step 1: Input "I am" -> Output "happy"
Step 2: Input "I am happy" -> Output "to"
Step 3: Input "I am happy to" -> Output "help"
Final: "I am happy to help"

## 7. Code (Python)
```python
import torch

def generate_autoregressive(model, input_ids, max_new_tokens):
    for _ in range(max_new_tokens):
        # Forward pass (simplified, ignoring KV cache for clarity)
        with torch.no_grad():
            outputs = model(input_ids)
            next_token_logits = outputs[:, -1, :] # Logits of last token
            
        # Greedy decoding (argmax)
        next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
        
        # Append to sequence
        input_ids = torch.cat([input_ids, next_token], dim=-1)
        
        if next_token.item() == EOS_TOKEN_ID:
            break
            
    return input_ids
```

## 8. Common mistakes
- Thinking LLM inference is $O(1)$ time for a whole sentence. Generation is strictly sequential; generating 100 tokens requires 100 sequential forward passes.
- Implementing generation without a KV-cache, resulting in incredibly slow $O(N^2)$ inference times.

## 9. 30-second interview answer
"Autoregressive generation is how LLMs produce text during inference. They predict the next token, append it to the context, and repeat the process. Because this requires a full model forward pass for every single token, it is computationally bound. To make this efficient, we use a KV-cache to store past activations, avoiding redundant computations for previous tokens."

## 10. 2-minute interview answer
"Autoregressive generation means the model's output depends on its previous outputs. In decoder-only Transformers, inference is a sequential loop: feed the context, sample a token from the final logits, append it, and repeat. The major bottleneck is the Attention mechanism. Naively, computing step $t$ requires recomputing attention for all $1 \dots t-1$ tokens. We solve this with the KV-cache: we save the Key and Value vectors for all past tokens. At step $t$, we only compute the Query, Key, and Value for the single new token, and attend it against the cached Keys and Values. This reduces the time complexity per token from $O(N^2)$ to $O(N)$, turning generation from a compute-bound operation (matrix-matrix multiplication) into a memory-bandwidth-bound operation (matrix-vector multiplication reading the massive KV-cache from GPU memory)."

## 11. Follow-ups
- "Why is LLM inference typically memory-bandwidth bound?" (During generation with a KV-cache, the operation is a matrix-vector product. We have to load the entire model weights and KV-cache from HBM to SRAM for every single generated token, which takes more time than the actual math).

## 12. Deeper questions
- "What is speculative decoding?" (A technique to speed up autoregressive generation. A smaller, faster 'draft' model autoregressively generates $K$ tokens. The large target model evaluates all $K$ tokens in parallel in a single forward pass. If the large model agrees, we accept them, generating multiple tokens per forward pass).

## 13. Related concepts
- **KV-Cache**: Essential for efficient autoregressive generation.
- **Teacher Forcing**: The training technique that bypasses autoregressive loops.

## 14. When it breaks / Edge cases
- Long generation causes the KV-cache to exceed available GPU memory, leading to Out-Of-Memory (OOM) errors.

## 15. Comparison with alternative approaches
- **Autoregressive vs Non-Autoregressive:** Non-autoregressive models attempt to generate all tokens in parallel (e.g., in some machine translation models), vastly faster but currently inferior in quality for open-ended text.

---
*Where this shows up in ML:*
Every time ChatGPT types out an answer word-by-word.
