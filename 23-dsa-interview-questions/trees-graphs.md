# Trees & Graphs Interview Questions

---

## 1. Maximum Depth of Binary Tree

### 1. Restate the Problem
Find the maximum depth (number of nodes along the longest path from the root down to the farthest leaf node) of a binary tree.

### 2. Clarify Edge Cases
- Empty tree? Return 0.

### 3. Brute Force Approach
N/A. This is a basic traversal problem.

### 4. Key Insight
The max depth of a tree is `1 + max(depth(left), depth(right))`. This naturally suggests a recursive Depth-First Search (DFS).

### 5. Optimized Approach
Recursively call the function on the left and right children. Base case is `node is None` returning 0. Return 1 + the max of the two recursive calls.

### 6. Justification
Time: $O(N)$ since we visit every node exactly once. Space: $O(H)$ where $H$ is the height of the tree (recursion stack). Worst case $O(N)$ for skewed tree, best case $O(\log N)$ for balanced tree.

### 7. Code (Python)
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(root: TreeNode) -> int:
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

### 8. Dry Run
`root = [3,9,20,None,None,15,7]`
- maxDepth(3) calls maxDepth(9) and maxDepth(20)
- maxDepth(9) -> returns 1
- maxDepth(20) calls maxDepth(15) and maxDepth(7) -> returns 1 + max(1,1) = 2
- maxDepth(3) returns 1 + max(1, 2) = 3

### 9. Edge Cases Handled
Empty tree triggers `if not root` instantly.

### 10. Follow-ups
- "Can you do it iteratively?" -> Use BFS (level order traversal) with a queue. Return the number of levels.

### 11. Related Problems
Minimum Depth of Binary Tree, Diameter of Binary Tree.

---

## 2. Invert Binary Tree

### 1. Restate the Problem
Given the root of a binary tree, invert the tree (swap every left and right child), and return its root.

### 2. Clarify Edge Cases
- Empty tree? Return `None`.

### 3. Brute Force Approach
N/A.

### 4. Key Insight
To invert a tree, you just need to swap the left and right pointers of every single node in the tree. This can be done via DFS or BFS.

### 5. Optimized Approach
Recursive DFS. Base case: if root is None, return None. Swap `root.left` and `root.right`. Then recursively call the function on `root.left` and `root.right`. Return `root`.

### 6. Justification
Time: $O(N)$ (visit every node once). Space: $O(H)$ for recursion stack.

### 7. Code (Python)
```python
def invertTree(root: TreeNode) -> TreeNode:
    if not root:
        return None
        
    # Swap children
    root.left, root.right = root.right, root.left
    
    # Recursively invert subtrees
    invertTree(root.left)
    invertTree(root.right)
    
    return root
```

### 8. Dry Run
`root = [2, 1, 3]`
- invertTree(2): swaps left/right. left is now 3, right is 1.
- invertTree(3): base cases hit on its children. returns 3.
- invertTree(1): base cases hit on its children. returns 1.
- returns 2. Tree is `[2, 3, 1]`.

### 9. Edge Cases Handled
Empty subtrees swap perfectly (None gets moved to the other side).

### 10. Follow-ups
- "Can you do it iteratively?" -> Yes, use a standard BFS queue or DFS stack. When popping a node, swap its children, then push non-None children to the queue/stack.

### 11. Related Problems
Symmetric Tree, Same Tree.

---

## 3. Number of Islands (Graph BFS/DFS)

### 1. Restate the Problem
Given an $M \times N$ 2D binary grid `grid` which represents a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

### 2. Clarify Edge Cases
- Empty grid? Return 0.
- Diagonals count? No, only horizontal/vertical.

### 3. Brute Force Approach
N/A.

### 4. Key Insight
This is a Connected Components problem in a graph. Whenever we find a '1', we have found a new island. We must then traverse (DFS or BFS) the entire island and mark it as visited (or turn it to '0') so we don't count it again.

### 5. Optimized Approach
Iterate through every cell in the grid. If it's a '1', increment the island count and call a DFS function to sink the island (turn all connected '1's to '0's).

### 6. Justification
Time: $O(M \times N)$ because we visit every cell at most twice (once in loop, once in DFS). Space: $O(M \times N)$ in the worst case (the whole grid is one island, recursion stack goes deep).

### 7. Code (Python)
```python
from typing import List

def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0
        
    def dfs(r, c):
        if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] == '0':
            return
            
        grid[r][c] = '0' # Sink the island
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
                
    return count
```

### 8. Dry Run
`grid = [["1","1","0"], ["0","1","0"], ["1","0","0"]]`
- (0,0) is '1'. count=1. dfs(0,0) sinks (0,0), (0,1), (1,1).
- Loop continues. (0,1) is now '0'.
- (2,0) is '1'. count=2. dfs(2,0) sinks (2,0).
- Loop finishes. Return 2.

### 9. Edge Cases Handled
Out-of-bounds correctly handled at the top of DFS. Modifying grid directly avoids needing a `visited` set.

### 10. Follow-ups
- "What if you cannot modify the original grid?" -> Use a `visited` boolean matrix of the same size.

### 11. Related Problems
Max Area of Island, Clone Graph.

---

## 4. Course Schedule (Topological Sort)

### 1. Restate the Problem
There are `numCourses` courses labeled `0` to `numCourses - 1`. Given an array `prerequisites` where `prerequisites[i] = [a, b]` indicates you must take course `b` first to take course `a`, return true if you can finish all courses.

### 2. Clarify Edge Cases
- Unconnected courses? Valid.
- Essentially: Does the directed graph have a cycle?

### 3. Brute Force Approach
N/A.

### 4. Key Insight
This asks for cycle detection in a Directed Graph. Can be solved using DFS (checking for back-edges) or Kahn's Algorithm (Topological Sort via BFS).

### 5. Optimized Approach (Kahn's Algorithm)
1. Build an adjacency list and an in-degree array.
2. Queue all nodes with in-degree 0 (courses with no prerequisites).
3. While queue is not empty, pop node, increment a `courses_taken` counter. Reduce in-degree of its neighbors. If a neighbor hits 0, add to queue.
4. Return True if `courses_taken == numCourses`.

### 6. Justification
Time: $O(V + E)$ where $V$ is courses and $E$ is prerequisites. Space: $O(V + E)$ for adjacency list and queue.

### 7. Code (Python)
```python
from collections import deque, defaultdict
from typing import List

def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    adj = defaultdict(list)
    indegree = [0] * numCourses
    
    for crs, pre in prerequisites:
        adj[pre].append(crs)
        indegree[crs] += 1
        
    q = deque([i for i in range(numCourses) if indegree[i] == 0])
    count = 0
    
    while q:
        curr = q.popleft()
        count += 1
        for neighbor in adj[curr]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                q.append(neighbor)
                
    return count == numCourses
```

### 8. Dry Run
`numCourses = 2, pre = [[1,0], [0,1]]`
- in-degree: `[1, 1]`
- queue: `[]` (empty)
- Loop doesn't run. `count = 0 != 2`. Returns False (Cycle exists).

### 9. Edge Cases Handled
Empty prerequisites: all in-degrees are 0, everything added to queue, count reaches `numCourses`, True.

### 10. Follow-ups
- "Return the actual ordering?" -> Just append `curr` to a list and return the list (Course Schedule II).

### 11. Related Problems
Course Schedule II, Alien Dictionary.
