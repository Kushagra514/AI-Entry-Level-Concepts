import os

def write_and_commit(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch C)"')

files = {}

files["17-data-structures/hash-sets.md"] = r"""# Hash Sets

## 1. Definition
A Hash Set is a data structure that stores a collection of unique elements with no particular order, providing $O(1)$ average-case time for insertion, deletion, and membership checking via hashing.

## 2. Intuition
Imagine a stadium with 10,000 numbered seats. A Hash Set is like a VIP list tied to those seat numbers. If name "Alice" hashes to seat 4271, you instantly check seat 4271. No searching needed. Each seat holds only one person (uniqueness).

## 3. Why it exists
Checking if an element is in a Python `list` takes $O(N)$ time (linear scan). A Hash Set compresses that check to $O(1)$ by computing the element's location mathematically, making "have we seen this before?" instant.

## 4. Mechanics
- **Hashing:** The element is passed through a hash function that returns an integer bucket index.
- **Collision Handling:** Multiple elements can hash to the same bucket. Python resolves collisions via open addressing with probing.
- **Resize:** When the load factor exceeds a threshold (~0.75), the internal array doubles and all elements are rehashed to the new buckets.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(1)$ average for add, remove, and contains. $O(N)$ worst case if many elements hash to the same bucket (pathological inputs or poor hash functions).
- **Space Complexity:** $O(N)$ to store the elements.

## 6. Tiny worked example
Check for duplicates in `[1, 3, 4, 3, 1]`:
- Add 1. Seen: `{1}`.
- Add 3. Seen: `{1, 3}`.
- Add 4. Seen: `{1, 3, 4}`.
- Check 3: `3 in {1, 3, 4}` → True. **Duplicate found in $O(1)$!**

## 7. Code (Python, with type hints)
```python
from typing import List

def has_duplicate(nums: List[int]) -> bool:
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}
union = a | b        # {1, 2, 3, 4}
intersection = a & b # {2, 3}
difference = a - b   # {1}
```

## 8. Common mistakes
- Using a `list` for `seen` tracking. `if n in my_list` is $O(N)$; `if n in my_set` is $O(1)$.
- Trying to add mutable objects (lists, dicts) to a set. Only hashable (immutable) types are allowed. Use `frozenset` or `tuple` for compound keys.

## 9. 30-second interview answer
"A Hash Set stores unique elements and provides $O(1)$ average-case lookup. It is the definitive structure for deduplication and membership testing, trading $O(N)$ space for instant 'have we seen this?' answers — used in cycle detection, two-sum, and visited-node tracking."

## 10. 2-minute interview answer
"Hash Sets are the backbone of optimizing linear-scan membership checks. When a brute-force approach nests two loops to compare every pair of elements, we usually eliminate the inner loop entirely by checking a Hash Set instead. The set computes the element's index via a hash function in $O(1)$ time, so repeated membership tests cost nothing. The practical engineering tradeoff is space: we consume $O(N)$ auxiliary memory. In graph traversal, maintaining a `visited` set is what distinguishes an $O(V+E)$ BFS from an infinite loop. In Two-Sum, storing complements in a set transforms an $O(N^2)$ nested-loop solution into an $O(N)$ single-pass one."

## 11. Follow-ups
- "How does a Hash Set differ from a Hash Map?" (A Hash Map stores key-value pairs. A Hash Set is a Hash Map where the key is the element itself and the value is a trivial boolean/sentinel).

## 12. Deeper questions
- "What is a perfect hash function?" (A hash function where no two inputs produce the same output, eliminating all collisions. Practically impossible for arbitrary inputs, but achievable for small, fixed-key domains).

## 13. Related concepts
- **Hash Maps**: The generalization with values attached.
- **Bloom Filters**: A probabilistic, memory-compressed alternative that allows false positives.

## 14. When it breaks / Edge cases
- Pathological hash collisions degrade $O(1)$ to $O(N)$. Python mitigates this via hash randomization (seeded on process start).

## 15. Comparison with alternative approaches
- **vs Sorted Array (Binary Search):** Sorted array gives $O(\log N)$ lookup but $O(N)$ insertion. Hash Set gives $O(1)$ for both but uses more memory and loses order.

---
*Where this shows up in ML:*
Vocabulary deduplication during tokenizer training; tracking visited nodes in graph-based reasoning over knowledge graphs.
"""

files["17-data-structures/segment-trees-fenwick-trees.md"] = r"""# Segment Trees & Fenwick Trees

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
"""

