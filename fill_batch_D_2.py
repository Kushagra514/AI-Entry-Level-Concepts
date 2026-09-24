import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch D)"')

# ---- 05-transformers ----
wc("05-transformers/positional-encoding.md", r"""# Positional Encoding

## 1. Definition
Positional Encoding adds position-dependent signals to token embeddings in Transformers, giving the model information about where each token appears in the sequence — since Self-Attention itself is permutation-invariant.

## 2. Intuition
Imagine giving 10 identical red boxes to 10 people in a line. You can't tell who is first and who is last — the boxes are identical. Positional Encoding is like writing the person's queue number on each box before they receive it, so the model can tell "token at position 3" from "token at position 7."

## 3. Why it exists
Self-Attention computes pairwise scores between all tokens simultaneously — it has no inherent notion of sequence order. If you shuffled the tokens, the attention output would be the same (just permuted). Positional encodings inject order.

## 4. Mechanics
- **Sinusoidal PE (Original "Attention Is All You Need"):** For position $pos$ and dimension $i$:
  $PE_{(pos,2i)} = \sin(pos/10000^{2i/d})$
  $PE_{(pos,2i+1)} = \cos(pos/10000^{2i/d})$
  Added (not concatenated) to the token embedding.
- **Learned PE (GPT, BERT):** A trainable embedding matrix where position index is looked up, like a word embedding. More flexible, but doesn't generalize to unseen positions.
- **Rotary PE (RoPE — used in Llama):** Encodes position via rotation of the Q and K vectors before the dot product, enabling relative position awareness and better length generalization.
- **ALiBi:** Instead of adding to embeddings, adds a position-based penalty to attention scores.

## 5. Complexity (Time & Space)
- **Time:** $O(1)$ additional computation per token (simple lookup or sin/cos).
- **Space:** $O(L \times d)$ for learned PE (L = max sequence length, d = embedding dim).

## 6. Tiny worked example
Token "cat" has embedding $[0.5, 0.3]$. At position 4 with $d=2$:
$PE_{(4,0)} = \sin(4/10000^0) = \sin(4) \approx -0.757$
$PE_{(4,1)} = \cos(4/10000^0) = \cos(4) \approx -0.654$
Final input: $[0.5 + (-0.757), 0.3 + (-0.654)] = [-0.257, -0.354]$.

## 7. Code (Python)
```python
import torch
import numpy as np

def sinusoidal_pe(max_len: int, d_model: int) -> torch.Tensor:
    pe = torch.zeros(max_len, d_model)
    position = torch.arange(0, max_len).unsqueeze(1).float()
    div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                         -(np.log(10000.0) / d_model))
    pe[:, 0::2] = torch.sin(position * div_term)  # Even dims
    pe[:, 1::2] = torch.cos(position * div_term)  # Odd dims
    return pe  # Shape: (max_len, d_model)
```

## 8. Common mistakes
- Confusing Absolute PE (original paper) with Relative PE (RoPE, ALiBi). Absolute PE assigns a fixed vector to each position. Relative PE encodes the distance between positions, making it more robust to sequence lengths unseen during training.
- Forgetting to add PE before the first Transformer block, not after.

## 9. 30-second interview answer
"Positional Encoding injects sequence-order information into the Transformer because Self-Attention is permutation-invariant. The original paper used fixed sinusoidal encodings added to embeddings. Modern LLMs (Llama) use Rotary PE (RoPE), which encodes relative positions via Q/K vector rotation, offering better length generalization."

## 10. 2-minute interview answer
"The Transformer's permutation invariance is a design feature (parallelism) that requires a workaround: positional encodings. The original Transformer uses sinusoids with different frequencies for each embedding dimension. Lower dimensions encode coarse position; higher dimensions encode fine-grained position. The frequencies were chosen so that any offset $k$ corresponds to a linear transformation, enabling the model to attend to relative positions via linear combination. Modern LLMs like Llama use RoPE (Rotary Position Embedding), which encodes position by rotating Q and K vectors. The dot product of RoPE-encoded Q and K vectors depends only on their relative position, not absolute positions, enabling better generalization beyond the training context length."

## 11. Follow-ups
- "Why do models struggle with context lengths beyond their training length?" (Learned PEs produce out-of-distribution embeddings for unseen positions. Sinusoidal PEs theoretically extrapolate, but attention patterns still shift. RoPE + ALiBi generalize somewhat better).

## 12. Deeper questions
- "What is context window extension (e.g., RoPE scaling / YaRN)?" (By scaling the position indices in RoPE's rotation formula, you can extend a model trained on 4K context to 128K context without full retraining, with some fine-tuning to adapt).

## 13. Related concepts
- **Self-Attention**: Becomes position-aware only via PE.
- **RoPE**: The dominant PE in open-source LLMs.

## 14. When it breaks / Edge cases
- Learned PE fails completely at positions > the training max length. Sinusoidal PE degrades gracefully. RoPE with scaling handles it best.

## 15. Comparison with alternative approaches
- **Sinusoidal vs Learned vs RoPE vs ALiBi:** Sinusoidal = no parameters, good extrapolation theory. Learned = more flexible, poor extrapolation. RoPE = relative, good generalization. ALiBi = minimal parameters, strong length generalization via attention bias.

---
*Where this shows up in ML:*
Every Transformer model. Llama uses RoPE. GPT-2/3 uses learned PE. The original Transformer uses sinusoidal. Context length extension techniques (YaRN, LongRoPE) are active research areas.
""")

