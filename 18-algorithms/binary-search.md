# Binary Search

## 1. Definition
Binary Search is a divide-and-conquer algorithm that finds the position of a target value within a **sorted** array by repeatedly dividing the search interval in half.

## 2. Intuition
If you are looking for the word "Machine" in a physical dictionary, you don't start at page 1 and flip one by one. You open to the middle. If you see "Orange", you know "Machine" must be in the left half. You tear the book in half, discard the right side, and repeat until you find the word. 

## 3. Why it exists
Linear search takes $O(N)$ time, which is too slow for massive datasets. Binary search exists to exploit the property of "sortedness" (monotonicity), reducing the search time exponentially to $O(\log N)$.

## 4. Mechanics
1. Initialize two pointers: `left = 0`, `right = len(array) - 1`.
2. Find the midpoint: `mid = left + (right - left) // 2`.
3. Check if `array[mid] == target`. If so, return `mid`.
4. If `array[mid] < target`, the target must be in the right half. Update `left = mid + 1`.
5. If `array[mid] > target`, the target must be in the left half. Update `right = mid - 1`.
6. Repeat until `left > right`.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\log N)$ - The search space is halved every step.
- **Space Complexity:** $O(1)$ - Iterative implementation requires just three pointers (`left`, `right`, `mid`).

## 6. Tiny worked example
Array: `[2, 4, 6, 8, 10]`, Target: `8`
- `L=0`, `R=4`. `mid=2` (val `6`). `6 < 8`, so `L = 3`.
- `L=3`, `R=4`. `mid=3` (val `8`). `8 == 8`. Found at index 3.

## 7. Code (Python, with type hints)
```python
from typing import List

def binary_search(arr: List[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    
    while left <= right:
        # Prevents integer overflow in languages like Java/C++
        mid = left + (right - left) // 2 
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1
```

## 8. Common mistakes
- **Off-by-one errors:** Using `while left < right` instead of `<=`, or `left = mid` instead of `mid + 1`, causing infinite loops.
- Calculating mid as `(left + right) // 2`. In Python this is fine, but in Java/C++ it can cause integer overflow if left and right are huge. Use `left + (right - left) / 2`.
- Attempting to use Binary Search on an unsorted array.

## 9. 30-second interview answer
"Binary Search is an $O(\log N)$ algorithm for finding a target in a sorted array. It works by repeatedly comparing the target to the middle element and halving the search space. It's incredibly fast but requires the data to be monotonic."

## 10. 2-minute interview answer
"Binary Search is the premier algorithm for optimizing $O(N)$ searches down to $O(\log N)$, provided the search space is sorted or monotonic. The classic implementation uses a `while left <= right` loop and integer division to find the midpoint. The most critical part of writing it bug-free is ensuring the search boundaries shrink correctly (`left = mid + 1` and `right = mid - 1`) to avoid infinite loops. Beyond simple arrays, the most powerful application of this pattern in interviews is 'Binary Search on the Answer', where we binary search not over an array, but over a numerical range of possible answers, validating each midpoint using a helper function."

## 11. Follow-ups
- "How do you find the *first* occurrence of a target in an array with duplicates?" (Modify the check: if `arr[mid] == target`, don't return. Instead, record the index and shrink the right bound `right = mid - 1` to keep searching left).
- "What is `bisect` in Python?" (Python's built-in binary search library).

## 12. Deeper questions
- "How would you perform Binary Search on an array where the size is unknown or infinite?" (Start with bounds 0 and 1. If target > arr[1], double the bounds to 1 and 2, then 2 and 4, 4 and 8... until you bound the target, then do standard binary search. $O(\log P)$ where P is position).

## 13. Related concepts
- **Binary Search Trees (BST)**: A tree structure built around the binary search concept.
- **Binary Search on Answer**: A master pattern for optimization problems.

## 14. When it breaks / Edge cases
- Breaks entirely if the array isn't sorted.
- Fails if the array contains duplicate targets and you are asked for a specific one (without modifying the standard template).

## 15. Comparison with alternative approaches
- **vs Hash Map:** Hash Map gives $O(1)$ search, but takes $O(N)$ space and loses sorted ordering (e.g., you can't easily find "the closest number" with a Hash Map, but you can with Binary Search).

---
*Where this shows up in ML:* 
In Decision Trees, finding the optimal threshold to split continuous numerical features often involves sorting the features and searching (though fully exhaustive trees check all points, optimized versions use bisecting logic). Additionally, in hyperparameter tuning, if a parameter's effect on loss is monotonic, one could conceptually binary-search for the optimal value.
