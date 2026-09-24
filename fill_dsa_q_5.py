import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (DSA Qs)"')

wc("23-dsa-interview-questions/greedy.md", r"""# Greedy Interview Questions

---

## 1. Jump Game

### 1. Restate the Problem
Given an integer array `nums` where `nums[i]` represents your maximum jump length at that position, return true if you can reach the last index.

### 2. Clarify Edge Cases
- Array length 1? Always True (already at last index).
- `[0]`? True. `[0, 1]`? False.

### 3. Brute Force Approach
DFS/Backtracking. From each index, try all possible jumps from 1 to `nums[i]`. Time: $O(2^N)$ because at each step we have multiple choices.

### 4. Key Insight
Instead of searching forward and trying every path, we can work backwards. Ask: "Can I reach the end from the second-to-last position?" If yes, then the goal just became reaching the second-to-last position. We can aggressively shift our "goal post" backwards.

### 5. Optimized Approach (Greedy)
Initialize `goal = len(nums) - 1`. Iterate backwards through the array from `len(nums) - 2` to `0`. If the current index `i` plus its jump length `nums[i]` is greater than or equal to `goal`, we know we can reach the goal from `i`. So, update `goal = i`. After the loop, if `goal == 0`, return True.

### 6. Justification
Time: $O(N)$ because we do a single pass backwards through the array. Space: $O(1)$ because we only track a single integer (`goal`).

### 7. Code (Python)
```python
from typing import List

def canJump(nums: List[int]) -> bool:
    goal = len(nums) - 1
    
    for i in range(len(nums) - 1, -1, -1):
        if i + nums[i] >= goal:
            goal = i
            
    return True if goal == 0 else False
```

### 8. Dry Run
`nums = [2, 3, 1, 1, 4]`
- init: goal = 4
- i=3 (val 1): 3+1 >= 4. goal = 3
- i=2 (val 1): 2+1 >= 3. goal = 2
- i=1 (val 3): 1+3 >= 2. goal = 1
- i=0 (val 2): 0+2 >= 1. goal = 0
- loop ends. goal == 0. True.

### 9. Edge Cases Handled
Length 1 array: loop runs zero times, `goal == 0`, returns True.

### 10. Follow-ups
- "What if you need to find the *minimum number of jumps* to reach the end?" -> This requires a forward greedy approach (Jump Game II), tracking the farthest reachable index for the current jump.

### 11. Related Problems
Jump Game II, Maximum Subarray (Kadane's).

---

## 2. Maximum Subarray (Kadane's Algorithm)

### 1. Restate the Problem
Given an integer array `nums`, find the contiguous subarray containing at least one number which has the largest sum and return its sum.

### 2. Clarify Edge Cases
- All negative numbers? Should return the single largest negative number (least negative).
- Empty array? Constraints usually say $\ge 1$ elements.

### 3. Brute Force Approach
Calculate the sum of every possible subarray (nested loops). Time: $O(N^2)$, Space: $O(1)$.

### 4. Key Insight
A negative prefix sum will only hurt any future subarray. If the running sum ever drops below zero, we should completely discard it and start a new subarray from the next element.

### 5. Optimized Approach (Greedy/DP)
Initialize `max_sub = nums[0]` and `current_sum = 0`. Iterate through the array. If `current_sum` is negative, reset it to 0. Add the current number to `current_sum`. Update `max_sub = max(max_sub, current_sum)`.

### 6. Justification
Time: $O(N)$ for a single pass. Space: $O(1)$ for two variables.

### 7. Code (Python)
```python
def maxSubArray(nums: List[int]) -> int:
    max_sub = nums[0]
    current_sum = 0
    
    for num in nums:
        if current_sum < 0:
            current_sum = 0
        current_sum += num
        max_sub = max(max_sub, current_sum)
        
    return max_sub
```

### 8. Dry Run
`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`
- init: max_sub=-2, current_sum=0
- -2: sum=-2, max_sub=-2
- 1: sum < 0 so reset sum=0. sum=1, max_sub=1
- -3: sum=-2, max_sub=1
- 4: sum < 0 so reset sum=0. sum=4, max_sub=4
- -1: sum=3, max_sub=4
- 2: sum=5, max_sub=5
- 1: sum=6, max_sub=6
- -5: sum=1, max_sub=6
- 4: sum=5, max_sub=6
- Return 6.

### 9. Edge Cases Handled
All negative array: `current_sum` resets to 0 before adding the next negative, so it essentially just checks single elements and returns the max single negative.

### 10. Follow-ups
- "Can you print the actual subarray?" -> Keep track of `start` and `end` indices, updating `start` whenever `current_sum` is reset.

### 11. Related Problems
Maximum Product Subarray, Longest Increasing Subsequence.
""")

