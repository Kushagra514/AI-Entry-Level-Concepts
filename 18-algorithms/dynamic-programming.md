# Dynamic Programming Intro

## 1. Definition
Dynamic Programming (DP) is an algorithmic paradigm that solves complex problems by breaking them down into simpler, overlapping subproblems, and storing the results of these subproblems to avoid redundant computation.

## 2. Intuition
"Those who cannot remember the past are condemned to repeat it." If I ask you what 1+1+1+1+1 is, you say 5. If I add another "+1" at the end, you don't recount from the beginning; you just add 1 to your previous answer (5), getting 6. DP is just teaching a computer to remember its previous answers.

## 3. Why it exists
Many recursive problems (like Naive Fibonacci) compute the exact same states millions of times, leading to massive $O(2^n)$ exponential time complexities. DP exists to trade a little bit of memory ($O(N)$ space) to remember those states, collapsing the time complexity down to $O(N)$ polynomial time.

## 4. Mechanics
DP can be implemented in two ways:
1. **Top-Down (Memoization):** Write a standard recursive function, but before returning an answer, save it in a Hash Map/Array. Before doing work, check if the answer is already in the map.
2. **Bottom-Up (Tabulation):** Eliminate recursion entirely. Build an array from the base case (index 0) up to the target `n`, using a `for` loop and a state transition equation.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\text{Number of States} \times \text{Time per State transition})$. Usually polynomial (e.g., $O(N)$ or $O(N^2)$).
- **Space Complexity:** $O(\text{Number of States})$ to store the memoization table or DP array. Often optimizable to $O(1)$ in Bottom-Up if you only need the last few states.

## 6. Tiny worked example
Fibonacci: `F(n) = F(n-1) + F(n-2)`
Naive `F(4)` calls `F(3)` and `F(2)`. `F(3)` calls `F(2)` and `F(1)`. `F(2)` is computed twice.
DP Top-Down: Compute `F(2)` once, save it in `memo[2]`. Next time, just return `memo[2]`.

## 7. Code (Python, with type hints)
```python
from typing import Dict

# Top-Down (Memoization)
def fib_memo(n: int, memo: Dict[int, int] = None) -> int:
    if memo is None: memo = {}
    if n in memo: return memo[n]
    if n <= 1: return n
    
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# Bottom-Up (Tabulation) with O(1) space optimization
def fib_tab(n: int) -> int:
    if n <= 1: return n
    prev2, prev1 = 0, 1
    
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
        
    return prev1
```

## 8. Common mistakes
- Confusing DP with Divide and Conquer. (Merge sort is Divide and Conquer because the subproblems are *independent*. DP is used when subproblems *overlap*).
- Failing to properly define the "State" (what variables uniquely identify a subproblem).

## 9. 30-second interview answer
"Dynamic Programming is an optimization technique for recursive problems with overlapping subproblems and optimal substructure. By caching the results of subproblems either top-down via memoization or bottom-up via tabulation, we reduce exponential time complexities to polynomial time."

## 10. 2-minute interview answer
"Dynamic programming transforms exponential time recursion into polynomial time iteration or memoization. For a problem to be solvable with DP, it must have two properties: Overlapping Subproblems (we solve the exact same thing multiple times) and Optimal Substructure (the optimal solution to the big problem is made of optimal solutions to its smaller parts). The easiest way to solve DP problems is to first write the brute-force recursive solution. Once you have that, Top-Down DP is trivially achieved by adding a hash map to cache the return values. However, for production code, Bottom-Up Tabulation is preferred because it avoids the recursive call stack overhead entirely and often allows for state-space reduction, turning an $O(N)$ memory footprint into $O(1)$ if we only rely on the immediately preceding states."

## 11. Follow-ups
- "When would you prefer Memoization over Tabulation?" (When the state space is sparse—meaning you don't actually need to compute every single subproblem to reach the end, Top-Down will naturally skip the unnecessary ones).

## 12. Deeper questions
- "What is State Space Reduction?" (In bottom-up DP, if `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`, you don't need an array of size $N$; you just need two variables, saving massive memory).

## 13. Related concepts
- **Greedy Algorithms**: Like DP, they require optimal substructure, but Greedy algorithms make a localized optimal choice and *never look back*, whereas DP considers all possibilities.

## 14. When it breaks / Edge cases
- Breaks if the problem lacks Optimal Substructure (e.g., finding the longest *simple* path in a graph—a sub-path of the longest path isn't necessarily the longest path between those two sub-nodes).

## 15. Comparison with alternative approaches
- **vs Backtracking:** Backtracking is optimized exhaustive search for non-overlapping problems (like Sudoku). DP is caching for overlapping problems.

---
*Where this shows up in ML:* 
The Viterbi algorithm (used in Hidden Markov Models for NLP tagging) is a classic 2D Dynamic Programming algorithm. Dynamic Time Warping (DTW) for speech recognition is pure DP. Sequence alignment algorithms (Needleman-Wunsch) used in bioinformatics/AI are also standard DP.
