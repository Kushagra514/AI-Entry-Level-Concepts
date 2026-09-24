# Embeddings

## 1. Definition
Embeddings are dense, low-dimensional continuous vector representations of discrete data (like words, sentences, or images) that capture semantic meaning.

## 2. Intuition
Imagine mapping words to a 3D room. You put "King" in the back-right corner. You put "Man" next to it. You put "Apple" on the opposite side of the room. By looking at the distance between coordinates, the computer mathematically understands that a King is related to a Man, but completely unrelated to an Apple.

## 3. Why it exists
Computers only understand numbers. Naive text encoding (One-Hot Encoding) creates massive, sparse vectors (e.g., $1 	imes 50,000$ for a vocabulary) where every word is mathematically equidistant from every other word, destroying semantic relationships. Embeddings compress this into dense vectors (e.g., $1 	imes 768$) where geometric distance equals semantic similarity.

## 4. Mechanics
- A model (like Word2Vec, BERT, or text-embedding-ada-002) is trained on massive text corpora to predict missing words.
- The internal weights of this model learn to represent words/sentences as vectors.
- After training, the model acts as a lookup table (for words) or a forward-pass function (for sentences), converting input text into an array of floats.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(L 	imes d^2)$ for generating contextual embeddings (like Transformers), where $L$ is sequence length and $d$ is embedding dimension.
- **Space Complexity:** $O(V 	imes d)$ to store the embedding matrix for a vocabulary of size $V$.

## 6. Tiny worked example
One-hot: `Apple = [1,0,0]`, `Orange = [0,1,0]`. Dot product (similarity) = 0.
Embedding: `Apple = [0.9, 0.1]`, `Orange = [0.8, 0.2]`. Dot product > 0 (high similarity).
Vector arithmetic: $Embedding(King) - Embedding(Man) + Embedding(Woman) \approx Embedding(Queen)$.

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
