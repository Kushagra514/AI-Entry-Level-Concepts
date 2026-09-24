# RAG Overview (Retrieval-Augmented Generation)

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
    context = "
".join(context_chunks)
    prompt = f"Context:
{context}

Answer the query: {query}"
    
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
