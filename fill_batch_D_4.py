import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch D)"')

wc("07-rag/chunking.md", r"""# RAG Chunking

## 1. Definition
Chunking is the process of breaking large documents into smaller, semantically meaningful pieces of text before embedding and indexing them in a vector database for Retrieval-Augmented Generation (RAG).

## 2. Intuition
You can't embed an entire 500-page book into a single vector and expect to retrieve a specific paragraph about a character. The vector would average out all meaning. Chunking slices the book into paragraphs so you can find exactly the paragraph you need.

## 3. Why it exists
Embedding models have fixed context limits (e.g., 512 or 8192 tokens). Furthermore, dense retrieval relies on vector similarity; smaller, focused chunks yield more accurate similarity scores for specific queries than massive, multi-topic documents.

## 4. Mechanics
- **Fixed-size chunking:** Split by a fixed number of characters or tokens (e.g., 500 tokens). Fast but can cut sentences in half.
- **Overlap:** Include a sliding window (e.g., 50 tokens overlap) so context isn't lost if a concept spans a boundary.
- **Sentence/Paragraph chunking:** Split on natural boundaries (periods, newlines).
- **Semantic chunking:** Use a smaller NLP model or LLM to determine boundaries where the topic shifts.
- **Recursive chunking:** Try to split by paragraphs; if still too large, split by sentences; if still too large, split by words (standard in LangChain).

## 5. Complexity (Time & Space)
- **Time:** $O(N)$ where $N$ is text length. Semantic chunking can be much slower.
- **Space:** Increases storage requirements because of overlaps and metadata per chunk.

## 6. Tiny worked example
Text: "The sky is blue. The grass is green. The sun is hot."
Fixed chunking (size=4 words, overlap=1):
Chunk 1: "The sky is blue."
Chunk 2: "blue. The grass is" -> Semantic disaster!
Sentence chunking:
Chunk 1: "The sky is blue."
Chunk 2: "The grass is green."

## 7. Code (Python)
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text = "Your very long document text goes here..."

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_text(text)
print(f"Split into {len(chunks)} chunks.")
```

## 8. Common mistakes
- **Too large chunks:** Dilutes the semantic meaning; relevant details get lost in the noise of the rest of the chunk.
- **Too small chunks:** Loses necessary context (e.g., retrieving the pronoun "He" without the preceding sentence that names the person).
- **No overlap:** Slicing a crucial sentence exactly in half across two chunks.

## 9. 30-second interview answer
"Chunking breaks large documents into smaller pieces for embedding. We do this because embedding models have token limits, and smaller chunks yield higher-quality, more specific vector similarities. The standard approach is recursive character chunking with overlap to preserve boundaries, while advanced pipelines use semantic chunking."

## 10. 2-minute interview answer
"Chunking is the foundational step of a RAG pipeline that dictates retrieval quality. If you embed an entire document, the resulting vector is an average of all its topics, making it impossible to match specific queries. If chunks are too small, they lack the context the LLM needs to generate an answer. The industry baseline is Recursive Character Chunking with a 10-20% overlap, which attempts to split on paragraphs, then sentences, then words. A more advanced strategy is Parent-Child (or Small-to-Big) retrieval: you chunk the document into very small, specific sentences for precise vector matching, but when a match is found, you pass the parent paragraph to the LLM to provide full context. Evaluating chunking strategies requires looking at your downstream RAG metrics like context precision and recall."

## 11. Follow-ups
- "What is Parent-Child (Small-to-Big) retrieval?" (Embed small sentence-level chunks for high-precision search. When retrieved, instead of giving the small chunk to the LLM, give it the larger parent paragraph the chunk belongs to).

## 12. Deeper questions
- "How does semantic chunking work?" (You compute embeddings for every sentence, calculate the cosine similarity between adjacent sentences, and set a chunk boundary wherever the similarity drops below a certain threshold, indicating a topic shift).

## 13. Related concepts
- **Embedding Models**: What consumes the chunks.
- **Vector Databases**: Where the chunks and vectors are stored.

## 14. When it breaks / Edge cases
- Code files: Standard text chunking destroys code logic. You must use AST-based (Abstract Syntax Tree) chunking to keep functions and classes intact.

## 15. Comparison with alternative approaches
- **Fixed vs Semantic:** Fixed is fast and cheap. Semantic is slow and requires embedding calls during preprocessing, but yields higher retrieval quality.

---
*Where this shows up in ML:*
Data ingestion pipelines for every RAG system (LangChain, LlamaIndex).
""")

