# DSA Complexity Cheat Sheet

## Data Structure Operations — Time Complexity

| Data Structure | Access | Search | Insert | Delete | Space |
|---|---|---|---|---|---|
| Array | $O(1)$ | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ |
| Dynamic Array (list) | $O(1)$ | $O(N)$ | $O(1)$* amortized | $O(N)$ | $O(N)$ |
| Linked List (singly) | $O(N)$ | $O(N)$ | $O(1)$ head | $O(N)$ | $O(N)$ |
| Stack | $O(N)$ | $O(N)$ | $O(1)$ push | $O(1)$ pop | $O(N)$ |
| Queue | $O(N)$ | $O(N)$ | $O(1)$ enqueue | $O(1)$ dequeue | $O(N)$ |
| Deque | $O(N)$ | $O(N)$ | $O(1)$ both ends | $O(1)$ both ends | $O(N)$ |
| Hash Map (avg) | $O(1)$ | $O(1)$ | $O(1)$* | $O(1)$* | $O(N)$ |
| Hash Map (worst) | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ |
| Hash Set | — | $O(1)$ avg | $O(1)$ avg | $O(1)$ avg | $O(N)$ |
| Binary Search Tree (balanced) | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| BST (unbalanced/worst) | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ | $O(N)$ |
| Min/Max Heap | $O(1)$ peek | $O(N)$ | $O(\log N)$ push | $O(\log N)$ pop | $O(N)$ |
| Heapify (build heap) | — | — | $O(N)$ all at once | — | $O(N)$ |
| Trie | $O(L)$ | $O(L)$ | $O(L)$ | $O(L)$ | $O(N \cdot L)$ |
| Union-Find | — | $O(\alpha(N))$ | $O(\alpha(N))$ | N/A | $O(N)$ |
| Segment Tree | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(4N)$ |
| Fenwick Tree | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| Deque (collections.deque) | $O(N)$ mid | — | $O(1)$ ends | $O(1)$ ends | $O(N)$ |

*Amortized

## Sorting Algorithm Complexity

| Algorithm | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| Bubble Sort | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | ✅ |
| Selection Sort | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | ❌ |
| Insertion Sort | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | ✅ |
| Merge Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | ✅ |
| Quick Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | ❌ |
| Heap Sort | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | ❌ |
| Counting Sort | $O(N+K)$ | $O(N+K)$ | $O(N+K)$ | $O(K)$ | ✅ |
| Radix Sort | $O(dN)$ | $O(dN)$ | $O(dN)$ | $O(N+K)$ | ✅ |
| Timsort (Python) | $O(N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | ✅ |

## Graph Algorithm Complexity

| Algorithm | Time | Space | Use Case |
|---|---|---|---|
| BFS | $O(V+E)$ | $O(V)$ | Shortest path (unweighted), level order |
| DFS | $O(V+E)$ | $O(V)$ | Cycle detection, topological sort |
| Dijkstra | $O((V+E)\log V)$ | $O(V)$ | Shortest path (non-negative weights) |
| Bellman-Ford | $O(VE)$ | $O(V)$ | Shortest path (negative weights) |
| Floyd-Warshall | $O(V^3)$ | $O(V^2)$ | All-pairs shortest path |
| Kruskal's MST | $O(E \log E)$ | $O(V)$ | Minimum Spanning Tree |
| Prim's MST | $O(E \log V)$ | $O(V)$ | Minimum Spanning Tree |
| Topological Sort | $O(V+E)$ | $O(V)$ | DAG ordering |

## Input Size → Allowed Complexity

| Max N | Max Complexity | Common Approach |
|---|---|---|
| $N \leq 10$ | $O(N!)$ | Backtracking, Permutations |
| $N \leq 20$ | $O(2^N)$ | Bitmask DP, Subsets |
| $N \leq 500$ | $O(N^3)$ | Floyd-Warshall, 3D DP |
| $N \leq 5000$ | $O(N^2)$ | 2D DP, LIS |
| $N \leq 10^5$ | $O(N \log N)$ | Sorting, Binary Search, Heaps |
| $N \leq 10^6$ | $O(N)$ | Two Pointers, Sliding Window, Hash Map |
| $N \leq 10^9$ | $O(\log N)$ | Binary Search, Math |

## DP Pattern Complexity Summary

| Problem Type | Time | Space | Optimizable? |
|---|---|---|---|
| 1D DP (Fibonacci, House Robber) | $O(N)$ | $O(N)$ | $O(1)$ with rolling vars |
| 2D DP (LCS, Edit Distance) | $O(NM)$ | $O(NM)$ | $O(\min(N,M))$ rows |
| 0/1 Knapsack | $O(NC)$ | $O(NC)$ | $O(C)$ 1D array |
| Interval DP (Matrix Chain) | $O(N^3)$ | $O(N^2)$ | No |
| Bitmask DP (TSP) | $O(2^N \cdot N^2)$ | $O(2^N \cdot N)$ | No |
| Tree DP | $O(N)$ | $O(N)$ | No |

---
> **Quick Rule:** If the problem says $O(\log N)$ and the array is sorted → Binary Search. If "Top K" → Heap. If "subarray/substring" → Sliding Window. If "all combinations" → Backtracking.
