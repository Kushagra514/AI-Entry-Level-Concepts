# Memoization

## 1. Definition
Memoization is a Top-Down Dynamic Programming optimization technique that caches the return value of a recursive function for a given set of arguments, returning the cached result immediately if the function is called again with the same arguments.

## 2. Intuition
Imagine a student solving math problems. On a test with 100 questions, question 47 asks "What is 13 × 17?" and question 89 asks the same thing. A smart student writes the answer in the margin after question 47 and just looks it up for question 89. Memoization is the "write it in the margin" step.

## 3. Why it exists
Naive recursion for problems like Fibonacci or Longest Common Subsequence recomputes identical subproblems exponentially many times, yielding $O(2^N)$ complexity. Memoization computes each unique subproblem exactly once, collapsing the time complexity to the number of distinct states.

## 4. Mechanics
1. Write the recursive brute-force solution.
2. Identify the function parameters that define a unique subproblem (the "state").
3. Add a dictionary/array `memo` that maps `(state) -> result`.
4. At the top of the function: if `state in memo`, return `memo[state]`.
5. At the bottom, before returning: store `memo[state] = result`.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\text{unique states} \times \text{work per state})$. For Fibonacci: $O(N)$.
- **Space Complexity:** $O(\text{unique states})$ for the cache, plus $O(\text{depth})$ for the call stack.

## 6. Tiny worked example
Fibonacci without memoization: `fib(5)` calls `fib(4)` and `fib(3)`. `fib(4)` calls `fib(3)` and `fib(2)`. `fib(3)` is computed **twice**. Total calls: $2^N - 1 = 31$ for $N=5$.

With memoization: `fib(3)` computed once, stored. Second call returns instantly. Total calls: $2N - 1 = 9$ for $N=5$.

## 7. Code (Python, with type hints)
```python
from functools import lru_cache

# Python's @lru_cache automatically memoizes any pure function
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Manual memoization for more control (e.g., multi-parameter states)
def lcs(s1: str, s2: str) -> int:
    memo = {}
    def dp(i: int, j: int) -> int:
        if i == len(s1) or j == len(s2):
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        if s1[i] == s2[j]:
            result = 1 + dp(i + 1, j + 1)
        else:
            result = max(dp(i + 1, j), dp(i, j + 1))
        memo[(i, j)] = result
        return result
    return dp(0, 0)
```

## 8. Common mistakes
- Memoizing functions with mutable arguments (like lists). Mutable objects are not hashable and cannot be dict keys. Converts lists to tuples as dictionary keys.
- Forgetting to return `memo[state]` early. If you store in memo but still compute the full recursion, you get the right answer but no speedup.

## 9. 30-second interview answer
"Memoization caches recursive function results for previously computed inputs. It transforms exponential brute-force recursion into polynomial time by ensuring each unique state is computed exactly once. In Python, `@functools.lru_cache` provides this transparently for any pure function."

## 10. 2-minute interview answer
"Memoization is the Top-Down approach to Dynamic Programming. The workflow is systematic: write the brute-force recursive solution, identify what input values define a unique subproblem (these are the 'state variables'), and add a dictionary mapping `state -> result`. Before computing anything, check if the result is already cached. This simple pattern transforms Fibonacci from $O(2^N)$ to $O(N)$ and Longest Common Subsequence from $O(3^N)$ to $O(N \times M)$, reducing the problem's time complexity to exactly the number of distinct states times the work per state. Python's `@functools.lru_cache` automates this for functions with hashable arguments, making the pattern almost trivially easy to apply."

## 11. Follow-ups
- "When would you choose Memoization (Top-Down) over Tabulation (Bottom-Up)?" (Memoization is preferable when only a sparse subset of the state space is actually visited — for example, when many subproblems can be pruned early. Tabulation fills the entire table regardless).

## 12. Deeper questions
- "What is the difference between `lru_cache` and a plain `dict`-based memo?" (`lru_cache` has a configurable max size and evicts the Least Recently Used entry when full. A plain `dict` cache grows unboundedly. For interview problems with small inputs, both are equivalent).

## 13. Related concepts
- **Dynamic Programming (Bottom-Up Tabulation)**: The equivalent iterative approach.
- **Backtracking + Memo**: When memoization is added to backtracking to avoid recomputing the same state.

## 14. When it breaks / Edge cases
- If the recursion depth exceeds Python's default limit (~1000), a `RecursionError` is thrown. Use Bottom-Up DP or increase `sys.setrecursionlimit`.

## 15. Comparison with alternative approaches
- **vs Tabulation:** Memoization is recursive (uses call stack) and lazy (only computes needed states). Tabulation is iterative (no stack overflow risk) and eager (fills all states). Tabulation is usually faster in practice; memoization is easier to derive correctly.

---
*Where this shows up in ML:*
The KV-Cache in autoregressive LLM inference is conceptually memoization — previously computed key/value states are cached so they aren't recomputed at every new token generation step.
