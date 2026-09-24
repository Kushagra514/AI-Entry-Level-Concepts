import os

def write_and_commit(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch B)"')

files = {}

files["07-rag/embeddings.md"] = """# Embeddings

## 1. Definition
Embeddings are dense, low-dimensional continuous vector representations of discrete data (like words, sentences, or images) that capture semantic meaning.

## 2. Intuition
Imagine mapping words to a 3D room. You put "King" in the back-right corner. You put "Man" next to it. You put "Apple" on the opposite side of the room. By looking at the distance between coordinates, the computer mathematically understands that a King is related to a Man, but completely unrelated to an Apple.

## 3. Why it exists
Computers only understand numbers. Naive text encoding (One-Hot Encoding) creates massive, sparse vectors (e.g., $1 \times 50,000$ for a vocabulary) where every word is mathematically equidistant from every other word, destroying semantic relationships. Embeddings compress this into dense vectors (e.g., $1 \times 768$) where geometric distance equals semantic similarity.

## 4. Mechanics
- A model (like Word2Vec, BERT, or text-embedding-ada-002) is trained on massive text corpora to predict missing words.
- The internal weights of this model learn to represent words/sentences as vectors.
- After training, the model acts as a lookup table (for words) or a forward-pass function (for sentences), converting input text into an array of floats.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(L \times d^2)$ for generating contextual embeddings (like Transformers), where $L$ is sequence length and $d$ is embedding dimension.
- **Space Complexity:** $O(V \times d)$ to store the embedding matrix for a vocabulary of size $V$.

## 6. Tiny worked example
One-hot: `Apple = [1,0,0]`, `Orange = [0,1,0]`. Dot product (similarity) = 0.
Embedding: `Apple = [0.9, 0.1]`, `Orange = [0.8, 0.2]`. Dot product > 0 (high similarity).
Vector arithmetic: $Embedding(King) - Embedding(Man) + Embedding(Woman) \\approx Embedding(Queen)$.

## 7. Code (Python, with type hints)
```python
import torch
import torch.nn as nn

# A simple lookup table for 10,000 words, embedding them into 768 dimensions
vocab_size = 10000
embed_dim = 768
embedding_layer = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embed_dim)

# Input: tensor of word IDs (e.g., Batch=2, Seq_len=5)
word_ids = torch.randint(0, vocab_size, (2, 5))
# Output: (2, 5, 768)
dense_vectors = embedding_layer(word_ids) 
```

## 8. Common mistakes
- Confusing Static embeddings (Word2Vec: "bank" always has one vector) with Contextual embeddings (BERT: "river bank" and "bank account" have different vectors).
- Not normalizing embeddings before using Dot Product for similarity (Cosine Similarity inherently normalizes).

## 9. 30-second interview answer
"Embeddings are dense vector representations of discrete data that capture semantic meaning. Instead of sparse one-hot vectors, embeddings project data into a continuous space where geometric distance represents semantic similarity, powering NLP tasks and RAG pipelines."

## 10. 2-minute interview answer
"Embeddings are the bridge between human language and deep learning math. Because one-hot encoding suffers from the curse of dimensionality and fails to capture relationships—the dot product of any two one-hot words is zero—we use neural networks to learn dense, low-dimensional continuous spaces. In this embedding space, semantic similarity correlates directly with cosine similarity. Modern embeddings are 'contextual', meaning a Transformer architecture processes the entire sentence to generate a vector that understands polysemy (e.g., 'apple' the fruit vs 'apple' the company). In enterprise systems, embeddings are the bedrock of Retrieval-Augmented Generation (RAG); we embed a user's query and perform a nearest-neighbor search against a Vector Database of embedded documents to find contextually relevant information."

## 11. Follow-ups
- "How do you measure distance between embeddings?" (Cosine Similarity is standard. Euclidean (L2) distance is also used, and they are proportional if vectors are normalized).

## 12. Deeper questions
- "What is the difference between Word Embeddings and Sentence Embeddings?" (Word embeddings map tokens. Sentence embeddings pool those tokens (e.g., averaging or using a [CLS] token) and are explicitly fine-tuned via contrastive learning (like SBERT) to cluster semantically similar sentences together).

## 13. Related concepts
- **Cosine Similarity**: The metric used to compare embeddings.
- **Vector Databases**: Infrastructure built specifically to store and index embeddings.

## 14. When it breaks / Edge cases
- Out-of-Vocabulary (OOV) words in static embeddings break the lookup. (Solved by Subword Tokenization).

## 15. Comparison with alternative approaches
- **vs TF-IDF:** TF-IDF represents text based on word frequency. It captures exact keyword matches but fails on synonyms (lexical vs semantic search). Embeddings capture meaning but can occasionally miss exact keyword specifics.

---
*Where this shows up in ML:* 
The foundational layer of every LLM and the core retrieval mechanism for RAG.
"""

