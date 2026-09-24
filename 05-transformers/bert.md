# BERT (Bidirectional Encoder Representations from Transformers)

## 1. Definition
BERT is an encoder-only Transformer pretrained on Masked Language Modeling (MLM) and Next Sentence Prediction (NSP) on large text corpora, producing deeply bidirectional contextual embeddings used for downstream NLP tasks.

## 2. Intuition
When you read the sentence "The bank is by the river," you understand "bank" means shore — not by processing left to right, but by simultaneously seeing all surrounding words ("river", "by"). BERT does exactly this: it reads the entire sentence at once in both directions simultaneously.

## 3. Why it exists
Pre-BERT NLP models like ELMo produced unidirectional representations (either left-to-right or a shallow concatenation). The Transformer encoder natively attends in all directions, but without clever pretraining, it wasn't used for contextual embeddings. BERT was the first to demonstrate that pretraining a large bidirectional Transformer on raw text produces universal representations fine-tunable for nearly any NLP task.

## 4. Mechanics
**Pretraining:**
1. **MLM (Masked Language Modeling):** Randomly mask 15% of tokens (80% → [MASK], 10% → random word, 10% → unchanged). Predict the original tokens from the context.
2. **NSP (Next Sentence Prediction):** Given two sentences, predict if B follows A in the original text. (Criticized in later work; removed in RoBERTa).

**Architecture:** 12 Transformer Encoder layers (BERT-base) or 24 layers (BERT-large). 768 or 1024 dimensional embeddings.

**Fine-tuning:** Prepend [CLS] token. Use [CLS] representation for classification tasks. Use token representations for sequence labeling.

## 5. Complexity (Time & Space)
- **Pretraining:** $O(N^2 d)$ per layer, trillion+ tokens, weeks on TPU pods.
- **Inference:** $O(N^2)$ attention — entire input processed bidirectionally in one pass.

## 6. Tiny worked example
Input: "The [MASK] sat on the mat."
BERT attends to "The", "sat", "on", "the", "mat" simultaneously.
Predicts [MASK] = "cat" with high probability — because these words are more associated with cats than any other animal.

## 7. Code (Python)
```python
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
outputs = model(**inputs)

# outputs.last_hidden_state: (batch, seq_len, 768)
# outputs.pooler_output: (batch, 768) — [CLS] representation
cls_embedding = outputs.pooler_output
```

## 8. Common mistakes
- Using BERT for text generation. BERT is encoder-only; it sees the entire input bidirectionally, making autoregressive generation contradictory with its masked pretraining.
- Forgetting the [CLS] and [SEP] special tokens BERT requires, causing embedding mismatch.

## 9. 30-second interview answer
"BERT is a pretrained encoder-only Transformer using Masked Language Modeling — predicting randomly masked tokens from full bidirectional context. It produces rich contextual embeddings that transfer to almost any NLP classification or sequence labeling task via fine-tuning. RoBERTa improved BERT by removing NSP and training longer with more data."

## 10. 2-minute interview answer
"BERT revolutionized NLP by demonstrating that pretraining a large bidirectional Transformer encoder on raw text corpora — billions of words — produces universal language representations. MLM forces the model to understand deep context: predicting [MASK] requires attending to all surrounding words. Fine-tuning then adapts these representations to specific tasks by adding a small task head and training on labeled data. BERT established the 'pretrain-finetune' paradigm that now dominates NLP. Its successors fixed its weaknesses: RoBERTa removed NSP and trained longer; ALBERT shared weights across layers for parameter efficiency; DistilBERT used knowledge distillation to reduce size 40% with 97% performance; DeBERTa improved attention with disentangled relative positions."

## 11. Follow-ups
- "What is Sentence-BERT (SBERT)?" (BERT fine-tuned with Siamese networks using contrastive loss to make the [CLS] embedding directly meaningful as a sentence similarity metric — enabling efficient semantic search).

## 12. Deeper questions
- "Why does BERT use WordPiece tokenization?" (To handle rare and out-of-vocabulary words by breaking them into known subword units, using a vocabulary of ~30,000 tokens).

## 13. Related concepts
- **GPT**: Decoder-only counterpart — generates text instead of encoding it.
- **RoBERTa**: Improved BERT with better training.

## 14. When it breaks / Edge cases
- BERT's quadratic attention makes it expensive for long documents (>512 tokens). Longformer and BigBird extend BERT's context.

## 15. Comparison with alternative approaches
- **vs GPT:** BERT is better for understanding tasks (classification, NER, QA). GPT is better for generation. In the current era, decoder-only LLMs have surpassed BERT on most benchmarks when instruction-tuned.

---
*Where this shows up in ML:*
Embedding generation for RAG pipelines, sentiment analysis, NER, question answering. Sentence-BERT embeddings are widely used for semantic search.
