# Gradient Descent

## 1. Definition
Gradient Descent is a first-order iterative optimization algorithm used to minimize a loss function by updating parameters in the opposite direction of the gradient.

## 2. Intuition
You are blindfolded on a mountain and want to reach the bottom. You feel the slope with your foot (calculate gradient), take a step downhill (update weights), and repeat until the ground feels flat (minimum loss).

## 3. Why it exists
For complex neural networks, there is no closed-form mathematical solution to find the minimum of the loss function (you can't just set the derivative to zero and solve for $W$). Gradient Descent exists to find the minimum numerically through iterative approximation.

## 4. Mechanics
1. Initialize weights randomly.
2. Compute the gradient of the loss $\nabla L(W)$.
3. Update weights: $W_{new} = W_{old} - \alpha \nabla L(W)$, where $\alpha$ is the Learning Rate.
4. Repeat until convergence.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(E \times N \times W)$ where $E$ is epochs, $N$ is samples, $W$ is parameters.
- **Space Complexity:** $O(W)$ to hold the gradients and weights.

## 6. Tiny worked example
Weight $w = 5$, Learning Rate $\alpha = 0.1$.
Gradient is calculated as $2$.
Update: $w_{new} = 5 - (0.1 \times 2) = 5 - 0.2 = 4.8$.

## 7. Code (Python, with type hints)
```python
import numpy as np

def gradient_descent_step(weights: np.ndarray, gradients: np.ndarray, lr: float) -> np.ndarray:
    return weights - lr * gradients
```

## 8. Common mistakes
- Setting the Learning Rate too high, causing the updates to overshoot the minimum and diverge (loss goes to infinity).
- Setting the Learning Rate too low, causing the model to take forever to train or get stuck in local minima.

## 9. 30-second interview answer
"Gradient descent is an optimization algorithm that minimizes the loss function. It iteratively subtracts the gradient of the loss from the weights, scaled by a learning rate, steering the model toward a local or global minimum."

## 10. 2-minute interview answer
"Gradient Descent is the workhorse of machine learning optimization. Since neural networks lack a closed-form solution, we must solve for the optimal weights iteratively. By calculating the gradient of the loss landscape via backpropagation, we know the direction of steepest ascent. Gradient descent simply steps in the exact opposite direction. The step size is controlled by the learning rate, which is the most critical hyperparameter: too high, and the model diverges; too low, and it stagnates. Standard 'Batch' Gradient Descent computes the gradient over the entire dataset before stepping, which provides a precise vector but is incredibly slow and memory-intensive, leading to the creation of Stochastic and Mini-Batch variants."

## 11. Follow-ups
- "What happens if you get stuck in a local minimum?" (In very high-dimensional spaces like Deep Learning, true local minima are rare; saddle points are the real issue. Momentum helps escape them).

## 12. Deeper questions
- "How do 2nd-order methods (like Newton's Method) differ?" (They compute the Hessian to know the curvature of the space, allowing massive, accurate steps, but computing a $W \times W$ Hessian for 1B parameters is impossible).

## 13. Related concepts
- **Learning Rate**: Controls the step size.
- **SGD / Adam**: Advanced variants of basic Gradient Descent.

## 14. When it breaks / Edge cases
- Diverges to `NaN` if the learning rate is too large.

## 15. Comparison with alternative approaches
- **vs Closed Form (Normal Equation):** Linear regression can be solved exactly in one step taking $O(F^3)$ time (matrix inversion). Gradient descent is used when inversion is too slow or impossible (non-linear networks).

---
*Where this shows up in ML:* 
The underlying mechanism behind `optimizer.step()`.