files["03-nlp/tokenization.md"] = """# Tokenization

## 1. Definition
Tokenization is the process of breaking down raw text into smaller, discrete chunks (tokens)—such as words, subwords, or characters—that a machine learning model can process.

## 2. Intuition
If you want to teach a child to read, you don't feed them a whole book at once. You break it down into sentences, then words, then syllables. Tokenization is breaking human text into "syllables" that the AI's dictionary recognizes.

## 3. Why it exists
Models cannot process raw strings; they need numbers. If we map every unique English word to a number (Word-level), the dictionary size becomes infinitely large (due to misspellings, plurals, new words). If we map every character (Char-level), the sequences become too long and lose meaning. Subword tokenization exists to balance vocabulary size with sequence length.

## 4. Mechanics
- **Word-Level:** Split by spaces. Huge vocab, fails on Out-Of-Vocabulary (OOV) words.
- **Character-Level:** Split by characters. Tiny vocab (256), but sequences are too long for Transformers.
- **Subword (BPE / WordPiece):** Starts with characters, iteratively merges the most frequently adjacent pairs. "unhappiness" becomes ["un", "happi", "ness"]. Keeps vocab size fixed (e.g., 50k) while handling rare words by breaking them into known chunks.

## 5. Complexity (Time & Space)
- **Time Complexity:** O(N) where N is sequence length for encoding. Training a BPE tokenizer takes time proportional to corpus size.
- **Space Complexity:** O(V) to store the vocabulary mapping in memory.

## 6. Tiny worked example
Sentence: "The AI is learningg"
Subword Tokenization (BPE):
- "The" -> ID: 412
- "AI" -> ID: 8901
- "is" -> ID: 31
- "learning" -> ID: 432
- "g" -> ID: 15 (Handled typo by splitting into known chunks)
Final output: `[412, 8901, 31, 432, 15]`

## 7. Code (Python, with type hints)
```python
from transformers import AutoTokenizer
from typing import List

# Load a pre-trained BPE tokenizer (e.g., from GPT-2 or Llama)
tokenizer = AutoTokenizer.from_pretrained("gpt2")

text: str = "Tokenization is fascinating!"
# Convert string to integer IDs
token_ids: List[int] = tokenizer.encode(text) 
# Decode back to string
decoded_text: str = tokenizer.decode(token_ids)
```

## 8. Common mistakes
- Thinking "Tokens == Words". In modern LLMs (like GPT-4), 1 token is roughly 0.75 words.
- Using a tokenizer from Model A to feed data into Model B (Token IDs are strictly tied to a specific model's embedding matrix).

## 9. 30-second interview answer
"Tokenization breaks raw text into integers so neural networks can process them. Modern LLMs use Subword Tokenization, like Byte-Pair Encoding (BPE), which merges frequent character pairs. This solves the Out-of-Vocabulary problem while keeping the vocabulary size manageable and sequences relatively short."

## 10. 2-minute interview answer
"Tokenization is the critical preprocessing step that bridges raw strings and numerical embeddings. Historically, word-level tokenization resulted in massive, sparse vocabularies and catastrophic Out-Of-Vocabulary failures. We solved this with subword algorithms like Byte-Pair Encoding (BPE), WordPiece, or SentencePiece. BPE is a data-driven compression algorithm: it starts with a base vocabulary of characters and iteratively merges the most frequent pairs in a training corpus until a target vocabulary size (often 30k-100k) is reached. This is brilliant because common words remain single tokens, maximizing context-window efficiency, while rare words or typos are broken down into recognizable phonetic chunks, guaranteeing 100% vocabulary coverage."

## 11. Follow-ups
- "Why can LLMs struggle with rhyming or spelling tasks?" (Because BPE might tokenize "cat" and "hat" completely differently at the subword level, hiding the phonetic spelling from the neural network).

## 12. Deeper questions
- "What is Byte-Level BPE (BBPE)?" (Instead of base characters, it uses the 256 raw bytes. This ensures it can tokenize *any* Unicode character across all languages without needing a massive base vocabulary).

## 13. Related concepts
- **Embeddings**: The step immediately following Tokenization.
- **Context Window**: Measured in Tokens, not words.

## 14. When it breaks / Edge cases
- Tokenizing code or JSON with heavy indentation can waste massive amounts of tokens if spaces aren't merged efficiently by the specific tokenizer.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The very first API call when interacting with any LLM (`tokenizer(text)`).
"""

files["05-transformers/transformer-overview.md"] = """# Transformer Overview

## 1. Definition
The Transformer is a neural network architecture introduced in 2017 ("Attention Is All You Need") that relies entirely on Self-Attention mechanisms, dispensing with recurrence (RNNs) and convolutions (CNNs).

## 2. Intuition
Imagine reading a book. Instead of reading word-by-word and trying to remember everything perfectly in your head (RNN), you have the magical ability to look at a specific word and instantly draw connecting lines to every other relevant word on the page simultaneously, grasping the context perfectly (Transformer).

## 3. Why it exists
RNNs/LSTMs process data sequentially ($O(N)$ sequential steps), making them impossible to parallelize on GPUs. Furthermore, they suffer from catastrophic forgetting on long sequences. The Transformer exists to solve both: it processes the entire sequence in parallel (massive GPU utilization) and directly connects any two words regardless of distance (solving long-term dependencies).

## 4. Mechanics
1. **Input:** Tokens are embedded and combined with Positional Encoding (since the model processes everything in parallel and has no innate sense of order).
2. **Encoder (Optional):** Stacks of Multi-Head Self-Attention + Feed-Forward Networks. Processes the full context bidirectionally (e.g., BERT).
3. **Decoder (Optional):** Masked Self-Attention (prevents looking into the future) + Cross-Attention + Feed-Forward. Generates text autoregressively (e.g., GPT).
4. **Attention:** The core mechanism dynamically routing information between tokens.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N^2 \times d)$ per layer, where $N$ is sequence length and $d$ is embedding dim. (The $N^2$ is the attention bottleneck).
- **Space Complexity:** $O(N^2)$ to store the attention matrix.

## 6. Tiny worked example
Input: "The bank of the river."
The Transformer embeds this. The Self-Attention mechanism calculates that the word "bank" has a high attention score (similarity) with "river", heavily updating the embedding for "bank" to represent geography rather than finance.

## 7. Code (Python, with type hints)
```python
import torch.nn as nn

# A high-level PyTorch Transformer block
class TransformerBlock(nn.Module):
    def __init__(self, embed_dim: int, num_heads: int):
        super().__init__()
        self.attention = nn.MultiheadAttention(embed_dim, num_heads)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, 4 * embed_dim),
            nn.GELU(),
            nn.Linear(4 * embed_dim, embed_dim)
        )
        
    def forward(self, x):
        # Residual connections around Attention and FFN
        attended, _ = self.attention(x, x, x)
        x = self.norm1(x + attended)
        forwarded = self.ffn(x)
        x = self.norm2(x + forwarded)
        return x
```

## 8. Common mistakes
- Thinking Transformers process text sequentially. They don't. All tokens enter the first layer simultaneously.
- Forgetting that the $O(N^2)$ complexity is with respect to *sequence length*, not vocabulary size.

## 9. 30-second interview answer
"The Transformer is an architecture that replaced RNNs by using Self-Attention. It processes sequences entirely in parallel, enabling massive GPU scaling. Its core components are Positional Encodings, Multi-Head Attention, and Feed-Forward networks, forming the basis of all modern LLMs like BERT and GPT."

## 10. 2-minute interview answer
"The Transformer revolutionized AI by abandoning recurrence in favor of pure Attention. Because RNNs process tokens sequentially, they create a computational bottleneck that prevents scaling. The Transformer takes an entire sequence of tokens simultaneously, relying on Positional Encodings to inject order. In the core Multi-Head Attention layers, every token computes a dot product with every other token, creating an $N \times N$ attention matrix. This allows the model to form rich, contextualized representations with direct mathematical paths between words, utterly solving the long-term dependency issue. While this $O(N^2)$ attention mechanism is computationally heavy for long contexts, its highly parallelizable matrix math maps perfectly to GPU hardware, allowing the scaling laws of modern LLMs to take flight."

## 11. Follow-ups
- "What is the difference between Encoder-only and Decoder-only?" (Encoder-only (BERT) sees the whole sequence bidirectionally for understanding. Decoder-only (GPT) uses masked attention to hide future tokens, optimizing for generation).

## 12. Deeper questions
- "How do we fix the $O(N^2)$ bottleneck for long contexts?" (Using Linear Attention approximations, Sparse Attention, Sliding Window Attention, or state-space models like Mamba).

## 13. Related concepts
- **Self-Attention**: The mathematical heart of the Transformer.
- **LLMs**: Almost entirely Decoder-only Transformers.

## 14. When it breaks / Edge cases
- Breaks on infinite or massive sequence lengths (e.g., 1 million tokens) due to the $O(N^2)$ memory requirement of the attention matrix, leading to OOM.

## 15. Comparison with alternative approaches
- **vs RNN/LSTM:** RNNs have $O(N)$ inference complexity (great for memory) but are slow to train (no parallelization) and forget early tokens. Transformers are fast to train but memory hungry during inference.

---
*Where this shows up in ML:* 
Every modern LLM (GPT, Claude, Llama) is a Transformer.
"""