files["18-algorithms/counting-radix-bucket-sort.md"] = r"""# Counting, Radix, and Bucket Sort

## 1. Definition
Three non-comparison-based sorting algorithms that bypass the $O(N \log N)$ lower bound of comparison sorts by exploiting the structure of the input data.

## 2. Intuition
- **Counting Sort:** Count how many times each value appears. Then reconstruct the sorted array by outputting each value exactly that many times. Like counting votes: 3 votes for A, 5 for B, 1 for C → output AAABBBBBС.
- **Radix Sort:** Sort digit by digit, from least significant to most significant. Like sorting words alphabetically by first sorting all last letters, then all second-to-last letters, and so on.
- **Bucket Sort:** Distribute elements into evenly-spaced ranges ("buckets"), sort each small bucket individually, then concatenate.

## 3. Why it exists
Comparison sorts are bounded by $\Omega(N \log N)$ by the information-theoretic lower bound. If we know the range or structure of the input (integers in a range, uniform floats), we can sort faster.

## 4. Mechanics
- **Counting Sort:** Array `count[v]++`. Then prefix sum to find positions. Stable in $O(N + K)$ where $K$ is value range.
- **Radix Sort:** Apply stable Counting Sort on each digit position (units, tens, hundreds). $O(d(N + K))$ where $d$ is number of digits, $K$ is digit range (usually 10).
- **Bucket Sort:** Map each element to a bucket (`index = floor(N * element/max_val)`). Sort each bucket (insertion sort). Concatenate. $O(N)$ average for uniform distributions.

## 5. Complexity (Time & Space)
| Algorithm | Time | Space | Best For |
|---|---|---|---|
| Counting | $O(N+K)$ | $O(K)$ | Integers in small range |
| Radix | $O(d(N+K))$ | $O(N+K)$ | Large integers with bounded digits |
| Bucket | $O(N)$ avg | $O(N)$ | Uniformly distributed floats |

## 6. Tiny worked example
Counting Sort on `[3, 1, 2, 3, 1]`, range 1–3:
- Count: `[0, 2, 1, 2]` (counts for values 0, 1, 2, 3).
- Output: 1, 1, 2, 3, 3.

## 7. Code (Python, with type hints)
```python
from typing import List

def counting_sort(nums: List[int], max_val: int) -> List[int]:
    count = [0] * (max_val + 1)
    for n in nums:
        count[n] += 1
    result = []
    for val, freq in enumerate(count):
        result.extend([val] * freq)
    return result

def radix_sort(nums: List[int]) -> List[int]:
    max_val = max(nums)
    exp = 1
    while max_val // exp > 0:
        # Counting sort on current digit
        output = [0] * len(nums)
        count = [0] * 10
        for n in nums:
            count[(n // exp) % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for n in reversed(nums):
            idx = (n // exp) % 10
            output[count[idx] - 1] = n
            count[idx] -= 1
        nums = output
        exp *= 10
    return nums
```

## 8. Common mistakes
- Using Counting Sort when $K >> N$ (e.g., sorting 10 numbers in range 0–1,000,000,000). You'd allocate a billion-element count array. Use Radix Sort instead.
- Bucket Sort producing wrong output for non-uniform distributions (all elements in one bucket degrades to $O(N^2)$).

## 9. 30-second interview answer
"Counting, Radix, and Bucket sort bypass the $O(N \log N)$ comparison lower bound by leveraging input structure. Counting Sort is $O(N+K)$ for integers in a range $K$. Radix Sort handles large integers digit-by-digit in $O(d \cdot N)$. Bucket Sort achieves $O(N)$ average for uniformly distributed data."

## 10. 2-minute interview answer
"These three algorithms exploit the fact that for specific input types, we can extract more information per operation than a simple 'is A greater than B?' comparison. Counting Sort works when the value range $K$ is small — it literally counts occurrences and reconstructs the sorted output, achieving $O(N+K)$ with no comparisons whatsoever. Radix Sort generalizes this to large integers by applying Counting Sort on each digit independently, using the stability of Counting Sort to preserve ordering from previous passes. Bucket Sort is the probabilistic option — for uniformly distributed inputs, it guarantees constant-time sorting on average by distributing values into proportionally-sized bins, each of which is small enough to sort trivially."

## 11. Follow-ups
- "Why must Counting Sort be stable for Radix Sort to work?" (Radix Sort sorts digit-by-digit from LSD to MSD. If the inner sort is not stable, the relative order from previous digits is lost, corrupting the final result).

## 12. Deeper questions
- "Can you sort strings with Radix Sort?" (Yes. Sort character by character from the last character to the first, treating each character as a base-256 digit).

## 13. Related concepts
- **Comparison Sorts**: Merge Sort, Quick Sort as alternatives.
- **Stable Sort**: Required property for Radix Sort's sub-sort.

## 14. When it breaks / Edge cases
- Counting/Radix fail on floating-point numbers without transformation. Negative numbers require offsetting indices.

## 15. Comparison with alternative approaches
- **vs Merge Sort:** Merge Sort is simpler, general-purpose, but bounded at $O(N \log N)$. These specialized sorts can be faster in practice when constraints are satisfied.

---
*Where this shows up in ML:*
Radix sort is used in GPU-accelerated sorting algorithms inside CUDA for building spatial data structures (like BVH trees in ray tracing for neural rendering).
"""

