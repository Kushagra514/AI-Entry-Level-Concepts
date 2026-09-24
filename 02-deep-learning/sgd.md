# Stochastic Gradient Descent (SGD) & Mini-Batch SGD

## 1. Definition
Stochastic Gradient Descent (SGD) approximates the true gradient by evaluating the loss on a single random training example (or a small Mini-Batch) per step, rather than the entire dataset.

## 2. Intuition
Instead of surveying 10,000 people to perfectly decide which way to step (Batch GD), you ask 32 random people (Mini-Batch SGD). Their average opinion is a bit noisy, but it's "good enough" to take a step, and you can take hundreds of steps in the time it would take to survey all 10,000 once.

## 3. Why it exists
Standard Batch Gradient Descent requires evaluating the entire dataset to take *one* step. If you have 1 million images, it's computationally agonizing and doesn't fit in RAM. SGD allows frequent, lightweight updates, drastically accelerating training.

## 4. Mechanics
- **Pure SGD:** Batch size = 1. High noise, slow hardware utilization (no matrix parallelization).
- **Mini-Batch SGD:** Batch size = 16 to 1024. Strikes a balance: smooths out noise, fits in GPU memory, and perfectly utilizes GPU matrix parallelization.
- Often paired with **Momentum**: adding a fraction of the previous update to the current one to plow through noise and saddle points.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(B \times W)$ per step, where $B$ is batch size.
- **Space Complexity:** $O(B \times A)$ for activations. Fits nicely in GPU VRAM.

## 6. Tiny worked example
Dataset size 100.
- Batch GD: 1 step per epoch. True gradient.
- Mini-batch (size 10): 10 steps per epoch. Slightly noisy gradients.
- Pure SGD (size 1): 100 steps per epoch. Highly erratic gradients.

## 7. Code (Python, with type hints)
```python
import torch

# PyTorch Optimizer setup
# lr is learning rate, momentum helps smooth the SGD path
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Inside training loop:
# optimizer.zero_grad()
# loss.backward()
# optimizer.step()
```

## 8. Common mistakes
- Using pure SGD (batch size 1) in production. It completely wastes GPU parallelization capabilities.
- Not shuffling the dataset before creating mini-batches. If batches are ordered by class, the gradients will pull the model violently in different directions.

## 9. 30-second interview answer
"SGD optimizes neural networks by updating weights using a small mini-batch of data rather than the entire dataset. This introduces noise but allows for exponentially faster, more frequent updates and ensures the data fits into GPU memory."

## 10. 2-minute interview answer
"Mini-Batch SGD is the de facto standard for training neural networks. Computing the true gradient over millions of samples before taking a single step is computationally unfeasible. By sampling a random mini-batch—say, 256 images—we get an unbiased, slightly noisy estimate of the true gradient. This noise acts as a feature, not a bug, providing a regularizing effect that helps the model bounce out of shallow local minima. More importantly, it strikes the perfect balance for hardware: it fits within GPU VRAM constraints while being just large enough to max out SIMD matrix-multiplication efficiency. We almost always enhance it with Momentum, which acts like a moving average on the gradients, dampening the batch-to-batch oscillations and accelerating convergence along consistent dimensions."

## 11. Follow-ups
- "What happens if the batch size is too large?" (It mimics Batch GD: updates become rare, it requires massive memory, and ironically, generalizing performance often drops because the lack of noise causes it to settle into sharp local minima).

## 12. Deeper questions
- "How does Adam differ from SGD with Momentum?" (Adam uses adaptive learning rates for *each parameter* based on the 1st and 2nd moments of the gradients, whereas SGD applies the same learning rate to all parameters).

## 13. Related concepts
- **Adam Optimizer**: The most popular advanced alternative to SGD.
- **Batch Normalization**: Often needed to stabilize the erratic internal shifts caused by mini-batch updates.

## 14. When it breaks / Edge cases
- Breaks if the dataset isn't I.I.D (independent and identically distributed). Shuffling is mandatory.

## 15. Comparison with alternative approaches
- **vs Adam:** SGD with Momentum often generalizes slightly better on Computer Vision tasks (ResNets), while Adam converges much faster and is universally preferred for NLP/Transformers.

---
*Where this shows up in ML:* 
The core optimizer loop training every modern AI model.
