# Decision Trees

## 1. Definition
A Decision Tree is a supervised learning model that partitions the feature space into a hierarchy of binary splits (internal nodes), each split choosing a feature and threshold, terminating in leaf nodes that output predictions.

## 2. Intuition
A game of 20 Questions. "Is it an animal?" → Yes. "Does it have 4 legs?" → Yes. "Is it a pet?" → Yes. → Predict: Cat. The tree builds the optimal sequence of yes/no questions about features to classify the target.

## 3. Why it exists
Unlike linear models, Decision Trees natively handle non-linear relationships, interactions between features, mixed feature types (numerical + categorical), and are inherently interpretable — you can print the tree and explain every decision.

## 4. Mechanics
- **Splitting Criterion:**
  - **Classification:** Gini Impurity $G = 1 - \sum_k p_k^2$ or Entropy $H = -\sum_k p_k \log p_k$.
  - **Regression:** Variance reduction (MSE decrease).
- **Greedy construction:** At each node, try all features and thresholds, pick the split minimizing impurity.
- **Stopping:** Max depth, min samples per leaf, no impurity improvement > threshold.
- **Prediction:** Traverse the tree from root to leaf following split conditions.

## 5. Complexity (Time & Space)
- **Training:** $O(N F \log N)$ for $N$ samples and $F$ features. Sorting each feature at each depth.
- **Inference:** $O(\log N)$ for balanced tree.
- **Space:** $O(2^{depth})$ nodes.

## 6. Tiny worked example
Features: [Sunny, Hot, High Humidity]. Target: Play tennis?
- Best split: Humidity (High → No, Normal → Yes). Gini drops from 0.5 to 0.
- Leaf 1 (High): Predict No. Leaf 2 (Normal): Predict Yes.

## 7. Code (Python)
```python
from sklearn.tree import DecisionTreeClassifier
import numpy as np

X = np.array([[1,1],[1,0],[0,1],[0,0]])
y = np.array([0, 1, 1, 0])  # XOR — needs depth 2

tree = DecisionTreeClassifier(max_depth=2, criterion='gini')
tree.fit(X, y)
print(tree.predict([[1,1]]))  # [0]
```

## 8. Common mistakes
- Using a deep unrestricted tree (depth = N) — it perfectly memorizes training data (every leaf has one sample), achieving 100% train accuracy and near-random test accuracy (extreme overfitting).
- Forgetting that Decision Trees are greedy (locally optimal splits) and don't backtrack.

## 9. 30-second interview answer
"Decision Trees recursively split the feature space using greedy impurity minimization (Gini or Entropy for classification, MSE for regression). They are highly interpretable and handle non-linear boundaries natively, but overfit severely without depth constraints. Random Forests and Gradient Boosting address this by ensembling many trees."

## 10. 2-minute interview answer
"Decision Trees are the building blocks of the most powerful tabular ML models in production. Their greedy construction — at each node, exhaustively searching all features and thresholds for the split that maximally reduces impurity — produces an interpretable hierarchical model. A single tree, however, has high variance: small changes in training data lead to completely different trees. This is why we ensemble them. Random Forests grow many independent trees on bootstrap samples of data with random feature subsets (bagging + feature randomization), averaging predictions to reduce variance without increasing bias. Gradient Boosting (XGBoost, LightGBM) instead trains trees sequentially, each correcting the residual errors of the previous, achieving exceptionally low bias with careful regularization. On structured/tabular data, gradient boosted trees consistently outperform neural networks in Kaggle competitions."

## 11. Follow-ups
- "What is the difference between Random Forest and Gradient Boosting?" (RF: parallel trees, bagging, reduces variance. GB: sequential trees, boosting, reduces bias. GB is usually more accurate but more prone to overfitting and slower to train).

## 12. Deeper questions
- "Why is a Decision Tree a Greedy algorithm?" (At each node it picks the locally best split — the one maximizing immediate impurity reduction — without searching future splits. A split that looks poor now might enable much better children splits, but the tree never considers this).

## 13. Related concepts
- **Random Forests**: Ensemble of decision trees.
- **XGBoost/LightGBM**: Gradient boosted tree implementations.

## 14. When it breaks / Edge cases
- Extrapolation: trees cannot predict beyond the range of training values (they always output a leaf mean/mode). A tree trained on houses priced 100k-500k will incorrectly predict 500k for a house worth 2M.

## 15. Comparison with alternative approaches
- **vs Neural Networks on Tabular Data:** Trees handle missing values, don't require feature scaling, and are more interpretable. NNs require more data, careful preprocessing, but can learn richer representations.

---
*Where this shows up in ML:*
XGBoost and LightGBM (based on decision trees) are the dominant models for structured data in industry. Feature importance in trees is used to explain black-box models (SHAP values).
