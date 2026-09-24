# Statistics & Math Cheat Sheet for ML Interviews

## Probability Rules

| Rule | Formula |
|---|---|
| Addition | $P(A \cup B) = P(A)+P(B)-P(A\cap B)$ |
| Multiplication | $P(A \cap B) = P(A|B)P(B)$ |
| Bayes' Theorem | $P(H|E) = \frac{P(E|H)P(H)}{P(E)}$ |
| Law of Total Probability | $P(B) = \sum_i P(B|A_i)P(A_i)$ |
| Conditional Independence | $P(A|B,C)=P(A|C)$ if A⊥B|C |

## Key Distributions

| Distribution | PMF/PDF | Mean | Variance | ML Use |
|---|---|---|---|---|
| Bernoulli$(p)$ | $p^x(1-p)^{1-x}$ | $p$ | $p(1-p)$ | Binary classification |
| Binomial$(n,p)$ | $\binom{n}{k}p^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ | Count successes |
| Gaussian $\mathcal{N}(\mu,\sigma^2)$ | $\frac{1}{\sqrt{2\pi\sigma^2}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ | $\mu$ | $\sigma^2$ | Weight init, noise |
| Poisson$(\lambda)$ | $\frac{\lambda^k e^{-\lambda}}{k!}$ | $\lambda$ | $\lambda$ | Event counts |
| Uniform$(a,b)$ | $\frac{1}{b-a}$ | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$ | Random sampling |

## Statistical Tests

| Test | When to Use | Null Hypothesis | Typical α |
|---|---|---|---|
| t-test (one-sample) | Compare sample mean to population | $\mu = \mu_0$ | 0.05 |
| t-test (two-sample) | Compare two group means | $\mu_1 = \mu_2$ | 0.05 |
| Chi-squared test | Categorical association | Independence | 0.05 |
| ANOVA | Compare 3+ group means | All means equal | 0.05 |
| Wilcoxon | Non-parametric t-test alternative | Distributions equal | 0.05 |

## Important Inequalities & Theorems

| Theorem | Statement | ML Relevance |
|---|---|---|
| Central Limit Theorem | $\bar{X} \to \mathcal{N}(\mu, \sigma^2/n)$ as $n\to\infty$ | SGD gradient noise is Gaussian |
| Law of Large Numbers | $\bar{X} \to \mu$ as $n\to\infty$ | Consistency of estimators |
| Jensen's Inequality | $f(E[X]) \leq E[f(X)]$ for convex $f$ | KL divergence is non-negative |
| Chebyshev's Inequality | $P(|X-\mu|\geq k\sigma) \leq \frac{1}{k^2}$ | Bounding tail probabilities |

## Key Formulas

| Concept | Formula |
|---|---|
| MLE | $\hat{\theta}_{MLE} = \arg\max_\theta \prod_i P(x_i|\theta)$ |
| MAP | $\hat{\theta}_{MAP} = \arg\max_\theta [\sum_i\log P(x_i|\theta) + \log P(\theta)]$ |
| KL Divergence | $D_{KL}(P||Q) = \sum_x P(x)\log\frac{P(x)}{Q(x)} \geq 0$ |
| Entropy | $H(X) = -\sum_x P(x)\log P(x)$ |
| Cross-Entropy | $H(P,Q) = -\sum_x P(x)\log Q(x) = H(P) + D_{KL}(P||Q)$ |
| Mutual Information | $I(X;Y) = H(X) - H(X|Y)$ |
| Pearson Correlation | $r = \frac{\sum(x-\bar{x})(y-\bar{y})}{\sqrt{\sum(x-\bar{x})^2\sum(y-\bar{y})^2}}$ |
| Cosine Similarity | $\cos(\theta) = \frac{A\cdot B}{||A||||B||}$ |
| Gradient Descent Update | $\theta \leftarrow \theta - \alpha\nabla_\theta\mathcal{L}$ |
| Chain Rule (backprop) | $\frac{\partial\mathcal{L}}{\partial x} = \frac{\partial\mathcal{L}}{\partial y}\cdot\frac{\partial y}{\partial x}$ |
| Attention Formula | $\text{softmax}(QK^T/\sqrt{d_k})V$ |
| L2 Regularization (Ridge) | $\mathcal{L}_{reg} = \mathcal{L} + \lambda||W||_2^2$ |
| Softmax | $\sigma(z)_i = e^{z_i}/\sum_j e^{z_j}$ |
| Sigmoid | $\sigma(z) = 1/(1+e^{-z})$ |
| ReLU | $f(z) = \max(0, z)$ |

## Hypothesis Testing Quick Reference

```
1. State H₀ (null) and H₁ (alternative)
2. Choose significance level α (usually 0.05)
3. Compute test statistic
4. Find p-value = P(data this extreme | H₀ true)
5. If p < α: Reject H₀ (result is statistically significant)
6. If p ≥ α: Fail to reject H₀ (insufficient evidence)

Type I Error (False Positive): Reject H₀ when it's true. Rate = α
Type II Error (False Negative): Accept H₀ when it's false. Rate = β
Power = 1 - β = P(reject H₀ | H₁ is true)
```
