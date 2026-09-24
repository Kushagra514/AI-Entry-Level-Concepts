# Logistic Regression

## 1. Definition
Logistic Regression is a supervised classification algorithm that models the probability that an input belongs to a specific class. It does this by applying the logistic (sigmoid) function to a linear combination of the input features: $P(y=1 \mid x) = \sigma(W^T x + b)$.

## 2. Intuition
Take standard linear regression, which draws a line through data, but notice that a line goes to positive and negative infinity—terrible for predicting probabilities (which must be between 0 and 1). We take the output of that linear equation and squash it through a mathematical S-curve (the sigmoid function). This maps any real number to a probability between 0 and 1. If the probability is $> 0.5$, we predict Class 1.

## 3. Why It Exists
Linear regression outputs unbounded real values, unsuitable for probabilities. Hard step functions output exactly 0 or 1, but they are not differentiable, making them impossible to train with gradient descent. Logistic Regression exists to produce calibrated, bounded probabilities for binary classification while remaining smooth and differentiable.

## 4. Core Mechanics
1. **Linear Combination:** Compute $z = W^T x + b$.
2. **Activation:** Apply sigmoid: $\hat{p} = \frac{1}{1 + e^{-z}}$.
3. **Loss:** Calculate the Binary Cross-Entropy (Log Loss) between $\hat{p}$ and the true label $y \in \{0, 1\}$.
4. **Update:** Compute the gradient of the loss with respect to $W$ and $b$, and update parameters using gradient descent.

## 5. Mathematical View
**Hypothesis:**
$$ \hat{p} = \sigma(W^T x + b) = \frac{1}{1 + e^{-(W^T x + b)}} $$

**Binary Cross-Entropy Loss (for a single example):**
$$ \mathcal{L} = - [y \log(\hat{p}) + (1 - y) \log(1 - \hat{p})] $$

**Gradient:**
$$ \frac{\partial \mathcal{L}}{\partial W} = (\hat{p} - y)x $$

## 6. Shape / Dimension Tracking
Assuming batch size $N$, feature dimension $F$:
```text
X: (N, F)
W: (F, 1)
b: (1,)

Z = X @ W + b -> (N, 1)
p_hat = sigmoid(Z) -> (N, 1)
y: (N, 1)

dL/dW = X.T @ (p_hat - y) / N -> (F, 1)
```

## 7. Tiny Worked Example
1D feature $x$, weight $w=2$, bias $b=-1$. True class $y=1$.
Point $x = 1$.
$z = 2(1) - 1 = 1$.
$\hat{p} = \frac{1}{1 + e^{-1}} \approx 0.73$.
Since $0.73 > 0.5$, we correctly predict Class 1.
Loss = $-[1 \log(0.73) + 0] \approx 0.31$.
If $x$ were $-2$, $z = -5$, $\hat{p} \approx 0.006$. We would predict Class 0, getting a huge penalty if the true label was 1.

## 8. Minimal Implementation
```python
import numpy as np

def sigmoid(z): 
    return 1 / (1 + np.exp(-z))

def logistic_step(X: np.ndarray, y: np.ndarray, W: np.ndarray, b: float, lr=0.01):
    # X: (N, F), y: (N, 1), W: (F, 1)
    N = X.shape[0]
    
    # Forward
    z = X @ W + b
    y_hat = sigmoid(z)
    
    # Backward
    dW = (X.T @ (y_hat - y)) / N
    db = np.mean(y_hat - y)
    
    # Update
    W -= lr * dW
    b -= lr * db
    
    return W, b
```

## 9. Common Misconceptions
- **"It's a regression algorithm."** No, it is a classification algorithm. The word "regression" is a historical artifact.
- **"The decision boundary is curved."** The *probability surface* is curved (the S-curve), but the decision boundary in the feature space (where $P=0.5$, meaning $W^Tx+b=0$) is a perfectly straight hyperplane.

## 10. 30-Second Interview Answer
"Logistic Regression is a foundational binary classification algorithm. It passes a linear combination of inputs through a sigmoid function to output a probability between 0 and 1. Trained using Binary Cross-Entropy loss via gradient descent, it learns a linear decision boundary in the feature space. Conceptually, it is equivalent to a one-layer neural network with a sigmoid activation."

## 11. 2-Minute Interview Answer
"Logistic Regression bridges linear regression and neural networks. By applying the sigmoid function, we ensure the output is a valid probability. The decision boundary—where $W^Tx+b=0$—is a hyperplane that linearly separates the two classes. Unlike linear regression, which uses Mean Squared Error, Logistic Regression uses Binary Cross-Entropy. This is the theoretically correct loss when the output is a Bernoulli probability, corresponding to Maximum Likelihood Estimation. The gradient simplifies beautifully to $(\hat{p}-y)x$. The primary limitation is that it fails when classes are not linearly separable in the original feature space. This is precisely why deep neural networks exist: hidden layers learn nonlinear feature transformations that make the final representation linearly separable, allowing a logistic regression layer at the very end to classify it."

## 12. Follow-Up Questions
- **"What is Softmax Regression?"** 
  Also known as Multinomial Logistic Regression. It generalizes the model to $K$ classes by using $K$ weight vectors and applying the Softmax function instead of Sigmoid.
- **"Why not use Mean Squared Error (MSE) for Logistic Regression?"**
  MSE with a sigmoid activation results in a non-convex loss landscape with many local minima. Binary Cross-Entropy guarantees a convex loss landscape for logistic regression, ensuring gradient descent finds the global minimum.

## 13. Deeper Questions
- **"What happens if the data is perfectly linearly separable?"**
  The loss function will push the weights to infinity. To get the loss closer and closer to 0, the sigmoid output needs to get closer to exactly 1 or 0, which requires $z \to \pm \infty$. This causes severe overfitting (large weights). Regularization ($L2$) is required to prevent this.

## 14. Failure Modes / Edge Cases
- **Imbalanced Datasets:** With 99% negative samples, the model minimizes loss by predicting negative for everything. The default 0.5 threshold fails; you must use class-weighted loss or adjust the classification threshold.
- **XOR Problem:** Fails entirely on data like XOR that cannot be separated by a single straight line.

## 15. Comparison
- **vs Support Vector Machines (SVM):** SVM finds the maximum-margin hyperplane; Logistic Regression maximizes likelihood. SVM is generally better with small datasets and handles non-linearity via the kernel trick; Logistic Regression natively outputs calibrated probabilities.

## 16. What To Remember
- It is a classifier, not a regressor.
- Hypothesis: $\sigma(W^T x + b)$.
- Loss: Binary Cross-Entropy (Log Loss).
- Gradient: $(\hat{p} - y)x$.
- The decision boundary in feature space is linear.

## 17. Interview Trap
> **Q:** "Is logistic regression a regression algorithm?"
> **A:** Despite its name, it is a classification algorithm. The model predicts a continuous probability using a regression-like linear equation, but a threshold converts that probability into a discrete class prediction.

---
*Connected Concepts:* [Linear Regression](linear-regression.md), [Activation Functions](../02-deep-learning/activation-functions.md), [Loss Functions](../02-deep-learning/loss-functions.md)
