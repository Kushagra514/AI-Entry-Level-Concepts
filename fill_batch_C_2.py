import os

def write_and_commit(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch C)"')

files = {}

files["20-dsa-patterns/pattern-binary-search-on-answer.md"] = r"""# Pattern: Binary Search on Answer

## 1. Definition
Binary Search on Answer is a technique used to find the optimal solution to an optimization problem (minimize the maximum or maximize the minimum) by binary searching the *range of possible answers* rather than the input array itself.

## 2. Intuition
Imagine trying to find the minimum capacity a delivery truck needs to ship packages in $D$ days. You know a capacity of 1 is too small. You know a capacity of 1,000,000 is definitely large enough. Instead of simulating every capacity from 1 to 1,000,000, you guess 500,000. If 500,000 works, you try 250,000. If it fails, you try 750,000. You are searching the *answer space*.

## 3. Why it exists
Optimization problems are often NP-hard to solve constructively. However, verifying if a specific answer works (a decision problem) is often easy ($O(N)$). Binary Search on Answer turns a hard optimization problem into $\log(\text{Range})$ easy verification problems.

## 4. Mechanics
1. **Define Search Space:** Find the absolute minimum possible answer (`low`) and maximum possible answer (`high`).
2. **Binary Search:** Calculate `mid = (low + high) // 2`.
3. **Condition/Verification Function:** Write a greedy $O(N)$ helper function `is_valid(mid)` that checks if `mid` is a valid answer.
4. **Adjust Bounds:** 
   - If `is_valid(mid)` is true, you have a valid answer, but can you do better? Adjust `high = mid` (or `low = mid` if maximizing).
   - If false, adjust `low = mid + 1` (or `high = mid - 1`).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \log(\text{Range}))$. $N$ for the validation function, $\log(\text{Range})$ for the binary search.
- **Space Complexity:** $O(1)$ usually, as validation is typically a greedy scan.

## 6. Tiny worked example
Koko Eating Bananas. Koko must eat `[3, 6, 7, 11]` bananas in $H=8$ hours. Speed is $K$ bananas/hr.
- Min speed = 1. Max speed = 11 (max in array).
- Mid = 6. Can she eat them at 6/hr in 8 hours? $1 + 1 + 2 + 2 = 6$ hours. Valid! Try slower.
- Mid = 3. Time: $1 + 2 + 3 + 4 = 10$ hours. Invalid! 10 > 8. Try faster.
- Eventually converges to optimal $K = 4$.

## 7. Code (Python, with type hints)
```python
import math
from typing import List

def minEatingSpeed(piles: List[int], h: int) -> int:
    def can_finish(speed: int) -> bool:
        hours = sum(math.ceil(pile / speed) for pile in piles)
        return hours <= h

    low, high = 1, max(piles)
    
    while low < high:
        mid = (low + high) // 2
        if can_finish(mid):
            high = mid # Mid is valid, but maybe we can go slower
        else:
            low = mid + 1 # Mid is too slow, must increase speed
            
    return low
```

## 8. Common mistakes
- Not realizing the problem is monotonic. The validation function *must* be monotonic (i.e., if $K$ works, $K+1$ must also work). If the validity goes `[False, True, False, True]`, binary search fails.
- Off-by-one errors in `low` and `high` updates (`low = mid + 1` vs `high = mid`).

## 9. 30-second interview answer
"Binary Search on Answer solves optimization problems by binary searching the range of possible solutions. Instead of building the answer directly, we guess a value and use a greedy $O(N)$ validation function to verify if the guess works. This reduces complexity to $O(N \log(\text{Range}))$."

## 10. 2-minute interview answer
"Whenever an interview question asks to 'minimize the maximum' or 'maximize the minimum', it is almost always Binary Search on Answer. The paradigm shifts the problem from construction to verification. Instead of figuring out the perfect allocation, we define the search space—the lowest possible answer and the highest possible answer. We then pick the midpoint and run a greedy $O(N)$ boolean function to check: 'Is this midpoint a valid solution?'. If it is, we try to find a tighter bound. The crucial mathematical requirement is monotonicity: the boolean answers over the range must form a pattern like `[False, False, True, True, True]`. This allows us to binary search the exact boundary in $O(N \log(\text{Range}))$ time, turning an impossible combinatorial problem into a trivial one."

## 11. Follow-ups
- "What if the answer space is continuous (floats) instead of integers?" (You run the binary search for a fixed number of iterations, e.g., 100 times, or until `high - low < 1e-6`).

## 12. Deeper questions
- "How does this relate to the Fractional Cascading technique?" (Advanced DS technique that speeds up binary searches across multiple lists).

## 13. Related concepts
- **Binary Search**: The core driver.
- **Greedy Algorithms**: The validation function is always greedy.

## 14. When it breaks / Edge cases
- Breaks entirely if the validation function is not monotonic (e.g., a speed of 5 works, but a speed of 6 fails due to weird problem constraints).

## 15. Comparison with alternative approaches
- **vs Dynamic Programming:** DP can solve some of these (like splitting arrays), but takes $O(N^2 \times K)$ time, whereas Binary Search on Answer takes $O(N \log(\text{Sum}))$, which is significantly faster.

---
*Where this shows up in ML:* 
Hyperparameter search (like learning rate bounding) sometimes behaves monotonically and can be optimized using binary-search-like heuristics (though usually Bayesian optimization is preferred due to noise).
"""