files["18-algorithms/heap-sort.md"] = r"""# Heap Sort

## 1. Definition
Heap Sort is a comparison-based, in-place sorting algorithm that first organizes the array into a Max-Heap structure, then repeatedly extracts the maximum element to the end of the array to produce a sorted output.

## 2. Intuition
Imagine a tournament bracket where the strongest player always rises to the top. Heap Sort runs two phases: "Seeding" (building the heap so the strongest is at the root) and "Championship" (repeatedly crowning the champion, removing them, and re-seeding the remaining players until all are ordered).

## 3. Why it exists
Merge Sort is $O(N \log N)$ but requires $O(N)$ auxiliary space. Quick Sort is $O(N \log N)$ average but $O(N^2)$ worst case. Heap Sort achieves $O(N \log N)$ guaranteed time with $O(1)$ in-place space, making it the theoretically optimal comparison sort.

## 4. Mechanics
1. **Build Max-Heap (Heapify):** Starting from the last non-leaf node (`n//2 - 1`), call `sift_down` on every node up to the root. Total time: $O(N)$.
2. **Sort:** Swap root (max element) with the last element, shrink the heap size by 1, and `sift_down` the new root to restore the heap property. Repeat for all elements.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \log N)$ in all cases (best, average, worst). The `heapify` pass is $O(N)$, the extraction phase is $O(N \log N)$.
- **Space Complexity:** $O(1)$ auxiliary space. Truly in-place. Only $O(\log N)$ for the implicit call stack during `sift_down`.

## 6. Tiny worked example
Array: `[4, 10, 3]`. Build Max-Heap: `[10, 4, 3]`.
- Swap root (10) with last (3): `[3, 4, 10]`. Sift-down 3: `[4, 3, 10]`.
- Swap root (4) with last unsorted (3): `[3, 4, 10]`.
- One element left. Done. Sorted: `[3, 4, 10]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def heap_sort(nums: List[int]) -> None:
    n = len(nums)

    def sift_down(root: int, end: int) -> None:
        while True:
            largest = root
            left, right = 2 * root + 1, 2 * root + 2
            if left < end and nums[left] > nums[largest]:
                largest = left
            if right < end and nums[right] > nums[largest]:
                largest = right
            if largest == root:
                break
            nums[root], nums[largest] = nums[largest], nums[root]
            root = largest

    # Phase 1: Build Max-Heap in O(N)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)

    # Phase 2: Extract max elements one by one
    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(0, end)
```

## 8. Common mistakes
- Starting the heapify loop from the wrong index. It must start at `n//2 - 1` (last non-leaf node), not `n-1` (last leaf). Leaves don't need sifting.
- Forgetting to shrink the effective heap size (`end` pointer) during the extraction phase, causing already-sorted elements to be re-heapified.

## 9. 30-second interview answer
"Heap Sort is an in-place, $O(N \log N)$ comparison sort in all cases. It builds a Max-Heap from the array in $O(N)$ time, then repeatedly swaps the root (max) with the last element and sifts down, producing a sorted array. It uses $O(1)$ auxiliary space, unlike Merge Sort."

## 10. 2-minute interview answer
"Heap Sort is theoretically attractive because it combines the $O(N \log N)$ worst-case guarantee of Merge Sort with the $O(1)$ auxiliary space of an in-place sort. The algorithm works in two phases. In the first phase, we convert the raw array into a Max-Heap using a bottom-up heapify procedure that runs in $O(N)$ time (not $O(N \log N)$ as naively expected, because lower nodes require less sifting). In the second phase, we repeatedly swap the root — always the maximum — to the end of the array and shrink the heap boundary, restoring the heap property after each swap. Despite its theoretical elegance, Heap Sort is rarely used in practice because it has poor cache locality: sifting accesses distant parent-child indices in memory, causing frequent cache misses. Quick Sort's cache-friendly sequential access makes it significantly faster in practice despite its $O(N^2)$ worst case."

## 11. Follow-ups
- "Why is Heap Sort not stable?" (When we swap the root with the last element, equal elements can jump past each other, breaking relative ordering).

## 12. Deeper questions
- "Why does building a heap take $O(N)$ and not $O(N \log N)$?" (Nodes near the bottom have smaller subtrees and sift down fewer levels. Summing the geometric series of work per level converges to $O(N)$, not $O(N \log N)$).

## 13. Related concepts
- **Heaps / Priority Queues**: The underlying data structure.
- **Quick Sort & Merge Sort**: The practical alternatives.

## 14. When it breaks / Edge cases
- Not stable, so cannot be used where equal elements must preserve their relative order.

## 15. Comparison with alternative approaches
- **vs Quick Sort:** Quick Sort is faster in practice (cache-friendly), but $O(N^2)$ worst case. Heap Sort is $O(N \log N)$ guaranteed but cache-unfriendly.

---
*Where this shows up in ML:*
GPU sorting libraries (like `cub::DeviceRadixSort` in CUDA) inform architectural decisions. Heap Sort's predictable complexity is relevant when implementing priority-based sampling in RL replay buffers.
"""

