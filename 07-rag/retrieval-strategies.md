# RAG Retrieval Strategies

## 1. Definition
Retrieval strategies define how a RAG system searches its database to find the most relevant context for a user's query, moving beyond basic dense vector search to improve accuracy.

## 2. Intuition
If you ask "What is Apple's Q3 revenue?", dense search looks for documents conceptually related to "fruit" or "finance". Keyword search looks for the exact strings "Apple" and "Q3". Using both (Hybrid) gives you the best of both worlds. If the question is complex, rewriting it first (HyDE, Multi-Query) makes it easier to search.

## 3. Why it exists
Naive dense retrieval (just embedding the user query and doing a cosine similarity search) often fails. It struggles with exact keyword matches (IDs, acronyms), and queries are often too short or poorly phrased to match the semantic space of long, formal document chunks.

## 4. Mechanics
- **Dense Retrieval:** Embed query → Cosine similarity with document embeddings. Good for semantic understanding.
- **Sparse Retrieval (BM25):** TF-IDF based keyword matching. Good for exact names, acronyms, and part numbers.
- **Hybrid Search:** Run both Dense and BM25, then combine their scores using Reciprocal Rank Fusion (RRF).
- **Multi-Query:** Use an LLM to generate 3-5 variations of the user's query, retrieve documents for all variations, and take the union. Smooths out phrasing differences.
- **HyDE (Hypothetical Document Embeddings):** Use an LLM to generate a fake, hypothetical answer to the user's query. Embed the fake answer, and use *that* vector to search the DB.

## 5. Complexity (Time & Space)
- **Time:** Advanced strategies increase latency. Multi-query and HyDE require an LLM call *before* retrieval. Hybrid search requires two database queries.
- **Space:** Hybrid requires maintaining both a vector index and an inverted text index.

## 6. Tiny worked example
*Query:* "How to setup SSO with Okta?"
*HyDE Strategy:*
1. Prompt LLM: "Write a document answering: How to setup SSO with Okta?"
2. LLM outputs: "To configure Single Sign-On with Okta, navigate to the admin dashboard, create a SAML 2.0 app, and copy the IdP metadata URL..." (Hypothetical)
3. Embed this rich paragraph.
4. Search DB. It matches the actual documentation much better than the short 6-word query would have.

## 7. Code (Python)
```python
# Conceptual Hybrid Search with Reciprocal Rank Fusion (RRF)
def reciprocal_rank_fusion(dense_ranks, sparse_ranks, k=60):
    rrf_scores = {}
    
    for doc_id, rank in dense_ranks.items():
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (k + rank)
        
    for doc_id, rank in sparse_ranks.items():
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + 1.0 / (k + rank)
        
    # Sort by highest RRF score
    return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
```

## 8. Common mistakes
- Relying exclusively on dense retrieval for domain-specific data containing many IDs or proper nouns. Dense models often fail to distinguish between serial number "AX-552" and "AX-553", whereas BM25 perfectly separates them.
- Ignoring the latency cost of HyDE. Adding an LLM generation step before retrieval adds 1-2 seconds to the TTFB (Time To First Byte).

## 9. 30-second interview answer
"Naive RAG uses only dense vector retrieval, which struggles with exact keywords and short queries. Production RAG uses Hybrid Search, combining dense embeddings with BM25 keyword search via Reciprocal Rank Fusion. For complex queries, strategies like Multi-Query (generating query variations) or HyDE (generating a hypothetical answer to embed) are used to bridge the semantic gap between short queries and long documents."

## 10. 2-minute interview answer
"The biggest point of failure in a RAG pipeline is the retrieval step. If you embed a short user query like 'error 404 deployment', its vector sits in a different semantic space than the dense, formal 500-word documentation chunk that contains the answer. To solve this, we use advanced retrieval strategies. First is Hybrid Search: we combine dense vector search with sparse BM25 keyword search. BM25 catches the exact part numbers or error codes, while dense search catches the semantic meaning. We fuse their results using Reciprocal Rank Fusion (RRF). Second is Query Transformation. Using HyDE (Hypothetical Document Embeddings), we ask an LLM to hallucinate an answer to the query, embed that hallucinated answer, and use it to search. Because the hypothetical answer looks structurally identical to the target document, it yields much higher cosine similarity. Alternatively, we use Multi-Query retrieval, where an LLM rewrites the query into five different perspectives, we retrieve for all five, and take the union of the results. This eliminates the brittleness of specific prompt phrasing."

## 11. Follow-ups
- "What is Reciprocal Rank Fusion?" (A method to combine results from different search algorithms without worrying about absolute score scaling. Score is $1 / (k + \text{rank})$. Top ranked items get the most points).

## 12. Deeper questions
- "How do you handle conversational follow-up questions in RAG?" (Contextual Compression or Query Condensation: pass the chat history and the new question "What is its price?" to an LLM, asking it to rewrite it into a standalone query "What is the price of the iPhone 15?").

## 13. Related concepts
- **Reranking**: Usually applied *after* these retrieval strategies.
- **BM25**: The standard sparse retrieval algorithm based on TF-IDF.

## 14. When it breaks / Edge cases
- HyDE fails if the LLM completely misunderstands the domain and hallucinates a hypothetical document full of entirely wrong keywords, leading retrieval astray.

## 15. Comparison with alternative approaches
- **Dense vs BM25:** Dense understands "puppy" == "dog". BM25 understands "ID-4452" != "ID-4453". Hybrid is required for production.

---
*Where this shows up in ML:*
Building enterprise RAG applications; optimizing LangChain/LlamaIndex pipelines.
