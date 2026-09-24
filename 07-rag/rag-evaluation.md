# RAG Evaluation

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