files["20-dsa-patterns/pattern-cyclic-sort.md"] = r"""# Pattern: Cyclic Sort

## 1. Definition
Cyclic Sort is an in-place $O(N)$ sorting algorithm specifically designed for arrays where the elements are known to fall within a continuous range from $1$ to $N$ (or $0$ to $N$).

## 2. Intuition
Imagine a team of 5 runners wearing jerseys numbered 1 through 5, standing in random order. To sort them, you look at the person in the first spot. If they are wearing jersey #4, you tell them to go to spot #4, and the person at spot #4 comes to spot #1. You repeat this until jersey #1 is finally in spot #1. Because every swap puts at least one person in their correct spot, everyone is sorted instantly.

## 3. Why it exists
Standard sorting takes $O(N \log N)$. If we know the array contains numbers from $1$ to $N$, we can use the array indices themselves as a Hash Map, sorting the array in $O(N)$ time and strictly $O(1)$ space. It is the optimal solution for finding missing or duplicate numbers in a fixed range.

## 4. Mechanics
1. Iterate through the array with index `i`.
2. Check if `nums[i]` is in its correct index (i.e., `nums[i] == nums[nums[i] - 1]`).
3. If not, swap `nums[i]` with the element at its target index.
4. Do NOT increment `i` until the correct number lands at `nums[i]`.
5. After the array is sorted, iterate again to find the index where the number doesn't match the index (the missing/duplicate number).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$. Even though there is a `while` loop inside a `for` loop, each number is swapped to its correct position at most once. Max swaps is $N-1$.
- **Space Complexity:** $O(1)$ auxiliary space.

## 6. Tiny worked example
Array: `[3, 1, 4, 2]`
- `i=0`, val=3. Target idx=2. Swap `arr[0]` and `arr[2]`. Array: `[4, 1, 3, 2]`.
- `i=0`, val=4. Target idx=3. Swap `arr[0]` and `arr[3]`. Array: `[2, 1, 3, 4]`.
- `i=0`, val=2. Target idx=1. Swap `arr[0]` and `arr[1]`. Array: `[1, 2, 3, 4]`.
- `i=0`, val=1. Correct! Move `i=1`.
- `i=1,2,3` all correct. Done.

## 7. Code (Python, with type hints)
```python
from typing import List

def find_missing_number(nums: List[int]) -> int:
    i, n = 0, len(nums)
    
    # 1. Cyclic Sort
    while i < n:
        j = nums[i] # Target index (assuming range 0 to N)
        if j < n and nums[i] != nums[j]:
            nums[i], nums[j] = nums[j], nums[i] # Swap
        else:
            i += 1
            
    # 2. Find missing
    for i in range(n):
        if nums[i] != i:
            return i
            
    return n
```

## 8. Common mistakes
- Using a `for` loop without adjusting the index. You must use a `while` loop, or explicitly keep checking `i` until it holds the correct value. If you swap and immediately move on, the new value swapped into `i` remains unchecked.
- Infinite loops caused by duplicate numbers. You must check `nums[i] != nums[j]` before swapping.

## 9. 30-second interview answer
"Cyclic sort is an $O(N)$ time, $O(1)$ space sorting algorithm for arrays containing numbers in a strict range from 1 to N. It works by treating the array indices as a hash map and swapping each number directly to its correct index. It's the definitive pattern for finding missing or duplicate numbers in a fixed range."

## 10. 2-minute interview answer
"Whenever an interview problem states 'an array containing numbers in the range 1 to N', it is screaming for a Cyclic Sort. While we could find missing or duplicate numbers using a Hash Set ($O(N)$ space) or by standard sorting ($O(N \log N)$ time), Cyclic Sort achieves the optimal $O(N)$ time and $O(1)$ space. The logic is simple: we iterate through the array, and if the number we are looking at isn't at its correct index, we swap it with the number that currently occupies its correct index. We repeat this at the current position until the correct number arrives, then move to the next position. Because every swap firmly places at least one number into its permanent home, the maximum number of swaps across the entire array is $N-1$, ensuring strictly linear time complexity."

## 11. Follow-ups
- "How do you find all duplicates in an array?" (After Cyclic Sort, any number sitting at the wrong index is a duplicate).

## 12. Deeper questions
- "What if the range is 1 to N, but the array is immutable/read-only?" (Cyclic Sort modifies the array. If immutable, use Floyd's Tortoise and Hare for duplicates, or Binary Search on Answer).

## 13. Related concepts
- **In-place Hashing**: Conceptually identical to Cyclic Sort.

## 14. When it breaks / Edge cases
- Fails completely if the numbers are negative, floats, or wildly out of bounds (e.g., `[1, 100000]`), as the array index mapping is destroyed.

## 15. Comparison with alternative approaches
- **vs Bit Manipulation (XOR):** XOR can find a single missing number in $O(N)$ time and $O(1)$ space without modifying the array, but Cyclic Sort handles multiple missing/duplicate numbers simultaneously.

---
*Where this shows up in ML:* 
Not generally used in ML contexts, purely a DSA optimization trick.
"""

