# 2D Dynamic Programming

## 1. Definition
2D Dynamic Programming solves problems by maintaining a 2D state matrix, usually `dp[i][j]`. It is heavily used when the state depends on two variables: two strings (e.g., Edit Distance), a grid (e.g., Unique Paths), or an item index and a capacity (e.g., Knapsack).

## 2. Intuition
If you are navigating a grid from top-left to bottom-right, the number of ways to reach cell `(i, j)` depends entirely on the ways to reach the cell directly above `(i-1, j)` and directly to the left `(i, j-1)`. You sum them. By building a 2D table, you solve the maze step by step.

## 3. Why it exists
Many problems have optimal substructure defined by two independent axes. 1D DP cannot capture the relationship (e.g., comparing string A to string B requires tracking positions in both strings). 

## 4. Mechanics
- **Grid Traversal:** `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
- **String Matching:** `dp[i][j]` depends on `dp[i-1][j-1]` (if characters match) or `max(dp[i-1][j], dp[i][j-1])` (if they don't, e.g., Longest Common Subsequence).
- **0/1 Knapsack:** `dp[i][w]` depends on `dp[i-1][w]` (exclude item) and `dp[i-1][w-weight[i]] + value[i]` (include item).

## 5. Complexity (Time & Space)
- **Time:** $O(M \times N)$ to fill the $M \times N$ matrix.
- **Space:** $O(M \times N)$ naively. Can often be optimized to $O(\min(M, N))$ by noticing that row `i` only depends on row `i-1`.

## 6. Tiny worked example
Grid Paths. 2x2 Grid. Top-left is 1.
`dp = [[1, 1], [1, 0]]` (initialized row 0 and col 0 to 1).
`dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2`.
2 paths to the bottom-right.

## 7. Code (Python)
```python
# Unique Paths with Obstacles
def uniquePathsWithObstacles(obstacleGrid):
    M, N = len(obstacleGrid), len(obstacleGrid[0])
    if obstacleGrid[0][0] == 1: return 0
    
    dp = [[0]*N for _ in range(M)]
    dp[0][0] = 1
    
    for i in range(M):
        for j in range(N):
            if obstacleGrid[i][j] == 1:
                dp[i][j] = 0
                continue
            if i > 0: dp[i][j] += dp[i-1][j]
            if j > 0: dp[i][j] += dp[i][j-1]
            
    return dp[M-1][N-1]
```

## 8. Common mistakes
- **Initialization errors:** Forgetting to properly initialize the first row and first column. E.g., in a grid with an obstacle in the first row, all cells *after* the obstacle in that row must be 0, not 1.
- **Index out of bounds:** Not handling `i-1` and `j-1` for the 0th row/col. Pad the array with an extra row/col of zeros to avoid `if` statements.

## 9. 30-second interview answer
"2D DP is used when a problem's state relies on two dimensions, such as tracking two strings in Edit Distance or navigating a grid. We construct an $O(M \times N)$ table where `dp[i][j]` is calculated using adjacent cells like `dp[i-1][j]` and `dp[i][j-1]`. Space complexity can usually be optimized to $O(N)$ by only storing the previous row."

## 10. 2-minute interview answer
"2D Dynamic Programming is a vast category encompassing grid traversal, string comparison, and 0/1 knapsack problems. The core concept is that the optimal solution requires tracking two independent variables. For example, in Longest Common Subsequence, `dp[i][j]` represents the LCS of string1 up to index `i` and string2 up to index `j`. If the characters match, the state transitions from `dp[i-1][j-1]`. If not, it transitions from the max of `dp[i-1][j]` or `dp[i][j-1]`. Because we fill an $M \times N$ matrix, the time complexity is strictly $O(M \times N)$. However, a crucial realization for system design and space-constrained environments is that row `i` almost always depends *only* on row `i-1`. By keeping only two 1D arrays (the 'current' row and 'previous' row) instead of the full matrix, we reduce space complexity from $O(M \times N)$ to $O(N)$. This space optimization is a standard interview follow-up."

## 11. Follow-ups
- "Can you optimize the space to $O(N)$?" (Yes, by realizing `dp[i][j]` only needs `dp[i-1][...]`. Maintain `prev_row` and `curr_row`).

## 12. Deeper questions
- "How do you recover the actual path/string (e.g., the exact LCS)?" (You cannot space-optimize to $O(N)$. You must keep the full $M \times N$ matrix and backtrack from `dp[M][N]`, moving to the cell that provided the optimal value at each step).

## 13. Related concepts
- **1D DP**: The simpler version.
- **Backtracking**: Finding the path after the DP table is filled.

## 14. When it breaks / Edge cases
- Grids with cycles (e.g., you can move up, down, left, right). You cannot use standard 2D DP; you must use Dijkstra's or BFS because the strict topological ordering of DP is broken.

## 15. Comparison with alternative approaches
- **Top-Down (Memoization) vs Bottom-Up (Tabulation):** Top-down is easier to write for complex string problems and computes only necessary states. Bottom-up is faster (no recursion overhead) and easier to space-optimize.

---
*Where this shows up in ML:*
Dynamic Time Warping (DTW) for speech recognition and time-series alignment is exactly a 2D DP algorithm on a grid.