files["05-transformers/self-attention.md"] = """# Self-Attention

## 1. Definition
Self-Attention is a sequence-to-sequence operation where each token in a sequence dynamically updates its own representation by computing a weighted sum of all other tokens in the same sequence, based on how "relevant" they are to it.

## 2. Intuition
You are at a cocktail party. You are talking to someone, but you hear your name across the room. Your brain instantly lowers the "attention weight" on the person in front of you and raises the "attention weight" on the distant conversation. Self-attention does this for words: the word "it" looks across the sentence to figure out what noun it refers to.

## 3. Why it exists
Static embeddings (Word2Vec) map "bank" to a single vector. But "river bank" and "bank account" mean different things. Self-attention exists to create *contextual* embeddings, allowing words to alter their mathematical meaning based on their neighbors.

## 4. Mechanics
1. Every token generates three vectors via learned linear projections: Query (Q), Key (K), and Value (V).
2. **Score:** Compute the dot product between a token's Q and all other tokens' K. (High dot product = high relevance).
3. **Scale:** Divide by $\\sqrt{d_k}$ (dimension size) to stabilize gradients.
4. **Softmax:** Apply Softmax to the scores to get weights that sum to 1.
5. **Output:** Multiply these weights by the V vectors and sum them up.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N^2 \times d)$ where $N$ is sequence length. The $Q \\times K^T$ multiplication creates an $N \\times N$ matrix.
- **Space Complexity:** $O(N^2)$ to store the attention score matrix.

## 6. Tiny worked example
"Apple is tasty."
- "Apple" (Query) checks Keys of "Apple", "is", "tasty".
- Dot products: `[Apple=10, is=2, tasty=8]`.
- Softmax weights: `[Apple=0.8, is=0.01, tasty=0.19]`.
- Output for "Apple": `0.8*V(Apple) + 0.01*V(is) + 0.19*V(tasty)`. The vector for "Apple" now mathematically contains a hint of "tasty".

## 7. Code (Python, with type hints)
```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, mask: torch.Tensor = None) -> torch.Tensor:
    d_k = Q.size(-1)
    # 1. Dot product of Q and K^T
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k ** 0.5)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
        
    # 2. Softmax to get probabilities
    attention_weights = F.softmax(scores, dim=-1)
    
    # 3. Multiply by Values
    output = torch.matmul(attention_weights, V)
    return output
```

## 8. Common mistakes
- Forgetting the scaling factor $\\sqrt{d_k}$. Without it, large dimensions cause large dot products, pushing Softmax into regions with vanishing gradients.
- Confusing Cross-Attention (Q comes from decoder, K/V from encoder) with Self-Attention (Q, K, V all come from the same sequence).

## 9. 30-second interview answer
"Self-attention allows tokens in a sequence to dynamically route information among themselves. It calculates an $N \\times N$ attention matrix by taking the dot product of Query and Key vectors, scaling and applying Softmax, and using the resulting weights to combine Value vectors. This yields highly contextualized embeddings."

## 10. 2-minute interview answer
"Self-attention is the mechanism that solves the long-term dependency problem in NLP. Unlike RNNs, it provides an $O(1)$ path length between any two words in a text. Mathematically, it operates as a differentiable dictionary retrieval system. We project input embeddings into Queries, Keys, and Values. The attention scores are the dot products of $Q$ and $K^T$, representing how much 'focus' word A should put on word B. We scale this by $\\sqrt{d_k}$ to prevent softmax saturation, apply softmax to normalize the scores, and multiply by $V$. The result is a new representation for each token that has absorbed relevant context from the entire sequence. The fundamental tradeoff is its $O(N^2)$ complexity, which makes processing massive contexts computationally prohibitive without hardware optimization."

## 11. Follow-ups
- "What does Masked Self-Attention do?" (Used in decoders like GPT. It forces the upper triangle of the $Q \\times K^T$ matrix to $-\\infty$ before Softmax, preventing tokens from looking at future tokens during training).

## 12. Deeper questions
- "What is FlashAttention?" (A hardware-aware algorithm that fuses the Q, K, V operations, avoiding writing the massive $N \\times N$ intermediate attention matrix to slow GPU HBM memory, keeping it in fast SRAM).

## 13. Related concepts
- **Transformer**: The architecture built around this mechanism.
- **QKV**: The specific projections used.

## 14. When it breaks / Edge cases
- Memory blows up quadratically with $N$. A 100k context window requires gigabytes of VRAM just for the attention matrix.

## 15. Comparison with alternative approaches
- **vs Convolutions:** CNNs only look at local neighbors (fixed receptive field). Self-attention has a global receptive field at layer 1.

---
*Where this shows up in ML:* 
The defining operation in all Transformers.
"""