files["18-algorithms/bubble-insertion-selection-sort.md"] = r"""# Bubble, Insertion, and Selection Sort

## 1. Definition
Three elementary $O(N^2)$ comparison-based sorting algorithms, each building a sorted array through different repeated-comparison strategies.

## 2. Intuition
- **Bubble Sort:** Like bubbles rising in water. Repeatedly compare adjacent pairs; larger values "bubble" to the end.
- **Insertion Sort:** Like sorting playing cards in hand. Pick the next card, slide it left until it's in the right place.
- **Selection Sort:** Like choosing the smallest shirt from a pile and hanging it first. Repeatedly find the minimum of the remaining elements and place it at the front.

## 3. Why it exists
They are the simplest sorting algorithms to understand and implement from scratch. Insertion Sort specifically excels on nearly-sorted data, and all three operate in $O(1)$ extra space.

## 4. Mechanics
- **Bubble Sort:** Two nested loops. Swap adjacent `arr[j]` and `arr[j+1]` if out of order. Largest unsorted bubbles to the end each pass.
- **Insertion Sort:** Outer loop `i` from 1 to N. Inner loop slides `arr[i]` leftward as long as it's smaller than the left neighbor.
- **Selection Sort:** Outer loop `i` from 0 to N. Find `min_idx` in `arr[i:]`. Swap `arr[i]` with `arr[min_idx]`.

## 5. Complexity (Time & Space)
| Algorithm | Best | Avg | Worst | Space | Stable |
|---|---|---|---|---|---|
| Bubble | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes |
| Insertion | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes |
| Selection | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | No |

## 6. Tiny worked example
Insertion Sort on `[3, 1, 2]`:
- i=1: key=1. Compare 3>1, shift. Insert 1: `[1, 3, 2]`.
- i=2: key=2. Compare 3>2, shift. Compare 1<2, stop. Insert 2: `[1, 2, 3]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def insertion_sort(nums: List[int]) -> None:
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > key:
            nums[j + 1] = nums[j]  # Shift right
            j -= 1
        nums[j + 1] = key  # Insert key in correct position

def bubble_sort(nums: List[int]) -> None:
    n = len(nums)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:  # Optimization: early exit if already sorted
            break
```

## 8. Common mistakes
- Not adding the early-exit optimization (`if not swapped: break`) to Bubble Sort, making it always $O(N^2)$ even on already-sorted input.
- Using Selection Sort when stability is required — it is inherently unstable.

## 9. 30-second interview answer
"Bubble, Insertion, and Selection Sort are elementary $O(N^2)$ algorithms. Insertion Sort is uniquely practical — it runs in $O(N)$ on nearly-sorted data and is used by Timsort for small runs. All three operate in $O(1)$ space. In interviews, they are typically asked to assess sorting fundamentals, not as practical solutions."

## 10. 2-minute interview answer
"These three $O(N^2)$ sorts are foundational but have distinct characters. Selection Sort is the simplest conceptually — find the minimum, place it — but makes $O(N^2)$ comparisons regardless of input and is not stable. Bubble Sort makes adjacent swaps until no swaps are needed, with the early-exit optimization making it $O(N)$ on already-sorted arrays. Insertion Sort is the most practically useful of the three. It builds the sorted portion by inserting elements one by one into their correct position, which mimics how humans naturally sort cards. Because it accesses a nearly-sorted array with minimal movements, it is the sorting algorithm of choice for small subarrays and is embedded inside Timsort (Python's built-in sort) for runs under 64 elements, where its cache-friendly sequential access outperforms Merge Sort's overhead."

## 11. Follow-ups
- "What is Timsort?" (Python's and Java's built-in sort. It is a hybrid of Merge Sort and Insertion Sort. It splits the array into naturally ordered 'runs', sorts small runs with Insertion Sort, then merges them with Merge Sort).

## 12. Deeper questions
- "Which of the three would you use if you needed to minimize the number of writes to the array?" (Selection Sort. It makes exactly $N-1$ swaps regardless of input, minimizing writes to memory — useful for write-expensive storage like flash memory).

## 13. Related concepts
- **Merge Sort / Quick Sort**: The $O(N \log N)$ replacements.
- **Timsort**: The hybrid that incorporates Insertion Sort.

## 14. When it breaks / Edge cases
- All three degrade on large inputs ($N > 10^4$) due to the quadratic time complexity.

## 15. Comparison with alternative approaches
- **vs Merge Sort:** Merge Sort is $O(N \log N)$ always, but $O(N)$ extra space. For small arrays (N < 20), Insertion Sort's constant factor makes it faster in practice.

---
*Where this shows up in ML:*
Timsort, which incorporates Insertion Sort, is used every time you call `sorted()` or `.sort()` on a Python list — including during data preprocessing.
"""

files["18-algorithms/search-variants.md"] = r"""# Search Variants

## 1. Definition
Variants of the classic Binary Search adapted for problems where the answer isn't an exact match but a boundary, a rotated array, or a 2D matrix.

## 2. Intuition
Binary Search is not just "find this value". It is a general-purpose tool for cutting a search space in half when the space is **monotone** (sorted or has a clear left/right boundary). All variants follow the same skeleton; only the condition and what you do with the bounds changes.

## 3. Why it exists
Interviewers rarely ask for plain Binary Search. Instead they dress it up: "the array was rotated", "find the leftmost position", "search a matrix". These variants test whether you have a deep mental model of the algorithm vs. a surface-level memorization.

## 4. Mechanics
**Key template (Left Boundary / Leftmost True):**
```
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    if condition(mid):  # True = valid half
        hi = mid
    else:
        lo = mid + 1
return lo
```
- **Find exact value:** standard `if arr[mid] == target`.
- **Leftmost occurrence:** move `hi = mid` even on match (keep searching left).
- **Rightmost occurrence:** move `lo = mid + 1` on match (keep searching right).
- **Rotated sorted array:** determine which half is sorted, then narrow bounds accordingly.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\log N)$ for all variants.
- **Space Complexity:** $O(1)$ iterative; $O(\log N)$ recursive.

## 6. Tiny worked example
Leftmost occurrence of `2` in `[1, 2, 2, 2, 3]`:
- `lo=0, hi=4`. `mid=2`, `arr[2]=2`. Match! `hi=2`.
- `lo=0, hi=2`. `mid=1`, `arr[1]=2`. Match! `hi=1`.
- `lo=0, hi=1`. `mid=0`, `arr[0]=1`. No match. `lo=1`.
- `lo==hi==1`. Return `1`. (Correct: index of first `2`.)

## 7. Code (Python, with type hints)
```python
from typing import List

def search_rotated(nums: List[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        # Left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

def find_leftmost(nums: List[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(nums) and nums[lo] == target else -1
```

## 8. Common mistakes
- Off-by-one errors in `lo/hi` initialization and update: use `hi = n` (exclusive) for boundary searches and `hi = n-1` (inclusive) for exact searches.
- In rotated array search, forgetting to handle duplicates. Duplicates require `lo += 1` fallback when `nums[lo] == nums[mid]`.

## 9. 30-second interview answer
"Binary Search variants reuse the same halving skeleton but adapt the condition and bound updates. Leftmost/rightmost occurrence shifts bounds even on a match. Rotated-array search checks which half is sorted to decide which side to eliminate. All variants remain $O(\log N)$."

## 10. 2-minute interview answer
"The key to all Binary Search variants is internalizing a single invariant: at every step, the answer lies within `[lo, hi]`. In leftmost occurrence, when we find a match at `mid`, we don't immediately return — we keep the match as a candidate but continue searching left by setting `hi = mid`. When searching a rotated sorted array, we cannot directly compare `arr[mid]` to the target, because the array wraps around. Instead, we first determine which of the two halves is cleanly sorted by comparing `arr[lo]` to `arr[mid]`. Once we know which half is sorted, we check if the target lies within that half's bounds. If yes, we search there; otherwise, we search the other half. This restores the standard Binary Search logic and preserves $O(\log N)$."

## 11. Follow-ups
- "How do you binary-search a 2D matrix where each row is sorted?" (Treat the matrix as a flat array of size `M*N`. Map `mid` to `(mid // N, mid % N)` for the actual cell access).

## 12. Deeper questions
- "What is Exponential Search?" (For sorted arrays of unknown length. Double the index from 1, 2, 4, 8… until you overshoot, then Binary Search within `[prev, current]`. $O(\log N)$ overall).

## 13. Related concepts
- **Binary Search on Answer**: Binary searching the answer space rather than an array index.
- **Two Pointers**: An alternative for some sorted-array search problems.

## 14. When it breaks / Edge cases
- Rotated array with all duplicates (`[2, 2, 2, 2]`) degrades to $O(N)$ since you can't determine which half is sorted.

## 15. Comparison with alternative approaches
- **vs Hash Map:** Hash Map gives $O(1)$ exact lookup but requires $O(N)$ preprocessing space. Binary Search requires only sorted input and $O(1)$ space.

---
*Where this shows up in ML:*
Hyperparameter grid searches use binary-search-style pruning in tools like Optuna (Tree-structured Parzen Estimator).
"""

