# Binary Search Interview Questions

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