files["05-transformers/query-key-value.md"] = """# Query, Key, Value (QKV)

## 1. Definition
Query, Key, and Value (QKV) are three distinct vectors generated for every token in a Transformer, used by the Self-Attention mechanism to calculate contextual relationships. 

## 2. Intuition
Think of a database search or a library. 
- **Query (Q):** What you type into the search bar ("Action movies").
- **Key (K):** The metadata/tags on the books on the shelf ("Genre: Action", "Genre: Romance").
- **Value (V):** The actual content of the book.
Attention compares your Query to all Keys. Where they match, you extract that Value.

## 3. Why it exists
If we just computed the dot product of the raw word embeddings with themselves, we'd lack flexibility. Generating three distinct projections (Q, K, V) allows the model to learn asymmetrical relationships. E.g., the word "it" (Query) might seek out nouns (Keys), while the noun outputs its grammatical features (Values).

## 4. Mechanics
1. We have three learned weight matrices: $W_Q, W_K, W_V$.
2. The input embedding $X$ is multiplied by these matrices to produce $Q = X W_Q$, $K = X W_K$, $V = X W_V$.
3. These representations are fed into the scaled dot-product attention formula: $Attention(Q, K, V) = Softmax(QK^T / \\sqrt{d_k}) V$.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \times d^2)$ to project a sequence of $N$ tokens from dimension $d$ to Q, K, V.
- **Space Complexity:** $O(N \times d)$ to store the Q, K, V matrices.

## 6. Tiny worked example
Input embedding $X$ for "He".
$W_Q, W_K, W_V$ are learned matrices.
"He" generates $Q_{he}$ (looking for verbs).
"Ran" generates $K_{ran}$ (identifies as a verb).
$Q_{he} \cdot K_{ran}$ is high.
"He" pulls in $V_{ran}$ to update its meaning.

## 7. Code (Python, with type hints)
```python
import torch
import torch.nn as nn

class QKVProjection(nn.Module):
    def __init__(self, embed_dim: int, head_dim: int):
        super().__init__()
        # In practice, usually fused into one linear layer for speed
        self.q_proj = nn.Linear(embed_dim, head_dim)
        self.k_proj = nn.Linear(embed_dim, head_dim)
        self.v_proj = nn.Linear(embed_dim, head_dim)
        
    def forward(self, x: torch.Tensor):
        Q = self.q_proj(x)
        K = self.k_proj(x)
        V = self.v_proj(x)
        return Q, K, V
```

## 8. Common mistakes
- Assuming Q, K, and V must have the same dimensions as the input. (In Multi-Head Attention, they are projected down to $d_{model} / num\_heads$).
- Thinking Q and K must have the same dimension as V. (Q and K must match to do the dot product, but V can technically be any dimension, though they are usually kept the same).

## 9. 30-second interview answer
"QKV is the abstraction used in Self-Attention, inspired by database retrieval. Input tokens are projected into Queries (what the token is looking for), Keys (what the token contains), and Values (the actual information it provides). The dot product of Queries and Keys determines the attention weights applied to the Values."

## 10. 2-minute interview answer
"The QKV mechanism is how Transformers achieve asymmetric, dynamic routing of information. If we used raw embeddings to compute attention, the relationship between token A and token B would be perfectly symmetric. By applying three separate learned linear transformations—$W_Q$, $W_K$, and $W_V$—the model learns specialized roles. A token's Query vector encodes what context it needs to disambiguate itself. Its Key vector encodes what context it can offer to others. The dot product $Q \\times K^T$ yields the relevance score. Finally, the Value vector contains the actual semantic payload that gets aggregated and passed to the next layer. In modern implementations, these three projections are often fused into a single dense matrix multiplication for maximum GPU efficiency."

## 11. Follow-ups
- "What happens in Cross-Attention (e.g., Encoder-Decoder)?" (The Queries come from the Decoder's current state, but the Keys and Values come from the Encoder's final output).

## 12. Deeper questions
- "What is Grouped Query Attention (GQA) / Multi-Query Attention (MQA)?" (To save memory during LLM inference, MQA shares a single K and V head across multiple Q heads, drastically reducing the KV-cache size).

## 13. Related concepts
- **Self-Attention**: Consumes QKV.
- **KV-Cache**: In LLM generation, we cache the K and V matrices of past tokens to avoid recomputing them.

## 14. When it breaks / Edge cases
- Memory constraints in autoregressive generation (the KV-cache grows linearly with sequence length, eventually causing Out Of Memory).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The first step of every Attention block.
"""

