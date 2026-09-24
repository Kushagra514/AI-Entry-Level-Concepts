# RAG Overview (Retrieval-Augmented Generation)

## 1. Definition
Retrieval-Augmented Generation (RAG) is an architectural framework that improves Large Language Model (LLM) responses by grounding them in external, retrieved data. It separates knowledge retrieval from language generation, injecting relevant context into the model's prompt at inference time.

## 2. Intuition
Taking a test with a standalone LLM is a closed-book exam; the model relies entirely on what it memorized during training. RAG turns it into an open-book exam. When asked a question, it searches a library (database), pulls the relevant pages, and uses them as context to synthesize an accurate answer.

## 3. Why It Exists
Standalone LLMs have significant limitations:
1. **Hallucinations:** They confidently generate plausible but incorrect facts.
2. **Static Knowledge:** Their internal knowledge is frozen at their training cutoff date.
3. **Data Privacy/Access:** They do not natively know your private, proprietary, or highly specialized data.
RAG addresses these by fetching factual, up-to-date context at inference time without requiring expensive model fine-tuning.

## 4. Core Mechanics (The Complete Mental Model)
```text
[OFFLINE PIPELINE]
Documents → Parsing → Chunking → Embedding Model → Vector Database Index

[ONLINE PIPELINE]
User Query
    ↓
Query Embedding
    ↓
Retrieval (Dense/Sparse/Hybrid)
    ↓
Reranking (Optional, Cross-Encoder)
    ↓
Context Construction (Prompting)
    ↓
LLM Generation
    ↓
Answer
```

## 5. Mathematical View
Retrieval often relies on Cosine Similarity between a query embedding $q$ and a document chunk embedding $d$:

$$ \text{similarity} = \cos(\theta) = \frac{q \cdot d}{\|q\| \|d\|} $$

The retrieval system returns the top-$K$ chunks that maximize this score.

## 6. Tiny Worked Example
- **Query:** "What is the return policy for clearance items?"
- **Retrieval:** The database returns `Chunk_102`: "Clearance items are final sale and cannot be returned."
- **Augmented Prompt:**
  ```text
  Context: Clearance items are final sale and cannot be returned.
  Question: What is the return policy for clearance items?
  Answer based strictly on the context.
  ```
- **Output:** "Clearance items cannot be returned as they are final sale."

## 7. Minimal Implementation
```python
# Conceptual minimal RAG
def simple_rag(query: str, vector_db, embed_model, llm) -> str:
    # 1. Embed Query
    query_vec = embed_model.encode(query)
    
    # 2. Retrieve
    chunks = vector_db.search(query_vec, top_k=3)
    context = "\n".join(chunks)
    
    # 3. Augment
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    # 4. Generate
    return llm.generate(prompt)
```

## 8. Common Misconceptions
- **"RAG eliminates hallucinations."** RAG *reduces* hallucinations by providing grounding, but does not eliminate them. The model might ignore the context, misunderstand it, or hallucinate if the retrieved context is irrelevant or contradictory.
- **"RAG is just semantic search."** RAG is the full pipeline (Retrieval + Generation). Semantic search is only the retrieval component.
- **"Just put the whole database in the prompt."** LLMs have strict context window limits. Even with massive 1M+ token windows, putting too much data causes "Lost in the Middle" syndrome, degrades reasoning, and heavily increases latency and cost.

## 9. 30-Second Interview Answer
"RAG separates knowledge retrieval from language generation. Instead of relying only on what the model memorized during training, we retrieve relevant external documents—typically via vector search—and provide them as context to the model at inference time. This grounds the model in factual data and significantly reduces hallucinations."

## 10. 2-Minute Interview Answer
"RAG is a framework for grounding LLMs in external data. It consists of two pipelines. In the offline pipeline, documents are parsed, split into smaller chunks, converted to dense vectors using an embedding model, and stored in a vector database. In the online pipeline, the user's query is embedded and used to search the database. We often use hybrid search—combining semantic dense vectors with exact-keyword sparse BM25 search—to maximize retrieval recall. The top retrieved chunks are then passed through a cross-encoder to rerank them for relevance. Finally, these top chunks are injected into the LLM's prompt. By instructing the model to synthesize its answer strictly from the provided context, RAG minimizes hallucinations, allows access to private or real-time data, and avoids the high costs and catastrophic forgetting associated with fine-tuning."

## 11. Follow-Up Questions
- **"What is Hybrid Search?"**
  Using both dense embeddings (semantic meaning, e.g., "fast car" matches "sports vehicle") and sparse keyword search (BM25/TF-IDF, which is better for exact names or serial numbers) to get the best of both worlds.
- **"Why do we need Reranking if we already did retrieval?"**
  Fast vector retrieval (bi-encoders) is less accurate because it relies on pre-computed dot products. A reranker (cross-encoder) processes the query and document *together* through a Transformer, providing highly accurate relevance scores at the cost of being too slow to run on the entire database.

## 12. RAG Failure Analysis (Crucial for Interviews)
When a RAG system provides a bad answer, it is usually one of these:
1. **Bad Retrieval:** The correct document was in the database, but the search didn't find it (e.g., poor chunking strategy or keyword mismatch).
2. **Insufficient Context:** The document was retrieved, but it lacked the specific detail needed to answer fully.
3. **Generation Error:** The correct context was retrieved, but the LLM ignored it, reasoned poorly, or hallucinated.
4. **Conflicting Data:** The database contained contradictory documents (e.g., outdated vs. new policy) and the LLM couldn't resolve the truth.

## 13. Comparison
- **RAG vs. Fine-Tuning:** Fine-tuning adapts a model's *behavior*, format, and tone. It is poor at memorizing new facts. RAG adapts a model's *knowledge* by injecting facts. Use RAG for knowledge; use fine-tuning for behavior.

## 14. What To Remember
- RAG = Retrieval + Augmentation + Generation.
- Distinguish between retrieval quality (did we find it?) and generation quality (did the LLM say it right?).
- Chunks, embeddings, vector DB, hybrid search, reranker.

## 15. Interview Trap
> **Q:** "If an LLM hallucinates facts about our company, should we fine-tune it on our company wiki?"
> **A:** No. Fine-tuning is notoriously bad at reliable knowledge injection and is difficult to update when the wiki changes. You should use RAG to retrieve the wiki pages dynamically.

---
*Connected Concepts:* [Embeddings](embeddings.md), [Vector Databases](vector-databases.md), [Reranking](reranking.md), [Fine-Tuning](../06-llms/fine-tuning.md)
