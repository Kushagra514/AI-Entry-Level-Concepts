# Pattern: Tree BFS & DFS

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
