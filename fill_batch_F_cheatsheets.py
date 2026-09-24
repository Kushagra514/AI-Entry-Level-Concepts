import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch F)"')

wc("14-cheat-sheets/dsa-complexity.md", r"""# DSA Complexity Cheat Sheet

## Data Structure Operations — Time Complexity

| Data Structure | Access | Search | Insert | Delete | Space |
|---|---|---|---|---|---|
| Array | $O(1)$ | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ |
| Dynamic Array (list) | $O(1)$ | $O(N)$ | $O(1)$* amortized | $O(N)$ | $O(N)$ |
| Linked List (singly) | $O(N)$ | $O(N)$ | $O(1)$ head | $O(N)$ | $O(N)$ |
| Stack | $O(N)$ | $O(N)$ | $O(1)$ push | $O(1)$ pop | $O(N)$ |
| Queue | $O(N)$ | $O(N)$ | $O(1)$ enqueue | $O(1)$ dequeue | $O(N)$ |
| Deque | $O(N)$ | $O(N)$ | $O(1)$ both ends | $O(1)$ both ends | $O(N)$ |
| Hash Map (avg) | $O(1)$ | $O(1)$ | $O(1)$* | $O(1)$* | $O(N)$ |
| Hash Map (worst) | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ |
| Hash Set | — | $O(1)$ avg | $O(1)$ avg | $O(1)$ avg | $O(N)$ |
| Binary Search Tree (balanced) | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| BST (unbalanced/worst) | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ |
| Min/Max Heap | $O(1)$ peek | $O(N)$ | $O(\log N)$ push | $O(\log N)$ pop | $O(N)$ |
| Heapify (build heap) | — | — | $O(N)$ all at once | — | $O(N)$ |
| Trie | $O(L)$ | $O(L)$ | $O(L)$ | $O(L)$ | $O(N \cdot L)$ |
| Union-Find | — | $O(\alpha(N))$ | $O(\alpha(N))$ | N/A | $O(N)$ |
| Segment Tree | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(4N)$ |
| Fenwick Tree | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| Deque (collections.deque) | $O(N)$ mid | — | $O(1)$ ends | $O(1)$ ends | $O(N)$ |

*Amortized

## Sorting Algorithm Complexity

| Algorithm | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| Bubble Sort | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | ✅ |
| Selection Sort | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | ❌ |
| Insertion Sort | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | ✅ |
| Merge Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | ✅ |
| Quick Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | ❌ |
| Heap Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | ❌ |
| Counting Sort | $O(N+K)$ | $O(N+K)$ | $O(N+K)$ | $O(K)$ | ✅ |
| Radix Sort | $O(dN)$ | $O(dN)$ | $O(dN)$ | $O(N+K)$ | ✅ |
| Timsort (Python) | $O(N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | ✅ |

## Graph Algorithm Complexity

| Algorithm | Time | Space | Use Case |
|---|---|---|---|
| BFS | $O(V+E)$ | $O(V)$ | Shortest path (unweighted), level order |
| DFS | $O(V+E)$ | $O(V)$ | Cycle detection, topological sort |
| Dijkstra | $O((V+E)\log V)$ | $O(V)$ | Shortest path (non-negative weights) |
| Bellman-Ford | $O(VE)$ | $O(V)$ | Shortest path (negative weights) |
| Floyd-Warshall | $O(V^3)$ | $O(V^2)$ | All-pairs shortest path |
| Kruskal's MST | $O(E \log E)$ | $O(V)$ | Minimum Spanning Tree |
| Prim's MST | $O(E \log V)$ | $O(V)$ | Minimum Spanning Tree |
| Topological Sort | $O(V+E)$ | $O(V)$ | DAG ordering |

## Input Size → Allowed Complexity

| Max N | Max Complexity | Common Approach |
|---|---|---|
| $N \leq 10$ | $O(N!)$ | Backtracking, Permutations |
| $N \leq 20$ | $O(2^N)$ | Bitmask DP, Subsets |
| $N \leq 500$ | $O(N^3)$ | Floyd-Warshall, 3D DP |
| $N \leq 5000$ | $O(N^2)$ | 2D DP, LIS |
| $N \leq 10^5$ | $O(N \log N)$ | Sorting, Binary Search, Heaps |
| $N \leq 10^6$ | $O(N)$ | Two Pointers, Sliding Window, Hash Map |
| $N \leq 10^9$ | $O(\log N)$ | Binary Search, Math |

## DP Pattern Complexity Summary

| Problem Type | Time | Space | Optimizable? |
|---|---|---|---|
| 1D DP (Fibonacci, House Robber) | $O(N)$ | $O(N)$ | $O(1)$ with rolling vars |
| 2D DP (LCS, Edit Distance) | $O(NM)$ | $O(NM)$ | $O(\min(N,M))$ rows |
| 0/1 Knapsack | $O(NC)$ | $O(NC)$ | $O(C)$ 1D array |
| Interval DP (Matrix Chain) | $O(N^3)$ | $O(N^2)$ | No |
| Bitmask DP (TSP) | $O(2^N \cdot N^2)$ | $O(2^N \cdot N)$ | No |
| Tree DP | $O(N)$ | $O(N)$ | No |

---
> **Quick Rule:** If the problem says $O(\log N)$ and the array is sorted → Binary Search. If "Top K" → Heap. If "subarray/substring" → Sliding Window. If "all combinations" → Backtracking.
""")

