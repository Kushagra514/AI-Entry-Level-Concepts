# Linear Algebra for ML

## 1. Definition
Linear algebra is the branch of mathematics studying vectors, matrices, and linear transformations. It provides the computational substrate for all neural network operations.

## 2. Intuition
A neural network layer is a mathematical machine that takes an input arrow (vector) in some high-dimensional space and stretches, rotates, or squishes it into a new arrow in a different space. Linear algebra formalizes and makes efficient every single one of these transformations.

## 3. Why it exists
ML models operate on collections of numbers (tensors). All forward passes, gradient computations, and attention mechanisms are matrix multiplications and vector operations. Without linear algebra, we have no efficient, parallelizable operations.

## 4. Mechanics
- **Vector Space:** A set of vectors closed under addition and scalar multiplication.
- **Matrix Multiplication:** $(AB)_{ij} = \sum_k A_{ik} B_{kj}$. Composing linear transformations.
- **Transpose:** $(A^T)_{ij} = A_{ji}$. Used in dot products and gradient computation.
- **Eigenvalues/Eigenvectors:** $Av = \lambda v$. Eigenvectors are directions unchanged by transformation; eigenvalues scale them.
- **SVD:** $A = U\Sigma V^T$. Decomposes any matrix. Used in PCA, recommendation systems, and understanding LoRA.
- **Norms:** $||v||_2 = \sqrt{\sum v_i^2}$ (L2). $||v||_1 = \sum |v_i|$ (L1). Used in regularization and similarity.

## 5. Complexity (Time & Space)
- Matrix mult $(m \times n)(n \times p)$: $O(mnp)$ naively, heavily optimized by BLAS to $O(mn p / \text{CPU parallelism})$.
- SVD of $m \times n$ matrix: $O(mn^2)$.

## 6. Tiny worked example
Rotation in 2D: $R = \begin{pmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{pmatrix}$. Applied to $v = [1, 0]$: $Rv = [\cos\theta, \sin\theta]$. The vector rotates; its length is preserved ($||Rv||=1$).

## 7. Code (Python)
```python
import numpy as np

A = np.array([[1, 2], [3, 4]], dtype=float)
b = np.array([5, 6])

# Solve Ax = b via least-squares (linear regression closed form)
x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

# SVD decomposition
U, S, Vt = np.linalg.svd(A)  # A = U @ diag(S) @ Vt

# Cosine similarity between two vectors
v1, v2 = np.array([1, 0, 1]), np.array([0, 1, 1])
cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
```

## 8. Common mistakes
- Treating matrix multiplication as commutative: $AB \neq BA$ in general.
- Ignoring numerical stability: large condition numbers in matrices cause catastrophic cancellation.

## 9. 30-second interview answer
"Linear algebra provides the operations for every neural network layer: matrix multiplications for linear transformations, dot products for similarity (Attention), SVD for dimensionality reduction, and norms for regularization. GPUs exist specifically to execute large batched matrix multiplications efficiently."

## 10. 2-minute interview answer
"Every forward pass of a neural network is a chain of matrix multiplications and element-wise nonlinearities. An embedding lookup is matrix-vector multiplication. Attention is $\text{softmax}(QK^T/\sqrt{d_k})V$ — entirely matrix operations. Backpropagation computes Jacobians (matrices of partial derivatives) via the chain rule, which is matrix multiplication in reverse. Understanding SVD is especially important for ML engineers: it's how PCA works, how LoRA's low-rank approximation is motivated, and how we measure the intrinsic dimensionality of data. The matrix rank is how many independent directions of variation exist — high-rank matrices contain more information."

## 11. Follow-ups
- "What is Principal Component Analysis?" (PCA rotates data to the eigenvectors of the covariance matrix, sorted by eigenvalue. The top $k$ components capture the most variance, enabling dimensionality reduction).

## 12. Deeper questions
- "Why is the Transformer's attention score divided by $\sqrt{d_k}$?" (Without scaling, larger dimensions produce larger dot products, pushing softmax into saturation regions with near-zero gradients).

## 13. Related concepts
- **Tensors**: Generalization of matrices.
- **Cosine Similarity**: Derived from the dot product and L2 norm.

## 14. When it breaks / Edge cases
- Singular matrices (rank-deficient) cannot be inverted, breaking exact linear regression solutions.

## 15. Comparison with alternative approaches
- N/A — foundational mathematics.

---
*Where this shows up in ML:*
`nn.Linear(in, out)` is $y = xW^T + b$ — pure matrix multiplication. Attention is three matrix multiplications. The gradient of a matrix operation is a matrix operation.
