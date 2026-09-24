# Pattern: Cyclic Sort

## 1. Definition
Cyclic Sort is an in-place $O(N)$ sorting algorithm specifically designed for arrays where the elements are known to fall within a continuous range from $1$ to $N$ (or $0$ to $N$).

## 2. Intuition
Imagine a team of 5 runners wearing jerseys numbered 1 through 5, standing in random order. To sort them, you look at the person in the first spot. If they are wearing jersey #4, you tell them to go to spot #4, and the person at spot #4 comes to spot #1. You repeat this until jersey #1 is finally in spot #1. Because every swap puts at least one person in their correct spot, everyone is sorted instantly.

## 3. Why it exists
Standard sorting takes $O(N \log N)$. If we know the array contains numbers from $1$ to $N$, we can use the array indices themselves as a Hash Map, sorting the array in $O(N)$ time and strictly $O(1)$ space. It is the optimal solution for finding missing or duplicate numbers in a fixed range.

## 4. Mechanics
1. Iterate through the array with index `i`.
2. Check if `nums[i]` is in its correct index (i.e., `nums[i] == nums[nums[i] - 1]`).
3. If not, swap `nums[i]` with the element at its target index.
4. Do NOT increment `i` until the correct number lands at `nums[i]`.
5. After the array is sorted, iterate again to find the index where the number doesn't match the index (the missing/duplicate number).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$. Even though there is a `while` loop inside a `for` loop, each number is swapped to its correct position at most once. Max swaps is $N-1$.
- **Space Complexity:** $O(1)$ auxiliary space.

## 6. Tiny worked example
Array: `[3, 1, 4, 2]`
- `i=0`, val=3. Target idx=2. Swap `arr[0]` and `arr[2]`. Array: `[4, 1, 3, 2]`.
- `i=0`, val=4. Target idx=3. Swap `arr[0]` and `arr[3]`. Array: `[2, 1, 3, 4]`.
- `i=0`, val=2. Target idx=1. Swap `arr[0]` and `arr[1]`. Array: `[1, 2, 3, 4]`.
- `i=0`, val=1. Correct! Move `i=1`.
- `i=1,2,3` all correct. Done.

## 7. Code (Python, with type hints)
```python
from typing import List

def find_missing_number(nums: List[int]) -> int:
    i, n = 0, len(nums)
    
    # 1. Cyclic Sort
    while i < n:
        j = nums[i] # Target index (assuming range 0 to N)
        if j < n and nums[i] != nums[j]:
            nums[i], nums[j] = nums[j], nums[i] # Swap
        else:
            i += 1
            
    # 2. Find missing
    for i in range(n):
        if nums[i] != i:
            return i
            
    return n
```

## 8. Common mistakes
- Using a `for` loop without adjusting the index. You must use a `while` loop, or explicitly keep checking `i` until it holds the correct value. If you swap and immediately move on, the new value swapped into `i` remains unchecked.
- Infinite loops caused by duplicate numbers. You must check `nums[i] != nums[j]` before swapping.

## 9. 30-second interview answer
"Cyclic sort is an $O(N)$ time, $O(1)$ space sorting algorithm for arrays containing numbers in a strict range from 1 to N. It works by treating the array indices as a hash map and swapping each number directly to its correct index. It's the definitive pattern for finding missing or duplicate numbers in a fixed range."

## 10. 2-minute interview answer
"Whenever an interview problem states 'an array containing numbers in the range 1 to N', it is screaming for a Cyclic Sort. While we could find missing or duplicate numbers using a Hash Set ($O(N)$ space) or by standard sorting ($O(N \log N)$ time), Cyclic Sort achieves the optimal $O(N)$ time and $O(1)$ space. The logic is simple: we iterate through the array, and if the number we are looking at isn't at its correct index, we swap it with the number that currently occupies its correct index. We repeat this at the current position until the correct number arrives, then move to the next position. Because every swap firmly places at least one number into its permanent home, the maximum number of swaps across the entire array is $N-1$, ensuring strictly linear time complexity."

## 11. Follow-ups
- "How do you find all duplicates in an array?" (After Cyclic Sort, any number sitting at the wrong index is a duplicate).

## 12. Deeper questions
- "What if the range is 1 to N, but the array is immutable/read-only?" (Cyclic Sort modifies the array. If immutable, use Floyd's Tortoise and Hare for duplicates, or Binary Search on Answer).

## 13. Related concepts
- **In-place Hashing**: Conceptually identical to Cyclic Sort.

## 14. When it breaks / Edge cases
- Fails completely if the numbers are negative, floats, or wildly out of bounds (e.g., `[1, 100000]`), as the array index mapping is destroyed.

## 15. Comparison with alternative approaches
- **vs Bit Manipulation (XOR):** XOR can find a single missing number in $O(N)$ time and $O(1)$ space without modifying the array, but Cyclic Sort handles multiple missing/duplicate numbers simultaneously.

---
*Where this shows up in ML:* 
Not generally used in ML contexts, purely a DSA optimization trick.
