# RAG Chunking

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
