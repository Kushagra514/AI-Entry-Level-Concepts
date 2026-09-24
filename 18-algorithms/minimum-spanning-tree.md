# Minimum Spanning Tree (MST)

## 1. Definition
A Minimum Spanning Tree (MST) is a subset of the edges of a connected, edge-weighted, undirected graph that connects all the vertices together without any cycles, minimizing the total edge weight.

## 2. Intuition
Imagine you have 5 cities and want to connect them all to the electrical grid. Laying cable costs money (edge weights). You want to connect every city using the absolute minimum length of cable. You don't care about the shortest path between A and B; you only care about the total system cost. The resulting network is the MST.

## 3. Why it exists
It exists to optimize network design (telecom, electrical grids, road networks). It answers the question: "What is the cheapest way to connect everything?"

## 4. Mechanics
Two famous greedy algorithms:
1. **Kruskal's Algorithm:**
   - Sort all edges by weight.
   - Initialize a Union-Find structure.
   - Iterate through the sorted edges. If the edge connects two nodes not already in the same set, add it to the MST and Union them.
2. **Prim's Algorithm:**
   - Start at any arbitrary node.
   - Use a Min-Heap to track edges connecting the current MST to unvisited nodes.
   - Pop the cheapest edge. If it leads to an unvisited node, add it to the MST, mark visited, and push its edges to the Heap.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Kruskal's: $O(E \log E)$ due to sorting the edges.
  - Prim's: $O(E \log V)$ using a Min-Heap.
- **Space Complexity:** $O(V + E)$ for both (Union-Find arrays or Heaps).

## 6. Tiny worked example
Nodes: A, B, C. Edges: A-B(1), B-C(2), A-C(3).
Kruskal:
- Sort: 1, 2, 3.
- Take A-B (1). Union(A,B).
- Take B-C (2). Union(B,C). All connected!
- Ignore A-C (3) because A and C are already in the same set (it forms a cycle).
Total weight: 3.

## 7. Code (Python, with type hints)
```python
# Kruskal's Implementation
from typing import List, Tuple

class UnionFind:
    # (Implementation omitted for brevity, see Union-Find file)
    pass

def kruskal(n: int, edges: List[Tuple[int, int, int]]) -> int:
    # edges is a list of (weight, u, v)
    edges.sort() 
    uf = UnionFind(n)
    mst_weight = 0
    edges_used = 0
    
    for weight, u, v in edges:
        if uf.union(u, v):
            mst_weight += weight
            edges_used += 1
            if edges_used == n - 1:
                break
                
    return mst_weight
```

## 8. Common mistakes
- Confusing MST with Shortest Path (Dijkstra's). Dijkstra's minimizes distance from a source. MST minimizes the global edge sum.
- Forgetting to check if an edge forms a cycle in Kruskal's (without Union-Find, you will build a graph with cycles instead of a tree).

## 9. 30-second interview answer
"A Minimum Spanning Tree connects all nodes in an undirected, weighted graph with the minimum total edge weight. We solve it using Kruskal's algorithm, which sorts edges and uses Union-Find to avoid cycles, or Prim's algorithm, which builds the tree outward using a Min-Heap. Both operate greedily."

## 10. 2-minute interview answer
"The MST problem asks for the cheapest way to connect all nodes in a network. Because it exhibits the greedy choice property, we solve it using either Kruskal's or Prim's algorithms. I usually default to Kruskal's because it's incredibly easy to implement if you have a Union-Find template. You simply sort all edges by weight—taking $O(E \log E)$ time—and greedily add them to your tree, using Union-Find to skip any edge that would create a cycle. Prim's algorithm operates differently, mimicking Dijkstra's by starting at a single node and using a Min-Heap to continually expand the MST via the cheapest available cut-edge. Prim's is marginally faster on dense graphs ($O(E \log V)$), but Kruskal's is generally cleaner for interview settings."

## 11. Follow-ups
- "When would you prefer Prim's over Kruskal's?" (Prim's is faster on extremely dense graphs where $E \approx V^2$, especially if implemented with a Fibonacci Heap).

## 12. Deeper questions
- "What if all edge weights are identical?" (Any spanning tree is an MST. DFS or BFS can find it in $O(V+E)$).

## 13. Related concepts
- **Union-Find**: Mandatory for Kruskal's.
- **Greedy Algorithms**: The paradigm behind both algorithms.

## 14. When it breaks / Edge cases
- Breaks if the graph is disconnected (you get a Minimum Spanning *Forest* instead).

## 15. Comparison with alternative approaches
- **vs Dijkstra's:** Dijkstra's tree minimizes path lengths from the root. MST minimizes total sum. The two trees are rarely identical.

---
*Where this shows up in ML:* 
MSTs are used in unsupervised learning, specifically in graph-based clustering algorithms (removing the $K-1$ heaviest edges of an MST yields $K$ distinct clusters).