wc("14-cheat-sheets/dsa-patterns.md", r"""# DSA Patterns Cheat Sheet

## Keyword → Pattern → Data Structure

| Problem Keywords | Pattern | Primary Data Structure | Time |
|---|---|---|---|
| Sorted array + target | Two Pointers / Binary Search | Array | $O(N)$ or $O(\log N)$ |
| Contiguous subarray + max/min | Sliding Window | Array + Two Pointers | $O(N)$ |
| Top K / Kth largest | Heap | Min-Heap or Max-Heap | $O(N \log K)$ |
| Next greater element | Monotonic Stack | Stack | $O(N)$ |
| Overlapping intervals | Merge Intervals | Sort + Array | $O(N \log N)$ |
| Cycle in linked list | Fast & Slow Pointers | Linked List | $O(N)$ |
| Combinations / Permutations | Backtracking | Recursion + Path Array | $O(2^N)$ |
| Maximize / Minimize with overlap | Dynamic Programming | Array or 2D Table | Varies |
| Connected components | BFS / DFS | Graph + Visited Set | $O(V+E)$ |
| Task dependencies | Topological Sort | DAG + In-degree Array | $O(V+E)$ |
| Dynamic connectivity | Union-Find | Parent Array | $O(\alpha N)$ |
| Numbers in range 1-N | Cyclic Sort | Array | $O(N)$ |
| All subsets of set | Subsets Backtracking | Path List | $O(2^N)$ |
| Find missing / duplicate | Hash Set / XOR / Cyclic Sort | Hash Set | $O(N)$ |
| Shortest path unweighted | BFS | Queue | $O(V+E)$ |
| Shortest path weighted | Dijkstra | Min-Heap | $O((V+E)\log V)$ |
| Shortest path negative weights | Bellman-Ford | Edge List | $O(VE)$ |
| Min Spanning Tree | Kruskal / Prim | Union-Find / Heap | $O(E \log E)$ |
| Two-sum variants | Hash Map | Hash Map | $O(N)$ |
| String prefix matching | Trie | Trie | $O(L)$ |
| Range sum queries (static) | Prefix Sum | Array | $O(1)$ query |
| Range queries + updates | Segment Tree / Fenwick | Tree | $O(\log N)$ |
| Min/Max in sliding window | Monotonic Deque | Deque | $O(N)$ |
| Median of stream | Two Heaps | Max-Heap + Min-Heap | $O(\log N)$ |
| Binary search on answer | Binary Search + Greedy check | N/A | $O(N \log(\text{Range}))$ |
| Check sorted array split | Rotated Binary Search | Array | $O(\log N)$ |

## Pattern Identification Flowchart

```
Problem has...
├── Array + sorted + O(log N) hint → Binary Search
├── Array + target sum + sorted → Two Pointers  
├── Substring/subarray + window → Sliding Window
├── "Top K" → Min-Heap of size K
├── Intervals with start/end → Merge Intervals (sort by start)
├── Linked list with cycle detection → Fast/Slow Pointers
├── All possible combinations → Backtracking
│   └── With overlap in subproblems → +Memoization = DP
├── Graph + connectivity → BFS/DFS
│   ├── Dynamic edge additions → Union-Find
│   └── Task ordering → Topological Sort
├── Maximize/minimize over index → 1D DP
├── Maximize/minimize over two strings → 2D DP (LCS/Edit Distance)
└── Subset over range 1 to N → Cyclic Sort
```

## Two-Pointer Patterns

| Variant | When | Example |
|---|---|---|
| Left + Right converging | Sorted array, pair sum | Two Sum II |
| Both from left (fast/slow) | Cycle detection, midpoint | Linked List Cycle |
| Both from left (same dir) | Sliding window count | Count of Subarrays |

## Sliding Window Variants

| Variant | Template | Example |
|---|---|---|
| Fixed size window | Maintain window of size K | Max sum of K elements |
| Variable size (max window) | Expand right, shrink left when invalid | Longest substring without repeat |
| Variable size (min window) | Shrink left as soon as valid | Minimum window substring |

## Backtracking Template

```python
def backtrack(start, path):
    if goal_reached(path):
        result.append(path.copy())
        return
    for choice in choices(start):
        path.append(choice)       # Choose
        backtrack(next, path)     # Explore
        path.pop()                # Un-choose
```

## DP State Definition Quick Guide

| Problem Type | State Definition | Base Case |
|---|---|---|
| 1D sequence | `dp[i]` = optimal at index `i` | `dp[0]` = first element |
| 2D grid | `dp[i][j]` = optimal at cell `(i,j)` | `dp[0][0]` = start |
| Two strings | `dp[i][j]` = optimal for `s1[:i]`, `s2[:j]` | `dp[0][j]` = j deletions |
| Knapsack | `dp[i][c]` = max value using items `[0..i]` with capacity `c` | `dp[0][c]` = item 0 if fits |
| Bitmask | `dp[mask][i]` = optimal for visited set `mask`, at node `i` | `dp[1][0]` = start node |
| Interval | `dp[i][j]` = optimal for range `[i,j]` | `dp[i][i]` = single element |

## Common Pitfalls Quick Reference

| Mistake | Symptom | Fix |
|---|---|---|
| `result.append(path)` not copy | All results empty at end | `result.append(path[:])` |
| Queue with `list.pop(0)` | $O(N^2)$ BFS | Use `collections.deque` |
| Knapsack inner loop forward | Items reused (Unbounded) | Iterate capacity backwards |
| No `visited` in graph DFS | Infinite loop / stack overflow | Always use `visited` set |
| `while fast.next.next` | NullPointer on non-cycle | Check `fast and fast.next` |
| Binary search: `lo = mid` | Infinite loop | Use `lo = mid + 1` |
""")