files["20-dsa-patterns/pattern-in-place-reversal.md"] = r"""# Pattern: In-Place Reversal of a LinkedList

## 1. Definition
The In-Place Reversal pattern is a technique used to reverse the links of a Linked List without using extra memory, strictly operating on the existing nodes.

## 2. Intuition
Imagine holding a chain of paperclips. To reverse the direction, you don't buy a new box of paperclips. You detach the second clip, hook it to the first clip facing backwards, detach the third, hook it to the second, and so on. You only need two hands (pointers) to manage the disconnections.

## 3. Why it exists
Reversing a list by copying values to an array, reversing the array, and building a new list takes $O(N)$ extra space. In-place reversal does it in $O(1)$ space, which is an absolute requirement for most Linked List interview questions.

## 4. Mechanics
You need three pointers: `prev`, `curr`, and `next_node`.
1. Initialize `prev = None`, `curr = head`.
2. While `curr` is not None:
   - Save the next node: `next_node = curr.next`.
   - Reverse the link: `curr.next = prev`.
   - Move `prev` forward: `prev = curr`.
   - Move `curr` forward: `curr = next_node`.
3. Return `prev` (the new head).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - One pass through the list.
- **Space Complexity:** $O(1)$ - Only three pointers used.

## 6. Tiny worked example
List: `1 -> 2 -> 3 -> None`. `prev = None`, `curr = 1`.
- Step 1: `next = 2`. `1.next = None`. `prev = 1`, `curr = 2`. (List: `1->None`, `2->3`)
- Step 2: `next = 3`. `2.next = 1`. `prev = 2`, `curr = 3`. (List: `2->1->None`, `3`)
- Step 3: `next = None`. `3.next = 2`. `prev = 3`, `curr = None`.
Return `prev` (3). Final list: `3 -> 2 -> 1 -> None`.

## 7. Code (Python, with type hints)
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    
    while curr:
        next_node = curr.next  # Save next
        curr.next = prev       # Reverse
        prev = curr            # Advance prev
        curr = next_node       # Advance curr
        
    return prev
```

## 8. Common mistakes
- **Losing the rest of the list:** If you do `curr.next = prev` before saving `curr.next` to a temporary variable, the rest of the list is permanently lost to garbage collection.
- Returning `curr` instead of `prev` at the end (since `curr` is None when the loop finishes).

## 9. 30-second interview answer
"The In-Place Reversal pattern uses three pointers (prev, curr, and next) to iteratively reverse the pointers of a Linked List. By saving the next node before overwriting the current node's pointer, we traverse and reverse the list in $O(N)$ time and strictly $O(1)$ space."

## 10. 2-minute interview answer
"Reversing a Linked List in-place is the foundational manipulation technique for node-based structures. The algorithm operates in $O(N)$ time and $O(1)$ space using a sliding window of three pointers. At every step, we cache the 'next' node to prevent losing the chain, repoint the 'current' node backwards to 'prev', and then slide both 'prev' and 'current' forward. This pattern is rarely asked in isolation; it is usually a subroutine. For example, to check if a Linked List is a palindrome, we use Fast/Slow pointers to find the middle, use In-Place Reversal to flip the second half, and then compare the two halves. It's also the core logic for reversing sub-lists, like 'Reverse Nodes in k-Group'."

## 11. Follow-ups
- "How do you reverse only a sub-list (e.g., from position M to N)?" (Traverse to M-1, save it as `before_M`, run the standard reversal loop $N-M$ times, then reconnect `before_M` to the new head, and the original M node to the rest of the list).

## 12. Deeper questions
- "Can you reverse a list recursively?" (Yes. `head.next.next = head; head.next = None`. It takes $O(N)$ space on the call stack, so iterative is strictly better for memory).

## 13. Related concepts
- **Fast & Slow Pointers**: Often combined with reversal (e.g., Palindrome Linked List).

## 14. When it breaks / Edge cases
- Null heads (`head is None`) or single-node lists. The standard logic handles these flawlessly without extra `if` statements.

## 15. Comparison with alternative approaches
- **vs Array copy:** Creating an array takes $O(N)$ memory, which fails the strict $O(1)$ requirement of these problems.

---
*Where this shows up in ML:* 
Not applicable.
"""

