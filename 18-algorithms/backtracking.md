# Backtracking

## 1. Definition
Backtracking is an algorithmic paradigm that systematically searches for a solution to a problem among all available options. It does so by building candidates incrementally and abandoning ("backtracking" from) a candidate as soon as it determines the candidate cannot yield a valid solution.

## 2. Intuition
Imagine navigating a physical maze. You walk down a path, leaving a trail of breadcrumbs. You hit a dead end. You turn around, walk back along your breadcrumbs to the last intersection, pick up those crumbs, and try a different path. You "undo" your mistake and try again.

## 3. Why it exists
For problems requiring us to find *all* permutations, combinations, or a specific valid configuration (like Sudoku), there is no mathematical shortcut or greedy logic. We must exhaustively search. Backtracking organizes this exhaustive search, pruning invalid paths early (bounding) to save massive amounts of time compared to pure brute-force generation.

## 4. Mechanics
1. **Choose:** Pick an option and add it to the current state/path.
2. **Explore:** Recursively call the backtracking function with the new state.
3. **Un-choose (Backtrack):** Remove the option from the current state/path, returning it to how it was before step 1, so the next loop iteration can try a different option cleanly.
4. **Base Case:** If the state is a valid final solution, save a *copy* of it. If it violates constraints, return immediately (prune).

## 5. Complexity (Time & Space)
- **Time Complexity:** Usually exponential or factorial. $O(2^N)$ for subsets, $O(N!)$ for permutations.
- **Space Complexity:** $O(N)$ for the recursion stack and the path array.

## 6. Tiny worked example
Permutations of `[1, 2]`.
- Start: `[]`
- Loop: Pick `1`. Path: `[1]`.
  - Explore: Pick `2`. Path `[1, 2]`. Base case hit! Save `[1, 2]`.
  - Un-choose: Remove `2`. Path `[1]`.
- Un-choose: Remove `1`. Path: `[]`.
- Loop: Pick `2`. Path: `[2]`.
  - Explore: Pick `1`. Path `[2, 1]`. Base case hit! Save `[2, 1]`.
- Output: `[[1, 2], [2, 1]]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def permute(nums: List[int]) -> List[List[int]]:
    result = []
    
    def backtrack(path: List[int], used: List[bool]):
        if len(path) == len(nums):
            result.append(path.copy()) # MUST APPEND A COPY!
            return
            
        for i in range(len(nums)):
            if used[i]: continue
            
            # 1. Choose
            used[i] = True
            path.append(nums[i])
            
            # 2. Explore
            backtrack(path, used)
            
            # 3. Un-choose
            path.pop()
            used[i] = False
            
    backtrack([], [False] * len(nums))
    return result
```

## 8. Common mistakes
- **Not appending a copy:** `result.append(path)` in Python appends a *reference* to the list. When the list is later popped/modified during backtracking, the saved result changes too, leaving you with a list of empty arrays. Always use `path.copy()` or `path[:]`.
- Forgetting the "un-choose" step, leading to states bleeding into each other.

## 9. 30-second interview answer
"Backtracking is an optimized exhaustive search method used for permutations, combinations, and constraint satisfaction problems. It builds a state incrementally, recursively explores, and most importantly, 'undoes' the choice (backtracks) to allow the exploration of alternative paths. We prune invalid paths early to beat pure brute-force generation."

## 10. 2-minute interview answer
"Backtracking is essentially Depth-First Search applied to an abstract state-space tree. We use it when a problem asks for 'all possible ways' to arrange or combine elements, dictating an inherently exponential $O(2^N)$ or $O(N!)$ time complexity. The core template involves three steps inside a loop: choose an option, recursively explore that choice, and then 'un-choose' it by popping it off the state tracking array. This un-choosing ensures the state is perfectly clean for the next iteration of the loop. The critical bug candidates write is forgetting to deep-copy the path array when adding it to the final results list. To optimize, we focus heavily on bounding/pruning—if a partial state already violates a constraint, we return immediately, severing that entire branch of the recursion tree and saving massive computation."

## 11. Follow-ups
- "How do you handle duplicates in Permutations or Subsets?" (Sort the input array first. Inside the loop, if `i > start` and `nums[i] == nums[i-1]`, `continue` to skip the duplicate branch).

## 12. Deeper questions
- "What's the difference between Backtracking and Branch & Bound?" (Backtracking explores all valid solutions. Branch and Bound is used for optimization problems—if the current branch's 'best possible' score is worse than the current global best, it prunes the branch).

## 13. Related concepts
- **Depth-First Search (DFS)**: Backtracking is DFS.
- **Dynamic Programming**: If backtracking subproblems overlap, adding a memoization cache turns it into Top-Down DP.

## 14. When it breaks / Edge cases
- Breaks entirely on large $N$ (e.g., $N=50$). $O(2^{50})$ will never finish executing.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
In traditional AI, constraint satisfaction problems (like Sudoku or scheduling algorithms) are solved using backtracking. In modern ML, Beam Search is somewhat related—it explores branches of generated text, but instead of exhaustive backtracking, it greedily prunes the tree to a fixed width (beam size) to maintain tractability.
