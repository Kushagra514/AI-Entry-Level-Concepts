import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + '\n')
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch E)"')

BASE = "/home/kushagra/Interview"

# ── 1. Interval DP ────────────────────────────────────────────────────────────
wc(f"{BASE}/19-dp-deep-dive/interval-dp.md", """
# Interval DP

## 1. Core Idea
dp[i][j] = optimal answer for subarray/subproblem on range [i, j].
Enumerate all split points k in [i, j-1] to combine sub-answers.

## 2. Complexity
O(N³) time, O(N²) space — typical for interval DP.

## 3. Template
```python
n = len(arr)
dp = [[0]*n for _ in range(n)]
for length in range(2, n+1):          # subproblem length
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = float('inf')
        for k in range(i, j):         # split point
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + cost(i,k,j))
```

## 4. Matrix Chain Multiplication
Cost of multiplying chain A[i]…A[j]: dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1].

```python
def matrix_chain(p):
    n = len(p) - 1
    dp = [[0]*n for _ in range(n)]
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i+l-1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n-1]
```

## 5. Burst Balloons (LC 312)
dp[i][j] = max coins bursting all balloons between i and j (exclusive).
Key insight: think of k as the LAST balloon burst in [i+1,j-1].
dp[i][j] = max(dp[i][k] + nums[i]*nums[k]*nums[j] + dp[k][j]) for k in (i+1,j).

```python
def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n):
        for left in range(0, n-length):
            right = left + length
            for k in range(left+1, right):
                dp[left][right] = max(dp[left][right],
                    dp[left][k] + nums[left]*nums[k]*nums[right] + dp[k][right])
    return dp[0][n-1]
```

## 6. Palindrome Partitioning II (LC 132)
Min cuts for palindrome partitioning. Use interval DP to precompute isPalin[i][j].

```python
def minCut(s):
    n = len(s)
    pal = [[False]*n for _ in range(n)]
    for i in range(n): pal[i][i] = True
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i+l-1
            pal[i][j] = (s[i]==s[j]) and (l==2 or pal[i+1][j-1])
    cuts = list(range(-1, n))
    for j in range(1, n):
        for i in range(j+1):
            if pal[i][j]:
                cuts[j+1] = min(cuts[j+1], cuts[i]+1)
    return cuts[n]
```

## 7. Optimal BST
dp[i][j] = min cost of BST for keys i..j with given frequencies.

## 8. Stone Merge
Merge stones[i..j] into one pile: cost = sum(stones[i..j]). dp[i][j] = min total cost.

## 9. Key Insight Pattern
Always add padding sentinels (like burst balloons) when boundaries matter.
Think "what is the LAST operation" rather than the first.

## 10. When Split-Point Enumeration Works
- Problem decomposes into two non-overlapping sub-intervals
- Combining two intervals has a measurable cost
- Optimal substructure holds over intervals

## 11. Space Optimization
Usually not possible due to 2D dependency; store full N×N table.

## 12. Interview Tip
Draw the DP table. Fill diagonals (by length). k loop fills each cell.

## 13. Common Mistakes
- Wrong loop order: must iterate by length, not by i.
- Off-by-one on k range.
- Forgetting base cases: dp[i][i] = 0 or single-element cost.

## 14. Related Problems
Strange Printer (LC 664), Remove Boxes (LC 546), Zuma Game (LC 488).

## 15. Complexity Comparison
| Problem | Time | Space |
|---------|------|-------|
| Matrix Chain | O(N³) | O(N²) |
| Burst Balloons | O(N³) | O(N²) |
| Palindrome Partition | O(N²) | O(N²) |
""")

# ── 2. DP on Trees ────────────────────────────────────────────────────────────
wc(f"{BASE}/19-dp-deep-dive/dp-on-trees.md", """
# DP on Trees

## 1. Core Idea
Post-order DFS: compute child subtree answers first, then combine at parent.
State: dp[node] = some optimal value for the subtree rooted at node.

## 2. Template
```python
def dfs(node, parent):
    result = base_case
    for child in graph[node]:
        if child == parent: continue
        child_val = dfs(child, node)
        result = combine(result, child_val)
    return result
```

## 3. Tree Diameter (LC 543)
At each node, diameter passing through it = left_depth + right_depth.
```python
def diameterOfBinaryTree(root):
    ans = [0]
    def depth(node):
        if not node: return 0
        L, R = depth(node.left), depth(node.right)
        ans[0] = max(ans[0], L + R)
        return 1 + max(L, R)
    depth(root)
    return ans[0]
```

## 4. Max Path Sum (LC 124)
Path can start/end anywhere. At each node, gain = node.val + max(0,left) + max(0,right).
```python
def maxPathSum(root):
    best = [float('-inf')]
    def dp(node):
        if not node: return 0
        l = max(dp(node.left), 0)
        r = max(dp(node.right), 0)
        best[0] = max(best[0], node.val + l + r)
        return node.val + max(l, r)   # only one branch for parent
    dp(root)
    return best[0]
```

## 5. House Robber III (LC 337)
State: (rob_root, skip_root). Can't rob adjacent nodes.
```python
def rob(root):
    def dp(node):
        if not node: return (0, 0)  # (rob, skip)
        lr, ls = dp(node.left)
        rr, rs = dp(node.right)
        rob_cur = node.val + ls + rs
        skip_cur = max(lr, ls) + max(rr, rs)
        return (rob_cur, skip_cur)
    return max(dp(root))
```

## 6. Binary Tree Cameras (LC 968)
State per node: 0=needs cover, 1=has camera, 2=covered no camera.

## 7. Rerooting Technique
Compute dp[root] in O(N), then re-root answers for all nodes in second DFS pass.
Useful when answer for each node as root is needed.

## 8. DP on General Trees (N-ary)
```python
def tree_dp(node, par, graph, vals):
    dp = [0] * 2   # dp[0]=skip, dp[1]=take
    dp[1] = vals[node]
    for child in graph[node]:
        if child == par:
            continue
        c = tree_dp(child, node, graph, vals)
        dp[0] += max(c)
        dp[1] += c[0]   # if we take node, children must be skipped
    return dp
```

## 9. Counting Paths / Subtree Sizes
sz[u] = 1 + sum(sz[child]). Used in centroid decomposition, LCA preprocessing.

## 10. Lowest Common Ancestor (Binary Lifting)
Precompute anc[node][j] = 2^j-th ancestor. dp[node][j] = dp[dp[node][j-1]][j-1].

## 11. DP on Tree + Knapsack
"Select k nodes from subtree" — dp[node][k] = max value with k nodes chosen.
Time: O(N²) with careful merging.

## 12. Interview Pattern
- Identify: what info does parent need from child?
- Return tuple from DFS when multiple states needed.
- Track global answer in a nonlocal/list variable.

## 13. Common Mistakes
- Forgetting to block parent edge in undirected tree DFS.
- Returning wrong value up the recursion (confusing subtree answer vs path answer).

## 14. Complexity
O(N) time and space for most tree DP (single pass DFS).

## 15. Key Problems List
| Problem | State |
|---------|-------|
| Diameter | depth from each node |
| Max Path Sum | max one-sided gain |
| House Robber III | (rob, skip) pair |
| Tree Cameras | 3-state coverage |
| Max Independent Set | (include, exclude) |
""")

# ── 3. DP on Graphs ───────────────────────────────────────────────────────────
wc(f"{BASE}/19-dp-deep-dive/dp-on-graphs.md", """
# DP on Graphs

## 1. Prerequisite: DAG
DP on graphs works cleanly on DAGs (Directed Acyclic Graphs). Cycles require Bellman-Ford or other approaches.

## 2. Topological Order = DP Order
Process nodes in topological order. dp[node] depends only on already-computed predecessors.

## 3. Longest Path in DAG
```python
from collections import defaultdict, deque

def longest_path(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    # Kahn's topo sort
    queue = deque(i for i in range(n) if indegree[i] == 0)
    dp = [0] * n
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            dp[v] = max(dp[v], dp[u] + 1)
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return max(dp)
```

## 4. Counting Paths in DAG
```python
def count_paths(src, dst, graph, memo={}):
    if src == dst: return 1
    if src in memo: return memo[src]
    memo[src] = sum(count_paths(v, dst, graph, memo) for v in graph[src])
    return memo[src]
```

## 5. Memoized DFS (implicit DAG)
LC 329 — Longest Increasing Path in Matrix. Each cell is a node; edge exists if neighbor is larger.
```python
def longestIncreasingPath(matrix):
    m, n = len(matrix), len(matrix[0])
    memo = {}
    def dfs(r, c):
        if (r,c) in memo: return memo[(r,c)]
        best = 1
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0<=nr<m and 0<=nc<n and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        memo[(r,c)] = best
        return best
    return max(dfs(r,c) for r in range(m) for c in range(n))
```

## 6. Shortest Path DP (Bellman-Ford)
dp[v] after k iterations = shortest path using at most k edges. Relax all edges k times.

## 7. Minimum Cost to Reach Destination
LC 787 — Cheapest Flights Within K Stops. dp[k][v] = min cost reaching v in k stops.

## 8. DP + Dijkstra Hybrid
When edge weights are non-negative, Dijkstra order = topo order for shortest path DP.

## 9. Cycle Detection Prevents Naive DP
If graph has cycles, must detect them. Use DFS coloring: white/gray/black.

## 10. State Augmentation
Add extra dimensions to break cycles: dp[node][step], dp[node][remaining_fuel].

## 11. All-Pairs Shortest Path: Floyd-Warshall
```python
def floyd(dist, n):
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```
dp[i][j] through intermediate node k.

## 12. Number of Ways: LC 1976
Count shortest paths in weighted graph. Combine Dijkstra + DP count array.

## 13. Key Interview Questions
- Longest path in DAG → topo sort + DP
- Min cost path with constraints → state = (node, constraint)
- Count paths → memoized DFS on DAG

## 14. Common Mistakes
- Applying DP directly on cyclic graph.
- Wrong topo order (using BFS indegree vs DFS finish time — both work).

## 15. Summary Table
| Problem | Approach | Complexity |
|---------|----------|------------|
| Longest path in DAG | Topo + DP | O(V+E) |
| Shortest path k stops | DP by layers | O(K·E) |
| All pairs shortest | Floyd-Warshall | O(V³) |
| Longest path in matrix | Memoized DFS | O(M·N) |
""")