wc("23-dsa-interview-questions/binary-search.md", r"""# Binary Search Interview Questions

---

## 1. Binary Search

### 1. Restate the Problem
Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, return its index. Otherwise, return `-1`.

### 2. Clarify Edge Cases
- Target not in array? Return -1.
- Array length 0? Return -1.

### 3. Brute Force Approach
Linear scan through the array. Time: $O(N)$.

### 4. Key Insight
Because the array is sorted, comparing the target to the middle element allows us to definitively eliminate half of the remaining array in one operation.

### 5. Optimized Approach
Initialize `l = 0` and `r = len(nums) - 1`. Loop `while l <= r`. Calculate `mid = (l + r) // 2`. If `nums[mid] == target`, return `mid`. If `nums[mid] < target`, the target must be on the right, so `l = mid + 1`. Else, it's on the left, so `r = mid - 1`.

### 6. Justification
Time: $O(\log N)$ because the search space halves at each step. Space: $O(1)$.

### 7. Code (Python)
```python
from typing import List

def search(nums: List[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    
    while l <= r:
        # mid = l + ((r - l) // 2) # Prevents integer overflow in Java/C++
        mid = (l + r) // 2
        
        if nums[mid] > target:
            r = mid - 1
        elif nums[mid] < target:
            l = mid + 1
        else:
            return mid
            
    return -1
```

### 8. Dry Run
`nums = [-1,0,3,5,9,12], target = 9`
- l=0, r=5, mid=2 (val 3). 3 < 9 -> l = 3.
- l=3, r=5, mid=4 (val 9). 9 == 9 -> return 4.

### 9. Edge Cases Handled
If target > largest, `l` eventually surpasses `r` and loop terminates.

### 10. Follow-ups
- "What if the array has duplicates and you want the *first* occurrence?" -> Instead of returning immediately, do `res = mid; r = mid - 1` to keep searching left.

### 11. Related Problems
Search Insert Position, Find First and Last Position of Element in Sorted Array.

---

## 2. Search in Rotated Sorted Array

### 1. Restate the Problem
An array sorted in ascending order is rotated at some pivot unknown to you beforehand. Given the array and a target, find the index of target.

### 2. Clarify Edge Cases
- Not rotated? (Standard binary search).
- Target not found? Return -1.

### 3. Brute Force Approach
Linear scan. Time: $O(N)$.

### 4. Key Insight
Even if rotated, one half of the array (split by `mid`) MUST be strictly sorted. We can determine which half is sorted, check if our target falls within that sorted range, and decide which way to search.

### 5. Optimized Approach
Standard binary search loop. Find `mid`. Check if left sorted: `nums[l] <= nums[mid]`. If so, check if target is in `[l, mid]`. If it is, `r = mid - 1`, else `l = mid + 1`. If right is sorted (`nums[mid] <= nums[r]`), check if target is in `[mid, r]`. If so, `l = mid + 1`, else `r = mid - 1`.

### 6. Justification
Time: $O(\log N)$. Space: $O(1)$.

### 7. Code (Python)
```python
def search(nums: List[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    
    while l <= r:
        mid = (l + r) // 2
        
        if nums[mid] == target:
            return mid
            
        # Left sorted portion
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        # Right sorted portion
        else:
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
                
    return -1
```

### 8. Dry Run
`nums = [4,5,6,7,0,1,2], target = 0`
- l=0, r=6, mid=3 (val 7). Left is sorted [4..7]. target 0 is NOT in this range. So l = 4.
- l=4, r=6, mid=5 (val 1). Left is sorted [0..1]. target 0 IS in this range (0 <= 0 < 1). So r = 4.
- l=4, r=4, mid=4 (val 0). 0 == 0. Return 4.

### 9. Edge Cases Handled
Array of size 1 handled by `<=`.

### 10. Follow-ups
- "What if there are duplicates?" -> `nums[l] == nums[mid]` doesn't guarantee left is sorted. Must do `l += 1` to slowly skip duplicates ($O(N)$ worst case).

### 11. Related Problems
Find Minimum in Rotated Sorted Array.
""")
print("DSA Qs 5 complete")
