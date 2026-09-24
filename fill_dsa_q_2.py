import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (DSA Qs)"')

wc("23-dsa-interview-questions/stacks-queues.md", r"""# Stacks & Queues Interview Questions

---

## 1. Valid Parentheses

### 1. Restate the Problem
Given a string containing just the characters `'(', ')', '{', '}', '[' and ']'`, determine if the input string is valid (every open bracket is closed by the same type of bracket in the correct order).

### 2. Clarify Edge Cases
- Empty string? Valid.
- String with only open or only close brackets? Invalid.

### 3. Brute Force Approach
Repeatedly replace `()`, `{}`, and `[]` with empty strings until no more replacements can be made. If the string becomes empty, it's valid. Time: $O(N^2)$.

### 4. Key Insight
A Stack perfectly models this LIFO (Last-In-First-Out) requirement. The last open bracket seen must be the first one closed.

### 5. Optimized Approach
Iterate through the string. If we see an open bracket, push it to the stack. If we see a close bracket, pop from the stack and check if it matches the corresponding open bracket. If the stack is empty when seeing a close bracket, or if the stack is not empty at the end, it's invalid.

### 6. Justification
Time: $O(N)$ since we iterate through the string once and push/pop take $O(1)$. Space: $O(N)$ for the stack in the worst case (all open brackets).

### 7. Code (Python)
```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            # Pop element if stack is not empty, else use dummy value
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack
```

### 8. Dry Run
`s = "{[]}"`
- '{' -> stack = ['{']
- '[' -> stack = ['{', '[']
- ']' -> pop '[', matches map[']']. stack = ['{']
- '}' -> pop '{', matches map['}']. stack = []
- Returns True.

### 9. Edge Cases Handled
- `]`: stack is empty, pops `#`, map[']'] is `[`, False.
- `[`: ends with stack not empty, `not stack` evaluates to False.

### 10. Follow-ups
- "What if there are other characters (letters) in the string?" -> Just ignore them and only process brackets.

### 11. Related Problems
Generate Parentheses, Minimum Remove to Make Valid Parentheses.

---

## 2. Min Stack

### 1. Restate the Problem
Design a stack that supports `push`, `pop`, `top`, and retrieving the minimum element in constant time ($O(1)$).

### 2. Clarify Edge Cases
- Popping an empty stack? Assume valid operations per constraints.
- Duplicate minimums? Should handle fine.

### 3. Brute Force Approach
Standard stack. When `getMin` is called, iterate through the entire stack to find the minimum. Time: $O(N)$ for `getMin`, $O(1)$ for others.

### 4. Key Insight
We can't just keep a single `min` variable, because if we pop the minimum, we wouldn't know the *second* minimum. Therefore, we must store the current minimum *at each state of the stack*.

### 5. Optimized Approach
Use two stacks (or store tuples in one stack). The main stack stores values. The `min_stack` stores the minimum value seen so far. When pushing `x`, we push `min(x, min_stack.top())` onto the `min_stack`. When popping, we pop both.

### 6. Justification
Time: $O(1)$ for all operations. Space: $O(N)$ for the extra `min_stack`.

### 7. Code (Python)
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(val, self.min_stack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

### 8. Dry Run
`push(-2), push(0), push(-3), getMin(), pop(), top(), getMin()`
- push -2: stk=[-2], min=[-2]
- push 0: stk=[-2, 0], min=[-2, -2]
- push -3: stk=[-2, 0, -3], min=[-2, -2, -3]
- getMin: returns -3
- pop: stk=[-2, 0], min=[-2, -2]
- top: returns 0
- getMin: returns -2

### 9. Edge Cases Handled
Empty minimum stack on first push handled correctly.

### 10. Follow-ups
- "Can you optimize the space?" -> Yes, instead of storing duplicates in `min_stack`, only push to `min_stack` if `val <= min_stack[-1]`. Pop from `min_stack` only if the popped value equals `min_stack[-1]`.

### 11. Related Problems
Max Stack, Sliding Window Maximum.

---

## 3. Implement Queue using Stacks

### 1. Restate the Problem
Implement a FIFO queue using only two LIFO stacks. Support `push`, `pop`, `peek`, and `empty`.

### 2. Clarify Edge Cases
- All operations valid. No popping empty queues.

### 3. Brute Force Approach
N/A, this is a design problem.

### 4. Key Insight
A stack reverses order. Two stacks reverse the order twice, bringing it back to the original FIFO order.

### 5. Optimized Approach
Maintain `stack_in` and `stack_out`. For `push`, push to `stack_in`. For `pop` or `peek`, if `stack_out` is empty, pop all elements from `stack_in` and push them to `stack_out`. Then pop/peek from `stack_out`.

### 6. Justification
Time: `push` is $O(1)$. `pop`/`peek` is Amortized $O(1)$ (worst case $O(N)$ when moving elements, but each element is moved exactly once). Space: $O(N)$ for the stacks.

### 7. Code (Python)
```python
class MyQueue:
    def __init__(self):
        self.s_in = []
        self.s_out = []

    def push(self, x: int) -> None:
        self.s_in.append(x)

    def _move(self):
        if not self.s_out:
            while self.s_in:
                self.s_out.append(self.s_in.pop())

    def pop(self) -> int:
        self._move()
        return self.s_out.pop()

    def peek(self) -> int:
        self._move()
        return self.s_out[-1]

    def empty(self) -> bool:
        return not self.s_in and not self.s_out
```

### 8. Dry Run
`push(1), push(2), peek(), pop(), empty()`
- push 1: in=[1], out=[]
- push 2: in=[1, 2], out=[]
- peek: move all -> in=[], out=[2, 1]. returns 1
- pop: out pops 1. out=[2]. returns 1
- empty: in and out are not empty (out has 2). returns False

### 9. Edge Cases Handled
Subsequent pushes while `s_out` is full just go to `s_in`, maintaining correct order since they are newer than what is in `s_out`.

### 10. Follow-ups
- "Can you implement a Stack using Queues?" -> Yes, use one Queue, push element, then pop and push all existing elements behind it.

### 11. Related Problems
Implement Stack using Queues.

---

## 4. Daily Temperatures (Monotonic Stack)

### 1. Restate the Problem
Given an array of daily temperatures, return an array where `answer[i]` is the number of days you have to wait after the $i$-th day to get a warmer temperature. If none, keep 0.

### 2. Clarify Edge Cases
- No warmer days? Output 0.

### 3. Brute Force Approach
For each day, scan the rest of the array until a higher temperature is found. Time: $O(N^2)$, Space: $O(1)$.

### 4. Key Insight
We need to find the "next greater element". A Monotonic Decreasing Stack is perfect for this. It stores indices of days waiting for a warmer day.

### 5. Optimized Approach
Iterate through the array. While the current temp is greater than the temp at the index at the top of the stack, we found a warmer day for that past day! Pop it, calculate the difference in indices, and save it in the answer array. Then push the current day's index.

### 6. Justification
Time: $O(N)$ because every index is pushed and popped at most once. Space: $O(N)$ for the stack and output array.

### 7. Code (Python)
```python
from typing import List

def dailyTemperatures(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    ans = [0] * n
    stack = []  # stores indices
    
    for i, t in enumerate(temperatures):
        while stack and t > temperatures[stack[-1]]:
            prev_i = stack.pop()
            ans[prev_i] = i - prev_i
        stack.append(i)
        
    return ans
```

### 8. Dry Run
`T = [73, 74, 75, 71, 69, 72, 76, 73]`
- i=0, T=73: stack=[0]
- i=1, T=74: 74 > T[0](73). pop 0. ans[0] = 1-0 = 1. stack=[1]
- i=2, T=75: 75 > T[1](74). pop 1. ans[1] = 2-1 = 1. stack=[2]
- i=3, T=71: 71 < 75. stack=[2, 3]
- i=4, T=69: 69 < 71. stack=[2, 3, 4]
- i=5, T=72: 72 > T[4](69). pop 4, ans[4]=1. 72 > T[3](71). pop 3, ans[3]=2. stack=[2, 5]

### 9. Edge Cases Handled
Decreasing temperatures just stack up and default 0s remain in `ans`.

### 10. Follow-ups
- N/A.

### 11. Related Problems
Next Greater Element, Largest Rectangle in Histogram.
""")

wc("23-dsa-interview-questions/trees-graphs.md", r"""# Trees & Graphs Interview Questions

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
""")

