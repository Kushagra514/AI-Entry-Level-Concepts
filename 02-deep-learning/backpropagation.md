# Backpropagation

## 1. Definition
Backpropagation (backward propagation of errors) is an application of reverse-mode automatic differentiation used in neural networks. It efficiently calculates the gradient of a scalar loss function with respect to every parameter in the network by applying the calculus chain rule backward from the output to the input.

## 2. Intuition
Imagine an assembly line where the final product is defective. The quality inspector (Loss) evaluates the final product and passes the total error back to the last worker. That worker calculates their share of the blame and passes the remaining error backward to the previous worker. Backpropagation calculates exactly how much "blame" (gradient) each parameter deserves for the final error, by multiplying the local impact of each step.

## 3. Why It Exists
Finite-difference numerical gradient (bumping each parameter by $\epsilon$ and doing a forward pass) requires $O(P)$ forward passes, where $P$ is the parameter count. This is computationally impossible for networks with millions or billions of parameters. Backpropagation computes all gradients efficiently in a single backward sweep by reusing intermediate quantities, transforming gradient computation into a process mathematically proportional to just one forward pass.

## 4. Core Mechanics
1. **Forward Pass:** The network computes the output and caches intermediate activations (since they are required for local derivatives).
2. **Loss Computation:** A scalar loss is calculated comparing the prediction to the target.
3. **Loss Gradient:** Calculate the derivative of the loss with respect to the network's final output.
4. **Backward Pass (Chain Rule):** For each operation, multiply the incoming gradient from the layer above by the local derivative of the current operation.
5. **Accumulation:** Store the resulting gradients for each parameter.

## 5. Mathematical View
Consider a single linear layer $z = Wx + b$ followed by an activation $a = f(z)$ and a loss $L(a, y)$.
The gradients are computed via the chain rule:

$$ \frac{\partial L}{\partial a} = L'(a, y) $$

$$ \frac{\partial L}{\partial z} = \frac{\partial L}{\partial a} \odot f'(z) $$

$$ \frac{\partial L}{\partial W} = \frac{\partial L}{\partial z} x^T $$

$$ \frac{\partial L}{\partial b} = \frac{\partial L}{\partial z} $$

$$ \frac{\partial L}{\partial x} = W^T \frac{\partial L}{\partial z} $$

*(Note: $\frac{\partial L}{\partial x}$ is passed down to the previous layer.)*

## 6. Shape / Dimension Tracking
Assuming batch size $B$, input features $N$, and output features $M$:
```text
x: (B, N)
W: (M, N)
b: (M,)
z, a: (B, M)

∂L/∂a: (B, M)
∂L/∂z: (B, M)
∂L/∂W: (M, N)  <-- Computed via (∂L/∂z)^T @ x
∂L/∂x: (B, N)  <-- Computed via ∂L/∂z @ W
```

## 7. Tiny Worked Example
Let $z = w \cdot x$, $L = \frac{1}{2}(z - y)^2$.
Inputs: $x=2, w=3, y=10$.
**Forward:**
$z = 3 \cdot 2 = 6$
$L = \frac{1}{2}(6 - 10)^2 = 8$
**Backward:**
$\frac{\partial L}{\partial z} = (z - y) = 6 - 10 = -4$
$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial z} \cdot \frac{\partial z}{\partial w} = -4 \cdot x = -4 \cdot 2 = -8$
The gradient of $w$ is $-8$. If we subtract this (scaled by learning rate) from $w$, $w$ will increase, raising $z$ closer to $10$.

## 8. Minimal Implementation
```python
import numpy as np

def linear_backward(dZ: np.ndarray, X: np.ndarray, W: np.ndarray):
    # dZ: (Batch, M), X: (Batch, N), W: (M, N)
    
    # Gradients with respect to weights and biases
    dW = dZ.T @ X  # (M, N)
    db = np.sum(dZ, axis=0) # (M,)
    
    # Gradient to pass further backward
    dX = dZ @ W # (Batch, N)
    
    return dX, dW, db
```