wc("05-transformers/residual-connections.md", r"""# Residual Connections (Skip Connections)

## 1. Definition
A Residual Connection (Skip Connection) adds the input of a layer directly to its output: $\text{output} = F(x) + x$, allowing gradients to flow directly through identity paths during backpropagation.

## 2. Intuition
Imagine teaching a student by asking them to learn only the "delta" — the correction to their current answer, not the entire answer from scratch. Instead of learning $y = F(x)$, the layer learns $\text{residual} = F(x) - x$, which is typically a small correction. This is easier to learn and far easier to train with gradient descent.

## 3. Why it exists
Deep networks (20+ layers) fail to train without residual connections due to the **Vanishing Gradient Problem**. Gradients in the backward pass are products of layer-local derivatives. Even tiny values (0.9) multiplied 100 times become $0.9^{100} \approx 0.00003$, essentially zero. Residual connections create gradient highways that bypass this.

## 4. Mechanics
- **Forward Pass:** $y = F(x, W) + x$ (or with projection $W_s x$ if dimensions differ).
- **Backward Pass:** $\partial L/\partial x = \partial L/\partial y \cdot (F'(x) + I)$. The identity term $I$ ensures gradient flows even if $F'(x) \to 0$.
- In Transformers, every sub-layer (Attention and FFN) has a residual connection: $x \leftarrow x + \text{Attention}(x)$, then $x \leftarrow x + \text{FFN}(x)$.
- **Pre-LN vs Post-LN:** Whether LayerNorm is applied before or after the sub-layer. Modern LLMs use Pre-LN for training stability.

## 5. Complexity (Time & Space)
- **Time:** $O(d)$ per token — just an elementwise addition.
- **Space:** $O(d)$ to keep the residual (input) in memory alongside the layer output.

## 6. Tiny worked example
Without residual: If $F(x)$ has gradient $0.01$ and there are 100 layers: $0.01^{100} \approx 10^{-200}$. Effectively zero. No learning.

With residual: Gradient becomes $0.01 + 1 = 1.01$ through the identity path. $1.01^{100} \approx 2.7$. The gradient is preserved.

## 7. Code (Python)
```python
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, d_model: int):
        super().__init__()
        self.norm = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model)
        )

    def forward(self, x):
        # Pre-LN residual (modern convention)
        return x + self.ff(self.norm(x))
```

## 8. Common mistakes
- Applying residual connections only to some layers and not others, creating bottlenecks.
- Using residual connections when input and output dimensions differ without projecting the residual ($W_s x$) to match dimensions.

## 9. 30-second interview answer
"Residual connections add the input to the layer output: $y = F(x) + x$. They solve the Vanishing Gradient Problem by providing gradient highways through identity paths, enabling training of very deep networks (100+ layers). Every Transformer sub-layer wraps a residual connection around Attention and FFN."

## 10. 2-minute interview answer
"ResNets introduced residual connections in 2015, enabling 152-layer networks where 20-layer plain networks failed. The core insight is reformulating what the layer learns: instead of learning a complete transformation $H(x)$, the layer learns only the residual $F(x) = H(x) - x$, which is small and easy to train. During backpropagation, the identity term in $\partial L/\partial x = \partial L/\partial y \cdot (F'(x)+I)$ ensures a gradient pathway even when the learned transformation's gradient vanishes. In Transformers, residual connections are combined with Layer Normalization in a 'sublayer wrapper': $x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$ (Pre-LN), which provides both gradient flow and activation scale stability. The residual stream in Transformers has been deeply studied — the residual stream can be understood as a communication bus between layers, each layer reading from and writing to this shared state."

## 11. Follow-ups
- "What is the 'residual stream' perspective of Transformers?" (Each attention head and FFN layer reads from the residual stream and adds a vector to it. The stream accumulates information across all layers as an additive process).

## 12. Deeper questions
- "Why are deeper Transformers better? Isn't the residual connection effectively making early layers optional?" (Each additional layer has the *opportunity* to refine the representation. With residual connections, the network can choose to 'skip' a layer by learning near-zero weights in $F(x)$).

## 13. Related concepts
- **Layer Normalization**: Almost always paired with residual connections in Transformers.
- **Highway Networks**: A gated predecessor to ResNets with learned skip weights.

## 14. When it breaks / Edge cases
- Post-LN (original Transformer paper) can be unstable without careful learning rate warmup. Pre-LN is now standard.

## 15. Comparison with alternative approaches
- **vs Dense/DenseNet connections:** DenseNet connects every layer to every subsequent layer ($O(N^2)$ connections). ResNets use simple skip-one connections. Transformers use residual-to-every-layer because the architecture is sequential.

---
*Where this shows up in ML:*
Every modern deep learning architecture: ResNets (vision), Transformers (NLP), U-Nets (segmentation). Without residual connections, models beyond ~20 layers cannot be trained effectively.
""")

