# Encoder-Decoder Architecture

## 1. Definition
The Encoder-Decoder Transformer is a full Transformer architecture where an Encoder processes the input sequence into a latent representation, and a Decoder generates the output sequence autoregressively, attending to the encoder's output via Cross-Attention.

## 2. Intuition
The Encoder is a reader who deeply comprehends a source text (e.g., an English sentence), compressing its meaning into a rich contextual representation. The Decoder is a writer who reads both that compressed understanding (Cross-Attention) and their own generated output so far (Masked Self-Attention) to produce the next word in the target language.

## 3. Why it exists
Sequence-to-sequence tasks (translation, summarization) require understanding the full input before generating output. Encoder-Decoder separates concerns: the Encoder builds full bidirectional context over the entire source; the Decoder generates output conditioned on that encoded context.

## 4. Mechanics
**Encoder:** Takes source tokens, processes them through $N$ blocks of [Multi-Head Self-Attention + FFN] with residual connections. Each token attends to all other source tokens (bidirectional). Outputs a sequence of contextualized embeddings.

**Decoder:** Takes target tokens (shifted right during training). Each block has:
1. **Masked Self-Attention:** Attend only to previous target tokens.
2. **Cross-Attention:** $Q$ from decoder, $K$ and $V$ from encoder output.
3. **FFN.**

**Training:** Teacher forcing — feed the ground-truth previous tokens as input.
**Inference:** Autoregressive — generate one token at a time, each fed back as input.

## 5. Complexity (Time & Space)
- **Encoder:** $O(N_s^2 d)$ per layer ($N_s$ = source length).
- **Decoder:** $O(N_t^2 d + N_t N_s d)$ per layer ($N_t$ = target length, second term = Cross-Attention).

## 6. Tiny worked example
Translation: "Hello" → "Bonjour".
- Encoder processes "Hello" → contextual embedding $e_{\text{hello}}$.
- Decoder Step 1: Input `[BOS]`. Cross-attends to $e_{\text{hello}}$. Predicts "Bonjour".
- Decoder Step 2: Input `[BOS, Bonjour]`. Predicts `[EOS]`. Generation complete.

## 7. Code (Python)
```python
import torch.nn as nn

enc_layer = nn.TransformerEncoderLayer(d_model=512, nhead=8)
dec_layer = nn.TransformerDecoderLayer(d_model=512, nhead=8)

encoder = nn.TransformerEncoder(enc_layer, num_layers=6)
decoder = nn.TransformerDecoder(dec_layer, num_layers=6)

# memory = encoder output; tgt = target sequence
# memory = encoder(src)
# out = decoder(tgt, memory, tgt_mask=causal_mask)
```

## 8. Common mistakes
- Forgetting causal masking in the Decoder's Self-Attention. Without it, the decoder sees future target tokens during training — it would trivially copy the next token and learn nothing.
- Confusing Cross-Attention source: Cross-Attention $K$ and $V$ come from the **encoder output** (constant across all decoder layers), not from the decoder's own activations.

## 9. 30-second interview answer
"The Encoder-Decoder Transformer processes source sequences bidirectionally (Encoder) and generates target sequences autoregressively (Decoder). The Decoder attends to the Encoder output via Cross-Attention ($Q$ from decoder, $K/V$ from encoder). It's used for translation (BART, T5), summarization, and any seq2seq task where full source understanding is needed before output generation."

## 10. 2-minute interview answer
"Encoder-Decoder models are designed for transduction tasks — mapping one sequence to another of potentially different length and vocabulary. The Encoder builds a rich, bidirectional representation of the source, with each token attending to the entire source context. The Decoder generates the target autoregressively: at each step it has access to its own previously generated tokens via Masked Self-Attention, and to the full encoded source via Cross-Attention. This two-phase design is optimal for tasks where full source comprehension precedes generation. Compared to decoder-only models (GPT), encoder-decoder models (T5, BART) excel at tasks requiring faithful source conditioning, like summarization or question answering. Decoder-only models are generally preferred for open-ended generation and have dominated recent scaling because they require less architectural complexity."

## 11. Follow-ups
- "When would you choose Decoder-only (GPT) over Encoder-Decoder (T5) for a task?" (Decoder-only is better for open-ended generation, instruction following, and when a single model should handle both understanding and generation. Encoder-decoder is better when faithfulness to a specific source is critical).

## 12. Deeper questions
- "What is BART?" (BART is an encoder-decoder model pretrained by corrupting text (masking, shuffling, deletion) and training the decoder to reconstruct the original. This pretraining makes it powerful for text generation tasks like summarization and data-to-text).

## 13. Related concepts
- **BERT**: Encoder-only (no decoder).
- **GPT**: Decoder-only (no encoder).
- **T5 / BART**: Full encoder-decoder.

## 14. When it breaks / Edge cases
- Cross-attention doubles decoder compute per token. For generation tasks with long decoding, this makes encoder-decoder models slower than decoder-only.

## 15. Comparison with alternative approaches
- **vs Decoder-only:** Decoder-only is simpler (one pretraining objective), easier to scale, and dominant in instruction-following. Encoder-decoder has stronger source conditioning for faithful generation tasks.

---
*Where this shows up in ML:*
Google Translate (GNMT), T5 (text-to-text transfer), BART (summarization), Whisper (speech-to-text) all use Encoder-Decoder Transformers.
