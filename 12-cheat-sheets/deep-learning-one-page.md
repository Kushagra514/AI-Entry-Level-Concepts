# Deep Learning One-Page Revision

## Core Loop
1. **Forward Pass:** $Z = WX + b$, $A = \sigma(Z)$. Cache intermediate activations.
2. **Loss:** Measure error $L = \text{Loss}(A, Y)$.
3. **Backward Pass (Backprop):** Calculate $\partial L / \partial W$ recursively using the Chain Rule.
4. **Update:** $W \leftarrow W - \alpha \frac{\partial L}{\partial W}$.

## Backpropagation & Gradients
- **Chain Rule:** $\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial x}$.
- **Complexity:** $O(P)$ time for $P$ parameters. (Proportional to one forward pass).
- **Memory Bottleneck:** Must store all intermediate activations in VRAM to compute local derivatives during the backward pass.

## Optimizers
- **SGD:** Updates weights based on current batch gradient. Noisy, can get stuck in local minima.
- **Momentum:** Keeps a moving average of gradients. Dampens oscillations and accelerates through flat valleys.
- **Adam (Adaptive Moment Estimation):** Combines Momentum (1st moment) and RMSProp (2nd moment, scaling learning rate by inverse of uncentered variance). The default optimizer for Deep Learning.

## Loss Functions
- **MSE (Mean Squared Error):** Regression. $\frac{1}{N} \sum (y - \hat{y})^2$.
- **BCE (Binary Cross-Entropy):** Binary classification (with Sigmoid). $-[y \log \hat{y} + (1-y)\log(1-\hat{y})]$.
- **Categorical Cross-Entropy:** Multi-class (with Softmax). $-\sum y_i \log \hat{y}_i$.

## Regularization (Fighting Overfitting)
- **L1 (Lasso):** Absolute value penalty. Drives weights to exactly zero (feature selection).
- **L2 (Ridge / Weight Decay):** Squared penalty. Drives weights close to zero.
- **Dropout:** Randomly zero out activations during training. Forces network to build redundant paths.

## Interview Traps
- *Does Backprop update weights?* No, Backprop computes gradients. The Optimizer updates weights.
- *What causes vanishing gradients?* Deep networks with activations like Sigmoid (derivative max 0.25). Repeated multiplication drives gradient to zero. Use ReLU or ResNets to fix.
