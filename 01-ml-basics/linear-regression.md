# Linear Regression

## 1. Definition
Linear Regression models the relationship between a continuous output variable $y$ and one or more input features $x$ by fitting a linear function $\hat{y} = Wx + b$ that minimizes the sum of squared residuals.

## 2. Intuition
Plot house sizes (x) vs prices (y). Draw the best-fitting straight line through the scatter. That line IS your model. Given a new house size, read off the predicted price from the line.

## 3. Why it exists
It is the simplest model that answers "what is the expected value of $y$ given $x$?" It is the mathematical foundation for understanding all regression, and its coefficients have direct interpretable meaning (a unit increase in feature $i$ changes $y$ by $W_i$).

## 4. Mechanics
- **Model:** $\hat{y} = Wx + b$.
- **Loss (MSE):** $L = \frac{1}{N}\sum_{i=1}^{N}(y_i - \hat{y}_i)^2$.
- **Closed-Form Solution (Normal Equation):** $W^* = (X^TX)^{-1}X^Ty$. Exact solution in one step. $O(F^3)$ for $F$ features.
- **Gradient Descent Solution:** $W \leftarrow W - \alpha \nabla L$. Used when $F$ is too large to invert.
- **Assumptions:** Linearity, Independence of errors, Homoscedasticity, Normality of residuals.

## 5. Complexity (Time & Space)
- **Normal Equation:** $O(N F^2 + F^3)$. Breaks for large $F$ (e.g., $10^5$ features).
- **Gradient Descent:** $O(N F)$ per step. Scalable but iterative.
- **Space:** $O(F)$ for the weight vector.

## 6. Tiny worked example
Data: $x=[1,2,3]$, $y=[2,4,6]$. Clearly $y=2x$.
Normal Equation: $W^* = (X^TX)^{-1}X^Ty = 2$. $b=0$.
Prediction at $x=5$: $\hat{y}=10$.

## 7. Code (Python)
```python
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge

X = np.array([[1],[2],[3],[4]])
y = np.array([2.1, 3.9, 6.1, 8.0])

model = LinearRegression()
model.fit(X, y)
print(model.coef_, model.intercept_)  # ~[2.0], ~0.05

# With L2 regularization (Ridge)
ridge = Ridge(alpha=1.0)
ridge.fit(X, y)
```

## 8. Common mistakes
- Not normalizing features. If $x_1 \in [0,1]$ and $x_2 \in [0,10^6]$, gradient descent will oscillate. Standardize features first.
- Using Normal Equation for very large feature spaces — matrix inversion is $O(F^3)$ and numerically unstable for ill-conditioned matrices.

## 9. 30-second interview answer
"Linear Regression fits $\hat{y} = Wx + b$ by minimizing MSE. It can be solved exactly via the Normal Equation $(X^TX)^{-1}X^Ty$ in $O(F^3)$ time, or iteratively via Gradient Descent. Regularization (Ridge = L2, Lasso = L1) prevents overfitting by penalizing large weights."

## 10. 2-minute interview answer
"Linear Regression is the foundation of supervised learning. By minimizing the sum of squared residuals, it finds the optimal linear mapping from features to a continuous output. The closed-form Normal Equation provides the exact solution but requires inverting an $F \times F$ matrix — impractical for modern high-dimensional data. Instead, we use Gradient Descent. Adding an L2 penalty (Ridge Regression) shrinks weights toward zero, combating overfitting and improving stability when features are collinear. L1 penalty (Lasso) forces some weights exactly to zero, performing automatic feature selection. The MLE interpretation reveals that minimizing MSE implicitly assumes Gaussian noise — it's the parameter that maximizes likelihood under a Gaussian output distribution."

## 11. Follow-ups
- "What is Lasso vs Ridge?" (L1 penalty: $\lambda||W||_1$ — sparse solutions, automatic feature selection. L2 penalty: $\lambda||W||_2^2$ — small weights, handles collinearity better).

## 12. Deeper questions
- "How does multicollinearity affect Linear Regression?" (Makes $X^TX$ nearly singular, causing the Normal Equation to be numerically unstable and coefficients to explode. Ridge fixes this by adding $\lambda I$ to the diagonal).

## 13. Related concepts
- **Logistic Regression**: Applies sigmoid to the linear output for classification.
- **Neural Networks**: Deep networks are compositions of many linear + nonlinear layers.

## 14. When it breaks / Edge cases
- Fails when the true relationship is nonlinear (use polynomial features or deeper models).

## 15. Comparison with alternative approaches
- **vs Decision Trees:** Trees handle non-linearity natively. Linear regression assumes linearity. Trees are less interpretable for continuous targets.

---
*Where this shows up in ML:*
The `nn.Linear` layer is the parametric form of a linear regression unit. The final regression head in many models is literally a one-layer linear regression.
