# LLM & RAG Interview Questions

---

## Q1. What is RAG and when would you use it instead of fine-tuning?

**Expected Answer:** RAG (Retrieval-Augmented Generation) retrieves relevant documents at inference time and injects them into the LLM's context. Use RAG when: knowledge is frequently updated (news, docs), you need source attribution, data is proprietary/confidential (can't expose to training), or you need to handle very large knowledge bases (>what fits in context). Use fine-tuning when: you need the model to learn a new style/format/behavior, the domain has very specific terminology, or you need inference latency improvement from fewer context tokens.

**Key Concepts:** Retrieval, chunking, embedding, in-context learning, knowledge freshness.

**Likely Follow-Up:** "What are the failure modes of RAG?" — Retrieval failure (relevant doc not retrieved), context faithfulness (LLM ignores retrieved context), chunking artifacts (answer splits across chunks), semantic gap (query and document use different vocabulary).

**Common Wrong Answer:** "RAG is always better because you don't need to retrain" — RAG adds retrieval latency and fails when the answer requires synthesizing across many documents or understanding domain-specific reasoning patterns not in the retrieved text.

**Strong Candidates Add:** RAGAS evaluation framework (faithfulness, answer relevancy, context recall); hybrid retrieval (BM25 + dense); HyDE (generate hypothetical document, then retrieve); reranking with cross-encoders.

---

## Q2. Explain RLHF. What is the reward model and why is it needed?

**Expected Answer:** RLHF (Reinforcement Learning from Human Feedback) has three stages: (1) Supervised Fine-Tuning (SFT) on high-quality human demonstrations; (2) Reward Model (RM) training: annotators rank model outputs, train a regression model to score outputs; (3) RL optimization: use PPO to maximize the reward model's score while a KL-divergence penalty prevents the policy from drifting too far from the SFT model. The reward model is needed because "good response" isn't easily defined by a differentiable loss — human preferences require a learned proxy.

**Key Concepts:** SFT, reward model, PPO, KL penalty, preference data.

**Likely Follow-Up:** "What is DPO and how does it differ from RLHF?" — DPO (Direct Preference Optimization) eliminates the separate RM and RL loop. It directly optimizes the policy using preference pairs, mathematically equivalent to RLHF under certain assumptions but simpler, more stable, and cheaper to implement.

**Common Wrong Answer:** "RLHF just means training the model to follow instructions" — SFT alone is instruction tuning; RLHF specifically adds the preference-based reward loop.

**Strong Candidates Add:** Constitutional AI (Anthropic's approach using AI feedback instead of human feedback for some stages); reward hacking (RM can be gamed, leading to degenerate outputs that score high but are poor); the tension between helpfulness and harmlessness.

---

## Q3. What is hallucination in LLMs and how do you mitigate it?

**Expected Answer:** Hallucination is when LLMs generate fluent, confident text that is factually incorrect. Types: intrinsic (contradicts the provided context), extrinsic (makes up external facts). Causes: models predict plausible next tokens, not truthful statements; training data noise; lack of explicit "I don't know" training. Mitigations: RAG (ground answers in retrieved documents), sampling with temperature 0 for factual tasks, chain-of-thought prompting, self-consistency (sample multiple answers), factual consistency training, tool use (search, calculator), output verification.

**Key Concepts:** Types of hallucination, RAG grounding, temperature, self-consistency.

**Likely Follow-Up:** "How would you build a system to detect hallucinations?" — Use a separate verifier model, compare claims to retrieved sources using NLI (Natural Language Inference), or use LLM-as-judge to score faithfulness.

**Common Wrong Answer:** "Just lower the temperature to 0" — greedy decoding reduces diversity but doesn't eliminate hallucination; models can confidently generate wrong facts.

**Strong Candidates Add:** SelfCheckGPT (sample multiple times, inconsistency across samples indicates hallucination); FACTSCORE for biography generation; citation-based generation where every claim is tied to a retrieved source.

---

## Q4. What is quantization and what are the tradeoffs?

**Expected Answer:** Quantization represents model weights/activations in lower-precision data types (FP16, INT8, INT4) to reduce memory and improve inference speed. PTQ (Post-Training Quantization): quantize after training, fast but accuracy loss. QAT (Quantization-Aware Training): simulate quantization during training, better accuracy. NF4 (NormalFloat4) used in QLoRA: designed for normally-distributed weights, minimal quality loss at 4-bit. Tradeoffs: 4-bit reduces model size 8x (FP32→INT4) but loses some accuracy, requires careful outlier handling (absmax/zeropoint scaling).

**Key Concepts:** PTQ vs QAT, INT8/INT4/NF4, accuracy tradeoff, bitsandbytes.

**Likely Follow-Up:** "What is GPTQ?" — A PTQ algorithm that computes quantization errors layer-by-layer using second-order information, achieving near-lossless INT4 quantization for large LLMs.

**Common Wrong Answer:** "Quantization always significantly degrades accuracy" — with modern methods (GPTQ, AWQ, NF4), 4-bit quantization of large LLMs often loses only 0-2% performance.

**Strong Candidates Add:** The outlier problem in LLM quantization: a few outlier weights/activations have very large magnitudes, making naive quantization poor. LLM.int8() and SmoothQuant address this by mixed-precision or migrating outlier difficulty from activations to weights.