wc("05-transformers/layer-normalization.md", r"""# Layer Normalization

## 1. Definition
Layer Normalization normalizes the activations within a single sample across the feature dimension, computing mean and variance per-sample rather than per-batch.

## 2. Intuition
Imagine everyone on a team speaks different languages with wildly different volumes. You apply noise-cancelling headphones (normalization) to each person individually, bringing everyone to the same volume level. Unlike Batch Norm, which adjusts all people in the room at once, Layer Norm adjusts each person independently.

## 3. Why it exists
Batch Normalization (normalizing across the batch) works poorly for variable-length sequences in NLP: batch statistics become meaningless when sequence lengths vary, and small batches on GPU produce noisy estimates. Layer Normalization normalizes per-sample, making it batch-size independent and suitable for Transformers and RNNs.

## 4. Mechanics
Given input $x \in \mathbb{R}^d$:
1. Compute mean: $\mu = \frac{1}{d}\sum_{i=1}^d x_i$.
2. Compute variance: $\sigma^2 = \frac{1}{d}\sum_{i=1}^d (x_i - \mu)^2$.
3. Normalize: $\hat{x}_i = (x_i - \mu)/\sqrt{\sigma^2 + \epsilon}$.
4. Scale & shift: $y_i = \gamma \hat{x}_i + \beta$ where $\gamma, \beta$ are learnable parameters.

Applied in Transformers as **Pre-LN** (before sub-layer) for stability:
$x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$.

## 5. Complexity (Time & Space)
- **Time:** $O(d)$ per token — two passes over the feature vector.
- **Space:** $O(d)$ for $\gamma$ and $\beta$ parameters; $O(1)$ auxiliary per-sample.

## 6. Tiny worked example
$x = [3, 5, 7]$. $d=3$.
$\mu = 5$. $\sigma^2 = \frac{(3-5)^2+(5-5)^2+(7-5)^2}{3} = \frac{8}{3} \approx 2.67$.
$\hat{x} = [-1.22, 0, 1.22]$.
With $\gamma=1$, $\beta=0$: $y = [-1.22, 0, 1.22]$.

## 7. Code (Python)
```python
import torch
import torch.nn as nn

# PyTorch's built-in LayerNorm
layer_norm = nn.LayerNorm(normalized_shape=512)  # Normalizes last 512 dims

# Manual implementation
def layer_norm_manual(x, gamma, beta, eps=1e-5):
    mu = x.mean(dim=-1, keepdim=True)
    sigma = x.var(dim=-1, keepdim=True, unbiased=False)
    x_hat = (x - mu) / (sigma + eps).sqrt()
    return gamma * x_hat + beta
```

## 8. Common mistakes
- Confusing Layer Norm (normalize across features for one sample) with Batch Norm (normalize across batch for one feature). In NLP: LayerNorm is almost always used; BatchNorm is rare because sequence lengths vary.
- Not using learnable $\gamma$ and $\beta$ (scale and shift). Without them, the normalization is too restrictive — it cannot learn to scale activations back up if needed.

## 9. 30-second interview answer
"Layer Normalization normalizes activations within each token's feature vector independently, computing per-sample statistics. Unlike Batch Norm (which fails on variable-length NLP sequences), LayerNorm is batch-size invariant and is used in every Transformer architecture alongside residual connections to stabilize training."

## 10. 2-minute interview answer
"Layer Normalization is critical for training deep Transformers. When activations grow large or small across layers, gradients either explode or vanish. LayerNorm constrains the magnitude of each token's embedding to have unit variance, making the activation landscape smooth and the gradients well-behaved. The learnable $\gamma$ and $\beta$ parameters allow the model to rescale the normalized activations appropriately for each layer. The placement matters: Post-LN (original Transformer) places LayerNorm after the residual, which works but requires very careful learning rate warmup. Pre-LN (modern standard, used in GPT-2+, Llama) places LayerNorm before each sub-layer, providing more stable training and often better final performance without warmup constraints. RMSNorm (used in Llama) further simplifies LayerNorm by only computing the RMS (no mean centering), reducing compute by ~30% with negligible accuracy impact."

## 11. Follow-ups
- "What is RMSNorm and why is it used in Llama?" (Simplified LayerNorm that skips mean subtraction. Only normalizes by RMS $\sqrt{(1/d)\sum x_i^2}$. Faster and empirically performs as well as full LayerNorm).

## 12. Deeper questions
- "How does LayerNorm interact with residual connections?" (Pre-LN: $x \leftarrow x + F(\text{LayerNorm}(x))$. The residual path carries unnormalized activations, while the learning path sees normalized input. This allows each layer's contribution to be well-conditioned while the residual stream can grow).

## 13. Related concepts
- **Batch Normalization**: The counterpart for vision models and CNNs.
- **Residual Connections**: Always paired with LayerNorm in Transformers.

## 14. When it breaks / Edge cases
- Very small feature dimensions (d=1 or d=2) make variance estimation noisy. LayerNorm assumes enough dimensions for stable statistics.

## 15. Comparison with alternative approaches
- **vs Batch Norm:** BatchNorm normalizes across the batch — dependent on batch size and sequence length. LayerNorm is batch-independent — normalizes across features — perfect for variable-length sequences.

---
*Where this shows up in ML:*
Every Transformer block: `x = x + Attention(LayerNorm(x))`, then `x = x + FFN(LayerNorm(x))`.
""")

