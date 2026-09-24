# 1D Dynamic Programming

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
