# Activation Functions

## 1. Definition
Activation functions are mathematical equations applied to the output of a neural network node that determine whether and how strongly the neuron should "fire".

## 2. Intuition
If a network was a judicial system, the linear weights are lawyers presenting evidence (numbers). The activation function is the judge. The judge looks at the evidence and makes a non-linear ruling: "Guilty (1)", "Not Guilty (0)", or "Pay exactly this much (ReLU)".

## 3. Why it exists
Without activation functions, a neural network of 100 layers collapses mathematically into a single linear layer ($W_3(W_2(W_1x)) = W_{combined}x$). Activation functions inject **non-linearity**, allowing the network to learn complex, curved boundaries (like XOR or image features).

## 4. Mechanics
- **Sigmoid:** Squashes $(-\infty, \infty)$ to $(0, 1)$. Bad for hidden layers (vanishing gradients).
- **Tanh:** Squashes to $(-1, 1)$. Zero-centered, better than Sigmoid.
- **ReLU (Rectified Linear Unit):** $\max(0, x)$. If negative, 0. If positive, passes through unchanged. Standard for hidden layers.
- **Softmax:** Converts a vector of scores into a probability distribution (summing to 1). Used in output layers for classification.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ element-wise operation.
- **Space Complexity:** $O(N)$ to cache the inputs for the backward pass.

## 6. Tiny worked example
Input $Z = [-2.0, 3.0]$.
ReLU(Z) = `[0.0, 3.0]`.
Sigmoid(Z) = `[0.11, 0.95]`.

## 7. Code (Python, with type hints)
```python
import numpy as np

def relu(z: np.ndarray) -> np.ndarray:
    return np.maximum(0, z)

def softmax(z: np.ndarray) -> np.ndarray:
    # Shift for numerical stability (prevent exp overflow)
    shifted_z = z - np.max(z)
    exps = np.exp(shifted_z)
    return exps / np.sum(exps)
```

## 8. Common mistakes
- Using Softmax in hidden layers (it destroys independent feature representations).
- Using Sigmoid in deep hidden layers, causing the "Vanishing Gradient Problem".

## 9. 30-second interview answer
"Activation functions introduce non-linearity into neural networks, allowing them to model complex, real-world data. ReLU is the standard for hidden layers because it avoids vanishing gradients. Softmax is used in output layers for multi-class probabilities."

## 10. 2-minute interview answer
"The primary purpose of activation functions is to break linearity. Without them, a deep network is mathematically equivalent to a single linear regression model. Historically, Sigmoid and Tanh were used, but they suffer from the Vanishing Gradient problem: for very high or low inputs, their derivative approaches zero, killing the backpropagation signal. ReLU solved this by providing a constant gradient of 1 for all positive inputs, allowing deep networks to actually train. However, ReLU can suffer from 'Dying ReLUs' where large negative bias updates permanently lock a neuron to 0. This led to variants like Leaky ReLU and modern NLP variants like GeLU. For the output layer, we almost universally use Softmax for classification, as it neatly normalizes raw logits into a valid probability distribution."

## 11. Follow-ups
- "What is the Dying ReLU problem?" (If a neuron's weights shift so that it only receives negative inputs, its gradient becomes 0, and it never updates again).

## 12. Deeper questions
- "Why is GeLU preferred in Transformers?" (Gaussian Error Linear Unit combines the properties of ReLU, Dropout, and Zoneout by weighting inputs by their value in a normal distribution, creating a smoother non-linearity).

## 13. Related concepts
- **Vanishing Gradients**: Directly caused by saturating activation functions.
- **Forward Propagation**: Where activations are applied.

## 14. When it breaks / Edge cases
- Exp() in Softmax overflows easily if logits are large; subtract the max logit before exponentiating (numerical stability).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Between every single linear/conv layer in a deep learning model.