wc("05-transformers/feed-forward-network.md", r"""# Feed-Forward Network (FFN) in Transformers

## 1. Definition
The Feed-Forward Network (FFN) in a Transformer block is a two-layer MLP applied independently to each token position, expanding and then projecting back: $\text{FFN}(x) = \text{GELU}(xW_1 + b_1)W_2 + b_2$.

## 2. Intuition
The Attention layer is like a social mixer — every token gathers information from others. The FFN is like a private thinking room — each token then processes what it gathered independently, reasoning about it with full MLP capacity. No communication between positions happens in the FFN.

## 3. Why it exists
Self-Attention is powerful at routing information but is linear in the embedding dimension (it's just weighted summation of Values). The FFN provides the non-linear, high-capacity computation that actually stores and transforms facts — much of the model's "knowledge" lives in FFN weights.

## 4. Mechanics
- **Architecture:** Linear(d, 4d) → GELU/ReLU → Linear(4d, d).
- **Expansion factor 4x:** Empirically chosen in the original paper; modern models often use 8x/3x for GLU variants.
- **Position-wise:** The same FFN weights are applied to every token independently. No weight sharing across the sequence.
- **GLU variants (SwiGLU, GeGLU):** Replace the simple GELU with a gated mechanism: $\text{FFN}(x) = (\sigma(xW) \odot xV)W'$. Used in Llama, PaLM — provides better performance.

## 5. Complexity (Time & Space)
- **Time:** $O(N \cdot d \cdot 4d) = O(Nd^2)$ per layer. FFN dominates over attention for large $d$ relative to $N$.
- **Parameters:** $2 \times d \times 4d = 8d^2$. Constitutes ~2/3 of total Transformer parameters.

## 6. Tiny worked example
$d=4$, Token embedding $x=[1, 0, -1, 0.5]$.
Layer 1 (Linear → 16): $W_1 \in \mathbb{R}^{4\times16}$, output $h \in \mathbb{R}^{16}$.
GELU(h): element-wise nonlinearity.
Layer 2 (Linear → 4): $W_2 \in \mathbb{R}^{16\times4}$, output $y \in \mathbb{R}^4$.
$y$ is the refined token embedding, injected back via residual.

## 7. Code (Python)
```python
import torch.nn as nn

class TransformerFFN(nn.Module):
    def __init__(self, d_model: int, expansion: int = 4, dropout: float = 0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, expansion * d_model),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(expansion * d_model, d_model),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        return self.net(x)
```

## 8. Common mistakes
- Thinking that FFN layers communicate across tokens. They don't — they are strictly position-wise. All cross-token communication happens in Attention.
- Ignoring that the FFN holds the majority of parameters: For GPT-3 with $d=12288$, each FFN has $8 \times 12288^2 \approx 1.2B$ parameters. Across 96 layers, FFN alone is ~115B of the ~175B total.

## 9. 30-second interview answer
"The FFN in a Transformer applies a 2-layer MLP independently to each token's embedding: expand 4x with GELU, project back. It provides non-linear, per-token computation after Attention's cross-token communication. FFN parameters constitute ~2/3 of total model parameters and are where factual knowledge is believed to be stored."

## 10. 2-minute interview answer
"The FFN sub-layer is often underestimated relative to Attention. Research has shown that the FFN acts as key-value memory: the first linear layer produces 'keys' that match input patterns, the activation function gates relevant memories, and the second linear layer outputs 'values' corresponding to those memories. Factual recall tasks correlate strongly with FFN weight patterns. The choice of activation matters: GELU outperforms ReLU empirically, and modern architectures use SwiGLU (Llama, PaLM) — a Swish-gated linear unit — which multiplies two parallel linear paths element-wise before the final projection. The 4x expansion factor is a hyperparameter; smaller models sometimes use 2.66x with SwiGLU to maintain parameter parity. MoE (Mixture of Experts) models replace the dense FFN with a sparse routing over multiple expert FFNs, routing each token to its top-K FFN experts."

## 11. Follow-ups
- "What is Mixture of Experts (MoE)?" (Replace the FFN with $E$ expert FFNs and a learned router that sends each token to its top-$k$ experts ($k$ typically 2). Only $k$ experts activate per token, reducing FLOPs while maintaining parameters — enabling scale without proportional compute cost. Used in Mixtral, GPT-4 (reported)).

## 12. Deeper questions
- "How does the FFN expand-then-contract architecture relate to bottleneck layers in ResNets?" (The 4x expansion creates a higher-dimensional latent space for the token to reason in, then projects back. The bottleneck (contracting) forces the model to extract the most useful transformation).

## 13. Related concepts
- **MoE (Mixture of Experts)**: Sparse FFN variant for scaling.
- **SwiGLU**: Gated FFN variant in modern LLMs.

## 14. When it breaks / Edge cases
- Very small expansion factors (1x) severely limit model capacity; the FFN becomes a simple linear layer.

## 15. Comparison with alternative approaches
- **vs Attention:** Attention routes information between positions; FFN processes information within each position. Together they are complementary — neither alone is sufficient.

---
*Where this shows up in ML:*
Every Transformer block: Attention handles communication, FFN handles computation. The FFN parameters in GPT-2 are the focus of many interpretability studies.
""")

