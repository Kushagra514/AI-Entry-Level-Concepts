# LLM Workflows

## 1. Definition
LLM Workflows are orchestrated sequences of LLM calls, deterministic code, and external tool executions linked together in a predefined Directed Acyclic Graph (DAG) or state machine to accomplish a complex task reliably.

## 2. Intuition
Instead of asking one smart person to build a car from scratch (an Agent), a workflow is an assembly line. One LLM extracts requirements, the next writes a draft, deterministic code compiles it, and a final LLM reviews it. The path is fixed and predictable.

## 3. Why it exists
Autonomous agents (where the LLM decides every step) are highly unreliable, prone to infinite loops, and difficult to debug. Workflows constrain the LLM, using it only for specific cognitive tasks within a robust software engineering framework, vastly increasing reliability for production systems.

## 4. Mechanics
- **Chains:** Sequential execution (Prompt 1 -> LLM 1 -> Prompt 2 -> LLM 2).
- **Routing:** Use a fast LLM or classifier to decide which sub-workflow to execute.
- **Parallelization:** Run multiple LLM calls simultaneously (e.g., summarizing 5 documents at once) and then aggregate.
- **Human-in-the-loop (HITL):** Pause the workflow at critical nodes for human approval before proceeding.
- **Frameworks:** LangChain, LangGraph, LlamaIndex, Apache Airflow.

## 5. Complexity (Time & Space)
- Time is deterministic based on the depth of the DAG. Avoids the unbounded execution time of autonomous agents.

## 6. Tiny worked example
Customer Support Workflow:
1. LLM 1 (Router): Classify email as "Refund" or "Tech Support". -> "Tech Support".
2. Code: Fetch user device info from DB.
3. LLM 2 (Solver): Given email + device info, write solution.
4. LLM 3 (Reviewer): Check if solution is polite. If not, rewrite.

## 7. Code (Python)
```python
# Conceptual Workflow using LangGraph State Graph
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    draft: str
    feedback: str

def writer_node(state):
    return {"draft": llm.invoke("Write a draft...")}

def reviewer_node(state):
    return {"feedback": llm.invoke(f"Review this: {state['draft']}")}

workflow = StateGraph(State)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_edge("writer", "reviewer")
workflow.add_edge("reviewer", END)
app = workflow.compile()
```

## 8. Common mistakes
- Using an autonomous Agent for a process that should be a Workflow. If the steps to solve a problem are known in advance, hardcode the steps (Workflow). Only use an Agent if the steps are unknown and must be discovered dynamically.
- Not implementing retries and fallbacks for individual LLM nodes.

## 9. 30-second interview answer
"LLM Workflows orchestrate multiple LLM calls and code execution in a predefined graph or state machine. Unlike autonomous agents that decide their own path, workflows constrain the LLM to specific tasks within a structured pipeline (like routing, drafting, and reviewing). This significantly increases reliability, determinism, and debuggability in production applications."

## 10. 2-minute interview answer
"In the transition from prototypes to production, the industry is moving from autonomous agents to structured LLM workflows. An autonomous agent uses an LLM to plan, select tools, and decide when to finish, which frequently leads to compounding errors, hallucinations, and infinite loops. Workflows, implemented via libraries like LangGraph, treat LLMs as functional components within a Directed Acyclic Graph (DAG). You might have a router node that classifies a query, a retrieval node that fetches data, a generator node that drafts an answer, and a critic node that evaluates the answer. The control flow is hardcoded in Python; the LLM only provides the 'reasoning engine' for specific nodes. This architecture allows for easy debugging (you know exactly which node failed), parallelization, and the insertion of human-in-the-loop approval gates. Workflows trade the theoretical flexibility of AGI-like agents for the reliability required in enterprise software."

## 11. Follow-ups
- "What is the reflection pattern in a workflow?" (Having a generation node pass its output to a critic node, which generates feedback. If the feedback is negative, the graph loops back to the generator to try again, up to a max retry limit).

## 12. Deeper questions
- "How do state machines (like LangGraph) differ from simple chains (like basic LangChain)?" (State machines allow cycles/loops for things like reflection or iterative refinement, and maintain a typed state object that is passed and mutated across nodes, rather than just a linear string passing).

## 13. Related concepts
- **Agents**: The autonomous alternative to workflows.
- **RAG**: A simple workflow (Retrieve -> Generate).

## 14. When it breaks / Edge cases
- Error handling in a complex DAG can be difficult if an early node hallucinates a badly formatted output that crashes a downstream deterministic Python function.

## 15. Comparison with alternative approaches
- **Workflows vs Agents:** Workflows = predefined path, high reliability, low flexibility. Agents = dynamic path, low reliability, high flexibility.

---
*Where this shows up in ML:*
Production LLM applications; replacing early AutoGPT experiments with LangGraph pipelines.
