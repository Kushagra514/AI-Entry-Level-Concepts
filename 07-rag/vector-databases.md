# Vector Databases

## 1. Definition
A Vector Database is a specialized database designed to store, manage, and query high-dimensional vectors (embeddings), optimized for Approximate Nearest Neighbor (ANN) search and metadata filtering.

## 2. Intuition
A traditional database finds exact matches (`WHERE name = 'John'`). A vector database finds conceptual similarities (`ORDER BY similarity(text, 'How do I fix my car?')`). It places documents in a vast geometric space and finds which ones are closest to your question.

## 3. Why it exists
Comparing a query vector against 10 million document vectors using exact dot products takes too long ($O(N)$). Vector databases use specialized index structures (like HNSW) to reduce the search time to $O(\log N)$, enabling millisecond retrieval over massive datasets.

## 4. Mechanics
- **Storage:** Stores the raw text (payload/metadata) alongside the dense vector.
- **Indexing:** Uses algorithms like HNSW (Hierarchical Navigable Small World) or IVF (Inverted File Index) to build a navigable graph or tree of the vectors.
- **Search (ANN):** Traverses the index to find the $K$ closest vectors to the query vector without scanning the whole database.
- **Filtering:** Pre-filtering (filter metadata, then search vectors) or post-filtering (search vectors, then filter metadata). Advanced DBs use single-stage filtered search.

## 5. Complexity (Time & Space)
- **Time (Search):** Exact KNN is $O(N \cdot d)$. ANN (HNSW) is $O(\log N \cdot d)$.
- **Space:** $O(N \cdot d)$ plus the overhead of the index graph structure (which can double the memory requirements).

## 6. Tiny worked example
Store: 
1. `[0.1, 0.9]` (Topic: Dogs)
2. `[0.8, 0.2]` (Topic: Finance)
Query: `[0.2, 0.8]` ("Tell me about puppies")
The DB uses cosine similarity, finds vector 1 is the closest, and returns the associated text document about Dogs.

## 7. Code (Python)
```python
import chromadb

# Initialize local ChromaDB
client = chromadb.Client()
collection = client.create_collection("my_docs")

# Add documents (Chroma handles embedding automatically by default)
collection.add(
    documents=["The stock market is up.", "My dog is cute."],
    metadatas=[{"source": "news"}, {"source": "blog"}],
    ids=["id1", "id2"]
)

# Query
results = collection.query(
    query_texts=["Tell me about pets"],
    n_results=1
)
print(results['documents']) # [['My dog is cute.']]
```

## 8. Common mistakes
- Confusing a Vector Database (Pinecone, Qdrant, Chroma, Weaviate) with an ANN library (FAISS, Annoy). FAISS is an in-memory C++ library for search. A vector database wraps ANN search with CRUD operations, persistence, distributed scaling, and metadata filtering.
- Not using metadata filtering, forcing the LLM to filter out irrelevant contexts that could have been excluded via simple SQL-like WHERE clauses.

## 9. 30-second interview answer
"Vector databases store document embeddings and perform sub-linear Approximate Nearest Neighbor (ANN) search, usually via HNSW indexes. Unlike in-memory libraries like FAISS, full vector databases like Pinecone or Qdrant support CRUD operations, distributed storage, and crucial metadata filtering, making them the standard retrieval backend for RAG."

## 10. 2-minute interview answer
"A vector database is the retrieval engine of a RAG pipeline. When we embed millions of documents, finding the most relevant one requires computing the distance between the query vector and every document vector. An exact K-Nearest Neighbors search is $O(N)$, which is too slow in production. Vector databases solve this using Approximate Nearest Neighbor (ANN) algorithms, the most dominant being HNSW (Hierarchical Navigable Small World). HNSW builds a multi-layered graph where upper layers have long-distance links for fast zooming, and bottom layers have dense links for precise local search, reducing search time to $O(\log N)$. Beyond search, production vector databases like Pinecone, Weaviate, or pgvector provide enterprise features: persistent storage, high availability, and metadata filtering. Metadata filtering is particularly tricky: if you filter *after* search (post-filtering), you might end up with 0 results. If you filter *before* search (pre-filtering), you ruin the structure of the HNSW graph. Modern vector databases solve this with custom single-stage filtered search algorithms."

## 11. Follow-ups
- "What is the tradeoff in Approximate Nearest Neighbor (ANN) search?" (Speed vs. Recall. You get massive speedups in exchange for a small probability that the absolute closest vector is missed).

## 12. Deeper questions
- "How does HNSW work at a high level?" (It's inspired by Skip Lists. It builds multiple layers of graphs. The top layer has very few nodes and long edges. You start at the top, navigate to the closest node, drop down a layer, and repeat until you hit the bottom layer containing all nodes).

## 13. Related concepts
- **Cosine Similarity**: The distance metric typically used.
- **pgvector**: Adding vector search to traditional Postgres.

## 14. When it breaks / Edge cases
- High dimensionality curse: As dimensions approach 10,000, distance metrics lose meaning and ANN structures degenerate to near-linear search performance.

## 15. Comparison with alternative approaches
- **FAISS vs Pinecone:** FAISS is a library (you manage memory and persistence). Pinecone is a managed SaaS database.

---
*Where this shows up in ML:*
RAG backend infrastructure.
