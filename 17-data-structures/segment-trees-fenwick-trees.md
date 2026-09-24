# Segment Trees & Fenwick Trees

## 1. Definition
**Segment Tree:** A tree data structure for answering range queries (e.g., range sum, range min/max) and handling point or range updates in $O(\log N)$ time.
**Fenwick Tree (Binary Indexed Tree / BIT):** A more memory-compact structure for prefix-sum queries and point updates, also in $O(\log N)$ time.

## 2. Intuition
- **Segment Tree:** Imagine a tournament bracket. Instead of summing 1000 individual scores, you precompute partial sums for every bracket group. To query any range, you just pick the relevant bracket results and combine them.
- **Fenwick Tree:** A clever bit-manipulation trick where each index "is responsible" for a specific range of elements determined by its lowest set bit.

## 3. Why it exists
Naive prefix-sum arrays answer range queries in $O(1)$ but take $O(N)$ to update (you must recompute the whole array). Segment Trees and Fenwick Trees exist to do both range queries AND updates in $O(\log N)$ time.

## 4. Mechanics
- **Segment Tree:** An array-backed binary tree of size $4N$. Each node stores the aggregate (sum/min/max) for a range. Queries and updates travel root-to-leaf in $O(\log N)$.
- **Fenwick Tree:** A flat array where `tree[i]` stores the sum of a specific power-of-2 sized range. Update by moving `i += i & (-i)`. Query prefix sum by moving `i -= i & (-i)`.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ to build. $O(\log N)$ for each query and update.
- **Space Complexity:** $O(N)$ for Fenwick, $O(4N)$ for Segment Tree.

## 6. Tiny worked example
Array: `[1, 3, 5, 7]`. Build Fenwick Tree.
- Query sum of indices 1-3: `1 + 3 + 5 = 9`.
- Update index 2 (+2): Array becomes `[1, 5, 5, 7]`.
- Re-query: `1 + 5 + 5 = 11`. Both operations in $O(\log 4) = 2$ steps.

## 7. Code (Python, with type hints)
```python
from typing import List

class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i: int, delta: int) -> None:
        # Point update: add delta to index i (1-indexed)
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)  # Move to next responsible index

    def query(self, i: int) -> int:
        # Prefix sum query: sum of [1..i].
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)  # Move to parent range
        return total

    def range_query(self, l: int, r: int) -> int:
        return self.query(r) - self.query(l - 1)
```

## 8. Common mistakes
- Fenwick Trees are 1-indexed; using 0-indexed input causes off-by-one errors and breaks `i & (-i)`.
- Confusing "Segment Tree with lazy propagation" (needed for range updates) with a plain Segment Tree (only point updates). Range updates require storing pending lazy tags at each node.

## 9. 30-second interview answer
"Segment Trees and Fenwick Trees answer range queries (sum, min, max) with point or range updates in $O(\log N)$ time versus $O(N)$ for naive arrays. Fenwick Trees are simpler and more memory-efficient for prefix-sum problems; Segment Trees are more general and support arbitrary range operations."

## 10. 2-minute interview answer
"When a problem requires both dynamic updates and range queries, neither a plain array ($O(1)$ query, $O(N)$ update) nor brute force ($O(N)$ query) is adequate. Fenwick Trees solve this elegantly for prefix-sum scenarios by exploiting binary representation: each index is responsible for the sum of a specific power-of-2 range determined by its lowest set bit. Updates propagate in $O(\log N)$ steps, and queries accumulate in $O(\log N)$ steps. For more complex operations like range min/max or range updates, the Segment Tree is preferred — it is a complete binary tree where each node stores the aggregate for its range, and queries decompose the range into $O(\log N)$ non-overlapping canonical segments."

## 11. Follow-ups
- "When would you use a Sparse Table instead?" (Sparse Tables answer range-minimum queries in $O(1)$ with $O(N \log N)$ preprocessing, but cannot handle updates. Ideal for static arrays).

## 12. Deeper questions
- "Explain lazy propagation in a Segment Tree." (Instead of pushing a range update to all $O(N)$ leaf nodes, store the pending operation in the tree node as a 'lazy tag'. Propagate it down only when that subtree is accessed, keeping updates to $O(\log N)$).

## 13. Related concepts
- **Prefix Sums**: The simpler static alternative.
- **Merge Sort Tree**: A Segment Tree storing sorted lists at each node, for range-order statistics.

## 14. When it breaks / Edge cases
- Segment Trees with range updates require lazy propagation; forgetting it silently produces wrong answers.

## 15. Comparison with alternative approaches
- **Fenwick vs Segment Tree**: Fenwick is 2x faster in practice and simpler to implement for prefix sums. Segment Tree is far more expressive for arbitrary monoid operations.

---
*Where this shows up in ML:*
Online learning systems that track running statistics (mean, variance) over sliding windows of training steps use similar incremental aggregation logic.
