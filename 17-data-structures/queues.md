# Queues

## 1. Definition
A Queue is a linear data structure that follows the First-In-First-Out (FIFO) principle. The first element added is the first element removed.

## 2. Intuition
Think of a checkout line at a grocery store. The first person to get in line is the first person to be served. If you arrive late, you must wait at the back of the line until everyone in front of you is finished.

## 3. Why it exists
Queues exist to manage processes in a fair, chronological order. They act as buffers between producers (who generate data) and consumers (who process data) ensuring that tasks are handled exactly in the order they arrived.

## 4. Mechanics
- **Enqueue (Push):** Add an element to the rear (tail).
- **Dequeue (Pop):** Remove and return the element at the front (head).
- **Peek:** View the front element.
- While a stack can use a simple array, a queue implemented with a standard array requires $O(N)$ time to dequeue (shifting all elements left). Therefore, they are efficiently implemented using a Linked List or a Ring Buffer (Circular Array).

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Enqueue, Dequeue, Peek: $O(1)$.
- **Space Complexity:** $O(N)$ to store $N$ elements.

## 6. Tiny worked example
Queue: `[]`
- `Enqueue(A)` -> `[A]`
- `Enqueue(B)` -> `[A, B]`
- `Dequeue()` -> Returns A. Queue: `[B]`
- `Enqueue(C)` -> `[B, C]`

## 7. Code (Python, with type hints)
```python
from collections import deque

# Python's deque (double-ended queue) is implemented as a doubly linked list
class Queue:
    def __init__(self):
        self.q = deque()
        
    def enqueue(self, val: int) -> None:
        self.q.append(val)    # O(1)
        
    def dequeue(self) -> int:
        if not self.is_empty():
            return self.q.popleft() # O(1)
        raise IndexError("dequeue from empty queue")
        
    def is_empty(self) -> bool:
        return len(self.q) == 0
```

## 8. Common mistakes
- Using a standard Python `list` as a queue and calling `queue.pop(0)`. This is an $O(N)$ operation because all other elements must shift left. Always use `collections.deque`.
- Confusing Enqueue (append) and Dequeue (popleft) with Stack operations (pop from right).

## 9. 30-second interview answer
"A queue is a First-In-First-Out (FIFO) data structure. Elements are added to the back and removed from the front in $O(1)$ time. In Python, you should always use `collections.deque` for queues, as standard lists take $O(N)$ time to pop from the front. They are the core data structure for Breadth-First Search (BFS)."

## 10. 2-minute interview answer
"Queues enforce FIFO ordering, making them essential for scheduling, buffering, and level-order traversal. Because dequeuing from a standard dynamic array takes $O(N)$ time due to shifting elements, an optimal queue is backed by either a linked list (with head and tail pointers) or a circular array. In Python, `collections.deque` provides an optimized C-level doubly-linked list for $O(1)$ appends and pops from both ends. In algorithm interviews, if you need to process data level-by-level, find the shortest path in an unweighted graph, or simulate a chronological pipeline, a queue (and therefore BFS) is exactly what you need."

## 11. Follow-ups
- "What is a Deque?" (A double-ended queue, allowing $O(1)$ inserts and pops from *both* ends).
- "How do you implement a Queue using Stacks?" (Use two stacks. Enqueue pushes to S1. Dequeue pops from S2; if S2 is empty, pop everything from S1 into S2 first to reverse the order).

## 12. Deeper questions
- "What is a circular queue and why use it over a linked list?" (A circular array uses a fixed block of memory and modulo arithmetic for pointers. It is vastly more CPU-cache friendly than a linked-list queue, making it preferred in low-level systems).

## 13. Related concepts
- **Breadth-First Search (BFS)**: Strictly relies on a Queue.
- **Priority Queue**: A queue where elements are popped based on a priority score (usually backed by a Heap), not FIFO order.

## 14. When it breaks / Edge cases
- `popleft()` on an empty `deque` throws an error.

## 15. Comparison with alternative approaches
- **vs Stack:** Queues process chronologically (FIFO). Stacks process recursively/reversely (LIFO).

---
*Where this shows up in ML:* 
In multi-processing data loader pipelines (like PyTorch `DataLoader`), queues are used to pass batches of augmented images from worker CPU threads to the main GPU thread. The GPU consumes the batches in the FIFO order they were queued.
