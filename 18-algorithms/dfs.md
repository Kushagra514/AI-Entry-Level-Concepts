# Depth-First Search (DFS)

## 1. Definition
Depth-First Search (DFS) is a traversal algorithm for trees or graphs that explores as far as possible along each branch before backtracking.

## 2. Intuition
Imagine exploring a massive maze. You pick a path and run down it as fast as you can. When you hit a dead end, you back up to the last intersection and try the next path. You keep plunging deep until you explore everything.

## 3. Why it exists
DFS exists to explore all possible configurations or paths in a search space. Because it relies on a stack (or recursion) rather than a wide queue, it is highly memory efficient for deep, branching structures compared to BFS.

## 4. Mechanics
1. Start at a node and mark it as visited.
2. Iterate through its neighbors.
3. If a neighbor hasn't been visited, recursively call DFS on that neighbor.
4. When all neighbors are explored, the function returns (backtracks).
*(Can also be implemented iteratively using an explicit Stack).*

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V + E)$ - We visit every vertex and evaluate every edge exactly once.
- **Space Complexity:** $O(V)$ worst-case for the call stack (in a linked-list-like graph). In a balanced tree, space is $O(\log V)$ for the height.

## 6. Tiny worked example
Graph: `A - B, A - C, B - D`
1. Start `A`. Mark `{A}`. Visit neighbor `B`.
2. At `B`. Mark `{A, B}`. Visit neighbor `D`.
3. At `D`. Mark `{A, B, D}`. No unvisited neighbors. Backtrack to `B`.
4. At `B`. No more unvisited neighbors. Backtrack to `A`.
5. At `A`. Visit neighbor `C`.
6. At `C`. Mark `{A, B, D, C}`. Done. Order: `A, B, D, C`.

## 7. Code (Python, with type hints)
```python
from typing import List, Dict, Set

def dfs_recursive(graph: Dict[int, List[int]], start: int, visited: Set[int] = None) -> List[int]:
    if visited is None:
        visited = set()
        
    visited.add(start)
    order = [start]
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            # Recursively explore deep
            order.extend(dfs_recursive(graph, neighbor, visited))
            
    return order
```

## 8. Common mistakes
- Forgetting to maintain a `visited` set for graphs, resulting in infinite recursion (Stack Overflow) if there's a cycle. (Trees don't need a visited set because they are acyclic directed).
- Thinking DFS will find the shortest path. It absolutely does not; it finds the *first* path.

## 9. 30-second interview answer
"DFS is a traversal algorithm that plunges as deep as possible into a graph before backtracking. It is typically implemented recursively, leveraging the call stack. It runs in $O(V + E)$ time and requires $O(H)$ space where $H$ is the max depth, making it memory-efficient for deep trees. It's ideal for cycle detection and topological sorting."

## 10. 2-minute interview answer
"DFS is the standard algorithm for exhaustive search and backtracking problems. By aggressively traversing down a single path until it terminates, it mimics human maze-solving. We implement it recursively, which inherently utilizes the OS call stack, or iteratively with an explicit Stack. For graphs, tracking visited nodes in a Hash Set is mandatory to prevent infinite loops on cycles. While BFS is required for shortest-path problems, DFS is vastly superior for cycle detection (by tracking the current recursion stack), Topological Sorting, and exploring permutations/combinations in backtracking, because its space complexity is bound by the maximum depth $O(H)$, rather than the maximum width."

## 11. Follow-ups
- "How do you detect a cycle using DFS?" (Pass an additional `current_path` set into the recursion. If you see a node that is in `current_path`, you have a back-edge, hence a cycle).
- "How do you implement DFS iteratively?" (Use a Stack. Push start, pop, mark visited, push neighbors).

## 12. Deeper questions
- "If a tree is highly unbalanced, what is the risk of recursive DFS?" (Stack Overflow. Python's recursion limit is usually 1000. An iterative stack on the heap is safer).

## 13. Related concepts
- **Backtracking**: Essentially DFS applied to an abstract state-space tree.
- **Topological Sort**: Done using DFS by pushing nodes to a stack *after* all their children are explored.

## 14. When it breaks / Edge cases
- Stack Overflow on deep graphs.
- Disconnected components require an outer loop over all vertices to trigger DFS.

## 15. Comparison with alternative approaches
- **vs BFS:** DFS uses less memory on wide trees and is easier to write (just recursion). BFS finds shortest paths and prevents getting "stuck" down an infinitely deep branch.

---
*Where this shows up in ML:* 
In PyTorch/TensorFlow, calculating gradients via Backpropagation is mathematically an application of the Chain Rule executed via a Depth-First Search post-order traversal over the computational graph.
