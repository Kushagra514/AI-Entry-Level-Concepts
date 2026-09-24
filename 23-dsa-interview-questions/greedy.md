# Greedy Interview Questions

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
