# Union Find / Disjoint Set

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