wc("07-rag/vector-databases.md", r"""# Vector Databases

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
""")

wc("07-rag/cosine-similarity.md", r"""# Cosine Similarity

## 1. Definition
Cosine Similarity measures the cosine of the angle between two non-zero vectors. It determines how similar two vectors are in orientation, regardless of their magnitude (length).

## 2. Intuition
Imagine two arrows starting from the origin. If they point in the exact same direction, they represent the same concept, even if one is longer than the other. Cosine similarity ignores the length and only cares about the angle. 

## 3. Why it exists
In NLP, document embeddings capture semantic meaning in their direction. The magnitude of a vector often just represents the frequency of words or document length. Cosine similarity isolates the semantic direction, making it the standard metric for comparing text embeddings.

## 4. Mechanics
- **Formula:** $\cos(\theta) = \frac{A \cdot B}{||A||_2 ||B||_2} = \frac{\sum A_i B_i}{\sqrt{\sum A_i^2} \sqrt{\sum B_i^2}}$
- **Range:** 
  - $1$: Exactly the same direction.
  - $0$: Orthogonal (completely unrelated).
  - $-1$: Exactly opposite direction.
- **Equivalence:** If vectors $A$ and $B$ are L2-normalized (length = 1), then Cosine Similarity is exactly equal to the Dot Product $A \cdot B$.

## 5. Complexity (Time & Space)
- **Time:** $O(d)$ where $d$ is the number of dimensions.
- **Space:** $O(1)$ auxiliary space.

## 6. Tiny worked example
$A = [3, 0]$, $B = [0, 4]$ (Orthogonal, angle 90)
$A \cdot B = 0$. Cosine Sim = 0.

$A = [2, 2]$, $B = [5, 5]$ (Same direction, angle 0)
$A \cdot B = 20$. 
$||A|| = \sqrt{8}$, $||B|| = \sqrt{50}$.
Cos Sim = $20 / (\sqrt{8}\sqrt{50}) = 20 / \sqrt{400} = 20 / 20 = 1$.

## 7. Code (Python)
```python
import numpy as np

def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

# Or using PyTorch
import torch
import torch.nn.functional as F

a = torch.tensor([1.0, 2.0])
b = torch.tensor([2.0, 4.0])
# Equivalent to cosine similarity when dim=0
sim = F.cosine_similarity(a, b, dim=0) 
```

## 8. Common mistakes
- Using Euclidean distance (L2 distance) on unnormalized vectors to measure semantic similarity. A very long document and a very short document about the exact same topic might have a huge Euclidean distance but a Cosine Similarity of 1.
- Re-calculating the denominator at inference time. In production RAG, all document vectors are L2-normalized upon ingestion. The query vector is normalized. Then, similarity is just a fast dot product.

## 9. 30-second interview answer
"Cosine similarity measures the angle between two vectors, defined as their dot product divided by the product of their magnitudes. It ranges from -1 to 1. It is the standard metric for comparing text embeddings because it captures semantic direction while ignoring vector magnitude, which is often an artifact of document length."

## 10. 2-minute interview answer
"Cosine similarity is the fundamental distance metric in vector search and RAG. Computed as $\frac{A \cdot B}{||A|| \cdot ||B||}$, it isolates the directional alignment of two high-dimensional vectors. In NLP, the direction of an embedding vector encodes its semantic meaning, while its magnitude often correlates with token count or word frequency. If we used Euclidean distance, a short summary and a long article about the same topic would appear distant. Cosine similarity correctly identifies them as conceptually identical. In production vector databases, we heavily optimize this: we L2-normalize all vectors (setting their magnitude to 1) during ingestion. When vectors are normalized, the denominator of the cosine formula becomes 1, meaning Cosine Similarity mathematically reduces to the simple Dot Product. Dot products are highly optimized in hardware via BLAS/CUDA, allowing us to compare a query against millions of documents in milliseconds."

## 11. Follow-ups
- "What is the relationship between Cosine Similarity and Euclidean Distance on normalized vectors?" (They are monotonically related: $||A-B||^2 = ||A||^2 + ||B||^2 - 2A\cdot B = 2 - 2\cos(\theta)$. Minimizing L2 distance is identical to maximizing cosine similarity for normalized vectors).

## 12. Deeper questions
- "Why does the Transformer Attention mechanism use Dot Product instead of Cosine Similarity?" (Attention wants to capture both direction and magnitude. A larger magnitude key vector might represent a more 'important' or 'confident' concept that should exert more pull on the query).

## 13. Related concepts
- **Dot Product**: Unnormalized version.
- **Euclidean Distance**: Distance between endpoints rather than angle.

## 14. When it breaks / Edge cases
- Fails if a vector is all zeros (division by zero).

## 15. Comparison with alternative approaches
- **Cosine vs Jaccard:** Jaccard is for discrete sets (bag of words). Cosine is for dense continuous embeddings.

---
*Where this shows up in ML:*
Vector databases, RAG, Word2Vec evaluation, contrastive learning (SimCLR, CLIP loss).
""")

