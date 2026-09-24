# Breadth-First Search (BFS)

## 1. Definition
Breadth-First Search (BFS) is a traversal algorithm for trees or graphs that explores all neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.

## 2. Intuition
Imagine dropping a stone in a calm pond. The ripples expand outward in perfect concentric circles. BFS works exactly like that: it explores the closest neighbors (distance 1), then the next circle of neighbors (distance 2), expanding evenly in all directions.

## 3. Why it exists
DFS plunges deep down one path, which is terrible if you are looking for the *shortest* path in an unweighted graph. BFS guarantees that the first time you reach a node, you have found the shortest path to it. 

## 4. Mechanics
1. Initialize a **Queue** and a **Visited Set**.
2. Push the starting node to the Queue and mark it as visited.
3. While the Queue is not empty:
   - Pop the front node.
   - Process the node.
   - Loop through its neighbors. If a neighbor is not visited, mark it visited and push it to the Queue.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V + E)$ where $V$ is Vertices and $E$ is Edges. We process every node and every edge once.
- **Space Complexity:** $O(V)$ in the worst case to hold the Queue and the Visited set. (In a tree, the bottom level can hold up to $V/2$ nodes).

## 6. Tiny worked example
Graph: `A - B, A - C, B - D`
1. Queue: `[A]`, Visited: `{A}`
2. Pop `A`. Neighbors: `B`, `C`. Queue: `[B, C]`, Visited: `{A, B, C}`
3. Pop `B`. Neighbors: `A` (visited), `D`. Queue: `[C, D]`, Visited: `{A, B, C, D}`
4. Pop `C`. No unvisited neighbors. Queue: `[D]`
5. Pop `D`. No unvisited neighbors. Done. Order: `A, B, C, D`.

## 7. Code (Python, with type hints)
```python
from typing import List, Dict, Set
from collections import deque

def bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    visited: Set[int] = {start}
    queue: deque = deque([start])
    order: List[int] = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return order
```

## 8. Common mistakes
- Marking nodes as visited *when they are popped* instead of *when they are added to the queue*. If you wait until they are popped, multiple nodes might add the same unvisited neighbor to the queue, causing massive memory bloat and redundancy.
- Using a `list` instead of `collections.deque` for the queue, turning an $O(1)$ pop into an $O(N)$ pop.

## 9. 30-second interview answer
"BFS is a graph and tree traversal algorithm that explores level by level. It uses a Queue to maintain the frontier and a Set to track visited nodes. It runs in $O(V + E)$ time and is the standard algorithm for finding the shortest path in unweighted graphs."

## 10. 2-minute interview answer
"BFS explores an unweighted graph uniformly in all directions, radiating outward. Because it processes all nodes at distance $K$ before any nodes at distance $K+1$, it is mathematically guaranteed to find the shortest path between the start node and any other reachable node. We implement it using a Queue for FIFO processing and a Hash Set to track visited nodes to avoid infinite cycles. A critical implementation detail is marking nodes as visited the moment they are added to the queue, not when they are processed, to prevent the queue from exploding with duplicates. It takes $O(V + E)$ time and $O(V)$ space."

## 11. Follow-ups
- "How do you track the actual shortest path, not just the distance?" (Maintain a `parent` dictionary mapping each neighbor back to the node that discovered it, then backtrack from the target to the start).

## 12. Deeper questions
- "What if the graph has weighted edges?" (BFS fails because the shortest path by edges might not be the shortest by weight. Use Dijkstra's Algorithm, which replaces the standard Queue with a Priority Queue).

## 13. Related concepts
- **Dijkstra's Algorithm**: Weighted BFS.
- **Topological Sort**: Kahn's algorithm is essentially a modified BFS based on in-degrees.

## 14. When it breaks / Edge cases
- Disconnected graphs: BFS only explores the connected component of the start node. You must loop over all vertices to guarantee full traversal.

## 15. Comparison with alternative approaches
- **vs DFS:** BFS uses more memory for wide trees but finds the shortest path. DFS uses less memory (proportional to depth, $O(H)$) and is better for maze-solving or topological sort, but cannot guarantee shortest paths.

---
*Where this shows up in ML:* 
In Knowledge Graphs (used heavily in GenAI RAG pipelines), BFS is used to find entities that are exactly $K$-hops away from a subject entity to expand context.
