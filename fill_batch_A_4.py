import os

def write_and_commit(path, content):
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch A)"')

files = {}

files["17-data-structures/heaps-priority-queues.md"] = """# Heaps & Priority Queues

## 1. Definition
A Priority Queue is an abstract data type like a regular queue, but every element has a "priority". Elements with higher priority are dequeued before elements with lower priority. A Heap is the optimal tree-based data structure used to implement a Priority Queue.

## 2. Intuition
Think of an ER waiting room. Unlike a grocery line (FIFO), patients are treated based on the severity of their condition. A gunshot wound (high priority) is treated before a sprained ankle (low priority), regardless of who arrived first. A Heap is the system that instantly tells the doctor who the highest-priority patient is at any moment.

## 3. Why it exists
If we use a sorted array for a priority queue, extracting the max is $O(1)$, but inserting a new element is $O(N)$. If we use an unsorted array, insert is $O(1)$ but finding the max is $O(N)$. A Heap offers a mathematical compromise: $O(\\log N)$ for both insertion and extraction, keeping the absolute highest (or lowest) element at the top at all times.

## 4. Mechanics
- **Structure:** A Heap is a *Complete Binary Tree* (all levels are fully filled except possibly the last level, filled left to right). Because it's complete, it's efficiently stored in a simple Array, not with pointers.
- **Heap Property:** In a Min-Heap, every parent is $\\le$ its children (root is the minimum). In a Max-Heap, every parent is $\\ge$ its children.
- **Insert:** Add to the end of the array, then "bubble up" (swap with parent) until the heap property is restored.
- **Pop:** Remove the root, replace it with the last element in the array, then "bubble down" (swap with smallest/largest child).

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Peek (find max/min): $O(1)$.
  - Push/Pop: $O(\\log N)$.
  - Heapify (convert array to heap): $O(N)$.
- **Space Complexity:** $O(N)$ to store the array.

## 6. Tiny worked example
Array representation: `[10, 20, 30]`. `10` is root. Children of index `i` are at `2i+1` and `2i+2`.
Insert `5` (Min-Heap):
- Add to end: `[10, 20, 30, 5]`.
- Bubble up: `5` is at index 3. Parent is index 1 (`20`). Swap.
- `[10, 5, 30, 20]`. Parent of index 1 is index 0 (`10`). Swap.
- Final: `[5, 10, 30, 20]`. Root is now 5.

## 7. Code (Python, with type hints)
```python
import heapq
from typing import List

# Python's heapq only implements Min-Heaps
def top_k_elements(nums: List[int], k: int) -> List[int]:
    min_heap = []
    
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            # Pop the smallest element, keeping the K largest in the heap
            heapq.heappop(min_heap)
            
    return min_heap
```

## 8. Common mistakes
- Forgetting that Python's `heapq` is a Min-Heap. To simulate a Max-Heap with integers, you must push `-val` and invert it when popping.
- Sorting the entire array ($O(N \\log N)$) when asked for the "Top K" elements, instead of using a Heap of size K ($O(N \\log K)$).

## 9. 30-second interview answer
"A Heap is a complete binary tree that satisfies the heap property, typically used to implement a Priority Queue. It provides $O(1)$ access to the minimum or maximum element, and $O(\\log N)$ time for insertions and deletions. It is the optimal data structure for 'Top-K' or scheduling problems."

## 10. 2-minute interview answer
"A Heap perfectly solves the Priority Queue problem by bridging the gap between $O(1)$ and $O(N)$ operations. Because a Heap is a complete binary tree, it doesn't need pointer-based nodes; it maps perfectly into a contiguous array, making it extremely cache-friendly. The 'Heap Property' guarantees the min or max is always at the root index 0. When we insert or extract, we perform logarithmic 'bubble' operations to maintain this property. In algorithmic interviews, whenever a problem asks for the 'Kth largest/smallest', 'Top K frequent', or involves continuously merging the smallest elements like in Huffman Coding or Dijkstra's algorithm, a Heap is the definitive answer, reducing an $O(N \\log N)$ sort to an $O(N \\log K)$ stream."

## 11. Follow-ups
- "Why does `heapify` take $O(N)$ time instead of $O(N \\log N)$?" (Most nodes are at the bottom of the tree and don't bubble down far; mathematically, the infinite sum bounds to $O(N)$).
- "How does Dijkstra's algorithm use a Priority Queue?" (To always explore the node with the current shortest known distance next).

## 12. Deeper questions
- "What's a Fibonacci Heap?" (A highly advanced theoretical heap that offers $O(1)$ amortized insertion and decrease-key operations, though it's too complex for most practical implementations).

## 13. Related concepts
- **Dijkstra's & Prim's Algorithms**: Rely heavily on priority queues.
- **Heap Sort**: An in-place $O(N \\log N)$ sort using a max-heap.

## 14. When it breaks / Edge cases
- If you need to search for an arbitrary element in a heap, it takes $O(N)$ time (it's not a BST).

## 15. Comparison with alternative approaches
- **vs BST:** BST gives $O(\\log N)$ for searching *any* value. Heap only gives $O(1)$ for the max/min, but has less memory overhead (no pointers) and faster average insertions.

---
*Where this shows up in ML:* 
In LLM generation, during Beam Search decoding, we use a Priority Queue (Heap) to keep track of the top-K most probable sequence hypotheses at each token generation step, discarding lower probability paths.
"""