wc("05-transformers/encoder-decoder.md", r"""# Encoder-Decoder Architecture

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
""")

wc("05-transformers/bert.md", r"""# BERT (Bidirectional Encoder Representations from Transformers)

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
""")

wc("05-transformers/gpt.md", r"""# GPT (Generative Pretrained Transformer)

## 1. Definition
GPT is a family of decoder-only Transformer models pretrained on Causal Language Modeling (next-token prediction) on large text corpora, producing generalist language models capable of in-context learning and instruction following.

## 2. Intuition
A very well-read person who has read essentially the entire internet. Give them a prompt and they will continue it in the most plausible way given everything they've read. They complete text — they don't just encode it. That is GPT.

## 3. Why it exists
BERT is powerful for understanding but cannot generate text. GPT showed that the simpler pretraining objective — predict the next token — scales massively and produces emergent capabilities: reasoning, translation, code generation, without task-specific training. GPT-3 demonstrated few-shot in-context learning at scale.

## 4. Mechanics
**Architecture:** Decoder-only. No encoder. No Cross-Attention.
- $N$ stacked Transformer decoder blocks, each with:
  - Masked (Causal) Self-Attention — each token attends only to previous tokens.
  - FFN.
  - Residual + LayerNorm (Pre-LN in GPT-2+).

**Pretraining Objective:** $\mathcal{L} = -\sum_{i} \log P(x_i | x_1, ..., x_{i-1})$. Standard left-to-right next-token prediction.

**Inference:** Autoregressive — sample one token at a time, append it, and re-run.

**In-Context Learning:** At inference, examples in the prompt act as implicit fine-tuning without weight updates. GPT-3 demonstrated this emergently at scale.

## 5. Complexity (Time & Space)
- **Training:** Efficiently parallelized — all positions computed simultaneously with causal masking.
- **Inference:** Sequential — each new token requires a full forward pass. KV-cache reduces this to $O(N \cdot d)$ per step after the first.

## 6. Tiny worked example
Prompt: "The capital of France is"
- GPT computes hidden states for all tokens in parallel.
- Final token's logits over vocabulary.
- Highest probability token: "Paris". Generate it, append, continue.

## 7. Code (Python)
```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

inputs = tokenizer("The capital of France is", return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_new_tokens=5,
    do_sample=True,
    temperature=0.7,
    top_p=0.9
)
print(tokenizer.decode(outputs[0]))
```

## 8. Common mistakes
- Thinking GPT processes text bidirectionally like BERT. It is strictly left-to-right (causal) at both train and inference time.
- Not using KV-cache during inference, causing $O(N^2)$ generation complexity instead of near-linear.

## 9. 30-second interview answer
"GPT is a decoder-only Transformer pretrained with causal next-token prediction. It attends only to previous tokens (causal masking), enabling autoregressive text generation. At scale, it develops emergent capabilities including in-context learning (GPT-3) and instruction following (InstructGPT/ChatGPT via RLHF). Modern LLMs (Llama, Claude, Gemini) all follow the GPT decoder-only architecture."

## 10. 2-minute interview answer
"GPT's key insight was simplicity at scale: a decoder-only Transformer with a single pretraining objective (next-token prediction) trained on increasingly large corpora produces increasingly capable models. GPT-1 showed transfer learning. GPT-2 showed zero-shot generalization. GPT-3 showed few-shot in-context learning — capabilities that emerged from scale without task-specific training. InstructGPT (2022) added RLHF (Reinforcement Learning from Human Feedback): supervised fine-tuning on human demonstrations, then reward model training, then PPO optimization to align the model to human preferences — creating ChatGPT. Modern open-source LLMs like Llama 3, Mistral, and Qwen are all GPT-style decoder-only Transformers differing in specific architectural choices (RoPE, GQA, SwiGLU, RMSNorm) and training data."

## 11. Follow-ups
- "What is RLHF?" (Reinforcement Learning from Human Feedback: fine-tune the LLM on human preference data using a learned reward model, then apply PPO to maximize the reward while a KL penalty prevents too much deviation from the base model).

## 12. Deeper questions
- "Why does the KV-cache grow with context length and what are the implications?" (Each new token appends K and V vectors to the cache. For a 70B model with 8K context, the KV-cache alone requires ~16GB VRAM. This is why context window length and number of KV heads (GQA/MQA) are critical deployment parameters).

## 13. Related concepts
- **BERT**: The encoder-only counterpart.
- **RLHF**: The alignment technique used to create ChatGPT from GPT.

## 14. When it breaks / Edge cases
- Catastrophic hallucination: GPT models generate fluent, confident text that is factually wrong because they predict plausible tokens, not truthful ones.

## 15. Comparison with alternative approaches
- **vs BERT:** BERT is better at understanding (classification, extraction). GPT is better at generation. GPT at instruction-following scale (ChatGPT) has largely superseded BERT-based systems.

---
*Where this shows up in ML:*
ChatGPT, GPT-4, Claude, Gemini, Llama 3, Mistral — all are GPT-style decoder-only Transformers.
""")