# ── 4. Bitmask DP ─────────────────────────────────────────────────────────────
wc(f"{BASE}/19-dp-deep-dive/dp-with-bitmasking.md", """
# Bitmask DP

## 1. Core Idea
Represent a subset of N elements as an integer bitmask (bit i = 1 means element i is in set).
State: dp[mask][i] = optimal answer for subset `mask`, currently at node i.

## 2. Complexity
O(2^N · N²) time, O(2^N · N) space. Feasible for N ≤ 20.

## 3. Bit Operations Cheat Sheet
```python
mask | (1<<i)    # add element i
mask & ~(1<<i)   # remove element i
mask & (1<<i)    # check if i in mask
mask ^ (1<<i)    # toggle i
bin(mask).count('1')  # popcount
(mask-1) & mask  # remove lowest set bit
```

## 4. TSP — Traveling Salesman Problem
```python
def tsp(dist, n):
    INF = float('inf')
    dp = [[INF]*n for _ in range(1<<n)]
    dp[1][0] = 0   # start at node 0, mask=0001
    for mask in range(1<<n):
        for u in range(n):
            if dp[mask][u] == INF: continue
            if not (mask >> u & 1): continue
            for v in range(n):
                if mask >> v & 1: continue   # v not yet visited
                nmask = mask | (1<<v)
                dp[nmask][v] = min(dp[nmask][v], dp[mask][u] + dist[u][v])
    full = (1<<n) - 1
    return min(dp[full][v] + dist[v][0] for v in range(n))
```

## 5. Assign Tasks to Workers (LC 1986 style)
dp[mask] = min time to finish subset `mask` of tasks.
Enumerate last completed task and worker assignment.

## 6. Minimum Number of People to Teach (subset DP)
Enumerate all language subsets for teams; dp[mask] = can team cover all queries.

## 7. Partition to K Equal Subset Sums (LC 698)
```python
def canPartitionKSubsets(nums, k):
    total = sum(nums)
    if total % k: return False
    target = total // k
    nums.sort(reverse=True)
    dp = [False] * (1 << len(nums))
    cur_sum = [0] * (1 << len(nums))
    dp[0] = True
    for mask in range(1 << len(nums)):
        if not dp[mask]: continue
        for i, num in enumerate(nums):
            if mask >> i & 1: continue
            nmask = mask | (1<<i)
            if cur_sum[mask] % target + num <= target:
                dp[nmask] = True
                cur_sum[nmask] = cur_sum[mask] + num
    return dp[(1<<len(nums))-1]
```

## 8. Minimum Cost to Connect All Points (not bitmask — Prim's), but if N≤15 use bitmask Steiner tree.

## 9. Counting Hamiltonian Paths
dp[mask][v] = number of paths visiting exactly the nodes in `mask`, ending at v.
Base: dp[1<<v][v] = 1 for all v. Transition same as TSP.

## 10. Profile DP (Broken Profile)
For grid tiling problems: process column by column, mask = state of current column boundary.

## 11. SOS DP (Sum over Subsets)
```python
# dp[mask] = sum of f[sub] for all sub ⊆ mask
for i in range(n):
    for mask in range(1<<n):
        if mask >> i & 1:
            dp[mask] += dp[mask ^ (1<<i)]
```
O(N · 2^N) — useful for AND/OR convolution.

## 12. When to Use Bitmask DP
- N ≤ 20 (usually ≤ 15 for interview)
- Need to track "which elements have been used"
- Assignment / matching / partition problems

## 13. Interview Tips
- Always verify N ≤ 20 before proposing.
- Initialize dp with INF or False carefully.
- Iterate masks in increasing order.

## 14. Common Mistakes
- Visiting node not in mask (check `mask >> u & 1`).
- Forgetting start state initialization.
- Using mutable default argument for memo in Python.

## 15. Complexity Summary
| Problem | N limit | Time |
|---------|---------|------|
| TSP | ≤ 20 | O(2^N · N²) |
| Partition K subsets | ≤ 16 | O(2^N · N) |
| SOS DP | ≤ 20 | O(N · 2^N) |
""")

# ── 5. 2D DP ──────────────────────────────────────────────────────────────────
wc(f"{BASE}/19-dp-deep-dive/2d-dp.md", """
# 2D DP

## 1. Core Idea
State depends on two variables — often two sequences, two indices, or grid position.
dp[i][j] derived from dp[i-1][j], dp[i][j-1], dp[i-1][j-1].

## 2. Unique Paths (LC 62)
```python
def uniquePaths(m, n):
    dp = [[1]*n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]
# Space O(n): dp = [1]*n; for i in 1..m: for j in 1..n: dp[j] += dp[j-1]
```

## 3. Min Path Sum (LC 64)
```python
def minPathSum(grid):
    m, n = len(grid), len(grid[0])
    dp = [row[:] for row in grid]
    for i in range(1, m): dp[i][0] += dp[i-1][0]
    for j in range(1, n): dp[0][j] += dp[0][j-1]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] += min(dp[i-1][j], dp[i][j-1])
    return dp[m-1][n-1]
```

## 4. Longest Common Subsequence (LC 1143)
```python
def lcs(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

## 5. Edit Distance (LC 72)
```python
def editDistance(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
```

## 6. Longest Common Substring
dp[i][j] = length of common substring ending at s[i-1], t[j-1].
```python
if s[i-1]==t[j-1]: dp[i][j] = dp[i-1][j-1]+1
else: dp[i][j] = 0
```

## 7. Distinct Subsequences (LC 115)
dp[i][j] = # ways s[0..i-1] contains t[0..j-1] as subseq.
```python
dp[i][j] = dp[i-1][j] + (dp[i-1][j-1] if s[i-1]==t[j-1] else 0)
```

## 8. Maximal Square (LC 221)
dp[i][j] = side length of largest square with bottom-right at (i,j).
```python
dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1  # if grid[i][j]=='1'
```

## 9. Dungeon Game (LC 174)
Work backwards: dp[i][j] = min health needed entering cell (i,j).

## 10. Space Optimization Pattern
When dp[i][j] depends only on row i-1: use two 1D arrays (prev, curr) or in-place rolling.
LCS and Edit Distance can both be reduced to O(min(M,N)) space.

## 11. Knapsack as 2D DP
dp[i][w] = max value using first i items with capacity w.
```python
for i in range(1, n+1):
    for w in range(W+1):
        dp[i][w] = dp[i-1][w]
        if weights[i-1] <= w:
            dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])
```

## 12. Interleaving String (LC 97)
dp[i][j] = s3[0..i+j-1] is interleaving of s1[0..i-1] and s2[0..j-1].

## 13. Interview Tips
- Always draw the table and fill a 3×3 example by hand.
- Confirm base cases for i=0 and j=0 rows.
- Ask if space optimization is needed.

## 14. Common Mistakes
- Mixing 0-indexed dp with 1-indexed strings.
- Wrong initialization of boundary rows/columns.

## 15. Complexity Reference
| Problem | Time | Space (optimized) |
|---------|------|-------------------|
| Unique Paths | O(M·N) | O(N) |
| LCS | O(M·N) | O(N) |
| Edit Distance | O(M·N) | O(N) |
| Knapsack 0/1 | O(N·W) | O(W) |
""")

