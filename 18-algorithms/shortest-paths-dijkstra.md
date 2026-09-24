# Dijkstra's Algorithm

## 1. Definition
Dijkstra's Algorithm is a greedy graph search algorithm that finds the shortest path from a single source node to all other nodes in a graph with **non-negative** edge weights.

## 2. Intuition
Imagine a network of water pipes with different lengths (weights). If you turn on the water at the source, it flows evenly in all directions at the same speed. The water will reach the closest intersections first. Dijkstra's mathematically simulates this water flow using a Priority Queue.

## 3. Why it exists
BFS finds the shortest path in *unweighted* graphs by jumping level-by-level. If edges have weights (e.g., mileage between cities), BFS fails. Dijkstra's generalizes BFS to account for edge weights by prioritizing the next closest node overall, rather than just the next layer.

## 4. Mechanics
1. Create a `distances` hash map initialized to $\infty$ for all nodes, except the start node (distance = 0).
2. Use a Min-Heap (Priority Queue) storing `(distance, node)`, initialized with `(0, start)`.
3. While the heap is not empty:
   - Pop the node with the smallest distance. If its popped distance is greater than the known `distances[node]`, skip it (stale entry).
   - For each neighbor, calculate `new_dist = curr_dist + edge_weight`.
   - If `new_dist < distances[neighbor]`, update the distance and push `(new_dist, neighbor)` to the heap.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O((V + E) \log V)$. Processing all edges, and each heap push/pop takes $\log V$.
- **Space Complexity:** $O(V + E)$ for the graph, plus $O(V)$ for the Heap and distances map.

## 6. Tiny worked example
Nodes: `A, B, C`. Edges: `A->B (4)`, `A->C (1)`, `C->B (2)`. Source: `A`.
- Heap: `[(0, A)]`. Dist: `A:0, B:inf, C:inf`.
- Pop A. Update neighbors. Heap: `[(1, C), (4, B)]`. Dist: `A:0, B:4, C:1`.
- Pop C (smallest). Update neighbors (B). `new_dist = 1+2 = 3`. $3 < 4$.
- Heap: `[(3, B), (4, B)]`. Dist: `A:0, B:3, C:1`.
- Pop B (3). Update neighbors (none).
- Pop B (4) - stale! Skip. Done.

## 7. Code (Python, with type hints)
```python
import heapq
from typing import List, Dict, Tuple

def dijkstra(n: int, edges: List[Tuple[int, int, int]], start: int) -> Dict[int, int]:
    adj = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))
        
    distances = {i: float('inf') for i in range(n)}
    distances[start] = 0
    min_heap = [(0, start)]
    
    while min_heap:
        curr_dist, u = heapq.heappop(min_heap)
        
        # Optimization: ignore stale heap entries
        if curr_dist > distances[u]:
            continue
            
        for v, weight in adj[u]:
            dist = curr_dist + weight
            if dist < distances[v]:
                distances[v] = dist
                heapq.heappush(min_heap, (dist, v))
                
    return distances
```

## 8. Common mistakes
- **Using a standard Queue:** This turns it into an inefficient BFS. You *must* use a Priority Queue / Min-Heap.
- **Forgetting the stale entry check:** `if curr_dist > distances[u]: continue`. Without this, the algorithm will redundantly process old paths, drastically increasing time complexity.

## 9. 30-second interview answer
"Dijkstra's is a greedy algorithm for finding the shortest path in a weighted graph. It uses a Min-Heap to continually expand the closest known node. It runs in $O((V+E)\log V)$ time but strictly requires all edge weights to be non-negative."

## 10. 2-minute interview answer
"Dijkstra's Algorithm is essentially BFS for weighted graphs. Because edges have varying costs, expanding level-by-level doesn't guarantee the shortest path. Instead, we use a Min-Heap to always expand the node with the absolute lowest cumulative cost from the source. This greedy choice guarantees optimality as long as there are no negative weights. The core logic involves 'relaxing' edges—if we find a cheaper way to reach a neighbor, we update its known distance and push it to the heap. A crucial implementation detail in Python is handling duplicate nodes in the heap. Since Python's `heapq` doesn't support `decrease-key`, we just push duplicate nodes and use a 'stale check' on pop to ignore outdated distances, yielding an $O((V+E)\log V)$ time complexity."

## 11. Follow-ups
- "Why does Dijkstra's fail with negative weights?" (Because the greedy assumption—that the current shortest path to a node can never be improved by taking a longer route—breaks if a longer route contains a massive negative weight).

## 12. Deeper questions
- "What is A* (A-star) search?" (It's Dijkstra's algorithm with a heuristic function added to the heap priority, guiding the search toward the target rather than expanding uniformly in all directions).

## 13. Related concepts
- **Bellman-Ford**: The $O(V \times E)$ alternative that handles negative weights.
- **Prim's Algorithm**: Extremely similar structure, but for Minimum Spanning Trees.

## 14. When it breaks / Edge cases
- Breaks on graphs with negative edge weights.

## 15. Comparison with alternative approaches
- **vs BFS:** BFS is faster ($O(V+E)$) but only works for unweighted graphs.

---
*Where this shows up in ML:* 
Conceptually similar to Viterbi decoding (finding the most likely path). In robotics and autonomous driving (AI path planning), Dijkstra's (and its heuristic extension A*) is fundamental.
