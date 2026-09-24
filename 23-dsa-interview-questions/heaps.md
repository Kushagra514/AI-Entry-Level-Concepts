# Heaps Interview Questions

---

## 1. Kth Largest Element in an Array

### 1. Restate the Problem
Given an integer array `nums` and an integer `k`, return the $k$-th largest element in the array.

### 2. Clarify Edge Cases
- $k$ is guaranteed to be $1 \le k \le \text{len(nums)}$.
- Array can have duplicates.

### 3. Brute Force Approach
Sort the array descending and return `nums[k-1]`. Time: $O(N \log N)$. Space: $O(1)$ (in-place sort).

### 4. Key Insight
We only care about the top $k$ elements, not sorting the entire array. A Min-Heap of size $k$ perfectly maintains the $k$ largest elements seen so far. The smallest of those $k$ (the root of the Min-Heap) is exactly the $k$-th largest overall.

### 5. Optimized Approach
Initialize an empty min-heap. Iterate through `nums`. Push each number onto the heap. If the heap size exceeds $k$, pop the smallest element. After processing all elements, the top of the heap is the answer.

### 6. Justification
Time: $O(N \log k)$ because we insert $N$ elements into a heap of size $k$. Space: $O(k)$ for the heap.

### 7. Code (Python)
```python
import heapq
from typing import List

def findKthLargest(nums: List[int], k: int) -> int:
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
            
    return min_heap[0]
```

### 8. Dry Run
`nums = [3,2,1,5,6,4], k = 2`
- 3: heap=[3]
- 2: heap=[2,3]
- 1: heap=[1,2,3] -> pop 1 -> heap=[2,3]
- 5: heap=[2,3,5] -> pop 2 -> heap=[3,5]
- 6: heap=[3,5,6] -> pop 3 -> heap=[5,6]
- 4: heap=[4,5,6] -> pop 4 -> heap=[5,6]
- Returns 5.

### 9. Edge Cases Handled
Duplicates are handled correctly (heap stores duplicates).

### 10. Follow-ups
- "Can you do it in $O(N)$ average time?" -> Yes, use Quickselect (Hoare's selection algorithm).

### 11. Related Problems
Top K Frequent Elements, Find Median from Data Stream.

---

## 2. Merge K Sorted Lists

### 1. Restate the Problem
Given an array of `k` linked-lists, each sorted in ascending order, merge all the linked-lists into one sorted linked-list and return it.

### 2. Clarify Edge Cases
- Array is empty? Return None.
- Some lists inside the array are empty? Ignore them.

### 3. Brute Force Approach
Extract all values from all linked lists into one massive array. Sort it. Rebuild a new linked list. Time: $O(N \log N)$ where $N$ is total nodes.

### 4. Key Insight
Since individual lists are sorted, the smallest overall element MUST be one of the $k$ heads. We can use a Min-Heap to rapidly find the minimum among the current $k$ heads.

### 5. Optimized Approach
Create a dummy head. Push the head node of each non-empty list into a min-heap. Pop the smallest node, attach it to our result list, and if that node has a `next` node, push it into the heap. Repeat until heap is empty.

*(Note: In Python, `heapq` compares tuples `(val, node)`. Since `ListNode` doesn't implement `<` by default, use `(val, index, node)` where `index` is a tiebreaker).*

### 6. Justification
Time: $O(N \log k)$ where $N$ is total nodes and $k$ is number of lists. Space: $O(k)$ for the heap.

### 7. Code (Python)
```python
import heapq

# Assuming ListNode is defined
def mergeKLists(lists: List[ListNode]) -> ListNode:
    min_heap = []
    
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(min_heap, (lst.val, i, lst))
            
    dummy = ListNode(0)
    curr = dummy
    
    while min_heap:
        val, i, node = heapq.heappop(min_heap)
        curr.next = node
        curr = curr.next
        
        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))
            
    return dummy.next
```

### 8. Dry Run
`L1=[1,4,5], L2=[1,3,4], L3=[2,6]`
- Init heap: `[(1,0,Node1), (1,1,Node1), (2,2,Node2)]`
- Pop (1,0). Append Node1(val 1). Push its next: `(4,0,Node4)`.
- Pop (1,1). Append Node1(val 1). Push its next: `(3,1,Node3)`.
- Pop (2,2). Append Node2(val 2). Push its next: `(6,2,Node6)`.
- Result builds: `1 -> 1 -> 2 ...`

### 9. Edge Cases Handled
Empty input array handled (loop skipped). Empty sublists handled (`if lst:` check).

### 10. Follow-ups
- "Can you do this using Divide and Conquer instead of a Heap?" -> Yes, merge pairs of lists iteratively until 1 remains. Same $O(N \log k)$ time, but $O(1)$ space.

### 11. Related Problems
Merge Two Sorted Lists, Kth Smallest Element in a Sorted Matrix.
