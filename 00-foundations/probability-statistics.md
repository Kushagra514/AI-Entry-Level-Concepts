# Probability & Statistics for ML

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