wc("07-rag/retrieval-strategies.md", r"""# RAG Retrieval Strategies

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
""")

wc("07-rag/reranking.md", r"""# Reranking in RAG

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
""")

wc("07-rag/rag-evaluation.md", r"""# RAG Evaluation

## 1. Definition
RAG Evaluation is the systematic measurement of a Retrieval-Augmented Generation pipeline's performance, isolating the quality of the retrieval component (did we find the right docs?) from the generation component (did the LLM answer correctly without hallucinating?).

## 2. Intuition
If your RAG chatbot gives a wrong answer, you need to know whose fault it is. Did the database fail to provide the right document? (Retrieval failure). Or did the database provide the perfect document, but the LLM ignored it and made something up? (Generation failure).

## 3. Why it exists
Standard ML metrics (Accuracy, F1, BLEU) don't work for open-ended LLM text generation. Human evaluation is the gold standard but is too slow and expensive for CI/CD pipelines. We need automated, scalable metrics to tune chunk sizes, embedding models, and prompts.

## 4. Mechanics
**RAGAS Framework (Retrieval Augmented Generation Assessment):** uses an "LLM-as-a-judge" to score four key metrics:
- **Context Precision:** Are the relevant documents ranked at the top of the retrieved context?
- **Context Recall:** Did the retrieved context contain all the information needed to answer the question? (Requires ground-truth answer).
- **Faithfulness:** Are all claims in the generated answer supported by the retrieved context? (Measures hallucination).
- **Answer Relevancy:** Does the generated answer directly address the user's question, without going on tangents?

## 5. Complexity (Time & Space)
- Evaluating a dataset of 100 questions with LLM-as-a-judge requires hundreds of API calls. It is computationally expensive and is typically run offline on a golden test set.

## 6. Tiny worked example
Question: "Where was Einstein born?"
Retrieved Context: "Einstein was a physicist born in Ulm, Germany."
Generated Answer: "Einstein was born in Ulm, Germany. He won the Nobel prize."
- Context Recall: High (Ulm, Germany is in the context).
- Faithfulness: Low (The Nobel prize claim is factually true, but NOT in the context. This is an extrinsic hallucination in RAG).

## 7. Code (Python)
```python
# Conceptual implementation of Faithfulness using LLM-as-judge
def evaluate_faithfulness(question, context, answer, llm_judge):
    prompt = f'''
    Context: {context}
    Answer: {answer}
    Extract all factual claims from the Answer. 
    For each claim, check if it is explicitly supported by the Context.
    Return the ratio of supported claims to total claims.
    '''
    score = llm_judge.generate(prompt)
    return float(score)

# In practice, use the ragas library:
# from ragas import evaluate
# from ragas.metrics import faithfulness, answer_relevancy
# result = evaluate(dataset, metrics=[faithfulness, answer_relevancy])
```

## 8. Common mistakes
- Only evaluating the final answer. If you change the embedding model and the answer gets worse, you won't know if the new embeddings are bad, or if the LLM just disliked the new chunk boundaries.
- Using simple string matching (BLEU/ROUGE) against a ground truth answer. LLMs paraphrase; "USA" and "United States" will be penalized by ROUGE but are semantically identical.

## 9. 30-second interview answer
"RAG evaluation must decouple retrieval quality from generation quality. We typically use frameworks like RAGAS, which employs an LLM-as-a-judge paradigm. For retrieval, we measure Context Precision and Context Recall. For generation, we measure Faithfulness (is the answer grounded entirely in the retrieved context, avoiding hallucinations?) and Answer Relevancy. This automated evaluation allows iterative tuning of the RAG pipeline."

## 10. 2-minute interview answer
"Evaluating RAG is uniquely challenging because it requires assessing a non-deterministic generative system. The industry standard approach is LLM-as-a-judge, formalized in frameworks like RAGAS or TruLens. We break evaluation into the RAG triad: Retrieval, Generation, and Relevance. To evaluate Retrieval, we measure Context Recall (did we retrieve the facts needed to answer the ground-truth question?) and Context Precision (were those facts at the top of the results?). To evaluate Generation, the most critical metric is Faithfulness. An LLM breaks the answer down into individual claims and checks if each claim can be logically deduced from the retrieved context. If an LLM answers correctly using its internal parametric memory, but the fact wasn't in the context, it is penalized for lack of faithfulness—because in an enterprise setting, ungrounded answers are hallucinations. Finally, Answer Relevancy ensures the generated text actually answers the user's prompt without waffling. By tracking these specific metrics, we can pinpoint whether an error requires fixing the chunking strategy, upgrading the embedding model, or tweaking the LLM's system prompt."

## 11. Follow-ups
- "What are the drawbacks of LLM-as-a-judge?" (It introduces its own biases, such as preferring longer answers, preferring its own writing style, and struggling with complex reasoning. It also costs API credits to run evaluations).

## 12. Deeper questions
- "How do you create a golden evaluation dataset if you don't have human labelers?" (Use a powerful model like GPT-4 to read your raw documents and synthetically generate Question-Answer pairs based on those documents. Then evaluate your smaller RAG system against this synthetic test set).

## 13. Related concepts
- **Hallucination**: Faithfulness directly measures this.
- **Precision and Recall**: Traditional IR metrics adapted for semantic context.

## 14. When it breaks / Edge cases
- LLM judges often fail on tasks requiring strict mathematical verification or code execution, returning high faithfulness scores for flawed logic.

## 15. Comparison with alternative approaches
- **LLM-as-judge vs Human Evaluation:** Humans are accurate but slow/expensive. LLMs are fast, scale well, and correlate strongly with human judgments on basic RAG metrics.

---
*Where this shows up in ML:*
MLOps for LLMs; building test suites for AI applications before pushing to production.
""")

