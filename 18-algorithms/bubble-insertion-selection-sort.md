# Bubble, Insertion, and Selection Sort

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
