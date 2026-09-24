# Agent Planning

## 1. Definition
Agent Planning refers to the prompting techniques and architectural structures that enable an LLM to break down a complex, high-level goal into a sequence of actionable subtasks before or during execution.

## 2. Intuition
If you ask someone to "organize a wedding," they don't immediately start buying cake. They make a master plan: venue, food, guest list. Agent planning forces the LLM to write out the master plan and reason about dependencies before taking action.

## 3. Why it exists
LLMs are autoregressive—they predict the next token. If they start taking action immediately without a plan, they often paint themselves into a corner. By forcing them to generate a plan first, we place the reasoning steps into the context window, which the model can then attend to during execution.

## 4. Mechanics
- **Chain of Thought (CoT):** "Let's think step by step." Forces sequential reasoning before the final answer.
- **ReAct (Reason + Act):** Interleaves planning and execution. The model thinks about the current state, acts, observes, and thinks again.
- **Plan-and-Solve (or Plan-and-Execute):** Two distinct phases. Phase 1: A Planner LLM generates a step-by-step list of subtasks. Phase 2: An Executor LLM runs each subtask sequentially, passing the results to the next step.
- **Tree of Thoughts (ToT):** Explores multiple reasoning paths simultaneously. Evaluates each path (using the LLM as a judge), abandons dead ends (backtracking), and expands the best paths.

## 5. Complexity (Time & Space)
- **Plan-and-Execute:** Cheaper than ReAct for long tasks because the executor only needs the current subtask context, not the entire history of reasoning.
- **Tree of Thoughts:** Extremely expensive (branching factor exponentially increases API calls).

## 6. Tiny worked example
Goal: "Compare the population of the capitals of France and Japan."
**Plan-and-Execute:**
*Planner:*
1. Find capital of France.
2. Find capital of Japan.
3. Find population of capital 1.
4. Find population of capital 2.
5. Compare populations.
*Executor runs step 1, passes result to step 3, etc.*

## 7. Code (Python)
```python
# Conceptual Plan-and-Execute
def plan_and_execute(goal, llm, executor):
    # Phase 1: Planning
    plan_prompt = f"Create a step-by-step plan to achieve: {goal}"
    plan = llm.generate(plan_prompt).split('\n')
    
    context = {}
    # Phase 2: Execution
    for step in plan:
        # Executor only sees the current step and accumulated context
        result = executor.run(step, context)
        context[f"Result of '{step}'"] = result
        
    return llm.generate(f"Given context {context}, answer goal: {goal}")
```

## 8. Common mistakes
- Using ReAct for tasks that require long-term planning. ReAct's context window fills up with tool observations, causing it to "forget" the original goal. Plan-and-Execute separates the plan from the execution noise.
- Providing too many tools to the planner. The planner only needs to know *what* can be done, not the exact API signatures (which the executor needs).

## 9. 30-second interview answer
"Agent Planning techniques force LLMs to decompose complex goals before acting. ReAct interleaves reasoning and acting, suitable for dynamic tasks. Plan-and-Execute separates the process: a Planner generates a sequence of subtasks, and an Executor completes them one by one. Tree of Thoughts is a more advanced technique that explores multiple reasoning paths and backtracks, used for highly complex logical problems."

## 10. 2-minute interview answer
"Because LLMs lack an internal workspace and generate text autoregressively, they struggle with complex tasks if forced to output an answer immediately. Planning techniques solve this by externalizing reasoning into the context window. The baseline is Chain of Thought, which improves reasoning but doesn't allow interaction with the environment. ReAct solves this by creating a Thought-Action-Observation loop, allowing the agent to adapt its plan based on tool outputs. However, ReAct suffers in long tasks because the context window gets bloated with tool outputs, leading to goal-forgetting. The industry has largely moved to the Plan-and-Execute pattern for complex tasks: a 'Planner' LLM generates a strict DAG of subtasks, and an 'Executor' agent handles them sequentially. This is highly efficient and modular. For tasks requiring deep search, like math proofs or creative writing, Tree of Thoughts allows the model to explore multiple branches, score them, and backtrack, effectively performing heuristic search over language generation."

## 11. Follow-ups
- "What is Reflection in agent planning?" (After a task is completed, or if it fails, prompting the LLM to review the outcome, identify mistakes, and generate an updated plan for the next attempt. Crucial for self-correction).

## 12. Deeper questions
- "How does the Executor in Plan-and-Execute handle dependencies between steps?" (The Planner must explicitly state dependencies, and a state manager passes the output of Step 1 as context into the prompt for Step 2).

## 13. Related concepts
- **Agents**: Planning is their core cognitive component.
- **Chain of Thought**: The foundational prompting technique for planning.

## 14. When it breaks / Edge cases
- In Plan-and-Execute, if the environment changes or a tool fails unpredictably during execution, the static plan breaks. A "Replanner" node is often needed to update the plan mid-execution.

## 15. Comparison with alternative approaches
- **ReAct vs Plan-and-Execute:** ReAct is dynamic but gets confused on long tasks. Plan-and-Execute is rigid but handles long tasks well by isolating context.

---
*Where this shows up in ML:*
AutoGPT architectures, advanced prompt engineering, solving complex SWE-bench tasks.
