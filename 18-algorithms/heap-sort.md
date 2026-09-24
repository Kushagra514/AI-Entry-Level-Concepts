# Heap Sort

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