# ── 6. OOP Fundamentals ───────────────────────────────────────────────────────
wc(f"{BASE}/21-oop-and-lld/oop-fundamentals.md", """
# OOP Fundamentals

## 1. Four Pillars
Encapsulation, Inheritance, Polymorphism, Abstraction.

## 2. Encapsulation
Bundle data and methods; hide internal state. Use `_` (protected) and `__` (private name-mangling) in Python.
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance          # private
    def deposit(self, amount):
        if amount > 0: self.__balance += amount
    def get_balance(self): return self.__balance
```

## 3. Inheritance
Subclass inherits attributes/methods from superclass. Enables code reuse.
```python
class Animal:
    def __init__(self, name): self.name = name
    def speak(self): raise NotImplementedError
class Dog(Animal):
    def speak(self): return f"{self.name} says Woof"
class Cat(Animal):
    def speak(self): return f"{self.name} says Meow"
```

## 4. Polymorphism
Same interface, different behavior. Works via duck typing in Python.
```python
animals = [Dog("Rex"), Cat("Luna")]
for a in animals: print(a.speak())   # runtime dispatch
```

## 5. Abstraction
Hide complexity; expose only necessary interface. Use `abc.ABC` in Python.
```python
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2
```

## 6. Composition vs Inheritance
Prefer composition ("has-a") over inheritance ("is-a") when behavior varies dynamically.
```python
class Engine:
    def start(self): return "Engine started"
class Car:
    def __init__(self): self.engine = Engine()   # composition
    def drive(self): return self.engine.start()
```

## 7. Method Resolution Order (MRO)
Python uses C3 linearization for multiple inheritance. Check via `ClassName.__mro__`.

## 8. super()
Calls parent class method without hardcoding parent name.
```python
class B(A):
    def __init__(self):
        super().__init__()   # calls A.__init__
```

## 9. Dunder Methods
```python
__init__, __str__, __repr__, __len__, __eq__, __lt__, __hash__
__enter__, __exit__    # context manager
__iter__, __next__     # iterator protocol
```

## 10. Class vs Static vs Instance Methods
```python
class MyClass:
    class_var = 0
    def instance_method(self): ...          # access self
    @classmethod
    def class_method(cls): ...              # access cls
    @staticmethod
    def static_method(): ...               # no self/cls
```

## 11. Properties
Control attribute access with getters/setters without changing API.
```python
class Circle:
    def __init__(self, r): self._r = r
    @property
    def radius(self): return self._r
    @radius.setter
    def radius(self, v):
        if v < 0: raise ValueError
        self._r = v
```

## 12. When to Use Each Pillar
- Encapsulation: always — protect invariants
- Inheritance: strong "is-a" relationships, shallow hierarchies
- Polymorphism: plugin architectures, strategy pattern
- Abstraction: define contracts in libraries/frameworks

## 13. Mixin Pattern
Add behavior without full inheritance hierarchy.
```python
class JSONMixin:
    def to_json(self): import json; return json.dumps(self.__dict__)
class User(JSONMixin, BaseModel): ...
```

## 14. Common Interview Questions
- Explain OOP with a real example.
- Composition vs inheritance tradeoffs.
- How does Python achieve polymorphism (duck typing vs interfaces)?

## 15. Python OOP Pitfalls
- Mutable default class variable shared across instances.
- Forgetting `self` in method signatures.
- Deep inheritance chains → fragile base class problem.
""")

# ── 7. SOLID Principles ───────────────────────────────────────────────────────
wc(f"{BASE}/21-oop-and-lld/solid-principles.md", """
# SOLID Principles

## 1. Overview
S — Single Responsibility, O — Open/Closed, L — Liskov Substitution,
I — Interface Segregation, D — Dependency Inversion.

## 2. Single Responsibility Principle (SRP)
A class should have only ONE reason to change.
```python
# Violation: Invoice handles both data and printing
class Invoice:
    def calculate_total(self): ...
    def print_invoice(self): ...   # unrelated concern
    def save_to_db(self): ...      # another concern

# Fix: separate classes
class Invoice: ...
class InvoicePrinter:
    def print(self, invoice): ...
class InvoiceRepository:
    def save(self, invoice): ...
```

## 3. Open/Closed Principle (OCP)
Open for extension, closed for modification.
```python
# Violation: must edit class to add new discount
class Discount:
    def apply(self, customer, price):
        if customer == 'VIP': return price * 0.8
        if customer == 'Regular': return price * 0.9  # keep adding if/else

# Fix: extend via subclasses
class Discount(ABC):
    @abstractmethod
    def apply(self, price): ...
class VIPDiscount(Discount):
    def apply(self, price): return price * 0.8
```

## 4. Liskov Substitution Principle (LSP)
Subclass instances must be substitutable for superclass without breaking correctness.
```python
# Violation
class Rectangle:
    def set_width(self, w): self.w = w
    def set_height(self, h): self.h = h
    def area(self): return self.w * self.h

class Square(Rectangle):         # Breaks LSP!
    def set_width(self, w): self.w = self.h = w   # unexpected side-effect
```
Fix: don't force Square to inherit from Rectangle. Use separate hierarchy.

## 5. Interface Segregation Principle (ISP)
Clients should not depend on methods they don't use. Split fat interfaces.
```python
# Violation
class Worker(ABC):
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self): ...    # Robot can't eat!

# Fix
class Workable(ABC):
    @abstractmethod
    def work(self): ...
class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class Human(Workable, Eatable): ...
class Robot(Workable): ...
```

## 6. Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules. Both depend on abstractions.
```python
# Violation: high-level class hardcodes low-level detail
class EmailService:
    def send(self, msg): ...
class Notification:
    def __init__(self): self.service = EmailService()  # concrete dependency

# Fix: inject abstraction
class MessageService(ABC):
    @abstractmethod
    def send(self, msg): ...
class EmailService(MessageService):
    def send(self, msg): ...
class Notification:
    def __init__(self, service: MessageService):
        self.service = service
```

## 7. SRP in Practice
Keep classes small. If describing a class requires "and", split it.

## 8. OCP and Strategy Pattern
OCP naturally leads to Strategy/Template Method patterns.

## 9. LSP Formal Definition
If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering correctness.
Behavioral subtypes: preconditions ≤ parent, postconditions ≥ parent, invariants preserved.

## 10. ISP and Python Protocols
Python's `typing.Protocol` enables structural subtyping — class matches protocol if it has required methods, no explicit inheritance needed.

## 11. DIP and Dependency Injection
```python
# DI container / manual injection
notification = Notification(service=SMSService())
```
Frameworks like FastAPI use DI extensively.

## 12. Recognizing Violations in Interviews
- Giant class doing everything → SRP
- Long if/elif chains on type → OCP
- Overriding method to do nothing or raise → LSP
- Empty interface method implementations → ISP
- `new ConcreteClass()` inside business logic → DIP

## 13. SOLID and Testing
DIP makes unit testing easier: inject mocks via constructor.
SRP means each class has focused, testable behavior.

## 14. Common Interview Q
"Design X following SOLID." Start: define abstractions → inject dependencies → split responsibilities.

## 15. Quick Reference
| Principle | Key Question |
|-----------|-------------|
| SRP | Does this class have one reason to change? |
| OCP | Can I add feature without editing existing code? |
| LSP | Can I swap subclass without breaking callers? |
| ISP | Do all clients use all interface methods? |
| DIP | Does high-level code depend on abstractions? |
""")

# ── 8. Design Patterns Overview ───────────────────────────────────────────────
wc(f"{BASE}/21-oop-and-lld/design-patterns-overview.md", """
# Design Patterns Overview

## 1. Categories
- **Creational**: object creation mechanisms
- **Structural**: class/object composition
- **Behavioral**: algorithms and object interaction

## 2. Singleton (Creational)
Ensure only one instance exists.
```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
# Thread-safe version uses threading.Lock
```
Use when: DB connection pool, config manager, logger.

## 3. Factory Method (Creational)
Delegate object creation to subclass/method.
```python
class Notification:
    @staticmethod
    def create(kind):
        if kind == 'email': return EmailNotification()
        if kind == 'sms':   return SMSNotification()
        raise ValueError
```
Use when: object type determined at runtime, hide creation logic.

## 4. Abstract Factory (Creational)
Family of related factories. GUI toolkit (Windows/Mac buttons + checkboxes).

## 5. Builder (Creational)
Step-by-step construction of complex objects.
```python
class QueryBuilder:
    def __init__(self): self._parts = []
    def select(self, cols): self._parts.append(f"SELECT {cols}"); return self
    def from_(self, tbl): self._parts.append(f"FROM {tbl}"); return self
    def build(self): return ' '.join(self._parts)
# Usage: QueryBuilder().select('*').from_('users').build()
```

## 6. Adapter (Structural)
Convert one interface to another.
```python
class OldPayment:
    def do_pay(self, amount): ...
class PaymentAdapter:
    def __init__(self, old): self.old = old
    def pay(self, amount): return self.old.do_pay(amount)
```

## 7. Decorator (Structural)
Add behavior without modifying class. Python `@` syntax is a native decorator.
```python
class Coffee:
    def cost(self): return 5
class MilkDecorator:
    def __init__(self, coffee): self._coffee = coffee
    def cost(self): return self._coffee.cost() + 2
```

## 8. Facade (Structural)
Simplified interface to a subsystem.
```python
class HomeTheaterFacade:
    def __init__(self, amp, dvd, proj): ...
    def watch_movie(self): # calls amp.on(), dvd.play(), proj.on()
```

## 9. Observer (Behavioral)
Subject notifies observers on state change. Event-driven systems.
```python
class EventEmitter:
    def __init__(self): self._listeners = {}
    def on(self, event, fn): self._listeners.setdefault(event, []).append(fn)
    def emit(self, event, *args):
        for fn in self._listeners.get(event, []): fn(*args)
```

## 10. Strategy (Behavioral)
Encapsulate interchangeable algorithms.
```python
class Sorter:
    def __init__(self, strategy): self.strategy = strategy
    def sort(self, data): return self.strategy(data)
sorter = Sorter(sorted)
```

## 11. Command (Behavioral)
Encapsulate a request as an object — supports undo/redo.
```python
class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...
```

## 12. Template Method (Behavioral)
Define skeleton of algorithm in base class; subclasses fill in steps.
```python
class DataProcessor(ABC):
    def process(self):
        self.read(); self.transform(); self.write()
    @abstractmethod
    def transform(self): ...
```

## 13. Proxy (Structural)
Control access to another object: lazy init, access control, logging.

## 14. When to Use Which
| Pattern | Signal |
|---------|--------|
| Singleton | "only one instance" |
| Factory | "create based on type" |
| Observer | "notify on change" |
| Strategy | "swap algorithms" |
| Decorator | "add behavior dynamically" |
| Command | "queue/undo operations" |

## 15. Anti-Patterns to Avoid
- Over-engineering with patterns where simple code suffices.
- God Object (violates SRP).
- Singleton abuse (hidden global state, hard to test).
""")

