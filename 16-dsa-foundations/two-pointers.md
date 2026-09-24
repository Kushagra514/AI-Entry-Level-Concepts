# Two Pointers Core Idea

## 1. Definition
The Two Pointers technique involves using two integer variables (pointers) to iterate through an iterable (like an array or string), often from different ends or at different speeds, to solve problems optimally.

## 2. Intuition
Imagine trying to find if a word is a palindrome. Instead of reversing the whole word and comparing it, you just point one finger at the first letter and one at the last letter. If they match, you move both fingers inward. You process the word efficiently by converging on the center.

## 3. Why it exists
Many naive solutions require nested loops ($O(n^2)$ time) to compare every pair of elements. Two Pointers allows us to reduce this to a single pass ($O(n)$ time) by intelligently moving pointers based on the sorted nature of the data or specific constraints.

## 4. Mechanics
- **Opposite Ends (Collision):** One pointer starts at index 0, the other at $n-1$. They move inward until they meet. Typically used on sorted arrays (e.g., Two Sum on sorted array).
- **Same Direction (Fast/Slow):** Both start at index 0. One moves faster than the other. Used for cycle detection or finding midpoints.
- **Two Iterables:** Pointers iterate over two different arrays simultaneously (e.g., merging two sorted arrays).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(n)$ - Each pointer traverses the sequence at most once.
- **Space Complexity:** $O(1)$ - Only two integer variables are used.

## 6. Tiny worked example
Find pair summing to 6 in sorted array: `[1, 2, 4, 5]`
- `L=1` (index 0), `R=5` (index 3). Sum = 6. Found!
- If target was 7: `L=1`, `R=5`. Sum = 6 < 7. Move L right.
- `L=2`, `R=5`. Sum = 7. Found!

## 7. Code (Python, with type hints)
```python
from typing import List

def two_sum_sorted(arr: List[int], target: int) -> List[int]:
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1  # Need a larger sum
        else:
            right -= 1 # Need a smaller sum
            
    return [-1, -1]
```

## 8. Common mistakes
- Using collision pointers on an **unsorted** array (the logic breaks because moving L/R doesn't guarantee an increase/decrease).
- Using `while left <= right` when `left < right` is required, leading to using the same element twice.
- Off-by-one errors when updating pointers.

## 9. 30-second interview answer
"Two Pointers is a space-efficient technique that uses two indices to traverse a data structure. It usually reduces an $O(n^2)$ search to $O(n)$. It is most commonly used on sorted arrays to find pairs, or on linked lists to detect cycles using fast and slow pointers."

## 10. 2-minute interview answer
"The Two Pointers pattern is a fundamental optimization technique for linear data structures. By using two indices, we can avoid nested iterations, trading $O(n^2)$ time for $O(n)$ time, while maintaining $O(1)$ space. The most common variant is the opposite-directional pointers used on sorted arrays; because the array is monotonic, we can deterministically decide which pointer to move to approach a target sum. Another critical variant is the fast/slow pointer technique, which is indispensable for linked lists where we lack random access, allowing us to find cycles or midpoints in a single pass. It's often the most elegant solution when space constraints prohibit using a Hash Map."

## 11. Follow-ups
- "What if the array is unsorted?" (You must sort it first $O(n \log n)$, or use a Hash Map $O(n)$ time / $O(n)$ space).
- "How does this apply to linked lists?" (Fast and slow pointers - Floyd's Cycle Detection).

## 12. Deeper questions
- "Can you use 3 pointers?" (Yes, for 3Sum, we lock one element and use 2 pointers for the rest, reducing $O(n^3)$ to $O(n^2)$).

## 13. Related concepts
- **Sliding Window**: A specific subtype of two pointers where the elements *between* the pointers form a valid state.
- **Binary Search**: Sometimes confused, but Binary Search jumps halves, while Two Pointers moves step-by-step.

## 14. When it breaks / Edge cases
- Fails on unsorted arrays for pair-sum problems.
- Be careful with arrays of size 0 or 1.

## 15. Comparison with alternative approaches
- **vs Hash Map:** Hash map can solve Two Sum on *unsorted* arrays in $O(n)$ time, but uses $O(n)$ space. Two Pointers on a sorted array is $O(n)$ time and $O(1)$ space.

---
*Where this shows up in ML:* 
In NLP, when processing sequences or implementing custom tokenizers, two-pointer techniques are frequently used to scan strings, identify word boundaries, or strip whitespace efficiently without allocating new strings in memory.