files["05-transformers/multi-head-attention.md"] = """# Multi-Head Attention

## 1. Definition
Multi-Head Attention (MHA) is the process of running multiple Self-Attention mechanisms (heads) in parallel within the same Transformer layer, then concatenating their outputs.

## 2. Intuition
Imagine analyzing a painting. If you only have one "head," you might focus entirely on the colors. By having multiple "heads," Head 1 focuses on colors, Head 2 analyzes the brush strokes, Head 3 identifies the objects, and Head 4 infers the historical context. They all look at the same painting simultaneously but extract different representations.

## 3. Why it exists
A single attention mechanism might average out complex relationships, forcing a token to pick one primary thing to attend to. MHA allows the model to jointly attend to information from different representation subspaces at different positions. (e.g., one head tracks grammar, another tracks pronoun references).

## 4. Mechanics
1. Instead of projecting the input embedding $X$ (size $d_{model}$) into one massive Q, K, and V, we project it into $H$ smaller sets of Q, K, V, each of size $d_{head} = d_{model} / H$.
2. Run standard Scaled Dot-Product Attention on all $H$ heads in parallel.
3. Concatenate the $H$ output matrices back together (resulting back in $d_{model}$ size).
4. Apply a final linear projection ($W_O$) to mix the information.

## 5. Complexity (Time & Space)
- **Time Complexity:** Same as single-head attention: $O(N^2 \times d_{model})$. Splitting the dimension size divides the work by $H$, but doing it $H$ times balances it out perfectly.
- **Space Complexity:** $O(N^2 \times H)$ to store the attention maps for all heads (though often optimized).

## 6. Tiny worked example
Model dim = 512, Heads = 8.
- Each head gets a subspace of $512 / 8 = 64$ dimensions.
- Head 1 does attention on 64 dims. Head 8 does attention on 64 dims.
- Outputs are $8 \times 64 = 512$ dims concatenated.
- Projected through a $512 \times 512$ matrix.

## 7. Code (Python, with type hints)
```python
import torch
import torch.nn as nn

# Conceptual block of MHA
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Fused projection for efficiency
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        
    def forward(self, x):
        batch, seq_len, d_model = x.size()
        
        # Project and reshape: (B, S, 3 * d_model) -> (B, S, 3, H, d_k)
        qkv = self.qkv(x).view(batch, seq_len, 3, self.num_heads, self.d_k)
        
        # Split into Q, K, V
        q, k, v = qkv[:, :, 0], qkv[:, :, 1], qkv[:, :, 2]
        
        # (Self-attention logic here on multiple heads...)
        # Concatenate and project
        # out = self.out_proj(concatenated_heads)
```

## 8. Common mistakes
- Thinking MHA increases the parameter count compared to single-head attention. It doesn't; the projection matrices are just sliced into smaller pieces ($H \times d_k = d_{model}$).
- Not realizing that the multiple heads are processed concurrently in a single massive tensor operation, not a python `for` loop.

## 9. 30-second interview answer
"Multi-Head Attention runs multiple independent self-attention mechanisms in parallel. By splitting the embedding dimension into smaller subspaces, the model can simultaneously attend to different semantic and syntactic relationships (like grammar vs. subject matter) without increasing overall computational complexity."

## 10. 2-minute interview answer
"Multi-Head Attention is what gives the Transformer its expressive power. If we used a single attention head, a token's updated representation would be a blunt weighted average of its neighbors, potentially losing distinct linguistic features. By projecting the Queries, Keys, and Values into $H$ lower-dimensional subspaces and computing attention independently, the model can track multiple distinct relationships. For instance, in 'The cat sat on its mat', one head might focus heavily on 'its' mapping to 'cat' for coreference resolution, while another head maps 'sat' to 'mat' for spatial tracking. These independent insights are then concatenated and linearly projected back to the original dimension. Elegantly, because $d_{head} = d_{model} / H$, the parameter count and FLOPs are virtually identical to a single massive attention head."

## 11. Follow-ups
- "What happens if you use too many heads?" (The dimensionality of each head $d_k$ becomes too small to capture meaningful vector relationships).

## 12. Deeper questions
- "Do we actually need all these heads?" (Research like 'Are Sixteen Heads Really Better than One?' shows that at inference time, many heads can be pruned away without performance loss, as they often learn redundant patterns).

## 13. Related concepts
- **Grouped Query Attention (GQA)**: A modern variant used in Llama 2/3 that reduces the number of K and V heads to save memory, while keeping multiple Q heads.

## 14. When it breaks / Edge cases
- MHA creates significant memory pressure during autoregressive decoding because you must cache the K and V matrices for *every* head across the sequence length (the KV-cache problem).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The primary workhorse layer in all Transformer models.
"""