files["18-algorithms/shortest-paths-bellman-ford.md"] = r"""# Bellman-Ford Algorithm

## 1. Definition
Bellman-Ford is a single-source shortest path algorithm that, unlike Dijkstra's, correctly handles graphs with **negative edge weights** and can detect **negative-weight cycles**.

## 2. Intuition
Imagine a city map where some roads give you cash back (negative weight — e.g., toll rebates). Dijkstra's greedily picks the "cheapest so far" exit and never revisits it, so it would miss the rebate. Bellman-Ford instead tries every possible road $V-1$ times, systematically relaxing all estimates until they converge to truth.

## 3. Why it exists
Dijkstra's greedy assumption ("the currently closest node will never get closer") breaks with negative weights. Bellman-Ford sacrifices speed for correctness, operating in $O(V \times E)$ time to guarantee correct shortest paths even with negative edges.

## 4. Mechanics
1. Initialize `dist[source] = 0`, all others `= infinity`.
2. Repeat $V-1$ times:
   - For every edge $(u, v, w)$: if `dist[u] + w < dist[v]`, update `dist[v] = dist[u] + w`.
3. **Negative Cycle Detection:** Run one more iteration. If any distance still updates, a negative-weight cycle exists.

**Why $V-1$ iterations?** The shortest path between any two vertices in a graph with $V$ nodes uses at most $V-1$ edges (otherwise it visits a node twice, implying a cycle).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V \times E)$. For dense graphs this is $O(V^3)$, far slower than Dijkstra's $O((V+E) \log V)$.
- **Space Complexity:** $O(V)$ for the distance array.

## 6. Tiny worked example
Nodes: A, B, C. Edges: `A->B (4)`, `A->C (5)`, `B->C (-6)`.
- Init: `A=0, B=inf, C=inf`.
- Pass 1: Relax `A->B`: `B=4`. Relax `A->C`: `C=5`. Relax `B->C`: `C = min(5, 4-6) = -2`.
- Pass 2: No further updates. Done. Shortest to C = -2.

## 7. Code (Python, with type hints)
```python
from typing import List, Tuple

def bellman_ford(n: int, edges: List[Tuple[int, int, int]], src: int):
    dist = [float('inf')] * n
    dist[src] = 0

    # Relax all edges V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Detect negative cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # Negative cycle exists

    return dist
```

## 8. Common mistakes
- Stopping after fewer than $V-1$ iterations on a sparse graph. The algorithm *requires* $V-1$ full passes regardless of apparent convergence (unless you add an early-exit optimization tracking whether any update occurred in a pass).
- Confusing "negative weight edge" (fine for Bellman-Ford) with "negative weight cycle" (makes shortest paths undefined and infinitely negative).

## 9. 30-second interview answer
"Bellman-Ford finds single-source shortest paths in $O(V \times E)$ time and, unlike Dijkstra's, handles negative edge weights. It relaxes all edges $V-1$ times and detects negative cycles with one extra pass. It's slower than Dijkstra's but necessary for graphs with negative edges."

## 10. 2-minute interview answer
"Bellman-Ford solves the single-source shortest path problem without the non-negative weight constraint that cripples Dijkstra's. It works by systematically relaxing every edge in the graph, repeating $V-1$ times. The intuition is that any shortest path in a graph of $V$ nodes uses at most $V-1$ edges. So after $k$ iterations, `dist[v]` holds the shortest path using at most $k$ edges. By $V-1$ iterations, all simple shortest paths have been discovered. The $(V)^{th}$ iteration serves as a negative-cycle detector: if any distance still decreases, it means a negative cycle exists and true shortest paths are undefined. While $O(V \times E)$ is significantly slower than Dijkstra's, Bellman-Ford is the correct choice for any graph where edge weights can be negative."

## 11. Follow-ups
- "What is SPFA (Shortest Path Faster Algorithm)?" (A queue-based optimization of Bellman-Ford. Only enqueue vertices whose distances were just updated. Average case $O(E)$, worst case still $O(VE)$).

## 12. Deeper questions
- "What is the Floyd-Warshall algorithm?" (An $O(V^3)$ DP algorithm that finds all-pairs shortest paths, not just from a single source. Also handles negative weights and detects negative cycles).

## 13. Related concepts
- **Dijkstra's Algorithm**: The faster alternative when weights are non-negative.
- **Floyd-Warshall**: The all-pairs generalization.

## 14. When it breaks / Edge cases
- If a negative cycle is reachable from the source, shortest paths are $-\infty$ along that cycle. The algorithm correctly reports the cycle but cannot compute finite distances.

## 15. Comparison with alternative approaches
- **vs Dijkstra's:** Dijkstra's is $O((V+E)\log V)$ but requires non-negative weights. Bellman-Ford is $O(VE)$ but handles all weights. Always prefer Dijkstra's when weights are guaranteed non-negative.

---
*Where this shows up in ML:*
In distributed systems and networking (BGP routing protocol for the internet uses a variant of Bellman-Ford). Also relevant for reward propagation in tabular Reinforcement Learning with negative rewards.
"""

