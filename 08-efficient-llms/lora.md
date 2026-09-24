# LoRA (Low-Rank Adaptation)

## 1. Definition
LoRA is a Parameter-Efficient Fine-Tuning (PEFT) technique that freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture, significantly reducing the number of trainable parameters.

## 2. Intuition
Imagine a gigantic, 10,000-page encyclopedia (the LLM). You want to update it for medical terminology. Instead of rewriting the entire encyclopedia (Full Fine-Tuning), you write your changes on a small stack of sticky notes (LoRA matrices) and stick them on the relevant pages. During reading, you look at the book and the sticky notes together.

## 3. Why it exists
Full fine-tuning of a 70B parameter model requires clusters of A100 GPUs and hundreds of gigabytes of VRAM to store optimizer states and gradients for every weight. LoRA exists to allow researchers to fine-tune massive models on a single consumer GPU by reducing the trainable parameters by up to 10,000x.

## 4. Mechanics
- A standard neural network layer performs $W_0 x$, where $W_0$ is a massive $d 	imes d$ matrix.
- LoRA freezes $W_0$ and adds a delta update matrix: $\Delta W = B 	imes A$.
- Matrix $A$ has shape $d 	imes r$, and $B$ has shape $r 	imes d$, where $r$ (rank) is very small (e.g., 8 or 16).
- $B 	imes A$ results in a $d 	imes d$ matrix, but because of the "low rank" bottleneck, it contains drastically fewer parameters.
- Forward pass becomes: $y = W_0 x + BAx$.
- Only $A$ and $B$ receive gradient updates.

## 5. Complexity (Time & Space)
- **Time Complexity:** Slightly slower forward pass during training (requires computing $BAx$). No latency hit during inference (matrices can be merged).
- **Space Complexity:** Huge VRAM savings. Training parameters drop from $d^2$ to $2rd$.

## 6. Tiny worked example
Let $W_0$ be $1000 	imes 1000$ (1,000,000 parameters).
Let Rank $r = 4$.
Matrix $A$ is $1000 	imes 4$ (4,000 params). Matrix $B$ is $4 	imes 1000$ (4,000 params).
Total trainable params: 8,000.
Reduction: 99.2% fewer parameters to train!

## 7. Code (Python, with type hints)
```python
# Conceptual implementation of a LoRA Linear layer
import torch
import torch.nn as nn

class LoRALinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, rank: int = 8):
        super().__init__()
        # The frozen pre-trained weights
        self.W_0 = nn.Linear(in_features, out_features, bias=False)
        self.W_0.weight.requires_grad = False
        
        # The LoRA trainable matrices
        self.lora_A = nn.Parameter(torch.randn(in_features, rank))
        self.lora_B = nn.Parameter(torch.zeros(rank, out_features)) # Init B to 0
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pre-trained output + LoRA delta
        frozen_out = self.W_0(x)
        lora_out = (x @ self.lora_A) @ self.lora_B
        return frozen_out + lora_out
```

## 8. Common mistakes
- Initializing matrix $B$ with random noise instead of zeros. If both are random, the initial forward pass will output garbage. Initializing $B$ to 0 ensures the initial LoRA output is 0, keeping the pre-trained behavior exactly identical at step 0.
- Forgetting to merge weights for inference.

## 9. 30-second interview answer
"LoRA is a parameter-efficient fine-tuning method. It freezes the original model weights and injects two low-rank matrices (A and B) into the architecture. By training only these much smaller matrices, we reduce VRAM requirements exponentially while achieving performance nearly identical to full fine-tuning."

## 10. 2-minute interview answer
"LoRA leverages the hypothesis that the 'intrinsic rank' of neural network updates is very low—meaning we don't need to change every weight independently to learn a new task. Instead of updating a massive $D 	imes D$ weight matrix, LoRA freezes it and learns an additive update represented by the product of two low-rank matrices, $B$ and $A$, with an inner dimension $r$. This reduces the optimizer state memory by orders of magnitude, making it possible to fine-tune 7B or 13B models on a single GPU. The greatest engineering benefit of LoRA is at inference time: because matrix addition is distributive, we can statically add the trained $BA$ matrix into the original $W_0$ matrix. This 'weight merging' means deploying a LoRA-tuned model incurs absolutely zero latency penalty compared to the base model."

## 11. Follow-ups
- "What is Alpha in LoRA?" (A scaling factor applied to the LoRA output, used to balance the magnitude of the update against the frozen weights, often set to 2x the Rank).

## 12. Deeper questions
- "If I want to serve 50 different customers with 50 different fine-tunes, how does LoRA help?" (You load the base model into GPU memory ONCE. You swap the tiny LoRA 'adapters' in and out of VRAM dynamically per request (Multi-LoRA serving), saving terabytes of VRAM).

## 13. Related concepts
- **QLoRA**: LoRA combined with Quantization.
- **Fine-Tuning**: The overarching goal.

## 14. When it breaks / Edge cases
- LoRA struggles with completely novel knowledge injection (like a language the base model has never seen). Full fine-tuning is better for fundamental domain shifts.

## 15. Comparison with alternative approaches
- **vs Prompt Tuning / Prefix Tuning:** LoRA modifies the computation internally and performs better. Prompt tuning consumes valuable context window tokens.

---
*Where this shows up in ML:* 
The `peft` library by HuggingFace, used to train almost every open-source customized model.
