# Topological Sort

## 1. Definition
Topological Sort is a linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge $U \rightarrow V$, vertex $U$ comes before $V$ in the ordering.

## 2. Intuition
Think of a college prerequisite system. You can't take Calculus 2 until you finish Calculus 1. Topological sort gives you a valid semester-by-semester schedule so you never violate a prerequisite.

## 3. Why it exists
It exists to resolve dependency resolution problems. From compiling code (Makefiles) to scheduling tasks, we need an algorithmic way to find a valid chronological execution order.

## 4. Mechanics
Two standard approaches:
1. **Kahn's Algorithm (BFS based):**
   - Calculate the `in-degree` (number of incoming edges) for all nodes.
   - Put all nodes with `in-degree == 0` into a Queue.
   - Pop a node, append to output, and reduce the `in-degree` of its neighbors by 1.
   - If a neighbor's `in-degree` hits 0, push it to the Queue.
2. **DFS based:**
   - Run DFS. When a node has NO unvisited neighbors (i.e., it finishes), push it to a Stack.
   - The topological order is the Stack popped in reverse.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V + E)$ - We visit every node and edge once.
- **Space Complexity:** $O(V + E)$ to store the graph and arrays for in-degrees/stack.

## 6. Tiny worked example
Edges: `A -> C`, `B -> C`, `C -> D`.
- In-degrees: A:0, B:0, C:2, D:1.
- Queue: `[A, B]`.
- Pop `A`. Decrease `C` in-degree to 1.
- Pop `B`. Decrease `C` in-degree to 0. Push `C`.
- Pop `C`. Decrease `D` in-degree to 0. Push `D`.
- Result: `[A, B, C, D]`.

## 7. Code (Python, with type hints)
```python
from collections import deque, defaultdict
from typing import List

def topological_sort(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    adj = defaultdict(list)
    in_degree = [0] * numCourses
    
    for dest, src in prerequisites:
        adj[src].append(dest)
        in_degree[dest] += 1
        
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []
    
    while queue:
        curr = queue.popleft()
        order.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    if len(order) == numCourses:
        return order
    return [] # Cycle detected!
```

## 8. Common mistakes
- Applying it to a graph with cycles. Topological sort is mathematically impossible if a cycle exists (e.g., A needs B, B needs A).
- In Kahn's algorithm, forgetting to check if the final output length equals $V$. If it doesn't, a cycle exists.

## 9. 30-second interview answer
"Topological Sort provides a linear ordering of nodes in a Directed Acyclic Graph honoring all edge dependencies. I implement it using Kahn's algorithm (BFS with in-degrees) or a DFS with a post-order stack. It runs in $O(V+E)$ time and is perfect for scheduling or prerequisite problems."

## 10. 2-minute interview answer
"Whenever a problem involves 'tasks with prerequisites', it is a Topological Sort problem. It requires a Directed Acyclic Graph (DAG). I prefer Kahn's Algorithm because it uses BFS and an in-degree array, making it extremely easy to detect cycles: if the final sorted array has fewer elements than the total number of vertices, a cycle prevented the queue from processing everything. Alternatively, we can use DFS, pushing nodes to a stack only after all their descendants are fully explored, then reversing the stack. Both methods operate in $O(V+E)$ time. Kahn's algorithm is often more extensible if we need to process independent tasks simultaneously, as everything in the queue at a given moment can be executed in parallel."

## 11. Follow-ups
- "Can there be multiple valid topological sorts for one graph?" (Yes, any independent nodes can be ordered arbitrarily).

## 12. Deeper questions
- "How do you find the lexicographically smallest topological sort?" (In Kahn's algorithm, replace the standard Queue with a Min-Priority Queue/Heap).

## 13. Related concepts
- **Directed Acyclic Graphs (DAG)**: The only graph type this works on.
- **Cycle Detection**: Kahn's implicitly detects cycles.

## 14. When it breaks / Edge cases
- Breaks immediately if the graph contains a cycle.

## 15. Comparison with alternative approaches
- **DFS vs BFS (Kahn's):** Kahn's is usually preferred because explicit cycle detection via array length is simpler than tracking back-edges with a 3-state visited array in DFS.

---
*Where this shows up in ML:* 
Computational graphs (like PyTorch Autograd or TensorFlow XLA) compile operations using a Topological Sort to ensure that the outputs of layer $N$ are computed before they are fed as inputs to layer $N+1$.