files["18-algorithms/divide-and-conquer.md"] = r"""# Divide and Conquer

## 1. Definition
Divide and Conquer is an algorithm design paradigm that recursively breaks a problem into two or more smaller, **independent** subproblems, solves each subproblem, and combines their solutions into a solution for the original problem.

## 2. Intuition
You are asked to count how many words are in a 1000-page book. Instead of reading it yourself, you rip it in half and hand each half to a friend. Each friend rips their half in half and hands those to two more friends. Eventually, someone is counting words on a single page. You collect and add up all the counts.

## 3. Why it exists
Certain problems can be decomposed such that solving smaller instances is dramatically easier. The key distinction from Dynamic Programming: the subproblems must be **independent** (non-overlapping). If they overlap, memoization (DP) is needed.

## 4. Mechanics
Three steps in every D&C algorithm:
1. **Divide:** Split the problem into subproblems of the same type.
2. **Conquer:** Recursively solve each subproblem. Base case: problem is small enough to solve directly.
3. **Combine:** Merge the subproblem solutions into the final answer.

Time complexity is analyzed using the **Master Theorem**: $T(N) = aT(N/b) + f(N)$, where $a$ = subproblems, $b$ = factor of reduction, $f(N)$ = combine cost.

## 5. Complexity (Time & Space)
- **Merge Sort:** $T(N) = 2T(N/2) + O(N)$ → $O(N \log N)$.
- **Binary Search:** $T(N) = T(N/2) + O(1)$ → $O(\log N)$.
- **Karatsuba Multiplication:** $T(N) = 3T(N/2) + O(N)$ → $O(N^{1.585})$.
- **Space:** $O(\log N)$ call stack for balanced splits.

## 6. Tiny worked example
Count inversions in `[3, 1, 2]` (pairs where `arr[i] > arr[j]` for `i < j`).
- Divide: `[3, 1]` and `[2]`.
- Merge `[3,1]` → `[1, 3]`, count 1 inversion (`3 > 1`).
- Merge `[1, 3]` and `[2]` → `[1, 2, 3]`, count 1 inversion (`3 > 2`).
- Total: 2 inversions.

## 7. Code (Python, with type hints)
```python
from typing import List

# Classic D&C: Count Inversions (via Merge Sort)
def count_inversions(nums: List[int]) -> int:
    if len(nums) <= 1:
        return 0
    
    mid = len(nums) // 2
    left, right = nums[:mid], nums[mid:]
    
    count = count_inversions(left) + count_inversions(right)
    
    # Merge and count cross-inversions
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            nums[k] = left[i]; i += 1
        else:
            count += len(left) - i  # All remaining left elements > right[j]
            nums[k] = right[j]; j += 1
        k += 1
    nums[k:] = left[i:] or right[j:]
    return count
```

## 8. Common mistakes
- Applying D&C when subproblems **overlap** (should be DP instead).
- Missing the base case, causing infinite recursion.
- In Merge Sort: allocating new arrays in every recursive call leads to $O(N \log N)$ space usage rather than $O(N)$.

## 9. 30-second interview answer
"Divide and Conquer splits a problem into independent subproblems, solves them recursively, and combines the results. Examples include Merge Sort, Quick Sort, Binary Search, and the Fast Fourier Transform. Its time complexity is analyzed with the Master Theorem."

## 10. 2-minute interview answer
"Divide and Conquer is the paradigm behind the most important algorithms in computer science. Its power comes from exploiting recursive self-similarity: a sorted array can be split into two sorted halves. The key requirement is subproblem independence — unlike DP, once we split, neither half depends on the other's intermediate state. The combine step is where the real work happens: Merge Sort's $O(N)$ merge pass is what gives it $O(N \log N)$ total complexity. The Master Theorem provides an $O(1)$ mechanical way to analyze any D&C recurrence relation of the form $T(N) = aT(N/b) + f(N)$ without unrolling the recursion. Beyond sorting, D&C underlies matrix multiplication (Strassen's), computational geometry (closest pair of points), and the Fast Fourier Transform."

## 11. Follow-ups
- "State the three cases of the Master Theorem." (1: $f(N) = O(N^{\log_b a - \epsilon})$ → $T = O(N^{\log_b a})$. 2: $f(N) = O(N^{\log_b a})$ → $T = O(N^{\log_b a} \log N)$. 3: $f(N) = \Omega(N^{\log_b a + \epsilon})$ and regularity → $T = O(f(N))$).

## 12. Deeper questions
- "How does the Closest Pair of Points problem use D&C to beat $O(N^2)$?" (Split points by x-coordinate. Recurse on each half. The tricky combine step checks points near the center strip in $O(N)$ time using a geometric argument).

## 13. Related concepts
- **Merge Sort / Quick Sort**: The canonical D&C sorts.
- **Dynamic Programming**: Used when subproblems overlap.

## 14. When it breaks / Edge cases
- Unbalanced splits (like Quick Sort's worst case with a bad pivot) destroy the $O(\log N)$ depth guarantee and degrade to $O(N^2)$.

## 15. Comparison with alternative approaches
- **vs DP:** If subproblems are non-overlapping → D&C. If overlapping → DP. D&C does not cache; DP does.

---
*Where this shows up in ML:*
Distributed training (like Data Parallelism in PyTorch DDP) is conceptually Divide and Conquer: split the batch across GPUs, compute gradients independently, combine (all-reduce) the gradients.
"""

