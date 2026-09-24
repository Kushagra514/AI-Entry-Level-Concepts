# Logistic Regression

## 1. Definition
Logistic Regression is a supervised classification algorithm that models the probability that an input belongs to a class by applying the sigmoid function to a linear combination of features: $P(y=1|x) = \sigma(Wx+b)$.

## 2. Intuition
Take linear regression and squash the output between 0 and 1. The sigmoid function $\sigma(z) = 1/(1+e^{-z})$ acts as a probability converter — it takes any real number and maps it to a probability. If the probability exceeds 0.5, predict class 1.

## 3. Why it exists
Linear regression outputs unbounded real values, unsuitable for probabilities. Logistic Regression exists to produce calibrated, bounded probabilities for binary classification while remaining differentiable (unlike step functions).

## 4. Mechanics
- **Model:** $\hat{p} = \sigma(Wx+b)$.
- **Decision Boundary:** $\hat{p} \geq 0.5 \Rightarrow y=1$. This is the hyperplane $Wx+b=0$ in feature space.
- **Loss (Binary Cross-Entropy):** $L = -\frac{1}{N}\sum [y_i \log\hat{p}_i + (1-y_i)\log(1-\hat{p}_i)]$.
- **Training:** Gradient descent. No closed-form solution (unlike linear regression).
- **Multiclass:** Use Softmax + Categorical Cross-Entropy instead of Sigmoid.

## 5. Complexity (Time & Space)
- **Time:** $O(NF)$ per gradient step.
- **Space:** $O(F)$ for weight vector.

## 6. Tiny worked example
Two features. Decision boundary $W_1 x_1 + W_2 x_2 + b = 0$. Points above the line: $P(y=1) > 0.5$. Points below: $P(y=0) > 0.5$. The model learns the best-fit dividing line.

## 7. Code (Python)
```python
import numpy as np

def sigmoid(z): return 1 / (1 + np.exp(-z))

def bce_loss(y_true, y_pred):
    y_pred = np.clip(y_pred, 1e-15, 1-1e-15)
    return -np.mean(y_true * np.log(y_pred) + (1-y_true)*np.log(1-y_pred))

# One gradient step
def logistic_step(X, y, W, b, lr=0.01):
    N = len(y)
    z = X @ W + b
    y_hat = sigmoid(z)
    dW = (X.T @ (y_hat - y)) / N
    db = np.mean(y_hat - y)
    W -= lr * dW
    b -= lr * db
    return W, b
```

## 8. Common mistakes
- Applying Logistic Regression to linearly non-separable data without adding polynomial features or using a different model.
- Interpreting the output as a hard label instead of a probability — many applications need calibrated probabilities.

## 9. 30-second interview answer
"Logistic Regression models binary classification probability via sigmoid of a linear combination: $\hat{p} = \sigma(Wx+b)$. Trained with Binary Cross-Entropy loss, it learns a linear decision boundary in feature space. It is the foundational classification model and is equivalent to a one-layer neural network with sigmoid activation."

## 10. 2-minute interview answer
"Logistic Regression bridges linear regression and neural networks. By applying the sigmoid function, we ensure the output is a valid probability. The decision boundary — where $Wx+b=0$ — is a hyperplane that linearly separates the two classes. Unlike linear regression's MSE, Logistic Regression uses Binary Cross-Entropy, which is the correct loss when the output is a Bernoulli probability (MLE interpretation). The gradient is beautifully simple: $\partial L/\partial W = X^T(\hat{p}-y)/N$. The model fails when classes are not linearly separable in the original feature space, which is why neural networks add layers: each layer learns a nonlinear feature transformation that makes the final classes linearly separable in that transformed space."

## 11. Follow-ups
- "What is Softmax Regression?" (Generalization of Logistic Regression to $K$ classes. Apply softmax to $K$ linear outputs. Trained with categorical cross-entropy).

## 12. Deeper questions
- "Why does Logistic Regression fail on imbalanced datasets?" (The decision threshold 0.5 implicitly assumes equal class frequency. With 99% negative samples, predicting all negative gives 99% accuracy. Use class-weighted loss or adjust the threshold).

## 13. Related concepts
- **Sigmoid Activation**: Same function used in hidden layers.
- **Neural Networks**: One-layer NN with sigmoid = Logistic Regression.

## 14. When it breaks / Edge cases
- Perfect linear separability causes gradient descent to never converge (weights grow to infinity to make the boundary sharper and sharper).

## 15. Comparison with alternative approaches
- **vs SVM:** SVM finds the maximum-margin hyperplane; Logistic Regression maximizes likelihood. SVM is generally better with small datasets; Logistic Regression gives calibrated probabilities.

---
*Where this shows up in ML:*
The output layer of binary classification neural networks. Also used as the final gate activation in LSTMs.
