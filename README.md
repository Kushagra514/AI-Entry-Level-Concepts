# AI/ML + DSA Interview Preparation System

This repository is a comprehensive, structured study system designed for entry-level Artificial Intelligence, Machine Learning, and Data Structures & Algorithms interviews. It is optimized for deep understanding over rote memorization, employing highly structured frameworks to break down complex theoretical and coding concepts.

## 🧠 Core Philosophy
Instead of generic tutorials or shallow definitions, every topic in this repository is designed around two objectives:
1. **ML Theory:** If asked an ML theoretical question, you must be able to explain the intuition, mathematics, implementation implications, tradeoffs, and a practical example clearly.
2. **DSA Coding:** If asked a DSA question, you must be able to walk the interviewer through the constraints, brute force approach, key insight, optimized code, dry run, and time/space complexity before writing a single line of code.

## 🗺️ Repository Structure & Map

The repository is divided into numbered modules progressing from foundations to advanced topics, project defenses, and mock interviews.

### Machine Learning Progression
* **`00-foundations/`**: Probability, Statistics, Linear Algebra, Calculus
* **`01-ml-basics/`**: Linear & Logistic Regression, Decision Trees, Bias-Variance
* **`02-deep-learning/`**: Neural Networks, Backprop, Optimizers (SGD/Adam), Regularization
* **`03-nlp/`**: Embeddings, Tokenization, TF-IDF
* **`05-transformers/`**: Self-Attention, Multi-Head, Positional Encoding, BERT/GPT
* **`06-llms/`**: Pretraining, Next Token Prediction, Fine-Tuning (SFT, RLHF)
* **`07-rag/`**: Vector DBs, Chunking, Retrieval, Reranking
* **`08-efficient-llms/`**: Quantization, LoRA, Distillation
* **`09-agents/`**: Tool Calling, Workflows, Planning, Memory

### Data Structures & Algorithms (DSA) Progression
* **`16-dsa-foundations/`**: Big-O Notation, Arrays, Strings
* **`17-data-structures/`**: Linked Lists, Stacks, Queues, Hash Maps, Trees, Graphs, Heaps
* **`18-algorithms/`**: Sorting, Binary Search, DFS/BFS
* **`19-dp-deep-dive/`**: 1D/2D DP, DP on Trees/Graphs, Bitmask DP
* **`20-dsa-patterns/`**: Two Pointers, Sliding Window, Top K, Monotonic Stack
* **`23-dsa-interview-questions/`**: Real problems with 11-step breakdowns

### System Design & CS Fundamentals
* **`10-system-design-ml/`**: Model Serving, Feature Stores, Pipelines
* **`21-oop-and-lld/`**: OOP Pillars, SOLID, Design Patterns
* **`22-cs-fundamentals/`**: OS, Memory (Stack/Heap), DB Normalization, ACID, Networks

### Synthesis & Mocks
* **`12-cheat-sheets/`**: Quick-reference guides and Big-O tables
* **`13-project-defense/`**: NEXEN Rainfall Regime-Aware Bias Correction System
* **`15-mock-interviews/`** & **`24-dsa-mock-interviews/`**: Full transcript simulations

---

## 🏗️ Learning Frameworks

### The 15-Section ML Topic Framework
Every ML theoretical file follows this exact structure to ensure no gaps in understanding:
1. Definition
2. Intuition (ELI5)
3. Why it exists
4. Mechanics (How it works under the hood)
5. Mathematical formulation
6. Tiny worked example
7. Code snippet (PyTorch/NumPy)
8. Common mistakes/misconceptions
9. 30-second interview answer
10. 2-minute interview answer
11. Standard follow-ups
12. Deeper questions (Edge cases)
13. Related concepts
14. When it breaks (Failure modes)
15. Comparison with alternative approaches

### The 11-Step DSA Problem Framework
Every DSA interview question follows this structured communication path:
1. Restate the problem
2. Clarify edge cases
3. Brute force approach (Time/Space)
4. Key Insight (The "Aha!" moment)
5. Optimized approach
6. Justification (Time/Space)
7. Code (Python)
8. Dry run trace
9. Edge cases handled
10. Follow-ups
11. Related Problems

---

## 📚 Study Order

For optimal comprehension, study the modules in this exact sequence:

1. **Phase 1 (The Bedrock):** `00-foundations/`, `16-dsa-foundations/`, `17-data-structures/`
2. **Phase 2 (Core Algorithms & Classical ML):** `01-ml-basics/`, `18-algorithms/`, `20-dsa-patterns/`
3. **Phase 3 (Deep Learning & Advanced DSA):** `02-deep-learning/`, `19-dp-deep-dive/`, `23-dsa-interview-questions/`
4. **Phase 4 (Modern AI):** `03-nlp/`, `05-transformers/`, `06-llms/`, `07-rag/`, `08-efficient-llms/`, `09-agents/`
5. **Phase 5 (Engineering & Synthesis):** `21-oop-and-lld/`, `22-cs-fundamentals/`, `13-project-defense/`
6. **Phase 6 (Execution):** `12-cheat-sheets/`, `15-mock-interviews/`, `24-dsa-mock-interviews/`

---

## 🧮 Critical Equations Table

| Concept | Equation |
| :--- | :--- |
| Softmax | $P(y_i) = \frac{e^{z_i}}{\sum e^{z_j}}$ |
| Cross-Entropy Loss | $L = -\sum y_i \log(\hat{y}_i)$ |
| Self-Attention | $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$ |
| Logistic Function (Sigmoid) | $\sigma(z) = \frac{1}{1 + e^{-z}}$ |
| Cosine Similarity | $\cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$ |

---

## 📄 Foundational Papers
* *Attention Is All You Need* (Vaswani et al., 2017)
* *LoRA: Low-Rank Adaptation of Large Language Models* (Hu et al., 2021)
* *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (Lewis et al., 2020)
* *InstructGPT: Training language models to follow instructions with human feedback* (Ouyang et al., 2022)
* *Adam: A Method for Stochastic Optimization* (Kingma & Ba, 2014)

---

## ✅ Self-Assessment & Revision Checklist
* [ ] Can I derive backpropagation for a single dense layer on a whiteboard?
* [ ] Can I write a bug-free Binary Search from memory in under 2 minutes?
* [ ] Can I explain the exact mechanism of Q, K, V matrices in Self-Attention?
* [ ] Can I describe the Time/Space complexity of 10 common DSA patterns?
* [ ] Can I defend every architectural choice in my NEXEN SIH project?
* [ ] Can I implement a Trie, a Min-Heap, and an LRU Cache from scratch?
* [ ] Can I articulate the CAP theorem and the difference between SQL/NoSQL?

*This repository is designed for long-term mastery. Do not rush. One concept thoroughly understood is worth ten concepts memorized.*
