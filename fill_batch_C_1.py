import os

def write_and_commit(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch C)"')

files = {}

files["17-data-structures/union-find-disjoint-set.md"] = r"""# Union Find / Disjoint Set

## 1. Definition
Union-Find is a data structure that tracks a set of elements partitioned into a number of disjoint (non-overlapping) subsets, optimizing for two operations: Find (determining which subset an element is in) and Union (joining two subsets).

## 2. Intuition
Imagine a group of people forming friend circles. Everyone starts alone. When A and B become friends, they form a circle (Union). To check if A and Z are in the same circle, we find the "leader" of A's circle and the "leader" of Z's circle (Find). If the leaders are the same, they are in the same circle.

## 3. Why it exists
Standard graph traversals like BFS/DFS can find connected components, but they take $O(V+E)$ time. If edges are being added dynamically and we need to repeatedly check connectivity, BFS/DFS is too slow. Union-Find does this in nearly $O(1)$ amortized time.

## 4. Mechanics
- **Initialization:** An array `parent` where `parent[i] = i`.
- **Find:** Recursively follow `parent` pointers until `parent[i] == i`.
  - *Path Compression:* While returning, make all nodes on the path point directly to the root, flattening the tree.
- **Union:** Find roots of both elements. If different, make one root point to the other.
  - *Union by Rank/Size:* Always attach the smaller tree under the root of the larger tree to keep the tree shallow.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\alpha(N))$ amortized for Find and Union, where $\alpha$ is the Inverse Ackermann function (effectively $\le 4$, i.e., $O(1)$).
- **Space Complexity:** $O(N)$ for the parent and rank/size arrays.

## 6. Tiny worked example
Sets: `{1}`, `{2}`, `{3}`
Union(1, 2): `{1, 2}`, `{3}`. `parent[2] = 1`.
Find(2): follows `parent[2]` -> returns `1`.

## 7. Code (Python, with type hints)
```python
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, p: int) -> int:
        # Path compression
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p: int, q: int) -> bool:
        rootP = self.find(p)
        rootQ = self.find(q)
        if rootP == rootQ: return False # Cycle detected

        # Union by rank
        if self.rank[rootP] > self.rank[rootQ]:
            self.parent[rootQ] = rootP
        elif self.rank[rootP] < self.rank[rootQ]:
            self.parent[rootP] = rootQ
        else:
            self.parent[rootQ] = rootP
            self.rank[rootP] += 1
        return True
```

## 8. Common mistakes
- Forgetting Path Compression in `find()`, causing the tree to become a linked list ($O(N)$ time).
- Confusing the element itself with its root during a `union` (e.g., doing `parent[q] = p` instead of `parent[rootQ] = rootP`).

## 9. 30-second interview answer
"Union-Find is a data structure for keeping track of disjoint sets. Using an underlying array, it supports nearly $O(1)$ amortized Union and Find operations by leveraging Path Compression and Union by Rank. It is the optimal structure for dynamic connectivity and detecting cycles in undirected graphs."

## 10. 2-minute interview answer
"Union-Find is the ultimate dynamic connectivity structure. While DFS/BFS can find connected components statically, Union-Find handles streaming edge additions efficiently. It uses an array to represent trees of connected elements. By implementing Path Compression—where nodes point directly to the root after a Find—and Union by Rank—where smaller trees are attached to larger ones—the height of the trees remains infinitesimally small. This gives operations an amortized time complexity of $O(\alpha(N))$, which is practically $O(1)$. It's the engine behind Kruskal's Minimum Spanning Tree algorithm and the best way to detect cycles in undirected graphs."

## 11. Follow-ups
- "Can Union-Find handle edge deletions?" (No, it only merges. Edge deletion requires a completely different approach or rolling back states).

## 12. Deeper questions
- "What is the Inverse Ackermann function?" (A function that grows so slowly that for any conceivable $N$ in the universe, $\alpha(N) \le 4$. Thus, it is practically $O(1)$).

## 13. Related concepts
- **Kruskal's Algorithm**: Uses Union-Find to sort and add edges safely.
- **Graphs**: Connected components.

## 14. When it breaks / Edge cases
- Cannot easily represent directed graphs or track edge removals.

## 15. Comparison with alternative approaches
- **vs BFS/DFS:** BFS/DFS is better for static graph analysis. Union-Find is better for dynamic edge additions.

---
*Where this shows up in ML:* 
Used in hierarchical clustering algorithms (like Single Linkage clustering) to efficiently merge clusters.
"""

