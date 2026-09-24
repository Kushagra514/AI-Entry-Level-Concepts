import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch E)"')

wc("19-dp-deep-dive/interval-dp.md", r"""# Interval DP

## 1. Definition
Interval DP is a dynamic programming pattern where subproblems are defined over contiguous subarrays (intervals) of the input. The state is typically `dp[i][j]`, representing the optimal answer for the interval from index `i` to `j`.

## 2. Intuition
To solve a big problem (the whole array), you solve smaller problems (smaller intervals). The optimal solution for an interval `[i, j]` is usually found by trying every possible split point `k` between `i` and `j`, combining the optimal solutions of `[i, k]` and `[k+1, j]`.

## 3. Why it exists
Problems like Matrix Chain Multiplication or bursting balloons cannot be solved linearly because the operations collapse intervals unpredictably. We must explore all parenthesizations/groupings, which naturally forms an interval structure.

## 4. Mechanics
- **State:** `dp[i][j]` = optimal cost/value for `arr[i...j]`.
- **Transitions:** `dp[i][j] = min/max(dp[i][k] + dp[k+1][j] + cost(i, k, j))` for `k` from `i` to `j-1`.
- **Base Cases:** `dp[i][i]` is usually the cost for a single element (often 0 or a base value).
- **Iteration Order:** Must iterate by *length* of the interval (from 1 to $N$), then by start index `i`. You cannot iterate `i` and `j` in a standard nested loop because `dp[i][j]` depends on smaller lengths.

## 5. Complexity (Time & Space)
- **Time:** $O(N^3)$. There are $O(N^2)$ states (`i`, `j`), and transitioning takes $O(N)$ (looping over `k`).
- **Space:** $O(N^2)$ to store the `dp` table.

## 6. Tiny worked example
Array `A` of matrices to multiply. Lengths: 10, 30, 5, 60.
Cost of `A[0]*A[1]` is $10 \times 30 \times 5 = 1500$.
To find optimal grouping of `A[0..2]`, try splitting at `k=0` (`A[0] * (A[1]*A[2])`) and `k=1` (`(A[0]*A[1]) * A[2]`). Pick the min cost.

## 7. Code (Python)
```python
def matrix_chain_multiplication(p):
    n = len(p) - 1 # number of matrices
    dp = [[0] * n for _ in range(n)]
    
    # l is the length of the interval
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')
            # k is the split point
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]
                dp[i][j] = min(dp[i][j], cost)
                
    return dp[0][n-1]
```

## 8. Common mistakes
- Iterating `i` from 0 to N and `j` from `i` to N. This is wrong because when calculating `dp[0][3]`, you might need `dp[1][3]`, which hasn't been computed yet. Always iterate by `length`.
- Getting indices mixed up in the cost function, especially when padding arrays (e.g., in Burst Balloons).

## 9. 30-second interview answer
"Interval DP solves problems by finding optimal solutions for contiguous subarrays. The state is `dp[i][j]` for the range `[i, j]`. The transition involves testing all split points `k` between `i` and `j` to combine the results of the two halves. It generally takes $O(N^3)$ time and $O(N^2)$ space, and requires iterating by interval length rather than start index."

## 10. 2-minute interview answer
"Interval DP is a specific DP pattern used when operations merge adjacent elements, like Matrix Chain Multiplication, Burst Balloons, or Palindrome Partitioning. Because merging changes the adjacent elements for future operations, greedy or simple 1D DP fails. Instead, we define our state as the optimal cost for the subarray `[i, j]`. To compute `dp[i][j]`, we guess the *last* operation that combines the two halves. We enumerate all split points `k`, adding the cost of `[i, k]` and `[k+1, j]` plus the cost of merging them. A critical implementation detail is the loop structure: we must build the table by increasing interval lengths, starting from length 1 up to $N$, ensuring subproblems are solved before they are needed. The complexity is almost always $O(N^3)$ time and $O(N^2)$ space."

## 11. Follow-ups
- "How do you solve Burst Balloons?" (Instead of guessing which balloon pops first, guess which balloon pops *last* in the interval `[i, j]`. That way, its adjacent balloons are strictly `i-1` and `j+1`, which are outside the interval and haven't popped yet).

## 12. Deeper questions
- "What is Knuth's Optimization?" (An optimization for certain Interval DP problems that reduces time from $O(N^3)$ to $O(N^2)$. If the optimal split point $K[i][j]$ satisfies $K[i][j-1] \le K[i][j] \le K[i+1][j]$, we can bound the `k` loop. Applies to Optimal Binary Search Tree).

## 13. Related concepts
- **2D DP**: Interval DP is a subset of 2D DP.
- **Divide and Conquer**: The transition mimics a D&C merge step, but memoized.

## 14. When it breaks / Edge cases
- If the problem allows swapping or rearranging elements, intervals are broken, and Interval DP cannot be used (might need Bitmask DP).

## 15. Comparison with alternative approaches
- **Interval DP vs 1D DP:** If the problem only involves making a decision at index $i$ based on $i-1$, use 1D DP. If it involves combining segments, use Interval DP.

---
*Where this shows up in ML:*
Sequence alignment algorithms, parsing algorithms (CYK for context-free grammars).
""")

