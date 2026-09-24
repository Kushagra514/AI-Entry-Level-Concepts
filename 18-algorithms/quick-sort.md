# Quick Sort

## 1. Definition
Quick Sort is a highly efficient, divide-and-conquer, in-place sorting algorithm. It works by selecting a 'pivot' element and partitioning the other elements into two sub-arrays, according to whether they are less than or greater than the pivot.

## 2. Intuition
Imagine a gym teacher organizing students by height. They pick a random student (the pivot). They tell everyone shorter to stand on the left, and everyone taller to stand on the right. Now, the pivot is in their exact final position. They then do the same thing for the group on the left, and the group on the right, recursively.

## 3. Why it exists
While Merge Sort guarantees $O(N \log N)$ time, it requires $O(N)$ extra memory. Quick Sort was developed to sort data *in-place*, drastically reducing memory overhead and taking advantage of CPU caching, making it practically faster for most real-world arrays.

## 4. Mechanics
1. **Choose Pivot:** Pick an element from the array (first, last, random, or median).
2. **Partition:** Rearrange the array so all elements smaller than the pivot are to its left, and all larger elements are to its right.
3. **Recursion:** Recursively apply the above steps to the sub-array of smaller elements and the sub-array of larger elements.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Best / Average: $O(N \log N)$
  - Worst: $O(N^2)$ (occurs when the pivot is always the smallest or largest element, usually on an already sorted array with a naive pivot).
- **Space Complexity:** $O(\log N)$ on average for the recursive call stack. $O(N)$ worst-case stack depth.

## 6. Tiny worked example
Array: `[10, 80, 30, 90, 40]`
- Pick pivot `40` (last element).
- Partition: `[10, 30]` (less) + `40` + `[80, 90]` (greater).
- `40` is locked. Recursively quicksort `[10, 30]` and `[80, 90]`.
- Array becomes `[10, 30, 40, 80, 90]`.

## 7. Code (Python, with type hints)
```python
from typing import List
import random

def quick_sort(arr: List[int], low: int, high: int) -> None:
    if low < high:
        # Partition the array and get the pivot index
        pi = partition(arr, low, high)
        
        # Recursively sort the sub-arrays
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr: List[int], low: int, high: int) -> int:
    # Pick a random pivot to avoid O(N^2) on sorted arrays
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    
    pivot = arr[high]
    i = low - 1  # Index of smaller element
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    # Swap pivot to its final position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

## 8. Common mistakes
- Using the first or last element as the pivot *without* randomization, which causes $O(N^2)$ time on already-sorted arrays (a common real-world scenario).
- Forgetting that Quick Sort is **Unstable**.
- Writing out-of-place Quick Sort in interviews (e.g., using list comprehensions `[x for x in arr if x < p]`). This is readable but ruins the $O(1)$ auxiliary space benefit, showing a lack of systems understanding.

## 9. 30-second interview answer
"Quick Sort is an in-place, divide-and-conquer sorting algorithm. It partitions an array around a pivot element and recursively sorts the left and right sides. It averages $O(N \log N)$ time and $O(\log N)$ space but can degrade to $O(N^2)$ if pivots are chosen poorly. It is unstable."

## 10. 2-minute interview answer
"Quick Sort is usually the fastest comparison-based sort in practice because its in-place partitioning makes it highly cache-efficient. The algorithm hinges on the partition step, where we place a pivot element in its final sorted position by swapping smaller elements to its left and larger to its right. Because it operates in-place, it only requires $O(\log N)$ auxiliary space for the recursion stack. The critical flaw is its worst-case $O(N^2)$ time complexity, which happens if the data is already sorted and we naively pick the last element as a pivot. We mitigate this by choosing a random pivot or using the Median-of-Three method. Unlike Merge Sort, it is unstable, meaning it may swap the relative order of identical elements."

## 11. Follow-ups
- "What is Quickselect?" (A modification of Quick Sort that only recurses into one half of the partition to find the $K$-th largest element in average $O(N)$ time).

## 12. Deeper questions
- "How does Python's Timsort avoid Quick Sort's instability?" (It doesn't use Quick Sort at all; it uses Merge Sort and Insertion Sort).

## 13. Related concepts
- **Merge Sort**: The stable, out-of-place alternative.
- **Top-K Elements**: Solved via Quickselect.

## 14. When it breaks / Edge cases
- Deep recursion on worst-case pivots can cause Stack Overflows in languages without deep stack limits.

## 15. Comparison with alternative approaches
- **vs Merge Sort:** Quick Sort is in-place ($O(\log N)$ space) and faster due to cache locality, but unstable. Merge Sort is out-of-place ($O(N)$ space) but stable and guaranteed $O(N \log N)$ time.

---
*Where this shows up in ML:* 
Finding the Median or Top-K probabilities (e.g., Top-K sampling in LLM generation) uses Quickselect, which relies entirely on the Quick Sort partitioning subroutine.
