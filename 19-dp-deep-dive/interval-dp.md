# Interval DP

## 1. Definition
Interval DP is a dynamic programming pattern where subproblems are defined over contiguous subarrays (intervals) of the input. The state is typically `dp[i][j]`, representing the optimal answer for the interval from index `i` to `j`.

## 2. Intuition
To solve a big problem (the whole array), you solve smaller problems (smaller intervals). The optimal solution for an interval `[i, j]` is usually found by trying every possible split point `k` between `i` and `j`, combining the optimal solutions of `[i, k]` and `[k+1, j]`.

## 3. Why it exists
Problems like Matrix Chain Multiplication or bursting balloons cannot be solved linearly because the operations collapse intervals unpredictably. We must explore all parenthesizations/groupings, which naturally forms an interval structure.

## 4. Mechanics
- **State:** `dp[i][j]` = optimal cost/value for `arr[i...j]`.
- **Transitions:** `dp[i][j] = min/max(dp[i][k] + dp[k+1][j] + cost(i, k, j))` for `k` from `i` to `j-1`.
- **Base Cases:** `dp[i][i]` is usually the cost for a single element (often 0 or a base value).
- **Iteration Order:** Must iterate by *length* of the interval (from 1 to $N$), then by start index `i`. You cannot iterate `i` and `j` in a standard nested loop because `dp[i][j]` depends on smaller lengths.

## 5. Complexity (Time & Space)
- **Time:** $O(N^3)$. There are $O(N^2)$ states (`i`, `j`), and transitioning takes $O(N)$ (looping over `k`).
- **Space:** $O(N^2)$ to store the `dp` table.

## 6. Tiny worked example
Array `A` of matrices to multiply. Lengths: 10, 30, 5, 60.
Cost of `A[0]*A[1]` is $10 \times 30 \times 5 = 1500$.
To find optimal grouping of `A[0..2]`, try splitting at `k=0` (`A[0] * (A[1]*A[2])`) and `k=1` (`(A[0]*A[1]) * A[2]`). Pick the min cost.

## 7. Code (Python)
```python
def matrix_chain_multiplication(p):
    n = len(p) - 1 # number of matrices
    dp = [[0] * n for _ in range(n)]
    
    # l is the length of the interval
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')
            # k is the split point
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]
                dp[i][j] = min(dp[i][j], cost)
                
    return dp[0][n-1]
```

## 8. Common mistakes
- Iterating `i` from 0 to N and `j` from `i` to N. This is wrong because when calculating `dp[0][3]`, you might need `dp[1][3]`, which hasn't been computed yet. Always iterate by `length`.
- Getting indices mixed up in the cost function, especially when padding arrays (e.g., in Burst Balloons).

## 9. 30-second interview answer
"Interval DP solves problems by finding optimal solutions for contiguous subarrays. The state is `dp[i][j]` for the range `[i, j]`. The transition involves testing all split points `k` between `i` and `j` to combine the results of the two halves. It generally takes $O(N^3)$ time and $O(N^2)$ space, and requires iterating by interval length rather than start index."

## 10. 2-minute interview answer
"Interval DP is a specific DP pattern used when operations merge adjacent elements, like Matrix Chain Multiplication, Burst Balloons, or Palindrome Partitioning. Because merging changes the adjacent elements for future operations, greedy or simple 1D DP fails. Instead, we define our state as the optimal cost for the subarray `[i, j]`. To compute `dp[i][j]`, we guess the *last* operation that combines the two halves. We enumerate all split points `k`, adding the cost of `[i, k]` and `[k+1, j]` plus the cost of merging them. A critical implementation detail is the loop structure: we must build the table by increasing interval lengths, starting from length 1 up to $N$, ensuring subproblems are solved before they are needed. The complexity is almost always $O(N^3)$ time and $O(N^2)$ space."

## 11. Follow-ups
- "How do you solve Burst Balloons?" (Instead of guessing which balloon pops first, guess which balloon pops *last* in the interval `[i, j]`. That way, its adjacent balloons are strictly `i-1` and `j+1`, which are outside the interval and haven't popped yet).

## 12. Deeper questions
- "What is Knuth's Optimization?" (An optimization for certain Interval DP problems that reduces time from $O(N^3)$ to $O(N^2)$. If the optimal split point $K[i][j]$ satisfies $K[i][j-1] \le K[i][j] \le K[i+1][j]$, we can bound the `k` loop. Applies to Optimal Binary Search Tree).

## 13. Related concepts
- **2D DP**: Interval DP is a subset of 2D DP.
- **Divide and Conquer**: The transition mimics a D&C merge step, but memoized.

## 14. When it breaks / Edge cases
- If the problem allows swapping or rearranging elements, intervals are broken, and Interval DP cannot be used (might need Bitmask DP).

## 15. Comparison with alternative approaches
- **Interval DP vs 1D DP:** If the problem only involves making a decision at index $i$ based on $i-1$, use 1D DP. If it involves combining segments, use Interval DP.

---
*Where this shows up in ML:*
Sequence alignment algorithms, parsing algorithms (CYK for context-free grammars).