wc("08-efficient-llms/quantization.md", r"""# Quantization

## 1. Definition
Quantization is the process of mapping high-precision neural network parameters (weights and activations, typically 32-bit floating point) to lower-precision data types (like 8-bit or 4-bit integers) to reduce memory footprint and increase inference speed, with minimal loss in accuracy.

## 2. Intuition
Imagine a high-res photograph taking up 10 MB. You can compress it to a 1 MB JPEG. The colors might be slightly less precise if you zoom in, but to the human eye, it looks the same. Quantization does this to neural network weights, shrinking a 28GB model to 4GB so it fits on a laptop GPU.

## 3. Why it exists
LLMs are massively memory-bound. A 70-Billion parameter model requires ~140 GB of VRAM just to load in 16-bit precision (requiring 2x 80GB A100 GPUs costing $30k). Quantizing to 4-bit reduces this to ~35 GB, allowing deployment on vastly cheaper consumer hardware. Furthermore, lower precision allows faster memory bandwidth transfer, speeding up inference.

## 4. Mechanics
- **Data Types:** FP32 (Full precision), FP16/BF16 (Half precision, standard for LLMs), INT8, INT4, NF4 (NormalFloat4, optimized for normally distributed weights).
- **Scaling Factor:** To convert a float tensor to INT8: $X_{int8} = \text{round}(X_{float} / S) + Z$. $S$ is the scale (e.g., $\max(|X|) / 127$), $Z$ is the zero-point.
- **PTQ (Post-Training Quantization):** Take a fully trained model and quantize it. Methods: GPTQ, AWQ, SmoothQuant.
- **QAT (Quantization-Aware Training):** Simulate quantization errors during the training forward pass, so the model learns to be robust to them. Yields better accuracy but requires retraining.

## 5. Complexity (Time & Space)
- **Memory reduction:** FP16 to INT8 halves memory (2x reduction). FP16 to INT4 is a 4x reduction.
- **Speed:** Can increase speed by 2-3x because reading weights from GPU memory (HBM) is the bottleneck in LLM inference.

## 6. Tiny worked example
Weights: `[-1.2, 0.4, 2.8, -3.0]` (FP32)
Map to INT8 range `[-127, 127]`. Max absolute value is 3.0.
Scale factor $S = 3.0 / 127 \approx 0.0236$.
Quantized: `[-1.2/S, 0.4/S, 2.8/S, -3.0/S]` -> Round -> `[-51, 17, 119, -127]`.
Dequantized at inference: `[-51*S, ...]` -> `[-1.203, 0.401, 2.808, -3.0]`. Tiny precision loss introduced!

## 7. Code (Python)
```python
# Using HuggingFace bitsandbytes for 4-bit quantization
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# Configure QLoRA's 4-bit NormalFloat quantization
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",       # NormalFloat 4-bit
    bnb_4bit_compute_dtype=torch.bfloat16, # Compute in 16-bit
    bnb_4bit_use_double_quant=True   # Quantize the quantization constants
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b",
    quantization_config=quant_config,
    device_map="auto"
)
# A 7B model now takes ~4GB VRAM instead of 14GB!
```

## 8. Common mistakes
- Naive round-to-nearest quantization for LLMs. LLMs feature massive "outliers" in their activations (values 100x larger than others). Naive scaling based on the max value crushes all normal values to zero, destroying the model.
- Thinking compute happens in 4-bit. In frameworks like bitsandbytes, weights are stored in 4-bit, but dequantized to 16-bit on the fly in SRAM before the matrix multiplication happens.

## 9. 30-second interview answer
"Quantization reduces the precision of model weights (e.g., from 16-bit to 4-bit integers) to drastically reduce memory footprint and increase inference speed. For LLMs, Post-Training Quantization (PTQ) techniques like GPTQ or AWQ are standard, carefully managing outlier activations to preserve accuracy. QLoRA utilizes NF4 quantization to allow fine-tuning of massive models on single consumer GPUs."

## 10. 2-minute interview answer
"Quantization is the primary reason open-source LLMs are accessible today. Because LLM inference is memory-bandwidth bound, shrinking weights from 16-bit floats to 4-bit integers not only cuts VRAM usage by 75% but also dramatically speeds up generation. The challenge is the 'outlier problem'. At scale, LLMs develop specific feature dimensions with extreme magnitude. If you naively scale a tensor to an 8-bit integer based on its maximum value, these outliers force the scaling factor to be so large that 99% of the normal weights get rounded to zero, ruining the model. Modern PTQ algorithms solve this elegantly. SmoothQuant migrates the difficulty from activations to weights mathematically. GPTQ uses second-order Hessian information to adjust the remaining weights to compensate for the quantization error of the rounded weights. For fine-tuning, QLoRA introduced NF4 (NormalFloat4), a data type theoretically optimal for normally distributed weights, allowing us to store the base model in 4-bit while computing gradients for 16-bit LoRA adapters."

## 11. Follow-ups
- "What is the difference between weight-only quantization and weight-activation quantization?" (Weight-only stores weights in INT4/8 but computes in FP16. Solves memory bottlenecks. Weight-activation quantizes both, allowing the use of INT8 tensor cores for math, speeding up compute bottlenecks, but is much harder to maintain accuracy).

## 12. Deeper questions
- "What is Double Quantization in QLoRA?" (Quantization produces scaling constants for every block of weights. Double Quantization quantizes those scaling constants themselves from 32-bit to 8-bit, saving an additional ~0.4 bits per parameter).

## 13. Related concepts
- **QLoRA**: Relies entirely on 4-bit quantization.
- **Inference Optimization**: Quantization is a pillar of fast serving.

## 14. When it breaks / Edge cases
- Sub-4-bit quantization (like 2-bit or 1-bit/Ternary models like BitNet) currently causes severe degradation in reasoning capabilities and requires specialized Quantization-Aware Training from scratch.

## 15. Comparison with alternative approaches
- **Quantization vs Pruning:** Pruning removes weights entirely (sets to zero). Quantization reduces the precision of all weights. Quantization currently yields much better performance retention for LLMs than unstructured pruning.

---
*Where this shows up in ML:*
Deploying models via llama.cpp (GGUF format), vLLM (AWQ/GPTQ formats), and QLoRA fine-tuning.
""")

