import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch D)"')

# ---- 00-foundations ----
wc("00-foundations/probability-statistics.md", r"""# Probability & Statistics for ML

## 1. Definition
Probability quantifies uncertainty; statistics uses data to infer properties of underlying distributions. Both are foundational to understanding why ML algorithms work and when they fail.

## 2. Intuition
Probability is the engine; statistics is the reverse-engineering. Probability says "if a coin is fair, what fraction of 1000 flips will be heads?" Statistics says "I flipped 1000 times and got 530 heads — is the coin fair?"

## 3. Why it exists
Every ML model is a probabilistic function mapping inputs to distributions over outputs. Without probability and statistics, we cannot reason about model uncertainty, dataset representativeness, or whether an observed improvement is real or noise.

## 4. Mechanics
- **Probability Rules:** $P(A \cup B) = P(A)+P(B)-P(A\cap B)$. $P(A|B) = P(A\cap B)/P(B)$.
- **Bayes' Theorem:** $P(H|E) = P(E|H)P(H)/P(E)$. Posterior = Likelihood × Prior / Evidence.
- **Distributions:** Gaussian $\mathcal{N}(\mu,\sigma^2)$, Bernoulli, Categorical (softmax output), Poisson.
- **Expectation & Variance:** $E[X] = \sum x P(x)$. $\text{Var}(X) = E[X^2]-E[X]^2$.
- **Central Limit Theorem:** Sum of many i.i.d. random variables → Gaussian, regardless of the original distribution. Explains why gradient noise becomes Gaussian in SGD.
- **Maximum Likelihood Estimation (MLE):** Choose parameters $\theta$ that maximize $P(\text{data}|\theta)$. Training NNs with Cross-Entropy loss is MLE under a Categorical distribution.

## 5. Complexity (Time & Space)
- N/A — mathematical framework, not an algorithm.

## 6. Tiny worked example
Bayes' Theorem (Medical Test):
- Disease prevalence: $P(D)=0.01$.
- Test sensitivity: $P(+|D)=0.99$.
- False positive rate: $P(+|\neg D)=0.05$.
- $P(D|+) = \frac{0.99 \times 0.01}{0.99\times0.01 + 0.05\times0.99} \approx 0.167$.
Only 16.7% chance of disease even with a positive test! The rare disease prior dominates.

## 7. Code (Python)
```python
import numpy as np
from scipy import stats

# MLE for Gaussian: mean and std from data
data = np.array([2.1, 2.9, 3.1, 3.8, 4.2])
mu_mle = np.mean(data)        # 3.22
sigma_mle = np.std(data)      # 0.74

# P-value: is observed mean significantly different from 3.0?
t_stat, p_val = stats.ttest_1samp(data, popmean=3.0)
print(f"p-value: {p_val:.3f}")  # > 0.05 → not significant
```

## 8. Common mistakes
- Confusing correlation with causation. High $r$ does not imply A causes B.
- Forgetting that $P(A|B) \neq P(B|A)$. The Prosecutor's Fallacy.

## 9. 30-second interview answer
"Probability quantifies uncertainty and powers every ML model through distributions, expectations, and Bayes' Theorem. MLE — maximizing the likelihood of the training data — is the theoretical basis of cross-entropy loss. The Central Limit Theorem guarantees that stochastic gradient noise approaches Gaussian, justifying many optimization assumptions."

## 10. 2-minute interview answer
"Probability and statistics are the formal language of ML. Every neural network output is a parameterized probability distribution — classification outputs a Categorical distribution via softmax, regression assumes a Gaussian via MSE loss. Bayes' Theorem is the principled way to update beliefs given evidence, and it directly underpins probabilistic graphical models and Bayesian neural networks. In practice, when interviewer asks 'why does your model have 80% accuracy on the test set?' you need statistics to determine whether that's genuinely better than baseline or within the noise of a small evaluation set — which requires hypothesis testing and p-values."

## 11. Follow-ups
- "What is the difference between MLE and MAP estimation?" (MAP adds a prior, maximizing $P(\theta|\text{data}) \propto P(\text{data}|\theta)P(\theta)$. L2 regularization is MAP with a Gaussian prior on weights).

## 12. Deeper questions
- "What is the Bias-Variance decomposition mathematically?" ($\text{MSE} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise}$).

## 13. Related concepts
- **Loss Functions**: Cross-entropy is negative log-likelihood under a Categorical distribution.
- **Bayesian Deep Learning**: Applies posterior inference over weights.

## 14. When it breaks / Edge cases
- CLT requires i.i.d. samples. Correlated data (time series) violates this, invalidating standard confidence intervals.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:*
Every component: softmax outputs are probabilities; cross-entropy is negative log-likelihood; dropout at inference approximates Bayesian uncertainty; A/B testing model releases uses hypothesis testing.
""")

