# DP Intuition and Identification

## 1. Definition
This is a meta-pattern for recognizing during an interview whether a problem requires Dynamic Programming, and mathematically defining the state and transition required to solve it.

## 2. Intuition
You're in an interview. You see a problem asking for "the maximum," "the minimum," or "the number of ways." You think: is there a greedy shortcut? If greed fails because future choices depend on current choices, and you have to essentially check all combinations, it's almost certainly DP.

## 3. Why it exists
Candidates often freeze when asked a DP problem because they try to jump straight to a nested `for` loop (bottom-up tabulation) without understanding the core logic. A structured identification method exists to bridge the gap from English prompt -> Recursion -> DP.

## 4. Mechanics (The FAST Method)
1. **F - First Solution:** Write or conceptualize the naive recursive brute-force solution. What choices do you make at each step? (e.g., "take item" or "skip item").
2. **A - Analyze:** Does it do the same work repeatedly? (Overlapping subproblems). Does the final optimal answer depend on optimal sub-answers? (Optimal substructure).
3. **S - Subproblem (State):** Define the state variables. What changes between recursive calls? (e.g., `index`, `remaining_capacity`). Let `dp(i, c)` be the max value at index `i` with capacity `c`.
4. **T - Turn Around:** Define the Transition Equation. How does `dp(i, c)` relate to smaller states? e.g., `dp(i, c) = max(dp(i-1, c), val[i] + dp(i-1, c-weight[i]))`.

## 5. Complexity (Time & Space)
- **Time:** $O(\text{Unique States} \times \text{Transitions per State})$.
- **Space:** $O(\text{Unique States})$.

## 6. Tiny worked example
Problem: "Climbing Stairs". You can take 1 or 2 steps. How many ways to reach top $N$?
- **First:** `ways(N) = ways(N-1) + ways(N-2)`.
- **Analyze:** `ways(4)` calls `ways(3)` and `ways(2)`. `ways(3)` calls `ways(2)`. Overlap!
- **State:** `dp(i)` = number of ways to reach step `i`.
- **Transition:** `dp(i) = dp(i-1) + dp(i-2)`. (This is just Fibonacci).

## 7. Code (Python, with type hints)
*(Concept code for transitioning from Recursion to Memoization)*
```python
# The Universal DP Template (Top-Down)
def solve_dp(params):
    memo = {}
    def dp(state_vars):
        if base_case_condition(state_vars):
            return base_value
            
        if state_vars in memo:
            return memo[state_vars]
            
        # Try all choices, take min/max/sum
        ans = min/max/sum(
            dp(new_state) + cost for new_state in choices
        )
        
        memo[state_vars] = ans
        return ans
        
    return dp(initial_state)
```

## 8. Common mistakes
- **Greedy Trap:** Assuming a problem is greedy when it's actually DP. Example: 0/1 Knapsack. Greedy (taking highest value/weight ratio) fails. You *must* use DP.
- **State Bloat:** Including variables in the state that can be derived from other variables, wasting massive amounts of memory.

## 9. 30-second interview answer
"I identify DP problems by looking for keywords like 'maximize', 'minimize', or 'total ways', coupled with constraints that prevent a purely greedy approach. I map out the choices at a single step, write the recursive relation, and memoize the overlapping states."

## 10. 2-minute interview answer
*(N/A - this is a meta-skill file, use the 30-second answer in practice).*

## 11. Follow-ups
- "How do you know if Greedy will work instead of DP?" (You have to prove that a local optimum *always* leads to a global optimum. If you can think of a single counter-example where taking the best immediate choice ruins a better long-term choice, Greedy is out, DP is in).

## 12. Deeper questions
- "How do you handle DP states that are subsets or combinations?" (Bitmask DP. Instead of passing an array of `visited` boolean flags as state, which isn't hashable, you pass an integer where the bits represent the flags).

## 13. Related concepts
- **1D DP**: State relies on 1 variable (like index).
- **2D DP**: State relies on 2 variables (like index and remaining capacity).

## 14. When it breaks / Edge cases
- Fails if the state space is too large (e.g., $N=10^9$). DP will TLE (Time Limit Exceeded). You probably need a Math formula or Matrix Exponentiation.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Formulating Markov Decision Processes (MDPs) in Reinforcement Learning requires identifying the "State", the "Action", and the "Reward" transition matrix, which is conceptually identical to identifying DP states and transitions.