wc("14-cheat-sheets/ml-cheatsheet.md", r"""# ML Cheat Sheet

## Key ML Algorithms at a Glance

| Algorithm | Type | When to Use | Key Hyperparameter |
|---|---|---|---|
| Linear Regression | Regression | Continuous output, linear relationship | Regularization (α) |
| Ridge / Lasso | Regression | Prevent overfitting / feature selection | λ |
| Logistic Regression | Classification | Binary classification, interpretability | Regularization |
| Decision Tree | Both | Interpretable, non-linear boundaries | max_depth |
| Random Forest | Both | Tabular data, robust to noise | n_estimators, max_depth |
| Gradient Boosting (XGBoost) | Both | High accuracy on tabular, Kaggle | learning_rate, n_estimators |
| SVM | Classification | Small dataset, high-dimensional | C, kernel |
| K-Nearest Neighbors | Both | Non-parametric, lazy learning | K |
| Naive Bayes | Classification | Text, fast, low data | Smoothing |
| K-Means | Clustering | Unsupervised, spherical clusters | K |
| PCA | Dimensionality Reduction | Feature compression, visualization | n_components |

## Bias-Variance Tradeoff

| Symptom | Cause | Fix |
|---|---|---|
| High train error + high val error | High Bias (Underfitting) | Larger model, more features, less regularization |
| Low train error + high val error | High Variance (Overfitting) | More data, regularization, dropout, early stopping |

## Regularization Types

| Type | Penalty | Effect | When |
|---|---|---|---|
| L1 (Lasso) | $\lambda\sum|w_i|$ | Sparse weights, feature selection | Many irrelevant features |
| L2 (Ridge) | $\lambda\sum w_i^2$ | Small weights, collinearity | Most regression problems |
| Elastic Net | $\alpha L1 + (1-\alpha) L2$ | Both effects | Large feature sets |
| Dropout | Random zeroing | Prevents co-adaptation | Neural networks |

## Loss Functions

| Task | Loss | Formula | When |
|---|---|---|---|
| Regression | MSE | $\frac{1}{N}\sum(y-\hat{y})^2$ | Standard regression |
| Regression | MAE | $\frac{1}{N}\sum|y-\hat{y}|$ | Outlier-robust |
| Binary Classification | BCE | $-[y\log\hat{p}+(1-y)\log(1-\hat{p})]$ | Sigmoid output |
| Multi-class | Categorical CE | $-\sum y_k\log\hat{p}_k$ | Softmax output |
| Ranking | Hinge | $\max(0, 1-y\hat{f})$ | SVMs |
| Generation | Perplexity | $\exp(-\frac{1}{T}\sum\log p_t)$ | Language models |

## Evaluation Metrics

| Task | Metric | Formula | Use When |
|---|---|---|---|
| Classification | Accuracy | $\frac{TP+TN}{N}$ | Balanced classes |
| Classification | Precision | $\frac{TP}{TP+FP}$ | FP costly (spam) |
| Classification | Recall | $\frac{TP}{TP+FN}$ | FN costly (disease) |
| Classification | F1 | $\frac{2PR}{P+R}$ | Imbalanced |
| Classification | AUC-ROC | Area under ROC | Ranking model |
| Regression | RMSE | $\sqrt{MSE}$ | Same units as y |
| Regression | R² | $1-\frac{SS_{res}}{SS_{tot}}$ | % variance explained |
| NLP | BLEU | n-gram precision | Machine translation |
| NLP | ROUGE | n-gram recall | Summarization |
| RAG | Faithfulness | Supported by context? | Hallucination check |

## Cross-Validation Strategies

| Strategy | When | Notes |
|---|---|---|
| k-Fold (k=5 or 10) | Standard | Good bias-variance tradeoff |
| Stratified k-Fold | Imbalanced classes | Preserves class ratio in each fold |
| Leave-One-Out (LOO) | Very small dataset | High variance, expensive |
| Time Series Split | Sequential data | No future leakage — always test on later data |

## Probability Distributions in ML

| Distribution | Use in ML | Parameters |
|---|---|---|
| Gaussian $\mathcal{N}(\mu, \sigma^2)$ | Weight init, noise, regression | mean, variance |
| Bernoulli | Binary classification output | $p$ |
| Categorical | Multiclass output (softmax) | probabilities over K classes |
| Uniform | Random initialization baseline | min, max |
| Dirichlet | Topic models, prior over distributions | concentration $\alpha$ |
""")

