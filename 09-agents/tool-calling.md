# Tool Calling in LLMs

## 1. Definition
Tool calling (or function calling) is the capability of an LLM to recognize when it needs external information or actions, select the appropriate tool from a provided schema, and format a structured request. The LLM pauses generation while the host application executes the tool and returns the result, after which the LLM resumes generation.

## 2. Intuition
An LLM is a brain in a jar. It knows a lot, but it can't check today's weather, evaluate complex math, or send an email. Tool calling provides the brain with a remote control. You give the LLM a manual of buttons it can press (the tool schema). When it needs to, it presses a button (outputs JSON), waits for you to read the result back to it, and then continues talking.

## 3. Why It Exists
LLMs suffer from fundamental limitations: knowledge cutoffs, hallucination on arithmetic/logic, and an inability to affect the external world. Tool calling bridges this gap, allowing deterministic code to handle what LLMs are bad at (math, live data, APIs), while the LLM handles what it is good at (reasoning, routing, natural language).

## 4. Core Mechanics
It is critical to understand that **the LLM does not execute code**.
1. **Definition:** The developer defines a set of tools using JSON schema (name, description, expected parameters).
2. **Prompting:** The application injects these schemas into the LLM's system prompt.
3. **Generation:** The LLM evaluates the user prompt. If a tool is needed, it generates a special stop token and outputs the JSON arguments.
4. **Execution:** The *application* intercepts this response, parses the JSON, executes the actual Python/Node function, and captures the return value.
5. **Observation:** The application appends the return value to the conversation history as a `ToolMessage` and triggers the LLM again.
6. **Synthesis:** The LLM reads the tool output and synthesizes the final natural language answer.

## 5. Mathematical View
Not applicable for this architectural pattern.

## 6. Shape / Dimension Tracking
Not applicable for this architectural pattern.

## 7. Tiny Worked Example
User: "What's the weather in Tokyo?"
LLM knows it has `get_weather(location: string)`.
LLM outputs: `{"name": "get_weather", "arguments": {"location": "Tokyo"}}`
*(LLM generation halts)*
App parses JSON, calls its local `weather_api("Tokyo")`, gets `"22°C, Sunny"`.
App sends new message to LLM: `Role: Tool, Content: "22°C, Sunny"`
LLM outputs: "It is currently 22°C and sunny in Tokyo."

## 8. Minimal Implementation
```python
# Conceptual flow
def run_agent(user_query: str, tools: list, llm):
    messages = [{"role": "user", "content": user_query}]
    
    # First LLM call
    response = llm.generate(messages, tools=tools)
    
    if response.tool_calls:
        for call in response.tool_calls:
            # 1. Parse LLM intent
            func_name = call.name
            args = json.loads(call.arguments)
            
            # 2. Application executes the tool
            result = execute_local_function(func_name, args)
            
            # 3. Append observation
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })
            
        # 4. Second LLM call to synthesize
        final_response = llm.generate(messages, tools=tools)
        return final_response
    else:
        return response.content
```

## 9. Common Misconceptions
- **"The LLM runs the Python code."** No. The LLM only generates a string of text formatted as JSON. The host server parses that string and executes the code.
- **"Tool calling is a prompt engineering trick."** While early models relied on prompt engineering to output JSON, modern models are explicitly fine-tuned (Instruction Tuned) on datasets containing tool-use trajectories to natively understand when and how to output specific tool-call tokens.

## 10. 30-Second Interview Answer
"Tool calling allows an LLM to interact with external systems. Models are fine-tuned to recognize when a query requires external data, select the appropriate tool from a provided JSON schema, and generate the correct arguments. Crucially, the model pauses while the host application executes the tool. The application then feeds the result back as an observation, allowing the LLM to synthesize the final response."

## 11. 2-Minute Interview Answer
"Tool calling transforms an LLM from a static text generator into an active agent. Foundation models are specifically fine-tuned on tool-use datasets to reliably output structured payloads. In practice, you pass a JSON schema defining available functions to the model. When the model encounters a prompt requiring a tool, it outputs a structured JSON payload and halts. The application layer must intercept this, execute the corresponding code—whether that's a SQL query, a web search, or a Python REPL—and return the output as a 'Tool Observation'. The model then resumes generation, incorporating the fresh data. This design pattern solves the LLM's fundamental flaws: knowledge cutoffs are solved by web search tools, math hallucinations are solved by calculator tools, and the inability to take action is solved by API tools. The main engineering challenges are handling hallucinated arguments and ensuring the LLM gracefully recovers if the tool execution fails."

## 12. Follow-Up Questions
- **"How does the LLM know which tool to use?"**
  It relies heavily on the `description` fields provided in the JSON schema. "Fetches user data" is a bad description; "Fetches user ID and email given a username" is a good description.
- **"What happens if the LLM outputs malformed JSON?"**
  The application parsing step will throw an error. A robust system will catch this error, pass the error message back to the LLM as a ToolMessage, and ask it to fix its formatting.

## 13. Deeper Questions
- **"What are the security implications of Tool Calling?"**
  If a tool executes code (like a Python REPL) or modifies a database, a malicious user can use Prompt Injection to trick the LLM into generating a destructive tool call (e.g., `drop_table()`). Tools must be strictly sandboxed and adhere to the Principle of Least Privilege.

## 14. Failure Modes / Edge Cases
- **Context Overflow:** If a tool (like `search_web`) returns a massive payload, it can exceed the LLM's context window. The application must truncate, summarize, or RAG the tool output before feeding it back.
- **Infinite Loops:** An LLM might repeatedly call a failing tool with the same arguments if it gets stuck in a reasoning loop.

## 15. Comparison
- **Tool Calling vs Pure Prompting:** Tool calling offloads deterministic tasks (math, search) to code. Pure prompting forces the LLM to guess the answer using its weights, which is error-prone for precise tasks.

## 16. What To Remember
- The LLM outputs text/JSON; the Application runs the code.
- Tool calling requires multiple round-trips to the LLM API.
- It requires models explicitly fine-tuned for this capability.
- Schemas and descriptions are the interface.

## 17. Interview Trap
> **Q:** "If we give the LLM a `delete_user` tool, how does the LLM securely connect to the database to run the deletion?"
> **A:** The LLM does not connect to the database. The LLM only outputs a string like `{"function": "delete_user", "id": 123}`. Your backend application receives this string, authenticates the request, and your backend executes the actual SQL query.

---
*Connected Concepts:* [Agents](agents.md), [RAG](../07-rag/rag-overview.md)
