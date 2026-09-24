# Quantization

## 1. Definition
Quantization is the process of mapping high-precision neural network parameters (weights and activations, typically 32-bit floating point) to lower-precision data types (like 8-bit or 4-bit integers) to reduce memory footprint and increase inference speed, with minimal loss in accuracy.

## 2. Intuition
Imagine a high-res photograph taking up 10 MB. You can compress it to a 1 MB JPEG. The colors might be slightly less precise if you zoom in, but to the human eye, it looks the same. Quantization does this to neural network weights, shrinking a 28GB model to 4GB so it fits on a laptop GPU.

## 3. Why it exists
LLMs are massively memory-bound. A 70-Billion parameter model requires ~140 GB of VRAM just to load in 16-bit precision (requiring 2x 80GB A100 GPUs costing $30k). Quantizing to 4-bit reduces this to ~35 GB, allowing deployment on vastly cheaper consumer hardware. Furthermore, lower precision allows faster memory bandwidth transfer, speeding up inference.

## 4. Mechanics
- **Data Types:** FP32 (Full precision), FP16/BF16 (Half precision, standard for LLMs), INT8, INT4, NF4 (NormalFloat4, optimized for normally distributed weights).
- **Scaling Factor:** To convert a float tensor to INT8: $X_{int8} = \text{round}(X_{float} / S) + Z$. $S$ is the scale (e.g., $\max(|X|) / 127$), $Z$ is the zero-point.
- **PTQ (Post-Training Quantization):** Take a fully trained model and quantize it. Methods: GPTQ, AWQ, SmoothQuant.
- **QAT (Quantization-Aware Training):** Simulate quantization errors during the training forward pass, so the model learns to be robust to them. Yields better accuracy but requires retraining.

## 5. Complexity (Time & Space)
- **Memory reduction:** FP16 to INT8 halves memory (2x reduction). FP16 to INT4 is a 4x reduction.
- **Speed:** Can increase speed by 2-3x because reading weights from GPU memory (HBM) is the bottleneck in LLM inference.

## 6. Tiny worked example
Weights: `[-1.2, 0.4, 2.8, -3.0]` (FP32)
Map to INT8 range `[-127, 127]`. Max absolute value is 3.0.
Scale factor $S = 3.0 / 127 \approx 0.0236$.
Quantized: `[-1.2/S, 0.4/S, 2.8/S, -3.0/S]` -> Round -> `[-51, 17, 119, -127]`.
Dequantized at inference: `[-51*S, ...]` -> `[-1.203, 0.401, 2.808, -3.0]`. Tiny precision loss introduced!

## 7. Code (Python)
```python
# Using HuggingFace bitsandbytes for 4-bit quantization
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# Configure QLoRA's 4-bit NormalFloat quantization
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",       # NormalFloat 4-bit
    bnb_4bit_compute_dtype=torch.bfloat16, # Compute in 16-bit
    bnb_4bit_use_double_quant=True   # Quantize the quantization constants
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b",
    quantization_config=quant_config,
    device_map="auto"
)
# A 7B model now takes ~4GB VRAM instead of 14GB!
```

## 8. Common mistakes
- Naive round-to-nearest quantization for LLMs. LLMs feature massive "outliers" in their activations (values 100x larger than others). Naive scaling based on the max value crushes all normal values to zero, destroying the model.
- Thinking compute happens in 4-bit. In frameworks like bitsandbytes, weights are stored in 4-bit, but dequantized to 16-bit on the fly in SRAM before the matrix multiplication happens.

## 9. 30-second interview answer
"Quantization reduces the precision of model weights (e.g., from 16-bit to 4-bit integers) to drastically reduce memory footprint and increase inference speed. For LLMs, Post-Training Quantization (PTQ) techniques like GPTQ or AWQ are standard, carefully managing outlier activations to preserve accuracy. QLoRA utilizes NF4 quantization to allow fine-tuning of massive models on single consumer GPUs."

## 10. 2-minute interview answer
"Quantization is the primary reason open-source LLMs are accessible today. Because LLM inference is memory-bandwidth bound, shrinking weights from 16-bit floats to 4-bit integers not only cuts VRAM usage by 75% but also dramatically speeds up generation. The challenge is the 'outlier problem'. At scale, LLMs develop specific feature dimensions with extreme magnitude. If you naively scale a tensor to an 8-bit integer based on its maximum value, these outliers force the scaling factor to be so large that 99% of the normal weights get rounded to zero, ruining the model. Modern PTQ algorithms solve this elegantly. SmoothQuant migrates the difficulty from activations to weights mathematically. GPTQ uses second-order Hessian information to adjust the remaining weights to compensate for the quantization error of the rounded weights. For fine-tuning, QLoRA introduced NF4 (NormalFloat4), a data type theoretically optimal for normally distributed weights, allowing us to store the base model in 4-bit while computing gradients for 16-bit LoRA adapters."

## 11. Follow-ups
- "What is the difference between weight-only quantization and weight-activation quantization?" (Weight-only stores weights in INT4/8 but computes in FP16. Solves memory bottlenecks. Weight-activation quantizes both, allowing the use of INT8 tensor cores for math, speeding up compute bottlenecks, but is much harder to maintain accuracy).

## 12. Deeper questions
- "What is Double Quantization in QLoRA?" (Quantization produces scaling constants for every block of weights. Double Quantization quantizes those scaling constants themselves from 32-bit to 8-bit, saving an additional ~0.4 bits per parameter).

## 13. Related concepts
- **QLoRA**: Relies entirely on 4-bit quantization.
- **Inference Optimization**: Quantization is a pillar of fast serving.

## 14. When it breaks / Edge cases
- Sub-4-bit quantization (like 2-bit or 1-bit/Ternary models like BitNet) currently causes severe degradation in reasoning capabilities and requires specialized Quantization-Aware Training from scratch.

## 15. Comparison with alternative approaches
- **Quantization vs Pruning:** Pruning removes weights entirely (sets to zero). Quantization reduces the precision of all weights. Quantization currently yields much better performance retention for LLMs than unstructured pruning.

---
*Where this shows up in ML:*
Deploying models via llama.cpp (GGUF format), vLLM (AWQ/GPTQ formats), and QLoRA fine-tuning.
