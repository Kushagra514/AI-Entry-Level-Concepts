# Agents vs Workflows

## 1. Definition
This represents the architectural decision between granting an LLM autonomy to determine its own execution path (Agents) versus constraining the LLM within a hardcoded, deterministic graph of operations (Workflows).

## 2. Intuition
- **Agent:** You tell a chef, "Make me a great dinner." They decide the menu, buy the ingredients, and cook it however they want.
- **Workflow:** You give a cook a recipe. "Chop onions (tool). If brown (LLM check), add tomatoes (tool). Wait 10 mins (code)."

## 3. Why it exists
Early hype (AutoGPT) assumed autonomous agents would solve everything. Reality showed they get stuck in loops, hallucinate tool calls, and fail at complex tasks. Workflows emerged as the pragmatic, production-ready alternative for enterprise applications.

## 4. Mechanics
- **Agents (Dynamic Control Flow):** LLM uses a `while loop`. It loops (Thought -> Action -> Observation) until it decides to output a `Final Answer`. The path is completely unpredictable.
- **Workflows (Static Control Flow):** Developer uses a Directed Acyclic Graph (DAG). Node A always goes to Node B or Node C based on predefined rules. The LLM only executes specific cognitive tasks inside the nodes.

## 5. Complexity (Time & Space)
- **Agents:** Unbounded execution time. High token usage due to long reasoning traces.
- **Workflows:** Bounded execution time. Predictable token usage.

## 6. Tiny worked example
Task: Write a blog post from a URL.
**Agent approach:** 
Prompt: "Write a blog post based on this URL." 
*Agent might search the web, get distracted, write a python script to scrape, fail, try again.*
**Workflow approach:**
Node 1 (Code): Scrape URL. 
Node 2 (LLM): Extract key bullet points. 
Node 3 (LLM): Draft post from bullets. 
*Reliable, fast, predictable.*

## 7. Code (Python)
```python
# Agent: The control flow is inside the LLM's brain
while True:
    response = llm(prompt + history)
    if is_final(response): break
    execute_tool(response)

# Workflow: The control flow is in Python (LangGraph style)
def process():
    data = scrape_tool(url)                # Deterministic
    summary = summarize_llm(data)          # Cognitive
    draft = draft_llm(summary)             # Cognitive
    return draft
```

## 8. Common mistakes
- Reaching for an Agent architecture when a Workflow is sufficient. If you can draw a flowchart of how the task *should* be done, you should build a workflow.
- Assuming workflows are purely linear. Workflows can have loops (e.g., a reflection loop where a reviewer sends a draft back to a writer), but the *path* of the loop is hardcoded.

## 9. 30-second interview answer
"The core difference is control flow. In an Agent, the LLM dynamically decides the sequence of actions, loops, and when to terminate. In a Workflow, the developer hardcodes the control flow as a graph or state machine, using the LLM only for specific cognitive tasks within the nodes. Workflows prioritize reliability and debuggability, while Agents prioritize flexibility in open-ended environments."

## 10. 2-minute interview answer
"In production AI systems, the choice between Agents and Workflows is the most critical architectural decision. Autonomous agents use frameworks like ReAct to decide their own control flow. While highly capable in unpredictable environments, they suffer from compounding errors: one hallucinated tool call can derail the entire loop, leading to infinite loops or failure. They are a nightmare to debug because the execution path is non-deterministic. Workflows address this by keeping the control flow in Python or frameworks like LangGraph. The developer defines a state machine. The LLM acts as a specific component—a router, a summarizer, or an evaluator—rather than the CEO. This ensures predictable execution, easy insertion of human-in-the-loop approval gates, and targeted error handling. The industry consensus is to use Workflows for 95% of enterprise tasks, and only use Agents for open-ended exploration tasks where the sequence of steps genuinely cannot be known in advance."

## 11. Follow-ups
- "When would you absolutely need an Agent instead of a Workflow?" (For tasks like autonomous penetration testing or open-ended web research, where the next action depends entirely on the unpredictable result of the previous action).

## 12. Deeper questions
- "How do you test an Agent vs a Workflow?" (Workflows can be unit-tested per node: mock the inputs, test the LLM output. Agents require integration testing in simulated environments to see if they achieve the final goal, which is much harder).

## 13. Related concepts
- **ReAct**: The pattern used by Agents.
- **State Machines**: The pattern used by Workflows.

## 14. When it breaks / Edge cases
- Workflows break when the real-world input doesn't fit any of the predefined paths in the DAG. Agents break by hallucinating entirely new, wrong paths.

## 15. Comparison with alternative approaches
- N/A — This is the primary dichotomy in LLM orchestration.

---
*Where this shows up in ML:*
System design interviews for AI applications; choosing between LangChain Agents vs LangGraph.
