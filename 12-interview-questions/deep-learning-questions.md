# Deep Learning Interview Questions

---

## Q1. How does backpropagation work?

**Expected Answer:** Backpropagation applies the chain rule to compute gradients of the loss with respect to all parameters. For a composition $L = f(g(h(x)))$: $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial f}\cdot\frac{\partial f}{\partial g}\cdot\frac{\partial g}{\partial h}\cdot\frac{\partial h}{\partial x}$. Starting from the output, we propagate error signals backward through each layer, computing local Jacobians and multiplying them. PyTorch builds a dynamic computation graph (DAG) and traverses it in reverse topological order.

**Key Concepts:** Chain rule, computation graph, local gradients, vanishing/exploding gradients.

**Likely Follow-Up:** "What is the vanishing gradient problem and how do residual connections fix it?" — Multiplying many Jacobians (each < 1 for saturating activations) approaches zero. Residual connections add an identity path: gradient = $F'(x) + I$, so even if $F'(x) \to 0$, gradient is still $\approx 1$.

**Common Wrong Answer:** "Backprop just adjusts weights toward the correct answer" — misses the calculus derivation and chain rule.

**Strong Candidates Add:** Gradient checkpointing for memory efficiency; mixed-precision training accumulates gradients in FP32 to avoid underflow; gradient accumulation simulates larger batches.

---

## Q2. What are activation functions and why do we need non-linear ones?

**Expected Answer:** Activation functions introduce non-linearity. Without them, any stack of linear layers collapses to a single linear transformation (matrix product is closed under composition). Non-linear activations enable the Universal Approximation Theorem: a two-layer network with enough units can approximate any continuous function. Common activations: ReLU ($\max(0,x)$, fast, sparse), GELU ($x\Phi(x)$, smooth, used in transformers), Sigmoid (saturates, used in gates), Tanh (zero-centered sigmoid).

**Key Concepts:** Non-linearity, UAT, dying ReLU, vanishing gradients, GELU vs ReLU.

**Likely Follow-Up:** "What is the dying ReLU problem?" — Neurons with consistently negative pre-activation receive zero gradient and never recover. Leaky ReLU and ELU address this with a small negative slope.

**Common Wrong Answer:** "We need non-linear activations so the network is more complex" — misses the mathematical reason (composition of linear functions is linear).

**Strong Candidates Add:** GELU's probabilistic interpretation (Gaussian CDF gating); SwiGLU's gating mechanism in modern LLMs; BatchNorm/LayerNorm as "activation normalization" that keeps activations in the non-saturated regime.

---

## Q3. Explain the transformer attention mechanism mathematically.

**Expected Answer:** $\text{Attention}(Q,K,V) = \text{softmax}(QK^T/\sqrt{d_k})V$. Q, K, V are linear projections of the input. The dot product $QK^T$ computes pairwise similarities between queries and keys; dividing by $\sqrt{d_k}$ prevents softmax saturation from large dot products in high dimensions; softmax normalizes to attention weights; weighted sum of V produces the output. Multi-head attention applies this in $h$ parallel subspaces and concatenates.

**Key Concepts:** QKV projections, scaling, softmax, multi-head, $O(N^2)$ complexity.

**Likely Follow-Up:** "Why scale by $\sqrt{d_k}$?" — When $d_k$ is large, random initialization causes dot products to have magnitude $\sqrt{d_k}$. Without scaling, softmax receives very large inputs and becomes nearly one-hot, losing gradient signal.

**Common Wrong Answer:** Dividing by $d_k$ instead of $\sqrt{d_k}$.

**Strong Candidates Add:** Flash Attention's IO-aware implementation that fuses operations to avoid writing the $N\times N$ attention matrix to HBM; GQA (Grouped Query Attention) in Llama which reduces KV-cache by sharing K,V across multiple Q heads.

---

## Q4. What is batch normalization and when should you use it?

**Expected Answer:** BatchNorm normalizes each feature across the batch: $\hat{x} = (x-\mu_B)/\sqrt{\sigma_B^2+\epsilon}$, then rescales with learnable $\gamma, \beta$. Benefits: reduces internal covariate shift, allows higher learning rates, acts as regularizer (different for each batch's noise). Drawbacks: depends on batch size (fails for small batches), problematic for sequential data and variable-length sequences. Use LayerNorm for Transformers/RNNs; BatchNorm for CNNs/MLPs with adequate batch size.

**Key Concepts:** Internal covariate shift, batch statistics, learnable scale/shift, train vs inference mode.

**Likely Follow-Up:** "What changes at inference time for BatchNorm?" — Uses running mean/variance accumulated during training (via exponential moving average), not batch statistics. Important to call `model.eval()` in PyTorch.

**Common Wrong Answer:** "BatchNorm prevents overfitting" — it reduces internal covariate shift primarily; regularization effect is a side benefit.

**Strong Candidates Add:** GroupNorm as a compromise between BatchNorm and LayerNorm; Instance Normalization for style transfer; the failure mode of BatchNorm with batch size 1.
