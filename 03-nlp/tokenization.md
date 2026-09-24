# Tokenization

## 1. Definition
Tokenization is the process of breaking down raw text into smaller, discrete chunks (tokens)—such as words, subwords, or characters—that a machine learning model can process.

## 2. Intuition
If you want to teach a child to read, you don't feed them a whole book at once. You break it down into sentences, then words, then syllables. Tokenization is breaking human text into "syllables" that the AI's dictionary recognizes.

## 3. Why it exists
Models cannot process raw strings; they need numbers. If we map every unique English word to a number (Word-level), the dictionary size becomes infinitely large (due to misspellings, plurals, new words). If we map every character (Char-level), the sequences become too long and lose meaning. Subword tokenization exists to balance vocabulary size with sequence length.

## 4. Mechanics
- **Word-Level:** Split by spaces. Huge vocab, fails on Out-Of-Vocabulary (OOV) words.
- **Character-Level:** Split by characters. Tiny vocab (256), but sequences are too long for Transformers.
- **Subword (BPE / WordPiece):** Starts with characters, iteratively merges the most frequently adjacent pairs. "unhappiness" becomes ["un", "happi", "ness"]. Keeps vocab size fixed (e.g., 50k) while handling rare words by breaking them into known chunks.

## 5. Complexity (Time & Space)
- **Time Complexity:** O(N) where N is sequence length for encoding. Training a BPE tokenizer takes time proportional to corpus size.
- **Space Complexity:** O(V) to store the vocabulary mapping in memory.

## 6. Tiny worked example
Sentence: "The AI is learningg"
Subword Tokenization (BPE):
- "The" -> ID: 412
- "AI" -> ID: 8901
- "is" -> ID: 31
- "learning" -> ID: 432
- "g" -> ID: 15 (Handled typo by splitting into known chunks)
Final output: `[412, 8901, 31, 432, 15]`

## 7. Code (Python, with type hints)
```python
from transformers import AutoTokenizer
from typing import List

# Load a pre-trained BPE tokenizer (e.g., from GPT-2 or Llama)
tokenizer = AutoTokenizer.from_pretrained("gpt2")

text: str = "Tokenization is fascinating!"
# Convert string to integer IDs
token_ids: List[int] = tokenizer.encode(text) 
# Decode back to string
decoded_text: str = tokenizer.decode(token_ids)
```

## 8. Common mistakes
- Thinking "Tokens == Words". In modern LLMs (like GPT-4), 1 token is roughly 0.75 words.
- Using a tokenizer from Model A to feed data into Model B (Token IDs are strictly tied to a specific model's embedding matrix).

## 9. 30-second interview answer
"Tokenization breaks raw text into integers so neural networks can process them. Modern LLMs use Subword Tokenization, like Byte-Pair Encoding (BPE), which merges frequent character pairs. This solves the Out-of-Vocabulary problem while keeping the vocabulary size manageable and sequences relatively short."

## 10. 2-minute interview answer
"Tokenization is the critical preprocessing step that bridges raw strings and numerical embeddings. Historically, word-level tokenization resulted in massive, sparse vocabularies and catastrophic Out-Of-Vocabulary failures. We solved this with subword algorithms like Byte-Pair Encoding (BPE), WordPiece, or SentencePiece. BPE is a data-driven compression algorithm: it starts with a base vocabulary of characters and iteratively merges the most frequent pairs in a training corpus until a target vocabulary size (often 30k-100k) is reached. This is brilliant because common words remain single tokens, maximizing context-window efficiency, while rare words or typos are broken down into recognizable phonetic chunks, guaranteeing 100% vocabulary coverage."

## 11. Follow-ups
- "Why can LLMs struggle with rhyming or spelling tasks?" (Because BPE might tokenize "cat" and "hat" completely differently at the subword level, hiding the phonetic spelling from the neural network).

## 12. Deeper questions
- "What is Byte-Level BPE (BBPE)?" (Instead of base characters, it uses the 256 raw bytes. This ensures it can tokenize *any* Unicode character across all languages without needing a massive base vocabulary).

## 13. Related concepts
- **Embeddings**: The step immediately following Tokenization.
- **Context Window**: Measured in Tokens, not words.

## 14. When it breaks / Edge cases
- Tokenizing code or JSON with heavy indentation can waste massive amounts of tokens if spaces aren't merged efficiently by the specific tokenizer.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The very first API call when interacting with any LLM (`tokenizer(text)`).
