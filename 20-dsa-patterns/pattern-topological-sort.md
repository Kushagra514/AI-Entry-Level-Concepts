# Pattern: Topological Sort

## 1. Definition
Topological Sort is a pattern used to find a linear ordering of elements that have complex dependencies on one another, ensuring that no element is processed before its prerequisites. It strictly applies to Directed Acyclic Graphs (DAGs).

## 2. Intuition
Imagine getting dressed in the morning. You must put on your socks before your shoes. You must put on your underwear before your pants. Topological sort takes all these individual rules and spits out a valid, chronological sequence (Underwear -> Pants -> Socks -> Shoes) so you don't end up putting your underwear over your pants.

## 3. Why it exists
Problems like task scheduling, course prerequisites, and package manager dependencies present pairs of local constraints (A must precede B). We need a global algorithm that merges all local constraints into one master timeline while mathematically proving whether a timeline is even possible (i.e., no cycles).

## 4. Mechanics (Kahn's Algorithm)
1. **Initialization:** Build an Adjacency List and an `in_degree` array (tracking how many prerequisites each node has).
2. **Queue:** Push all nodes with `in_degree == 0` (no prerequisites) into a Queue.
3. **Process:** Pop a node, add it to the sorted output, and iterate through its neighbors.
4. **Decrement:** For each neighbor, decrement its `in_degree` by 1 (since you just completed one of its prerequisites).
5. **Enqueue:** If a neighbor's `in_degree` reaches 0, push it to the Queue.
6. **Cycle Check:** If the output list length != total nodes, a cycle exists.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V + E)$ where $V$ is tasks and $E$ is dependencies.
- **Space Complexity:** $O(V + E)$ for the Adjacency List, In-Degree array, and Queue.

## 6. Tiny worked example
Courses: 0, 1, 2. Prerequisites: `[1,0]` (0 before 1), `[2,0]` (0 before 2).
- `in_degree`: 0:0, 1:1, 2:1.
- Queue: `[0]`.
- Pop 0. Output: `[0]`. Neighbors: 1, 2.
- 1's `in_degree` becomes 0. Push 1.
- 2's `in_degree` becomes 0. Push 2.
- Pop 1, Pop 2. Output: `[0, 1, 2]`.

## 7. Code (Python, with type hints)
```python
from collections import deque, defaultdict
from typing import List

def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    # Build Graph
    for dest, src in prerequisites:
        graph[src].append(dest)
        in_degree[dest] += 1
        
    # Start with nodes having no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    top_order = []
    
    # Process
    while queue:
        node = queue.popleft()
        top_order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # Cycle detection
    return top_order if len(top_order) == numCourses else []
```

## 8. Common mistakes
- **Graph Building Direction:** Reversing the edge direction. If taking course $A$ is a prerequisite for $B$, the edge must be $A \rightarrow B$, not the other way around.
- **Skipping Isolated Nodes:** If a node has no edges at all, its `in_degree` is 0. It must be included in the initial Queue.

## 9. 30-second interview answer
"The Topological Sort pattern is used to linearly order items that have dependencies. Using Kahn's Algorithm, we track the 'in-degree' of every node, process nodes with zero dependencies via a Queue, and sequentially unlock their neighbors. It runs in $O(V+E)$ time and inherently detects cyclic impossibilities."

## 10. 2-minute interview answer
"Whenever an interview question asks to 'find a valid order', 'schedule tasks', or 'compile dependencies', it is a Topological Sort problem on a Directed Acyclic Graph. The most robust implementation is Kahn's Algorithm using BFS. We first translate the dependencies into an Adjacency List while tracking the 'in-degree'—the number of prerequisites—for every node. We push all independent nodes (in-degree 0) into a Queue. As we process each node, we simulate 'completing' that task by decrementing the in-degree of its neighbors. Once a neighbor's in-degree hits 0, it is fully unlocked and pushed to the Queue. The beauty of Kahn's is its built-in cycle detection: if there is a mutual dependency (A needs B, B needs A), they will never reach an in-degree of 0, and the final output array will be shorter than the total number of nodes."

## 11. Follow-ups
- "Can you solve this with DFS?" (Yes. Traverse to the deepest leaf, mark it visited, push it to a Stack. Return the reversed Stack. Requires a 3-state visited array: Unvisited, Visiting, Visited, to detect cycles).

## 12. Deeper questions
- "How do you find if a sequence of words constitutes a valid 'Alien Dictionary'?" (Compare adjacent words to find the first differing letter, treat that as a directed edge, build the graph, and Topological Sort it).

## 13. Related concepts
- **Graphs**: Topological Sort is a graph algorithm.
- **BFS**: The engine of Kahn's Algorithm.

## 14. When it breaks / Edge cases
- Disconnected components or isolated tasks. Kahn's handles them perfectly because they initialize with `in_degree == 0` and are instantly processed.

## 15. Comparison with alternative approaches
- **DFS vs Kahn's:** Kahn's (BFS) is slightly easier to reason about for cycle detection and can easily process tasks in parallel groupings (everything in the queue at one level can be executed simultaneously).

---
*Where this shows up in ML:* 
The order of operations in PyTorch's execution graph is determined by a topological sort.
