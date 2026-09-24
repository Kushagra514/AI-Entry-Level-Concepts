# ML Interview Questions

Each question includes: Expected Answer • Key Concepts • Likely Follow-Up • Common Wrong Answer • What Strong Candidates Add

---

## Q1. What is the bias-variance tradeoff?

**Expected Answer:** Every model's test error decomposes as: $\text{Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise}$. Bias is error from wrong assumptions (underfitting); variance is sensitivity to training data fluctuations (overfitting). Simpler models have high bias, low variance; complex models have low bias, high variance. Regularization, ensemble methods, and cross-validation manage this tradeoff.

**Key Concepts:** Decomposition formula, underfitting vs overfitting, regularization, ensemble methods.

**Likely Follow-Up:** "How does ensemble learning (Random Forest) reduce variance without increasing bias?" — Averaging independent high-variance models reduces their combined variance by factor $1/N$ (assuming independence).

**Common Wrong Answer:** "Bias is when the model is biased toward certain predictions" — this conflates statistical bias with fairness bias.

**Strong Candidates Add:** The mathematical derivation $E[(y-\hat{f})^2] = \text{Bias}[\hat{f}]^2 + \text{Var}[\hat{f}] + \sigma^2$; how dropout addresses variance; that irreducible noise sets a hard floor on achievable performance.

---

## Q2. Explain gradient descent and its variants.

**Expected Answer:** Gradient Descent minimizes loss by iteratively moving parameters in the opposite direction of the gradient: $\theta \leftarrow \theta - \alpha\nabla_\theta\mathcal{L}$. Variants: Batch GD (full dataset per step, slow), SGD (one sample, noisy), Mini-batch SGD (practical default). Adaptive optimizers: Adam (momentum + per-parameter LR via first and second moment estimates), RMSProp, AdaGrad.

**Key Concepts:** Gradient, learning rate, SGD, momentum, Adam, convergence.

**Likely Follow-Up:** "Why does SGD sometimes generalize better than Adam?" — SGD's noise acts as implicit regularization, finding flatter minima that generalize better. Adam converges faster but can find sharp, less generalizable minima.

**Common Wrong Answer:** Describing Adam as "always better than SGD" — several papers show SGD + momentum outperforms Adam on image classification when properly tuned.

**Strong Candidates Add:** Adam hyperparameters ($\beta_1=0.9$, $\beta_2=0.999$, $\epsilon=10^{-8}$), learning rate scheduling (warmup + cosine decay), gradient clipping for RNN/Transformer training stability.

---

## Q3. What is cross-entropy loss and why is it used for classification?

**Expected Answer:** Cross-entropy loss: $\mathcal{L} = -\sum_k y_k \log \hat{p}_k$. For binary classification: $\mathcal{L} = -[y\log\hat{p} + (1-y)\log(1-\hat{p})]$. It is derived from Maximum Likelihood Estimation: minimizing cross-entropy is equivalent to maximizing the likelihood of the training data under a Categorical distribution. It penalizes confident wrong predictions logarithmically (infinite penalty for predicting 0 probability for the correct class).

**Key Concepts:** MLE, log-likelihood, softmax, probability calibration.

**Likely Follow-Up:** "Why not use MSE for classification?" — MSE doesn't penalize confident wrong predictions sufficiently and produces very small gradients when the sigmoid output is near 0 or 1 (vanishing gradient in output layer).

**Common Wrong Answer:** "Cross-entropy just measures how close the predictions are to labels" — misses the MLE/information-theoretic grounding.

**Strong Candidates Add:** The connection $H(P,Q) = H(P) + D_{KL}(P||Q)$ — minimizing cross-entropy is minimizing KL divergence from the true distribution; label smoothing as a regularization that prevents overconfident predictions.

---

## Q4. How does a Random Forest differ from Gradient Boosting?

**Expected Answer:** Random Forest grows many independent decision trees in parallel using bootstrap samples and random feature subsets (bagging + feature randomization). It reduces variance by averaging predictions. Gradient Boosting grows trees sequentially, each fitting the residuals of the previous ensemble, reducing bias. RF is harder to overfit; XGBoost/LightGBM (GBT implementations) achieve higher accuracy but require more careful regularization.

**Key Concepts:** Bagging vs boosting, variance reduction vs bias reduction, parallel vs sequential.

**Likely Follow-Up:** "When would you choose Random Forest over XGBoost?" — RF is preferred when training speed matters, when data is very noisy (boosting can overfit noise), or when interpretability of individual trees is needed.

**Common Wrong Answer:** Confusing bagging and boosting. Bagging = parallel, independent. Boosting = sequential, dependent.

**Strong Candidates Add:** Gradient Boosting's update rule: $F_m(x) = F_{m-1}(x) + \gamma_m h_m(x)$ where $h_m$ fits negative gradients (pseudo-residuals); LightGBM's leaf-wise growth vs XGBoost's level-wise growth; SHAP values for both.

---

## Q5. What is overfitting and how do you prevent it?

**Expected Answer:** Overfitting occurs when a model learns the training data noise rather than the underlying signal, achieving high training accuracy but poor generalization. Prevention: more training data, regularization (L1/L2/dropout), early stopping, cross-validation, reducing model complexity, data augmentation, batch normalization.

**Key Concepts:** Generalization, train/val/test split, regularization, model complexity.

**Likely Follow-Up:** "How does dropout prevent overfitting?" — Randomly zeroing activations forces the network to learn redundant representations. No single unit can rely on specific co-activations, preventing complex co-adaptations. Equivalent to training an ensemble of $2^N$ thinned networks.

**Common Wrong Answer:** Treating overfitting as "model is too big" — model size alone isn't the issue; the ratio of parameters to training samples is.

**Strong Candidates Add:** Double descent phenomenon — as model size grows beyond interpolation threshold, test error can decrease again; early stopping implicitly bounds model complexity by the optimization path; weight decay (L2) is equivalent to Gaussian prior MAP estimation.
