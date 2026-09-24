import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (DSA Qs)"')

wc("23-dsa-interview-questions/recursion-backtracking.md", r"""# Recursion & Backtracking Interview Questions

---

## 1. Permutations

### 1. Restate the Problem
Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in any order.

### 2. Clarify Edge Cases
- Elements are distinct.
- Array length $1 \le N \le 6$. (Factorial time constraint).

### 3. Brute Force Approach
Generate all possible combinations of elements of length N and filter out those with duplicates. Time: $O(N^N)$.

### 4. Key Insight
We can build permutations element by element using a tree-like decision process (DFS). At each step, we choose a number we haven't chosen yet. Once the current path reaches length $N$, we've found a permutation.

### 5. Optimized Approach (Backtracking)
Use a helper function `backtrack(path, remaining)`. If `remaining` is empty, append `path` to results. Otherwise, iterate through `remaining`. For each element, append it to `path`, recursively call `backtrack`, and then "backtrack" (remove it from `path`) to try the next element.

### 6. Justification
Time: $O(N \cdot N!)$ because there are $N!$ permutations, and copying the path to the result takes $O(N)$. Space: $O(N)$ for the recursion stack (ignoring output space).

### 7. Code (Python)
```python
from typing import List

def permute(nums: List[int]) -> List[List[int]]:
    ans = []
    
    def backtrack(path, remaining):
        if not remaining:
            ans.append(path[:]) # Append a copy of path
            return
            
        for i in range(len(remaining)):
            # Choose
            path.append(remaining[i])
            # Explore (pass remaining without the chosen element)
            backtrack(path, remaining[:i] + remaining[i+1:])
            # Un-choose (Backtrack)
            path.pop()
            
    backtrack([], nums)
    return ans
```

### 8. Dry Run
`nums = [1,2,3]`
- backtrack([], [1,2,3])
  - choose 1 -> backtrack([1], [2,3])
    - choose 2 -> backtrack([1,2], [3])
      - choose 3 -> backtrack([1,2,3], []) -> append [1,2,3]
      - pop 3
    - pop 2
    - choose 3 -> backtrack([1,3], [2]) -> append [1,3,2]
  - pop 1
- ...

### 9. Edge Cases Handled
Single element array returns `[[x]]`.

### 10. Follow-ups
- "What if there are duplicates in `nums`?" -> Sort the array first. In the loop, if `i > 0 and remaining[i] == remaining[i-1]`, skip it to avoid duplicate permutations. (Permutations II).

### 11. Related Problems
Subsets, Combinations.

---

## 2. Combination Sum

### 1. Restate the Problem
Given an array of distinct integers `candidates` and a `target` integer, return a list of all unique combinations where the chosen numbers sum to `target`. You may use the same number an unlimited number of times.

### 2. Clarify Edge Cases
- All positive integers.
- Combinations `(1,2)` and `(2,1)` are considered the same.

### 3. Brute Force Approach
N/A.

### 4. Key Insight
Since we can reuse elements, at each step we have two choices: Include the current element (and stay at the current index to potentially reuse it), or skip the current element (move to the next index).

### 5. Optimized Approach (Backtracking)
Use `dfs(i, current_path, current_sum)`. 
Base cases: If `current_sum == target`, append copy of path. If `current_sum > target` or `i >= len(candidates)`, return.
Recursive steps: 
1. Include `candidates[i]`: add to path, call `dfs(i, path, sum+cand)`.
2. Skip `candidates[i]`: pop from path, call `dfs(i+1, path, sum)`.

### 6. Justification
Time: $O(2^T)$ in the worst case where $T$ is the target (since minimum candidate is 1). Space: $O(T)$ for recursion depth.

### 7. Code (Python)
```python
def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    ans = []
    
    def dfs(i, current_path, current_sum):
        if current_sum == target:
            ans.append(current_path[:])
            return
        if i >= len(candidates) or current_sum > target:
            return
            
        # Decision 1: Include candidates[i]
        current_path.append(candidates[i])
        dfs(i, current_path, current_sum + candidates[i])
        
        # Decision 2: Skip candidates[i]
        current_path.pop()
        dfs(i + 1, current_path, current_sum)
        
    dfs(0, [], 0)
    return ans
```

### 8. Dry Run
`c=[2,3], t=4`
- dfs(0, [], 0):
  - incl 2: dfs(0, [2], 2)
    - incl 2: dfs(0, [2,2], 4) -> matches! append [2,2]
    - skip 2: dfs(1, [2], 2)
      - incl 3: dfs(1, [2,3], 5) -> returns (sum > target)
      - skip 3: dfs(2, [2], 2) -> returns (i > len)
  - skip 2: dfs(1, [], 0)
    - incl 3: dfs(1, [3], 3)
      - incl 3: dfs(1, [3,3], 6) -> returns
      - skip 3: dfs(2, [3], 3) -> returns
    - skip 3: dfs(2, [], 0) -> returns

### 9. Edge Cases Handled
Target unattainable simply returns empty list as no base case matches `target`.

### 10. Follow-ups
- "What if each number can only be used once?" -> Only call `dfs(i+1)` for the inclusion step. (Combination Sum II).

### 11. Related Problems
Subsets, Letter Combinations of a Phone Number.
""")

