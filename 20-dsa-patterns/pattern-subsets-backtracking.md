# Pattern: Subsets / Backtracking

## 1. Definition
The Subsets/Backtracking pattern is a methodology to exhaustively search for all valid permutations, combinations, or subsets of a dataset by incrementally building candidates and abandoning ("backtracking") invalid paths.

## 2. Intuition
Imagine picking a 3-character password from "ABC". You start with "A". Then "AB". Then "ABC". You write it down. You erase "C" and try the next letter. No letters left. You erase "B" and try "C", getting "AC". Then "ACB". You are methodically exploring every branch of a decision tree and erasing your tracks to keep the workspace clean for the next branch.

## 3. Why it exists
For problems asking for "all possible ways", mathematical shortcuts usually don't exist. You must physically generate every option. Backtracking organizes this exhaustive generation, pruning invalid branches immediately to save exponential amounts of time.

## 4. Mechanics
A recursive template is universally applied:
1. **Goal Check:** If the current path satisfies the conditions, add a *deep copy* of the path to the results array.
2. **Loop/Choices:** Iterate over the available options.
3. **Choose:** Add the option to the current path.
4. **Explore:** Recursively call the function.
5. **Un-choose (Backtrack):** Remove the option from the current path so the next iteration of the loop starts with a clean slate.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(2^N)$ for Subsets/Combinations. $O(N!)$ for Permutations.
- **Space Complexity:** $O(N)$ for the recursion stack and temporary path array.

## 6. Tiny worked example
Subsets of `[1, 2]`.
- Path `[]` -> Save `[]`.
- Loop 1: Pick `1`. Path `[1]` -> Save `[1]`.
  - Loop 2: Pick `2`. Path `[1, 2]` -> Save `[1, 2]`.
  - Un-choose `2`. Path `[1]`.
- Un-choose `1`. Path `[]`.
- Loop 2: Pick `2`. Path `[2]` -> Save `[2]`.
- Un-choose `2`. Path `[]`.
Output: `[], [1], [1, 2], [2]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def subsets(nums: List[int]) -> List[List[int]]:
    result = []
    
    def backtrack(start: int, path: List[int]):
        # 1. Goal Check (for subsets, every path is a goal)
        result.append(path.copy()) # MUST DEEP COPY!
        
        # 2. Loop Choices
        for i in range(start, len(nums)):
            # 3. Choose
            path.append(nums[i])
            # 4. Explore
            backtrack(i + 1, path)
            # 5. Un-choose
            path.pop()
            
    backtrack(0, [])
    return result
```

## 8. Common mistakes
- **Pass by Reference Bug:** Doing `result.append(path)` instead of `result.append(path.copy())`. Because `path` is modified by `pop()` later, the final result will be an array of empty lists!
- Not handling duplicates correctly. If the input has duplicates, sort the array first, and add `if i > start and nums[i] == nums[i-1]: continue` inside the loop.

## 9. 30-second interview answer
"Backtracking is a DFS approach for generating combinations, permutations, and subsets. It uses a recursive template where we make a choice, recursively explore that path, and then 'undo' the choice to explore alternatives, taking $O(2^N)$ or $O(N!)$ time. Bounding constraints allow us to prune invalid paths early."

## 10. 2-minute interview answer
"Whenever an interview asks for 'all possible configurations'—like Sudoku, N-Queens, or distinct subsets—it is a Backtracking problem. Because these problems have exponential or factorial time complexities, the algorithmic challenge isn't finding a polynomial shortcut, but structuring the exhaustive search flawlessly. We model the problem as a state-space tree traversed via DFS. At each node, we loop through available choices, append a choice to our state, recurse, and critically, `pop()` the choice off the state before the loop continues. This 'un-choosing' ensures state purity. The most common bug candidates face is appending the reference of the state array to the results list, which later gets mutated to empty; a deep copy is mandatory. To optimize, we focus on pruning: immediately returning from the recursion if the current state violates problem constraints."

## 11. Follow-ups
- "How do Permutations differ from Subsets?" (Subsets use a `start` index to only look forward, preventing duplicate identical combinations like `[1,2]` and `[2,1]`. Permutations look at the *entire* array every time, using a `visited` boolean array to skip already used numbers).

## 12. Deeper questions
- "Is it possible to generate Subsets iteratively?" (Yes, cascading. Start with `[[]]`. For each number, take all existing subsets, copy them, and append the number).

## 13. Related concepts
- **Depth-First Search**: Backtracking is just DFS on an abstract graph.
- **Dynamic Programming**: If you add memoization to overlapping backtracking states, it becomes Top-Down DP.

## 14. When it breaks / Edge cases
- Cannot scale past $N=20$ for $O(2^N)$ or $N=12$ for $O(N!)$.

## 15. Comparison with alternative approaches
- **vs Bit Manipulation:** Subsets can be generated using a binary counter from $0$ to $2^N-1$. If the $i$-th bit is 1, include `nums[i]`. This is often cleaner than recursion for pure subsets, but less flexible for constraint pruning.

---
*Where this shows up in ML:* 
Beam Search (used in LLM decoding) is a greedy variation of backtracking. Instead of exploring all $O(V^N)$ branches, it prunes everything except the top $K$ most probable branches at each step.