wc("08-efficient-llms/distillation.md", r"""# Knowledge Distillation

## 1. Definition
Knowledge Distillation is a model compression technique where a small, fast "Student" model is trained to mimic the behavior, outputs, and internal representations of a large, accurate "Teacher" model.

## 2. Intuition
The Teacher is a grandmaster who knows exactly why a move is good. The Student is a beginner. If the Student only learns from win/loss labels (hard targets), they learn slowly. If the Teacher explains the probabilities of *all* possible moves (soft targets), the Student learns the rich internal logic and improves much faster.

## 3. Why it exists
Large models (like GPT-4 or BERT-Large) are too expensive and slow for real-time inference or edge devices. Distillation transfers the generalization capabilities of a 100-billion parameter model into a 1-billion parameter model that can run on a phone.

## 4. Mechanics
- **Hard Targets:** The actual ground-truth label (e.g., `[1, 0, 0]`).
- **Soft Targets:** The probability distribution output by the Teacher (e.g., `[0.8, 0.15, 0.05]`). The 0.15 indicates class 2 is somewhat similar to class 1, providing rich "dark knowledge".
- **Temperature Scaling:** A high temperature $T$ is applied to the softmax of both Teacher and Student during training to soften the probabilities and amplify the signals of the non-winning classes.
- **Loss Function:** $\mathcal{L} = \alpha \cdot \text{CE}(\text{Student}, \text{Hard}) + (1-\alpha) \cdot T^2 \cdot \text{KL}(\text{Student\_Soft}, \text{Teacher\_Soft})$
- **Feature matching:** Advanced distillation also forces the Student's hidden states/attention matrices to match the Teacher's.

## 5. Complexity (Time & Space)
- **Time:** Training is expensive (requires running forward passes of the massive Teacher).
- **Space:** Student is drastically smaller, achieving 10x-100x inference speedups.

## 6. Tiny worked example
Image classification: Dog vs Cat vs Car.
Image is a Dog.
Hard target: `[1, 0, 0]`
Teacher output (Soft): `[0.85, 0.14, 0.01]` (The teacher knows a dog looks a bit like a cat, but nothing like a car).
Training the student on the soft targets teaches it that dog and cat features overlap, information entirely missing from the hard target.

## 7. Code (Python)
```python
import torch.nn.functional as F

def distillation_loss(student_logits, teacher_logits, true_labels, T=2.0, alpha=0.5):
    # Standard supervised loss (Hard Targets)
    hard_loss = F.cross_entropy(student_logits, true_labels)
    
    # Distillation loss (Soft Targets with Temperature)
    student_soft = F.log_softmax(student_logits / T, dim=-1)
    teacher_soft = F.softmax(teacher_logits / T, dim=-1)
    
    # KL Divergence between softened distributions
    soft_loss = F.kl_div(student_soft, teacher_soft, reduction='batchmean')
    
    # Combine (multiply soft_loss by T^2 to scale gradients properly)
    return (alpha * hard_loss) + ((1 - alpha) * (T ** 2) * soft_loss)
```

## 8. Common mistakes
- Not multiplying the distillation loss by $T^2$. Since gradients scale by $1/T^2$ when temperature is applied to softmax, failing to multiply by $T^2$ makes the soft loss contribution vanish.
- Distilling a massive LLM purely by generating text (black-box distillation) and calling it equivalent to logit distillation (white-box). Generating text only transfers the top-1 choices, missing the rich probability distribution.

## 9. 30-second interview answer
"Knowledge Distillation transfers knowledge from a large Teacher model to a smaller Student model. Instead of training the Student only on ground-truth labels, it is trained to match the soft probability distribution output by the Teacher. By raising the softmax temperature, the Student learns the relative probabilities of incorrect classes (dark knowledge), resulting in a compact model with much higher accuracy than if trained from scratch."

## 10. 2-minute interview answer
"Knowledge Distillation is the premier technique for deploying state-of-the-art models to production environments with strict latency budgets. Introduced formally by Hinton, the core concept is training a Student model to match the Teacher's 'soft targets' — the full probability distribution over the vocabulary. This distribution contains 'dark knowledge'; for example, a language model predicting the next word after 'I am going to the' will assign high probability to 'store' and 'park', and zero to 'jump'. Training on this distribution teaches the Student the semantic relationships between words much faster than a one-hot ground truth label. We use a Temperature parameter in the softmax to flatten the Teacher's distribution, exposing the probabilities of the lesser-likely tokens. In modern LLMs, we see Distillation used heavily: DistilBERT retained 97% of BERT's performance with 40% fewer parameters. Today, open-source models often undergo 'Step-by-Step' distillation, where a Student is trained on Chain-of-Thought reasoning traces generated by GPT-4, transferring reasoning capabilities into much smaller models."

## 11. Follow-ups
- "What is white-box vs black-box distillation?" (White-box requires access to the Teacher's logits/hidden states. Black-box only requires the Teacher's text output. Generating synthetic data using GPT-4 to train open-source models is black-box distillation).

## 12. Deeper questions
- "How did DistilBERT work?" (It initialized the student with every other layer of the Teacher BERT model, then trained using a linear combination of Masked Language Modeling loss, distillation loss on the logits, and cosine embedding loss on the hidden states).

## 13. Related concepts
- **Quantization**: Often combined with distillation for maximum compression.
- **Model Pruning**: Removing weights; distillation is training a smaller architecture from scratch.

## 14. When it breaks / Edge cases
- If the Student capacity is too small, forcing it to mimic complex Teacher distributions can actually harm performance compared to just training it on hard labels.

## 15. Comparison with alternative approaches
- **Distillation vs Quantization:** Quantization keeps the exact same architecture but lowers precision (no retraining needed). Distillation trains a brand new, smaller architecture.

---
*Where this shows up in ML:*
DistilBERT, TinyBERT, using GPT-4 to generate training data for smaller models (Alpaca, Vicuna).
""")

