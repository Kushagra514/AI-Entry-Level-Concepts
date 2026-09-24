# Overfitting and Underfitting

## 1. Definition
**Underfitting** occurs when a model is too simple to capture the underlying patterns in the data (high bias). **Overfitting** occurs when a model is too complex and memorizes the training noise instead of the signal (high variance).

## 2. Intuition
- **Underfitting:** A student who studies for a math test by only learning addition, failing to understand multiplication. They fail both the practice test and the real test.
- **Overfitting:** A student who memorizes the exact answers to the practice test questions without understanding the formulas. They score 100% on the practice test, but fail the real test.

## 3. Why it exists
The central goal of ML is **generalization**—performing well on unseen data. Overfitting/underfitting are the two failure modes of generalization, dictating the Bias-Variance Tradeoff.

## 4. Mechanics
- **Underfitting:** High Training Error, High Validation Error. Caused by insufficient model capacity (e.g., linear model for non-linear data) or excessive regularization.
- **Overfitting:** Low Training Error, High Validation Error. Caused by excessive model capacity (deep networks on small datasets), too many epochs, or lack of regularization.

## 5. Complexity (Time & Space)
- N/A - conceptual phenomenons.

## 6. Tiny worked example
Dataset: Housing prices (curves upward).
- Linear Regression (Underfit): Draws a straight line. Huge errors.
- 10th Degree Polynomial (Overfit): Wiggles wildly to perfectly touch every single training point. Predicts $0 for a house slightly outside the data.
- Quadratic (Just right): Captures the smooth upward curve.

## 7. Code (Python, with type hints)
```python
# Mitigating Overfitting with L2 Regularization (Weight Decay)
from sklearn.linear_model import Ridge

# alpha is the regularization strength. 
# High alpha pushes weights to 0 (fights overfitting, risks underfitting).
# Low alpha allows complex weights (risks overfitting).
model = Ridge(alpha=1.0) 
model.fit(X_train, y_train)
```

## 8. Common mistakes
- Continuing to train just because "training loss is still going down." You must monitor validation loss. If training goes down but validation goes up, you are overfitting.
- Evaluating the model on the test set repeatedly to tune hyperparameters (this overfits to the test set! You must use a separate validation set).

## 9. 30-second interview answer
"Underfitting means a model is too simple and fails to learn the data, showing high error on both training and validation sets. Overfitting means a model is too complex and memorizes noise, showing low training error but high validation error. We balance them using the Bias-Variance tradeoff."

## 10. 2-minute interview answer
"Overfitting and underfitting represent the fundamental tension in machine learning: the Bias-Variance tradeoff. Underfitting implies high bias; the model makes strong, incorrect assumptions and lacks the capacity to capture the data's complexity. We fix this by increasing model size, adding features, or training longer. Overfitting implies high variance; the model has so much capacity that it memorizes the idiosyncratic noise of the training set, destroying its ability to generalize to unseen data. We detect overfitting when training loss drops while validation loss spikes. To combat overfitting, we rely on regularization techniques: L1/L2 weight penalties, Dropout, Early Stopping, or simply gathering more training data to drown out the noise."

## 11. Follow-ups
- "What is Early Stopping?" (Monitoring validation loss during training and halting training the moment it begins to increase, preserving the model weights from before the overfitting started).
- "How does Dropout prevent overfitting?" (By randomly zeroing out neurons during training, it prevents the network from relying too heavily on any single feature, forcing redundant, robust representations).

## 12. Deeper questions
- "What is 'Double Descent' in modern Deep Learning?" (A phenomenon where, contrary to classical statistics, as model capacity increases past the point of overfitting, the test error drops again, suggesting massive models implicitly self-regularize).

## 13. Related concepts
- **Regularization**: The cure for overfitting.
- **Cross-Validation**: The method used to detect overfitting reliably.

## 14. When it breaks / Edge cases
- In NLP (LLMs), models are often trained for exactly 1 epoch over trillions of tokens. Traditional overfitting is rare because the model never sees the same data twice.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
The core motivation behind architectural choices like Dropout layers in Vision, and Weight Decay in AdamW optimizers.
