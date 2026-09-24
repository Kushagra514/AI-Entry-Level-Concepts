# Bitmask DP

## 1. Core Idea
Represent a subset of N elements as an integer bitmask (bit i = 1 means element i is in set).
State: dp[mask][i] = optimal answer for subset `mask`, currently at node i.

## 2. Complexity
O(2^N · N²) time, O(2^N · N) space. Feasible for N ≤ 20.

## 3. Bit Operations Cheat Sheet
```python
mask | (1<<i)    # add element i
mask & ~(1<<i)   # remove element i
mask & (1<<i)    # check if i in mask
mask ^ (1<<i)    # toggle i
bin(mask).count('1')  # popcount
(mask-1) & mask  # remove lowest set bit
```

## 4. TSP — Traveling Salesman Problem
```python
def tsp(dist, n):
    INF = float('inf')
    dp = [[INF]*n for _ in range(1<<n)]
    dp[1][0] = 0   # start at node 0, mask=0001
    for mask in range(1<<n):
        for u in range(n):
            if dp[mask][u] == INF: continue
            if not (mask >> u & 1): continue
            for v in range(n):
                if mask >> v & 1: continue   # v not yet visited
                nmask = mask | (1<<v)
                dp[nmask][v] = min(dp[nmask][v], dp[mask][u] + dist[u][v])
    full = (1<<n) - 1
    return min(dp[full][v] + dist[v][0] for v in range(n))
```

## 5. Assign Tasks to Workers (LC 1986 style)
dp[mask] = min time to finish subset `mask` of tasks.
Enumerate last completed task and worker assignment.

## 6. Minimum Number of People to Teach (subset DP)
Enumerate all language subsets for teams; dp[mask] = can team cover all queries.

## 7. Partition to K Equal Subset Sums (LC 698)
```python
def canPartitionKSubsets(nums, k):
    total = sum(nums)
    if total % k: return False
    target = total // k
    nums.sort(reverse=True)
    dp = [False] * (1 << len(nums))
    cur_sum = [0] * (1 << len(nums))
    dp[0] = True
    for mask in range(1 << len(nums)):
        if not dp[mask]: continue
        for i, num in enumerate(nums):
            if mask >> i & 1: continue
            nmask = mask | (1<<i)
            if cur_sum[mask] % target + num <= target:
                dp[nmask] = True
                cur_sum[nmask] = cur_sum[mask] + num
    return dp[(1<<len(nums))-1]
```

## 8. Minimum Cost to Connect All Points (not bitmask — Prim's), but if N≤15 use bitmask Steiner tree.

## 9. Counting Hamiltonian Paths
dp[mask][v] = number of paths visiting exactly the nodes in `mask`, ending at v.
Base: dp[1<<v][v] = 1 for all v. Transition same as TSP.

## 10. Profile DP (Broken Profile)
For grid tiling problems: process column by column, mask = state of current column boundary.

## 11. SOS DP (Sum over Subsets)
```python
# dp[mask] = sum of f[sub] for all sub ⊆ mask
for i in range(n):
    for mask in range(1<<n):
        if mask >> i & 1:
            dp[mask] += dp[mask ^ (1<<i)]
```
O(N · 2^N) — useful for AND/OR convolution.

## 12. When to Use Bitmask DP
- N ≤ 20 (usually ≤ 15 for interview)
- Need to track "which elements have been used"
- Assignment / matching / partition problems

## 13. Interview Tips
- Always verify N ≤ 20 before proposing.
- Initialize dp with INF or False carefully.
- Iterate masks in increasing order.

## 14. Common Mistakes
- Visiting node not in mask (check `mask >> u & 1`).
- Forgetting start state initialization.
- Using mutable default argument for memo in Python.

## 15. Complexity Summary
| Problem | N limit | Time |
|---------|---------|------|
| TSP | ≤ 20 | O(2^N · N²) |
| Partition K subsets | ≤ 16 | O(2^N · N) |
| SOS DP | ≤ 20 | O(N · 2^N) |