files["20-dsa-patterns/pattern-tree-bfs-dfs.md"] = r"""# Pattern: Tree BFS & DFS

## 1. Definition
Tree BFS (Breadth-First Search) explores a tree level-by-level using a Queue. Tree DFS (Depth-First Search) explores a tree branch-by-branch using Recursion (or a Stack).

## 2. Intuition
- **BFS:** Pouring water on the root of a tree. The water fills the top level completely before dripping down to the next level.
- **DFS:** A rat in a maze. It runs as fast and deep as possible down a single hallway until it hits a dead end, then backtracks.

## 3. Why it exists
Trees are non-linear; you can't just `for i in range(N)`. We need structured algorithms to visit every node. BFS exists to find shortest paths or level-order structure. DFS exists to solve problems requiring full branch context (like path sums) or deep state evaluation.

## 4. Mechanics
- **BFS:** Uses a `collections.deque`. 
  - Push root. Loop while Queue is not empty.
  - *Level-order trick:* `size = len(queue)`. Loop `size` times, popping nodes and pushing children. This isolates exactly one level per outer loop iteration.
- **DFS:** Uses Recursion. 
  - Pre-order (Node, Left, Right)
  - In-order (Left, Node, Right) - Yields sorted order for BSTs.
  - Post-order (Left, Right, Node) - Used when node processing depends on children (e.g., calculating tree height).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ for both. Every node is visited once.
- **Space Complexity:** 
  - BFS: $O(W)$, where $W$ is max width of the tree (can be $N/2$ for a perfect tree).
  - DFS: $O(H)$, where $H$ is max height of the tree (recursion stack, $O(N)$ worst case, $O(\log N)$ balanced).

## 6. Tiny worked example
Tree: `1` with children `2, 3`.
- BFS: Queue `[1]`. Pop `1`, push `2, 3`. Queue `[2, 3]`. Pop `2`. Pop `3`. Order: 1, 2, 3.
- DFS (Pre-order): Visit `1`. Recurse left to `2`. Visit `2`. Recurse right to `3`. Visit `3`. Order: 1, 2, 3.

## 7. Code (Python, with type hints)
```python
from collections import deque
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# BFS (Level Order)
def tree_bfs(root: Optional[TreeNode]) -> list:
    if not root: return []
    queue = deque([root])
    levels = []
    
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        levels.append(current_level)
    return levels

# DFS (Post-order example: Max Depth)
def max_depth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    return max(left_depth, right_depth) + 1
```

## 8. Common mistakes
- **BFS:** Forgetting to capture `level_size = len(queue)` before popping, destroying the level-by-level isolation.
- **DFS:** Forgetting to return a base case (e.g., `return 0` if `not root`), causing `TypeError` on addition.

## 9. 30-second interview answer
"BFS explores trees level-by-level using a Queue, taking $O(W)$ space, making it perfect for finding shortest paths or level structures. DFS explores branch-by-branch using recursion, taking $O(H)$ space, making it ideal for path sums, subtree evaluations, and deep explorations."

## 10. 2-minute interview answer
"BFS and DFS are the fundamental paradigms for Tree manipulation. BFS is implemented iteratively using a Double-Ended Queue. By snapping the length of the queue at the start of each while-loop iteration, we can process the tree precisely level-by-level, which is exactly how we solve 'Binary Tree Right Side View' or 'Level Order Traversal'. Its space complexity scales with the tree's maximum width. DFS is typically implemented recursively, leveraging the call stack. Its space complexity scales with tree height. DFS offers three variations: Pre-order for copying trees, In-order for extracting sorted arrays from BSTs, and Post-order—which is arguably the most powerful—for bottom-up calculations where a parent's state depends entirely on the results of its left and right children, like calculating Tree Diameter."

## 11. Follow-ups
- "When would BFS cause Memory Limit Exceeded?" (On a massive, extremely wide, perfect binary tree, the leaf level contains $N/2$ nodes. If memory is tight, DFS is safer as it only takes $\log N$ space on a balanced tree).

## 12. Deeper questions
- "How do you do In-Order DFS iteratively?" (Use a `while` loop and an explicit Stack. Traverse left until `None`, pop, process, and step right).

## 13. Related concepts
- **Graph BFS/DFS**: Identical logic, but requires a `visited` set.

## 14. When it breaks / Edge cases
- Python's default recursion limit is 1000. If the tree is completely unbalanced (like a linked list of 2000 nodes), DFS will trigger a `RecursionError`.

## 15. Comparison with alternative approaches
- **Morris Traversal:** Achieves $O(N)$ time and strict $O(1)$ space by temporarily modifying the tree's leaf pointers to act as return paths, bypassing both Queues and Stacks.

---
*Where this shows up in ML:* 
Decision Trees (like Random Forests/XGBoost) evaluate predictions by traversing the tree based on feature splits, which is essentially an optimized path traversal (DFS).
"""

