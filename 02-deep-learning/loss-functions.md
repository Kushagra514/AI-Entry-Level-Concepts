# Loss Functions

## 1. Definition
A loss function (or cost function) quantifies the difference between a model's predicted output and the actual ground-truth label.

## 2. Intuition
It's a grading rubric. If a student guesses an answer, the teacher uses the rubric to assign a penalty score based on how wrong the guess was. The goal of the student (model) is to get a score of zero.

## 3. Why it exists
Optimization algorithms (like Gradient Descent) need a singular, differentiable mathematical objective to minimize. You can't just tell a model to "do better"; you must provide a mathematical landscape where "down" means "better".

## 4. Mechanics
- **Regression (MSE):** Mean Squared Error. Calculates the average squared difference between predictions and targets. Heavily penalizes large outliers.
- **Classification (Cross-Entropy):** Calculates the divergence between the predicted probability distribution and the true one-hot distribution. Uses logarithms to heavily penalize confident wrong answers.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ where $N$ is the batch size (calculated element-wise).
- **Space Complexity:** $O(N)$ to store the gradient of the loss.

## 6. Tiny worked example
MSE: Target = 10, Prediction = 8.
Loss = $(10 - 8)^2 = 4$.

Cross Entropy: Target = `[1, 0]`, Pred = `[0.9, 0.1]`.
Loss = $-(1 \times \log(0.9) + 0 \times \log(0.1)) \approx 0.105$.

## 7. Code (Python, with type hints)
```python
import numpy as np

def mse_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return np.mean((y_true - y_pred) ** 2)

def binary_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    # Add epsilon to prevent log(0)
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
```

## 8. Common mistakes
- Using MSE for classification problems (it works poorly because the classification space isn't convex with MSE, leading to vanishing gradients).
- Forgetting to handle $\log(0)$ in Cross-Entropy implementation, causing `NaN` errors.

## 9. 30-second interview answer
"A loss function measures the error between predictions and ground truth. Mean Squared Error (MSE) is standard for regression tasks, while Cross-Entropy is standard for classification. The goal of training is to minimize this function using gradient descent."

## 10. 2-minute interview answer
"Loss functions define the objective landscape for neural networks. For regression, we typically use L2 loss (MSE) which penalizes outliers quadratically, or L1 loss (MAE) for robustness to outliers. For classification, we use Cross-Entropy, which measures the information-theoretic distance between the predicted softmax probabilities and the true distribution. The critical requirement for any loss function is that it must be differentiable with respect to the network's outputs, because its derivative acts as the starting signal for Backpropagation. If the loss function is flat (zero gradient), the network cannot learn."

## 11. Follow-ups
- "Why use Cross-Entropy instead of MSE for Classification?" (Cross-entropy paired with Softmax provides well-scaled gradients, whereas MSE with Sigmoid/Softmax causes vanishing gradients when predictions are confidently wrong).

## 12. Deeper questions
- "What is Focal Loss?" (A modification of Cross-Entropy used in object detection that down-weights the loss assigned to easy-to-classify background examples, focusing on hard, minority class examples).

## 13. Related concepts
- **Gradients**: Calculated directly from the loss function.
- **Regularization**: Often added directly to the loss function (e.g., L2 penalty).

## 14. When it breaks / Edge cases
- Unscaled losses on massive batches can overflow float16/float32 limits.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Next-Token Prediction in LLMs uses Causal Language Modeling loss, which is just standard categorical Cross-Entropy applied to vocabulary probabilities.