wc("08-efficient-llms/inference-optimization.md", r"""# LLM Inference Optimization

## 1. Definition
LLM Inference Optimization encompasses hardware-aware algorithms and systems engineering techniques designed to maximize generation throughput (tokens/second) and minimize latency (Time To First Byte) during autoregressive text generation.

## 2. Intuition
Generating text with a 70B model is like moving a mountain of data for a spoonful of math. Every time you generate a single word, you have to read 140GB of weights from the GPU memory into the processor. To make this fast, we need to minimize memory movement, batch requests smartly, and cache everything we can.

## 3. Why it exists
LLM inference is fundamentally **Memory-Bandwidth Bound**, not Compute-Bound. The math (matrix-vector multiplication) is fast, but waiting for the weights to travel from HBM (High Bandwidth Memory) to SRAM takes forever. Optimization techniques tackle this bottleneck.

## 4. Mechanics
- **KV-Cache:** Stores the Key and Value vectors of past tokens to prevent $O(N^2)$ recomputation.
- **Continuous Batching (In-flight Batching):** Traditional batching waits for the longest sentence to finish before starting a new batch. Continuous batching ejects finished requests and inserts new ones at the token level, vastly increasing throughput.
- **PagedAttention (vLLM):** KV-cache grows unpredictably. Traditional allocators pre-allocate max memory, wasting 60-80% to fragmentation. PagedAttention divides KV-cache into blocks (like OS virtual memory), allowing non-contiguous storage and near-zero waste, allowing much larger batch sizes.
- **FlashAttention:** Fuses the QKV attention operations in SRAM to avoid reading/writing the $N \times N$ attention matrix to slow HBM.
- **Speculative Decoding:** A small 1B draft model generates 4 tokens quickly. The large 70B model verifies all 4 tokens in a single forward pass. Speeds up latency 2-3x without changing the output distribution.

## 5. Complexity (Time & Space)
- Optimization targets the constant factors of memory IO and batch utilization, yielding 10x to 24x throughput improvements in production systems (e.g., vLLM vs naive HuggingFace).

## 6. Tiny worked example
*Traditional Batching:* Req A (3 tokens), Req B (6 tokens). Req A finishes in 3 steps, GPU idles that slot for 3 more steps waiting for B.
*Continuous Batching:* Req A finishes. Step 4 instantly slots in Req C. 100% GPU utilization.

## 7. Code (Python)
```python
# Utilizing optimized inference engines rather than native PyTorch
from vllm import LLM, SamplingParams

# vLLM automatically handles PagedAttention, Continuous Batching, 
# and FlashAttention under the hood.
llm = LLM(model="meta-llama/Llama-2-7b-chat-hf")
prompts = ["Hello, my name is", "The president of the US is"]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

# This executes with massive throughput compared to HuggingFace .generate()
outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print(output.outputs[0].text)
```

## 8. Common mistakes
- Benchmarking LLMs using `batch_size=1`. LLM throughput scales massively with batch size up to the VRAM limit because loading the weights once can serve 100 requests simultaneously.
- Using native `transformers` `model.generate()` in production. It lacks continuous batching and PagedAttention. Use vLLM, TensorRT-LLM, or TGI.

## 9. 30-second interview answer
"LLM autoregressive generation is memory-bandwidth bound. To optimize it, we use the KV-Cache to avoid recomputation, FlashAttention to avoid HBM read/writes during attention, and Continuous Batching to maximize GPU utilization. Most importantly, systems like vLLM use PagedAttention to manage the KV-cache in non-contiguous blocks, eliminating memory fragmentation and allowing much larger batch sizes, increasing throughput by up to 24x."

## 10. 2-minute interview answer
"Optimizing LLM inference requires shifting focus from FLOPs to memory bandwidth. Because autoregressive generation requires loading the entire model weights from HBM to SRAM for every single generated token, the GPU's compute cores sit idle waiting for data. We optimize this at three levels. First, algorithmically: the KV-cache saves past Key/Value states so we only compute attention for the new token. Second, at the kernel level: FlashAttention fuses the attention calculation in SRAM, preventing the $O(N^2)$ intermediate matrix from ever touching slow memory. Third, at the systems level: engines like vLLM use Continuous Batching to slot new requests in at the token level, and PagedAttention to manage KV-cache memory like OS virtual memory. Before PagedAttention, unpredictable sequence lengths caused massive memory fragmentation, limiting batch sizes. By allocating non-contiguous blocks, vLLM maximizes batch size, which means loading the model weights once serves many more requests, drastically increasing tokens-per-second throughput. For latency-sensitive applications, we add Speculative Decoding, using a tiny draft model to guess tokens and the large model to verify them in parallel."

## 11. Follow-ups
- "What is Tensor Parallelism?" (Splitting the weight matrices of a single model across multiple GPUs. Necessary when a model (like 70B) doesn't fit on one GPU. Communication happens via All-Reduce operations across NVLink).

## 12. Deeper questions
- "How does Speculative Decoding guarantee the exact same output distribution as the target model?" (By using a specific rejection sampling scheme. If the target model's probability for the draft token is higher than the draft model's, it's accepted. If lower, it's accepted with probability $p_{target}/p_{draft}$, otherwise rejected and resampled from the target distribution).

## 13. Related concepts
- **Quantization**: Reduces weight size, directly tackling the memory-bandwidth bottleneck.
- **Autoregressive Generation**: The process being optimized.

## 14. When it breaks / Edge cases
- Very long context lengths (e.g., 100k) cause the KV-cache size to exceed the model weight size, shifting the bottleneck and requiring techniques like Ring Attention (distributing context across GPUs).

## 15. Comparison with alternative approaches
- N/A — these are compounding optimizations, typically all used together in modern serving engines.

---
*Where this shows up in ML:*
MLOps, deploying models using vLLM, TGI, or TensorRT-LLM.
""")

print("Batch D Part 4 complete")