files["17-data-structures/tries.md"] = r"""# Tries (Prefix Trees)

## 1. Definition
A Trie is an N-ary tree data structure used for efficiently storing and retrieving strings over a finite alphabet, where each node represents a single character.

## 2. Intuition
Think of a physical dictionary. You don't read every word to find "Apple". You flip to 'A', then go to 'P', then 'P'. A Trie maps this exact physical process into a tree structure, sharing the prefix "APP" for both "Apple" and "Application".

## 3. Why it exists
Searching for a prefix in a Hash Set of strings takes $O(N)$ time (since hashes don't preserve partial string matches). A Trie allows $O(L)$ prefix searching (where $L$ is word length) while compressing storage by sharing common prefixes.

## 4. Mechanics
- **Node:** Contains a Hash Map or Array of child nodes (e.g., size 26 for English letters) and a boolean `is_end_of_word`.
- **Insert:** Traverse the tree character by character. Create nodes for missing characters. Mark the last node as `is_end`.
- **Search:** Traverse character by character. If a character is missing, it doesn't exist. If you reach the end of the word, check `is_end`.
- **StartsWith:** Same as Search, but return `True` without checking `is_end`.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(L)$ for Insert, Search, and StartsWith, where $L$ is the length of the word. Independent of the number of words stored.
- **Space Complexity:** $O(N \times L)$ in the worst case (no shared prefixes), but heavily compressed in practice.

## 6. Tiny worked example
Insert "CAT" and "CAR".
- Root -> C -> A -> T (is_end=True)
- Insert "CAR": Root -> C (exists) -> A (exists) -> R (create, is_end=True).
Both words share the "CA" nodes.

## 7. Code (Python, with type hints)
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end = True

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return True
```

## 8. Common mistakes
- Forgetting the `is_end_of_word` flag, which makes it impossible to distinguish if "APP" is a word in the dictionary or just a prefix of "APPLE".
- Using an array of size 256 for children when a Hash Map is more memory efficient for sparse trees.

## 9. 30-second interview answer
"A Trie is a prefix tree used for string storage. It provides $O(L)$ time complexity for insertions and prefix searches, where $L$ is word length, beating Hash Sets for prefix operations. It is the core structure for autocomplete and spell checkers."

## 10. 2-minute interview answer
"Tries are specialized N-ary trees designed for string retrieval. While a Hash Set can find an exact word in $O(1)$ time, it completely fails at prefix matching (e.g., 'give me all words starting with auto-'). Tries solve this by storing characters hierarchically, implicitly sharing common prefixes. This yields $O(L)$ time for insertions and lookups, which is optimal. The main tradeoff is space; while prefix sharing saves memory, the pointer overhead for nodes can be massive compared to a flat array. In practice, Tries are the definitive choice for autocomplete systems, IP routing (longest prefix match), and word games like Boggle."

## 11. Follow-ups
- "How do you optimize a Trie's memory?" (Use a Radix Tree / Compressed Trie, which merges nodes with a single child into a single node holding a string).

## 12. Deeper questions
- "How does Aho-Corasick algorithm relate to Tries?" (It builds a Trie of search terms and adds 'failure links' (like KMP), allowing multiple substring searches simultaneously in $O(N)$ time).

## 13. Related concepts
- **Hash Maps**: The alternative for exact word matching.
- **Prefix Match**: The primary use case.

## 14. When it breaks / Edge cases
- Massive memory bloat if the alphabet is large (e.g., all Unicode characters) and there are no shared prefixes.

## 15. Comparison with alternative approaches
- **vs Hash Set:** Hash Set is $O(L)$ to hash a word, but takes more memory to store exact string copies and cannot do `startsWith` queries.

---
*Where this shows up in ML:* 
LLM Tokenizers (like WordPiece or BPE) often use Tries under the hood to efficiently match character sequences against the token vocabulary during the encoding phase.
"""

files["17-data-structures/graphs.md"] = r"""# Graphs

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
"""

files["18-algorithms/topological-sort.md"] = r"""# Topological Sort

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
"""

files["18-algorithms/shortest-paths-dijkstra.md"] = r"""# Dijkstra's Algorithm

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
"""

files["18-algorithms/minimum-spanning-tree.md"] = r"""# Minimum Spanning Tree (MST)

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
"""