files["18-algorithms/dynamic-programming.md"] = """# Dynamic Programming Intro

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
- **Time Complexity:** $O(\\text{Number of States} \\times \\text{Time per State transition})$. Usually polynomial (e.g., $O(N)$ or $O(N^2)$).
- **Space Complexity:** $O(\\text{Number of States})$ to store the memoization table or DP array. Often optimizable to $O(1)$ in Bottom-Up if you only need the last few states.

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
"""

files["19-dp-deep-dive/dp-intuition-and-identification.md"] = """# DP Intuition and Identification

## 1. Definition
This is a meta-pattern for recognizing during an interview whether a problem requires Dynamic Programming, and mathematically defining the state and transition required to solve it.

## 2. Intuition
You're in an interview. You see a problem asking for "the maximum," "the minimum," or "the number of ways." You think: is there a greedy shortcut? If greed fails because future choices depend on current choices, and you have to essentially check all combinations, it's almost certainly DP.

## 3. Why it exists
Candidates often freeze when asked a DP problem because they try to jump straight to a nested `for` loop (bottom-up tabulation) without understanding the core logic. A structured identification method exists to bridge the gap from English prompt -> Recursion -> DP.

## 4. Mechanics (The FAST Method)
1. **F - First Solution:** Write or conceptualize the naive recursive brute-force solution. What choices do you make at each step? (e.g., "take item" or "skip item").
2. **A - Analyze:** Does it do the same work repeatedly? (Overlapping subproblems). Does the final optimal answer depend on optimal sub-answers? (Optimal substructure).
3. **S - Subproblem (State):** Define the state variables. What changes between recursive calls? (e.g., `index`, `remaining_capacity`). Let `dp(i, c)` be the max value at index `i` with capacity `c`.
4. **T - Turn Around:** Define the Transition Equation. How does `dp(i, c)` relate to smaller states? e.g., `dp(i, c) = max(dp(i-1, c), val[i] + dp(i-1, c-weight[i]))`.

## 5. Complexity (Time & Space)
- **Time:** $O(\\text{Unique States} \\times \\text{Transitions per State})$.
- **Space:** $O(\\text{Unique States})$.

## 6. Tiny worked example
Problem: "Climbing Stairs". You can take 1 or 2 steps. How many ways to reach top $N$?
- **First:** `ways(N) = ways(N-1) + ways(N-2)`.
- **Analyze:** `ways(4)` calls `ways(3)` and `ways(2)`. `ways(3)` calls `ways(2)`. Overlap!
- **State:** `dp(i)` = number of ways to reach step `i`.
- **Transition:** `dp(i) = dp(i-1) + dp(i-2)`. (This is just Fibonacci).

## 7. Code (Python, with type hints)
*(Concept code for transitioning from Recursion to Memoization)*
```python
# The Universal DP Template (Top-Down)
def solve_dp(params):
    memo = {}
    def dp(state_vars):
        if base_case_condition(state_vars):
            return base_value
            
        if state_vars in memo:
            return memo[state_vars]
            
        # Try all choices, take min/max/sum
        ans = min/max/sum(
            dp(new_state) + cost for new_state in choices
        )
        
        memo[state_vars] = ans
        return ans
        
    return dp(initial_state)
```

## 8. Common mistakes
- **Greedy Trap:** Assuming a problem is greedy when it's actually DP. Example: 0/1 Knapsack. Greedy (taking highest value/weight ratio) fails. You *must* use DP.
- **State Bloat:** Including variables in the state that can be derived from other variables, wasting massive amounts of memory.

## 9. 30-second interview answer
"I identify DP problems by looking for keywords like 'maximize', 'minimize', or 'total ways', coupled with constraints that prevent a purely greedy approach. I map out the choices at a single step, write the recursive relation, and memoize the overlapping states."

## 10. 2-minute interview answer
*(N/A - this is a meta-skill file, use the 30-second answer in practice).*

## 11. Follow-ups
- "How do you know if Greedy will work instead of DP?" (You have to prove that a local optimum *always* leads to a global optimum. If you can think of a single counter-example where taking the best immediate choice ruins a better long-term choice, Greedy is out, DP is in).

## 12. Deeper questions
- "How do you handle DP states that are subsets or combinations?" (Bitmask DP. Instead of passing an array of `visited` boolean flags as state, which isn't hashable, you pass an integer where the bits represent the flags).

## 13. Related concepts
- **1D DP**: State relies on 1 variable (like index).
- **2D DP**: State relies on 2 variables (like index and remaining capacity).

## 14. When it breaks / Edge cases
- Fails if the state space is too large (e.g., $N=10^9$). DP will TLE (Time Limit Exceeded). You probably need a Math formula or Matrix Exponentiation.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Formulating Markov Decision Processes (MDPs) in Reinforcement Learning requires identifying the "State", the "Action", and the "Reward" transition matrix, which is conceptually identical to identifying DP states and transitions.
"""