wc("00-foundations/linear-algebra.md", r"""# Linear Algebra for ML

## 1. Definition
Linear algebra is the branch of mathematics studying vectors, matrices, and linear transformations. It provides the computational substrate for all neural network operations.

## 2. Intuition
A neural network layer is a mathematical machine that takes an input arrow (vector) in some high-dimensional space and stretches, rotates, or squishes it into a new arrow in a different space. Linear algebra formalizes and makes efficient every single one of these transformations.

## 3. Why it exists
ML models operate on collections of numbers (tensors). All forward passes, gradient computations, and attention mechanisms are matrix multiplications and vector operations. Without linear algebra, we have no efficient, parallelizable operations.

## 4. Mechanics
- **Vector Space:** A set of vectors closed under addition and scalar multiplication.
- **Matrix Multiplication:** $(AB)_{ij} = \sum_k A_{ik} B_{kj}$. Composing linear transformations.
- **Transpose:** $(A^T)_{ij} = A_{ji}$. Used in dot products and gradient computation.
- **Eigenvalues/Eigenvectors:** $Av = \lambda v$. Eigenvectors are directions unchanged by transformation; eigenvalues scale them.
- **SVD:** $A = U\Sigma V^T$. Decomposes any matrix. Used in PCA, recommendation systems, and understanding LoRA.
- **Norms:** $||v||_2 = \sqrt{\sum v_i^2}$ (L2). $||v||_1 = \sum |v_i|$ (L1). Used in regularization and similarity.

## 5. Complexity (Time & Space)
- Matrix mult $(m \times n)(n \times p)$: $O(mnp)$ naively, heavily optimized by BLAS to $O(mn p / \text{CPU parallelism})$.
- SVD of $m \times n$ matrix: $O(mn^2)$.

## 6. Tiny worked example
Rotation in 2D: $R = \begin{pmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{pmatrix}$. Applied to $v = [1, 0]$: $Rv = [\cos\theta, \sin\theta]$. The vector rotates; its length is preserved ($||Rv||=1$).

## 7. Code (Python)
```python
import numpy as np

A = np.array([[1, 2], [3, 4]], dtype=float)
b = np.array([5, 6])

# Solve Ax = b via least-squares (linear regression closed form)
x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

# SVD decomposition
U, S, Vt = np.linalg.svd(A)  # A = U @ diag(S) @ Vt

# Cosine similarity between two vectors
v1, v2 = np.array([1, 0, 1]), np.array([0, 1, 1])
cos_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
```

## 8. Common mistakes
- Treating matrix multiplication as commutative: $AB \neq BA$ in general.
- Ignoring numerical stability: large condition numbers in matrices cause catastrophic cancellation.

## 9. 30-second interview answer
"Linear algebra provides the operations for every neural network layer: matrix multiplications for linear transformations, dot products for similarity (Attention), SVD for dimensionality reduction, and norms for regularization. GPUs exist specifically to execute large batched matrix multiplications efficiently."

## 10. 2-minute interview answer
"Every forward pass of a neural network is a chain of matrix multiplications and element-wise nonlinearities. An embedding lookup is matrix-vector multiplication. Attention is $\text{softmax}(QK^T/\sqrt{d_k})V$ — entirely matrix operations. Backpropagation computes Jacobians (matrices of partial derivatives) via the chain rule, which is matrix multiplication in reverse. Understanding SVD is especially important for ML engineers: it's how PCA works, how LoRA's low-rank approximation is motivated, and how we measure the intrinsic dimensionality of data. The matrix rank is how many independent directions of variation exist — high-rank matrices contain more information."

## 11. Follow-ups
- "What is Principal Component Analysis?" (PCA rotates data to the eigenvectors of the covariance matrix, sorted by eigenvalue. The top $k$ components capture the most variance, enabling dimensionality reduction).

## 12. Deeper questions
- "Why is the Transformer's attention score divided by $\sqrt{d_k}$?" (Without scaling, larger dimensions produce larger dot products, pushing softmax into saturation regions with near-zero gradients).

## 13. Related concepts
- **Tensors**: Generalization of matrices.
- **Cosine Similarity**: Derived from the dot product and L2 norm.

## 14. When it breaks / Edge cases
- Singular matrices (rank-deficient) cannot be inverted, breaking exact linear regression solutions.

## 15. Comparison with alternative approaches
- N/A — foundational mathematics.

---
*Where this shows up in ML:*
`nn.Linear(in, out)` is $y = xW^T + b$ — pure matrix multiplication. Attention is three matrix multiplications. The gradient of a matrix operation is a matrix operation.
""")

# ---- 01-ml-basics ----
wc("01-ml-basics/linear-regression.md", r"""# Linear Regression

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
""")

wc("01-ml-basics/logistic-regression.md", r"""# Logistic Regression

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
""")

wc("01-ml-basics/decision-trees.md", r"""# Decision Trees

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
""")

