# Recursion vs Iteration

## 1. Definition
**Recursion** solves a problem by having a function call itself with a smaller input until a base case is reached. **Iteration** solves the same problem by repeating a block of code with a loop and explicit state variables.

## 2. Intuition
- **Recursion:** To eat a pizza, eat one slice, then eat the rest of the pizza (which is now a smaller pizza). Keep going until no slices remain.
- **Iteration:** To eat a pizza, pick up a slice, eat it, pick up another slice, eat it, repeat until the pizza is gone.
Same result. Recursion expresses *what* to do. Iteration expresses *how* to step.

## 3. Why it exists
Recursion is often more **readable and mathematically natural** for problems that are inherently self-similar (trees, graphs, divide-and-conquer). Iteration is more **memory-efficient and performant**, as it avoids function call overhead and stack allocation.

## 4. Mechanics
- **Recursion:** Relies on the program's **call stack** to store intermediate state. Every call adds a stack frame containing local variables and the return address.
- **Iteration:** Explicitly maintains state in variables and loops. Uses no implicit stack; state lives only in heap/register variables.
- **Conversion:** Any recursive algorithm can be converted to an iterative one by using an explicit stack data structure (essentially simulating what the call stack does implicitly).

## 5. Complexity (Time & Space)
| Approach | Time | Space |
|---|---|---|
| Recursion | Same as iterative | $O(depth)$ call stack |
| Iteration | Same as recursive | $O(1)$ if no explicit stack |

## 6. Tiny worked example
Factorial of 5:
- **Recursive:** `f(5) → 5*f(4) → 5*4*f(3) → 5*4*3*f(2) → 5*4*3*2*f(1) → 120`. Stack depth = 5.
- **Iterative:** `result = 1; for i in [1..5]: result *= i`. Stack depth = 1 (constant).

## 7. Code (Python, with type hints)
```python
# Recursive DFS (concise, natural)
def dfs_recursive(root):
    if not root:
        return
    print(root.val)
    dfs_recursive(root.left)
    dfs_recursive(root.right)

# Iterative DFS (avoids Python's recursion limit)
from collections import deque
def dfs_iterative(root):
    if not root:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.val)
        if node.right: stack.append(node.right)
        if node.left:  stack.append(node.left)
```

## 8. Common mistakes
- Using deep recursion in Python without checking the depth. Python's default recursion limit is 1000 frames. A perfectly balanced tree of depth 100,000 will cause `RecursionError`.
- Writing iterative code that is more complex and harder to verify than its recursive equivalent, introducing subtle bugs where recursion would have been cleaner.

## 9. 30-second interview answer
"Recursion is elegant and maps naturally to self-similar problems like trees and divide-and-conquer, but carries $O(depth)$ call stack overhead. Iteration is memory-efficient and avoids stack overflow risks, but can be verbose. Any recursion can be converted to iteration using an explicit stack. For Python, prefer iteration for deep structures to avoid the recursion limit."

## 10. 2-minute interview answer
"The choice between recursion and iteration is a space-clarity tradeoff. Recursion leverages the OS call stack to implicitly store computation state, producing clean, declarative code that closely mirrors mathematical definitions — like DFS or Merge Sort. However, the call stack is limited (Python: ~1000, Java: ~10,000), and each frame adds overhead from pushing/popping registers and setting up scope. Iteration uses explicit variables and loops, achieving $O(1)$ overhead per step at the cost of verbosity. For many tree problems in an interview context, recursive code is preferable for its clarity and correctness. For production code with deeply nested structures, iterative solutions using an explicit stack are safer. Tail-call optimization (supported in languages like Scheme, not Python or Java) can make recursion as efficient as iteration when the recursive call is the last operation in the function."

## 11. Follow-ups
- "What is tail recursion?" (When the recursive call is the *last operation* in the function — no pending computation after the call returns. Languages with tail-call optimization (TCO) reuse the current stack frame, achieving $O(1)$ space like iteration. Python does NOT support TCO).

## 12. Deeper questions
- "How do you convert Merge Sort from recursive to iterative?" (Bottom-up Merge Sort: start with subarrays of size 1, merge pairs to size 2, then 4, then 8, doubling each pass. No recursion stack needed).

## 13. Related concepts
- **Memoization**: Often paired with recursion to cache results.
- **Divide and Conquer**: Naturally expressed recursively.

## 14. When it breaks / Edge cases
- Python's recursion limit (1000) breaks on unbalanced trees or long chains. Use `sys.setrecursionlimit(N)` or convert to iteration.

## 15. Comparison with alternative approaches
- N/A — they are two sides of the same computational coin.

---
*Where this shows up in ML:*
Autograd in PyTorch computes gradients by traversing a recursively-built computation graph. Internally it uses iterative topological sorting to avoid deep Python call stacks.