# ── 9. LLD Interview Questions ────────────────────────────────────────────────
wc(f"{BASE}/21-oop-and-lld/low-level-design-questions.md", """
# Low-Level Design (LLD) Interview Questions

## 1. What Interviewers Look For
- Identify entities and their relationships
- Apply OOP + SOLID principles
- Handle edge cases and concurrency
- Extensible, clean class design

## 2. General Approach (5 Steps)
1. Clarify requirements & constraints
2. Identify core entities (nouns → classes)
3. Define relationships (has-a, is-a)
4. Define methods and interactions
5. Handle edge cases, threading, storage

## 3. Parking Lot — Entities
```
ParkingLot (floors, entry/exit points)
ParkingFloor (spots[])
ParkingSpot (type: compact/large/handicapped, isOccupied)
Vehicle (licensePlate, type)
Ticket (entryTime, spot)
ParkingAttendant
```

## 4. Parking Lot — Key Methods
```python
class ParkingLot:
    def park(self, vehicle) -> Ticket: ...
    def unpark(self, ticket) -> float: ...  # return fee
    def find_spot(self, vehicle_type) -> ParkingSpot: ...
```

## 5. Library System — Entities
```
Library, Book (ISBN, copies), BookItem (physical copy), Member, Librarian
BookReservation, BookLending, Fine
Catalog (search by title/author/subject)
```

## 6. Library System — Key Interactions
- Member searches catalog → reserves book → librarian checks out → return → fine calculation.

## 7. Elevator System — Entities
```
ElevatorSystem, Elevator (currentFloor, state, direction)
ElevatorButton, HallButton (floor, direction)
ElevatorPanel (buttons inside elevator)
Request (floor, direction)
Dispatcher (scheduling algorithm: SCAN/LOOK)
```

## 8. Hotel Booking System — Entities
Room, RoomType, Booking, Guest, Hotel, Payment, Invoice.
Key: room availability check with date ranges.

## 9. Chess Game — Entities
Board (8×8), Piece (subclasses: King, Queen, Rook, Bishop, Knight, Pawn),
Player, Move, GameController.
```python
class Piece(ABC):
    @abstractmethod
    def get_valid_moves(self, board) -> list[Move]: ...
```

## 10. ATM — Entities
ATM, Card, Account, Transaction, CashDispenser, ReceiptPrinter,
Keypad, Screen, BankServer.
State machine: idle → card inserted → pin entered → transaction → eject.

## 11. Class Diagram Tips
- Use UML notation: `+` public, `-` private, `#` protected
- Arrows: inheritance (△), composition (◆), aggregation (◇), association (→)
- Show multiplicities: 1..*, 0..1

## 12. Handling Concurrency
- Parking Lot: lock spot before assigning to avoid double booking.
- Use optimistic locking (version field) for DB-backed designs.
- Python: `threading.Lock()` or database transactions.

## 13. Extensibility Hooks
- Use Strategy pattern for variable parts (pricing strategy, scheduling algorithm).
- Use Factory for object creation (VehicleFactory, SpotFactory).

## 14. Common Interview Mistakes
- Jumping to code without clarifying requirements.
- Missing edge cases: vehicle type mismatch, full lot, expired reservation.
- Making everything static/global.

## 15. Practice Problems Ranked by Frequency
1. Parking Lot ★★★★★
2. LRU Cache ★★★★★
3. Library System ★★★★
4. Elevator ★★★★
5. Chess/Snake&Ladder ★★★
6. ATM ★★★
7. Hotel Booking ★★★
""")

# ── 10. Common LLD Problems ───────────────────────────────────────────────────
wc(f"{BASE}/21-oop-and-lld/common-lld-problems.md", """
# Common LLD Problems

## 1. LRU Cache (LC 146)
Classes: `LRUCache`, `DoublyLinkedList`, `DLinkedNode`.
```python
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}   # key -> node
        self.head, self.tail = DLinkedNode(), DLinkedNode()
        self.head.next = self.tail; self.tail.prev = self.head

    def get(self, key):
        if key not in self.cache: return -1
        self._move_to_front(self.cache[key])
        return self.cache[key].val

    def put(self, key, value):
        if key in self.cache:
            self.cache[key].val = value; self._move_to_front(self.cache[key])
        else:
            node = DLinkedNode(key, value)
            self.cache[key] = node; self._add_to_front(node)
            if len(self.cache) > self.cap:
                lru = self._pop_tail()
                del self.cache[lru.key]
```

## 2. Rate Limiter — Types
- **Token Bucket**: tokens refill at rate r; request consumes 1 token.
- **Leaky Bucket**: queue requests; drain at fixed rate.
- **Fixed Window Counter**: count per time window.
- **Sliding Window Log**: store timestamps of requests.

## 3. Token Bucket Rate Limiter
```python
import time
class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate; self.capacity = capacity
        self.tokens = capacity; self.last = time.time()
    def allow(self):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1; return True
        return False
```

## 4. Notification System — Entities
`NotificationService`, `Notification`, `Channel (Email/SMS/Push)`,
`User`, `NotificationPreference`, `TemplateEngine`.

## 5. Notification System — Design
```python
class Channel(ABC):
    @abstractmethod
    def send(self, user, message): ...
class EmailChannel(Channel):
    def send(self, user, message): ...  # SMTP call
class NotificationService:
    def __init__(self, channels: list[Channel]):
        self.channels = channels
    def notify(self, user, message):
        prefs = user.get_preferences()
        for ch in self.channels:
            if type(ch).__name__ in prefs: ch.send(user, message)
```

## 6. URL Shortener — Entities
`URLShortener`, `URLMapping`, `Base62Encoder`, `Analytics`, `Cache`.

## 7. URL Shortener — Design
```python
class URLShortener:
    BASE62 = "0-9A-Za-z"
    def __init__(self, db, cache):
        self.db = db; self.cache = cache; self.counter = 0
    def shorten(self, long_url) -> str:
        self.counter += 1
        short = self._encode(self.counter)
        self.db.save(short, long_url)
        return f"https://short.ly/{short}"
    def resolve(self, short) -> str:
        if short in self.cache: return self.cache[short]
        url = self.db.get(short); self.cache[short] = url; return url
    def _encode(self, num) -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        res = []
        while num: res.append(chars[num%62]); num //= 62
        return ''.join(reversed(res))
```

## 8. Designing a Logger
```python
class Logger:
    _instance = None
    LEVELS = ['DEBUG','INFO','WARN','ERROR']
    def __new__(cls): ...  # Singleton
    def log(self, level, msg):
        if self.LEVELS.index(level) >= self.LEVELS.index(self.min_level):
            self._write(f"[{level}] {msg}")
```

## 9. Vending Machine — States
Idle → HasMoney → Dispensing → OutOfStock. Use State pattern.

## 10. File System Design
`FileSystem`, `Entry (abstract)`, `File`, `Directory`.
Directory has list of Entry (composite pattern).

## 11. Pub-Sub System
`Broker`, `Topic`, `Publisher`, `Subscriber`, `Message`.
Subscriber registers to topics. Broker fans out messages.

## 12. Design Checklist
- [ ] Defined all core entities with fields
- [ ] Defined relationships (has-a, is-a)
- [ ] Identified key operations/methods
- [ ] Handled concurrency if needed
- [ ] Applied at least one design pattern
- [ ] Discussed extensibility

## 13. LRU Cache — Python Built-in
```python
from functools import lru_cache
from collections import OrderedDict
# OrderedDict: move_to_end(key), popitem(last=False)
```

## 14. Common Gotchas
- Thread safety in rate limiter (use `threading.Lock`).
- URL shortener: collision handling for same URL.
- LRU: O(1) get and put requires hash map + doubly linked list.

## 15. Design Quality Signals
| Signal | Good Design |
|--------|-------------|
| Extensibility | Adding new channel doesn't break existing code |
| Testability | Can inject mock DB/cache |
| SRP | Each class has one job |
| Performance | LRU O(1), Rate limiter O(1) |
""")

# ── 11. OS Basics ─────────────────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/operating-systems-basics.md", """
# Operating Systems Basics

## 1. What is an OS?
Software layer between hardware and applications.
Manages CPU, memory, I/O, file system, and provides process isolation.

## 2. Kernel vs User Space
- **Kernel space**: privileged mode, direct hardware access, OS code runs here.
- **User space**: restricted mode, applications run here.
- System calls cross the boundary: `read()`, `write()`, `fork()`, `exec()`.

## 3. System Calls
Interface for user programs to request kernel services.
```c
// In Python, abstractions over syscalls:
open(), read(), write()     # file I/O
os.fork()                   # create process
socket(), connect(), send() # networking
```
Syscall: user → trap → kernel → return result.

## 4. Process
An instance of a running program. Has: PID, memory (code/data/stack/heap), open file descriptors, CPU registers state.
States: New → Ready → Running → Waiting → Terminated.

## 5. Thread
Lightweight unit of execution within a process. Shares memory/code/data of process. Has own stack and registers.

## 6. Scheduling Algorithms
Goal: maximize CPU utilization, minimize wait time and response time.

## 7. FCFS (First-Come-First-Served)
Non-preemptive. Convoy effect: short jobs stuck behind long ones.
Avg waiting time = sum of burst times of jobs ahead.

## 8. SJF (Shortest Job First)
Optimal average waiting time. Requires knowing burst time in advance (impractical). Can cause starvation of long jobs.