files["16-dsa-foundations/bit-manipulation.md"] = r"""# Bit Manipulation

## 1. Definition
Bit manipulation involves applying logical operations directly to the individual bits (0s and 1s) of binary numbers to achieve highly optimized computational tasks.

## 2. Intuition
Instead of using math operators like `+`, `-`, `*`, or `/`, you act like an electrician flipping microscopic switches. Because CPUs execute these bitwise operations at the hardware level in a single clock cycle, it is the fastest possible way to compute certain mathematical or logical relationships.

## 3. Why it exists
It exists to maximize performance and minimize memory. Storing 32 boolean flags in an array takes 32 bytes. Storing them in a single 32-bit integer takes 4 bytes. Hardware drivers, cryptography, and ultra-optimized algorithmic solutions rely heavily on bits.

## 4. Mechanics
- **AND (`&`):** 1 if both bits are 1. Used to mask/extract bits.
- **OR (`|`):** 1 if either bit is 1. Used to set bits.
- **XOR (`^`):** 1 if bits are different. $x \oplus x = 0$. $x \oplus 0 = x$.
- **NOT (`~`):** Flips all bits.
- **Left Shift (`<<`):** Shifts bits left, filling with 0. Equivalent to multiplying by $2^k$.
- **Right Shift (`>>`):** Shifts bits right. Equivalent to integer division by $2^k$.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(1)$ for single operations.
- **Space Complexity:** $O(1)$.

## 6. Tiny worked example
Is a number even or odd?
Math: `n % 2 == 0`. (Division is a slow CPU instruction).
Bitwise: `n & 1 == 0`. (Fast).
If `n = 6` (110 in binary): `110 & 001 = 000` (Even).
If `n = 5` (101 in binary): `101 & 001 = 001` (Odd).

## 7. Code (Python, with type hints)
```python
def bit_tricks(n: int) -> int:
    # Is Even?
    is_even = (n & 1) == 0
    
    # Multiply by 2
    mult2 = n << 1
    
    # Clear the lowest set bit (useful for counting 1s)
    # 1010 -> 1000
    n = n & (n - 1)
    
    # Toggle the i-th bit
    i = 2
    n = n ^ (1 << i)
    
    return n
```

## 8. Common mistakes
- **Precedence errors:** Bitwise operators have very low precedence in Python/C++. Always wrap them in parentheses. E.g., `n & 1 == 0` evaluates as `n & (1 == 0)` in some languages, not `(n & 1) == 0`.
- Forgetting that negative numbers in Python have an infinite number of leading 1s (because Python has arbitrary-precision integers), making operations like `~` tricky without explicit 32-bit masking (`n & 0xFFFFFFFF`).

## 9. 30-second interview answer
"Bit manipulation leverages low-level CPU instructions like AND, OR, XOR, and Shifts to solve problems with maximum efficiency. It's commonly used to represent sets of booleans in $O(1)$ space, calculate powers of 2, or cancel out duplicate elements using the XOR property."

## 10. 2-minute interview answer
"Bit manipulation is an advanced optimization technique that replaces arithmetic with raw logical circuitry operations. The most critical operator in interviews is XOR (`^`), because of its cancellation property: $x \oplus x = 0$. This solves the classic 'Single Number' problem in $O(N)$ time and $O(1)$ space. Another vital pattern is using integers as 'Bitmasks' to represent subsets; a 32-bit integer can act as a Hash Set of 32 boolean flags, radically compressing DP states. Finally, Brian Kernighan’s algorithm `n & (n - 1)` drops the lowest set bit, allowing us to count 1-bits in time proportional to the number of set bits, rather than the total bits."

## 11. Follow-ups
- "How do you swap two variables without a temporary variable?" (`a = a^b`, `b = a^b`, `a = a^b`).

## 12. Deeper questions
- "How do you isolate the rightmost 1-bit?" (`n & -n`. Two's complement makes `-n` equal to `~n + 1`).

## 13. Related concepts
- **DP with Bitmasking**: Uses integers to track subset states.

## 14. When it breaks / Edge cases
- Python handles negative numbers differently than C++/Java because it lacks a fixed 32-bit limit, so you often need to manually mask with `0xFFFFFFFF`.

## 15. Comparison with alternative approaches
- **vs Modulo/Division:** Bitwise AND/Shifts are significantly faster on the CPU level.

---
*Where this shows up in ML:* 
In ultra-low precision Deep Learning (e.g., 1-bit or 2-bit quantization, BitNet), matrix multiplications are replaced entirely by bitwise XNOR and POPCOUNT operations, drastically accelerating hardware inference.
"""

