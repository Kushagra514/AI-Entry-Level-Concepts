# Knapsack DP Family

## 1. Definition
The Knapsack problem is a classic 2D Dynamic Programming pattern where you must choose a subset of items, each with a weight and a value, to maximize total value without exceeding a capacity constraint.

## 2. Intuition
Imagine you are a thief with a backpack that holds exactly 50 lbs. You break into a vault with various items (gold bars, jewels, TVs). A TV is valuable but heavy. A jewel is light and moderately valuable. You can't just take the most valuable items (they might be too heavy), nor just the lightest (they might be worthless). You must evaluate the tradeoff for every single item: "Do I take this, or leave it?"

## 3. Why it exists
A greedy approach (sorting by value-to-weight ratio) fails for the "0/1 Knapsack" (where items cannot be broken into fractions) because you might leave empty space in the bag that could have been filled perfectly by a suboptimal item. DP exists to exhaustively but efficiently explore the "take it or leave it" branches.

## 4. Mechanics
- **State:** `dp(i, c)` = the maximum value using a subset of items from index `0` to `i`, with remaining capacity `c`.
- **Transition (0/1 Knapsack):** For item `i`, you can either:
  1. Leave it: `dp(i-1, c)`
  2. Take it (if it fits): `val[i] + dp(i-1, c - weight[i])`
  `dp(i, c)` is the maximum of those two choices.
- **Variations:** 
  - *Unbounded Knapsack:* You can take item `i` infinitely many times. Transition uses `dp(i, c - weight[i])` instead of `i-1`.
  - *Subset Sum:* Can you achieve exactly capacity `c`? (Boolean return).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \times C)$ where $N$ is the number of items and $C$ is the capacity constraint. (Note: This is pseudo-polynomial, meaning it's proportional to the *value* of $C$, not the *length* of the input).
- **Space Complexity:** $O(N \times C)$ for a 2D table. Can be space-optimized to $O(C)$ by only keeping the previous row.

## 6. Tiny worked example
Items (Wt, Val): A(1, 10), B(2, 15), C(3, 40). Capacity: 3.
- Cap 3, look at C: Take C (Val=40, Cap=0). Leave C (Look at A,B with Cap 3).
- Max is taking C (40).
- Wait, what about taking A and B? (W=3, Val=25). 40 > 25.
- DP table elegantly calculates this by building up from Capacity 0 to 3.

## 7. Code (Python, with type hints)
```python
from typing import List

def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    n = len(weights)
    # Space optimized to 1D array of size Capacity + 1
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Traverse backwards for 0/1 knapsack to avoid reusing the same item
        for c in range(capacity, weights[i] - 1, -1):
            dp[c] = max(dp[c], values[i] + dp[c - weights[i]])
            
    return dp[capacity]
```

## 8. Common mistakes
- **Traversal Direction in 1D Optimization:** In 0/1 Knapsack, if you optimize space to a 1D array, you *must* iterate the inner capacity loop backwards. If you iterate forwards, you might use the same item multiple times (which accidentally solves the Unbounded Knapsack problem!).
- Trying to use a Greedy algorithm (Value/Weight ratio) for 0/1 Knapsack. (Greedy only works for *Fractional* Knapsack).

## 9. 30-second interview answer
"The Knapsack pattern solves constrained optimization problems by deciding whether to 'take' or 'leave' an item. The state is defined by the current item index and the remaining capacity. It runs in $O(N \times C)$ time. The 2D memory footprint can be optimized to $O(C)$ by storing only the previous row, iterating backwards to prevent item reuse."

## 10. 2-minute interview answer
"The 0/1 Knapsack problem is the archetype for 2D Dynamic Programming where decisions are constrained by a resource limit. Because a greedy value-to-weight ratio fails for indivisible items, we must evaluate the 'take it or leave it' branches. We define a 2D state `dp[i][c]`, representing the max value up to item `i` with capacity `c`. The transition equation takes the max of leaving the item `dp[i-1][c]` or taking it `value[i] + dp[i-1][c-weight[i]]`. While this takes $O(N \times C)$ time and space, we can space-optimize it to $O(C)$ by noticing that row `i` only depends on row `i-1`. The trick in the 1D optimized version is that the capacity loop must run backwards; running it forwards would allow an item to recursively build on itself, transforming the algorithm into the Unbounded Knapsack solution."

## 11. Follow-ups
- "How do you solve Unbounded Knapsack (Coin Change)?" (Same 1D array optimization, but run the capacity loop forwards).
- "How do you solve Subset Sum (e.g., Partition Equal Subset Sum)?" (It's a knapsack where you don't maximize value, you just track boolean `True/False` if a capacity can be reached).

## 12. Deeper questions
- "Is $O(N \times C)$ polynomial time?" (No, it's pseudo-polynomial. If $C$ is $10^9$, the algorithm takes billions of operations, even if $N$ is just 5. The input size of $C$ in binary is only ~30 bits, so time is exponential relative to the input *size*).

## 13. Related concepts
- **Subset Sum**: Exact same logic, boolean states.
- **Target Sum**: Adds subtraction to the choices.

## 14. When it breaks / Edge cases
- Breaks if $C$ is massive (e.g., $10^9$). You will get a Time Limit Exceeded (TLE) and Memory Error.

## 15. Comparison with alternative approaches
- **vs Fractional Knapsack:** If you can cut items in half (like gold dust), you just sort by Value/Weight ratio and take as much as you can. Greedy works. $O(N \log N)$.

---
*Where this shows up in ML:* 
Resource allocation in AI infrastructure (e.g., bin-packing models onto limited GPU VRAM) is fundamentally a variation of the Knapsack problem.
