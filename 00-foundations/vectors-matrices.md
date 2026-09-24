# Vectors and Matrices

## 1. Definition
A vector is a 1D array representing magnitude and direction. A matrix is a 2D array of numbers representing a linear transformation or a dataset.

## 2. Intuition
A vector is an arrow in space; it tells you where to go. A matrix is a machine that takes an arrow and stretches, rotates, or squishes it into a new arrow.

## 3. Why it exists
They form the mathematical foundation of Linear Algebra, allowing us to concisely represent and solve systems of linear equations and transform geometric spaces, which is exactly what a neural network layer does.

## 4. Mechanics
- **Dot Product (Vectors):** Sum of element-wise products. Measures alignment (similarity).
- **Matrix Multiplication:** Applies the transformation of a matrix to a vector (or another matrix). To multiply $A (m \times n)$ and $B (n \times p)$, the inner dimensions ($n$) must match, yielding $(m \times p)$.

## 5. Complexity (Time & Space)
- **Time Complexity:** Dot product of length $N$: $O(N)$. Matrix mult of two $N \times N$ matrices: $O(N^3)$ (Strassen's is slightly better).
- **Space Complexity:** $O(N)$ for vectors, $O(N \times M)$ for matrices.

## 6. Tiny worked example
Vector $v = [1, 2]$
Matrix $M = [[2, 0], [0, 2]]$ (A scaling matrix).
$M \times v = [(2\times 1 + 0\times 2), (0\times 1 + 2\times 2)] = [2, 4]$. The vector was scaled by 2.

## 7. Code (Python, with type hints)
```python
import numpy as np

v1 = np.array([1, 2])
v2 = np.array([3, 4])
dot_product = np.dot(v1, v2)  # 1*3 + 2*4 = 11

M = np.array([[1, 2], [3, 4]])
transformed = M @ v1          # Matrix multiplication
```

## 8. Common mistakes
- Misaligning dimensions during matrix multiplication (the inner dimensions must match).
- Confusing element-wise multiplication (Hadamard product) with true matrix multiplication.

## 9. 30-second interview answer
"Vectors are 1D arrays representing points or directions, and matrices are 2D arrays representing linear transformations. In ML, datasets are matrices where rows are samples and columns are features, and layers apply matrix multiplications to transform these features."

## 10. 2-minute interview answer
"In ML, we use vectors to represent individual data points (like word embeddings) and matrices to represent entire datasets or the trainable weights of a neural network layer. When data passes through a Linear layer, we are simply performing matrix multiplication: transforming the input vector space into a new, learned vector space. The dot product between vectors is especially crucial, as it mathematically encodes the cosine similarity—or how 'aligned' two vectors are—which is the core mechanism behind Attention mechanisms in Transformers and similarity search in Vector Databases."

## 11. Follow-ups
- "What is an identity matrix?" (A square matrix with 1s on the diagonal, which leaves vectors unchanged when multiplied).

## 12. Deeper questions
- "What are Eigenvectors?" (Vectors that do not change direction when a specific linear transformation (matrix) is applied to them, only their magnitude scales by the eigenvalue).

## 13. Related concepts
- **Tensors**: Generalization of vectors and matrices.
- **Cosine Similarity**: Derived directly from the dot product.

## 14. When it breaks / Edge cases
- Singular (non-invertible) matrices break algorithms that require matrix inversion (like exact OLS regression).

## 15. Comparison with alternative approaches
- N/A - they are foundational mathematics.

---
*Where this shows up in ML:* 
Weight matrices $W$ in every `nn.Linear(in, out)` layer.