## 9. Common Misconceptions
- **Backprop is the optimizer:** Backprop ONLY computes gradients. It does not update weights. An optimizer (like SGD or Adam) uses the gradients computed by backprop to update the weights.
- **Backprop is finite differences:** Finite differences compute gradients by slightly perturbing inputs. Backprop uses analytical derivatives via the chain rule.
- **Auto-diff is symbolic differentiation:** Modern ML frameworks do not generate massive mathematical formulas for the whole network (symbolic diff). They compute exact numerical values of gradients node-by-node (auto-diff).

## 10. 30-Second Interview Answer
"Backpropagation is an application of reverse-mode automatic differentiation. It calculates the gradient of a scalar loss function with respect to every network parameter by recursively applying the calculus chain rule from the output layer back to the input. This dynamic programming approach reuses intermediate values, making gradient computation computationally proportional to a single forward pass."

## 11. 2-Minute Interview Answer
"Backpropagation solves the computational impossibility of finding gradients in deep networks. If we used finite differences, computing gradients for a model with $P$ parameters would require $O(P)$ forward passes, which is impossible for modern networks. Instead, backpropagation utilizes reverse-mode automatic differentiation. During the forward pass, the network caches intermediate activations. During the backward pass, it computes the error signal starting from the scalar loss at the output. By recursively applying the chain rule, it multiplies the incoming gradient from the layer above by the local derivative of the current operation. This means we compute the exact analytical gradient for every single parameter in a single backward sweep. The tradeoff is space complexity: because local derivatives depend on the inputs to that layer, we must store the forward pass activations in VRAM, which is the primary bottleneck in training large models."

## 12. Follow-Up Questions
- **"Why does backpropagation require so much memory?"**
  Because the local derivative of operations (like $Wx$) depends on the input ($x$). Therefore, all intermediate activations from the forward pass must be held in VRAM until their corresponding backward step is executed.
- **"What is Gradient Accumulation?"**
  If a batch size doesn't fit in memory, you do forward/backward passes on micro-batches, accumulating (summing) the gradients in the `.grad` attributes without updating weights, then performing a single optimizer step.

## 13. Deeper Questions
- **"How does backprop handle operations with multiple outputs (e.g., a tensor used in two different branches)?"**
  By the multivariate chain rule, the gradient flowing back into that tensor is the sum of the gradients flowing backward from all the branches that consumed it.

## 14. Failure Modes / Edge Cases
- **Vanishing Gradients:** In deep networks with certain activations (like Sigmoid), the local derivative is often $< 1$. Multiplying these small numbers across many layers causes the gradient to decay to zero, preventing early layers from learning.
- **Exploding Gradients:** Conversely, if local derivatives are $> 1$, the gradient grows exponentially, causing numerical overflow (NaNs). Solved via gradient clipping.
- **Non-differentiable Operations:** Operations like `argmax` or a hard step function have a gradient of zero almost everywhere, breaking the chain rule.

## 15. Comparison
- **Reverse-Mode Auto-Diff (Backprop) vs Forward-Mode Auto-Diff:** Forward mode computes derivatives simultaneously with the forward pass. It is efficient when a function has few inputs but many outputs. Reverse mode (Backprop) is highly efficient when there are millions of inputs (parameters) but only one output (a scalar Loss), making it perfectly suited for Deep Learning.

## 16. What To Remember
- Backprop computes gradients; it does not update weights.
- It applies the chain rule backward from the scalar loss.
- Time complexity is roughly equivalent to one forward pass.
- Space complexity is high because forward activations must be cached.
- Tensor dimensions are critical: the gradient of a tensor always has the exact same shape as the tensor itself.

## 17. Interview Trap
> **Q:** "Does Backpropagation update the weights of the neural network?"
> **A:** No. Backpropagation strictly computes the gradient (the direction of steepest ascent). The optimizer (like SGD or Adam) is responsible for actually modifying the weights using those gradients.

---
*Connected Concepts:* [Loss Functions](loss-functions.md), [Gradient Descent](gradient-descent.md), [SGD](sgd.md), [Tensors](tensors.md)
