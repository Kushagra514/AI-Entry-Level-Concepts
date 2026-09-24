# Transformer & LLM Cheat Sheet

## Core Transformer Equations

| Equation | Formula | Notes |
|---|---|---|
| Scaled Dot-Product Attention | $\text{softmax}(QK^T/\sqrt{d_k})V$ | $d_k$=head dim |
| Multi-Head Attention | $\text{Concat}(\text{head}_1...\text{head}_h)W_O$ | $h$ parallel heads |
| FFN | $\text{GELU}(xW_1+b_1)W_2+b_2$ | 4x expansion |
| Layer Norm | $(x-\mu)/\sqrt{\sigma^2+\epsilon}\cdot\gamma+\beta$ | Per-token |
| Pre-LN Residual | $x \leftarrow x + \text{Sublayer}(\text{LayerNorm}(x))$ | Modern standard |
| CLM Loss | $-\frac{1}{T}\sum_t\log P_\theta(x_t|x_{<t})$ | Next-token prediction |
| Perplexity | $\exp(\text{CLM Loss})$ | Lower = better |
| Cosine Similarity | $\frac{A \cdot B}{||A|| \cdot ||B||}$ | Range [-1, 1] |

## Transformer Variants

| Model | Type | Pretraining | Best For |
|---|---|---|---|
| BERT | Encoder-only | MLM + NSP | Classification, NER, QA |
| RoBERTa | Encoder-only | MLM (no NSP, more data) | Same as BERT, better |
| GPT-2/3/4 | Decoder-only | CLM (next-token) | Generation, completion |
| T5 | Encoder-Decoder | Text-to-Text | Translation, summarization |
| BART | Encoder-Decoder | Denoising | Summarization, generation |
| Llama 2/3 | Decoder-only | CLM + RLHF | Open-source LLM |
| Mistral | Decoder-only | CLM | Efficient open-source LLM |

## Architecture Choices in Modern LLMs

| Component | Original (2017) | Modern (Llama 3, Mistral) | Why Changed |
|---|---|---|---|
| Positional Encoding | Sinusoidal (fixed) | RoPE (rotary) | Better length generalization |
| Normalization | Post-LN | Pre-RMSNorm | More stable training |
| Activation | ReLU | SwiGLU | Better performance |
| Attention heads | All heads use full KV | GQA (grouped query attention) | Smaller KV-cache |
| Vocabulary size | 30k (BERT) | 32k-128k | Better coverage |

## Sampling Strategies

| Strategy | Formula/Rule | Effect |
|---|---|---|
| Greedy | $\arg\max P(x)$ | Deterministic, repetitive |
| Temperature | Divide logits by $T$ before softmax | $T<1$: sharper, $T>1$: diverse |
| Top-K | Sample from top $K$ tokens only | Controls diversity |
| Top-P (nucleus) | Sample from smallest set with $\sum P \geq p$ | Adaptive vocabulary |
| Beam Search | Keep top-B hypotheses at each step | Better for structured tasks |

## PEFT Methods Comparison

| Method | Trainable Params | Memory | When to Use |
|---|---|---|---|
| Full Fine-Tuning | 100% | Very High | Enough GPU + data |
| LoRA | ~0.1-1% | Low | Single GPU, limited data |
| QLoRA | ~0.1-1% (4-bit base) | Very Low | Consumer GPU fine-tuning |
| Prefix Tuning | Small | Low | Light adaptation |
| Prompt Tuning | Tiny | Minimal | Frozen model |

## RAG Pipeline Quick Reference

| Step | Tool/Method | Key Decision |
|---|---|---|
| Chunking | Fixed (512 tokens), Sentence, Semantic | Chunk size vs overlap |
| Embedding | text-embedding-ada-002, BGE, E5 | Quality vs speed |
| Indexing | FAISS, HNSW, IVF | Speed vs accuracy vs memory |
| Retrieval | Dense, Sparse (BM25), Hybrid | Semantic vs keyword match |
| Reranking | Cross-encoder (Cohere), ColBERT | Latency vs quality |
| Generation | LLM with context prompt | Hallucination vs faithfulness |

## Quantization Quick Reference

| Precision | Bits | Memory (7B model) | Quality Loss |
|---|---|---|---|
| FP32 | 32 | 28 GB | Baseline |
| BF16 / FP16 | 16 | 14 GB | Minimal |
| INT8 | 8 | 7 GB | Small |
| INT4 / NF4 | 4 | 3.5 GB | Moderate |
| INT2 / 1-bit | 2/1 | 1.75 GB / 0.9 GB | Significant |

## LLM Inference Optimization

| Technique | What It Does | Speedup |
|---|---|---|
| KV-Cache | Cache K,V for past tokens; avoid recompute | ~10x vs naive |
| Continuous Batching | Don't wait for all requests to finish; batch dynamically | 2-5x throughput |
| PagedAttention (vLLM) | Non-contiguous KV-cache memory blocks | 24x throughput |
| Speculative Decoding | Draft model generates candidates; main model verifies | 2-3x latency |
| Flash Attention | Fused Q,K,V ops in SRAM; avoids HBM writes | 2-4x, lower memory |
| Tensor Parallelism | Split weight matrices across GPUs | Linear with GPU count |
