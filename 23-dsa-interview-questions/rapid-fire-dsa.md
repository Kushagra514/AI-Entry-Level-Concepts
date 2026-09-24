# Rapid Fire DSA Patterns

---

## 1. Find the Duplicate Number

### 1. Restate the Problem
Given an array of integers `nums` containing $n + 1$ integers where each integer is in the range $[1, n]$ inclusive. There is only one repeated number in `nums`, return this repeated number. Must solve in $O(N)$ time and $O(1)$ space without modifying the array.

### 2. Clarify Edge Cases
- Modifying array not allowed.
- Multiple duplicates of the same number are allowed (e.g., `[1, 2, 2, 2]`).

### 3. Brute Force Approach
Hash set to detect cycle. Time $O(N)$, Space $O(N)$. Fails space constraint.

### 4. Key Insight
Because the values are from 1 to $n$, we can treat the array as a linked list where `index` points to `value`. A duplicate means two indices point to the same value, creating a cycle. We can use Floyd's Tortoise and Hare algorithm.

### 5. Optimized Approach
Initialize `slow` and `fast` to `nums[0]`. Move `slow` by 1 step (`nums[slow]`) and `fast` by 2 steps (`nums[nums[fast]]`) until they meet. Then, reset `slow` to `nums[0]` and move both by 1 step. Where they meet again is the duplicate (cycle start).

### 6. Justification
Time: $O(N)$. Space: $O(1)$.

### 7. Code (Python)
```python
from typing import List

def findDuplicate(nums: List[int]) -> int:
    slow, fast = nums[0], nums[0]
    
    # Phase 1: Detect cycle
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
            
    # Phase 2: Find cycle start
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
        
    return slow
```

### 8. Dry Run
`nums = [1, 3, 4, 2, 2]`
- slow=1, fast=1
- slow=nums[1]=3, fast=nums[nums[1]]=nums[3]=2
- slow=nums[3]=2, fast=nums[nums[2]]=nums[4]=2
- Met at 2.
- slow reset to 1 (nums[0]). fast stays at 2.
- slow=nums[1]=3, fast=nums[2]=4.
- slow=nums[3]=2, fast=nums[4]=2.
- Met at 2. Return 2.

### 9. Edge Cases Handled
Cycles are guaranteed to exist per the Pigeonhole Principle.

### 10. Follow-ups
- "What if the array can't be mapped to indices (e.g., negative numbers)?" -> Can't use cycle sort. Use binary search on the range of numbers $O(N \log N)$.

### 11. Related Problems
Linked List Cycle II, Missing Number.

---

## 2. Invert a Binary Tree (Rapid Fire Edition)

### 1. Restate the Problem
Invert a binary tree.

### 5. Optimized Approach
Simple DFS. Swap left and right.

### 7. Code (Python)
```python
def invertTree(root):
    if not root: return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

---

## 3. Top K Frequent Elements (Rapid Fire Edition)

### 1. Restate the Problem
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

### 4. Key Insight
Count frequencies using a Hash Map. Then use Bucket Sort instead of a Heap for strictly $O(N)$ time.

### 7. Code (Python)
```python
from collections import Counter

def topKFrequent(nums: List[int], k: int) -> List[int]:
    count = Counter(nums)
    freq = [[] for _ in range(len(nums) + 1)]
    
    for num, c in count.items():
        freq[c].append(num)
        
    res = []
    for i in range(len(freq) - 1, 0, -1):
        for num in freq[i]:
            res.append(num)
            if len(res) == k:
                return res
```

### 6. Justification
Time: $O(N)$ (counting is $N$, bucket sorting is $N$). Space: $O(N)$ for hash map and buckets.
