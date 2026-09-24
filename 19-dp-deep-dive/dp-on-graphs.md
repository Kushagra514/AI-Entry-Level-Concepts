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
