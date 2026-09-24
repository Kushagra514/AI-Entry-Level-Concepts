# DP with Bitmasking

## 1. Definition
Bitmask DP is a technique where an integer is used as a bitmask to represent a subset of items (visited cities, available items) as part of the DP state. It is typically used for problems requiring permutations or combinations of small sets ($N \le 20$).

## 2. Intuition
If you have 10 cities to visit, tracking `visited = [True, False, True...]` is clunky and can't be easily used as an array index for a DP table. Instead, use binary: `101...`. The integer `5` (binary `101`) perfectly represents that cities 0 and 2 are visited. The DP state becomes `dp[current_city][bitmask]`.

## 3. Why it exists
Problems like the Traveling Salesperson Problem (TSP) are NP-hard. Brute force permutations take $O(N!)$. Bitmask DP reduces this to $O(N^2 2^N)$ by recognizing overlapping subproblems: reaching city $C$ having visited the same subset of cities has the same future cost, regardless of the exact order the subset was visited in.

## 4. Mechanics
- **Representation:** Node $i$ is represented by the $i$-th bit. `1 << i`.
- **Set bit (visit):** `mask | (1 << i)`.
- **Check bit (is visited?):** `mask & (1 << i) != 0`.
- **Clear bit:** `mask & ~(1 << i)`.
- **State:** `dp[mask][last_node]` = min cost to visit the set of nodes in `mask`, ending at `last_node`.

## 5. Complexity (Time & Space)
- **Time:** $O(2^N \cdot N^2)$. There are $2^N$ masks, $N$ ending nodes, and for each state, we transition by trying to visit the remaining $N$ nodes.
- **Space:** $O(2^N \cdot N)$ to store the DP table. This is why $N$ cannot exceed ~20.

## 6. Tiny worked example
Cities A(0), B(1), C(2). TSP.
Start at A. Mask = `001` (binary) = 1.
State: `dp[1][0]`. 
Transitions:
Go to B: new mask = `011` (3). Cost = `dp[1][0] + dist(A,B)`. Store in `dp[3][1]`.
Go to C: new mask = `101` (5). Cost = `dp[1][0] + dist(A,C)`. Store in `dp[5][2]`.

## 7. Code (Python)
```python
# Traveling Salesperson Problem (Shortest path visiting all nodes)
def tsp(n, dist):
    # dp[mask][i] = min distance visiting subset 'mask' ending at 'i'
    # 1 << n is 2^n
    dp = [[float('inf')] * n for _ in range(1 << n)]
    
    # Base cases: starting at each node
    for i in range(n):
        dp[1 << i][i] = 0
        
    for mask in range(1 << n):
        for u in range(n):
            # If u is in the mask
            if mask & (1 << u):
                for v in range(n):
                    # If v is NOT in the mask, we can transition to it
                    if not (mask & (1 << v)):
                        new_mask = mask | (1 << v)
                        dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])
                        
    # Answer is min cost of full mask (all 1s) ending anywhere
    full_mask = (1 << n) - 1
    return min(dp[full_mask][i] for i in range(n))
```

## 8. Common mistakes
- Confusing bitwise operator precedence. Always use parentheses: `if (mask & (1 << i)) != 0`.
- Doing $O(N!)$ DFS without memoization when a bitmask DP would easily pass. Look at the constraints! If $N \le 20$, think Bitmask.

## 9. 30-second interview answer
"Bitmask DP uses integers to represent subsets of items, turning combinations into hashable, indexable DP states. It reduces factorial time complexities like $O(N!)$ to exponential $O(N^2 2^N)$. The classic example is the Traveling Salesperson Problem, where the state is the current bitmask of visited cities and the last city visited."

## 10. 2-minute interview answer
"Problems that require exploring all permutations usually imply a brute force $O(N!)$ search. However, if the problem exhibits optimal substructure, we can use Bitmask Dynamic Programming. In the Traveling Salesperson Problem, if I have visited cities {A, B, C} and I am currently at C, the minimum cost to visit the remaining cities depends ONLY on the fact that I am at C and the set of remaining cities. It does not matter if I visited them in the order A->B->C or B->A->C. By using a bitmask—an integer where the $i$-th bit is 1 if city $i$ is visited—I can uniquely represent the visited set. The DP state becomes `dp[bitmask][current_city]`. There are $2^N$ possible masks and $N$ possible current cities, and calculating each takes $O(N)$ transitions to unvisited cities. This drops the complexity from $O(N!)$ to $O(2^N \cdot N^2)$. Because $2^{20}$ is about 1 million, this approach is perfectly suited for input sizes around $N \le 20$."

## 11. Follow-ups
- "How do you iterate through all subsets of a given mask?" (Using bitwise logic: `submask = (submask - 1) & mask` inside a while loop allows $O(3^N)$ subset DP).

## 12. Deeper questions
- "What is SOS DP (Sum Over Subsets)?" (A fast way to compute the sum of values for all submasks of every mask. Naively it takes $O(3^N)$, SOS DP does it in $O(N 2^N)$ using a DP similar to multi-dimensional prefix sums).

## 13. Related concepts
- **Graph traversal**: Often applied to graphs (TSP, Hamiltonian Path).
- **Memoized DFS**: Often easier to write Bitmask DP top-down than bottom-up.

## 14. When it breaks / Edge cases
- $N > 20$. $2^{25}$ is 33 million, which starts hitting Time Limit Exceeded. $2^{30}$ is 1 billion and will definitively fail/OOM.

## 15. Comparison with alternative approaches
- **Bitmask DP vs Backtracking:** Backtracking explores the whole $O(N!)$ tree. Bitmask DP merges overlapping branches using memoization.

---
*Where this shows up in ML:*
Combinatorial optimization problems, feature selection algorithms where $N$ is small.
