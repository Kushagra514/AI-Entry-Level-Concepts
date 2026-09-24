# 2D DP

## 1. Core Idea
State depends on two variables — often two sequences, two indices, or grid position.
dp[i][j] derived from dp[i-1][j], dp[i][j-1], dp[i-1][j-1].

## 2. Unique Paths (LC 62)
```python
def uniquePaths(m, n):
    dp = [[1]*n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]
# Space O(n): dp = [1]*n; for i in 1..m: for j in 1..n: dp[j] += dp[j-1]
```

## 3. Min Path Sum (LC 64)
```python
def minPathSum(grid):
    m, n = len(grid), len(grid[0])
    dp = [row[:] for row in grid]
    for i in range(1, m): dp[i][0] += dp[i-1][0]
    for j in range(1, n): dp[0][j] += dp[0][j-1]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] += min(dp[i-1][j], dp[i][j-1])
    return dp[m-1][n-1]
```

## 4. Longest Common Subsequence (LC 1143)
```python
def lcs(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

## 5. Edit Distance (LC 72)
```python
def editDistance(s, t):
    m, n = len(s), len(t)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
```

## 6. Longest Common Substring
dp[i][j] = length of common substring ending at s[i-1], t[j-1].
```python
if s[i-1]==t[j-1]: dp[i][j] = dp[i-1][j-1]+1
else: dp[i][j] = 0
```

## 7. Distinct Subsequences (LC 115)
dp[i][j] = # ways s[0..i-1] contains t[0..j-1] as subseq.
```python
dp[i][j] = dp[i-1][j] + (dp[i-1][j-1] if s[i-1]==t[j-1] else 0)
```

## 8. Maximal Square (LC 221)
dp[i][j] = side length of largest square with bottom-right at (i,j).
```python
dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1  # if grid[i][j]=='1'
```

## 9. Dungeon Game (LC 174)
Work backwards: dp[i][j] = min health needed entering cell (i,j).

## 10. Space Optimization Pattern
When dp[i][j] depends only on row i-1: use two 1D arrays (prev, curr) or in-place rolling.
LCS and Edit Distance can both be reduced to O(min(M,N)) space.

## 11. Knapsack as 2D DP
dp[i][w] = max value using first i items with capacity w.
```python
for i in range(1, n+1):
    for w in range(W+1):
        dp[i][w] = dp[i-1][w]
        if weights[i-1] <= w:
            dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])
```

## 12. Interleaving String (LC 97)
dp[i][j] = s3[0..i+j-1] is interleaving of s1[0..i-1] and s2[0..j-1].

## 13. Interview Tips
- Always draw the table and fill a 3×3 example by hand.
- Confirm base cases for i=0 and j=0 rows.
- Ask if space optimization is needed.

## 14. Common Mistakes
- Mixing 0-indexed dp with 1-indexed strings.
- Wrong initialization of boundary rows/columns.

## 15. Complexity Reference
| Problem | Time | Space (optimized) |
|---------|------|-------------------|
| Unique Paths | O(M·N) | O(N) |
| LCS | O(M·N) | O(N) |
| Edit Distance | O(M·N) | O(N) |
| Knapsack 0/1 | O(N·W) | O(W) |