wc("05-transformers/transformer-equations.md", r"""# Transformer Key Equations

## 1. Definition
A consolidated reference of the core mathematical formulas underlying the Transformer architecture, suitable for interview derivation and exam-style questions.

## 2. Intuition
These equations are not abstract — each one is a computational step you can trace through the architecture. Understanding each equation operationally (what goes in, what comes out, why it's this form) is essential for deep interviews.

## 3. Why it exists
Interviewers often ask "derive the attention formula" or "what is the softmax over?". Having these formulas memorized and internalized avoids black-box answers.

## 4. Mechanics

### Token Embedding
$x_i = \text{Embedding}(t_i) + \text{PE}(i) \in \mathbb{R}^d$

### Sinusoidal Positional Encoding
$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right)$, $PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)$

### QKV Projections
$Q = XW_Q,\quad K = XW_K,\quad V = XW_V \quad (W_Q, W_K, W_V \in \mathbb{R}^{d \times d_k})$

### Scaled Dot-Product Attention
$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

- Scaling by $\sqrt{d_k}$ prevents softmax saturation.
- Output shape: $(N, d_v)$ where $N$ is sequence length.

### Multi-Head Attention
$$\text{MHA}(Q,K,V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W_O$$
$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$
where $d_k = d_v = d_{model}/h$.

### Causal Mask (Decoder)
Replace $QK^T/\sqrt{d_k}$ with $QK^T/\sqrt{d_k} + M$ where $M_{ij} = 0$ if $i \geq j$ else $-\infty$.

### Feed-Forward Network
$$\text{FFN}(x) = \text{GELU}(xW_1 + b_1)W_2 + b_2$$
$W_1 \in \mathbb{R}^{d \times 4d}$, $W_2 \in \mathbb{R}^{4d \times d}$.

### Layer Normalization
$$\text{LayerNorm}(x) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \cdot \gamma + \beta$$

### Pre-LN Residual Wrapper
$$x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$$

### Softmax
$$\text{softmax}(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$$
Numerically stable: subtract $\max(z)$ before exponentiating.

### Cross-Entropy Loss (Language Model)
$$\mathcal{L} = -\frac{1}{T}\sum_{t=1}^{T} \log P_\theta(x_t | x_{<t})$$

### Perplexity
$$\text{PPL} = \exp\!\left(\mathcal{L}\right) = \exp\!\left(-\frac{1}{T}\sum_t \log P_\theta(x_t|x_{<t})\right)$$
Lower is better. PPL = 10 means the model is as uncertain as uniformly over 10 choices at each step.

## 5. Complexity (Time & Space)
| Component | Time per layer | Parameters |
|---|---|---|
| Attention | $O(N^2 d)$ | $4d^2$ (Q,K,V,O projections) |
| FFN | $O(N d^2)$ | $8d^2$ |
| LayerNorm | $O(Nd)$ | $2d$ |
| Total per layer | $O(N^2 d + Nd^2)$ | $12d^2$ |

## 6. Tiny worked example
$d_k = 64$. Dot product of Q and K vectors of magnitude ~1: expected magnitude $\approx \sqrt{64} = 8$. Without scaling, softmax saturates. With $\sqrt{d_k}=8$ scaling, scores are $O(1)$ — gradients stay healthy.

## 7. Code (Python)
```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    attn = F.softmax(scores, dim=-1)
    return attn @ V, attn
```

## 8. Common mistakes
- Dividing by $d_k$ instead of $\sqrt{d_k}$ — a common slip in interviews.
- Applying softmax over the wrong dimension (should be the key dimension, `dim=-1` over sequence positions).

## 9. 30-second interview answer
"The core Transformer equation is $\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$. The scaling by $\sqrt{d_k}$ prevents softmax saturation from large dot products. Multi-head attention applies this independently in $h$ subspaces and concatenates. Every sub-layer is wrapped in $x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$."

## 10. 2-minute interview answer
"Walking through the Transformer equations: input tokens become embeddings plus sinusoidal positional encodings. These pass through $L$ identical encoder blocks. Each block first applies Multi-Head Attention: input is linearly projected into $h$ sets of Q, K, V matrices, scaled dot-product attention is computed in each head's subspace, and the outputs are concatenated and projected through $W_O$. A residual connection adds the pre-attention input back, and LayerNorm stabilizes the scale. The FFN then applies two linear layers with GELU, again wrapped in residual + LayerNorm. The final output of the last encoder layer represents each token as a contextual, high-dimensional vector."

## 11. Follow-ups
- "What does perplexity measure and what is a good value?" (PPL measures how surprised the model is by each next token on average. GPT-3 achieves ~20 on Penn Treebank. A PPL of 1 means perfect prediction; PPL = vocabulary size means random guessing).

## 12. Deeper questions
- "Why is the attention score matrix's diagonal dominant?" (Tokens often find themselves most relevant — especially early in training before the model learns richer dependencies. This is known as the 'attention sink' phenomenon, exploited by StreamingLLM).

## 13. Related concepts
- **All Transformer files**: These equations underpin every component.

## 14. When it breaks / Edge cases
- Numerical instability in softmax with very large logits. Always subtract `max(scores)` before `exp`.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:*
Every interview question about how Transformers work. Derivable directly from the architecture.
""")

print("Batch D Part 2 complete (05-transformers: all 8 files)")