files["20-dsa-patterns/pattern-subsets-backtracking.md"] = r"""# Pattern: Subsets / Backtracking

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
"""

files["20-dsa-patterns/pattern-topological-sort.md"] = r"""# Pattern: Topological Sort

## 1. Definition
Topological Sort is a pattern used to find a linear ordering of elements that have complex dependencies on one another, ensuring that no element is processed before its prerequisites. It strictly applies to Directed Acyclic Graphs (DAGs).

## 2. Intuition
Imagine getting dressed in the morning. You must put on your socks before your shoes. You must put on your underwear before your pants. Topological sort takes all these individual rules and spits out a valid, chronological sequence (Underwear -> Pants -> Socks -> Shoes) so you don't end up putting your underwear over your pants.

## 3. Why it exists
Problems like task scheduling, course prerequisites, and package manager dependencies present pairs of local constraints (A must precede B). We need a global algorithm that merges all local constraints into one master timeline while mathematically proving whether a timeline is even possible (i.e., no cycles).

## 4. Mechanics (Kahn's Algorithm)
1. **Initialization:** Build an Adjacency List and an `in_degree` array (tracking how many prerequisites each node has).
2. **Queue:** Push all nodes with `in_degree == 0` (no prerequisites) into a Queue.
3. **Process:** Pop a node, add it to the sorted output, and iterate through its neighbors.
4. **Decrement:** For each neighbor, decrement its `in_degree` by 1 (since you just completed one of its prerequisites).
5. **Enqueue:** If a neighbor's `in_degree` reaches 0, push it to the Queue.
6. **Cycle Check:** If the output list length != total nodes, a cycle exists.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V + E)$ where $V$ is tasks and $E$ is dependencies.
- **Space Complexity:** $O(V + E)$ for the Adjacency List, In-Degree array, and Queue.

## 6. Tiny worked example
Courses: 0, 1, 2. Prerequisites: `[1,0]` (0 before 1), `[2,0]` (0 before 2).
- `in_degree`: 0:0, 1:1, 2:1.
- Queue: `[0]`.
- Pop 0. Output: `[0]`. Neighbors: 1, 2.
- 1's `in_degree` becomes 0. Push 1.
- 2's `in_degree` becomes 0. Push 2.
- Pop 1, Pop 2. Output: `[0, 1, 2]`.

## 7. Code (Python, with type hints)
```python
from collections import deque, defaultdict
from typing import List

def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    # Build Graph
    for dest, src in prerequisites:
        graph[src].append(dest)
        in_degree[dest] += 1
        
    # Start with nodes having no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    top_order = []
    
    # Process
    while queue:
        node = queue.popleft()
        top_order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # Cycle detection
    return top_order if len(top_order) == numCourses else []
```

## 8. Common mistakes
- **Graph Building Direction:** Reversing the edge direction. If taking course $A$ is a prerequisite for $B$, the edge must be $A \rightarrow B$, not the other way around.
- **Skipping Isolated Nodes:** If a node has no edges at all, its `in_degree` is 0. It must be included in the initial Queue.

## 9. 30-second interview answer
"The Topological Sort pattern is used to linearly order items that have dependencies. Using Kahn's Algorithm, we track the 'in-degree' of every node, process nodes with zero dependencies via a Queue, and sequentially unlock their neighbors. It runs in $O(V+E)$ time and inherently detects cyclic impossibilities."

## 10. 2-minute interview answer
"Whenever an interview question asks to 'find a valid order', 'schedule tasks', or 'compile dependencies', it is a Topological Sort problem on a Directed Acyclic Graph. The most robust implementation is Kahn's Algorithm using BFS. We first translate the dependencies into an Adjacency List while tracking the 'in-degree'—the number of prerequisites—for every node. We push all independent nodes (in-degree 0) into a Queue. As we process each node, we simulate 'completing' that task by decrementing the in-degree of its neighbors. Once a neighbor's in-degree hits 0, it is fully unlocked and pushed to the Queue. The beauty of Kahn's is its built-in cycle detection: if there is a mutual dependency (A needs B, B needs A), they will never reach an in-degree of 0, and the final output array will be shorter than the total number of nodes."

## 11. Follow-ups
- "Can you solve this with DFS?" (Yes. Traverse to the deepest leaf, mark it visited, push it to a Stack. Return the reversed Stack. Requires a 3-state visited array: Unvisited, Visiting, Visited, to detect cycles).

## 12. Deeper questions
- "How do you find if a sequence of words constitutes a valid 'Alien Dictionary'?" (Compare adjacent words to find the first differing letter, treat that as a directed edge, build the graph, and Topological Sort it).

## 13. Related concepts
- **Graphs**: Topological Sort is a graph algorithm.
- **BFS**: The engine of Kahn's Algorithm.

## 14. When it breaks / Edge cases
- Disconnected components or isolated tasks. Kahn's handles them perfectly because they initialize with `in_degree == 0` and are instantly processed.

## 15. Comparison with alternative approaches
- **DFS vs Kahn's:** Kahn's (BFS) is slightly easier to reason about for cycle detection and can easily process tasks in parallel groupings (everything in the queue at one level can be executed simultaneously).

---
*Where this shows up in ML:* 
The order of operations in PyTorch's execution graph is determined by a topological sort.
"""

