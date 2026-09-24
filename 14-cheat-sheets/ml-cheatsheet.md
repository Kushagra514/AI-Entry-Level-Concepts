# ML Cheat Sheet

## Key ML Algorithms at a Glance

| Algorithm | Type | When to Use | Key Hyperparameter |
|---|---|---|---|
| Linear Regression | Regression | Continuous output, linear relationship | Regularization (α) |
| Ridge / Lasso | Regression | Prevent overfitting / feature selection | λ |
| Logistic Regression | Classification | Binary classification, interpretability | Regularization |
| Decision Tree | Both | Interpretable, non-linear boundaries | max_depth |
| Random Forest | Both | Tabular data, robust to noise | n_estimators, max_depth |
| Gradient Boosting (XGBoost) | Both | High accuracy on tabular, Kaggle | learning_rate, n_estimators |
| SVM | Classification | Small dataset, high-dimensional | C, kernel |
| K-Nearest Neighbors | Both | Non-parametric, lazy learning | K |
| Naive Bayes | Classification | Text, fast, low data | Smoothing |
| K-Means | Clustering | Unsupervised, spherical clusters | K |
| PCA | Dimensionality Reduction | Feature compression, visualization | n_components |

## Bias-Variance Tradeoff

| Symptom | Cause | Fix |
|---|---|---|
| High train error + high val error | High Bias (Underfitting) | Larger model, more features, less regularization |
| Low train error + high val error | High Variance (Overfitting) | More data, regularization, dropout, early stopping |

## Regularization Types

| Type | Penalty | Effect | When |
|---|---|---|---|
| L1 (Lasso) | $\lambda\sum|w_i|$ | Sparse weights, feature selection | Many irrelevant features |
| L2 (Ridge) | $\lambda\sum w_i^2$ | Small weights, collinearity | Most regression problems |
| Elastic Net | $\alpha L1 + (1-\alpha) L2$ | Both effects | Large feature sets |
| Dropout | Random zeroing | Prevents co-adaptation | Neural networks |

## Loss Functions

| Task | Loss | Formula | When |
|---|---|---|---|
| Regression | MSE | $\frac{1}{N}\sum(y-\hat{y})^2$ | Standard regression |
| Regression | MAE | $\frac{1}{N}\sum|y-\hat{y}|$ | Outlier-robust |
| Binary Classification | BCE | $-[y\log\hat{p}+(1-y)\log(1-\hat{p})]$ | Sigmoid output |
| Multi-class | Categorical CE | $-\sum y_k\log\hat{p}_k$ | Softmax output |
| Ranking | Hinge | $\max(0, 1-y\hat{f})$ | SVMs |
| Generation | Perplexity | $\exp(-\frac{1}{T}\sum\log p_t)$ | Language models |

## Evaluation Metrics

| Task | Metric | Formula | Use When |
|---|---|---|---|
| Classification | Accuracy | $\frac{TP+TN}{N}$ | Balanced classes |
| Classification | Precision | $\frac{TP}{TP+FP}$ | FP costly (spam) |
| Classification | Recall | $\frac{TP}{TP+FN}$ | FN costly (disease) |
| Classification | F1 | $\frac{2PR}{P+R}$ | Imbalanced |
| Classification | AUC-ROC | Area under ROC | Ranking model |
| Regression | RMSE | $\sqrt{MSE}$ | Same units as y |
| Regression | R² | $1-\frac{SS_{res}}{SS_{tot}}$ | % variance explained |
| NLP | BLEU | n-gram precision | Machine translation |
| NLP | ROUGE | n-gram recall | Summarization |
| RAG | Faithfulness | Supported by context? | Hallucination check |

## Cross-Validation Strategies

| Strategy | When | Notes |
|---|---|---|
| k-Fold (k=5 or 10) | Standard | Good bias-variance tradeoff |
| Stratified k-Fold | Imbalanced classes | Preserves class ratio in each fold |
| Leave-One-Out (LOO) | Very small dataset | High variance, expensive |
| Time Series Split | Sequential data | No future leakage — always test on later data |

## Probability Distributions in ML

| Distribution | Use in ML | Parameters |
|---|---|---|
| Gaussian $\mathcal{N}(\mu, \sigma^2)$ | Weight init, noise, regression | mean, variance |
| Bernoulli | Binary classification output | $p$ |
| Categorical | Multiclass output (softmax) | probabilities over K classes |
| Uniform | Random initialization baseline | min, max |
| Dirichlet | Topic models, prior over distributions | concentration $\alpha$ |
