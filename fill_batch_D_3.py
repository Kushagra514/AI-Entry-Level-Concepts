import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch D)"')

# ---- 06-llms ----
wc("06-llms/language-models.md", r"""# Language Models

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
""")

wc("06-llms/pretraining.md", r"""# LLM Pretraining

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
""")

wc("06-llms/next-token-prediction.md", r"""# Next Token Prediction (Causal Language Modeling)

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
""")

wc("06-llms/autoregressive-models.md", r"""# Autoregressive Generation

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
""")

wc("06-llms/fine-tuning.md", r"""# Fine-Tuning LLMs

## 1. Definition
Fine-tuning is the process of taking a pretrained foundation model and training it further on a smaller, task-specific dataset to adapt its behavior, format, or domain knowledge.

## 2. Intuition
Pretraining teaches the model "how to speak English and understand the world" (getting a college degree). Fine-tuning teaches it "how to be a polite customer service agent" (on-the-job training).

## 3. Why it exists
Pretrained models only want to complete text (e.g., if you prompt "What is the capital of France?", it might output "What is the capital of Germany?"). Fine-tuning aligns the model to follow instructions, answer questions, or perform specific formatting (like outputting valid JSON).

## 4. Mechanics
- **Full Fine-Tuning:** Update all parameters of the model. Requires massive GPU memory (e.g., 8x A100s for a 7B model) to store optimizer states for all weights.
- **PEFT (Parameter-Efficient Fine-Tuning):** Freeze the base model and train a small number of extra parameters.
  - **LoRA (Low-Rank Adaptation):** Injects trainable low-rank matrices into the attention layers.
  - **QLoRA:** Quantizes the base model to 4-bit, training LoRA adapters on top (fits a 7B model on a single 24GB consumer GPU).
- **Dataset:** Usually Supervised Fine-Tuning (SFT) format: `{"prompt": "...", "response": "..."}`. High quality > high quantity (1,000 great examples beats 100,000 mediocre ones).

## 5. Complexity (Time & Space)
- **Full FT Space:** 4-6x the model parameters (Model + Gradients + Adam states).
- **LoRA Space:** ~1x model parameters (frozen) + tiny optimizer state for adapters.

## 6. Tiny worked example
Goal: Make model output JSON.
Dataset: 
`[{"instruction": "Extract names", "input": "Bob and Alice", "output": "{\"names\": [\"Bob\", \"Alice\"]}"}]`
Train with CLM loss only on the `output` portion (masking the prompt from the loss).

## 7. Code (Python)
```python
# Using HuggingFace PEFT (LoRA)
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b")

# Configure LoRA: rank 8, target attention projection layers
config = LoraConfig(
    r=8, 
    lora_alpha=32, 
    target_modules=["q_proj", "v_proj"], 
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Wraps model: freezes base weights, adds trainable LoRA weights
peft_model = get_peft_model(model, config)
peft_model.print_trainable_parameters() 
# "trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%"
```

## 8. Common mistakes
- Training on the prompt. Loss should only be calculated on the model's *response*, not the user's instruction.
- Using fine-tuning to inject new factual knowledge. Fine-tuning is prone to catastrophic forgetting and hallucinations. RAG is better for facts; fine-tuning is for *behavior/style*.

## 9. 30-second interview answer
"Fine-tuning adapts a pretrained model to specific tasks. Full fine-tuning updates all weights but is highly resource-intensive. Parameter-Efficient Fine-Tuning (PEFT) methods like LoRA freeze the base model and train small adapter layers, allowing fine-tuning on consumer hardware. We use fine-tuning to teach the model how to behave (e.g., instruction following) rather than to teach it new facts."

## 10. 2-minute interview answer
"Fine-tuning bridges the gap between a raw predictive model and a useful application. While full fine-tuning updates the entire parameter space, it requires extensive VRAM for optimizer states. Therefore, the industry standard for custom adaptation is LoRA (Low-Rank Adaptation). LoRA freezes the pretrained weights and injects trainable rank-decomposition matrices into each layer. This reduces trainable parameters by 99% while achieving near-parity with full fine-tuning. The most critical aspect of fine-tuning is data quality; a few thousand highly curated examples (LIMA paper) can outperform millions of low-quality examples. We generally follow the rule: use RAG to give the model new knowledge, and use fine-tuning to teach the model a new format, tone, or specific reasoning pattern."

## 11. Follow-ups
- "What is catastrophic forgetting?" (When fine-tuning on a narrow dataset, the model's weights change and it forgets the broad general knowledge it learned during pretraining. LoRA helps mitigate this).

## 12. Deeper questions
- "How does QLoRA work?" (It loads the base model in 4-bit NormalFloat precision. During the backward pass, activations are dequantized to 16-bit to compute gradients for the 16-bit LoRA adapters. This drastically reduces memory footprint).

## 13. Related concepts
- **Instruction Tuning**: A specific type of supervised fine-tuning.
- **RAG**: The alternative/complement to fine-tuning for knowledge injection.

## 14. When it breaks / Edge cases
- Overfitting occurs very quickly on small fine-tuning datasets, causing the model to lose its conversational abilities.

## 15. Comparison with alternative approaches
- **Fine-Tuning vs Prompt Engineering (Few-Shot):** Few-shot is fast and requires no training, but consumes context window. Fine-tuning bakes the behavior in, saving tokens and handling more complex pattern matching.

---
*Where this shows up in ML:*
Adapting Llama-3 or Mistral for specific enterprise use-cases (code generation, medical Q&A, JSON extraction).
""")

