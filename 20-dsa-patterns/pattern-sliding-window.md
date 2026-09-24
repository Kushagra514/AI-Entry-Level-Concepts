# Pattern: Sliding Window

## 1. Definition
The Sliding Window pattern involves creating a "window" over a subset of an array or string (often defined by two pointers, `left` and `right`) and shifting that window to solve problems involving contiguous subarrays or substrings.

## 2. Intuition
Imagine looking at a long landscape through a small rectangular window. Instead of picking up the window and moving it to every possible spot from scratch, you slowly slide it to the right, adding a new slice of the landscape on the right and losing a slice on the left. You only update what changed at the edges.

## 3. Why it exists
It exists to optimize $O(n^2)$ brute-force solutions that repeatedly evaluate overlapping subarrays. By keeping a running state of the window, we reuse the overlapping computations.

## 4. Mechanics
1. Initialize `left` and `right` pointers at the start (or `window_start`, `window_end`).
2. Expand the window by moving `right` and adding `arr[right]` to the window's state.
3. If the window violates a condition (or reaches a fixed size), shrink it by moving `left` and removing `arr[left]` from the state until the condition is valid again.
4. Update the global answer (e.g., max length, min length) at valid states.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - Both `left` and `right` pointers only move forward. Each element is processed at most twice (once added, once removed).
- **Space Complexity:** $O(1)$ to $O(K)$ depending on the state being tracked (e.g., a hash map of character counts).

## 6. Tiny worked example
Find max sum of subarray of size 3 in `[2, 1, 5, 1, 3, 2]`
- Window `[2, 1, 5]`: sum = 8. Max = 8.
- Slide right: add `1`, remove `2`. Window `[1, 5, 1]`: sum = 7. Max = 8.
- Slide right: add `3`, remove `1`. Window `[5, 1, 3]`: sum = 9. Max = 9.

## 7. Code (Python, with type hints)
```python
from typing import List

def max_sub_array_of_size_k(k: int, arr: List[int]) -> int:
    max_sum = 0
    window_sum = 0
    window_start = 0

    for window_end in range(len(arr)):
        window_sum += arr[window_end]  # add the next element

        # slide the window if we've hit the size k
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]  # subtract the element going out
            window_start += 1  # slide the window ahead
            
    return max_sum
```

## 8. Common mistakes
- Confusing *fixed* window (size $K$ is given) with *dynamic* window (shrink/expand based on a condition like sum < $S$).
- Forgetting to remove the `arr[left]` element from the state when shrinking the window.
- Off-by-one errors when checking window size (`window_end - window_start + 1`).

## 9. 30-second interview answer
"Sliding Window is an optimization technique used for problems involving contiguous subarrays or substrings. By maintaining a dynamic or fixed-size window and updating the state incrementally as the window shifts, it reduces nested loops ($O(N^2)$) to a single linear pass ($O(N)$)."

## 10. 2-minute interview answer
"Whenever a problem asks for the longest, shortest, or optimal contiguous subarray or substring, Sliding Window is my first thought. Instead of re-evaluating overlapping subarrays from scratch, we maintain a state—like a running sum or a frequency map—within a window defined by two pointers. We expand the right edge to explore new elements, and if a constraint is violated, we shrink the left edge until the window is valid again. This guarantees that both pointers only move forward, turning an $O(N^2)$ brute-force approach into an $O(N)$ time complexity solution. It perfectly balances exploring the search space while caching the overlapping computations."

## 11. Follow-ups
- "What if the array contains negative numbers and we need a dynamic window for a target sum?" (Sliding window breaks here because expanding doesn't guarantee the sum increases. We need Prefix Sums + Hash Map instead).

## 12. Deeper questions
- "How would you implement a sliding window minimum/maximum over an array?" (Requires an auxiliary Monotonic Deque to maintain the optimal elements in the window in $O(N)$).

## 13. Related concepts
- **Two Pointers**: Sliding window is a specific subtype of Two Pointers.
- **Prefix Sums**: Often used as an alternative when sliding window doesn't work (e.g., negative numbers).

## 14. When it breaks / Edge cases
- Fails when the target condition doesn't have a monotonic property (e.g., if adding an element might make a previously invalid window valid, you don't know when to shrink).

## 15. Comparison with alternative approaches
- **vs Dynamic Programming:** DP solves subsets/subsequences (non-contiguous). Sliding Window solves contiguous segments.

---
*Where this shows up in ML:* 
In NLP, n-grams extraction relies on a sliding window over tokens. In Time Series forecasting, we create training datasets by passing a sliding window over historical data (e.g., taking the past 7 days to predict the 8th day).
