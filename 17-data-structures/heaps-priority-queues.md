# Heaps & Priority Queues

## 1. Definition
A Priority Queue is an abstract data type like a regular queue, but every element has a "priority". Elements with higher priority are dequeued before elements with lower priority. A Heap is the optimal tree-based data structure used to implement a Priority Queue.

## 2. Intuition
Think of an ER waiting room. Unlike a grocery line (FIFO), patients are treated based on the severity of their condition. A gunshot wound (high priority) is treated before a sprained ankle (low priority), regardless of who arrived first. A Heap is the system that instantly tells the doctor who the highest-priority patient is at any moment.

## 3. Why it exists
If we use a sorted array for a priority queue, extracting the max is $O(1)$, but inserting a new element is $O(N)$. If we use an unsorted array, insert is $O(1)$ but finding the max is $O(N)$. A Heap offers a mathematical compromise: $O(\log N)$ for both insertion and extraction, keeping the absolute highest (or lowest) element at the top at all times.

## 4. Mechanics
- **Structure:** A Heap is a *Complete Binary Tree* (all levels are fully filled except possibly the last level, filled left to right). Because it's complete, it's efficiently stored in a simple Array, not with pointers.
- **Heap Property:** In a Min-Heap, every parent is $\le$ its children (root is the minimum). In a Max-Heap, every parent is $\ge$ its children.
- **Insert:** Add to the end of the array, then "bubble up" (swap with parent) until the heap property is restored.
- **Pop:** Remove the root, replace it with the last element in the array, then "bubble down" (swap with smallest/largest child).

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Peek (find max/min): $O(1)$.
  - Push/Pop: $O(\log N)$.
  - Heapify (convert array to heap): $O(N)$.
- **Space Complexity:** $O(N)$ to store the array.

## 6. Tiny worked example
Array representation: `[10, 20, 30]`. `10` is root. Children of index `i` are at `2i+1` and `2i+2`.
Insert `5` (Min-Heap):
- Add to end: `[10, 20, 30, 5]`.
- Bubble up: `5` is at index 3. Parent is index 1 (`20`). Swap.
- `[10, 5, 30, 20]`. Parent of index 1 is index 0 (`10`). Swap.
- Final: `[5, 10, 30, 20]`. Root is now 5.

## 7. Code (Python, with type hints)
```python
import heapq
from typing import List

# Python's heapq only implements Min-Heaps
def top_k_elements(nums: List[int], k: int) -> List[int]:
    min_heap = []
    
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            # Pop the smallest element, keeping the K largest in the heap
            heapq.heappop(min_heap)
            
    return min_heap
```

## 8. Common mistakes
- Forgetting that Python's `heapq` is a Min-Heap. To simulate a Max-Heap with integers, you must push `-val` and invert it when popping.
- Sorting the entire array ($O(N \log N)$) when asked for the "Top K" elements, instead of using a Heap of size K ($O(N \log K)$).

## 9. 30-second interview answer
"A Heap is a complete binary tree that satisfies the heap property, typically used to implement a Priority Queue. It provides $O(1)$ access to the minimum or maximum element, and $O(\log N)$ time for insertions and deletions. It is the optimal data structure for 'Top-K' or scheduling problems."

## 10. 2-minute interview answer
"A Heap perfectly solves the Priority Queue problem by bridging the gap between $O(1)$ and $O(N)$ operations. Because a Heap is a complete binary tree, it doesn't need pointer-based nodes; it maps perfectly into a contiguous array, making it extremely cache-friendly. The 'Heap Property' guarantees the min or max is always at the root index 0. When we insert or extract, we perform logarithmic 'bubble' operations to maintain this property. In algorithmic interviews, whenever a problem asks for the 'Kth largest/smallest', 'Top K frequent', or involves continuously merging the smallest elements like in Huffman Coding or Dijkstra's algorithm, a Heap is the definitive answer, reducing an $O(N \log N)$ sort to an $O(N \log K)$ stream."

## 11. Follow-ups
- "Why does `heapify` take $O(N)$ time instead of $O(N \log N)$?" (Most nodes are at the bottom of the tree and don't bubble down far; mathematically, the infinite sum bounds to $O(N)$).
- "How does Dijkstra's algorithm use a Priority Queue?" (To always explore the node with the current shortest known distance next).

## 12. Deeper questions
- "What's a Fibonacci Heap?" (A highly advanced theoretical heap that offers $O(1)$ amortized insertion and decrease-key operations, though it's too complex for most practical implementations).

## 13. Related concepts
- **Dijkstra's & Prim's Algorithms**: Rely heavily on priority queues.
- **Heap Sort**: An in-place $O(N \log N)$ sort using a max-heap.

## 14. When it breaks / Edge cases
- If you need to search for an arbitrary element in a heap, it takes $O(N)$ time (it's not a BST).

## 15. Comparison with alternative approaches
- **vs BST:** BST gives $O(\log N)$ for searching *any* value. Heap only gives $O(1)$ for the max/min, but has less memory overhead (no pointers) and faster average insertions.

---
*Where this shows up in ML:* 
In LLM generation, during Beam Search decoding, we use a Priority Queue (Heap) to keep track of the top-K most probable sequence hypotheses at each token generation step, discarding lower probability paths.
