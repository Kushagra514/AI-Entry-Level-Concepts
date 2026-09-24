# Graphs

## 1. Definition
A Graph is a non-linear data structure consisting of nodes (vertices) and the connections between them (edges), which can be directed or undirected, weighted or unweighted.

## 2. Intuition
Think of a social network. You (a vertex) are connected to your friends (edges). If friendship is mutual, it's an undirected graph (Facebook). If you can follow someone without them following you back, it's a directed graph (Twitter). 

## 3. Why it exists
Trees are restricted graphs (hierarchical, no cycles). Graphs exist to model complex, real-world networks where any entity can be connected to any other entity in arbitrary ways (maps, internet routing, social connections).

## 4. Mechanics
Two primary ways to represent graphs in memory:
1. **Adjacency Matrix:** A 2D array of size $V \times V$. `matrix[i][j] = 1` if edge exists. $O(1)$ lookup, $O(V^2)$ space. Good for dense graphs.
2. **Adjacency List:** A Hash Map or Array of Lists. `list[i] = [j, k]`. $O(E)$ lookup, $O(V+E)$ space. Good for sparse graphs (most common in interviews).

## 5. Complexity (Time & Space)
- **Time Complexity:** Traversals (BFS/DFS) take $O(V + E)$ using an Adjacency List.
- **Space Complexity:** $O(V + E)$ for an Adjacency List.

## 6. Tiny worked example
Nodes: 0, 1, 2. Edges: 0-1, 1-2.
Adjacency List:
```python
{
  0: [1],
  1: [0, 2],
  2: [1]
}
```

## 7. Code (Python, with type hints)
```python
from collections import defaultdict
from typing import List, Dict

class Graph:
    def __init__(self):
        self.adj_list: Dict[int, List[int]] = defaultdict(list)
        
    def add_edge(self, u: int, v: int, directed: bool = False):
        self.adj_list[u].append(v)
        if not directed:
            self.adj_list[v].append(u)
```

## 8. Common mistakes
- Forgetting to track `visited` nodes during traversal, resulting in infinite loops (Stack Overflow or OOM) due to cycles.
- Using an Adjacency Matrix for a massive, sparse graph, causing Memory Limit Exceeded (e.g., $10^5$ nodes needs a $10^{10}$ matrix, which is 10GB of RAM).

## 9. 30-second interview answer
"A graph represents relationships between entities using vertices and edges. We typically represent them using an Adjacency List to save memory ($O(V+E)$ space). We traverse them using BFS for shortest-path problems and DFS for deep exploration or cycle detection, always maintaining a 'visited' set to prevent infinite loops."

## 10. 2-minute interview answer
"Graphs are the most generalized data structure for modeling networks. Because they lack the strict rules of trees (they can have cycles and multiple parents), traversing them requires explicit state tracking via a `visited` set. In interviews, 99% of graphs are sparse, meaning we model them using Adjacency Lists to achieve $O(V+E)$ space and time traversals. The choice of algorithm depends heavily on the graph's properties: we use BFS for unweighted shortest paths, DFS for topological sorting or cycle detection, Dijkstra's for weighted shortest paths, and Union-Find for dynamic connectivity in undirected graphs. Recognizing whether a problem is implicitly a graph (e.g., a 2D matrix maze or word transformations) is half the battle."

## 11. Follow-ups
- "What is a Bipartite Graph?" (A graph whose vertices can be divided into two disjoint sets such that every edge connects a vertex in Set U to one in Set V. Detectable via 2-color BFS/DFS).

## 12. Deeper questions
- "How do you find Strongly Connected Components in a directed graph?" (Kosaraju's Algorithm or Tarjan's Algorithm, which use specialized DFS passes).

## 13. Related concepts
- **BFS & DFS**: The standard algorithms.
- **Topological Sort**: Ordering a DAG.

## 14. When it breaks / Edge cases
- Disconnected components: A single traversal might not hit every node. You must loop over all vertices to initiate traversals.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Graph Neural Networks (GNNs) operate directly on graph structures, passing messages between nodes. Also, the computational graph in PyTorch (Autograd) is a Directed Acyclic Graph (DAG) used to trace backpropagation.