wc("19-dp-deep-dive/dp-on-trees.md", r"""# DP on Trees

## 1. Definition
DP on Trees (or Tree DP) is a pattern where dynamic programming is performed over the nodes of a tree structure, typically using a post-order Depth First Search (DFS) where a node's state depends on the computed states of its children.

## 2. Intuition
To know the optimal answer for a subtree rooted at node $U$, you first need the optimal answers for all subtrees rooted at $U$'s children. You gather the answers from the children, combine them with $U$'s own value, and return the result to $U$'s parent.

## 3. Why it exists
Trees inherently possess overlapping subproblems and optimal substructure. Many tree problems (like finding the largest independent set, or the maximum path sum) can be solved by deciding whether to include a node based on the optimal decisions made in its subtrees.

## 4. Mechanics
- **Traversal:** Post-order DFS. Process children first, then the parent.
- **State:** Usually `dp[u]` or `dp[u][state]`. For example, in "House Robber III", state is `(include_node, exclude_node)`.
- **Transitions:** At node `u`, iterate through its children `v`. `dp[u]` is updated using `dp[v]`.
- **Rerooting:** A more advanced technique to find the answer for *every* node as the root in $O(N)$ time. Do one bottom-up pass, then one top-down pass to pass the parent's contribution down.

## 5. Complexity (Time & Space)
- **Time:** $O(N)$ because every node and edge is visited a constant number of times.
- **Space:** $O(N)$ for the recursion stack and the DP array.

## 6. Tiny worked example
Tree Diameter (longest path). For a node $U$, the longest path passing through $U$ is `highest_child_depth + second_highest_child_depth`.
DFS returns the max depth of a subtree. As we compute this, we update a global `max_diameter` variable.

## 7. Code (Python)
```python
# House Robber III (Max independent set weight in a tree)
def rob(root):
    # Returns (max_if_robbed, max_if_not_robbed)
    def dfs(node):
        if not node:
            return (0, 0)
            
        left_rob, left_not = dfs(node.left)
        right_rob, right_not = dfs(node.right)
        
        # If we rob this node, we CANNOT rob its children
        rob_this = node.val + left_not + right_not
        
        # If we don't rob this node, we take the max of children (robbed or not)
        not_rob_this = max(left_rob, left_not) + max(right_rob, right_not)
        
        return (rob_this, not_rob_this)
        
    return max(dfs(root))
```

## 8. Common mistakes
- Passing states *down* the tree instead of passing results *up*. Top-down DP with memoization works, but bottom-up (returning tuples from DFS) is usually much cleaner.
- Modifying a global maximum incorrectly (e.g., forgetting that a path can go up through the parent and back down).

## 9. 30-second interview answer
"DP on Trees solves problems by computing optimal states for subtrees. It uses a post-order DFS where a parent node's DP state is calculated by aggregating the DP states returned by its children. It is highly efficient, running in $O(N)$ time, and is used for problems like Tree Diameter or Maximum Path Sum."

## 10. 2-minute interview answer
"Tree DP leverages the strict hierarchical structure of trees. Because there are no cycles, the subproblems are neatly isolated into subtrees. The standard pattern is a post-order DFS: we recursively call the DFS on a node's children, and the children return their optimal states. The parent node then combines these states to form its own optimal state. For example, in calculating the Maximum Path Sum, a node needs to know the maximum straight path down into its left and right subtrees. It combines them to see if the path arching over itself is the global maximum, but only returns the maximum single straight path up to its own parent. A more complex variant is 'Rerooting DP', used when you need to compute an answer for every node acting as the root. Instead of running an $O(N)$ DFS for every node (which is $O(N^2)$), we do it in two $O(N)$ passes: one bottom-up to get subtree answers, and one top-down to pass the remaining graph's answer from parent to child."

## 11. Follow-ups
- "What if the tree is an n-ary tree?" (The logic is identical. Instead of `left` and `right`, you iterate over the `children` array and accumulate the results).

## 12. Deeper questions
- "Explain the two passes of Rerooting DP." (Pass 1 (bottom-up): Compute the DP state for the subtree of every node assuming an arbitrary root, say 0. Pass 2 (top-down): To find the answer for node `v` when rooted at `v`, take the answer for its parent `u` (when rooted at `u`), subtract `v`'s subtree contribution to `u`, and add this remaining tree contribution to `v`'s state).

## 13. Related concepts
- **Graph DFS**: Tree DP is essentially post-order DFS with state combination.
- **State Machine DP**: Nodes often have multiple states (robbed/not robbed).

## 14. When it breaks / Edge cases
- Unusually deep trees (like a linked list) will cause recursion depth limit errors (`RecursionError` in Python). May need to increase recursion limit or use an explicit stack.

## 15. Comparison with alternative approaches
- **Tree DP vs Graph DP:** Trees are Directed Acyclic Graphs (if directed away from root). Tree DP doesn't need a `visited` set if you just pass the `parent` to avoid traversing backward.

---
*Where this shows up in ML:*
Belief propagation in tree-structured probabilistic graphical models.
""")