files["16-dsa-foundations/prefix-sums.md"] = r"""# Prefix Sums

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
"""

files["16-dsa-foundations/memoization.md"] = r"""# Memoization

## 1. Definition
Memoization is a Top-Down Dynamic Programming optimization technique that caches the return value of a recursive function for a given set of arguments, returning the cached result immediately if the function is called again with the same arguments.

## 2. Intuition
Imagine a student solving math problems. On a test with 100 questions, question 47 asks "What is 13 × 17?" and question 89 asks the same thing. A smart student writes the answer in the margin after question 47 and just looks it up for question 89. Memoization is the "write it in the margin" step.

## 3. Why it exists
Naive recursion for problems like Fibonacci or Longest Common Subsequence recomputes identical subproblems exponentially many times, yielding $O(2^N)$ complexity. Memoization computes each unique subproblem exactly once, collapsing the time complexity to the number of distinct states.

## 4. Mechanics
1. Write the recursive brute-force solution.
2. Identify the function parameters that define a unique subproblem (the "state").
3. Add a dictionary/array `memo` that maps `(state) -> result`.
4. At the top of the function: if `state in memo`, return `memo[state]`.
5. At the bottom, before returning: store `memo[state] = result`.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\text{unique states} \times \text{work per state})$. For Fibonacci: $O(N)$.
- **Space Complexity:** $O(\text{unique states})$ for the cache, plus $O(\text{depth})$ for the call stack.

## 6. Tiny worked example
Fibonacci without memoization: `fib(5)` calls `fib(4)` and `fib(3)`. `fib(4)` calls `fib(3)` and `fib(2)`. `fib(3)` is computed **twice**. Total calls: $2^N - 1 = 31$ for $N=5$.

With memoization: `fib(3)` computed once, stored. Second call returns instantly. Total calls: $2N - 1 = 9$ for $N=5$.

## 7. Code (Python, with type hints)
```python
from functools import lru_cache

# Python's @lru_cache automatically memoizes any pure function
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Manual memoization for more control (e.g., multi-parameter states)
def lcs(s1: str, s2: str) -> int:
    memo = {}
    def dp(i: int, j: int) -> int:
        if i == len(s1) or j == len(s2):
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        if s1[i] == s2[j]:
            result = 1 + dp(i + 1, j + 1)
        else:
            result = max(dp(i + 1, j), dp(i, j + 1))
        memo[(i, j)] = result
        return result
    return dp(0, 0)
```

## 8. Common mistakes
- Memoizing functions with mutable arguments (like lists). Mutable objects are not hashable and cannot be dict keys. Converts lists to tuples as dictionary keys.
- Forgetting to return `memo[state]` early. If you store in memo but still compute the full recursion, you get the right answer but no speedup.

## 9. 30-second interview answer
"Memoization caches recursive function results for previously computed inputs. It transforms exponential brute-force recursion into polynomial time by ensuring each unique state is computed exactly once. In Python, `@functools.lru_cache` provides this transparently for any pure function."

## 10. 2-minute interview answer
"Memoization is the Top-Down approach to Dynamic Programming. The workflow is systematic: write the brute-force recursive solution, identify what input values define a unique subproblem (these are the 'state variables'), and add a dictionary mapping `state -> result`. Before computing anything, check if the result is already cached. This simple pattern transforms Fibonacci from $O(2^N)$ to $O(N)$ and Longest Common Subsequence from $O(3^N)$ to $O(N \times M)$, reducing the problem's time complexity to exactly the number of distinct states times the work per state. Python's `@functools.lru_cache` automates this for functions with hashable arguments, making the pattern almost trivially easy to apply."

## 11. Follow-ups
- "When would you choose Memoization (Top-Down) over Tabulation (Bottom-Up)?" (Memoization is preferable when only a sparse subset of the state space is actually visited — for example, when many subproblems can be pruned early. Tabulation fills the entire table regardless).

## 12. Deeper questions
- "What is the difference between `lru_cache` and a plain `dict`-based memo?" (`lru_cache` has a configurable max size and evicts the Least Recently Used entry when full. A plain `dict` cache grows unboundedly. For interview problems with small inputs, both are equivalent).

## 13. Related concepts
- **Dynamic Programming (Bottom-Up Tabulation)**: The equivalent iterative approach.
- **Backtracking + Memo**: When memoization is added to backtracking to avoid recomputing the same state.

## 14. When it breaks / Edge cases
- If the recursion depth exceeds Python's default limit (~1000), a `RecursionError` is thrown. Use Bottom-Up DP or increase `sys.setrecursionlimit`.

## 15. Comparison with alternative approaches
- **vs Tabulation:** Memoization is recursive (uses call stack) and lazy (only computes needed states). Tabulation is iterative (no stack overflow risk) and eager (fills all states). Tabulation is usually faster in practice; memoization is easier to derive correctly.

---
*Where this shows up in ML:*
The KV-Cache in autoregressive LLM inference is conceptually memoization — previously computed key/value states are cached so they aren't recomputed at every new token generation step.
"""

