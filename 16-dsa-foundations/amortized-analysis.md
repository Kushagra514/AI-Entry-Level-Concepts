# Amortized Analysis

## 1. Definition
Amortized analysis is a technique for analyzing the average cost per operation over a sequence of operations, even if some individual operations are expensive, to show that the average cost is low.

## 2. Intuition
You park in a garage that charges \$1 per hour but has a sudden \$100 machine maintenance fee every 100 visits. On average, you pay \$1 + \$100/100 = \$2 per visit. The individual \$100 event is expensive, but amortized over 100 visits, the per-visit cost is still small. Amortized analysis finds this "blended average."

## 3. Why it exists
Per-operation worst-case analysis can be pessimistic. A single `append()` to a Python list might trigger an expensive resize ($O(N)$), but this happens so rarely that the per-operation average remains $O(1)$. Amortized analysis gives a tighter, more accurate complexity bound.

## 4. Mechanics
Three common techniques:
1. **Aggregate Method:** Count total cost for $N$ operations, then divide by $N$. Dynamic array: $N$ pushes cost $O(N)$ total (geometric series of resize costs) → $O(1)$ amortized per push.
2. **Accounting Method:** Assign a fixed "amortized cost" to each operation. Cheap operations pay extra ("save credits"). Expensive operations spend the saved credits.
3. **Potential Method:** Define a "potential function" $\Phi$ measuring stored work. Amortized cost = actual cost + $\Delta\Phi$. Prove the telescoping sum is bounded.

## 5. Complexity (Time & Space)
- N/A — this is an analysis technique, not a data structure.

## 6. Tiny worked example
Dynamic Array `append()` amortized analysis (Aggregate Method):
- Operations 1–8: each costs $O(1)$.
- Operation 9: triggers resize (copies 8 elements), costs $O(8)$.
- Operations 9–16: each costs $O(1)$.
- Operation 17: costs $O(16)$.

Total cost for $N$ appends: $N + 1 + 2 + 4 + 8 + ... + N = N + 2N = 3N = O(N)$.
Amortized cost per append: $O(N) / N = O(1)$.

## 7. Code (Python, with type hints)
```python
# Dynamic array growth strategy — the key to O(1) amortized append
class DynamicArray:
    def __init__(self):
        self._data = [None]
        self._size = 0
        self._capacity = 1

    def append(self, val) -> None:
        if self._size == self._capacity:
            # Double capacity: expensive O(N) operation but rare
            new_data = [None] * (2 * self._capacity)
            for i in range(self._size):
                new_data[i] = self._data[i]
            self._data = new_data
            self._capacity *= 2  # Doubling is critical for O(1) amortized
        self._data[self._size] = val
        self._size += 1
```

## 8. Common mistakes
- Confusing amortized $O(1)$ with worst-case $O(1)$. A single `append()` can still be $O(N)$ in the worst case; the amortized bound only applies as an average over many operations.
- Using additive growth (capacity += 1) instead of multiplicative growth (capacity *= 2) for dynamic arrays. Additive growth yields $O(N^2)$ total for $N$ appends; multiplicative growth yields $O(N)$ total.

## 9. 30-second interview answer
"Amortized analysis shows that while individual operations can be expensive occasionally, the average cost per operation over a sequence is low. The canonical example is Python's list `append()`: occasional $O(N)$ resizes are rare enough that the amortized cost per append is $O(1)$. This requires capacity doubling — additive growth destroys the guarantee."

## 10. 2-minute interview answer
"Amortized analysis is the mathematically rigorous way to reconcile a data structure that occasionally performs expensive operations with the intuition that 'on average, it's fast.' The classic example is the dynamic array. Inserting the $(N+1)$-th element into a full array triggers a copy of $N$ elements — an $O(N)$ operation. But because the array doubles its capacity each time, this copy only happens at sizes 1, 2, 4, 8, 16, ... The total copy work across $N$ appends forms a geometric series summing to $2N$. Dividing by $N$ operations yields $O(1)$ amortized. The same analysis applies to Python's `dict` (amortized $O(1)$ insert due to periodic rehashing) and Union-Find (amortized $O(\alpha(N))$ via Path Compression)."

## 11. Follow-ups
- "Does Python guarantee amortized $O(1)$ for `list.append()`?" (Yes. CPython uses a growth factor of approximately 1.125–2x depending on the current size, guaranteeing amortized $O(1)$ per append).

## 12. Deeper questions
- "How does the Splay Tree achieve amortized $O(\log N)$ per operation?" (Using a potential function $\Phi = \sum_i \log(\text{size of subtree at node } i)$. Expensive splays decrease $\Phi$ enough that the amortized cost stays logarithmic).

## 13. Related concepts
- **Dynamic Arrays (Lists)**: The canonical example.
- **Union-Find**: Amortized $O(\alpha(N))$ with Path Compression.

## 14. When it breaks / Edge cases
- Amortized analysis assumes operations are sequential. In a concurrent or real-time system, the occasional $O(N)$ resize spike is still unacceptable even if the average is $O(1)$.

## 15. Comparison with alternative approaches
- **vs Average-Case Analysis:** Average-case analysis averages over random inputs. Amortized analysis averages over a sequence of operations on the worst-case input.

---
*Where this shows up in ML:*
PyTorch's memory allocator uses a pool-based strategy where most allocations are $O(1)$ (grab from pool), but occasional pool expansion is $O(N)$. The amortized cost remains near-constant, enabling high throughput training.
