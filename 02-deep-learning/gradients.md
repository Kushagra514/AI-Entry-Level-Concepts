# Gradients

## 1. Definition
A gradient is a vector containing the partial derivatives of a function with respect to all of its variables. In ML, it points in the direction of the steepest ascent of the Loss function.

## 2. Intuition
Imagine standing blindfolded on a hilly terrain, trying to find the lowest valley (min loss). You feel the slope of the ground under your feet. The gradient tells you which way is strictly "uphill". To reach the valley, you take a step in the *exact opposite* direction of the gradient.

## 3. Why it exists
Without gradients, we would have to guess randomly to update weights (Random Search). Gradients exist to provide mathematical, deterministic directions on exactly how to adjust every single weight to reduce the error.

## 4. Mechanics
If Loss $L = w^2$, the gradient with respect to $w$ is $\frac{\partial L}{\partial w} = 2w$.
If $w = 3$, the gradient is 6. This means increasing $w$ slightly will increase $L$ sharply. So, we must *decrease* $w$.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(W)$ to compute for $W$ parameters.
- **Space Complexity:** $O(W)$ to store the gradient vector for the optimizer.

## 6. Tiny worked example
$L(w, b) = 3w + b^2$.
$\frac{\partial L}{\partial w} = 3$.
$\frac{\partial L}{\partial b} = 2b$.
The Gradient Vector $\nabla L = [3, 2b]$.

## 7. Code (Python, with type hints)
```python
import torch

# PyTorch automates gradient calculation
w = torch.tensor([3.0], requires_grad=True)
b = torch.tensor([4.0], requires_grad=True)

loss = 3 * w + b ** 2
loss.backward()

print(w.grad) # tensor([3.])
print(b.grad) # tensor([8.])
```

## 8. Common mistakes
- Forgetting to zero out gradients (`optimizer.zero_grad()`) in PyTorch before the next batch, causing gradients to accumulate incorrectly.
- Vanishing/Exploding gradients in deep networks.

## 9. 30-second interview answer
"A gradient is a vector of partial derivatives representing the slope of the loss function with respect to the model's weights. Because the gradient points to the steepest increase in loss, we subtract it from the weights during gradient descent to minimize the error."

## 10. 2-minute interview answer
"The gradient is the compass that guides neural network training. Mathematically, it is the vector of partial derivatives of the loss function evaluated at the current weight values. It inherently points in the direction of steepest ascent in the high-dimensional loss landscape. Optimization algorithms like SGD calculate this gradient via backpropagation and then step in the negative direction, scaled by a learning rate, to descend into a loss minimum. The main challenges in deep learning—like vanishing or exploding gradients—occur when these partial derivatives multiply over many layers, collapsing to zero or shooting to infinity, effectively breaking the 'compass'."

## 11. Follow-ups
- "What causes vanishing gradients?" (Repeatedly multiplying derivatives $< 1$, commonly caused by deep networks using Sigmoid or Tanh activations).

## 12. Deeper questions
- "What is the Jacobian Matrix vs the Hessian Matrix?" (Jacobian is 1st-order partial derivatives for vector-valued functions. Hessian is 2nd-order derivatives, describing the curvature of the loss landscape).

## 13. Related concepts
- **Backpropagation**: The algorithm used to efficiently compute the gradients.
- **Gradient Descent**: The algorithm that uses the gradients to update weights.

## 14. When it breaks / Edge cases
- Non-differentiable functions (like step functions or `argmax`) have undefined or zero gradients, making gradient-based learning impossible.

## 15. Comparison with alternative approaches
- **vs Evolutionary Algorithms:** Evolutionary algorithms don't use gradients, making them immune to non-differentiable bottlenecks, but they are vastly less sample-efficient than gradient descent.

---
*Where this shows up in ML:* 
The `.grad` attribute of parameters in PyTorch.
