# Recursion & Backtracking Interview Questions

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
