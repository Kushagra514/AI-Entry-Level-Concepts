# DSA Patterns Cheat Sheet

## Keyword → Pattern → Data Structure

| Problem Keywords | Pattern | Primary Data Structure | Time |
|---|---|---|---|
| Sorted array + target | Two Pointers / Binary Search | Array | $O(N)$ or $O(\log N)$ |
| Contiguous subarray + max/min | Sliding Window | Array + Two Pointers | $O(N)$ |
| Top K / Kth largest | Heap | Min-Heap or Max-Heap | $O(N \log K)$ |
| Next greater element | Monotonic Stack | Stack | $O(N)$ |
| Overlapping intervals | Merge Intervals | Sort + Array | $O(N \log N)$ |
| Cycle in linked list | Fast & Slow Pointers | Linked List | $O(N)$ |
| Combinations / Permutations | Backtracking | Recursion + Path Array | $O(2^N)$ |
| Maximize / Minimize with overlap | Dynamic Programming | Array or 2D Table | Varies |
| Connected components | BFS / DFS | Graph + Visited Set | $O(V+E)$ |
| Task dependencies | Topological Sort | DAG + In-degree Array | $O(V+E)$ |
| Dynamic connectivity | Union-Find | Parent Array | $O(\alpha N)$ |
| Numbers in range 1-N | Cyclic Sort | Array | $O(N)$ |
| All subsets of set | Subsets Backtracking | Path List | $O(2^N)$ |
| Find missing / duplicate | Hash Set / XOR / Cyclic Sort | Hash Set | $O(N)$ |
| Shortest path unweighted | BFS | Queue | $O(V+E)$ |
| Shortest path weighted | Dijkstra | Min-Heap | $O((V+E)\log V)$ |
| Shortest path negative weights | Bellman-Ford | Edge List | $O(VE)$ |
| Min Spanning Tree | Kruskal / Prim | Union-Find / Heap | $O(E \log E)$ |
| Two-sum variants | Hash Map | Hash Map | $O(N)$ |
| String prefix matching | Trie | Trie | $O(L)$ |
| Range sum queries (static) | Prefix Sum | Array | $O(1)$ query |
| Range queries + updates | Segment Tree / Fenwick | Tree | $O(\log N)$ |
| Min/Max in sliding window | Monotonic Deque | Deque | $O(N)$ |
| Median of stream | Two Heaps | Max-Heap + Min-Heap | $O(\log N)$ |
| Binary search on answer | Binary Search + Greedy check | N/A | $O(N \log(\text{Range}))$ |
| Check sorted array split | Rotated Binary Search | Array | $O(\log N)$ |

## Pattern Identification Flowchart

```
Problem has...
├── Array + sorted + O(log N) hint → Binary Search
├── Array + target sum + sorted → Two Pointers  
├── Substring/subarray + window → Sliding Window
├── "Top K" → Min-Heap of size K
├── Intervals with start/end → Merge Intervals (sort by start)
├── Linked list with cycle detection → Fast/Slow Pointers
├── All possible combinations → Backtracking
│   └── With overlap in subproblems → +Memoization = DP
├── Graph + connectivity → BFS/DFS
│   ├── Dynamic edge additions → Union-Find
│   └── Task ordering → Topological Sort
├── Maximize/minimize over index → 1D DP
├── Maximize/minimize over two strings → 2D DP (LCS/Edit Distance)
└── Subset over range 1 to N → Cyclic Sort
```

## Two-Pointer Patterns

| Variant | When | Example |
|---|---|---|
| Left + Right converging | Sorted array, pair sum | Two Sum II |
| Both from left (fast/slow) | Cycle detection, midpoint | Linked List Cycle |
| Both from left (same dir) | Sliding window count | Count of Subarrays |

## Sliding Window Variants

| Variant | Template | Example |
|---|---|---|
| Fixed size window | Maintain window of size K | Max sum of K elements |
| Variable size (max window) | Expand right, shrink left when invalid | Longest substring without repeat |
| Variable size (min window) | Shrink left as soon as valid | Minimum window substring |

## Backtracking Template

```python
def backtrack(start, path):
    if goal_reached(path):
        result.append(path.copy())
        return
    for choice in choices(start):
        path.append(choice)       # Choose
        backtrack(next, path)     # Explore
        path.pop()                # Un-choose
```

## DP State Definition Quick Guide

| Problem Type | State Definition | Base Case |
|---|---|---|
| 1D sequence | `dp[i]` = optimal at index `i` | `dp[0]` = first element |
| 2D grid | `dp[i][j]` = optimal at cell `(i,j)` | `dp[0][0]` = start |
| Two strings | `dp[i][j]` = optimal for `s1[:i]`, `s2[:j]` | `dp[0][j]` = j deletions |
| Knapsack | `dp[i][c]` = max value using items `[0..i]` with capacity `c` | `dp[0][c]` = item 0 if fits |
| Bitmask | `dp[mask][i]` = optimal for visited set `mask`, at node `i` | `dp[1][0]` = start node |
| Interval | `dp[i][j]` = optimal for range `[i,j]` | `dp[i][i]` = single element |

## Common Pitfalls Quick Reference

| Mistake | Symptom | Fix |
|---|---|---|
| `result.append(path)` not copy | All results empty at end | `result.append(path[:])` |
| Queue with `list.pop(0)` | $O(N^2)$ BFS | Use `collections.deque` |
| Knapsack inner loop forward | Items reused (Unbounded) | Iterate capacity backwards |
| No `visited` in graph DFS | Infinite loop / stack overflow | Always use `visited` set |
| `while fast.next.next` | NullPointer on non-cycle | Check `fast and fast.next` |
| Binary search: `lo = mid` | Infinite loop | Use `lo = mid + 1` |