files["19-dp-deep-dive/1d-dp.md"] = """# 1D Dynamic Programming

## 1. Definition
1D Dynamic Programming involves solving optimization or counting problems where the state can be uniquely defined by a single variable, typically an index `i` representing the position in an array or a target numerical value.

## 2. Intuition
Imagine you are walking down a path of stepping stones, and at each stone, you can either jump to the next stone or the one after it. To know the best way to reach stone 10, you only need to know the best way to reach stone 9 and stone 8. The single variable defining your state is just your current stone number.

## 3. Why it exists
Many linear sequences (arrays, strings, staircases, days in a month) contain subproblems that overlap in a strictly one-dimensional manner. 1D DP provides the simplest, most memory-efficient way to cache these computations.

## 4. Mechanics
- **State Definition:** Let `dp[i]` be the optimal answer for the subproblem ending at or involving index `i` (or target sum `i`).
- **Transition Equation:** Relate `dp[i]` to previous states, e.g., `dp[i-1]`, `dp[i-2]`.
- **Base Cases:** Define `dp[0]` and/or `dp[1]`.
- **Memory Optimization:** If `dp[i]` only relies on the previous $K$ states, you don't need a full array of size $N$; you just need $K$ variables.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - We compute $N$ states, and each state takes $O(1)$ time to transition.
- **Space Complexity:** $O(N)$ for the `dp` array, often reducible to $O(1)$ via State Space Reduction.

## 6. Tiny worked example
Problem: House Robber. Maximize money. Cannot rob adjacent houses.
Houses: `[2, 7, 9, 3, 1]`
- `dp[0] = 2` (Rob H0)
- `dp[1] = max(2, 7) = 7` (Rob H1)
- `dp[2] = max(dp[1], dp[0] + 9) = max(7, 11) = 11` (Skip H2, or Rob H0+H2)
- `dp[3] = max(dp[2], dp[1] + 3) = max(11, 10) = 11`
- `dp[4] = max(dp[3], dp[2] + 1) = max(11, 12) = 12`
Max money is 12.

## 7. Code (Python, with type hints)
```python
from typing import List

def rob(nums: List[int]) -> int:
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    
    # O(N) Space approach:
    # dp = [0] * len(nums)
    # dp[0] = nums[0]
    # dp[1] = max(nums[0], nums[1])
    # for i in range(2, len(nums)):
    #     dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    # return dp[-1]
    
    # O(1) Space approach (State Space Reduction):
    prev2, prev1 = 0, 0
    for num in nums:
        # dp[i] = max(dp[i-1], dp[i-2] + num)
        curr = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = curr
        
    return prev1
```

## 8. Common mistakes
- Failing to handle edge cases like `len(nums) == 0` or `len(nums) == 1` before iterating.
- Not recognizing that 1D DP can be space-optimized to $O(1)$. Interviewers *will* ask for this optimization.

## 9. 30-second interview answer
"1D DP solves problems where the state is defined by a single variable, like an array index. Classic examples are Climbing Stairs or House Robber. We define `dp[i]` based on a transition from `dp[i-1]` and `dp[i-2]`. Because we only look back a fixed number of steps, we can optimize the $O(N)$ space down to $O(1)$ by just keeping track of the previous variables."

## 10. 2-minute interview answer
"When dealing with sequence optimization problems where decisions at step $i$ depend only on the results of the immediately preceding steps, 1D DP is the optimal pattern. We define a state `dp[i]` representing the optimal solution up to index `i`. The core of the problem is identifying the recurrence relation—for instance, in the House Robber problem, the choice at house `i` is the maximum of either skipping it (taking `dp[i-1]`) or robbing it (taking `dp[i-2] + current_value`). While the naive tabular approach takes $O(N)$ time and $O(N)$ space, 1D DP almost always allows for State Space Reduction. Because we only need a trailing window of the last two states, we can drop the array entirely and use two variables, achieving $O(N)$ time and $O(1)$ space, which is the gold standard for these interview questions."

## 11. Follow-ups
- "What if the houses are in a circle?" (House Robber II: Run the 1D DP twice. Once from index 0 to N-2, and once from 1 to N-1, return the max of both).

## 12. Deeper questions
- "What if the transition depends on *all* previous states, not just the last two? (e.g., Longest Increasing Subsequence)" (Then space optimization to $O(1)$ is impossible. You must keep the full $O(N)$ array, and time complexity becomes $O(N^2)$ because calculating `dp[i]` requires a loop from `0` to `i-1`).

## 13. Related concepts
- **2D DP**: When a single index isn't enough (e.g., you need index AND remaining capacity).

## 14. When it breaks / Edge cases
- Breaks if the problem requires you to know the *exact path* taken. Space reduction discards previous states, so if you need to print the path, you must keep the $O(N)$ array and backtrace.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
In Reinforcement Learning, basic 1D value-iteration for a 1D grid-world is exactly a 1D dynamic programming problem (computing the Bellman equation backwards).
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch A - Part 4 Complete")
