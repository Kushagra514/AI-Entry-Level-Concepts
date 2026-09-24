# Machine Learning One-Page Revision

## 1. Core Algorithms
- **Linear Regression:** Predicts continuous value. $\hat{y} = W^Tx + b$. Loss: Mean Squared Error (MSE). Closed-form solution exists, but Gradient Descent is used for large data.
- **Logistic Regression:** Binary classification. Passes linear output through Sigmoid $\sigma(z) = \frac{1}{1 + e^{-z}}$. Loss: Binary Cross-Entropy (BCE). Decision boundary is linear.
- **Decision Trees:** Splits data based on features to maximize Information Gain (minimize Entropy or Gini Impurity). Prone to overfitting.
- **Random Forest:** Ensemble of Decision Trees (Bagging). Trains many deep trees on random subsets of data and features. Averages predictions to reduce variance (overfitting).
- **Gradient Boosting (XGBoost):** Ensemble (Boosting). Trains shallow trees sequentially, where each tree tries to correct the residual errors of the previous sequence. Reduces bias.

## 2. Model Evaluation
- **Accuracy:** Correct Predictions / Total. Fails on imbalanced datasets.
- **Precision:** True Positives / (True Positives + False Positives). "Of all the spam predictions I made, how many were actually spam?" (Cost of False Positive is high).
- **Recall:** True Positives / (True Positives + False Negatives). "Of all the actual spam emails, how many did I catch?" (Cost of False Negative is high).
- **F1-Score:** Harmonic mean of Precision and Recall. $2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$.

## 3. The Bias-Variance Tradeoff
- **Bias (Underfitting):** The model is too simple to capture the underlying pattern. (High training error, high test error).
- **Variance (Overfitting):** The model is too complex and memorizes the training noise. (Low training error, high test error).
- **Tradeoff:** As model complexity increases, bias decreases and variance increases. The goal is the sweet spot minimizing total error.

## 4. Unsupervised Learning
- **K-Means Clustering:** Partition data into $K$ clusters. Assign points to nearest centroid, move centroid to mean of points. Iterate. Fails on non-circular clusters.
- **PCA (Principal Component Analysis):** Dimensionality reduction. Projects data onto orthogonal axes that maximize variance.

## 5. Interview Traps
- *Is Logistic Regression for regression?* No, it's for classification.
- *Does scaling/normalization matter for Decision Trees?* No, tree splits are invariant to monotonic transformations. It matters heavily for distance-based algorithms (KNN, K-Means) and Gradient Descent.
