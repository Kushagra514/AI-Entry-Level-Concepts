# Merge Sort

## 1. Definition
Merge Sort is a stable, divide-and-conquer, comparison-based sorting algorithm that recursively splits an array into halves, sorts them, and merges them back together.

## 2. Intuition
If you have a messy stack of 100 papers to alphabetize, you could split it into two stacks of 50, hand one to a friend, and both alphabetize your stacks. When you're done, you look at the top paper of each stack and repeatedly take the alphabetically smaller one, perfectly merging the two sorted stacks into one.

## 3. Why it exists
Older algorithms like Insertion or Bubble sort took $O(N^2)$ time, which scales terribly. Merge Sort was invented by John von Neumann in 1945 to guarantee an $O(N \log N)$ worst-case time complexity, providing a mathematical ceiling on how slow sorting could be.

## 4. Mechanics
1. **Divide:** Recursively divide the array into two halves until you have sub-arrays of size 1 (which are inherently sorted).
2. **Conquer/Merge:** Take two sorted sub-arrays and merge them into a single sorted array. 
3. To merge: use two pointers, one at the start of each sub-array. Compare the elements, copy the smaller one to a temporary array, and move the pointer forward.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \log N)$ in Best, Average, and Worst cases. The array is split in half $\log N$ times, and merging takes $O(N)$ time at each level.
- **Space Complexity:** $O(N)$ - Requires a temporary array of size $N$ to hold the merged elements.

## 6. Tiny worked example
`[38, 27, 43, 3]`
- Split: `[38, 27]` and `[43, 3]`
- Split: `[38]`, `[27]` and `[43]`, `[3]`
- Merge: `[27, 38]` and `[3, 43]`
- Merge: Compare 27 and 3. Take 3. Compare 27 and 43. Take 27. Compare 38 and 43. Take 38. Take 43. -> `[3, 27, 38, 43]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # The '<=' ensures STABILITY. 
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # Append any remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged
```

## 8. Common mistakes
- Forgetting that array slicing in Python (`arr[:mid]`) creates copies, which is fine for readability but adds overhead. In strict interviews, you should pass index pointers `(arr, start, end)` to save memory.
- Using `<` instead of `<=` during the merge step, which breaks the **stability** of the sort.

## 9. 30-second interview answer
"Merge Sort is a divide-and-conquer algorithm with a guaranteed $O(N \log N)$ time complexity. It works by recursively halving the array until size 1, then merging the sorted halves. It is a stable sort, but its main drawback is requiring $O(N)$ auxiliary space."

## 10. 2-minute interview answer
"Merge sort is the textbook example of divide-and-conquer. Because it strictly halves the data $\log N$ times and merges them in $N$ operations per level, it strictly guarantees $O(N \log N)$ time across best, average, and worst cases. Furthermore, it is a stable sort—if two elements are equal, their original relative order is preserved, which is vital when sorting objects by multiple criteria. However, because it cannot easily merge arrays in-place without degrading to $O(N^2)$, it requires $O(N)$ auxiliary memory. Therefore, for purely in-memory arrays, Quicksort is often preferred for cache locality, but Merge Sort shines for Linked Lists or external sorting where data doesn't fit in RAM."

## 11. Follow-ups
- "Why is Merge Sort better than Quick Sort for Linked Lists?" (Linked lists don't have random access, making Quick Sort's pivot swapping inefficient. Merge Sort easily splits linked lists and merges them by just changing pointers in $O(1)$ space).

## 12. Deeper questions
- "How does Merge Sort apply to External Sorting?" (If you have 100GB of data and 1GB of RAM, you chunk the data into 1GB files, sort them in RAM, and then stream them back using the Merge step of Merge Sort).

## 13. Related concepts
- **Count Inversions**: A classic hard interview problem solved by slightly modifying the Merge Sort merge step.
- **Divide and Conquer**: The overarching algorithmic paradigm.

## 14. When it breaks / Edge cases
- Fails in highly memory-constrained embedded environments due to the $O(N)$ space requirement.

## 15. Comparison with alternative approaches
- **vs Quick Sort:** Quick Sort is usually faster in practice (better cache locality) and uses $O(\log N)$ space, but is unstable and has a worst-case of $O(N^2)$. Merge Sort is stable, strictly $O(N \log N)$, but takes $O(N)$ space.

---
*Where this shows up in ML:* 
When training models on datasets too large to fit in RAM (e.g., shuffling terabytes of TFRecords), distributed systems use External Merge Sort to order and process the data chunks on disk.