wc("23-dsa-interview-questions/dynamic-programming.md", r"""# Dynamic Programming Interview Questions

---

## 1. Climbing Stairs

### 1. Restate the Problem
You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### 2. Clarify Edge Cases
- $n = 1$? Return 1.
- $n = 2$? Return 2.

### 3. Brute Force Approach
DFS tree. Try taking 1 step and 2 steps from every position. Time: $O(2^N)$.

### 4. Key Insight
To reach step $N$, you must have come from either step $N-1$ (taking a 1-step) or step $N-2$ (taking a 2-step). Thus, `ways(N) = ways(N-1) + ways(N-2)`. This is the Fibonacci sequence. It has optimal substructure and overlapping subproblems.

### 5. Optimized Approach
Bottom-up DP. We don't need a full array of size $N$; we only need the last two values to compute the next one. Initialize `one = 1` and `two = 1` (for step 0 and 1). Loop $N-1$ times, calculating `temp = one + two`, updating `one = two` and `two = temp`.

### 6. Justification
Time: $O(N)$ because we iterate $N$ times. Space: $O(1)$ because we only store two integer variables.

### 7. Code (Python)
```python
def climbStairs(n: int) -> int:
    one, two = 1, 1
    
    for i in range(n - 1):
        temp = one + two
        one = two
        two = temp
        
    return two
```

### 8. Dry Run
`n = 3`
- init: one=1, two=1
- i=0: temp=2, one=1, two=2
- i=1: temp=3, one=2, two=3
- Return two (3). (Ways: 1+1+1, 1+2, 2+1).

### 9. Edge Cases Handled
`n=1` bypasses the loop and returns 1.

### 10. Follow-ups
- "What if you can take 1, 2, or 3 steps?" -> `ways(n) = ways(n-1) + ways(n-2) + ways(n-3)`. Store 3 variables instead of 2.

### 11. Related Problems
Fibonacci Number, Min Cost Climbing Stairs.

---

## 2. Coin Change

### 1. Restate the Problem
Given an integer array `coins` representing coins of different denominations and an integer `amount`, return the fewest number of coins that make up that amount. If it cannot be made, return `-1`.

### 2. Clarify Edge Cases
- `amount = 0`? Return 0.
- Cannot make amount? Return -1.

### 3. Brute Force Approach
Backtracking. Try taking every coin denomination recursively. Time: $O(S^N)$ where $S$ is amount and $N$ is coin count.

### 4. Key Insight
This is an Unbounded Knapsack problem. To find the min coins for amount `A`, if we try taking a coin of value `C`, the answer is `1 + min_coins(A - C)`. We can memoize this or build it bottom-up.

### 5. Optimized Approach (Bottom-up 1D DP)
Create a `dp` array of size `amount + 1`, initialized to `amount + 1` (acting as infinity). `dp[0] = 0`. Iterate through amounts from 1 to `amount`. For each amount, iterate through all coins. If `amount - coin >= 0`, `dp[amount] = min(dp[amount], 1 + dp[amount - coin])`. Return `dp[amount]` if it's less than "infinity", else -1.

### 6. Justification
Time: $O(A \cdot C)$ where $A$ is the amount and $C$ is the number of coins. Space: $O(A)$ for the `dp` array.

### 7. Code (Python)
```python
def coinChange(coins: List[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != amount + 1 else -1
```

### 8. Dry Run
`coins=[1,2,5], amount=11`
- a=1: trying 1 -> dp[1] = 1+dp[0] = 1.
- a=2: trying 1 -> 1+dp[1] = 2. trying 2 -> 1+dp[0] = 1. dp[2] = 1.
- ...
- a=11: trying 1 -> 1+dp[10]. trying 5 -> 1+dp[6]. dp[11] = 3.

### 9. Edge Cases Handled
Amount 0 instantly returns 0. Impossible amounts stay at `amount + 1` and return `-1`.

### 10. Follow-ups
- "What if you want to find the *number of combinations* to make the amount?" -> This is Coin Change II. `dp[a] += dp[a-c]`.

### 11. Related Problems
Coin Change II, Minimum Path Sum.
""")
print("DSA Qs 4 complete")