files["20-dsa-patterns/pattern-union-find.md"] = r"""# Pattern: Union Find

## 1. Definition
The Union-Find pattern utilizes the Disjoint Set data structure to efficiently track and merge connected components in a network, typically to detect cycles or dynamically group elements.

## 2. Intuition
Imagine a room full of strangers. When two people shake hands, they become part of a "network". Instead of everyone remembering everyone else in their network (which takes massive memory), everyone just remembers one "Boss". When two networks merge, the Boss of Network A shakes hands with the Boss of Network B. Now, to check if you and I are in the same network, we just trace up our chains of command and see if we have the same ultimate Boss.

## 3. Why it exists
If edges in a graph are given to you one by one (a stream), using DFS to constantly recalculate "are these two nodes connected?" takes $O(V+E)$ every single time. Union-Find does this in $O(1)$ amortized time.

## 4. Mechanics
1. **Initialize:** An array `parent` where every node is its own boss (`parent[i] = i`).
2. **Find(x):** Trace `parent[x]` up to the root.
   - *Path Compression:* On the way back down, make every node point directly to the root to flatten the tree.
3. **Union(x, y):** Find the roots of `x` and `y`. If they are different, make one root point to the other.
   - *Union by Rank:* Attach the smaller tree to the root of the taller tree to keep the overall tree shallow.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\alpha(N))$ per operation, where $\alpha$ is the inverse Ackermann function. Practically $O(1)$.
- **Space Complexity:** $O(N)$ for the `parent` and `rank` arrays.

## 6. Tiny worked example
Nodes 1, 2, 3.
- `Union(1, 2)`: 1 becomes boss of 2. `parent = {1:1, 2:1, 3:3}`
- Check `Find(2) == Find(3)`: `Find(2)->1`, `Find(3)->3`. Not connected.
- `Union(2, 3)`: Find(2)=1, Find(3)=3. Make 1 boss of 3. `parent = {1:1, 2:1, 3:1}`
- Check `Find(2) == Find(3)`: Both return 1. Connected!

## 7. Code (Python, with type hints)
```python
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False # Already connected (Cycle!)
            
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            
        return True
```

## 8. Common mistakes
- **Ignoring Path Compression:** Without `self.parent[x] = self.find(self.parent[x])`, the trees become unbalanced linked lists, turning $O(1)$ operations into $O(N)$.
- When doing `Union(x, y)`, setting `parent[y] = x` directly instead of setting `parent[root_y] = root_x`. You MUST link the roots, not the child nodes!

## 9. 30-second interview answer
"Union-Find is a pattern for dynamic connectivity. It groups elements into disjoint sets and can instantly answer if two elements are connected. By using Path Compression to flatten the tree during a Find, and Union by Rank to attach trees optimally, it achieves near $O(1)$ amortized time per operation."

## 10. 2-minute interview answer
"The Union-Find pattern is the optimal choice for problems involving dynamic connectivity, grouping items into sets, or detecting cycles in undirected graphs. It bypasses the overhead of heavy BFS/DFS traversals by maintaining a flat array of 'parent' pointers representing tree structures. The power of Union-Find comes from two optimizations. First, Path Compression: whenever we perform a Find, we recursively re-point every node along the path directly to the root, permanently squashing the tree's height. Second, Union by Rank: we explicitly track tree heights and always attach smaller trees under larger ones. Combined, these yield an amortized time complexity of $O(\alpha(N))$, bounded by the Inverse Ackermann function, which is effectively $O(1)$. It is the mathematical backbone of Kruskal's Minimum Spanning Tree algorithm."

## 11. Follow-ups
- "How do you count the number of connected components?" (Count how many nodes have `parent[i] == i`. Every root is exactly one component).

## 12. Deeper questions
- "Can Union-Find handle edge removal?" (No. It fundamentally only merges. If a problem requires edge removal, process the queries in reverse order (time-travel backwards), turning 'removals' into 'unions').

## 13. Related concepts
- **Kruskal's Algorithm**: Relies entirely on Union-Find.
- **Graph Connected Components**: The primary use case.

## 14. When it breaks / Edge cases
- Fails on Directed Graphs (since "connectivity" implies symmetry in Union-Find, but directed edges are one-way).

## 15. Comparison with alternative approaches
- **vs BFS/DFS:** If the graph is fully given upfront and never changes, a single $O(V+E)$ BFS is fine. If edges arrive dynamically (streaming), Union-Find is exponentially faster.

---
*Where this shows up in ML:* 
Used in image segmentation (like the Felzenszwalb-Huttenlocher algorithm) to quickly group adjacent pixels of similar color into cohesive objects.
"""

