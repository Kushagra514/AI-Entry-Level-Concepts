# Agent Memory

## 1. Definition
Agent Memory refers to the mechanisms by which an LLM retains and accesses information across a conversation, session, or lifetime, overcoming its inherently stateless nature.

## 2. Intuition
An LLM is like an amnesiac with a photographic memory. Every time you talk to it, it forgets everything that happened before (stateless). To give it "memory," you must remind it of everything that previously happened by pasting the transcript into its prompt (context window).

## 3. Why it exists
Meaningful AI assistants must remember user preferences, past interactions, and long-term project contexts. Because the context window is limited and expensive, we need systems to manage what information is kept in context, what is summarized, and what is stored externally.

## 4. Mechanics
- **Short-Term Memory (Context Window):** The raw transcript of the current session appended to the prompt.
- **Window Buffer:** Keeps only the last $N$ messages to prevent context overflow.
- **Summary Memory:** An LLM periodically reads the older conversation and generates a condensed summary to keep in the prompt, discarding the raw messages.
- **Long-Term / Episodic Memory (Vector DB):** Past conversations and facts are embedded and stored in a vector database. When the user asks a question, the agent performs RAG over its own past memories to retrieve relevant context.
- **Semantic/Entity Memory:** A structured knowledge graph or key-value store (e.g., extracting "User likes Python", "User lives in NY") updated dynamically by the agent.

## 5. Complexity (Time & Space)
- **Context Window:** Cost scales quadratically ($O(N^2)$) as memory grows.
- **Vector DB:** Cheap and scalable, but introduces retrieval latency.

## 6. Tiny worked example
User: "My dog is named Max."
Agent: Extract entity -> `{user_dog: Max}`. Save to DB.
(1 month later)
User: "What should I buy for my pet?"
Agent: Retrieves from DB -> `user_dog = Max`.
Agent replies: "You should buy some dog treats for Max!"

## 7. Code (Python)
```python
# Conceptual Summary Memory
def manage_memory(history_list, llm, max_tokens=1000):
    current_tokens = count_tokens(history_list)
    
    if current_tokens > max_tokens:
        # Separate the oldest messages
        old_messages = history_list[:-5]
        recent_messages = history_list[-5:]
        
        # Summarize the old messages
        summary = llm.generate(f"Summarize this conversation: {old_messages}")
        
        # New history is the summary + recent messages
        return [f"Previous context: {summary}"] + recent_messages
        
    return history_list
```

## 8. Common mistakes
- Dumping the entire conversation history into the prompt without a buffer. The app will suddenly crash with a "Context Length Exceeded" API error, or become incredibly slow and expensive.
- Using Vector DBs for *conversational flow*. If the user says "Yes, do that," retrieving the word "Yes" from a vector DB is useless without the immediately preceding turn. Vector DBs are for *facts*, Window buffers are for *flow*.

## 9. 30-second interview answer
"LLMs are stateless, so memory must be managed externally. Short-term memory is handled by passing recent conversation history in the context window. To prevent overflow, we use sliding windows or LLM-generated summaries of older turns. Long-term memory is implemented by storing extracted facts or past conversations in a vector database, allowing the agent to retrieve them via RAG when relevant."

## 10. 2-minute interview answer
"Agent memory bridges the gap between a stateless inference API and a persistent AI companion. We divide memory into short-term, long-term, and entity memory. Short-term memory manages the immediate context window. Because attention is $O(N^2)$, we cannot grow this infinitely. We use techniques like ConversationSummaryBuffer, which keeps the last few raw messages for immediate flow, and uses an LLM background task to compress older messages into a rolling summary. Long-term episodic memory treats the agent's past experiences as a corpus for RAG; conversations are chunked, embedded, and stored in a vector database. Entity memory is more structured: we prompt the LLM to extract specific user facts (e.g., 'User is allergic to peanuts') and store them in a key-value store or knowledge graph. When a new prompt comes in, the agent injects the rolling summary, retrieves relevant episodic chunks from the vector DB, and injects relevant structured entities, synthesizing a fully contextualized response."

## 11. Follow-ups
- "What is a Knowledge Graph and why use it for memory?" (It stores information as triples (Node-Edge-Node, e.g., User -> owns -> Dog). It allows for exact logical queries and multi-hop reasoning, which vector databases struggle with).

## 12. Deeper questions
- "How do you handle memory contradictory updates?" (If user says "I moved to SF" but old memory says "lives in NY", the memory system must update, not just append. We usually use a specific 'Memory Manager' LLM prompt whose job is strictly to consolidate and update the user's profile JSON).

## 13. Related concepts
- **Context Window**: The physical limit of short-term memory.
- **RAG**: The implementation of long-term memory.

## 14. When it breaks / Edge cases
- Summarization loss: If a user mentions a critical 6-digit reference number early on, the summary model might drop it as "unimportant details," destroying the memory.

## 15. Comparison with alternative approaches
- **Continuous Pretraining vs RAG Memory:** You cannot fine-tune a model continuously on user chats to memorize them (catastrophic forgetting, too expensive). RAG memory is the only viable approach.

---
*Where this shows up in ML:*
Building stateful chatbots (ChatGPT's "Memory" feature), Mem0 library.
