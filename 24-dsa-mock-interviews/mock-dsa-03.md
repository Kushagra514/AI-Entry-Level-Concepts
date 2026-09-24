# DSA Mock Interview 3: Dynamic Programming

## Problem Statement
**Interviewer:** You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If it cannot be made, return `-1`. 

## The Interview Conversation

**Me (Clarification):** Can we assume we have an infinite number of each coin? And is the `amount` guaranteed to be positive?
**Interviewer:** Yes, infinite coins. The amount can be 0 or positive.
**Me (Brute Force):** A brute force approach would be to try every possible combination of coins using a recursive DFS tree. For an amount $A$, we branch out for every coin $C$. The time complexity would be $O(S^N)$ where $S$ is the amount, which is exponential and will time out.
**Interviewer:** Exactly. What makes this problem suitable for dynamic programming?
**Me (Insight):** It has optimal substructure and overlapping subproblems. To find the minimum coins for amount 11, if I try using a 5 coin, the answer is `1 + min_coins(6)`. We will calculate `min_coins(6)` multiple times across different branches, so we should memoize it or build it bottom-up.
**Interviewer:** Let's do the bottom-up approach. What will your state represent?
**Me:** I'll create a 1D array `dp` of size `amount + 1`. `dp[i]` will store the minimum number of coins needed to make amount `i`. I'll initialize the array with a dummy "infinity" value, like `amount + 1`, and set `dp[0] = 0`.

## Code Implementation
```python
def coinChange(coins: List[int], amount: int) -> int:
    # Initialize DP array with 'infinity'
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != amount + 1 else -1
```

## Dry Run & Edge Cases
**Me:** Let's trace `coins = [2], amount = 3`.
- `dp` initialized to `[0, 4, 4, 4]`.
- `a=1`: `1 - 2 < 0`. `dp[1]` remains `4`.
- `a=2`: `2 - 2 >= 0`. `dp[2] = min(4, 1 + dp[0]) = 1`.
- `a=3`: `3 - 2 >= 0`. `dp[3] = min(4, 1 + dp[1]) = min(4, 1 + 4) = 5`.
- Loop finishes. `dp[3]` is `5`. Since `5 != 4` is true, wait—ah! `5 != amount + 1`, so my return check `dp[amount] != amount + 1` would actually return `5` instead of `-1`! My initialization of `amount + 1` is safe, but because I did `1 + dp[a-c]`, a failed path `1 + 4` became `5`.
**Interviewer:** Good catch! How do you fix it?
**Me:** I should only use the result of `dp[a - c]` if it's a valid amount. Or simpler, use `float('inf')` for initialization so `1 + inf = inf`. Let me rewrite that line.

## Code Implementation (Fixed)
```python
def coinChange(coins: List[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != float('inf') else -1
```

## Follow-up Questions
**Interviewer:** Much better. What is the time and space complexity?
**Me:** Time complexity is $O(\text{amount} \times \text{len(coins)})$ because of the nested loops. Space complexity is $O(\text{amount})$ to store the DP array.
