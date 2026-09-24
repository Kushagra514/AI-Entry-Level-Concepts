# Reranking in RAG

## 1. Definition
Reranking is a second-stage retrieval process where a highly accurate, computationally expensive model (a cross-encoder) re-scores and reorders a shortlist of documents retrieved by a fast, cheaper first-stage model (like a vector database).

## 2. Intuition
Imagine hiring an employee. Stage 1 (Vector DB): A computer scans 10,000 resumes for keywords/embeddings and gives you the top 50 in 1 second. Stage 2 (Reranker): You (the cross-encoder) spend 10 minutes deeply reading those 50 resumes to pick the absolute best 5 to interview.

## 3. Why it exists
Bi-encoders (embedding models) process the query and document separately into vectors, allowing pre-computation, but missing deep interaction between words. Cross-encoders process the query and document *together*, allowing attention to flow between them, yielding vastly superior accuracy but at extreme computational cost. Reranking gives the best of both worlds.

## 4. Mechanics
- **Stage 1 (Retrieval):** Fast bi-encoder or BM25 retrieves top $N$ documents (e.g., $N=50$) from a database of millions.
- **Stage 2 (Reranking):** The Query and Document are concatenated (`[CLS] Query [SEP] Document [SEP]`) and passed through a Cross-Encoder Transformer (e.g., Cohere Rerank, BGE-Reranker).
- **Output:** The cross-encoder outputs a relevance score (0 to 1). The top $K$ documents (e.g., $K=5$) are passed to the generative LLM.

## 5. Complexity (Time & Space)
- **Time:** $O(N \cdot L^2)$ where $N$ is the shortlist size (e.g., 50) and $L$ is query+doc length. Too slow for millions of docs, but fine for 50.
- **Space:** Requires running a medium-sized Transformer (e.g., 300M parameters) at inference time.

## 6. Tiny worked example
Query: "How to apply for leave?"
Stage 1 (Bi-encoder) retrieves 10 docs. 
Doc A (Rank 1): "Leave the building via the fire exit." (High cosine similarity due to word "leave").
Doc B (Rank 2): "Submit PTO requests via the HR portal." (Lower similarity).
Stage 2 (Cross-encoder) sees "apply for leave" paired with both docs. Its attention mechanism realizes Doc A is about exiting, Doc B is about PTO. 
Reranker outputs: Doc B score 0.95, Doc A score 0.05. Ranks are swapped.

## 7. Code (Python)
```python
from sentence_transformers import CrossEncoder

# Load a cross-encoder model
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

query = "What is the capital of France?"
documents = [
    "Paris is a beautiful city.",
    "The capital of France is Paris.",
    "France is in Europe."
]

# Create pairs of (Query, Document)
pairs = [[query, doc] for doc in documents]

# Predict scores (higher is more relevant)
scores = reranker.predict(pairs)

# Combine and sort
results = sorted(zip(scores, documents), reverse=True)
for score, doc in results:
    print(f"{score:.4f} | {doc}")
```

## 8. Common mistakes
- Running a cross-encoder on the entire database. It will take hours/days for a single query. Cross-encoders cannot be pre-computed.
- Retrieving only 5 documents in Stage 1 and reranking those 5. The reranker needs a wide net (e.g., 50-100 docs) to find the gems that Stage 1 misranked.

## 9. 30-second interview answer
"Reranking is a two-stage retrieval architecture. First, a fast bi-encoder (vector DB) retrieves a shortlist of ~50 documents. Second, a cross-encoder model reranks this shortlist by processing the query and document simultaneously. Because cross-encoders apply attention across both texts, they are highly accurate but too computationally expensive to run on the whole database. Reranking bridges the gap between speed and accuracy."

## 10. 2-minute interview answer
"Reranking solves the fundamental limitation of standard vector embeddings. Standard embeddings use a bi-encoder architecture: the query and document are embedded completely independently, and similarity is just a dot product. This allows us to pre-compute document vectors and search millions of them in milliseconds, but it loses deep semantic interactions—the model can't compare how specific words in the query relate to specific words in the document. A cross-encoder concatenates the query and document and feeds them through the Transformer together, allowing the self-attention mechanism to attend from query words directly to document words. This yields massive accuracy improvements, heavily penalizing superficial keyword matches that trick bi-encoders. Because cross-encoders cannot be pre-computed (the input depends on the dynamic query), they are $O(N)$ at inference time. Therefore, we use a pipeline: retrieve top 100 with a bi-encoder (fast), and rerank those 100 with a cross-encoder (accurate), before passing the top 5 to the LLM. Implementing Cohere Rerank or BGE-Reranker is usually the highest ROI upgrade you can make to a failing RAG pipeline."

## 11. Follow-ups
- "What is ColBERT?" (A late-interaction model that sits between bi-encoders and cross-encoders. It stores embeddings for every token in a document, and at query time, computes the maximum similarity for each query token against all document tokens. Faster than cross-encoders, more accurate than bi-encoders).

## 12. Deeper questions
- "How does the cross-encoder output a single score?" (Usually, a classification head is attached to the `[CLS]` token of the concatenated input, trained with Binary Cross-Entropy on relevant/irrelevant pairs to output a probability of relevance).

## 13. Related concepts
- **Bi-encoder**: The embedding model used for the vector database.
- **Cross-encoder**: The reranker model.

## 14. When it breaks / Edge cases
- Rerankers have strict context limits (often 512 tokens). If your retrieved chunks are large, the reranker will truncate them and fail to see the relevant information at the end of the chunk.

## 15. Comparison with alternative approaches
- **Bi-encoder (Embeddings) vs Cross-encoder (Reranker):** Bi-encoder = Independent processing, pre-computable, fast search, lower accuracy. Cross-encoder = Joint processing, dynamic only, slow search, highest accuracy.

---
*Where this shows up in ML:*
State-of-the-art search engines, advanced RAG architectures.
