# Dynamic Programming Interview Questions

---

## 1. Climbing Stairs

### 1. Restate the Problem
You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### 2. Clarify Edge Cases
- $n = 1$? Return 1.
- $n = 2$? Return 2.

### 3. Brute Force Approach
DFS tree. Try taking 1 step and 2 steps from every position. Time: $O(2^N)$.

### 4. Key Insight
To reach step $N$, you must have come from either step $N-1$ (taking a 1-step) or step $N-2$ (taking a 2-step). Thus, `ways(N) = ways(N-1) + ways(N-2)`. This is the Fibonacci sequence. It has optimal substructure and overlapping subproblems.

### 5. Optimized Approach
Bottom-up DP. We don't need a full array of size $N$; we only need the last two values to compute the next one. Initialize `one = 1` and `two = 1` (for step 0 and 1). Loop $N-1$ times, calculating `temp = one + two`, updating `one = two` and `two = temp`.

### 6. Justification
Time: $O(N)$ because we iterate $N$ times. Space: $O(1)$ because we only store two integer variables.

### 7. Code (Python)
```python
def climbStairs(n: int) -> int:
    one, two = 1, 1
    
    for i in range(n - 1):
        temp = one + two
        one = two
        two = temp
        
    return two
```

### 8. Dry Run
`n = 3`
- init: one=1, two=1
- i=0: temp=2, one=1, two=2
- i=1: temp=3, one=2, two=3
- Return two (3). (Ways: 1+1+1, 1+2, 2+1).

### 9. Edge Cases Handled
`n=1` bypasses the loop and returns 1.

### 10. Follow-ups
- "What if you can take 1, 2, or 3 steps?" -> `ways(n) = ways(n-1) + ways(n-2) + ways(n-3)`. Store 3 variables instead of 2.

### 11. Related Problems
Fibonacci Number, Min Cost Climbing Stairs.

---

## 2. Coin Change

### 1. Restate the Problem
Given an integer array `coins` representing coins of different denominations and an integer `amount`, return the fewest number of coins that make up that amount. If it cannot be made, return `-1`.

### 2. Clarify Edge Cases
- `amount = 0`? Return 0.
- Cannot make amount? Return -1.

### 3. Brute Force Approach
Backtracking. Try taking every coin denomination recursively. Time: $O(S^N)$ where $S$ is amount and $N$ is coin count.

### 4. Key Insight
This is an Unbounded Knapsack problem. To find the min coins for amount `A`, if we try taking a coin of value `C`, the answer is `1 + min_coins(A - C)`. We can memoize this or build it bottom-up.

### 5. Optimized Approach (Bottom-up 1D DP)
Create a `dp` array of size `amount + 1`, initialized to `amount + 1` (acting as infinity). `dp[0] = 0`. Iterate through amounts from 1 to `amount`. For each amount, iterate through all coins. If `amount - coin >= 0`, `dp[amount] = min(dp[amount], 1 + dp[amount - coin])`. Return `dp[amount]` if it's less than "infinity", else -1.

### 6. Justification
Time: $O(A \cdot C)$ where $A$ is the amount and $C$ is the number of coins. Space: $O(A)$ for the `dp` array.

### 7. Code (Python)
```python
def coinChange(coins: List[int], amount: int) -> int:
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != amount + 1 else -1
```

### 8. Dry Run
`coins=[1,2,5], amount=11`
- a=1: trying 1 -> dp[1] = 1+dp[0] = 1.
- a=2: trying 1 -> 1+dp[1] = 2. trying 2 -> 1+dp[0] = 1. dp[2] = 1.
- ...
- a=11: trying 1 -> 1+dp[10]. trying 5 -> 1+dp[6]. dp[11] = 3.

### 9. Edge Cases Handled
Amount 0 instantly returns 0. Impossible amounts stay at `amount + 1` and return `-1`.

### 10. Follow-ups
- "What if you want to find the *number of combinations* to make the amount?" -> This is Coin Change II. `dp[a] += dp[a-c]`.

### 11. Related Problems
Coin Change II, Minimum Path Sum.
