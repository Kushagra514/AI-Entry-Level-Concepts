# Pattern: Two Pointers

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