## 9. Round Robin
Each process gets a time quantum Q. If not done, preempted and queued at back.
- Small Q → many context switches (overhead).
- Large Q → degenerates to FCFS.
- Typically Q = 10–100ms.

## 10. Priority Scheduling
Each process has priority; highest priority runs first.
Problem: starvation → fix with aging (increase priority over time).

## 11. Multi-Level Queue / Feedback Queue
Multiple queues with different priorities and scheduling policies.
Processes can move between queues based on behavior (I/O vs CPU bound).

## 12. Context Switch
Save current process state (PCB: process control block), load next process state.
Cost: ~1–10 µs; pure overhead (no useful work done).

## 13. Inter-Process Communication (IPC)
- Pipes (unidirectional byte stream)
- Message queues
- Shared memory (fastest)
- Sockets (cross-machine)
- Signals (async notifications)

## 14. Deadlock Conditions (Coffman)
1. Mutual Exclusion, 2. Hold and Wait, 3. No Preemption, 4. Circular Wait.
Prevention: eliminate one condition. Detection: resource allocation graph.

## 15. Key Metrics
| Algorithm | Avg Wait | Starvation | Preemptive |
|-----------|----------|------------|------------|
| FCFS | High | No | No |
| SJF | Optimal | Yes | Optional |
| Round Robin | Medium | No | Yes |
| Priority | Varies | Yes | Optional |
""")

# ── 12. Processes vs Threads ──────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/processes-vs-threads.md", """
# Processes vs Threads

## 1. Key Differences
| | Process | Thread |
|--|---------|--------|
| Memory | Isolated address space | Shared address space |
| Creation | Expensive (fork) | Cheap |
| Context switch | Expensive | Cheaper |
| Communication | IPC required | Shared memory |
| Crash isolation | Yes | No (crashes whole process) |
| Python GIL | Not affected | Affected |

## 2. Process Creation (fork/exec)
```python
import os
pid = os.fork()
if pid == 0:
    # child
    os.execv('/usr/bin/ls', ['ls', '-la'])
else:
    # parent
    os.wait()
```

## 3. Python multiprocessing
Bypasses GIL. Each process has own Python interpreter.
```python
from multiprocessing import Process, Pool
def square(x): return x*x
with Pool(4) as p:
    results = p.map(square, range(10))
```
Good for: CPU-bound tasks (number crunching, image processing).

## 4. Python threading
GIL prevents true parallel execution for CPU-bound code.
I/O operations release the GIL → threads useful for I/O-bound tasks.
```python
import threading
def fetch(url): ...  # network call
threads = [threading.Thread(target=fetch, args=(u,)) for u in urls]
for t in threads: t.start()
for t in threads: t.join()
```

## 5. Python asyncio
Single-threaded concurrency via event loop. `async/await` — cooperative multitasking.
```python
import asyncio
import aiohttp
async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()
async def main():
    async with aiohttp.ClientSession() as s:
        tasks = [fetch(s, u) for u in urls]
        return await asyncio.gather(*tasks)
```

## 6. GIL — Global Interpreter Lock
CPython mutex ensuring only one thread executes Python bytecode at a time.
Released during I/O, C extensions (numpy), and `time.sleep`.
Does NOT protect against all race conditions (e.g., list.append is atomic but += is not).

## 7. When to Use What
| Scenario | Best Tool |
|----------|-----------|
| CPU-bound parallel | multiprocessing |
| I/O-bound (many requests) | asyncio |
| I/O-bound (blocking libs) | threading |
| Mixed workload | ProcessPool + asyncio |

## 8. Process vs Thread Memory
Processes use virtual memory with page tables — OS maps virtual→physical.
Copy-on-write (COW): fork shares memory pages until one side modifies.

## 9. Context Switch Cost
Thread: save/restore registers + stack pointer (~microseconds).
Process: additionally flush TLB, switch page tables (~more expensive).

## 10. Thread Safety
```python
import threading
lock = threading.Lock()
counter = 0
def increment():
    global counter
    with lock:
        counter += 1
```

## 11. Race Condition Example
```python
# UNSAFE: read-modify-write not atomic
counter += 1   # 3 bytecodes: LOAD, ADD, STORE — GIL can switch between them
```

## 12. Daemon Threads
Threads that die when main thread exits. Useful for background tasks.
`t.daemon = True; t.start()`

## 13. concurrent.futures — High-Level API
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
with ThreadPoolExecutor(max_workers=5) as ex:
    futures = [ex.submit(fetch, url) for url in urls]
    results = [f.result() for f in futures]
```

## 14. Interview Question: asyncio vs threading
asyncio: cooperative, single-threaded, explicit yield points (`await`), scales to thousands of connections, no race conditions.
threading: preemptive, multiple OS threads, need locks, simpler to retrofit blocking code.

## 15. Key Takeaways
- Use `multiprocessing` for CPU parallelism in Python.
- Use `asyncio` for high-concurrency I/O.
- GIL means threads don't help for CPU work.
- Threads still useful for blocking I/O with legacy libraries.
""")

# ── 13. Concurrency Basics ────────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/concurrency-basics.md", """
# Concurrency Basics

## 1. Concurrency vs Parallelism
- **Concurrency**: multiple tasks in progress at the same time (interleaved execution).
- **Parallelism**: multiple tasks running simultaneously (multi-core).
- asyncio is concurrent but not parallel. multiprocessing is both.

## 2. Race Condition
Outcome depends on order of thread/process execution.
```python
# Thread 1: x = x + 1
# Thread 2: x = x + 1
# Both read x=5, both write 6 → lost update
```

## 3. Mutex (Mutual Exclusion Lock)
Only one thread holds it at a time. Others block.
```python
lock = threading.Lock()
with lock:         # acquire on enter, release on exit
    shared_var += 1
```

## 4. Semaphore
Allows N concurrent accesses (generalized mutex where N=1).
```python
sem = threading.Semaphore(3)   # max 3 concurrent threads
with sem:
    access_db()
```

## 5. Condition Variable
Thread waits for a condition to become true.
```python
cond = threading.Condition()
# Producer
with cond:
    queue.append(item); cond.notify()
# Consumer
with cond:
    cond.wait_for(lambda: len(queue) > 0)
    item = queue.pop()
```

## 6. Deadlock
Two threads each hold a lock the other needs.
```python
# Thread 1: lock_a.acquire(); lock_b.acquire()
# Thread 2: lock_b.acquire(); lock_a.acquire()  → deadlock
```
Prevention: always acquire locks in the same order.

## 7. Livelock
Threads keep responding to each other without making progress (like two people dodging each other in a corridor).

## 8. Starvation
A thread is perpetually denied access to a resource because others keep acquiring it first. Fix: fair queuing (FIFO lock).

## 9. Python asyncio Concurrency Model
Event loop + coroutines. `await` yields control back to event loop.
```python
async def main():
    await asyncio.sleep(1)     # yields; loop can run other coroutines
    result = await some_io()
asyncio.run(main())
```

## 10. asyncio Primitives
```python
asyncio.Lock()        # async mutex
asyncio.Semaphore(n)  # async semaphore
asyncio.Event()       # set/wait
asyncio.Queue()       # async producer-consumer
```

## 11. Producer-Consumer Pattern
```python
q = asyncio.Queue()
async def producer():
    for i in range(5): await q.put(i); await asyncio.sleep(0.1)
async def consumer():
    while True:
        item = await q.get(); process(item); q.task_done()
```

## 12. Atomic Operations in Python
`list.append()`, `dict[k]=v` are GIL-atomic (single bytecode).
`counter += 1` is NOT atomic (LOAD, ADD, STORE).
Use `threading.Lock` or `queue.Queue` for safe sharing.

## 13. Thread Pool Pattern
```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as pool:
    futures = [pool.submit(task, arg) for arg in args]
    results = [f.result() for f in futures]
```

## 14. Common Concurrency Bugs
| Bug | Cause | Fix |
|-----|-------|-----|
| Race condition | Unsynchronized access | Lock |
| Deadlock | Circular lock acquisition | Lock ordering |
| Livelock | Reactive but no progress | Random backoff |
| Starvation | Unfair scheduling | Fair queue |
| Memory visibility | CPU caching | Memory barriers / lock |

## 15. Interview Tips
- Draw thread execution timeline to illustrate race conditions.
- Know difference: mutex vs semaphore vs condition variable.
- Explain GIL → why multiprocessing for CPU, asyncio for I/O.
- asyncio scales to 10k+ connections; threading saturates at ~100s.
""")

# ── 14. Memory Management ─────────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/memory-management.md", """
# Memory Management

## 1. Memory Layout of a Process
```
High address
┌───────────────┐
│  Stack        │ ← grows downward (function calls, local vars)
├───────────────┤
│  ↓         ↑  │
│  Heap         │ ← grows upward (dynamic allocation)
├───────────────┤
│  BSS          │ ← uninitialized globals
├───────────────┤
│  Data         │ ← initialized globals
├───────────────┤
│  Text (Code)  │ ← read-only
Low address
```

## 2. Stack
- Automatic allocation/deallocation (LIFO).
- Fixed size (typically 1–8 MB).
- Stack overflow: infinite recursion, huge local arrays.
- Fast: just move stack pointer.

## 3. Heap
- Manual (C: malloc/free) or GC-managed (Python, Java).
- Slower: needs allocator to find free block.
- Fragmentation: internal (wasted inside allocated block) and external (free blocks scattered).

## 4. Garbage Collection Strategies
| Strategy | How | Used By |
|----------|-----|---------|
| Reference counting | Count references, free at 0 | Python (primary), Swift |
| Mark-and-sweep | Mark reachable, sweep rest | Python (cycles), Go |
| Generational GC | Separate young/old objects | Java, Python |
| Tracing GC | Trace from roots | JVM, V8 |

## 5. Python's Reference Counting
```python
import sys
a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount arg)
b = a
print(sys.getrefcount(a))  # 3
del b
# refcount drops; if 0, memory freed immediately
```

## 6. Cyclic Reference Problem
```python
a = []
a.append(a)   # a refers to itself; refcount never reaches 0
# Python's cyclic GC (gc module) handles this
```

## 7. Python's gc Module
```python
import gc
gc.collect()          # manually trigger cycle collection
gc.disable()          # disable automatic GC (for performance-critical sections)
gc.get_count()        # (gen0, gen1, gen2) counts
```
Generational: objects that survive GC are promoted to older generations.

## 8. Memory Leaks
Causes: forgotten references, event listeners not removed, circular references without GC, caches that grow unbounded.
```python
# Common Python leak: class-level mutable default
class Foo:
    items = []   # shared across ALL instances!
    def add(self, x): self.items.append(x)  # leaks
