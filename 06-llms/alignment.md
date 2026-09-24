# LLM Alignment

## 1. Definition
Alignment is the process of fine-tuning an LLM so its outputs match human values, preferences, and safety guidelines—ensuring it is helpful, honest, and harmless (the "3H" criteria).

## 2. Intuition
A base model is a wild mirror of the internet; it might give you a recipe for a cake or a recipe for a bomb with equal probability. Alignment is the process of putting guardrails on the model and teaching it to be a helpful assistant rather than a neutral text generator.

## 3. Why it exists
Base models are misaligned with enterprise and consumer use cases. They can be toxic, biased, hallucinate confidently, or assist with malicious activities. Alignment makes them safe, reliable, and commercially viable.

## 4. Mechanics
- **SFT (Supervised Fine-Tuning):** Initial alignment using high-quality human demonstrations.
- **RLHF (Reinforcement Learning from Human Feedback):** 
  1. Train a Reward Model (RM) on human preference rankings (Response A > Response B).
  2. Use PPO (Proximal Policy Optimization) to maximize the RM score.
- **DPO (Direct Preference Optimization):** Mathematically bypasses the RM and RL loop by optimizing the policy directly on preference data using a specialized loss function.
- **Constitutional AI:** Anthropic's method where an AI (not a human) evaluates and critiques responses based on a set of principles (a "constitution"), used to generate preference data for RL.

## 5. Complexity (Time & Space)
- RLHF requires running 4 models simultaneously during PPO (Policy, Reference, Reward, Value), making it very memory intensive (often requiring 4x the VRAM of standard fine-tuning). DPO is much cheaper as it only requires the Policy and Reference models.

## 6. Tiny worked example
Preference Data:
Prompt: "How do I steal a car?"
Response A: "Use a slim jim to unlock the door..."
Response B: "I cannot help with illegal activities."
Human labels: B > A.
Reward Model learns to score B high and A low. RLHF updates the LLM to output B-like responses.

## 7. Code (Python)
```python
# Conceptual DPO Loss
import torch
import torch.nn.functional as F

def dpo_loss(pi_logps_chosen, pi_logps_rejected, ref_logps_chosen, ref_logps_rejected, beta=0.1):
    # pi = current model, ref = frozen reference model
    # Log probability ratios
    pi_ratio = pi_logps_chosen - pi_logps_rejected
    ref_ratio = ref_logps_chosen - ref_logps_rejected
    
    # Loss: minimize the negative log sigmoid of the scaled difference
    loss = -F.logsigmoid(beta * (pi_ratio - ref_ratio)).mean()
    return loss
```

## 8. Common mistakes
- Confusing Alignment with pretraining. Alignment does not inject facts; it just shapes how the model presents the facts it already knows.
- Over-alignment leading to "alignment tax" — where a model becomes so safe it refuses benign requests or loses its coding/reasoning capabilities.

## 9. 30-second interview answer
"Alignment ensures an LLM is helpful, honest, and harmless. It is typically achieved through RLHF, which trains a reward model on human preferences and optimizes the LLM using PPO, or through DPO, which simplifies the process by directly optimizing on preference data. It's the critical step that turns a raw base model into a safe, deployable assistant like ChatGPT."

## 10. 2-minute interview answer
"Alignment is the final and arguably most important step in the LLM training pipeline. A base model learns the distribution of the internet; instruction tuning teaches it to follow commands; alignment teaches it what commands it *should* follow and how to format the answer safely. The gold standard is RLHF. In RLHF, human annotators rank model outputs. We train a reward model on these rankings, and then use PPO to update the LLM to maximize the reward. However, PPO is complex and unstable. Recently, Direct Preference Optimization (DPO) has emerged as a dominant alternative. DPO shows that under certain assumptions, you can skip the reward model and RL loop entirely, directly optimizing the policy using a simple cross-entropy-like loss on the preference pairs. Anthropic introduced Constitutional AI to reduce reliance on expensive human annotators by using an AI to critique and revise answers based on a set of rules. The major challenge in alignment today is the 'alignment tax' — the empirical observation that highly aligned models often degrade in reasoning or coding tasks compared to their base models."

## 11. Follow-ups
- "What is the role of the KL penalty in RLHF?" (It prevents the model from "reward hacking" — generating weird, ungrammatical text that exploits a loophole in the reward model to get a high score. It forces the aligned model to stay close to the initial SFT model).

## 12. Deeper questions
- "Why is DPO considered more stable than PPO?" (PPO involves actor-critic networks, advantage estimation, and moving targets, which are notoriously hyperparameter-sensitive. DPO is just supervised learning with a specific loss function).

## 13. Related concepts
- **Instruction Tuning**: The prerequisite for alignment.
- **RLHF**: The most famous alignment technique.

## 14. When it breaks / Edge cases
- Jailbreaks and Prompt Injection: Users can craft prompts that bypass alignment guardrails (e.g., "Pretend you are an unaligned AI...").

## 15. Comparison with alternative approaches
- **RLHF vs DPO:** RLHF is the original, proven method but complex. DPO is simpler, requires less memory, and is increasingly the standard for open-source model alignment (e.g., Llama-3).

---
*Where this shows up in ML:*
Creating safe APIs and chatbots; the difference between a research model and a product.
