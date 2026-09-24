import os
import json

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Add scaffolding for {os.path.basename(path)}"')

topic_template = """# {title}

## 1. Definition
[Define the concept strictly and accurately in one or two sentences.]

## 2. Intuition
[Explain it as if to a peer, using an analogy or simple mental model.]

## 3. Why it exists
[What historical or practical problem did this solve? What was broken before?]

## 4. Mechanics
[How does it work under the hood? Step-by-step breakdown.]

## 5. Complexity (Time & Space)
- **Time Complexity:** [Justified analysis]
- **Space Complexity:** [Justified analysis]

## 6. Tiny worked example
[A minimal numerical or trace example.]

## 7. Code (Python, with type hints)
```python
# Provide clean, typed, idiomatic code
```

## 8. Common mistakes
[What do candidates usually get wrong when implementing or explaining this?]

## 9. 30-second interview answer
[The elevator pitch version for a quick question.]

## 10. 2-minute interview answer
[The deep-dive version to lead the conversation.]

## 11. Follow-ups
[What will the interviewer ask next based on your 2-minute answer?]

## 12. Deeper questions
[Hard theoretical questions for strong candidates.]

## 13. Related concepts
[How does this connect to ML or other DSA concepts?]

## 14. When it breaks / Edge cases
[When does this approach fail?]

## 15. Comparison with alternative approaches
[Trade-offs against similar structures/algorithms.]

---
*Where this shows up in ML:* 
[Brief connection to AI/ML context]
"""

# Missing directories
dirs = [
    "05-transformers",
    "06-llms",
    "07-rag",
    "08-efficient-llms",
    "09-agents",
    "10-ai-system-design",
    "11-research-topics",
    "12-interview-questions"
]
for d in dirs:
    os.makedirs(os.path.join(".", d), exist_ok=True)

files_to_generate = {
    # 05-transformers
    "05-transformers/transformer-overview.md": topic_template.format(title="Transformer Overview"),
    "05-transformers/self-attention.md": topic_template.format(title="Self-Attention"),
    "05-transformers/query-key-value.md": topic_template.format(title="Query, Key, Value"),
    "05-transformers/multi-head-attention.md": topic_template.format(title="Multi-Head Attention"),
    "05-transformers/positional-encoding.md": topic_template.format(title="Positional Encoding"),
    "05-transformers/residual-connections.md": topic_template.format(title="Residual Connections"),
    "05-transformers/layer-normalization.md": topic_template.format(title="Layer Normalization"),
    "05-transformers/feed-forward-network.md": topic_template.format(title="Feed Forward Network"),
    "05-transformers/encoder-decoder.md": topic_template.format(title="Encoder-Decoder Architecture"),
    "05-transformers/bert.md": topic_template.format(title="BERT"),
    "05-transformers/gpt.md": topic_template.format(title="GPT"),
    "05-transformers/transformer-equations.md": topic_template.format(title="Transformer Equations"),

    # 06-llms
    "06-llms/language-models.md": topic_template.format(title="Language Models"),
    "06-llms/pretraining.md": topic_template.format(title="Pretraining"),
    "06-llms/next-token-prediction.md": topic_template.format(title="Next-Token Prediction"),
    "06-llms/autoregressive-models.md": topic_template.format(title="Autoregressive Models"),
    "06-llms/fine-tuning.md": topic_template.format(title="Fine-Tuning"),
    "06-llms/instruction-tuning.md": topic_template.format(title="Instruction Tuning"),
    "06-llms/alignment.md": topic_template.format(title="Alignment (RLHF, DPO)"),
    "06-llms/temperature.md": topic_template.format(title="Temperature"),
    "06-llms/top-k-top-p.md": topic_template.format(title="Top-K & Top-P Sampling"),
    "06-llms/context-window.md": topic_template.format(title="Context Window"),

    # 07-rag
    "07-rag/rag-overview.md": topic_template.format(title="RAG Overview"),
    "07-rag/chunking.md": topic_template.format(title="Chunking"),
    "07-rag/embeddings.md": topic_template.format(title="Embeddings"),
    "07-rag/vector-databases.md": topic_template.format(title="Vector Databases"),
    "07-rag/faiss.md": topic_template.format(title="FAISS"),
    "07-rag/cosine-similarity.md": topic_template.format(title="Cosine Similarity"),
    "07-rag/retrieval-strategies.md": topic_template.format(title="Retrieval Strategies"),
    "07-rag/reranking.md": topic_template.format(title="Reranking"),
    "07-rag/rag-evaluation.md": topic_template.format(title="RAG Evaluation"),

    # 08-efficient-llms
    "08-efficient-llms/lora.md": topic_template.format(title="LoRA"),
    "08-efficient-llms/qlora.md": topic_template.format(title="QLoRA"),
    "08-efficient-llms/quantization.md": topic_template.format(title="Quantization"),
    "08-efficient-llms/distillation.md": topic_template.format(title="Knowledge Distillation"),
    "08-efficient-llms/inference-optimization.md": topic_template.format(title="Inference Optimization"),

    # 09-agents
    "09-agents/tool-calling.md": topic_template.format(title="Tool Calling"),
    "09-agents/workflows.md": topic_template.format(title="Workflows"),
    "09-agents/agents.md": topic_template.format(title="Agents"),
    "09-agents/agents-vs-workflows.md": topic_template.format(title="Agents vs Workflows"),
    "09-agents/planning.md": topic_template.format(title="Planning (ReAct, etc)"),
    "09-agents/memory.md": topic_template.format(title="Agent Memory"),
    "09-agents/agent-failure-modes.md": topic_template.format(title="Agent Failure Modes"),
}

for path, content in files_to_generate.items():
    write_file(path, content)

print(f"Generated {len(files_to_generate)} scaffolding files.")