files["20-dsa-patterns/pattern-fast-slow-pointers.md"] = r"""# Pattern: Fast and Slow Pointers

## 1. Definition
Fast and Slow Pointers (also known as Floyd's Tortoise and Hare) is an algorithm that uses two pointers moving through a sequence at different speeds to detect cycles or find midpoints.

## 2. Intuition
Imagine two runners on a track. One runs at 1x speed (slow), the other at 2x speed (fast). If the track is a straight line, the fast runner finishes and the race ends. But if the track is a circle, the fast runner will eventually lap the slow runner and they will meet. 

## 3. Why it exists
Detecting cycles in a Linked List usually requires a Hash Set to track visited nodes, taking $O(N)$ space. Floyd's algorithm solves this in $O(1)$ space.

## 4. Mechanics
- **Cycle Detection:** Initialize `slow = head` and `fast = head`. Loop: `slow = slow.next`, `fast = fast.next.next`. If `slow == fast`, there is a cycle.
- **Find Midpoint:** When `fast` reaches the end of the list, `slow` will be exactly at the midpoint (because it travels half as fast).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - In the worst case, the fast pointer traverses the list a constant number of times.
- **Space Complexity:** $O(1)$ - Only two pointers are used.

## 6. Tiny worked example
List: 1 -> 2 -> 3 -> 4 -> 5 -> (points back to 3)
- Step 0: S=1, F=1
- Step 1: S=2, F=3
- Step 2: S=3, F=5
- Step 3: S=4, F=4 (Collision! Cycle detected).

## 7. Code (Python, with type hints)
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head: ListNode) -> bool:
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
            
    return False
```

## 8. Common mistakes
- **Null Reference Errors:** Forgetting to check `while fast and fast.next:`. If you only check `while fast:`, calling `fast.next.next` will throw an error when `fast.next` is None.
- Over-complicating cycle math. 

## 9. 30-second interview answer
"The Fast and Slow pointer technique uses two pointers moving at different speeds to process sequences. It is primarily used on Linked Lists to detect cycles using $O(1)$ space via Floyd's algorithm, or to find the midpoint of a list in a single pass."

## 10. 2-minute interview answer
"Floyd's Tortoise and Hare is the definitive pattern for Linked List topology problems. By advancing one pointer by one step and another by two steps, we gain profound insights in $O(N)$ time and $O(1)$ space. If the sequence has an end, the fast pointer hits a null reference, and the slow pointer perfectly rests at the midpoint—this is essential for algorithms like Merge Sort on linked lists. If the sequence has a cycle, the relative distance between the two pointers decreases by one step each iteration, guaranteeing they will collide inside the loop. A beautiful extension of this is finding the exact start of the cycle: after a collision, if you reset one pointer to the head and move both at 1x speed, they will magically collide exactly at the cycle entrance."

## 11. Follow-ups
- "How do you mathematically prove they will meet exactly at the cycle entrance?" (Let distance to cycle be $x$. Distance inside cycle to meeting point be $y$. Fast traveled $2(x+y)$, Slow traveled $x+y$. The remaining distance is exactly $x$).

## 12. Deeper questions
- "Can you use this pattern to find duplicate numbers in an array?" (Yes! If array values are in the range `[1, n]`, you can treat the array as a Linked List where `arr[i]` points to `arr[arr[i]]`. Finding the cycle entrance finds the duplicate in $O(1)$ space).

## 13. Related concepts
- **Two Pointers**: The parent category of this pattern.
- **Linked Lists**: The primary data structure.

## 14. When it breaks / Edge cases
- Fails or errors out on empty lists or single-node lists without cycles if null checks are missing.

## 15. Comparison with alternative approaches
- **vs Hash Set:** Hash Set takes $O(N)$ space but can detect cycles immediately. Fast/Slow takes $O(1)$ space but takes slightly longer as it must traverse the loop until collision.

---
*Where this shows up in ML:* 
While not directly used in ML math, understanding topological loops is relevant for verifying Directed Acyclic Graphs (DAGs) in computation graphs.
"""

