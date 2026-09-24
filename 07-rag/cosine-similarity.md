# Cosine Similarity

## 1. Definition
Cosine Similarity measures the cosine of the angle between two non-zero vectors. It determines how similar two vectors are in orientation, regardless of their magnitude (length).

## 2. Intuition
Imagine two arrows starting from the origin. If they point in the exact same direction, they represent the same concept, even if one is longer than the other. Cosine similarity ignores the length and only cares about the angle. 

## 3. Why it exists
In NLP, document embeddings capture semantic meaning in their direction. The magnitude of a vector often just represents the frequency of words or document length. Cosine similarity isolates the semantic direction, making it the standard metric for comparing text embeddings.

## 4. Mechanics
- **Formula:** $\cos(\theta) = \frac{A \cdot B}{||A||_2 ||B||_2} = \frac{\sum A_i B_i}{\sqrt{\sum A_i^2} \sqrt{\sum B_i^2}}$
- **Range:** 
  - $1$: Exactly the same direction.
  - $0$: Orthogonal (completely unrelated).
  - $-1$: Exactly opposite direction.
- **Equivalence:** If vectors $A$ and $B$ are L2-normalized (length = 1), then Cosine Similarity is exactly equal to the Dot Product $A \cdot B$.

## 5. Complexity (Time & Space)
- **Time:** $O(d)$ where $d$ is the number of dimensions.
- **Space:** $O(1)$ auxiliary space.

## 6. Tiny worked example
$A = [3, 0]$, $B = [0, 4]$ (Orthogonal, angle 90)
$A \cdot B = 0$. Cosine Sim = 0.

$A = [2, 2]$, $B = [5, 5]$ (Same direction, angle 0)
$A \cdot B = 20$. 
$||A|| = \sqrt{8}$, $||B|| = \sqrt{50}$.
Cos Sim = $20 / (\sqrt{8}\sqrt{50}) = 20 / \sqrt{400} = 20 / 20 = 1$.

## 7. Code (Python)
```python
import numpy as np

def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

# Or using PyTorch
import torch
import torch.nn.functional as F

a = torch.tensor([1.0, 2.0])
b = torch.tensor([2.0, 4.0])
# Equivalent to cosine similarity when dim=0
sim = F.cosine_similarity(a, b, dim=0) 
```

## 8. Common mistakes
- Using Euclidean distance (L2 distance) on unnormalized vectors to measure semantic similarity. A very long document and a very short document about the exact same topic might have a huge Euclidean distance but a Cosine Similarity of 1.
- Re-calculating the denominator at inference time. In production RAG, all document vectors are L2-normalized upon ingestion. The query vector is normalized. Then, similarity is just a fast dot product.

## 9. 30-second interview answer
"Cosine similarity measures the angle between two vectors, defined as their dot product divided by the product of their magnitudes. It ranges from -1 to 1. It is the standard metric for comparing text embeddings because it captures semantic direction while ignoring vector magnitude, which is often an artifact of document length."

## 10. 2-minute interview answer
"Cosine similarity is the fundamental distance metric in vector search and RAG. Computed as $\frac{A \cdot B}{||A|| \cdot ||B||}$, it isolates the directional alignment of two high-dimensional vectors. In NLP, the direction of an embedding vector encodes its semantic meaning, while its magnitude often correlates with token count or word frequency. If we used Euclidean distance, a short summary and a long article about the same topic would appear distant. Cosine similarity correctly identifies them as conceptually identical. In production vector databases, we heavily optimize this: we L2-normalize all vectors (setting their magnitude to 1) during ingestion. When vectors are normalized, the denominator of the cosine formula becomes 1, meaning Cosine Similarity mathematically reduces to the simple Dot Product. Dot products are highly optimized in hardware via BLAS/CUDA, allowing us to compare a query against millions of documents in milliseconds."

## 11. Follow-ups
- "What is the relationship between Cosine Similarity and Euclidean Distance on normalized vectors?" (They are monotonically related: $||A-B||^2 = ||A||^2 + ||B||^2 - 2A\cdot B = 2 - 2\cos(\theta)$. Minimizing L2 distance is identical to maximizing cosine similarity for normalized vectors).

## 12. Deeper questions
- "Why does the Transformer Attention mechanism use Dot Product instead of Cosine Similarity?" (Attention wants to capture both direction and magnitude. A larger magnitude key vector might represent a more 'important' or 'confident' concept that should exert more pull on the query).

## 13. Related concepts
- **Dot Product**: Unnormalized version.
- **Euclidean Distance**: Distance between endpoints rather than angle.

## 14. When it breaks / Edge cases
- Fails if a vector is all zeros (division by zero).

## 15. Comparison with alternative approaches
- **Cosine vs Jaccard:** Jaccard is for discrete sets (bag of words). Cosine is for dense continuous embeddings.

---
*Where this shows up in ML:*
Vector databases, RAG, Word2Vec evaluation, contrastive learning (SimCLR, CLIP loss).
