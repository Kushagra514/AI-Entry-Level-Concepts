# Recursion

## 1. Definition
Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem, until it reaches a known base case.

## 2. Intuition
Imagine you are standing in a long line and want to know your position. You ask the person in front of you, "What's your position?" They don't know, so they ask the person in front of them. This continues until the person at the very front says, "I am number 1." The second person says, "I am 1 + 1 = 2," and so on, until the answer bubbles back to you.

## 3. Why it exists
It exists to elegantly solve problems that have a naturally recursive structure, such as tree traversals, graph algorithms, and divide-and-conquer strategies. Iterative solutions for these problems often require manually managing a stack, which makes code complex and harder to read.

## 4. Mechanics
Every recursive function needs two parts:
1. **Base Case:** The condition under which the function stops calling itself to prevent an infinite loop.
2. **Recursive Step:** The part of the function that breaks the problem into a smaller, simpler version of itself and calls the function again.
When a recursive call is made, the current function's state (variables) is paused and pushed onto the call stack until the child call returns.

## 5. Complexity (Time & Space)
- **Time Complexity:** Depends on the number of recursive calls and the work done per call. For branching recursion (like Naive Fibonacci), it can be $O(2^n)$.
- **Space Complexity:** $O(d)$, where $d$ is the maximum depth of the recursive call stack. Each active call consumes memory.

## 6. Tiny worked example
Factorial of 3:
- `fact(3)` calls `3 * fact(2)`
- `fact(2)` calls `2 * fact(1)`
- `fact(1)` calls `1 * fact(0)`
- `fact(0)` returns `1` (Base case)
- `fact(1)` returns `1 * 1 = 1`
- `fact(2)` returns `2 * 1 = 2`
- `fact(3)` returns `3 * 2 = 6`

## 7. Code (Python, with type hints)
```python
def factorial(n: int) -> int:
    # Base Case
    if n <= 1:
        return 1
    # Recursive Step
    return n * factorial(n - 1)
```

## 8. Common mistakes
- Forgetting the base case, leading to a `RecursionError` (Stack Overflow).
- Returning the recursive call incorrectly (e.g., calling the function but not returning its result).
- Passing the same arguments to the recursive call, preventing progression toward the base case.

## 9. 30-second interview answer
"Recursion is when a function calls itself to solve smaller subproblems of a larger problem. It requires a base case to terminate and a recursive step to shrink the input. It's highly readable for tree and graph problems but consumes $O(d)$ stack space where $d$ is the recursion depth."

## 10. 2-minute interview answer
"Recursion is a declarative approach to problem-solving that maps perfectly to naturally self-similar data structures like Trees and Graphs. Under the hood, it leverages the OS call stack to implicitly track state, avoiding the boilerplate of managing a manual stack. However, this comes with a space complexity cost proportional to the maximum recursion depth, $O(d)$. In environments without tail-call optimization, like Python, deep recursion can cause stack overflows. Therefore, while recursion is elegant for things like DFS or Merge Sort, we must be careful with linear recursion on large datasets, where iteration or memoization is safer."

## 11. Follow-ups
- "What happens if the base case is missing?" (Stack overflow because the call stack memory is exhausted).
- "How can you optimize recursive functions that compute the same states?" (Memoization/Dynamic Programming).

## 12. Deeper questions
- "What is Tail Call Optimization (TCO), and does Python support it?" (TCO is when the compiler reuses the current stack frame if the recursive call is the very last operation. Python does not support TCO by design to preserve stack traces).

## 13. Related concepts
- **Dynamic Programming**: Heavily relies on recursion + memoization.
- **Backtracking**: Uses recursion to explore search spaces and undo states.
- **Depth-First Search (DFS)**: Naturally implemented via recursion.

## 14. When it breaks / Edge cases
- Breaks when recursion depth exceeds the language's maximum stack limit (e.g., 1000 in Python).
- Breaks when the input size is massive and causes memory exhaustion.

## 15. Comparison with alternative approaches
- **vs Iteration:** Iteration has $O(1)$ space overhead (no call stack) and is generally faster due to lack of function call overhead, but is harder to write for complex branching logic like tree traversals.

---
*Where this shows up in ML:* 
Tree-based ML models (Decision Trees, Random Forests) are inherently recursive structures. The algorithms to split nodes during training (e.g., CART) are implemented recursively. Additionally, computation graphs in deep learning frameworks often use recursive graph traversals (DFS) during the backpropagation step to compute gradients via the chain rule.