files["20-dsa-patterns/pattern-merge-intervals.md"] = r"""# Pattern: Merge Intervals

## 1. Definition
The Merge Intervals pattern is used to solve problems involving overlapping scheduling, time ranges, or coordinates by sorting them and sequentially merging overlapping bounds.

## 2. Intuition
Imagine a hotel reservation book. Someone books a room from Monday to Wednesday. Another books Tuesday to Thursday. To find out when the room is occupied, you sort the bookings by start day. You see Monday overlaps with Tuesday, so you combine them into a single "occupied" block from Monday to Thursday.

## 3. Why it exists
Brute forcing interval overlaps requires comparing every interval to every other interval ($O(N^2)$). By sorting them first, any overlapping intervals are guaranteed to be strictly adjacent to each other, allowing us to process them in a single linear pass.

## 4. Mechanics
1. **Sort:** Sort the list of intervals strictly by their **start time**.
2. **Initialize:** Push the first interval into a `merged` results list.
3. **Iterate:** For each subsequent interval, compare its `start` time to the `end` time of the last interval in the `merged` list.
4. **Merge:** If `start <= end`, they overlap. Update the `end` of the merged interval to be the `max(current_end, new_end)`.
5. **Add:** If they don't overlap, append the new interval to the `merged` list.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \log N)$ heavily dominated by the initial sorting step. The merge pass is $O(N)$.
- **Space Complexity:** $O(N)$ to hold the sorted output array (or $O(\log N)$ for the sorting algorithm overhead).

## 6. Tiny worked example
Intervals: `[[1,3], [8,10], [2,6], [15,18]]`
- Sort: `[[1,3], [2,6], [8,10], [15,18]]`
- `merged = [[1,3]]`
- Check `[2,6]`. 2 <= 3. Overlap! Update end to `max(3, 6) = 6`. `merged = [[1,6]]`.
- Check `[8,10]`. 8 > 6. No overlap. `merged = [[1,6], [8,10]]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # Check for overlap
        if current[0] <= last_merged[1]:
            last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
            
    return merged
```

## 8. Common mistakes
- Forgetting to sort the array first.
- Merging the end times incorrectly by just taking the second interval's end time. E.g., merging `[1, 10]` and `[2, 5]` should yield `[1, 10]`, requiring `max(10, 5)`.
- Confusing "Merge Intervals" (sort by start time) with "Activity Selection / Greedy Interval Scheduling" (sort by end time).

## 9. 30-second interview answer
"The Merge Intervals pattern efficiently combines overlapping ranges. It requires sorting the intervals by their start times first, which takes $O(N \log N)$. Then, in a single $O(N)$ pass, we merge adjacent intervals if the current start time is less than or equal to the previous end time."

## 10. 2-minute interview answer
"Whenever a problem deals with timeframes, meetings, or continuous ranges, the Merge Intervals pattern is the standard approach. The core insight is that by sorting the intervals by their starting boundary, any intervals that overlap are forced to be adjacent in the sorted array. This allows us to reduce an $O(N^2)$ cross-check into an $O(N \log N)$ sort followed by a simple $O(N)$ linear scan. During the scan, we maintain a running list of merged blocks. If the next interval's start time falls within the previous block's end time, we merge them by extending the end time to the maximum of both boundaries. If not, we seal the block and start a new one."

## 11. Follow-ups
- "What if the intervals are a stream of data and you can't sort them upfront?" (You use a self-balancing BST (like a TreeMap in Java) to maintain sorted order on insertions, making each insert/merge $O(\log N)$).

## 12. Deeper questions
- "How do you find the intersection of two lists of disjoint intervals?" (Use Two Pointers, one on each list. The overlap is `[max(start1, start2), min(end1, end2)]`).

## 13. Related concepts
- **Sweep Line Algorithm**: A more advanced 1D variant for intervals, counting overlapping layers (+1 for start, -1 for end).

## 14. When it breaks / Edge cases
- Intervals that touch at the exact boundary (e.g., `[1,2]` and `[2,3]`). You must clarify with the interviewer if touching counts as overlapping (`<=` vs `<`).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Time-series data processing often requires merging irregularly sampled sensor data windows.
"""

