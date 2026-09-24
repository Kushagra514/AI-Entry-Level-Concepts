import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Remaining Topics)"')

wc("16-dsa-foundations/sliding-window.md", r"""# Sliding Window

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
""")

wc("20-dsa-patterns/pattern-two-pointers.md", r"""# Pattern: Two Pointers

## 1. Definition
The Two Pointers pattern involves using two pointers to iterate through an array or list, often from different ends or at different speeds, to solve problems related to pairs, subarrays, or specific conditions.

## 2. Intuition
Imagine you're trying to find two numbers in a sorted array that sum to a target. If you start one pointer at the beginning (smallest) and one at the end (largest), you can intelligently narrow down the search by moving the left pointer right to increase the sum, or the right pointer left to decrease it.

## 3. Why it exists
Many problems require comparing elements at different positions. A naive nested loop takes $O(N^2)$ time. Two pointers reduce this to $O(N)$ or $O(N \log N)$ (if sorting is required) by traversing the collection linearly.

## 4. Mechanics
- **Opposite Ends:** Pointers start at index 0 and index $N-1$ and move towards the center (e.g., checking for palindromes, Two Sum II). Requires a sorted array for sum-related problems.
- **Same Direction:** Pointers start at index 0 and move in the same direction, often at different speeds (e.g., removing duplicates, fast/slow pointers for linked list cycles).
- **Two Arrays:** Pointers traverse two different sorted arrays (e.g., merging two sorted arrays).

## 5. Complexity (Time & Space)
- **Time:** $O(N)$ for the traversal itself. If the array needs sorting first, the overall time is $O(N \log N)$.
- **Space:** $O(1)$ auxiliary space.

## 6. Tiny worked example
*Two Sum II (Sorted Array).* Array: `[2, 7, 11, 15]`, Target: `9`
`left = 0` (val: 2), `right = 3` (val: 15). Sum = 17.
17 > 9, so move `right` left. `right = 2` (val: 11). Sum = 13.
13 > 9, so move `right` left. `right = 1` (val: 7). Sum = 9.
9 == 9, return `[left, right]`.

## 7. Code (Python)
```python
def pair_with_targetsum(arr, target_sum):
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target_sum:
            return [left, right]
        
        if target_sum > current_sum:
            left += 1  # we need a pair with a bigger sum
        else:
            right -= 1  # we need a pair with a smaller sum
            
    return [-1, -1]
```

## 8. Common mistakes
- **Not sorting the array:** The opposite-ends technique for sum problems *requires* the array to be sorted.
- **Pointer overlap:** Forgetting the `while left < right` condition and letting the pointers cross each other, leading to duplicate pairs or infinite loops.

## 9. 30-second interview answer
"The Two Pointers pattern uses two indices to traverse a data structure linearly, often to avoid nested loops. The most common variants are opposite-ends pointers (starting at the ends and moving inward, typically used on sorted arrays for sum problems) and same-direction pointers (like fast/slow pointers). It generally reduces time complexity to $O(N)$ while using $O(1)$ space."

## 10. 2-minute interview answer
"Two Pointers is a highly versatile pattern used primarily for arrays and linked lists. For sorted arrays, the opposite-ends approach is standard. If we want to find a pair that sums to a target, we place one pointer at the start and one at the end. Since the array is sorted, if the sum is too small, we increment the left pointer; if it's too large, we decrement the right pointer. This gives an $O(N)$ solution instead of an $O(N^2)$ brute force. For problems like removing duplicates in-place, we use two pointers moving in the same direction: a 'slow' pointer tracks the position of the next unique element, while a 'fast' pointer scans for new unique elements. A specialized version of this is the Fast & Slow Pointers (Tortoise and Hare) technique used in Linked Lists to detect cycles or find the middle node. The defining characteristic of two-pointer solutions is their $O(1)$ space efficiency."

## 11. Follow-ups
- "Can you use this for finding triplets (3Sum)?" (Yes. Sort the array, then iterate through the array. For each element `i`, use the Two Pointers technique on the subarray `i+1` to `N-1` to find a pair that sums to `-arr[i]`).

## 12. Deeper questions
- "How does the Dutch National Flag problem use two pointers?" (It actually uses *three* pointers to partition an array into three segments (e.g., sorting 0s, 1s, and 2s) in a single pass).

## 13. Related concepts
- **Sliding Window**: A specific case of two pointers moving in the same direction.
- **Fast & Slow Pointers**: Another sub-pattern.

## 14. When it breaks / Edge cases
- Unsorted arrays for sum problems: Two pointers won't work. Use a Hash Map instead (which takes $O(N)$ space but $O(N)$ time without needing a sort).

## 15. Comparison with alternative approaches
- **Two Pointers vs Hash Map:** Hash Map gives $O(N)$ time and $O(N)$ space for Two Sum. Two Pointers (if sorted) gives $O(N)$ time and $O(1)$ space. If unsorted, Two Pointers is $O(N \log N)$ time and $O(1)$ space.

---
*Where this shows up in ML:*
Data preprocessing, text tokenization boundaries, merging sorted datasets.
""")

