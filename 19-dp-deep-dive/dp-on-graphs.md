# DP on Graphs (DAGs)

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
