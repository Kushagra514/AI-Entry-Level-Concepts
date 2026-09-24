# Sliding Window

## 1. Definition
The Sliding Window pattern is an algorithmic technique used to perform operations on a specific window size of a given array or string. It reduces the use of nested loops and replaces them with a single loop, thereby reducing time complexity.

## 2. Intuition
Imagine a window of fixed or variable size sliding over an array from left to right. Instead of recalculating the sum or checking conditions for every element inside the window from scratch, we just remove the effect of the element that slides out of the window and add the effect of the new element sliding in.

## 3. Why it exists
Many problems require finding the maximum, minimum, or longest/shortest subarray that satisfies a certain condition. A naive approach calculates this for every possible subarray, resulting in $O(N^2)$ or $O(N^3)$ time complexity. Sliding window reduces this to $O(N)$.

## 4. Mechanics
- **Fixed Window:** The window size is constant. We maintain the state of the window and update it as we move one step to the right.
- **Variable Window:** The window size can change. We use two pointers (left and right). We expand the window by moving the right pointer and shrink it by moving the left pointer when a condition is violated.

## 5. Complexity (Time & Space)
- **Time:** $O(N)$ because each element is added and removed from the window at most once.
- **Space:** $O(1)$ auxiliary space, or $O(K)$ if we need a hash map to store frequencies of elements in the window.

## 6. Tiny worked example
*Find max sum subarray of size 3.*
Array: `[2, 1, 5, 1, 3, 2]`
Window 1: `[2, 1, 5]` -> Sum = 8
Slide right: Remove 2, Add 1. Window 2: `[1, 5, 1]` -> Sum = 7
Slide right: Remove 1, Add 3. Window 3: `[5, 1, 3]` -> Sum = 9
Max sum = 9.

## 7. Code (Python)
```python
def max_sub_array_of_size_k(k, arr):
    max_sum = 0
    window_sum = 0
    window_start = 0

    for window_end in range(len(arr)):
        window_sum += arr[window_end]  # add the next element

        # slide the window, we don't need to slide if we've not hit the required window size of 'k'
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]  # subtract the element going out
            window_start += 1  # slide the window ahead
            
    return max_sum
```

## 8. Common mistakes
- **Off-by-one errors:** Miscalculating when the window reaches the required size or when to move the left pointer.
- **Handling shrinking incorrectly:** In variable windows, shrinking might require a `while` loop, not just an `if` statement, to ensure the window becomes valid again.

## 9. 30-second interview answer
"The Sliding Window pattern is used for finding contiguous subarrays or substrings that satisfy a condition. It can be fixed or variable size. It optimizes $O(N^2)$ brute-force solutions to $O(N)$ by reusing the computation from the previous window and only updating the elements that enter and exit the window."

## 10. 2-minute interview answer
"Sliding window is a foundational pattern for array and string problems. The core idea is to maintain a 'window' of elements that satisfy a specific condition. For fixed-size windows, like finding the max sum of a subarray of size K, we initialize the window sum, then as we iterate, we add the new element and subtract the element that fell out of the window. For variable-size windows, like finding the longest substring with K distinct characters, we use two pointers. We expand the window by moving the right pointer and adding characters to a frequency map. If the window violates the condition (e.g., more than K distinct characters), we shrink it by moving the left pointer until the condition is satisfied again. Because both the left and right pointers only move forward, every element is processed at most twice (once entering, once leaving), guaranteeing an $O(N)$ time complexity."

## 11. Follow-ups
- "How do you handle a sliding window problem with negative numbers?" (Fixed sliding window still works. But variable sliding window for a target sum might fail because adding a negative number decreases the sum, breaking the monotonic property. Prefix sums or a Deque might be needed).

## 12. Deeper questions
- "What if the window condition requires finding the maximum element in the current window?" (Use a Monotonic Deque, which keeps the elements in descending order and removes elements that are out of the window bounds. This achieves $O(N)$ time for the Sliding Window Maximum problem).

## 13. Related concepts
- **Two Pointers**: Sliding window is a specific type of two-pointer technique.
- **Prefix Sums**: Sometimes used in conjunction with or as an alternative to sliding windows.

## 14. When it breaks / Edge cases
- Subsequences (non-contiguous elements). Sliding window only works for contiguous subarrays/substrings.

## 15. Comparison with alternative approaches
- **Sliding Window vs DP:** Sliding window is for contiguous elements. DP can handle non-contiguous subsequences.

---
*Where this shows up in ML:*
Time-series forecasting, moving averages, rolling window metrics.
