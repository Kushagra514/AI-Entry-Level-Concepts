# Prefix Sums

## 1. Definition
A Prefix Sum array (also called a Cumulative Sum) is a precomputed array where each element `prefix[i]` contains the sum of all elements from index `0` to `i` in the original array. It allows range sum queries in $O(1)$ time after $O(N)$ preprocessing.

## 2. Intuition
Imagine a cash register tape showing sales per hour: `[10, 20, 30, 40]`. Instead of adding up every hour's sales to compute the total from hour 1 to 3, you record running totals: `[10, 30, 60, 100]`. The sum from hour 1 to 3 is just `total[3] - total[0] = 100 - 10 = 90`. One subtraction instead of two additions.

## 3. Why it exists
Without prefix sums, answering $Q$ range sum queries on an array of size $N$ takes $O(N \times Q)$ total time. With a prefix sum array (built in $O(N)$), each query is answered in $O(1)$, reducing total time to $O(N + Q)$.

## 4. Mechanics
- **Build:** `prefix[0] = arr[0]`. For `i > 0`: `prefix[i] = prefix[i-1] + arr[i]`.
- **Range Query `[l, r]`:** `prefix[r] - prefix[l-1]`. (Use `prefix[-1] = 0` as a sentinel to handle `l=0` cleanly).
- **2D Prefix Sums:** For matrices. `P[i][j] = arr[i][j] + P[i-1][j] + P[i][j-1] - P[i-1][j-1]` (inclusion-exclusion).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ to build. $O(1)$ per query.
- **Space Complexity:** $O(N)$ for the prefix array.

## 6. Tiny worked example
Array: `[3, 1, 4, 1, 5]`
Prefix: `[0, 3, 4, 8, 9, 14]` (with leading 0 sentinel)
Sum from index 2 to 4: `prefix[5] - prefix[2] = 14 - 4 = 10`. ✓ (4+1+5=10)

## 7. Code (Python, with type hints)
```python
from typing import List

def build_prefix(nums: List[int]) -> List[int]:
    prefix = [0] * (len(nums) + 1)  # +1 for sentinel at index 0
    for i, n in enumerate(nums):
        prefix[i + 1] = prefix[i] + n
    return prefix

def range_sum(prefix: List[int], l: int, r: int) -> int:
    return prefix[r + 1] - prefix[l]  # Inclusive [l, r]

# Find subarray with sum equal to k using prefix + hash map
def subarray_sum_k(nums: List[int], k: int) -> int:
    count, curr_sum = 0, 0
    seen = {0: 1}  # prefix sum 0 seen once (empty prefix)
    for n in nums:
        curr_sum += n
        count += seen.get(curr_sum - k, 0)
        seen[curr_sum] = seen.get(curr_sum, 0) + 1
    return count
```

## 8. Common mistakes
- Off-by-one errors. Building `prefix[i] = prefix[i-1] + arr[i]` without a leading zero sentinel forces a special case when `l == 0`.
- In the "Subarray Sum Equals K" problem, forgetting to seed the hash map with `{0: 1}`, missing subarrays that start from index 0.

## 9. 30-second interview answer
"A Prefix Sum array precomputes running sums in $O(N)$ time, reducing range sum queries from $O(N)$ to $O(1)$. It is essential for any problem involving repeated subarray summation queries and is the basis for the $O(N)$ 'Subarray Sum Equals K' pattern using a prefix sum + hash map."

## 10. 2-minute interview answer
"Prefix Sums transform a linear-time range query into a constant-time subtraction. By building a cumulative sum array in $O(N)$ time, any range sum `[l, r]` becomes `prefix[r+1] - prefix[l]` — a single arithmetic operation. Beyond straightforward range queries, prefix sums power the canonical 'Subarray Sum Equals K' pattern. Instead of a nested $O(N^2)$ brute force, we track the running prefix sum as we iterate. At each index, we check how many times `prefix_so_far - k` has appeared before (using a hash map). If `prefix[j] - prefix[i] == k`, then the subarray `[i+1, j]` sums to `k`. This reduces the problem to $O(N)$ time and $O(N)$ space, a common and impactful optimization that interviewers love."

## 11. Follow-ups
- "How does 2D prefix sum work?" (For matrix range queries. Build `P[i][j]` using inclusion-exclusion. Query a rectangle sum in $O(1)$ using four prefix values).

## 12. Deeper questions
- "What is a difference array?" (The inverse of prefix sum. Store differences `D[i] = arr[i] - arr[i-1]`. Range add-update `[l, r]` becomes two $O(1)$ edits. Reconstruct original by prefix-summing the difference array. Useful for $Q$ range updates followed by $N$ reads).

## 13. Related concepts
- **Fenwick Tree / Segment Tree**: When you need both updates and range queries dynamically.
- **Sliding Window**: Can sometimes replace prefix sums for maximum/minimum subarray problems.

## 14. When it breaks / Edge cases
- Prefix sums become stale the moment the underlying array is modified. For dynamic arrays with updates, use a Fenwick Tree.

## 15. Comparison with alternative approaches
- **vs Segment Tree:** Prefix sums give $O(1)$ query but $O(N)$ update. Segment Trees give $O(\log N)$ for both. Use prefix sums for static arrays, Segment Trees for dynamic ones.

---
*Where this shows up in ML:*
Cumulative distribution functions (CDFs) are prefix sums over probability mass functions. In attention mechanisms, the KV-cache accumulates key/value states akin to prefix information for efficient autoregressive decoding.
