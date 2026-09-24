# Sorting Interview Questions

---

## 1. Merge Intervals

### 1. Restate the Problem
Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

### 2. Clarify Edge Cases
- Empty intervals array? Return `[]`.
- `[1, 4]` and `[4, 5]` overlap? Yes, returns `[1, 5]`.

### 3. Brute Force Approach
Compare every interval with every other interval. If they overlap, merge them. Repeat until no more merges can happen. Time: $O(N^2)$.

### 4. Key Insight
If we sort the intervals by their start time, we guarantee that interval `i` starts before or at the same time as interval `i+1`. This means we only ever need to compare interval `i+1` against the *last* interval we added to our output list.

### 5. Optimized Approach
1. Sort `intervals` by `start_i`.
2. Initialize `merged` list with the first interval.
3. Iterate through `intervals`. For each interval, compare its start time with the end time of the last interval in `merged`.
4. If it overlaps (`curr_start <= last_end`), update `last_end = max(last_end, curr_end)`.
5. If it doesn't overlap, append the current interval to `merged`.

### 6. Justification
Time: $O(N \log N)$ due to sorting. The linear scan takes $O(N)$. Space: $O(N)$ (or $O(\log N)$ depending on sorting algorithm) for the output array.

### 7. Code (Python)
```python
from typing import List

def merge(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for interval in intervals[1:]:
        # If the current interval overlaps with the last merged one, merge them
        if interval[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], interval[1])
        else:
            merged.append(interval)
            
    return merged
```

### 8. Dry Run
`intervals = [[1,3],[2,6],[8,10],[15,18]]`
- Sorted: same.
- merged = [[1,3]]
- [2,6]: 2 <= 3. Overlap. merged[-1][1] = max(3, 6) = 6. merged = [[1,6]]
- [8,10]: 8 > 6. No overlap. append. merged = [[1,6], [8,10]]
- [15,18]: 15 > 10. No overlap. append. merged = [[1,6], [8,10], [15,18]]

### 9. Edge Cases Handled
Single interval is handled gracefully. `[[1,4],[2,3]]` properly merges into `[1,4]` due to `max()`.

### 10. Follow-ups
- "What if the intervals are already sorted?" -> The time complexity drops to $O(N)$.

### 11. Related Problems
Insert Interval, Non-overlapping Intervals, Meeting Rooms.

---

## 2. Sort Colors (Dutch National Flag Problem)

### 1. Restate the Problem
Given an array `nums` with $n$ objects colored red, white, or blue (represented as 0, 1, and 2), sort them in-place so that objects of the same color are adjacent, with the colors in the order 0, 1, and 2. Do not use the library's sort function.

### 2. Clarify Edge Cases
- All one color? Valid.
- In-place requirement implies $O(1)$ space.

### 3. Brute Force Approach
Counting sort. Count the 0s, 1s, and 2s in pass 1. Overwrite the array in pass 2. Time: $O(N)$ (two passes). Space: $O(1)$.

### 4. Key Insight
We can do this in a single pass using three pointers (Dutch National Flag algorithm). The array is divided into four sections: 0s (left), 1s (middle), unknown (between mid and right), and 2s (right).

### 5. Optimized Approach
`low = 0`, `mid = 0`, `high = len(nums) - 1`.
While `mid <= high`:
- If `nums[mid] == 0`: swap `nums[low]` and `nums[mid]`, increment both.
- If `nums[mid] == 1`: just increment `mid`.
- If `nums[mid] == 2`: swap `nums[mid]` and `nums[high]`, decrement `high` (do not increment `mid` because the swapped number needs to be evaluated).

### 6. Justification
Time: $O(N)$ in one pass. Space: $O(1)$ in-place.

### 7. Code (Python)
```python
def sortColors(nums: List[int]) -> None:
    low, mid, high = 0, 0, len(nums) - 1
    
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

### 8. Dry Run
`nums = [2,0,2,1,1,0]`
- low=0, mid=0, high=5. `nums[0]=2`. Swap with `high`. `[0,0,2,1,1,2]`. high=4.
- mid=0. `nums[0]=0`. Swap low/mid. `[0,0,2,1,1,2]`. low=1, mid=1.
- mid=1. `nums[1]=0`. Swap low/mid. `[0,0,2,1,1,2]`. low=2, mid=2.
- mid=2. `nums[2]=2`. Swap with `high`. `[0,0,1,1,2,2]`. high=3.
- mid=2. `nums[2]=1`. mid=3.
- mid=3. `nums[3]=1`. mid=4.
- loop ends (mid > high). Sorted!

### 9. Edge Cases Handled
If array contains only 0s and 2s, the `mid` pointer naturally skips 1s logic and functions perfectly.

### 10. Follow-ups
- N/A (this is the one-pass optimal).

### 11. Related Problems
Partition Labels, Wiggle Sort.