files["07-rag/rag-overview.md"] = """# RAG Overview (Retrieval-Augmented Generation)

## 1. Definition
Retrieval-Augmented Generation (RAG) is a framework that improves LLM responses by grounding them in external, up-to-date, or proprietary data retrieved from a database during inference.

## 2. Intuition
Taking a test with an LLM is a closed-book exam; it has to rely on what it memorized during training. RAG turns it into an open-book exam. When asked a question, it searches a massive library (database), pulls the relevant pages, puts them on the desk, and reads them to formulate a perfect answer.

## 3. Why it exists
LLMs have three critical flaws: 
1. **Hallucinations:** They confidently make things up.
2. **Static Knowledge:** Their weights are frozen after training; they don't know the news from yesterday.
3. **Data Privacy:** You cannot easily teach an LLM your private company documents without expensive fine-tuning.
RAG solves all three by providing external factual context at inference time.

## 4. Mechanics
1. **Ingestion (Offline):** Chunk documents -> Embed them using an Embedding Model -> Store in a Vector Database.
2. **Retrieval (Online):** User asks query -> Embed query -> Search Vector DB for top-K similar chunks.
3. **Augmentation:** Concatenate the retrieved chunks with the user's query into a prompt ("Given this context: [chunks], answer: [query]").
4. **Generation:** Send the augmented prompt to the LLM to generate the final answer.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(D \log N)$ for retrieval using Approximate Nearest Neighbors (where $N$ is DB size, $D$ is vector dim), plus LLM inference time.
- **Space Complexity:** High storage requirements for maintaining the dense vector database.

## 6. Tiny worked example
- Query: "What is our company's refund policy?"
- Retrieve: FAISS database returns Chunk 42: "Refunds are allowed within 30 days."
- Augmented Prompt: "Context: Refunds are allowed within 30 days. Question: What is our company's refund policy?"
- LLM Output: "You can get a refund within 30 days."

## 7. Code (Python, with type hints)
```python
# Conceptual RAG pipeline
def simple_rag(query: str, vector_db, llm_client) -> str:
    # 1. Embed Query
    query_vector = embed_model.encode(query)
    
    # 2. Retrieve top 3 relevant chunks
    context_chunks = vector_db.search(query_vector, top_k=3)
    
    # 3. Augment
    context = "\n".join(context_chunks)
    prompt = f"Context:\n{context}\n\nAnswer the query: {query}"
    
    # 4. Generate
    response = llm_client.generate(prompt)
    return response
```

## 8. Common mistakes
- Expecting RAG to solve complex reasoning over the whole database (e.g., "Summarize all 5,000 PDF documents"). RAG is for targeted extraction, not infinite context.
- Neglecting chunking strategy. If chunks are too small, context is lost. If too large, the retrieval becomes noisy and LLM context limits are exceeded.

## 9. 30-second interview answer
"RAG combines an information retrieval system with a generative LLM. By fetching relevant documents from a vector database and injecting them into the LLM's prompt, RAG grounds the model in factual, private, or real-time data, drastically reducing hallucinations without the need for model fine-tuning."

## 10. 2-minute interview answer
"RAG is the enterprise standard for deploying LLMs. Training or fine-tuning models on private data is expensive, prone to catastrophic forgetting, and doesn't inherently solve hallucinations. RAG decouples knowledge storage from language generation. In the offline phase, we chunk and embed documents into a Vector Database. At inference, we embed the user's query and perform a semantic cosine-similarity search. The top-K retrieved chunks are injected directly into the LLM's prompt. This 'open-book' approach forces the model to synthesize answers from cited facts, practically eliminating hallucinations. The most challenging engineering tasks in RAG aren't the LLM calls, but the data pipeline: optimal chunking, hybrid search (combining keyword and vector search), and reranking retrieved results for maximal relevance."

## 11. Follow-ups
- "What is Hybrid Search?" (Using both dense embeddings (semantic meaning) and sparse keyword search (BM25/TF-IDF) to get the best of both worlds).

## 12. Deeper questions
- "How do you handle Multi-Hop QA in RAG?" (Use agentic patterns like ReAct, or GraphRAG, where the LLM performs multiple sequential searches to connect disparate pieces of information).

## 13. Related concepts
- **Embeddings**: The math powering the retrieval.
- **Vector Databases**: The infrastructure storing the embeddings.

## 14. When it breaks / Edge cases
- Fails miserably if the retriever pulls the wrong documents. The LLM is only as good as the context it is fed (Garbage In, Garbage Out).

## 15. Comparison with alternative approaches
- **vs Fine-Tuning:** Fine-tuning teaches the model *how* to speak or behave (format, tone). RAG teaches the model *what* to say (facts). You almost always use RAG for knowledge injection.

---
*Where this shows up in ML:* 
The architecture of virtually every enterprise LLM chatbot (e.g., Notion AI, ChatGPT with Web Browsing).
"""

files["07-rag/faiss.md"] = """# FAISS (Facebook AI Similarity Search)

## 1. Definition
FAISS is an open-source C++ library developed by Meta AI that allows developers to quickly search for embeddings of multimedia documents that are similar to each other. It is the most popular library for dense vector similarity search.

## 2. Intuition
If you want to find the closest point in a 2D grid, you just look around. If you want to find the closest point in a 768-dimensional space among a billion points, checking every single point (Exhaustive Search) will take days. FAISS acts as an ultra-efficient, mathematical indexing system that can find the closest point in milliseconds using approximations.

## 3. Why it exists
Vector databases and RAG pipelines require comparing a query vector against millions of document vectors using Cosine Similarity or L2 distance. An exact $O(N)$ nearest-neighbor search is too slow for production latency requirements. FAISS exists to provide highly optimized Approximate Nearest Neighbor (ANN) search algorithms.

## 4. Mechanics
FAISS groups vectors mathematically to avoid searching everything:
1. **Flat Index (Exact):** L2 distance against every vector. $100\\%$ accurate, but slow.
2. **IVF (Inverted File Index):** Uses K-Means to cluster the vector space into Voronoi cells. When searching, FAISS only checks the vectors in the cell closest to the query.
3. **PQ (Product Quantization):** Compresses vectors by splitting them into sub-vectors and replacing them with short centroid IDs, drastically reducing memory usage and allowing calculations in compressed space.
4. **HNSW (Hierarchical Navigable Small World):** Builds a multi-layered graph of vectors for blazingly fast, highly accurate search without clustering, trading off higher memory usage.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ for Flat. $O(\log N)$ or better for HNSW/IVF search.
- **Space Complexity:** High for HNSW (graph pointers). Low for PQ (compressed bytes).

## 6. Tiny worked example
You have 1 million vectors. 
Using `IndexFlatL2`: Compares query to 1,000,000 vectors. Takes 50ms.
Using `IndexIVFFlat` (100 clusters): Compares query to nearest cluster (~10,000 vectors). Takes 2ms, but might miss the absolute closest vector if it's on a cluster boundary.

## 7. Code (Python, with type hints)
```python
import faiss
import numpy as np

dimension = 768
num_vectors = 10000

# Generate random mock data
data = np.random.random((num_vectors, dimension)).astype('float32')
query = np.random.random((1, dimension)).astype('float32')

# Create an exact search index
index = faiss.IndexFlatL2(dimension)
index.add(data)

# Search for the Top-5 nearest neighbors
distances, indices = index.search(query, k=5)
```

## 8. Common mistakes
- Not training the index. Indexes like `IVF` or `PQ` must be `.train()`'d on a representative sample of data so they can learn the clusters before you `.add()` data to them.
- Normalizing vectors incorrectly (L2 distance on normalized vectors is mathematically equivalent to Cosine Similarity, but if you forget to normalize, results will be ruined).

## 9. 30-second interview answer
"FAISS is a library for highly efficient vector similarity search. While exact search scales linearly and becomes too slow for large datasets, FAISS implements Approximate Nearest Neighbor (ANN) algorithms like HNSW, IVF, and Product Quantization to trade a tiny amount of accuracy for massive speed and memory optimizations."

## 10. 2-minute interview answer
"FAISS is the engine powering modern Vector Databases. In RAG pipelines, computing the cosine similarity between a query vector and millions of document vectors via brute force is an $O(N)$ operation that cripples latency. FAISS solves this using Approximate Nearest Neighbor (ANN) techniques. Depending on the hardware constraints, we can configure FAISS indexes differently. If memory is abundant and we need blazingly fast, high-recall search, we use HNSW, which navigates a multi-layer graph. If memory is tight, we combine IVF (Inverted File Index) to cluster the space with Product Quantization (PQ) to compress the vectors. FAISS allows ML engineers to perfectly balance search speed, RAM usage, and recall accuracy."

## 11. Follow-ups
- "How do you do Cosine Similarity in FAISS?" (FAISS natively prefers L2 distance. To do cosine similarity, you normalize all your vectors to a length of 1, then use `IndexFlatIP` (Inner Product)).

## 12. Deeper questions
- "Explain Product Quantization (PQ)." (It slices a high-dimensional vector into sub-vectors, runs K-Means on the sub-vectors, and replaces the floats with an 8-bit integer ID representing the closest centroid. It achieves massive compression, e.g., 32x).

## 13. Related concepts
- **Vector Databases**: Pinecone, Milvus, and Qdrant often use FAISS or HNSW algorithms under the hood.
- **Embeddings**: The data FAISS indexes.

## 14. When it breaks / Edge cases
- ANN indexes (like IVF) can suffer severe recall drops if the data distribution changes drastically after the index was trained.

## 15. Comparison with alternative approaches
- **FAISS vs Managed Vector DBs (Pinecone):** FAISS is just a local library in RAM. Managed Vector DBs wrap ANN algorithms with database features: CRUD operations, persistence, metadata filtering, and distributed scaling.

---
*Where this shows up in ML:* 
The core backend for retrieving documents in custom RAG pipelines.
"""