files["20-dsa-patterns/pattern-monotonic-stack.md"] = r"""# Pattern: Monotonic Stack

## 1. Definition
A Monotonic Stack is a stack whose elements are guaranteed to be strictly increasing or strictly decreasing. It is used to find the "Next Greater" or "Next Smaller" element in an array in $O(N)$ time.

## 2. Intuition
Imagine a line of people of varying heights looking to their right. You want to know who is the first person taller than you. If someone behind you is shorter than you, they are totally irrelevant because anyone looking right will see *you* before they see the shorter person. A monotonic stack naturally "hides" these irrelevant shorter people, maintaining only the relevant tall people in order.

## 3. Why it exists
Finding the "Next Greater Element" with nested loops takes $O(N^2)$. A Monotonic Stack prunes the search space by aggressively discarding elements that can no longer be the answer, reducing the problem to $O(N)$ time.

## 4. Mechanics
To find the **Next Greater Element**:
1. Iterate through the array.
2. While the stack is not empty AND the current element is *greater* than the top of the stack:
   - Pop the top element. The current element is the "Next Greater" answer for the popped element.
3. Push the current element (or its index) onto the stack.
*Result: The stack remains monotonically decreasing.*

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - Every element is pushed exactly once and popped at most once.
- **Space Complexity:** $O(N)$ - For the stack.

## 6. Tiny worked example
Array: `[2, 1, 5, 3]`
- `2`: Stack `[2]`.
- `1`: $1 \not> 2$. Push. Stack `[2, 1]`.
- `5`: $5 > 1$. Pop `1`. (Next greater for 1 is 5). 
       $5 > 2$. Pop `2`. (Next greater for 2 is 5). 
       Push 5. Stack `[5]`.
- `3`: $3 \not> 5$. Push. Stack `[5, 3]`.
(Elements left in stack have no greater element).

## 7. Code (Python, with type hints)
```python
from typing import List

def next_greater_elements(nums: List[int]) -> List[int]:
    n = len(nums)
    res = [-1] * n
    stack = [] # Stores INDICES, not values
    
    for i in range(n):
        # While stack has items and current element is strictly greater
        while stack and nums[i] > nums[stack[-1]]:
            popped_idx = stack.pop()
            res[popped_idx] = nums[i]
            
        stack.append(i)
        
    return res
```

## 8. Common mistakes
- Storing **values** in the stack instead of **indices**. You usually need the index to map the answer back to the output array.
- Confusing whether to use a Monotonic Increasing or Decreasing stack. (Rule of thumb: Looking for Next Greater -> Decreasing Stack. Next Smaller -> Increasing Stack).

## 9. 30-second interview answer
"A Monotonic Stack maintains elements in a strictly increasing or decreasing order. It is the optimal $O(N)$ pattern for finding the 'Next Greater' or 'Next Smaller' element. By popping elements that violate the monotonic property, it efficiently resolves pending queries."

## 10. 2-minute interview answer
"The Monotonic Stack is a specialized application of the LIFO principle used to optimize $O(N^2)$ range queries down to $O(N)$ time. It solves 'Next Greater Element' problems—like finding the next warmer day in a list of temperatures. As we iterate, we push indices onto the stack. If we encounter a value that breaks the monotonic property (e.g., a larger value when maintaining a decreasing stack), we know we have found the exact 'Next Greater' answer for the elements currently on the stack. We pop them off, record the answer, and push the new element. Because every element is pushed and popped exactly once, the time complexity is strictly linear."

## 11. Follow-ups
- "What if the array is circular?" (Loop through the array twice `range(2 * n)`, using `i % n` for the index).

## 12. Deeper questions
- "How does this apply to the 'Largest Rectangle in Histogram' problem?" (You use an increasing monotonic stack to find the Next Smaller and Previous Smaller elements simultaneously, which defines the boundaries of the rectangle for each bar).

## 13. Related concepts
- **Stacks**: The underlying data structure.
- **Sliding Window Maximum**: Uses a Monotonic *Deque*.

## 14. When it breaks / Edge cases
- Repeated elements (e.g., `[2, 2, 2]`) must be handled carefully with strictly greater `>` vs greater-than-equal `>=` depending on problem constraints.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Not heavily used in ML modeling, but crucial in systems engineering and competitive programming.
"""

