# Fine-Tuning LLMs

## 1. Definition
Fine-tuning is the process of taking a pretrained foundation model and training it further on a smaller, task-specific dataset to adapt its behavior, format, or domain knowledge.

## 2. Intuition
Pretraining teaches the model "how to speak English and understand the world" (getting a college degree). Fine-tuning teaches it "how to be a polite customer service agent" (on-the-job training).

## 3. Why it exists
Pretrained models only want to complete text (e.g., if you prompt "What is the capital of France?", it might output "What is the capital of Germany?"). Fine-tuning aligns the model to follow instructions, answer questions, or perform specific formatting (like outputting valid JSON).

## 4. Mechanics
- **Full Fine-Tuning:** Update all parameters of the model. Requires massive GPU memory (e.g., 8x A100s for a 7B model) to store optimizer states for all weights.
- **PEFT (Parameter-Efficient Fine-Tuning):** Freeze the base model and train a small number of extra parameters.
  - **LoRA (Low-Rank Adaptation):** Injects trainable low-rank matrices into the attention layers.
  - **QLoRA:** Quantizes the base model to 4-bit, training LoRA adapters on top (fits a 7B model on a single 24GB consumer GPU).
- **Dataset:** Usually Supervised Fine-Tuning (SFT) format: `{"prompt": "...", "response": "..."}`. High quality > high quantity (1,000 great examples beats 100,000 mediocre ones).

## 5. Complexity (Time & Space)
- **Full FT Space:** 4-6x the model parameters (Model + Gradients + Adam states).
- **LoRA Space:** ~1x model parameters (frozen) + tiny optimizer state for adapters.

## 6. Tiny worked example
Goal: Make model output JSON.
Dataset: 
`[{"instruction": "Extract names", "input": "Bob and Alice", "output": "{\"names\": [\"Bob\", \"Alice\"]}"}]`
Train with CLM loss only on the `output` portion (masking the prompt from the loss).

## 7. Code (Python)
```python
# Using HuggingFace PEFT (LoRA)
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b")

# Configure LoRA: rank 8, target attention projection layers
config = LoraConfig(
    r=8, 
    lora_alpha=32, 
    target_modules=["q_proj", "v_proj"], 
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Wraps model: freezes base weights, adds trainable LoRA weights
peft_model = get_peft_model(model, config)
peft_model.print_trainable_parameters() 
# "trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%"
```

## 8. Common mistakes
- Training on the prompt. Loss should only be calculated on the model's *response*, not the user's instruction.
- Using fine-tuning to inject new factual knowledge. Fine-tuning is prone to catastrophic forgetting and hallucinations. RAG is better for facts; fine-tuning is for *behavior/style*.

## 9. 30-second interview answer
"Fine-tuning adapts a pretrained model to specific tasks. Full fine-tuning updates all weights but is highly resource-intensive. Parameter-Efficient Fine-Tuning (PEFT) methods like LoRA freeze the base model and train small adapter layers, allowing fine-tuning on consumer hardware. We use fine-tuning to teach the model how to behave (e.g., instruction following) rather than to teach it new facts."

## 10. 2-minute interview answer
"Fine-tuning bridges the gap between a raw predictive model and a useful application. While full fine-tuning updates the entire parameter space, it requires extensive VRAM for optimizer states. Therefore, the industry standard for custom adaptation is LoRA (Low-Rank Adaptation). LoRA freezes the pretrained weights and injects trainable rank-decomposition matrices into each layer. This reduces trainable parameters by 99% while achieving near-parity with full fine-tuning. The most critical aspect of fine-tuning is data quality; a few thousand highly curated examples (LIMA paper) can outperform millions of low-quality examples. We generally follow the rule: use RAG to give the model new knowledge, and use fine-tuning to teach the model a new format, tone, or specific reasoning pattern."

## 11. Follow-ups
- "What is catastrophic forgetting?" (When fine-tuning on a narrow dataset, the model's weights change and it forgets the broad general knowledge it learned during pretraining. LoRA helps mitigate this).

## 12. Deeper questions
- "How does QLoRA work?" (It loads the base model in 4-bit NormalFloat precision. During the backward pass, activations are dequantized to 16-bit to compute gradients for the 16-bit LoRA adapters. This drastically reduces memory footprint).

## 13. Related concepts
- **Instruction Tuning**: A specific type of supervised fine-tuning.
- **RAG**: The alternative/complement to fine-tuning for knowledge injection.

## 14. When it breaks / Edge cases
- Overfitting occurs very quickly on small fine-tuning datasets, causing the model to lose its conversational abilities.

## 15. Comparison with alternative approaches
- **Fine-Tuning vs Prompt Engineering (Few-Shot):** Few-shot is fast and requires no training, but consumes context window. Fine-tuning bakes the behavior in, saving tokens and handling more complex pattern matching.

---
*Where this shows up in ML:*
Adapting Llama-3 or Mistral for specific enterprise use-cases (code generation, medical Q&A, JSON extraction).