files["08-efficient-llms/lora.md"] = """# LoRA (Low-Rank Adaptation)

## 1. Definition
LoRA is a Parameter-Efficient Fine-Tuning (PEFT) technique that freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture, significantly reducing the number of trainable parameters.

## 2. Intuition
Imagine a gigantic, 10,000-page encyclopedia (the LLM). You want to update it for medical terminology. Instead of rewriting the entire encyclopedia (Full Fine-Tuning), you write your changes on a small stack of sticky notes (LoRA matrices) and stick them on the relevant pages. During reading, you look at the book and the sticky notes together.

## 3. Why it exists
Full fine-tuning of a 70B parameter model requires clusters of A100 GPUs and hundreds of gigabytes of VRAM to store optimizer states and gradients for every weight. LoRA exists to allow researchers to fine-tune massive models on a single consumer GPU by reducing the trainable parameters by up to 10,000x.

## 4. Mechanics
- A standard neural network layer performs $W_0 x$, where $W_0$ is a massive $d \times d$ matrix.
- LoRA freezes $W_0$ and adds a delta update matrix: $\Delta W = B \times A$.
- Matrix $A$ has shape $d \times r$, and $B$ has shape $r \times d$, where $r$ (rank) is very small (e.g., 8 or 16).
- $B \times A$ results in a $d \times d$ matrix, but because of the "low rank" bottleneck, it contains drastically fewer parameters.
- Forward pass becomes: $y = W_0 x + BAx$.
- Only $A$ and $B$ receive gradient updates.

## 5. Complexity (Time & Space)
- **Time Complexity:** Slightly slower forward pass during training (requires computing $BAx$). No latency hit during inference (matrices can be merged).
- **Space Complexity:** Huge VRAM savings. Training parameters drop from $d^2$ to $2rd$.

## 6. Tiny worked example
Let $W_0$ be $1000 \times 1000$ (1,000,000 parameters).
Let Rank $r = 4$.
Matrix $A$ is $1000 \times 4$ (4,000 params). Matrix $B$ is $4 \times 1000$ (4,000 params).
Total trainable params: 8,000.
Reduction: 99.2% fewer parameters to train!

## 7. Code (Python, with type hints)
```python
# Conceptual implementation of a LoRA Linear layer
import torch
import torch.nn as nn

class LoRALinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, rank: int = 8):
        super().__init__()
        # The frozen pre-trained weights
        self.W_0 = nn.Linear(in_features, out_features, bias=False)
        self.W_0.weight.requires_grad = False
        
        # The LoRA trainable matrices
        self.lora_A = nn.Parameter(torch.randn(in_features, rank))
        self.lora_B = nn.Parameter(torch.zeros(rank, out_features)) # Init B to 0
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pre-trained output + LoRA delta
        frozen_out = self.W_0(x)
        lora_out = (x @ self.lora_A) @ self.lora_B
        return frozen_out + lora_out
```

## 8. Common mistakes
- Initializing matrix $B$ with random noise instead of zeros. If both are random, the initial forward pass will output garbage. Initializing $B$ to 0 ensures the initial LoRA output is 0, keeping the pre-trained behavior exactly identical at step 0.
- Forgetting to merge weights for inference.

## 9. 30-second interview answer
"LoRA is a parameter-efficient fine-tuning method. It freezes the original model weights and injects two low-rank matrices (A and B) into the architecture. By training only these much smaller matrices, we reduce VRAM requirements exponentially while achieving performance nearly identical to full fine-tuning."

## 10. 2-minute interview answer
"LoRA leverages the hypothesis that the 'intrinsic rank' of neural network updates is very low—meaning we don't need to change every weight independently to learn a new task. Instead of updating a massive $D \times D$ weight matrix, LoRA freezes it and learns an additive update represented by the product of two low-rank matrices, $B$ and $A$, with an inner dimension $r$. This reduces the optimizer state memory by orders of magnitude, making it possible to fine-tune 7B or 13B models on a single GPU. The greatest engineering benefit of LoRA is at inference time: because matrix addition is distributive, we can statically add the trained $BA$ matrix into the original $W_0$ matrix. This 'weight merging' means deploying a LoRA-tuned model incurs absolutely zero latency penalty compared to the base model."

## 11. Follow-ups
- "What is Alpha in LoRA?" (A scaling factor applied to the LoRA output, used to balance the magnitude of the update against the frozen weights, often set to 2x the Rank).

## 12. Deeper questions
- "If I want to serve 50 different customers with 50 different fine-tunes, how does LoRA help?" (You load the base model into GPU memory ONCE. You swap the tiny LoRA 'adapters' in and out of VRAM dynamically per request (Multi-LoRA serving), saving terabytes of VRAM).

## 13. Related concepts
- **QLoRA**: LoRA combined with Quantization.
- **Fine-Tuning**: The overarching goal.

## 14. When it breaks / Edge cases
- LoRA struggles with completely novel knowledge injection (like a language the base model has never seen). Full fine-tuning is better for fundamental domain shifts.

## 15. Comparison with alternative approaches
- **vs Prompt Tuning / Prefix Tuning:** LoRA modifies the computation internally and performs better. Prompt tuning consumes valuable context window tokens.

---
*Where this shows up in ML:* 
The `peft` library by HuggingFace, used to train almost every open-source customized model.
"""