wc("03-nlp/transformers.md", r"""# Transformers in NLP

## 1. Definition
The Transformer is a sequence-to-sequence architecture introduced in "Attention Is All You Need" (2017) that replaced recurrent architectures with purely attention-based mechanisms, becoming the foundation of all modern NLP models.

## 2. Intuition
Unlike RNNs that read text like a human — word by word, trying to remember — the Transformer reads the entire sentence simultaneously, like a photograph, and directly draws connections between any word and any other word in a single computation step.

## 3. Why it exists
RNNs were slow to train (sequential processing prevented GPU parallelization) and forgot distant context despite LSTM's improvements. The Transformer exists to parallelize sequence processing and provide direct (non-sequential) connectivity between all positions.

## 4. Mechanics
The full Transformer architecture:
1. **Tokenize** input → integer IDs.
2. **Embed** tokens → dense vectors.
3. **Add Positional Encodings** — since there's no recurrence, inject position information explicitly.
4. **Encoder** (in seq2seq models): $N$ stacks of [Multi-Head Self-Attention → Add & Norm → Feed-Forward → Add & Norm].
5. **Decoder** (in seq2seq models): Same, plus Masked Self-Attention (prevents looking at future tokens) and Cross-Attention (attends to encoder output).
6. **Output projection** → softmax over vocabulary → probabilities.

## 5. Complexity (Time & Space)
- **Time:** $O(N^2 d)$ per layer due to the attention matrix computation.
- **Space:** $O(N^2)$ for the attention matrix per head.

## 6. Tiny worked example
English → French translation: "The cat sat" → "Le chat s'est assis."
The decoder, when generating "chat", attends heavily to "cat" in the encoder output (Cross-Attention). The decoder's own Masked Self-Attention allows "chat" to attend to "Le" but NOT to future tokens "s'est assis."

## 7. Code (Python)
```python
import torch
import torch.nn as nn

# PyTorch's built-in Transformer
transformer = nn.Transformer(
    d_model=512,
    nhead=8,
    num_encoder_layers=6,
    num_decoder_layers=6,
    dim_feedforward=2048,
    dropout=0.1
)

src = torch.rand(10, 32, 512)  # (seq_len, batch, d_model)
tgt = torch.rand(20, 32, 512)
out = transformer(src, tgt)  # (20, 32, 512)
```

## 8. Common mistakes
- Thinking all modern LLMs use the full encoder-decoder Transformer. GPT-series uses decoder-only. BERT uses encoder-only. Only T5, BART, and translation models use full encoder-decoder.
- Forgetting that the Positional Encoding is added (not concatenated) to the token embedding.

## 9. 30-second interview answer
"The Transformer replaced RNNs with Multi-Head Self-Attention, enabling fully parallel sequence processing. Its $O(N^2)$ attention complexity is a tradeoff for direct, length-independent connectivity between all tokens. Modern LLMs are either encoder-only (BERT), decoder-only (GPT), or full encoder-decoder (T5)."

## 10. 2-minute interview answer
"The Transformer's key insight was that you don't need recurrence to model sequences — you need attention. By computing pairwise attention between all tokens simultaneously, it achieves what LSTMs struggled with: direct connections over arbitrarily long distances. The architecture is modular: 6 encoder layers of Self-Attention + FFN, each with Residual Connections and Layer Normalization to stabilize training. The decoder adds Masked Self-Attention (causal masking) to prevent the model from 'cheating' by looking at future target tokens, plus Cross-Attention to incorporate the encoded source context. This architecture scaled to become the foundation of BERT, GPT, T5, and every modern LLM by simply scaling up depth, width, heads, and training data."

## 11. Follow-ups
- "Why is Masked Self-Attention necessary in the decoder?" (During training, the entire target sequence is fed in parallel. Masking prevents the model from attending to future target tokens — this would make next-token prediction trivial and the model would learn nothing).

## 12. Deeper questions
- "How does Cross-Attention differ from Self-Attention?" (In Cross-Attention: $Q$ comes from the decoder's current state, $K$ and $V$ come from the encoder's output. This lets the decoder query the full source context at every generation step).

## 13. Related concepts
- **BERT**: Encoder-only Transformer, pretrained with Masked Language Modeling.
- **GPT**: Decoder-only Transformer, pretrained with causal next-token prediction.

## 14. When it breaks / Edge cases
- $O(N^2)$ attention breaks for very long sequences (>4096 tokens naively). Addressed by Sparse Attention, Sliding Window, or linear attention approximations.

## 15. Comparison with alternative approaches
- **vs LSTM:** LSTM is $O(N)$ inference (sequential), handles long sequences with less memory, but can't be parallelized during training. Transformer is $O(N^2)$ in sequence but $O(1)$ parallel training depth.

---
*Where this shows up in ML:*
Every state-of-the-art NLP model: GPT-4, Claude, Llama, Gemini, BERT, T5.
""")

print("Batch D Part 1 complete (foundations + ml-basics + nlp/transformers)")