```

## 9. Memory Profiling in Python
```python
# memory_profiler
from memory_profiler import profile
@profile
def my_func(): ...

# tracemalloc
import tracemalloc
tracemalloc.start()
# ... code ...
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:5]: print(stat)
```

## 10. Stack vs Heap — Python Specifics
Everything in Python is a heap object (even integers). Stack only holds frame pointers and local variable references.
`sys.setrecursionlimit(n)` controls Python stack depth (default 1000).

## 11. Virtual Memory
OS gives each process an illusion of large contiguous address space.
Pages (4KB) swapped between RAM and disk. Page fault → OS loads page from disk (slow!).

## 12. Memory Allocators
CPython uses its own allocator on top of malloc: PyMalloc for objects <512 bytes (pool-based, reduces fragmentation).

## 13. WeakRef — Avoid Cycles
```python
import weakref
class Node:
    def __init__(self): self.parent = None
node = Node()
ref = weakref.ref(node)   # doesn't increase refcount
```

## 14. Common Interview Questions
- What is a memory leak? How do you find it in Python?
- Explain stack overflow vs heap overflow.
- How does Python's GC work?
- Why is reference counting insufficient alone?

## 15. Key Facts
- Stack: fast, LIFO, size-limited, automatic.
- Heap: flexible, GC or manual, can fragment.
- Python: refcounting + cyclic GC + generational collection.
- `del x` doesn't guarantee memory freed — only decrements refcount.
""")

# ── 15. DBMS Basics ───────────────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/dbms-basics.md", """
# DBMS Basics

## 1. Relational Model
Data organized in tables (relations). Row = tuple, Column = attribute.
Schema defines structure; instance = actual data at a point in time.

## 2. Keys
- **Primary Key**: uniquely identifies each row. NOT NULL, unique.
- **Foreign Key**: references PK of another table. Enforces referential integrity.
- **Candidate Key**: minimal set of columns that uniquely identify a row.
- **Composite Key**: PK made of multiple columns.
- **Surrogate Key**: artificial PK (auto-increment ID).

## 3. SQL Joins
```sql
-- INNER JOIN: only matching rows from both tables
SELECT u.name, o.total FROM users u
JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: all rows from left, NULLs for no match on right
SELECT u.name, o.total FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- FULL OUTER JOIN: all rows from both; NULL where no match
-- CROSS JOIN: cartesian product
```

## 4. Aggregate Functions
```sql
SELECT dept, COUNT(*), AVG(salary), MAX(salary), SUM(salary)
FROM employees
GROUP BY dept
HAVING AVG(salary) > 50000;
```

## 5. Subqueries
```sql
-- Correlated subquery (runs per row)
SELECT name FROM employees e
WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept=e.dept);

-- Non-correlated
SELECT name FROM employees WHERE dept_id IN (SELECT id FROM depts WHERE city='NYC');
```

## 6. Window Functions
```sql
SELECT name, salary,
    RANK() OVER (PARTITION BY dept ORDER BY salary DESC),
    LAG(salary) OVER (ORDER BY hire_date)
FROM employees;
```

## 7. Transactions
A sequence of operations treated as a unit. Either all succeed or all fail (rollback).
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- or ROLLBACK on error
```

## 8. ACID Properties
- **Atomicity**: all or nothing.
- **Consistency**: DB goes from valid state to valid state.
- **Isolation**: concurrent transactions don't interfere.
- **Durability**: committed data survives crashes.

## 9. Isolation Levels
| Level | Dirty Read | Non-Repeatable | Phantom |
|-------|-----------|----------------|---------|
| Read Uncommitted | Yes | Yes | Yes |
| Read Committed | No | Yes | Yes |
| Repeatable Read | No | No | Yes |
| Serializable | No | No | No |

## 10. ER Diagram Concepts
Entities, Attributes, Relationships. Cardinality: 1:1, 1:N, M:N.
M:N requires junction/bridge table.

## 11. Stored Procedures vs Functions
```sql
-- Function: returns value, used in SELECT
CREATE FUNCTION get_balance(uid INT) RETURNS DECIMAL AS ...

-- Stored Procedure: may have side effects, called with EXEC/CALL
CREATE PROCEDURE transfer(from_id INT, to_id INT, amount DECIMAL) AS ...
```

## 12. Views
Virtual table based on SELECT. Simplifies complex queries; can be updatable.
```sql
CREATE VIEW active_users AS SELECT * FROM users WHERE status='active';
```

## 13. Triggers
Automatically execute on INSERT/UPDATE/DELETE.
```sql
CREATE TRIGGER update_timestamp BEFORE UPDATE ON orders
FOR EACH ROW SET NEW.updated_at = NOW();
```

## 14. Common Interview SQL Questions
- Find second highest salary.
- Find employees who earn more than their manager.
- Delete duplicate rows keeping one.
- Find customers who never placed an order.

## 15. Quick Reference
```sql
-- Second highest salary
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);
-- Or:
SELECT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;
```
""")

# ── 16. SQL vs NoSQL ──────────────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/sql-vs-nosql.md", """
# SQL vs NoSQL

## 1. SQL (Relational)
Structured data, fixed schema, ACID guarantees, powerful query language.
Examples: PostgreSQL, MySQL, SQLite, Oracle.

## 2. NoSQL Categories
| Type | Example | Use Case |
|------|---------|----------|
| Document | MongoDB, CouchDB | JSON-like objects |
| Key-Value | Redis, DynamoDB | Cache, session |
| Column-family | Cassandra, HBase | Time-series, analytics |
| Graph | Neo4j | Social networks, recommendations |

## 3. CAP Theorem
A distributed system can guarantee at most 2 of 3:
- **Consistency**: every read gets the latest write.
- **Availability**: every request gets a response (not necessarily latest).
- **Partition Tolerance**: system works despite network partition.

Network partitions always happen → choose C or A during partition.
- CP: MongoDB, HBase, ZooKeeper.
- AP: Cassandra, DynamoDB, CouchDB.

## 4. PACELC
Extends CAP: even without partition, tradeoff between Latency and Consistency.

## 5. When to Use SQL
- Strong ACID requirements (banking, e-commerce orders)
- Complex queries with JOINs
- Data with clear relational structure
- Reporting and analytics

## 6. When to Use NoSQL
- Unstructured/semi-structured data
- Horizontal scalability needed
- High write throughput (Cassandra)
- Simple access patterns (key lookups)
- Schema evolves frequently

## 7. MongoDB vs PostgreSQL
```javascript
// MongoDB — document query
db.orders.find({ user_id: "u123", status: "shipped" })
         .sort({ created_at: -1 }).limit(10)
```
```sql
-- PostgreSQL — relational query
SELECT * FROM orders WHERE user_id = 'u123' AND status = 'shipped'
ORDER BY created_at DESC LIMIT 10;
```

## 8. Eventual Consistency
Nodes may temporarily have different values, but will converge. DynamoDB, Cassandra default.
Acceptable for: social media likes, product view counts, shopping cart.

## 9. Strong Consistency
All reads see the latest committed write. Required for: bank balances, inventory, seat booking.

## 10. Sharding (Horizontal Partitioning)
Split data across multiple nodes by shard key.
- Range sharding: users A-M → shard1, N-Z → shard2.
- Hash sharding: shard = hash(key) % N (even distribution).
- Problem: cross-shard JOINs are expensive.

## 11. Replication
Master-slave: writes to master, reads from slaves. Lag between master and slave.
Multi-master: writes to any node; conflict resolution needed.

## 12. Redis Use Cases
```python
import redis
r = redis.Redis()
r.set('session:abc', user_json, ex=3600)   # TTL 1hr
r.incr('page_views:home')                   # atomic counter
r.lpush('queue:emails', email_json)         # message queue
r.zadd('leaderboard', {user: score})        # sorted set
```

## 13. Cassandra Data Model
Design tables around query patterns (not normalization).
Wide rows: partition key + clustering columns.
No JOINs; denormalization is intentional.

## 14. Common Interview Scenario
"Design a social feed." → Use Cassandra for posts (high write, time-series) + Redis for feed cache + PostgreSQL for user profiles.