files["08-efficient-llms/qlora.md"] = """# QLoRA (Quantized LoRA)

## 1. Definition
QLoRA is an extension of LoRA that allows for the fine-tuning of massive LLMs on highly memory-constrained hardware by quantizing the frozen base model to 4-bit precision, while training 16-bit LoRA adapters.

## 2. Intuition
Imagine you have a gigantic 10,000-page encyclopedia (Base Model), but your desk (GPU VRAM) is too small to hold it. You compress the book by printing it in micro-text (4-bit Quantization) so it fits. You can't write in micro-text yourself, so you use normal-sized sticky notes (16-bit LoRA) to write your updates. When reading, you decompress the micro-text line-by-line, read it with your sticky note, and move on.

## 3. Why it exists
Standard LoRA drastically reduces the optimizer memory (gradients), but the *base model weights* still have to fit in VRAM in 16-bit float. A 70B model in 16-bit requires 140GB of VRAM just to load. QLoRA exists to crush that base model footprint, allowing 70B models to be fine-tuned on a single 48GB consumer GPU.

## 4. Mechanics
1. **4-bit NormalFloat (NF4):** The base model is loaded into an information-theoretically optimal 4-bit data type designed specifically for normally distributed neural network weights.
2. **Double Quantization:** Even the quantization constants are quantized to save further memory.
3. **Paged Optimizers:** Uses NVIDIA Unified Memory to page optimizer states to CPU RAM if GPU VRAM spikes, preventing Out-Of-Memory crashes.
4. **Execution:** During the forward/backward pass, the 4-bit weights are "dequantized" back to 16-bit purely in the GPU compute registers just in time for matrix multiplication with the 16-bit LoRA adapters.

## 5. Complexity (Time & Space)
- **Time Complexity:** 30-50% slower training than standard LoRA because of the constant on-the-fly dequantization overhead.
- **Space Complexity:** Massive VRAM savings. Weights take 4 bits instead of 16 bits (a 4x reduction for the base model).

## 6. Tiny worked example
Llama-3 8B Base Model:
- 16-bit float: 16 GB VRAM to load.
- 4-bit QLoRA: 4.5 GB VRAM to load + ~1 GB for LoRA adapters and optimizer. 
- You can now fine-tune an 8B model on an 8GB RTX 3080.

## 7. Code (Python, with type hints)
```python
# Conceptual huggingface integration
from transformers import BitsAndBytesConfig

# Configure 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",       # NormalFloat4
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load model in 4-bit
# model = AutoModelForCausalLM.from_pretrained(..., quantization_config=bnb_config)
# Then apply LoRA using PEFT...
```

## 8. Common mistakes
- Misunderstanding where the computation happens. You cannot do matrix math directly in 4-bit NF4. The weights *rest* in VRAM in 4-bit, but are cast to 16-bit `bfloat16` in the SRAM registers before calculation.
- Trying to merge a 16-bit LoRA adapter into a 4-bit base model for deployment (you must either dequantize the base model back to 16-bit to merge, or use specialized inference engines).

## 9. 30-second interview answer
"QLoRA combines 4-bit quantization with LoRA. It loads the massive pre-trained base model in a highly compressed 4-bit format (NF4) to save VRAM, but maintains the trainable LoRA adapters in 16-bit precision. This enables fine-tuning of massive LLMs on single consumer GPUs with virtually no degradation in final model quality."

## 10. 2-minute interview answer
"QLoRA democratized LLM fine-tuning. While LoRA reduces the memory needed for gradients and optimizer states, the sheer size of the frozen base model remained a barrier. QLoRA solves this by aggressively quantizing the base model weights to 4-bit NormalFloat, an encoding specifically optimized for the bell-curve distribution of neural network weights. To maintain performance, the trainable LoRA adapters are kept in 16-bit BrainFloat (bfloat16). During the forward and backward passes, the 4-bit weights are dynamically dequantized to 16-bit inside the GPU's fast SRAM, computed, and then discarded. While this on-the-fly casting incurs a training time penalty, it slashes the VRAM footprint by 4x, making it possible to tune state-of-the-art models on consumer hardware without sacrificing accuracy."

## 11. Follow-ups
- "What is Double Quantization?" (The metadata/scaling blocks used to quantize the model also take up memory. Double Quantization runs a second round of quantization on those scaling blocks to squeeze out another few hundred megabytes of VRAM).

## 12. Deeper questions
- "If QLoRA trains the LoRA weights in 16-bit, how do you deploy it?" (For inference, you can use frameworks like `llama.cpp` or `vLLM` which support loading 4-bit base models alongside fp16 adapters, or you merge them in fp16 if you have the memory).

## 13. Related concepts
- **LoRA**: The foundational PEFT technique.
- **Quantization**: The broader concept of reducing float precision.

## 14. When it breaks / Edge cases
- Slower training speeds mean it is less ideal if you have unlimited GPU VRAM (in which case standard LoRA or full fine-tuning is faster).

## 15. Comparison with alternative approaches
- **vs PTQ (Post-Training Quantization):** PTQ quantizes a model *after* training, which often degrades accuracy. QLoRA is Quantization-Aware Parameter-Efficient Fine-Tuning; the LoRA adapters learn to compensate for any errors introduced by the 4-bit base model compression.

---
*Where this shows up in ML:* 
The `bitsandbytes` library used in almost all open-source HuggingFace fine-tuning scripts.
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch B - Sub-pass 2 Complete")