wc("19-dp-deep-dive/dp-on-graphs.md", r"""# DP on Graphs (DAGs)

## 1. Definition
Dynamic Programming on Graphs involves solving problems on Directed Acyclic Graphs (DAGs) by evaluating nodes in topological order. The DP state of a node depends on the DP states of its incoming or outgoing neighbors.

## 2. Intuition
If all roads go strictly from West to East (a DAG), you can figure out the longest route to a city by looking at all cities immediately West of it, taking their longest routes, and adding the distance to your city. You just have to process the cities in order from West to East.

## 3. Why it exists
Many DP problems can be modeled as finding the shortest/longest path or counting paths in a state-space graph. If the graph has cycles, DP fails because of infinite loops (you need algorithms like Dijkstra). If it's a DAG, DP provides linear time solutions $O(V+E)$.

## 4. Mechanics
Two ways to implement:
- **Memoized DFS:** Start at the target (or source). recursively call DFS on neighbors. Cache the results. The recursion implicitly handles the topological sort.
- **Topological Sort + Iteration:** Compute the in-degrees, use Kahn's algorithm to get a topological order, and then iterate through the order, updating neighbors.

## 5. Complexity (Time & Space)
- **Time:** $O(V + E)$ where $V$ is vertices and $E$ is edges. We visit each node and edge exactly once.
- **Space:** $O(V)$ for the DP array and memoization cache/recursion stack.

## 6. Tiny worked example
Longest path in a DAG.
Graph: A -> B, A -> C, B -> D, C -> D.
`dfs(u)` returns longest path from `u`.
`dfs(D) = 0`
`dfs(B) = 1 + dfs(D) = 1`
`dfs(C) = 1 + dfs(D) = 1`
`dfs(A) = 1 + max(dfs(B), dfs(C)) = 2`

## 7. Code (Python)
```python
# Longest path in a DAG using Memoized DFS
def longest_path(n, edges):
    adj = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        
    memo = {}
    
    def dfs(u):
        if u in memo:
            return memo[u]
            
        max_dist = 0
        for v in adj[u]:
            max_dist = max(max_dist, 1 + dfs(v))
            
        memo[u] = max_dist
        return max_dist
        
    # Check all nodes as possible starting points
    return max(dfs(i) for i in range(n))
```

## 8. Common mistakes
- Trying to use DP on a graph with cycles. If there's a cycle, `dfs(A)` calls `dfs(B)` which calls `dfs(A)`, infinite loop. You MUST ensure it's a DAG.
- Not checking all possible starting nodes if the problem doesn't specify a single source.

## 9. 30-second interview answer
"DP on graphs applies to Directed Acyclic Graphs (DAGs). Because there are no cycles, we can process nodes in topological order. The DP state of a node is calculated from its neighbors. This can be implemented via bottom-up topological sort iteration, or more simply via top-down memoized DFS, both taking $O(V+E)$ time."

## 10. 2-minute interview answer
"Any DP problem can be visualized as a DAG where states are nodes and transitions are directed edges. When dealing with explicit graph problems on DAGs—like finding the longest path or counting the number of paths between two nodes—DP is the optimal approach. Because there are no cycles, there is a strict topological ordering of nodes. We can calculate the optimal state for a node relying entirely on the already-calculated states of its predecessors (or successors). The easiest implementation is a Memoized DFS: when you need the answer for node U, you recursively ask for the answers of its neighbors, pick the best one, and cache it. Because every node is computed once and every edge is traversed once, the time complexity is strictly $O(V+E)$. This is vastly superior to algorithms like Dijkstra or Bellman-Ford, which are necessary for cyclic graphs but carry logarithmic or multiplicative overheads."

## 11. Follow-ups
- "How do you count the total number of paths from node A to node B?" (Base case: `dp[B] = 1`. For others, `dp[u] = sum(dp[v] for v in neighbors(u))`. Evaluate using memoized DFS from A).

## 12. Deeper questions
- "What if the graph has negative weights?" (DP on a DAG handles negative weights effortlessly because it processes in topological order and doesn't rely on greedy choices like Dijkstra. Bellman-Ford is only needed if there are cycles).

## 13. Related concepts
- **Topological Sort**: The underlying ordering that makes DP on DAGs work.
- **State Space Graphs**: The theoretical foundation of all DP.

## 14. When it breaks / Edge cases
- Graphs with cycles. If you need shortest path in a cyclic graph, use BFS (unweighted) or Dijkstra (weighted positive).

## 15. Comparison with alternative approaches
- **DP vs Dijkstra:** Dijkstra is $O(E \log V)$ for cyclic positive graphs. DP is $O(V+E)$ for DAGs (even with negative weights). Always use DP if you know the graph is a DAG.

---
*Where this shows up in ML:*
Markov Decision Processes (MDPs) in Reinforcement Learning, computation graphs in automatic differentiation (backprop is DP on a DAG).
""")