wc("14-cheat-sheets/transformer-cheatsheet.md", r"""# Transformer & LLM Cheat Sheet

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
""")

wc("14-cheat-sheets/statistics-cheatsheet.md", r"""# Statistics & Math Cheat Sheet for ML Interviews

## Probability Rules

| Rule | Formula |
|---|---|
| Addition | $P(A \cup B) = P(A)+P(B)-P(A\cap B)$ |
| Multiplication | $P(A \cap B) = P(A|B)P(B)$ |
| Bayes' Theorem | $P(H|E) = \frac{P(E|H)P(H)}{P(E)}$ |
| Law of Total Probability | $P(B) = \sum_i P(B|A_i)P(A_i)$ |
| Conditional Independence | $P(A|B,C)=P(A|C)$ if A⊥B|C |

## Key Distributions

| Distribution | PMF/PDF | Mean | Variance | ML Use |
|---|---|---|---|---|
| Bernoulli$(p)$ | $p^x(1-p)^{1-x}$ | $p$ | $p(1-p)$ | Binary classification |
| Binomial$(n,p)$ | $\binom{n}{k}p^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ | Count successes |
| Gaussian $\mathcal{N}(\mu,\sigma^2)$ | $\frac{1}{\sqrt{2\pi\sigma^2}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ | $\mu$ | $\sigma^2$ | Weight init, noise |
| Poisson$(\lambda)$ | $\frac{\lambda^k e^{-\lambda}}{k!}$ | $\lambda$ | $\lambda$ | Event counts |
| Uniform$(a,b)$ | $\frac{1}{b-a}$ | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$ | Random sampling |

## Statistical Tests

| Test | When to Use | Null Hypothesis | Typical α |
|---|---|---|---|
| t-test (one-sample) | Compare sample mean to population | $\mu = \mu_0$ | 0.05 |
| t-test (two-sample) | Compare two group means | $\mu_1 = \mu_2$ | 0.05 |
| Chi-squared test | Categorical association | Independence | 0.05 |
| ANOVA | Compare 3+ group means | All means equal | 0.05 |
| Wilcoxon | Non-parametric t-test alternative | Distributions equal | 0.05 |

## Important Inequalities & Theorems

| Theorem | Statement | ML Relevance |
|---|---|---|
| Central Limit Theorem | $\bar{X} \to \mathcal{N}(\mu, \sigma^2/n)$ as $n\to\infty$ | SGD gradient noise is Gaussian |
| Law of Large Numbers | $\bar{X} \to \mu$ as $n\to\infty$ | Consistency of estimators |
| Jensen's Inequality | $f(E[X]) \leq E[f(X)]$ for convex $f$ | KL divergence is non-negative |
| Chebyshev's Inequality | $P(|X-\mu|\geq k\sigma) \leq \frac{1}{k^2}$ | Bounding tail probabilities |

## Key Formulas

| Concept | Formula |
|---|---|
| MLE | $\hat{\theta}_{MLE} = \arg\max_\theta \prod_i P(x_i|\theta)$ |
| MAP | $\hat{\theta}_{MAP} = \arg\max_\theta [\sum_i\log P(x_i|\theta) + \log P(\theta)]$ |
| KL Divergence | $D_{KL}(P||Q) = \sum_x P(x)\log\frac{P(x)}{Q(x)} \geq 0$ |
| Entropy | $H(X) = -\sum_x P(x)\log P(x)$ |
| Cross-Entropy | $H(P,Q) = -\sum_x P(x)\log Q(x) = H(P) + D_{KL}(P||Q)$ |
| Mutual Information | $I(X;Y) = H(X) - H(X|Y)$ |
| Pearson Correlation | $r = \frac{\sum(x-\bar{x})(y-\bar{y})}{\sqrt{\sum(x-\bar{x})^2\sum(y-\bar{y})^2}}$ |
| Cosine Similarity | $\cos(\theta) = \frac{A\cdot B}{||A||||B||}$ |
| Gradient Descent Update | $\theta \leftarrow \theta - \alpha\nabla_\theta\mathcal{L}$ |
| Chain Rule (backprop) | $\frac{\partial\mathcal{L}}{\partial x} = \frac{\partial\mathcal{L}}{\partial y}\cdot\frac{\partial y}{\partial x}$ |
| Attention Formula | $\text{softmax}(QK^T/\sqrt{d_k})V$ |
| L2 Regularization (Ridge) | $\mathcal{L}_{reg} = \mathcal{L} + \lambda||W||_2^2$ |
| Softmax | $\sigma(z)_i = e^{z_i}/\sum_j e^{z_j}$ |
| Sigmoid | $\sigma(z) = 1/(1+e^{-z})$ |
| ReLU | $f(z) = \max(0, z)$ |

## Hypothesis Testing Quick Reference

```
1. State H₀ (null) and H₁ (alternative)
2. Choose significance level α (usually 0.05)
3. Compute test statistic
4. Find p-value = P(data this extreme | H₀ true)
5. If p < α: Reject H₀ (result is statistically significant)
6. If p ≥ α: Fail to reject H₀ (insufficient evidence)

Type I Error (False Positive): Reject H₀ when it's true. Rate = α
Type II Error (False Negative): Accept H₀ when it's false. Rate = β
Power = 1 - β = P(reject H₀ | H₁ is true)
```
""")

print("Cheat sheets complete")