files["20-dsa-patterns/pattern-two-heaps.md"] = r"""# Pattern: Two Heaps

## 1. Definition
The Two Heaps pattern uses a Max-Heap and a Min-Heap together to continuously track the median (or another percentile) of a stream of numbers.

## 2. Intuition
Imagine sorting a stream of numbers and drawing a line exactly down the middle. Everything on the left is the lower half, and you only care about the largest number there (Max-Heap). Everything on the right is the upper half, and you only care about the smallest number there (Min-Heap). The median is right at the boundary between the two heaps.

## 3. Why it exists
Sorting an array every time a new number arrives to find the median takes $O(N \log N)$ per insert. The Two Heaps pattern reduces the insertion time to $O(\log N)$ and the median retrieval time to $O(1)$.

## 4. Mechanics
- **Max-Heap (Lower Half):** Stores the smaller half of the numbers. The root is the largest of the small numbers.
- **Min-Heap (Upper Half):** Stores the larger half of the numbers. The root is the smallest of the large numbers.
- **Insertion:** Add to Max-Heap. Pop from Max-Heap and push to Min-Heap (to guarantee elements in Min-Heap are larger). If Min-Heap is larger than Max-Heap, pop from Min and push to Max to balance sizes.
- **Balance:** Max-Heap size must equal Min-Heap size (even count), or be exactly 1 larger (odd count).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\log N)$ for insertion, $O(1)$ to find the median.
- **Space Complexity:** $O(N)$ to store all elements in the heaps.

## 6. Tiny worked example
Insert `[3, 1, 5]`.
- Add 3: Max=`[3]`, Min=`[]`. Median = 3.
- Add 1: Max=`[3, 1]`. Pop 3 to Min. Max=`[1]`, Min=`[3]`. Median = (1+3)/2 = 2.
- Add 5: Max=`[1, 5]`. Pop 5 to Min. Max=`[1]`, Min=`[3, 5]`. Unbalanced! Pop 3 to Max. Max=`[3, 1]`, Min=`[5]`. Median = 3.

## 7. Code (Python, with type hints)
```python
import heapq

class MedianFinder:
    def __init__(self):
        # Python heapq is min-heap. Multiply by -1 for max-heap.
        self.small = [] # Max-Heap (lower half)
        self.large = [] # Min-Heap (upper half)

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        
        # Ensure max of small is <= min of large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
            
        # Balance sizes (small can be 1 larger, but not vice versa)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

## 8. Common mistakes
- Forgetting to invert numbers when using Python's `heapq` for the Max-Heap.
- Failing to balance the heaps correctly (e.g., pushing to Max, but the number was actually larger than the Min-Heap's root, violating the boundary).

## 9. 30-second interview answer
"The Two Heaps pattern elegantly maintains the median of a data stream in $O(\log N)$ time. We use a Max-Heap for the smaller half of numbers and a Min-Heap for the larger half. By keeping their sizes balanced, the median is always instantly accessible at the roots in $O(1)$ time."

## 10. 2-minute interview answer
"To find a dynamic median efficiently, we must split the sorted representation of the data perfectly in half. We achieve this using the Two Heaps pattern. The lower half of the data is stored in a Max-Heap, meaning the largest of the small numbers is always at the top. The upper half is stored in a Min-Heap. Upon inserting a new number, we first push it to the Max-Heap, then immediately pop the Max-Heap's root and push it to the Min-Heap. This guarantees that all numbers in the Min-Heap are strictly greater than those in the Max-Heap. Finally, we balance the heap sizes so the Max-Heap is equal to or exactly one element larger than the Min-Heap. Finding the median is an $O(1)$ peek at the roots, completely bypassing the $O(N \log N)$ cost of sorting a stream."

## 11. Follow-ups
- "What if you needed the 90th percentile instead of the median?" (Adjust the size balancing logic so the Max-Heap holds 90% of the elements and the Min-Heap holds 10%).

## 12. Deeper questions
- "How do you solve Sliding Window Median?" (It's Two Heaps, plus you need to remove elements that fall out of the window. Since heap removal is $O(N)$, you use 'lazy deletion' by keeping a hash map of expired elements and skipping them when they surface at the root).

## 13. Related concepts
- **Heaps / Priority Queues**: The underlying structures.
- **Sliding Window**: Often combined.

## 14. When it breaks / Edge cases
- Stream problems require memory. If the stream is infinite, $O(N)$ space will eventually cause OOM.

## 15. Comparison with alternative approaches
- **vs Binary Search Tree:** A balanced BST can also find the median dynamically, but Heaps are cache-friendly arrays and significantly easier to implement error-free in an interview.

---
*Where this shows up in ML:* 
Percentile tracking during streaming distributed training or analyzing latency percentiles (P50, P99) in MLOps monitoring.
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch C - Sub-pass 1 Complete")
