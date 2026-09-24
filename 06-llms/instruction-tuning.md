# Instruction Tuning

## 1. Definition
Instruction tuning is a specialized form of Supervised Fine-Tuning (SFT) where a pretrained language model is trained on datasets consisting of (Instruction, Response) pairs, teaching it to act as an assistant rather than just a text completer.

## 2. Intuition
A base model acts like a parrot that finishes your sentences. If you say "Translate to French: Hello", a base model might reply "Translate to Spanish: Hola". Instruction tuning teaches it that "Translate to French" is a command to be executed, resulting in "Bonjour".

## 3. Why it exists
Base models are difficult for end-users to interact with because they require complex "prompt engineering" to trick the model into completing the text in a useful way. Instruction tuning aligns the model's behavior with human expectations of an AI assistant.

## 4. Mechanics
- **Dataset format:** Usually structured with roles. E.g., User: "Write a poem." Assistant: "Roses are red..."
- **Chat Templates:** Special control tokens are introduced to format the conversation (e.g., `<|im_start|>user\n...<|im_end|>`).
- **Loss Masking:** During training, cross-entropy loss is calculated *only* on the tokens belonging to the Assistant's response. The User instruction tokens are ignored in the loss calculation.
- **FLAN (Fine-tuned LAnguage Net):** Google's early approach of taking thousands of traditional NLP datasets and converting them into instruction templates.

## 5. Complexity (Time & Space)
- Same as Supervised Fine-Tuning. Requires significantly less compute than pretraining (often just hours/days on a small cluster).

## 6. Tiny worked example
Raw Training Data:
`Instruction: Summarize this text: [TEXT]. Response: [SUMMARY]`

Using a Chat Template for Llama-3:
`<|start_header_id|>user<|end_header_id|>\nSummarize...<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n[SUMMARY]<|eot_id|>`

## 7. Code (Python)
```python
# Conceptual loss masking for instruction tuning
def compute_loss(model, input_ids, labels):
    # input_ids: [User_Token1, User_Token2, Asst_Token1, Asst_Token2]
    # labels:    [-100,       -100,        Asst_Token1, Asst_Token2]
    # PyTorch ignores index -100 in CrossEntropyLoss
    
    outputs = model(input_ids)
    logits = outputs.logits[:, :-1, :] # Shift for next token
    targets = labels[:, 1:]
    
    loss_fct = torch.nn.CrossEntropyLoss(ignore_index=-100)
    loss = loss_fct(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
    return loss
```

## 8. Common mistakes
- Training the model to predict the prompt. If you don't mask the prompt tokens with `-100`, the model learns to generate user questions, which wastes capacity and can cause weird generation artifacts.
- Mixing chat templates. If you fine-tune a model using the ChatML template, but inference uses the Llama-3 template, performance will degrade severely.

## 9. 30-second interview answer
"Instruction tuning is a stage of Supervised Fine-Tuning where a base model is trained on instruction-response pairs. It transforms a model from a generic text completer into an assistant that follows commands. Special chat template tokens are used to separate roles, and loss is only calculated on the assistant's response."

## 10. 2-minute interview answer
"Instruction tuning bridges the gap between next-token prediction and useful AI interaction. We take a pretrained base model and fine-tune it on tens of thousands of high-quality conversational turns. A critical implementation detail is the chat template: we wrap the user and assistant text in special control tokens (like `<|user|>` and `<|assistant|>`). This allows the model to differentiate between instructions it must follow and text it is generating. During the backward pass, we apply loss masking: the cross-entropy loss is computed only on the assistant's response tokens. Recent research, like the LIMA paper (Less Is More for Alignment), shows that instruction tuning doesn't inject new knowledge; rather, it just unlocks the knowledge already learned during pretraining, meaning 1,000 highly-curated examples often outperform 100,000 mediocre ones."

## 11. Follow-ups
- "What happens after instruction tuning?" (Usually RLHF or DPO to align the model further with human preferences, reduce toxicity, and improve helpfulness).

## 12. Deeper questions
- "How do you generate high-quality instruction tuning data without human annotators?" (Self-Instruct pipelines: use a powerful model like GPT-4 to generate complex instructions and responses, then train a smaller model on that synthetic data. This is how Alpaca and many open-source models were created).

## 13. Related concepts
- **RLHF**: The alignment step that usually follows instruction tuning.
- **System Prompts**: Enabled by the chat templates learned during instruction tuning.

## 14. When it breaks / Edge cases
- "Sycophancy" - instruction-tuned models tend to agree with the user's premise even when it is factually incorrect, because human annotators tend to rate polite, agreeable responses highly.

## 15. Comparison with alternative approaches
- **Instruction Tuning vs Few-Shot Prompting:** Few-shot works on base models but requires context space. Instruction-tuned models have zero-shot capability for commands.

---
*Where this shows up in ML:*
The difference between `Llama-3-8B` (base) and `Llama-3-8B-Instruct`.
