# Tensors

## 1. Definition
A tensor is a multi-dimensional mathematical array used as the fundamental data structure in deep learning frameworks to encode scalars, vectors, matrices, and higher-dimensional data.

## 2. Intuition
Think of a scalar as a point, a vector as a line, a matrix as a flat spreadsheet, and a tensor as a multi-level filing cabinet. A 3D tensor is like a book of spreadsheets; a 4D tensor is a bookshelf of books.

## 3. Why it exists
Neural networks require massive, parallelized matrix multiplications. Tensors exist as the standardized abstraction that allows hardware (GPUs/TPUs) to seamlessly process these operations across any number of dimensions in contiguous memory.

## 4. Mechanics
Tensors are defined by their `rank` (number of dimensions), `shape` (size of each dimension), and `dtype` (data type). E.g., an RGB image is a 3D tensor `[Height, Width, Channels]`. A batch of images is a 4D tensor `[Batch, Height, Width, Channels]`. 

## 5. Complexity (Time & Space)
- **Time Complexity:** Element-wise ops: $O(N)$ where $N$ is total elements. Matrix mult (2D): $O(N^3)$ naive, heavily optimized on GPU.
- **Space Complexity:** $O(N) \times$ size of dtype (e.g., float32 = 4 bytes per element).

## 6. Tiny worked example
Scalar (Rank 0): `5`
Vector (Rank 1): `[1, 2]` (Shape `[2]`)
Matrix (Rank 2): `[[1, 2], [3, 4]]` (Shape `[2, 2]`)
3D Tensor: `[[[1, 2]], [[3, 4]]]` (Shape `[2, 1, 2]`)

## 7. Code (Python, with type hints)
```python
import torch

# Create a 2D tensor (Matrix)
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32)
# Matrix multiplication
y = x @ x
```

## 8. Common mistakes
- Confusing Rank (number of axes) with Shape (size along axes).
- Forgetting that tensor operations on GPUs require contiguous memory layouts for peak speed.

## 9. 30-second interview answer
"Tensors are N-dimensional arrays used in deep learning. They generalize scalars (0D), vectors (1D), and matrices (2D) into higher dimensions. They are essential because they allow batched operations to be heavily parallelized on hardware accelerators like GPUs."

## 10. 2-minute interview answer
"Tensors are the foundational data structure of modern AI. Mathematically, they represent multilinear maps, but in computer science, they are just contiguous multi-dimensional arrays characterized by rank, shape, and data type. By organizing data into tensors—like representing a batch of text as `[Batch, Sequence_Length, Embedding_Dim]`—we avoid python `for` loops and instead dispatch single, massive BLAS (Basic Linear Algebra Subprograms) instructions to the GPU. This hardware parallelization is what makes training large neural networks computationally feasible."

## 11. Follow-ups
- "What is Broadcasting?" (Automatically expanding smaller tensors to match the shape of larger ones during arithmetic).

## 12. Deeper questions
- "How does memory stride relate to tensor contiguity?" (Strides define how many bytes to skip in memory to reach the next element in a dimension. A tensor is contiguous if its strides match the physical memory layout).

## 13. Related concepts
- **Vectors/Matrices**: Subsets of Tensors.
- **Embeddings**: Usually represented as 2D or 3D Tensors.

## 14. When it breaks / Edge cases
- Out of Memory (OOM) errors occur if tensor dimensions (like Batch Size) exceed GPU VRAM.

## 15. Comparison with alternative approaches
- **vs Python Lists:** Lists are pointers to scattered objects. Tensors are strict, contiguous blocks of numbers, enabling SIMD operations.

---
*Where this shows up in ML:* 
Every layer in PyTorch or TensorFlow takes a tensor as input and outputs a tensor.
