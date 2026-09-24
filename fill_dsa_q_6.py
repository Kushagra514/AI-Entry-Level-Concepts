import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (DSA Qs)"')

wc("23-dsa-interview-questions/sorting.md", r"""# Sorting Interview Questions

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
""")

wc("23-dsa-interview-questions/bit-manipulation.md", r"""# Bit Manipulation Interview Questions

---

## 1. Single Number

### 1. Restate the Problem
Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one. Must be linear runtime and constant extra space.

### 2. Clarify Edge Cases
- All elements appear exactly twice except one.
- Negative numbers allowed.

### 3. Brute Force Approach
Hash Map counting frequencies. Time: $O(N)$, Space: $O(N)$. Violates space constraint.

### 4. Key Insight
XOR bitwise operator (`^`). 
- $A \oplus A = 0$ (XORing a number with itself cancels it out).
- $A \oplus 0 = A$.
- XOR is associative and commutative. Therefore, if we XOR all numbers, pairs will cancel to 0, leaving only the single number.

### 5. Optimized Approach
Initialize `res = 0`. Iterate through all numbers in the array and do `res ^= num`. Return `res`.

### 6. Justification
Time: $O(N)$ for one pass. Space: $O(1)$ for the `res` variable.

### 7. Code (Python)
```python
from typing import List

def singleNumber(nums: List[int]) -> int:
    res = 0
    for num in nums:
        res ^= num
    return res
```

### 8. Dry Run
`nums = [4, 1, 2, 1, 2]`
- res = 0
- 0 ^ 4 = 4
- 4 ^ 1 = 5 (0100 ^ 0001 = 0101)
- 5 ^ 2 = 7 (0101 ^ 0010 = 0111)
- 7 ^ 1 = 6 (0111 ^ 0001 = 0110)
- 6 ^ 2 = 4 (0110 ^ 0010 = 0100)
- Returns 4.

### 9. Edge Cases Handled
Single element array immediately returns the element.

### 10. Follow-ups
- "What if every element appears THREE times except one?" -> XOR won't work perfectly here. You need to sum the bits of all numbers at each position and take modulo 3 (Single Number II).

### 11. Related Problems
Single Number II, Single Number III, Missing Number.

---

## 2. Counting Bits

### 1. Restate the Problem
Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` ($0 \le i \le n$), `ans[i]` is the number of `1`'s in the binary representation of `i`. Runs in $O(N)$ time.

### 2. Clarify Edge Cases
- $n = 0$? Return `[0]`.

### 3. Brute Force Approach
For each number from 0 to $n$, count the set bits by doing `x & (x-1)` in a loop. Time: $O(N \log N)$ (since $\log N$ is number of bits).

### 4. Key Insight
DP + Bit Manipulation. The number of 1s in $i$ is related to $i \gg 1$ (which is $i / 2$). If $i$ is even, it has the same number of 1s as $i/2$ (just shifted left, adding a 0). If $i$ is odd, it has one more 1 than $i/2$.

### 5. Optimized Approach
Create a DP array `ans = [0] * (n + 1)`. Loop from 1 to `n`. `ans[i] = ans[i >> 1] + (i & 1)`.

### 6. Justification
Time: $O(N)$ since calculating each element takes $O(1)$. Space: $O(N)$ for the result array.

### 7. Code (Python)
```python
def countBits(n: int) -> List[int]:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### 8. Dry Run
`n = 5`
- i=1: dp[1] = dp[0] + 1 = 1. (binary 1)
- i=2: dp[2] = dp[1] + 0 = 1. (binary 10)
- i=3: dp[3] = dp[1] + 1 = 2. (binary 11)
- i=4: dp[4] = dp[2] + 0 = 1. (binary 100)
- i=5: dp[5] = dp[2] + 1 = 2. (binary 101)
- Returns `[0, 1, 1, 2, 1, 2]`.

### 9. Edge Cases Handled
0 handled automatically via initialization.

### 10. Follow-ups
- "Can you explain an alternative bitwise DP relation?" -> `ans[i] = ans[i & (i-1)] + 1`. This uses the trick that `i & (i-1)` removes the rightmost set bit.

### 11. Related Problems
Number of 1 Bits (Hamming Weight).
""")

