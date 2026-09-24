# Interval DP

## 1. Core Idea
dp[i][j] = optimal answer for subarray/subproblem on range [i, j].
Enumerate all split points k in [i, j-1] to combine sub-answers.

## 2. Complexity
O(N³) time, O(N²) space — typical for interval DP.

## 3. Template
```python
n = len(arr)
dp = [[0]*n for _ in range(n)]
for length in range(2, n+1):          # subproblem length
    for i in range(n - length + 1):
        j = i + length - 1
        dp[i][j] = float('inf')
        for k in range(i, j):         # split point
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + cost(i,k,j))
```

## 4. Matrix Chain Multiplication
Cost of multiplying chain A[i]…A[j]: dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1].

```python
def matrix_chain(p):
    n = len(p) - 1
    dp = [[0]*n for _ in range(n)]
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i+l-1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n-1]
```

## 5. Burst Balloons (LC 312)
dp[i][j] = max coins bursting all balloons between i and j (exclusive).
Key insight: think of k as the LAST balloon burst in [i+1,j-1].
dp[i][j] = max(dp[i][k] + nums[i]*nums[k]*nums[j] + dp[k][j]) for k in (i+1,j).

```python
def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n):
        for left in range(0, n-length):
            right = left + length
            for k in range(left+1, right):
                dp[left][right] = max(dp[left][right],
                    dp[left][k] + nums[left]*nums[k]*nums[right] + dp[k][right])
    return dp[0][n-1]
```

## 6. Palindrome Partitioning II (LC 132)
Min cuts for palindrome partitioning. Use interval DP to precompute isPalin[i][j].

```python
def minCut(s):
    n = len(s)
    pal = [[False]*n for _ in range(n)]
    for i in range(n): pal[i][i] = True
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i+l-1
            pal[i][j] = (s[i]==s[j]) and (l==2 or pal[i+1][j-1])
    cuts = list(range(-1, n))
    for j in range(1, n):
        for i in range(j+1):
            if pal[i][j]:
                cuts[j+1] = min(cuts[j+1], cuts[i]+1)
    return cuts[n]
```

## 7. Optimal BST
dp[i][j] = min cost of BST for keys i..j with given frequencies.

## 8. Stone Merge
Merge stones[i..j] into one pile: cost = sum(stones[i..j]). dp[i][j] = min total cost.

## 9. Key Insight Pattern
Always add padding sentinels (like burst balloons) when boundaries matter.
Think "what is the LAST operation" rather than the first.

## 10. When Split-Point Enumeration Works
- Problem decomposes into two non-overlapping sub-intervals
- Combining two intervals has a measurable cost
- Optimal substructure holds over intervals

## 11. Space Optimization
Usually not possible due to 2D dependency; store full N×N table.

## 12. Interview Tip
Draw the DP table. Fill diagonals (by length). k loop fills each cell.

## 13. Common Mistakes
- Wrong loop order: must iterate by length, not by i.
- Off-by-one on k range.
- Forgetting base cases: dp[i][i] = 0 or single-element cost.

## 14. Related Problems
Strange Printer (LC 664), Remove Boxes (LC 546), Zuma Game (LC 488).

## 15. Complexity Comparison
| Problem | Time | Space |
|---------|------|-------|
| Matrix Chain | O(N³) | O(N²) |
| Burst Balloons | O(N³) | O(N²) |
| Palindrome Partition | O(N²) | O(N²) |
