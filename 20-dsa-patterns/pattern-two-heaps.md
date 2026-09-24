# Pattern: Two Heaps

## 1. Definition
The Two Heaps pattern uses a Max-Heap and a Min-Heap together to continuously track the median (or another percentile) of a stream of numbers.

## 2. Intuition
Imagine sorting a stream of numbers and drawing a line exactly down the middle. Everything on the left is the lower half, and you only care about the largest number there (Max-Heap). Everything on the right is the upper half, and you only care about the smallest number there (Min-Heap). The median is right at the boundary between the two heaps.

## 3. Why it exists
Sorting an array every time a new number arrives to find the median takes $O(N \log N)$ per insert. The Two Heaps pattern reduces the insertion time to $O(\log N)$ and the median retrieval time to $O(1)$.

## 4. Mechanics
- **Max-Heap (Lower Half):** Stores the smaller half of the numbers. The root is the largest of the small numbers.
- **Min-Heap (Upper Half):** Stores the larger half of the numbers. The root is the smallest of the large numbers.
- **Insertion:** Add to Max-Heap. Pop from Max-Heap and push to Min-Heap (to guarantee elements in Min-Heap are larger). If Min-Heap is larger than Max-Heap, pop from Min and push to Max to balance sizes.
- **Balance:** Max-Heap size must equal Min-Heap size (even count), or be exactly 1 larger (odd count).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\log N)$ for insertion, $O(1)$ to find the median.
- **Space Complexity:** $O(N)$ to store all elements in the heaps.

## 6. Tiny worked example
Insert `[3, 1, 5]`.
- Add 3: Max=`[3]`, Min=`[]`. Median = 3.
- Add 1: Max=`[3, 1]`. Pop 3 to Min. Max=`[1]`, Min=`[3]`. Median = (1+3)/2 = 2.
- Add 5: Max=`[1, 5]`. Pop 5 to Min. Max=`[1]`, Min=`[3, 5]`. Unbalanced! Pop 3 to Max. Max=`[3, 1]`, Min=`[5]`. Median = 3.

## 7. Code (Python, with type hints)
```python
import heapq

class MedianFinder:
    def __init__(self):
        # Python heapq is min-heap. Multiply by -1 for max-heap.
        self.small = [] # Max-Heap (lower half)
        self.large = [] # Min-Heap (upper half)

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        
        # Ensure max of small is <= min of large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
            
        # Balance sizes (small can be 1 larger, but not vice versa)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

## 8. Common mistakes
- Forgetting to invert numbers when using Python's `heapq` for the Max-Heap.
- Failing to balance the heaps correctly (e.g., pushing to Max, but the number was actually larger than the Min-Heap's root, violating the boundary).

## 9. 30-second interview answer
"The Two Heaps pattern elegantly maintains the median of a data stream in $O(\log N)$ time. We use a Max-Heap for the smaller half of numbers and a Min-Heap for the larger half. By keeping their sizes balanced, the median is always instantly accessible at the roots in $O(1)$ time."

## 10. 2-minute interview answer
"To find a dynamic median efficiently, we must split the sorted representation of the data perfectly in half. We achieve this using the Two Heaps pattern. The lower half of the data is stored in a Max-Heap, meaning the largest of the small numbers is always at the top. The upper half is stored in a Min-Heap. Upon inserting a new number, we first push it to the Max-Heap, then immediately pop the Max-Heap's root and push it to the Min-Heap. This guarantees that all numbers in the Min-Heap are strictly greater than those in the Max-Heap. Finally, we balance the heap sizes so the Max-Heap is equal to or exactly one element larger than the Min-Heap. Finding the median is an $O(1)$ peek at the roots, completely bypassing the $O(N \log N)$ cost of sorting a stream."

## 11. Follow-ups
- "What if you needed the 90th percentile instead of the median?" (Adjust the size balancing logic so the Max-Heap holds 90% of the elements and the Min-Heap holds 10%).

## 12. Deeper questions
- "How do you solve Sliding Window Median?" (It's Two Heaps, plus you need to remove elements that fall out of the window. Since heap removal is $O(N)$, you use 'lazy deletion' by keeping a hash map of expired elements and skipping them when they surface at the root).

## 13. Related concepts
- **Heaps / Priority Queues**: The underlying structures.
- **Sliding Window**: Often combined.

## 14. When it breaks / Edge cases
- Stream problems require memory. If the stream is infinite, $O(N)$ space will eventually cause OOM.

## 15. Comparison with alternative approaches
- **vs Binary Search Tree:** A balanced BST can also find the median dynamically, but Heaps are cache-friendly arrays and significantly easier to implement error-free in an interview.

---
*Where this shows up in ML:* 
Percentile tracking during streaming distributed training or analyzing latency percentiles (P50, P99) in MLOps monitoring.