wc("06-llms/instruction-tuning.md", r"""# Instruction Tuning

## 1. Definition
Instruction tuning is a specialized form of Supervised Fine-Tuning (SFT) where a pretrained language model is trained on datasets consisting of (Instruction, Response) pairs, teaching it to act as an assistant rather than just a text completer.

## 2. Intuition
A base model acts like a parrot that finishes your sentences. If you say "Translate to French: Hello", a base model might reply "Translate to Spanish: Hola". Instruction tuning teaches it that "Translate to French" is a command to be executed, resulting in "Bonjour".

## 3. Why it exists
Base models are difficult for end-users to interact with because they require complex "prompt engineering" to trick the model into completing the text in a useful way. Instruction tuning aligns the model's behavior with human expectations of an AI assistant.

## 4. Mechanics
- **Dataset format:** Usually structured with roles. E.g., User: "Write a poem." Assistant: "Roses are red..."
- **Chat Templates:** Special control tokens are introduced to format the conversation (e.g., `<|im_start|>user\n...<|im_end|>`).
- **Loss Masking:** During training, cross-entropy loss is calculated *only* on the tokens belonging to the Assistant's response. The User instruction tokens are ignored in the loss calculation.
- **FLAN (Fine-tuned LAnguage Net):** Google's early approach of taking thousands of traditional NLP datasets and converting them into instruction templates.

## 5. Complexity (Time & Space)
- Same as Supervised Fine-Tuning. Requires significantly less compute than pretraining (often just hours/days on a small cluster).

## 6. Tiny worked example
Raw Training Data:
`Instruction: Summarize this text: [TEXT]. Response: [SUMMARY]`

Using a Chat Template for Llama-3:
`<|start_header_id|>user<|end_header_id|>\nSummarize...<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n[SUMMARY]<|eot_id|>`

## 7. Code (Python)
```python
# Conceptual loss masking for instruction tuning
def compute_loss(model, input_ids, labels):
    # input_ids: [User_Token1, User_Token2, Asst_Token1, Asst_Token2]
    # labels:    [-100,       -100,        Asst_Token1, Asst_Token2]
    # PyTorch ignores index -100 in CrossEntropyLoss
    
    outputs = model(input_ids)
    logits = outputs.logits[:, :-1, :] # Shift for next token
    targets = labels[:, 1:]
    
    loss_fct = torch.nn.CrossEntropyLoss(ignore_index=-100)
    loss = loss_fct(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
    return loss
```

## 8. Common mistakes
- Training the model to predict the prompt. If you don't mask the prompt tokens with `-100`, the model learns to generate user questions, which wastes capacity and can cause weird generation artifacts.
- Mixing chat templates. If you fine-tune a model using the ChatML template, but inference uses the Llama-3 template, performance will degrade severely.

## 9. 30-second interview answer
"Instruction tuning is a stage of Supervised Fine-Tuning where a base model is trained on instruction-response pairs. It transforms a model from a generic text completer into an assistant that follows commands. Special chat template tokens are used to separate roles, and loss is only calculated on the assistant's response."

## 10. 2-minute interview answer
"Instruction tuning bridges the gap between next-token prediction and useful AI interaction. We take a pretrained base model and fine-tune it on tens of thousands of high-quality conversational turns. A critical implementation detail is the chat template: we wrap the user and assistant text in special control tokens (like `<|user|>` and `<|assistant|>`). This allows the model to differentiate between instructions it must follow and text it is generating. During the backward pass, we apply loss masking: the cross-entropy loss is computed only on the assistant's response tokens. Recent research, like the LIMA paper (Less Is More for Alignment), shows that instruction tuning doesn't inject new knowledge; rather, it just unlocks the knowledge already learned during pretraining, meaning 1,000 highly-curated examples often outperform 100,000 mediocre ones."

## 11. Follow-ups
- "What happens after instruction tuning?" (Usually RLHF or DPO to align the model further with human preferences, reduce toxicity, and improve helpfulness).

## 12. Deeper questions
- "How do you generate high-quality instruction tuning data without human annotators?" (Self-Instruct pipelines: use a powerful model like GPT-4 to generate complex instructions and responses, then train a smaller model on that synthetic data. This is how Alpaca and many open-source models were created).

## 13. Related concepts
- **RLHF**: The alignment step that usually follows instruction tuning.
- **System Prompts**: Enabled by the chat templates learned during instruction tuning.

## 14. When it breaks / Edge cases
- "Sycophancy" - instruction-tuned models tend to agree with the user's premise even when it is factually incorrect, because human annotators tend to rate polite, agreeable responses highly.

## 15. Comparison with alternative approaches
- **Instruction Tuning vs Few-Shot Prompting:** Few-shot works on base models but requires context space. Instruction-tuned models have zero-shot capability for commands.

---
*Where this shows up in ML:*
The difference between `Llama-3-8B` (base) and `Llama-3-8B-Instruct`.
""")

print("Batch D Part 3 complete")