files["20-dsa-patterns/pattern-matching-mapping-problems-to-patterns.md"] = r"""# Pattern Matching: Mapping Problems to Patterns

## 1. Definition
This is a meta-skill for coding interviews: reading a plain-English prompt, identifying algorithmic "keywords" or constraints, and instantly mapping them to the correct DSA pattern.

## 2. Intuition
You are a doctor diagnosing a patient. You don't try every medicine randomly. You listen to symptoms: "Cough, fever, loss of taste." Diagnosis: COVID-19. Treatment: Antivirals. In interviews, symptoms are constraints: "Sorted array, $O(\log N)$." Diagnosis: Binary Search. Treatment: Left/Right pointers.

## 3. Why it exists
Interviewers intentionally disguise classic algorithms behind wordy stories. Without pattern matching, candidates waste 20 minutes trying to invent a novel algorithm. With it, candidates derive the optimal algorithm in 60 seconds.

## 4. Mechanics (Symptom -> Pattern)
- **"Sorted Array" + "Target Sum"**: Two Pointers.
- **"Sorted Array" + "$O(\log N)$"**: Binary Search.
- **"Subarray / Substring" + "Max/Min Length"**: Sliding Window.
- **"Top K / Kth Largest"**: Heap / Priority Queue.
- **"Next Greater Element"**: Monotonic Stack.
- **"Combinations / Permutations / Subsets"**: Backtracking.
- **"All possible ways / Maximize/Minimize (with overlap)"**: Dynamic Programming.
- **"Connected Components / Network"**: BFS/DFS or Union-Find.
- **"Task Scheduling / Prerequisites"**: Topological Sort.
- **"Range from 1 to N" + "Missing/Duplicate"**: Cyclic Sort.
- **"Overlapping Times / Meetings"**: Merge Intervals.

## 5. Complexity (Time & Space)
- N/A

## 6. Tiny worked example
Prompt: *Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be. You must write an algorithm with $O(\log N)$ runtime.*
- Symptoms: "Sorted Array", "Target value", "$O(\log N)$".
- Diagnosis: Binary Search.

## 7. Code (Python, with type hints)
*(N/A - This is a conceptual mapping skill)*

## 8. Common mistakes
- **Ignoring Constraints:** Missing $N \le 20$ (screams $O(2^N)$ Backtracking) or $N \le 10^5$ (screams $O(N)$ or $O(N \log N)$, making $O(N^2)$ DP impossible).
- **False Positives:** Seeing "maximize" and assuming DP, when the problem might have the Greedy Choice Property (e.g., Interval Scheduling).

## 9. 30-second interview answer
"I map problems to patterns by identifying structural keywords and analyzing time complexity constraints. For example, 'Top K' triggers Heaps, 'contiguous subarrays' triggers Sliding Window, and $O(\log N)$ on a sorted array strictly points to Binary Search."

## 10. 2-minute interview answer
"The most critical skill in an interview is translating the prompt's constraints into a known architectural pattern. My thought process evaluates three things: the data structure, the mathematical keywords, and the Big-O bounds. If I see a string and the word 'substring', I immediately set up a Sliding Window. If the problem asks for 'all possible combinations', I know it's an $O(2^N)$ Backtracking problem. If it asks to 'minimize the maximum' across an array, I use Binary Search on Answer. Constraints give it away: an input size of $N=10^6$ means I can only afford an $O(N)$ algorithm, immediately ruling out nested loops or 2D DP. By applying this heuristic mapping, I spend my time writing clean code instead of struggling with algorithm design."

## 11. Follow-ups
- "What if multiple patterns seem to apply?" (Choose the one that satisfies the optimal time complexity. E.g., 'Target Sum' can be done via Hash Map $O(N)$ time/$O(N)$ space, or Two Pointers if sorted $O(N)$ time/$O(1)$ space. Mention both, implement the best).

## 12. Deeper questions
- "How do you identify a Monotonic Queue (Deque) problem?" (It is the exact intersection of 'Sliding Window' and 'Max/Min Element'—e.g., Sliding Window Maximum).

## 13. Related concepts
- **All DSA Patterns**

## 14. When it breaks / Edge cases
- FAANG 'Hard' problems often require *combining* two patterns (e.g., Binary Search over a Sliding Window validation function).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Translating a business problem ("we need to predict house prices") to an ML architecture (Regression vs Classification, tabular vs text).
"""