files["16-dsa-foundations/recursion-vs-iteration.md"] = r"""# Recursion vs Iteration

## 1. Definition
**Recursion** solves a problem by having a function call itself with a smaller input until a base case is reached. **Iteration** solves the same problem by repeating a block of code with a loop and explicit state variables.

## 2. Intuition
- **Recursion:** To eat a pizza, eat one slice, then eat the rest of the pizza (which is now a smaller pizza). Keep going until no slices remain.
- **Iteration:** To eat a pizza, pick up a slice, eat it, pick up another slice, eat it, repeat until the pizza is gone.
Same result. Recursion expresses *what* to do. Iteration expresses *how* to step.

## 3. Why it exists
Recursion is often more **readable and mathematically natural** for problems that are inherently self-similar (trees, graphs, divide-and-conquer). Iteration is more **memory-efficient and performant**, as it avoids function call overhead and stack allocation.

## 4. Mechanics
- **Recursion:** Relies on the program's **call stack** to store intermediate state. Every call adds a stack frame containing local variables and the return address.
- **Iteration:** Explicitly maintains state in variables and loops. Uses no implicit stack; state lives only in heap/register variables.
- **Conversion:** Any recursive algorithm can be converted to an iterative one by using an explicit stack data structure (essentially simulating what the call stack does implicitly).

## 5. Complexity (Time & Space)
| Approach | Time | Space |
|---|---|---|
| Recursion | Same as iterative | $O(depth)$ call stack |
| Iteration | Same as recursive | $O(1)$ if no explicit stack |

## 6. Tiny worked example
Factorial of 5:
- **Recursive:** `f(5) → 5*f(4) → 5*4*f(3) → 5*4*3*f(2) → 5*4*3*2*f(1) → 120`. Stack depth = 5.
- **Iterative:** `result = 1; for i in [1..5]: result *= i`. Stack depth = 1 (constant).

## 7. Code (Python, with type hints)
```python
# Recursive DFS (concise, natural)
def dfs_recursive(root):
    if not root:
        return
    print(root.val)
    dfs_recursive(root.left)
    dfs_recursive(root.right)

# Iterative DFS (avoids Python's recursion limit)
from collections import deque
def dfs_iterative(root):
    if not root:
        return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.val)
        if node.right: stack.append(node.right)
        if node.left:  stack.append(node.left)
```

## 8. Common mistakes
- Using deep recursion in Python without checking the depth. Python's default recursion limit is 1000 frames. A perfectly balanced tree of depth 100,000 will cause `RecursionError`.
- Writing iterative code that is more complex and harder to verify than its recursive equivalent, introducing subtle bugs where recursion would have been cleaner.

## 9. 30-second interview answer
"Recursion is elegant and maps naturally to self-similar problems like trees and divide-and-conquer, but carries $O(depth)$ call stack overhead. Iteration is memory-efficient and avoids stack overflow risks, but can be verbose. Any recursion can be converted to iteration using an explicit stack. For Python, prefer iteration for deep structures to avoid the recursion limit."

## 10. 2-minute interview answer
"The choice between recursion and iteration is a space-clarity tradeoff. Recursion leverages the OS call stack to implicitly store computation state, producing clean, declarative code that closely mirrors mathematical definitions — like DFS or Merge Sort. However, the call stack is limited (Python: ~1000, Java: ~10,000), and each frame adds overhead from pushing/popping registers and setting up scope. Iteration uses explicit variables and loops, achieving $O(1)$ overhead per step at the cost of verbosity. For many tree problems in an interview context, recursive code is preferable for its clarity and correctness. For production code with deeply nested structures, iterative solutions using an explicit stack are safer. Tail-call optimization (supported in languages like Scheme, not Python or Java) can make recursion as efficient as iteration when the recursive call is the last operation in the function."

## 11. Follow-ups
- "What is tail recursion?" (When the recursive call is the *last operation* in the function — no pending computation after the call returns. Languages with tail-call optimization (TCO) reuse the current stack frame, achieving $O(1)$ space like iteration. Python does NOT support TCO).

## 12. Deeper questions
- "How do you convert Merge Sort from recursive to iterative?" (Bottom-up Merge Sort: start with subarrays of size 1, merge pairs to size 2, then 4, then 8, doubling each pass. No recursion stack needed).

## 13. Related concepts
- **Memoization**: Often paired with recursion to cache results.
- **Divide and Conquer**: Naturally expressed recursively.

## 14. When it breaks / Edge cases
- Python's recursion limit (1000) breaks on unbalanced trees or long chains. Use `sys.setrecursionlimit(N)` or convert to iteration.

## 15. Comparison with alternative approaches
- N/A — they are two sides of the same computational coin.

---
*Where this shows up in ML:*
Autograd in PyTorch computes gradients by traversing a recursively-built computation graph. Internally it uses iterative topological sorting to avoid deep Python call stacks.
"""

files["16-dsa-foundations/amortized-analysis.md"] = r"""# Amortized Analysis

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
"""

files["16-dsa-foundations/time-vs-space-complexity.md"] = r"""# Time vs Space Complexity

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
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch C - Sub-pass 3 Complete")