## 15. Decision Framework
```
Transactional + relational → PostgreSQL
Cache/session → Redis
Flexible schema, JSON → MongoDB
High-write time-series → Cassandra
Graph traversals → Neo4j
Full-text search → Elasticsearch
```
""")

# ── 17. Indexing ──────────────────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/indexing.md", """
# Database Indexing

## 1. What is an Index?
Auxiliary data structure that speeds up data retrieval. Trade-off: faster reads, slower writes (index must be updated), extra storage.

## 2. B-Tree Index (Most Common)
Balanced tree. Leaf nodes contain data pointers; sorted order.
- O(log N) search, insert, delete.
- Supports: =, <, >, BETWEEN, ORDER BY, LIKE 'prefix%'.
- Default index type in PostgreSQL, MySQL.

## 3. Hash Index
Maps key → bucket with pointer. O(1) equality lookup.
- Only supports `=` — no range queries.
- Used in: hash partitioning, in-memory tables.

## 4. Clustered vs Non-Clustered Index
- **Clustered**: table data physically sorted by index key. Only ONE per table. (InnoDB: PK = clustered.)
- **Non-clustered**: separate structure with pointers to data rows. Multiple allowed.

## 5. B-Tree Index in PostgreSQL
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
-- Partial index (indexes subset of rows)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
```

## 6. Composite Index
Index on multiple columns. Column order matters.
```sql
INDEX (a, b, c)
-- Usable for: WHERE a=..., WHERE a=... AND b=...
-- NOT usable for: WHERE b=..., WHERE c=...
-- Leftmost prefix rule
```

## 7. Index Selectivity
Selectivity = distinct values / total rows. High selectivity → index is useful.
- email: high selectivity (nearly unique) → good for index.
- gender: low selectivity (only 2-3 values) → full scan often faster.

## 8. Covering Index
Index contains all columns needed by query — no heap lookup needed.
```sql
CREATE INDEX idx_cover ON orders(user_id, status, total);
SELECT status, total FROM orders WHERE user_id = 5;
-- Index-only scan (very fast)
```

## 9. EXPLAIN / Query Plan
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'a@b.com';
-- Seq Scan → no index used
-- Index Scan → using index
-- Bitmap Heap Scan → used for multiple OR conditions
```

## 10. When Index is NOT Used
- Low selectivity column (gender, boolean).
- Query uses function on indexed column: `WHERE LOWER(email) = ...` (create functional index).
- Leading column of composite index not in WHERE.
- Very small table (full scan cheaper).

## 11. Index for Sorting
```sql
-- ORDER BY created_at DESC: index on (created_at DESC) avoids sort step
CREATE INDEX idx_created ON posts(created_at DESC);
```

## 12. GIN and GiST Indexes (PostgreSQL)
- **GIN** (Generalized Inverted Index): full-text search, JSONB, arrays. `@>`, `@@` operators.
- **GiST**: geometric data, range types, fuzzy search.

## 13. Index Maintenance
Indexes bloat over time with updates/deletes. Run `VACUUM` and `ANALYZE` in PostgreSQL.
`REINDEX` rebuilds bloated indexes.

## 14. Index Strategy for Interviews
1. Index columns in WHERE, JOIN, ORDER BY, GROUP BY.
2. Composite index: most selective / most-queried first.
3. Avoid over-indexing — each index slows writes.
4. Use partial indexes for sparse conditions.
5. Check EXPLAIN output to verify index is used.

## 15. Common Interview Questions
- Why doesn't my query use the index? (function on column, low selectivity, small table)
- Clustered vs non-clustered? (physical order vs pointer)
- How does B-tree differ from hash index? (range vs equality)
- What is a covering index? (all needed cols in index)
""")

# ── 18. Normalization ─────────────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/normalization.md", """
# Database Normalization

## 1. Purpose
Eliminate data redundancy and anomalies (insert, update, delete anomalies).
Each normal form eliminates a specific type of dependency.

## 2. Functional Dependency
A → B: knowing A uniquely determines B.
Example: StudentID → StudentName, StudentID → DOB.

## 3. First Normal Form (1NF)
Rules: atomic values (no repeating groups, no arrays), each row unique.
```
Violation: courses = "Math, Physics, CS"   (multi-valued)
Fix: separate Courses table with one row per course.
```

## 4. Second Normal Form (2NF)
Must be in 1NF + no partial dependency (non-key attribute depends on PART of composite PK).
```
Table: (StudentID, CourseID) → Grade, StudentName
Violation: StudentName depends only on StudentID (partial dependency)
Fix: split into Student(StudentID, StudentName) + Enrollment(StudentID, CourseID, Grade)
```

## 5. Third Normal Form (3NF)
Must be in 2NF + no transitive dependency (non-key → non-key).
```
Table: EmployeeID → DeptID → DeptName
Violation: DeptName transitively depends on EmployeeID via DeptID
Fix: Department(DeptID, DeptName) + Employee(EmployeeID, DeptID)
```

## 6. Boyce-Codd Normal Form (BCNF)
Stricter than 3NF. For every functional dependency X → Y, X must be a superkey.
Handles anomalies 3NF misses with overlapping candidate keys.

## 7. 3NF vs BCNF
```
Course (Student, Subject, Teacher)
FDs: {Student,Subject}→Teacher; Teacher→Subject
3NF: satisfied (Teacher is candidate key for Subject)
BCNF: violated (Teacher→Subject but Teacher is not a superkey of the whole table)
```

## 8. 4NF — Multi-Valued Dependencies
Eliminate multi-valued dependencies. Rare in practice.

## 9. Anomalies Eliminated by Normalization
- **Insert anomaly**: can't add data without inserting other unrelated data.
- **Update anomaly**: same fact stored multiple times; inconsistent update.
- **Delete anomaly**: deleting one fact accidentally deletes another.

## 10. Denormalization
Intentional introduction of redundancy for performance (reduce JOINs).
```sql
-- Normalized: need JOIN orders + users to get user email
-- Denormalized: store user_email directly in orders table
```
Use when: read-heavy, analytical queries, JOINs are bottleneck.

## 11. Normalization in Practice
Most production databases aim for 3NF. BCNF and beyond are theoretical; full normalization may hurt performance.

## 12. Example — Full Normalization
```
Raw: (OrderID, CustomerName, CustomerCity, ProductName, Quantity, Price)
1NF: atomic values ✓ (already)
2NF: no partial deps → Customer(CustID, Name, City), Product(ProdID, Name, Price), Order(OrderID, CustID), OrderItem(OrderID, ProdID, Qty)
3NF: no transitive deps → already satisfied above
```

## 13. Star Schema vs Normalization
Data warehouses use star schema (denormalized): fact table + dimension tables.
Optimized for analytical queries, not OLTP.

## 14. Normalization Decision Guide
| Situation | Approach |
|-----------|----------|
| OLTP (transactions, writes) | Normalize to 3NF |
| OLAP (analytics, reads) | Denormalize / star schema |
| Read-heavy with known query patterns | Denormalize with indexes |
| Storage is a concern | Normalize |

## 15. Interview Quick Reference
| Form | Eliminates |
|------|-----------|
| 1NF | Non-atomic values, duplicate rows |
| 2NF | Partial dependencies on composite PK |
| 3NF | Transitive dependencies |
| BCNF | All non-trivial FDs must have superkey as determinant |
""")

# ── 19. ACID Properties ───────────────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/acid-properties.md", """
# ACID Properties

## 1. Overview
ACID = Atomicity, Consistency, Isolation, Durability.
Guarantees database transactions are processed reliably.

## 2. Atomicity
All operations in a transaction succeed, or ALL are rolled back. No partial updates.
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- If second UPDATE fails, first is also rolled back
COMMIT;
```
Implementation: Undo Log / Rollback Segments.

## 3. Consistency
Transaction brings DB from one valid state to another. All integrity constraints maintained.
Example: if balance cannot go negative (CHECK constraint), transaction violating this is rolled back.
Note: Consistency is partly guaranteed by the application (business rules) + DB constraints.

## 4. Isolation
Concurrent transactions execute as if serialized. Intermediate state is invisible to others.
```sql
-- Without isolation:
T1 reads balance=100; T2 reads balance=100
T1 deducts 50 → 50; T2 deducts 50 → 50; both commit
-- Final balance: 50 instead of 0 → lost update
```

## 5. Durability
Once committed, data survives system failures (crash, power loss).
Implementation: Write-Ahead Logging (WAL) — changes written to log before disk pages.
On crash recovery, replay WAL.

## 6. Isolation Levels
```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;  -- PostgreSQL default
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;    -- strictest
```

## 7. Read Anomalies
| Anomaly | Description |
|---------|-------------|
| Dirty Read | Read uncommitted data from another transaction |
| Non-Repeatable Read | Same row read twice gives different values |
| Phantom Read | Same query returns different set of rows |
| Lost Update | Two transactions overwrite each other |

## 8. Read Uncommitted
Lowest isolation. Allows dirty reads. Rarely used; no locks on reads.

## 9. Read Committed
Default in PostgreSQL. No dirty reads. Re-reads can see committed changes by others (non-repeatable reads).

## 10. Repeatable Read
Snapshot of DB at transaction start. Same rows read twice → same result.
Prevents dirty + non-repeatable reads. Phantoms still possible (in MySQL, InnoDB uses gap locks to prevent).

## 11. Serializable
Strictest. Transactions appear to execute serially. Implemented via:
- Two-Phase Locking (2PL)
- Serializable Snapshot Isolation (SSI) in PostgreSQL

## 12. MVCC (Multi-Version Concurrency Control)
PostgreSQL and MySQL InnoDB use MVCC: readers don't block writers and vice versa.
Each transaction sees a snapshot. Old versions kept until no longer needed.

## 13. WAL (Write-Ahead Log)
```
Before any data page is modified on disk:
1. Log record written to WAL (durable)
2. Data page updated in memory (buffer pool)
3. Data page flushed to disk lazily

