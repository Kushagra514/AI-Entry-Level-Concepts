# Tool Calling in LLMs

## 1. Definition
Tool calling (or function calling) is the capability of an LLM to recognize when it needs external information or actions, format a request matching a predefined JSON schema, and pause generation to wait for the external system to execute the tool and return the result.

## 2. Intuition
An LLM is a brain in a jar. It knows a lot, but it can't check today's weather or send an email. Tool calling gives the brain hands and eyes. You provide the LLM with a list of "tools" (functions it can use), and it decides when to use them.

## 3. Why it exists
LLMs suffer from knowledge cutoffs, hallucination on math/logic, and inability to interact with the real world. Tool calling bridges this gap, allowing models to query live databases, execute Python code for math, or trigger APIs.

## 4. Mechanics
1. **Definition:** Developer defines tools using JSON schema (name, description, parameters).
2. **Prompting:** The tools are injected into the LLM's system prompt in a specific syntax.
3. **Generation:** If the LLM decides a tool is needed, it generates a special token (e.g., `<tool_call>`) followed by the JSON arguments.
4. **Execution:** The application intercepts this, parses the JSON, runs the actual Python/Node function, and gets the result.
5. **Observation:** The application appends the result to the conversation as a `Tool Message` and prompts the LLM again to synthesize the final answer.

## 5. Complexity (Time & Space)
- Adds significant latency because it requires multiple round-trips to the LLM (Prompt -> Tool Call -> Execute -> Prompt -> Final Answer).

## 6. Tiny worked example
User: "What's the weather in Tokyo?"
LLM knows it has `get_weather(location: string)`.
LLM outputs: `{"name": "get_weather", "arguments": {"location": "Tokyo"}}`
App runs API, gets "22°C, Sunny".
App sends back: `ToolResponse: "22°C, Sunny"`
LLM outputs: "It is currently 22°C and sunny in Tokyo."

## 7. Code (Python)
```python
# OpenAI API Tool Calling Example
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather in a location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    }
}]

# model will return message.tool_calls containing the JSON payload
# you execute the function, then append a message with role="tool"
```

## 8. Common mistakes
- Not providing clear descriptions in the JSON schema. The LLM relies entirely on the `description` field to decide *when* to use the tool. "Fetches user data" is bad; "Fetches user ID and email given a username" is good.
- Assuming the LLM will always output valid JSON. You must implement robust error handling and potentially pass the JSON parsing error back to the LLM so it can correct itself.

## 9. 30-second interview answer
"Tool calling allows an LLM to interact with external systems. Models are fine-tuned to recognize when a user query requires external data, select the appropriate tool from a provided JSON schema, and generate the correct arguments. The application executes the tool and feeds the result back to the LLM to synthesize the final response."

## 10. 2-minute interview answer
"Tool calling transforms an LLM from a static text generator into an active agent. To enable this, foundation models are specifically fine-tuned on tool-use datasets (like Gorilla or Toolformer). In practice, you pass a JSON schema defining available functions in the system prompt. When the model encounters a prompt requiring a tool, it generates a structured JSON payload instead of natural language. The application layer must intercept this, execute the corresponding code—whether that's a SQL query, a web search, or a Python REPL—and return the output as a 'Tool Observation' message. The model then resumes generation, incorporating the fresh data. This design pattern solves the LLM's fundamental flaws: knowledge cutoffs are solved by web search tools, math hallucinations are solved by calculator tools, and inability to take action is solved by API tools. The main challenges are ensuring the LLM reliably outputs valid JSON and preventing prompt injection attacks from executing malicious tool calls."

## 11. Follow-ups
- "How do models learn to use tools?" (Through instruction tuning on datasets where the correct response is a tool call, teaching the model the syntax and the reasoning of when to trigger it).

## 12. Deeper questions
- "What happens if a tool returns a massive JSON payload that exceeds the context window?" (You must pre-process or summarize the tool output before feeding it back to the LLM, or use RAG over the tool output).

## 13. Related concepts
- **Agents**: Tool calling is the fundamental capability that enables agents.
- **RAG**: Can be implemented as a tool (`search_documents(query)`).

## 14. When it breaks / Edge cases
- Hallucinated arguments: The LLM invents parameters that don't exist in the schema, causing application crashes.

## 15. Comparison with alternative approaches
- **Tool Calling vs Pure Prompting:** Tool calling offloads deterministic tasks (math, search) to code. Pure prompting forces the LLM to guess, which is error-prone.

---
*Where this shows up in ML:*
OpenAI Function Calling, LangChain Tools, AutoGPT.
