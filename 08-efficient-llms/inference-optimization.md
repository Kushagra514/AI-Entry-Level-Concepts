# LLM Inference Optimization

## 1. Definition
LLM Inference Optimization encompasses hardware-aware algorithms and systems engineering techniques designed to maximize generation throughput (tokens/second) and minimize latency (Time To First Byte) during autoregressive text generation.

## 2. Intuition
Generating text with a 70B model is like moving a mountain of data for a spoonful of math. Every time you generate a single word, you have to read 140GB of weights from the GPU memory into the processor. To make this fast, we need to minimize memory movement, batch requests smartly, and cache everything we can.

## 3. Why it exists
LLM inference is fundamentally **Memory-Bandwidth Bound**, not Compute-Bound. The math (matrix-vector multiplication) is fast, but waiting for the weights to travel from HBM (High Bandwidth Memory) to SRAM takes forever. Optimization techniques tackle this bottleneck.

## 4. Mechanics
- **KV-Cache:** Stores the Key and Value vectors of past tokens to prevent $O(N^2)$ recomputation.
- **Continuous Batching (In-flight Batching):** Traditional batching waits for the longest sentence to finish before starting a new batch. Continuous batching ejects finished requests and inserts new ones at the token level, vastly increasing throughput.
- **PagedAttention (vLLM):** KV-cache grows unpredictably. Traditional allocators pre-allocate max memory, wasting 60-80% to fragmentation. PagedAttention divides KV-cache into blocks (like OS virtual memory), allowing non-contiguous storage and near-zero waste, allowing much larger batch sizes.
- **FlashAttention:** Fuses the QKV attention operations in SRAM to avoid reading/writing the $N \times N$ attention matrix to slow HBM.
- **Speculative Decoding:** A small 1B draft model generates 4 tokens quickly. The large 70B model verifies all 4 tokens in a single forward pass. Speeds up latency 2-3x without changing the output distribution.

## 5. Complexity (Time & Space)
- Optimization targets the constant factors of memory IO and batch utilization, yielding 10x to 24x throughput improvements in production systems (e.g., vLLM vs naive HuggingFace).

## 6. Tiny worked example
*Traditional Batching:* Req A (3 tokens), Req B (6 tokens). Req A finishes in 3 steps, GPU idles that slot for 3 more steps waiting for B.
*Continuous Batching:* Req A finishes. Step 4 instantly slots in Req C. 100% GPU utilization.

## 7. Code (Python)
```python
# Utilizing optimized inference engines rather than native PyTorch
from vllm import LLM, SamplingParams

# vLLM automatically handles PagedAttention, Continuous Batching, 
# and FlashAttention under the hood.
llm = LLM(model="meta-llama/Llama-2-7b-chat-hf")
prompts = ["Hello, my name is", "The president of the US is"]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

# This executes with massive throughput compared to HuggingFace .generate()
outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print(output.outputs[0].text)
```

## 8. Common mistakes
- Benchmarking LLMs using `batch_size=1`. LLM throughput scales massively with batch size up to the VRAM limit because loading the weights once can serve 100 requests simultaneously.
- Using native `transformers` `model.generate()` in production. It lacks continuous batching and PagedAttention. Use vLLM, TensorRT-LLM, or TGI.

## 9. 30-second interview answer
"LLM autoregressive generation is memory-bandwidth bound. To optimize it, we use the KV-Cache to avoid recomputation, FlashAttention to avoid HBM read/writes during attention, and Continuous Batching to maximize GPU utilization. Most importantly, systems like vLLM use PagedAttention to manage the KV-cache in non-contiguous blocks, eliminating memory fragmentation and allowing much larger batch sizes, increasing throughput by up to 24x."

## 10. 2-minute interview answer
"Optimizing LLM inference requires shifting focus from FLOPs to memory bandwidth. Because autoregressive generation requires loading the entire model weights from HBM to SRAM for every single generated token, the GPU's compute cores sit idle waiting for data. We optimize this at three levels. First, algorithmically: the KV-cache saves past Key/Value states so we only compute attention for the new token. Second, at the kernel level: FlashAttention fuses the attention calculation in SRAM, preventing the $O(N^2)$ intermediate matrix from ever touching slow memory. Third, at the systems level: engines like vLLM use Continuous Batching to slot new requests in at the token level, and PagedAttention to manage KV-cache memory like OS virtual memory. Before PagedAttention, unpredictable sequence lengths caused massive memory fragmentation, limiting batch sizes. By allocating non-contiguous blocks, vLLM maximizes batch size, which means loading the model weights once serves many more requests, drastically increasing tokens-per-second throughput. For latency-sensitive applications, we add Speculative Decoding, using a tiny draft model to guess tokens and the large model to verify them in parallel."

## 11. Follow-ups
- "What is Tensor Parallelism?" (Splitting the weight matrices of a single model across multiple GPUs. Necessary when a model (like 70B) doesn't fit on one GPU. Communication happens via All-Reduce operations across NVLink).

## 12. Deeper questions
- "How does Speculative Decoding guarantee the exact same output distribution as the target model?" (By using a specific rejection sampling scheme. If the target model's probability for the draft token is higher than the draft model's, it's accepted. If lower, it's accepted with probability $p_{target}/p_{draft}$, otherwise rejected and resampled from the target distribution).

## 13. Related concepts
- **Quantization**: Reduces weight size, directly tackling the memory-bandwidth bottleneck.
- **Autoregressive Generation**: The process being optimized.

## 14. When it breaks / Edge cases
- Very long context lengths (e.g., 100k) cause the KV-cache size to exceed the model weight size, shifting the bottleneck and requiring techniques like Ring Attention (distributing context across GPUs).

## 15. Comparison with alternative approaches
- N/A — these are compounding optimizations, typically all used together in modern serving engines.

---
*Where this shows up in ML:*
MLOps, deploying models using vLLM, TGI, or TensorRT-LLM.