On crash: replay WAL → recover committed changes.
```

## 14. BASE vs ACID (NoSQL)
- **Basically Available**: system always responds.
- **Soft state**: state may change even without input (eventual consistency).
- **Eventually Consistent**: all nodes converge eventually.
NoSQL systems (Cassandra, DynamoDB) typically offer BASE semantics.

## 15. Interview Tips
- Explain each property with a bank transfer example.
- Know: isolation level = trade-off between correctness and concurrency.
- MVCC enables high concurrency without heavy locking.
- Durability = WAL/journaling + fsync to disk.
""")

# ── 20. Computer Networks Basics ─────────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/computer-networks-basics.md", """
# Computer Networks Basics

## 1. OSI Model (7 Layers)
```
7. Application   — HTTP, FTP, SMTP, DNS, WebSocket
6. Presentation  — SSL/TLS, encoding, compression
5. Session       — session management
4. Transport     — TCP, UDP (ports, reliability)
3. Network       — IP, ICMP, routing
2. Data Link     — Ethernet, MAC addresses, switches
1. Physical      — bits on wire, fiber, radio
```
Mnemonic: "All People Seem To Need Data Processing"

## 2. TCP vs UDP
| | TCP | UDP |
|--|-----|-----|
| Connection | Connection-oriented (3-way handshake) | Connectionless |
| Reliability | Guaranteed delivery, ordered | Best-effort, no ordering |
| Flow control | Yes (sliding window) | No |
| Congestion control | Yes | No |
| Overhead | Higher | Lower |
| Use cases | HTTP, email, FTP | DNS, video streaming, gaming |

## 3. TCP 3-Way Handshake
```
Client → SYN → Server
Client ← SYN-ACK ← Server
Client → ACK → Server
[Connection established]
```
Termination: 4-way FIN handshake.

## 4. HTTP vs HTTPS
- HTTP: plaintext, port 80.
- HTTPS: HTTP over TLS (Transport Layer Security), port 443.
- TLS handshake: negotiate cipher, exchange certificates, establish session key.
- Data encrypted end-to-end after handshake.

## 5. HTTP Methods
GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove), OPTIONS (CORS preflight).

## 6. HTTP Status Codes
```
2xx Success:   200 OK, 201 Created, 204 No Content
3xx Redirect:  301 Permanent, 302 Temporary, 304 Not Modified
4xx Client:    400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Rate Limited
5xx Server:    500 Internal Error, 502 Bad Gateway, 503 Unavailable, 504 Timeout
```

## 7. DNS (Domain Name System)
Translates domain names → IP addresses.
```
Browser → Recursive Resolver → Root NS → TLD NS (.com) → Authoritative NS → IP
Result cached at each level (TTL-based).
```
Record types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), TXT (verification).

## 8. CDN (Content Delivery Network)
Distribute static assets to geographically distributed edge servers.
User routed to nearest PoP (Point of Presence) → lower latency.
Examples: Cloudflare, AWS CloudFront, Akamai.

## 9. Load Balancer
Distributes incoming requests across backend servers.
Algorithms: Round Robin, Least Connections, IP Hash, Weighted.
Operates at L4 (TCP) or L7 (HTTP — can route by URL/headers).

## 10. WebSockets
Full-duplex persistent connection between client and server.
Starts as HTTP, upgraded via `Upgrade: websocket` header.
Use for: chat, real-time notifications, live dashboards.

## 11. REST vs GraphQL
```
REST: GET /users/1, POST /orders — multiple endpoints, fixed response shape
GraphQL: single /graphql endpoint, client specifies exact fields needed
```

## 12. Latency Numbers
```
L1 cache: 1 ns           RAM: 100 ns
SSD: 100 µs              HDD: 10 ms
Same datacenter RTT: 0.5 ms
Cross-continent RTT: 150 ms
```

## 13. Subnet and CIDR
192.168.1.0/24 → 256 addresses, subnet mask 255.255.255.0.
Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.

## 14. Common Protocols Summary
| Protocol | Port | Layer | Purpose |
|----------|------|-------|---------|
| HTTP | 80 | 7 | Web |
| HTTPS | 443 | 7 | Secure web |
| DNS | 53 | 7 | Name resolution |
| SSH | 22 | 7 | Remote shell |
| SMTP | 25 | 7 | Email |
| TCP | — | 4 | Reliable transport |
| UDP | — | 4 | Fast transport |

## 15. Interview Tips
- TCP 3-way handshake: know SYN/SYN-ACK/ACK by heart.
- HTTPS: "HTTP + TLS encryption, port 443."
- DNS: resolver hierarchy, TTL caching.
- Know difference between L4 and L7 load balancers.
""")

# ── 21. System Design Basics (Non-ML) ─────────────────────────────────────────
wc(f"{BASE}/22-cs-fundamentals/system-design-basics-non-ml.md", """
# Non-ML System Design Basics

## 1. Approach to System Design Interview
1. Clarify requirements (functional + non-functional: scale, latency, consistency)
2. Estimate capacity (QPS, storage, bandwidth)
3. High-level design (components, data flow)
4. Deep dive (DB schema, API, key algorithms)
5. Identify bottlenecks + mitigations

## 2. Capacity Estimation
```
Twitter-like feed:
- 100M DAU, 50 tweets/user/day read = 5B reads/day ≈ 60K QPS
- 1M new tweets/day, 140 bytes each = 140 MB/day ≈ 50 GB/year
- With media: 100x → 5 TB/year
```

## 3. Horizontal vs Vertical Scaling
- **Vertical (Scale up)**: bigger machine (more CPU/RAM). Limit: hardware cap.
- **Horizontal (Scale out)**: more machines. Requires stateless services, load balancers.
- Prefer horizontal for internet-scale applications.

## 4. Caching
```
Client-side (browser) → CDN → API Gateway cache → Application cache (Redis) → DB cache (query cache)
```
Cache-aside: app checks cache; miss → fetch DB → populate cache.
Write-through: write to cache + DB simultaneously.
Write-back: write to cache only; async flush to DB.
Eviction: LRU (most common), LFU, TTL.

## 5. CAP Theorem in System Design
Partition tolerance is mandatory in distributed systems.
Choose between:
- CP (consistency): bank transactions, inventory. Sacrifice availability on partition.
- AP (availability): social likes, DNS, CDN. Sacrifice consistency on partition.

## 6. Database Choices
```
User profiles, orders → PostgreSQL (relational, ACID)
Session, cache → Redis (key-value, in-memory)
Feed, events → Cassandra (high-write, time-series)
Search → Elasticsearch (full-text)
Media files → S3 + CDN
```

## 7. Message Queues
Decouple producers and consumers. Enable async processing.
```
Use cases: email sending, image resizing, event streaming, order processing
Tools: Kafka (streaming, replay), RabbitMQ (task queues), SQS (managed)
```
Kafka: topics, partitions, consumer groups, offset-based consumption, persistent log.

## 8. Microservices vs Monolith
| | Monolith | Microservices |
|--|----------|---------------|
| Deployment | Single unit | Independent |
| Scalability | Scale whole app | Scale per service |
| Complexity | Simple dev | Complex ops |
| Latency | In-process | Network calls |
| Start with | Monolith | Split when needed |

## 9. API Gateway
Single entry point: auth, rate limiting, routing, SSL termination, monitoring.
Nginx, Kong, AWS API Gateway, Envoy.

## 10. Rate Limiting
Prevent abuse. Implement at: client, API gateway, application.
Algorithms: token bucket (allow bursts), sliding window (precise), fixed window (simple).

## 11. Consistent Hashing
For distributed caching / sharding: map keys to nodes on a ring.
Adding/removing nodes only remaps 1/N of keys (vs all with modulo hashing).
Virtual nodes improve even distribution.

## 12. URL Shortener Design
```
API: POST /shorten → {short_url}, GET /{code} → redirect
Storage: Hash map: code → long_url (DynamoDB or Redis)
Encoding: Base62(auto-increment ID) or MD5(first 7 chars)
Scale: 100M URLs → ~7 bytes/code * 100M = 700 MB (fits in Redis)
```

## 13. Design a Feed System (Twitter-like)
```
Fanout on write: pre-compute feed for each follower on tweet creation → low read latency, high write cost.
Fanout on read: pull tweets from followees at read time → high read latency, low write cost.
Hybrid: fanout on write for regular users, fanout on read for celebrities (many followers).
```

## 14. Reliability Patterns
- **Circuit Breaker**: stop calling failing service. States: closed/open/half-open.
- **Retry with exponential backoff**: avoid thundering herd.
- **Bulkhead**: isolate failure (separate thread pools per service).
- **Health checks + auto-restart**: Kubernetes liveness/readiness probes.

## 15. Non-Functional Requirements Checklist
| Concern | Solution |
|---------|----------|
| High availability | Replication, multi-AZ, load balancer |
| Low latency | CDN, caching, DB indexes |
| Scalability | Horizontal scaling, sharding |
| Durability | DB replication, backups, WAL |
| Security | HTTPS, auth, rate limiting, input validation |
| Observability | Metrics, logs, traces (Prometheus, Grafana, Jaeger) |
""")

print('Batch E script complete')
