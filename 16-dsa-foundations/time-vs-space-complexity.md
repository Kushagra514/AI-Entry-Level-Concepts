# Time vs Space Complexity

## 1. Definition
**Time Complexity** measures how the runtime of an algorithm scales with input size $N$. **Space Complexity** measures how the memory usage scales with $N$. Together they define the resource profile of an algorithm.

## 2. Intuition
Time is "how long does it take?" and space is "how much desk space do I need?" An algorithm that uses a massive cheat sheet (space) might finish an exam faster. An algorithm that uses no notes (space) might take much longer. This is the time-space tradeoff.

## 3. Why it exists
No single resource metric captures algorithmic efficiency. A solution using $O(1)$ memory might be slow. A fast solution might consume gigabytes of RAM. Understanding both dimensions allows engineers to pick the right algorithm for the hardware and latency constraints at hand.

## 4. Mechanics
**Complexity Hierarchy (time):** $O(1) < O(\log N) < O(N) < O(N \log N) < O(N^2) < O(2^N) < O(N!)$

**Rules:**
- Drop constants: $3N + 5 = O(N)$.
- Drop lower-order terms: $N^2 + N = O(N^2)$.
- Count worst-case inputs (unless stated otherwise).
- Space counts auxiliary memory (not the input itself), unless stated as "total space".

**Common Time-Space Tradeoffs:**
| Problem | Naive (Less Space) | Optimized (More Space) |
|---|---|---|
| Two Sum | $O(N^2)$ time, $O(1)$ space | $O(N)$ time, $O(N)$ space (Hash Map) |
| Subarray Sum K | $O(N^2)$ time, $O(1)$ space | $O(N)$ time, $O(N)$ space (Prefix + Map) |
| Count inversions | $O(N^2)$ time | $O(N \log N)$ time, $O(N)$ space (Merge Sort) |
| Fibonacci | $O(2^N)$ time, $O(N)$ stack | $O(N)$ time, $O(1)$ space (Bottom-Up DP) |

## 5. Complexity (Time & Space)
- N/A — this is itself the concept being defined.

## 6. Tiny worked example
Two Sum:
- Brute force: Nested loops. $O(N^2)$ time, $O(1)$ space.
- Hash Map: Single loop + map. $O(N)$ time, $O(N)$ space.
- If RAM is limited (embedded system), brute force wins. If latency matters, Hash Map wins.

## 7. Code (Python, with type hints)
```python
from typing import List

# O(N^2) time, O(1) space — minimal memory
def two_sum_slow(nums: List[int], target: int) -> List[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# O(N) time, O(N) space — minimal time
def two_sum_fast(nums: List[int], target: int) -> List[int]:
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []
```

## 8. Common mistakes
- **Ignoring space on stack:** Recursive DFS on a tree of depth $N$ uses $O(N)$ stack space even if no auxiliary data structures are allocated. Always count the recursion stack.
- Treating $O(N)$ and $O(2N)$ as different. They are asymptotically identical; constants are dropped.

## 9. 30-second interview answer
"Time complexity measures how runtime scales with input size; space complexity measures memory usage. Almost every optimization involves a time-space tradeoff: using a Hash Map costs $O(N)$ memory but speeds up lookups from $O(N)$ to $O(1)$. Knowing which resource is constrained guides the choice of algorithm."

## 10. 2-minute interview answer
"Time and space complexity are the two axes of algorithmic efficiency. In interview settings, the target time complexity is usually dictated by the input constraints: $N \le 10^8$ means you need $O(N)$ or $O(N \log N)$; $N \le 10^3$ might allow $O(N^2)$. Space is typically the secondary concern, but it matters. Recursion incurs $O(depth)$ implicit call-stack space, hash maps cost $O(N)$ auxiliary space, and 2D DP tables cost $O(N^2)$ — which can cause Memory Limit Exceeded on large inputs. Classic tradeoffs include: paying $O(N)$ space with a Hash Map to drop lookup time from $O(N)$ to $O(1)$; or paying $O(N)$ space with a prefix sum array to drop query time from $O(N)$ to $O(1)$. A strong engineer states both complexities explicitly, discusses the tradeoff with the interviewer, and adjusts based on the stated constraints."

## 11. Follow-ups
- "What is the distinction between auxiliary space and total space complexity?" (Auxiliary = extra memory beyond the input. Total = auxiliary + input. For Merge Sort: $O(N)$ auxiliary, $O(N)$ total. For Heap Sort: $O(\log N)$ auxiliary (call stack), $O(N)$ total).

## 12. Deeper questions
- "Can a problem have a theoretical lower bound on space?" (Yes. Sorting $N$ elements requires at least $\Omega(N)$ space just to store the output. No sorting algorithm can be truly $O(1)$ total space).

## 13. Related concepts
- **Big-O Notation**: The mathematical language of complexity.
- **Amortized Analysis**: When per-operation complexity is misleading.

## 14. When it breaks / Edge cases
- Big-O hides constant factors. An $O(N \log N)$ algorithm with a constant of 1000 can be slower than an $O(N^2)$ algorithm with a constant of 1 for small $N$. Always consider practical input sizes.

## 15. Comparison with alternative approaches
- N/A — it is the foundational framework for all algorithmic comparison.

---
*Where this shows up in ML:*
Model selection involves time-space tradeoffs: a larger model (more parameters = more space) may train faster (fewer epochs to converge). Quantization trades model accuracy for reduced space, which trades back to faster inference time.
