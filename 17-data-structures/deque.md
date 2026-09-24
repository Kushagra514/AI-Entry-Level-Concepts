# Deque (Double-Ended Queue)

## 1. Definition
A Deque (pronounced "deck") is a linear data structure that allows insertion and deletion of elements from both ends (front and back) in $O(1)$ time.

## 2. Intuition
Think of a queue of people at a theme park, but with a VIP rule. Normal people enter the back and leave from the front. But VIPs can cut directly to the front, and people who get tired of waiting can leave from the back. It operates as both a Stack and a Queue simultaneously.

## 3. Why it exists
An Array/List takes $O(N)$ time to insert/delete at the front because all elements must shift. A Deque solves this, providing $O(1)$ operations at both ends, making it the perfect underlying structure for Sliding Window Maximums and BFS algorithms.

## 4. Mechanics
- Typically implemented using a Doubly Linked List or a Circular Array.
- **Operations:** `append()` (add to right), `appendleft()` (add to left), `pop()` (remove from right), `popleft()` (remove from left).
- Unlike Python lists, Deques do not require massive memory reallocations for shifting.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(1)$ for insert/delete at both ends. $O(N)$ for random access/indexing in the middle.
- **Space Complexity:** $O(N)$.

## 6. Tiny worked example
```python
from collections import deque
dq = deque([1, 2])
dq.append(3)      # [1, 2, 3] (Queue behavior)
dq.appendleft(0)  # [0, 1, 2, 3]
dq.pop()          # 3 (Stack behavior) -> [0, 1, 2]
dq.popleft()      # 0 (Queue behavior) -> [1, 2]
```

## 7. Code (Python, with type hints)
```python
from collections import deque
from typing import List

# Classic Deque problem: Sliding Window Maximum
def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    dq = deque()  # Stores INDICES of array elements
    res = []
    
    for i in range(len(nums)):
        # 1. Remove indices that are out of the current window
        if dq and dq[0] < i - k + 1:
            dq.popleft()
            
        # 2. Remove smaller elements from back (they can never be the max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
            
        # 3. Add current element
        dq.append(i)
        
        # 4. Record max (element at front of deque)
        if i >= k - 1:
            res.append(nums[dq[0]])
            
    return res
```

## 8. Common mistakes
- Using a standard Python `list` as a queue (`list.pop(0)`). This is an immediate red flag in interviews because it runs in $O(N)$ time, turning an $O(N)$ BFS into an $O(N^2)$ disaster.
- Using a Deque for heavy random access (`dq[500]`), which takes $O(N)$ time in linked-list implementations.

## 9. 30-second interview answer
"A Deque is a Double-Ended Queue that supports $O(1)$ insertions and deletions from both the front and the back. In Python, it is implemented via `collections.deque` and is mandatory for BFS graph traversals and optimal Monotonic Queue problems like Sliding Window Maximum."

## 10. 2-minute interview answer
"A Deque bridges the gap between Stacks and Queues. By implementing it internally as a doubly-linked list or circular buffer, it allows strictly $O(1)$ time complexity for adding or removing elements at either boundary. In Python, candidates often make the fatal mistake of using a standard array with `.pop(0)` for BFS, destroying their time complexity via $O(N)$ memory shifts. The Deque's most powerful algorithmic application is the Monotonic Queue pattern, used in problems like 'Sliding Window Maximum'. By popping elements from the right that violate the monotonic property, and popping expired indices from the left, a Deque calculates the maximum of a moving window in perfectly linear $O(N)$ time."

## 11. Follow-ups
- "Are Deques thread-safe in Python?" (Yes, the `.append()` and `.pop()` operations on Python's `collections.deque` are thread-safe and atomic).

## 12. Deeper questions
- "How would you implement a Deque using an Array instead of a Linked List?" (Use a Circular Buffer with 'head' and 'tail' pointers that wrap around the array length using modulo arithmetic).

## 13. Related concepts
- **Queues**: For BFS.
- **Sliding Window**: For Monotonic Deques.

## 14. When it breaks / Edge cases
- Fails if you need fast $O(1)$ random access in the middle of the collection (use a standard Array instead).

## 15. Comparison with alternative approaches
- **vs List (Array):** Lists are $O(1)$ for right-side operations but $O(N)$ for left-side operations. Deques are $O(1)$ for both.

---
*Where this shows up in ML:* 
Replay buffers in Reinforcement Learning (DQN) are often implemented using fixed-size Deques. When the buffer is full, appending a new experience automatically drops the oldest one from the front in $O(1)$ time.
