# Pattern: Union Find

## 1. Definition
The Union-Find pattern utilizes the Disjoint Set data structure to efficiently track and merge connected components in a network, typically to detect cycles or dynamically group elements.

## 2. Intuition
Imagine a room full of strangers. When two people shake hands, they become part of a "network". Instead of everyone remembering everyone else in their network (which takes massive memory), everyone just remembers one "Boss". When two networks merge, the Boss of Network A shakes hands with the Boss of Network B. Now, to check if you and I are in the same network, we just trace up our chains of command and see if we have the same ultimate Boss.

## 3. Why it exists
If edges in a graph are given to you one by one (a stream), using DFS to constantly recalculate "are these two nodes connected?" takes $O(V+E)$ every single time. Union-Find does this in $O(1)$ amortized time.

## 4. Mechanics
1. **Initialize:** An array `parent` where every node is its own boss (`parent[i] = i`).
2. **Find(x):** Trace `parent[x]` up to the root.
   - *Path Compression:* On the way back down, make every node point directly to the root to flatten the tree.
3. **Union(x, y):** Find the roots of `x` and `y`. If they are different, make one root point to the other.
   - *Union by Rank:* Attach the smaller tree to the root of the taller tree to keep the overall tree shallow.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\alpha(N))$ per operation, where $\alpha$ is the inverse Ackermann function. Practically $O(1)$.
- **Space Complexity:** $O(N)$ for the `parent` and `rank` arrays.

## 6. Tiny worked example
Nodes 1, 2, 3.
- `Union(1, 2)`: 1 becomes boss of 2. `parent = {1:1, 2:1, 3:3}`
- Check `Find(2) == Find(3)`: `Find(2)->1`, `Find(3)->3`. Not connected.
- `Union(2, 3)`: Find(2)=1, Find(3)=3. Make 1 boss of 3. `parent = {1:1, 2:1, 3:1}`
- Check `Find(2) == Find(3)`: Both return 1. Connected!

## 7. Code (Python, with type hints)
```python
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False # Already connected (Cycle!)
            
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            
        return True
```

## 8. Common mistakes
- **Ignoring Path Compression:** Without `self.parent[x] = self.find(self.parent[x])`, the trees become unbalanced linked lists, turning $O(1)$ operations into $O(N)$.
- When doing `Union(x, y)`, setting `parent[y] = x` directly instead of setting `parent[root_y] = root_x`. You MUST link the roots, not the child nodes!

## 9. 30-second interview answer
"Union-Find is a pattern for dynamic connectivity. It groups elements into disjoint sets and can instantly answer if two elements are connected. By using Path Compression to flatten the tree during a Find, and Union by Rank to attach trees optimally, it achieves near $O(1)$ amortized time per operation."

## 10. 2-minute interview answer
"The Union-Find pattern is the optimal choice for problems involving dynamic connectivity, grouping items into sets, or detecting cycles in undirected graphs. It bypasses the overhead of heavy BFS/DFS traversals by maintaining a flat array of 'parent' pointers representing tree structures. The power of Union-Find comes from two optimizations. First, Path Compression: whenever we perform a Find, we recursively re-point every node along the path directly to the root, permanently squashing the tree's height. Second, Union by Rank: we explicitly track tree heights and always attach smaller trees under larger ones. Combined, these yield an amortized time complexity of $O(\alpha(N))$, bounded by the Inverse Ackermann function, which is effectively $O(1)$. It is the mathematical backbone of Kruskal's Minimum Spanning Tree algorithm."

## 11. Follow-ups
- "How do you count the number of connected components?" (Count how many nodes have `parent[i] == i`. Every root is exactly one component).

## 12. Deeper questions
- "Can Union-Find handle edge removal?" (No. It fundamentally only merges. If a problem requires edge removal, process the queries in reverse order (time-travel backwards), turning 'removals' into 'unions').

## 13. Related concepts
- **Kruskal's Algorithm**: Relies entirely on Union-Find.
- **Graph Connected Components**: The primary use case.

## 14. When it breaks / Edge cases
- Fails on Directed Graphs (since "connectivity" implies symmetry in Union-Find, but directed edges are one-way).

## 15. Comparison with alternative approaches
- **vs BFS/DFS:** If the graph is fully given upfront and never changes, a single $O(V+E)$ BFS is fine. If edges arrive dynamically (streaming), Union-Find is exponentially faster.

---
*Where this shows up in ML:* 
Used in image segmentation (like the Felzenszwalb-Huttenlocher algorithm) to quickly group adjacent pixels of similar color into cohesive objects.
