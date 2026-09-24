# RAG One-Page Revision

## What is RAG?
Retrieval-Augmented Generation. Instead of an LLM relying on frozen training weights, it searches a database for external documents and uses them as context to answer a query.

## The Pipeline
1. **Ingestion (Offline):** Parse PDFs/HTML $\to$ Chunk text (e.g., 512 tokens with overlap) $\to$ Pass through Embedding Model $\to$ Store in Vector DB.
2. **Retrieval (Online):** User Query $\to$ Embed Query $\to$ Cosine Similarity Search $\to$ Top-K Chunks.
3. **Generation:** Construct Prompt (`"Context: {chunks}, Question: {query}"`) $\to$ LLM answers.

## Advanced Retrieval
- **Sparse Search (BM25):** Keyword matching (TF-IDF variant). Excellent for exact serial numbers, names.
- **Dense Search (Embeddings):** Semantic matching ("fast car" matches "sports vehicle").
- **Hybrid Search:** Combine Sparse + Dense.
- **Reranking:** Bi-encoders (fast dense search) calculate dot products. Cross-encoders (Rerankers) process Query + Document together through a Transformer. High latency, extreme accuracy. Use Bi-encoder to fetch 100, use Reranker to narrow down to top 5.

## RAG Failure Modes (How to Debug)
1. **Retrieval Failure:** The vector search missed the document. (Fix: Better chunking, hybrid search).
2. **Context Failure:** Document was found, but lacks specific details. (Fix: Increase chunk size, metadata filtering).
3. **Generation Failure (Hallucination):** The context was perfect, but the LLM ignored it or made up an answer. (Fix: Better prompt, stronger LLM).

## Interview Traps
- *Does RAG eliminate hallucinations?* No. It *grounds* the model and reduces hallucinations, but the LLM can still misinterpret the retrieved text.
- *Why not put the whole database in a 1M token context window?* Cost, latency, and "Lost in the Middle" syndrome (models forget facts located in the middle of massive prompts).