files["17-data-structures/deque.md"] = r"""# Deque (Double-Ended Queue)

## 1. Definition
A Deque (pronounced "deck") is a linear data structure that allows insertion and deletion of elements from both ends (front and back) in $O(1)$ time.

## 2. Intuition
Think of a queue of people at a theme park, but with a VIP rule. Normal people enter the back and leave from the front. But VIPs can cut directly to the front, and people who get tired of waiting can leave from the back. It operates as both a Stack and a Queue simultaneously.

## 3. Why it exists
An Array/List takes $O(N)$ time to insert/delete at the front because all elements must shift. A Deque solves this, providing $O(1)$ operations at both ends, making it the perfect underlying structure for Sliding Window Maximums and BFS algorithms.

## 4. Mechanics
- Typically implemented using a Doubly Linked List or a Circular Array.
- **Operations:** `append()` (add to right), `appendleft()` (add to left), `pop()` (remove from right), `popleft()` (remove from left).
- Unlike Python lists, Deques do not require massive memory reallocations for shifting.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(1)$ for insert/delete at both ends. $O(N)$ for random access/indexing in the middle.
- **Space Complexity:** $O(N)$.

## 6. Tiny worked example
```python
from collections import deque
dq = deque([1, 2])
dq.append(3)      # [1, 2, 3] (Queue behavior)
dq.appendleft(0)  # [0, 1, 2, 3]
dq.pop()          # 3 (Stack behavior) -> [0, 1, 2]
dq.popleft()      # 0 (Queue behavior) -> [1, 2]
```

## 7. Code (Python, with type hints)
```python
from collections import deque
from typing import List

# Classic Deque problem: Sliding Window Maximum
def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    dq = deque()  # Stores INDICES of array elements
    res = []
    
    for i in range(len(nums)):
        # 1. Remove indices that are out of the current window
        if dq and dq[0] < i - k + 1:
            dq.popleft()
            
        # 2. Remove smaller elements from back (they can never be the max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
            
        # 3. Add current element
        dq.append(i)
        
        # 4. Record max (element at front of deque)
        if i >= k - 1:
            res.append(nums[dq[0]])
            
    return res
```

## 8. Common mistakes
- Using a standard Python `list` as a queue (`list.pop(0)`). This is an immediate red flag in interviews because it runs in $O(N)$ time, turning an $O(N)$ BFS into an $O(N^2)$ disaster.
- Using a Deque for heavy random access (`dq[500]`), which takes $O(N)$ time in linked-list implementations.

## 9. 30-second interview answer
"A Deque is a Double-Ended Queue that supports $O(1)$ insertions and deletions from both the front and the back. In Python, it is implemented via `collections.deque` and is mandatory for BFS graph traversals and optimal Monotonic Queue problems like Sliding Window Maximum."

## 10. 2-minute interview answer
"A Deque bridges the gap between Stacks and Queues. By implementing it internally as a doubly-linked list or circular buffer, it allows strictly $O(1)$ time complexity for adding or removing elements at either boundary. In Python, candidates often make the fatal mistake of using a standard array with `.pop(0)` for BFS, destroying their time complexity via $O(N)$ memory shifts. The Deque's most powerful algorithmic application is the Monotonic Queue pattern, used in problems like 'Sliding Window Maximum'. By popping elements from the right that violate the monotonic property, and popping expired indices from the left, a Deque calculates the maximum of a moving window in perfectly linear $O(N)$ time."

## 11. Follow-ups
- "Are Deques thread-safe in Python?" (Yes, the `.append()` and `.pop()` operations on Python's `collections.deque` are thread-safe and atomic).

## 12. Deeper questions
- "How would you implement a Deque using an Array instead of a Linked List?" (Use a Circular Buffer with 'head' and 'tail' pointers that wrap around the array length using modulo arithmetic).

## 13. Related concepts
- **Queues**: For BFS.
- **Sliding Window**: For Monotonic Deques.

## 14. When it breaks / Edge cases
- Fails if you need fast $O(1)$ random access in the middle of the collection (use a standard Array instead).

## 15. Comparison with alternative approaches
- **vs List (Array):** Lists are $O(1)$ for right-side operations but $O(N)$ for left-side operations. Deques are $O(1)$ for both.

---
*Where this shows up in ML:* 
Replay buffers in Reinforcement Learning (DQN) are often implemented using fixed-size Deques. When the buffer is full, appending a new experience automatically drops the oldest one from the front in $O(1)$ time.
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch C - Sub-pass 2 Complete")