wc("19-dp-deep-dive/dp-with-bitmasking.md", r"""# DP with Bitmasking

## 1. Definition
Bitmask DP is a technique where an integer is used as a bitmask to represent a subset of items (visited cities, available items) as part of the DP state. It is typically used for problems requiring permutations or combinations of small sets ($N \le 20$).

## 2. Intuition
If you have 10 cities to visit, tracking `visited = [True, False, True...]` is clunky and can't be easily used as an array index for a DP table. Instead, use binary: `101...`. The integer `5` (binary `101`) perfectly represents that cities 0 and 2 are visited. The DP state becomes `dp[current_city][bitmask]`.

## 3. Why it exists
Problems like the Traveling Salesperson Problem (TSP) are NP-hard. Brute force permutations take $O(N!)$. Bitmask DP reduces this to $O(N^2 2^N)$ by recognizing overlapping subproblems: reaching city $C$ having visited the same subset of cities has the same future cost, regardless of the exact order the subset was visited in.

## 4. Mechanics
- **Representation:** Node $i$ is represented by the $i$-th bit. `1 << i`.
- **Set bit (visit):** `mask | (1 << i)`.
- **Check bit (is visited?):** `mask & (1 << i) != 0`.
- **Clear bit:** `mask & ~(1 << i)`.
- **State:** `dp[mask][last_node]` = min cost to visit the set of nodes in `mask`, ending at `last_node`.

## 5. Complexity (Time & Space)
- **Time:** $O(2^N \cdot N^2)$. There are $2^N$ masks, $N$ ending nodes, and for each state, we transition by trying to visit the remaining $N$ nodes.
- **Space:** $O(2^N \cdot N)$ to store the DP table. This is why $N$ cannot exceed ~20.

## 6. Tiny worked example
Cities A(0), B(1), C(2). TSP.
Start at A. Mask = `001` (binary) = 1.
State: `dp[1][0]`. 
Transitions:
Go to B: new mask = `011` (3). Cost = `dp[1][0] + dist(A,B)`. Store in `dp[3][1]`.
Go to C: new mask = `101` (5). Cost = `dp[1][0] + dist(A,C)`. Store in `dp[5][2]`.

## 7. Code (Python)
```python
# Traveling Salesperson Problem (Shortest path visiting all nodes)
def tsp(n, dist):
    # dp[mask][i] = min distance visiting subset 'mask' ending at 'i'
    # 1 << n is 2^n
    dp = [[float('inf')] * n for _ in range(1 << n)]
    
    # Base cases: starting at each node
    for i in range(n):
        dp[1 << i][i] = 0
        
    for mask in range(1 << n):
        for u in range(n):
            # If u is in the mask
            if mask & (1 << u):
                for v in range(n):
                    # If v is NOT in the mask, we can transition to it
                    if not (mask & (1 << v)):
                        new_mask = mask | (1 << v)
                        dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])
                        
    # Answer is min cost of full mask (all 1s) ending anywhere
    full_mask = (1 << n) - 1
    return min(dp[full_mask][i] for i in range(n))
```

## 8. Common mistakes
- Confusing bitwise operator precedence. Always use parentheses: `if (mask & (1 << i)) != 0`.
- Doing $O(N!)$ DFS without memoization when a bitmask DP would easily pass. Look at the constraints! If $N \le 20$, think Bitmask.

## 9. 30-second interview answer
"Bitmask DP uses integers to represent subsets of items, turning combinations into hashable, indexable DP states. It reduces factorial time complexities like $O(N!)$ to exponential $O(N^2 2^N)$. The classic example is the Traveling Salesperson Problem, where the state is the current bitmask of visited cities and the last city visited."

## 10. 2-minute interview answer
"Problems that require exploring all permutations usually imply a brute force $O(N!)$ search. However, if the problem exhibits optimal substructure, we can use Bitmask Dynamic Programming. In the Traveling Salesperson Problem, if I have visited cities {A, B, C} and I am currently at C, the minimum cost to visit the remaining cities depends ONLY on the fact that I am at C and the set of remaining cities. It does not matter if I visited them in the order A->B->C or B->A->C. By using a bitmask—an integer where the $i$-th bit is 1 if city $i$ is visited—I can uniquely represent the visited set. The DP state becomes `dp[bitmask][current_city]`. There are $2^N$ possible masks and $N$ possible current cities, and calculating each takes $O(N)$ transitions to unvisited cities. This drops the complexity from $O(N!)$ to $O(2^N \cdot N^2)$. Because $2^{20}$ is about 1 million, this approach is perfectly suited for input sizes around $N \le 20$."

## 11. Follow-ups
- "How do you iterate through all subsets of a given mask?" (Using bitwise logic: `submask = (submask - 1) & mask` inside a while loop allows $O(3^N)$ subset DP).

## 12. Deeper questions
- "What is SOS DP (Sum Over Subsets)?" (A fast way to compute the sum of values for all submasks of every mask. Naively it takes $O(3^N)$, SOS DP does it in $O(N 2^N)$ using a DP similar to multi-dimensional prefix sums).

## 13. Related concepts
- **Graph traversal**: Often applied to graphs (TSP, Hamiltonian Path).
- **Memoized DFS**: Often easier to write Bitmask DP top-down than bottom-up.

## 14. When it breaks / Edge cases
- $N > 20$. $2^{25}$ is 33 million, which starts hitting Time Limit Exceeded. $2^{30}$ is 1 billion and will definitively fail/OOM.

## 15. Comparison with alternative approaches
- **Bitmask DP vs Backtracking:** Backtracking explores the whole $O(N!)$ tree. Bitmask DP merges overlapping branches using memoization.

---
*Where this shows up in ML:*
Combinatorial optimization problems, feature selection algorithms where $N$ is small.
""")

print("Batch E Part 1 complete")
