# Bellman-Ford Algorithm

## 1. Definition
Bellman-Ford is a single-source shortest path algorithm that, unlike Dijkstra's, correctly handles graphs with **negative edge weights** and can detect **negative-weight cycles**.

## 2. Intuition
Imagine a city map where some roads give you cash back (negative weight — e.g., toll rebates). Dijkstra's greedily picks the "cheapest so far" exit and never revisits it, so it would miss the rebate. Bellman-Ford instead tries every possible road $V-1$ times, systematically relaxing all estimates until they converge to truth.

## 3. Why it exists
Dijkstra's greedy assumption ("the currently closest node will never get closer") breaks with negative weights. Bellman-Ford sacrifices speed for correctness, operating in $O(V \times E)$ time to guarantee correct shortest paths even with negative edges.

## 4. Mechanics
1. Initialize `dist[source] = 0`, all others `= infinity`.
2. Repeat $V-1$ times:
   - For every edge $(u, v, w)$: if `dist[u] + w < dist[v]`, update `dist[v] = dist[u] + w`.
3. **Negative Cycle Detection:** Run one more iteration. If any distance still updates, a negative-weight cycle exists.

**Why $V-1$ iterations?** The shortest path between any two vertices in a graph with $V$ nodes uses at most $V-1$ edges (otherwise it visits a node twice, implying a cycle).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V \times E)$. For dense graphs this is $O(V^3)$, far slower than Dijkstra's $O((V+E) \log V)$.
- **Space Complexity:** $O(V)$ for the distance array.

## 6. Tiny worked example
Nodes: A, B, C. Edges: `A->B (4)`, `A->C (5)`, `B->C (-6)`.
- Init: `A=0, B=inf, C=inf`.
- Pass 1: Relax `A->B`: `B=4`. Relax `A->C`: `C=5`. Relax `B->C`: `C = min(5, 4-6) = -2`.
- Pass 2: No further updates. Done. Shortest to C = -2.

## 7. Code (Python, with type hints)
```python
from typing import List, Tuple

def bellman_ford(n: int, edges: List[Tuple[int, int, int]], src: int):
    dist = [float('inf')] * n
    dist[src] = 0

    # Relax all edges V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Detect negative cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # Negative cycle exists

    return dist
```

## 8. Common mistakes
- Stopping after fewer than $V-1$ iterations on a sparse graph. The algorithm *requires* $V-1$ full passes regardless of apparent convergence (unless you add an early-exit optimization tracking whether any update occurred in a pass).
- Confusing "negative weight edge" (fine for Bellman-Ford) with "negative weight cycle" (makes shortest paths undefined and infinitely negative).

## 9. 30-second interview answer
"Bellman-Ford finds single-source shortest paths in $O(V \times E)$ time and, unlike Dijkstra's, handles negative edge weights. It relaxes all edges $V-1$ times and detects negative cycles with one extra pass. It's slower than Dijkstra's but necessary for graphs with negative edges."

## 10. 2-minute interview answer
"Bellman-Ford solves the single-source shortest path problem without the non-negative weight constraint that cripples Dijkstra's. It works by systematically relaxing every edge in the graph, repeating $V-1$ times. The intuition is that any shortest path in a graph of $V$ nodes uses at most $V-1$ edges. So after $k$ iterations, `dist[v]` holds the shortest path using at most $k$ edges. By $V-1$ iterations, all simple shortest paths have been discovered. The $(V)^{th}$ iteration serves as a negative-cycle detector: if any distance still decreases, it means a negative cycle exists and true shortest paths are undefined. While $O(V \times E)$ is significantly slower than Dijkstra's, Bellman-Ford is the correct choice for any graph where edge weights can be negative."

## 11. Follow-ups
- "What is SPFA (Shortest Path Faster Algorithm)?" (A queue-based optimization of Bellman-Ford. Only enqueue vertices whose distances were just updated. Average case $O(E)$, worst case still $O(VE)$).

## 12. Deeper questions
- "What is the Floyd-Warshall algorithm?" (An $O(V^3)$ DP algorithm that finds all-pairs shortest paths, not just from a single source. Also handles negative weights and detects negative cycles).

## 13. Related concepts
- **Dijkstra's Algorithm**: The faster alternative when weights are non-negative.
- **Floyd-Warshall**: The all-pairs generalization.

## 14. When it breaks / Edge cases
- If a negative cycle is reachable from the source, shortest paths are $-\infty$ along that cycle. The algorithm correctly reports the cycle but cannot compute finite distances.

## 15. Comparison with alternative approaches
- **vs Dijkstra's:** Dijkstra's is $O((V+E)\log V)$ but requires non-negative weights. Bellman-Ford is $O(VE)$ but handles all weights. Always prefer Dijkstra's when weights are guaranteed non-negative.

---
*Where this shows up in ML:*
In distributed systems and networking (BGP routing protocol for the internet uses a variant of Bellman-Ford). Also relevant for reward propagation in tabular Reinforcement Learning with negative rewards.
