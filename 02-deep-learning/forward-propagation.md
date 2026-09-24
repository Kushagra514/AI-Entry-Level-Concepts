# Forward Propagation

## 1. Definition
Forward propagation is the process of passing input data through a neural network's layers to generate an output prediction.

## 2. Intuition
It's an assembly line. Raw materials (data) enter the factory. The first station processes it and passes it to the next. This continues until the finished product (prediction) comes out the other end. No one looks backward during this phase.

## 3. Why it exists
Neural networks are composite functions $f(g(h(x)))$. Forward propagation exists to explicitly compute the final value of this nested function from the inside out (from input $x$ to output).

## 4. Mechanics
1. Data $X$ is multiplied by layer weights $W_1$ and bias $b_1$ is added: $Z_1 = X W_1 + b_1$.
2. An activation function $\sigma$ is applied: $A_1 = \sigma(Z_1)$.
3. $A_1$ becomes the input for the next layer.
4. This repeats until the final layer outputs the prediction $\hat{Y}$.
5. Intermediate activations ($Z$ and $A$) are saved in memory for use later in Backpropagation.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(W)$ where $W$ is the total number of parameters (weights) in the network.
- **Space Complexity:** $O(A)$ where $A$ is the memory required to store all intermediate activations (crucial for training, omitted for inference).

## 6. Tiny worked example
Input $x = 2$, Weight $w = 3$, Bias $b = -1$.
Linear step: $z = 2 \times 3 - 1 = 5$.
ReLU Activation: $\max(0, 5) = 5$.
Prediction = 5.

## 7. Code (Python, with type hints)
```python
import numpy as np

def forward_pass(x: np.ndarray, w: np.ndarray, b: np.ndarray) -> np.ndarray:
    z = np.dot(x, w) + b
    # ReLU activation
    a = np.maximum(0, z)
    return a
```

## 8. Common mistakes
- Forgetting that intermediate activations must be stored during training, which is why training takes much more VRAM than inference.
- Dimension mismatches between $X$ and $W$.

## 9. 30-second interview answer
"Forward propagation is the inference step of a neural network. It calculates the output by sequentially applying linear transformations and non-linear activation functions to the input data, caching intermediate values if training."

## 10. 2-minute interview answer
"Forward propagation is the computational realization of the neural network's hypothesis function. Given input data, we compute the dot product with the weight matrices, add biases, and pass the result through non-linear activations layer by layer. If we are in inference mode, we discard intermediate activations to save memory. However, during training, we must cache these activations in a computational graph, because the Chain Rule during Backpropagation requires the forward values to compute local gradients. Thus, forward propagation isn't just about getting a prediction; it's about setting up the necessary state for the backward pass."

## 11. Follow-ups
- "Why do we need non-linear activations?" (Without them, the entire network collapses into a single linear transformation, regardless of depth).

## 12. Deeper questions
- "How does `torch.no_grad()` save memory?" (It prevents the framework from saving the intermediate activations and building the computational graph during the forward pass).

## 13. Related concepts
- **Backpropagation**: The reverse process that updates weights.
- **Loss Functions**: Evaluates the output of the forward pass.

## 14. When it breaks / Edge cases
- If weights are too large, forward propagation can result in `NaN`s or `Inf`s due to numerical overflow (exploding activations).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The `.forward()` method in every PyTorch `nn.Module`.
