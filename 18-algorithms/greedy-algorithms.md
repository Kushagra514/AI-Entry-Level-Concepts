# Greedy Algorithms

## 1. Definition
A Greedy Algorithm is an algorithmic paradigm that builds up a solution piece by piece, always choosing the next piece that offers the most immediate (local) benefit, with the hope that these local optimums lead to a global optimum.

## 2. Intuition
Imagine you are at a buffet and want to maximize the calories on your plate. A greedy approach would be to look at all the food, grab the highest-calorie item you see (pizza), then the next highest (cake), until your plate is full. You don't calculate combinations; you just take the best thing available right now.

## 3. Why it exists
Dynamic programming is powerful but requires $O(N^2)$ or $O(N \times C)$ time and space. Greedy algorithms, when mathematically applicable, solve optimization problems in $O(N)$ or $O(N \log N)$ time (usually just requiring a sort), making them incredibly fast and memory-efficient.

## 4. Mechanics
1. **Sort/Prioritize:** Often, the input must be sorted by some metric (e.g., end time, value/weight ratio).
2. **Iterate:** Go through the sorted data.
3. **Select:** If the current item satisfies the constraints, take it. Do not look back or reconsider.
4. **Update state:** Adjust remaining capacity or current end time.

## 5. Complexity (Time & Space)
- **Time Complexity:** Usually $O(N \log N)$ because sorting is required. If already sorted, $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary space (ignoring the sorting overhead).

## 6. Tiny worked example
Activity Selection / Meeting Rooms:
Meetings: `[(1,3), (2,5), (4,6)]`. Goal: Maximize non-overlapping meetings.
- Sort by end time: `(1,3), (2,5), (4,6)`.
- Take `(1,3)`. Current end time = 3.
- Next is `(2,5)`. Starts at 2. $2 < 3$. Conflict! Skip.
- Next is `(4,6)`. Starts at 4. $4 \ge 3$. Take it.
Result: 2 meetings.

## 7. Code (Python, with type hints)
```python
from typing import List

# Classic Interval Scheduling / Activity Selection
def max_non_overlapping(intervals: List[List[int]]) -> int:
    if not intervals: return 0
    
    # Sort strictly by END time
    intervals.sort(key=lambda x: x[1])
    
    count = 1
    current_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        start, end = intervals[i]
        if start >= current_end:
            # No overlap, greedily take it
            count += 1
            current_end = end
            
    return count
```

## 8. Common mistakes
- **Using Greedy when DP is required:** E.g., the 0/1 Knapsack problem or Coin Change with non-standard denominations (like coins of 1, 3, 4 to make 6. Greedy takes 4+1+1=3 coins. DP takes 3+3=2 coins).
- Sorting by the wrong metric. In Interval Scheduling, sorting by start time fails; you must sort by end time to free up the resource as early as possible.

## 9. 30-second interview answer
"Greedy algorithms make locally optimal choices at each step, hoping to find a global optimum. They are extremely fast—usually $O(N \log N)$ due to sorting—and $O(1)$ space. However, they only work if the problem satisfies the Greedy Choice Property, meaning a local best choice never compromises the overall solution. Otherwise, you must use Dynamic Programming."

## 10. 2-minute interview answer
"Greedy algorithms are highly efficient, single-pass decision-makers. They avoid the exhaustive branching of Backtracking and the memory overhead of Dynamic Programming. We typically apply them by sorting the input by a specific heuristic—like finishing time in interval problems or edge weight in spanning trees—and then iterating through, picking the best valid option without ever looking back. The catch is that they are mathematically brittle. To use a Greedy algorithm, you must be confident the problem exhibits the 'Greedy Choice Property'. For example, Dijkstra's algorithm and Kruskal's MST are greedy and perfectly optimal. But for problems like the 0/1 Knapsack, taking the immediately most valuable item might block you from taking two smaller items that total a higher value, forcing you to use DP instead."

## 11. Follow-ups
- "How do you prove a greedy algorithm is correct?" (Usually by a 'proof by contradiction' or 'exchange argument', showing that swapping the greedy choice for any other choice yields a worse or equal result).

## 12. Deeper questions
- "What is a Matroid?" (An abstract mathematical structure that, if a problem maps to it, guarantees a Greedy algorithm will yield the optimal solution).

## 13. Related concepts
- **Dynamic Programming**: The fallback when Greedy fails.
- **Minimum Spanning Trees**: Kruskal's and Prim's are famous greedy algorithms.
- **Dijkstra's Algorithm**: A greedy algorithm for shortest paths.

## 14. When it breaks / Edge cases
- Breaks when future choices are heavily constrained by current choices in non-uniform ways (e.g., negative weights in Dijkstra's).

## 15. Comparison with alternative approaches
- **vs DP:** DP is safe but slow/memory-intensive. Greedy is fast but risky (must mathematically prove it works).

---
*Where this shows up in ML:* 
Decision Trees (CART algorithm) are fundamentally Greedy algorithms. At each node, the tree greedily picks the feature and threshold that minimizes Gini Impurity or Entropy *right now*, without looking ahead to see if a worse split now might lead to better splits deeper in the tree.
