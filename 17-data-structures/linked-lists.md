# Linked Lists

## 1. Definition
A Linked List is a linear data structure where elements (nodes) are not stored contiguously in memory. Instead, each node contains data and a pointer/reference to the next node in the sequence.

## 2. Intuition
Imagine a scavenger hunt. You are given a clue that leads you to location A. At location A, you find a prize (data) and the next clue (pointer) leading you to location B. You cannot jump directly to location C; you must follow the clues in order.

## 3. Why it exists
Arrays require a contiguous block of memory and resizing them is expensive $O(N)$. Linked Lists solve this by allowing data to be scattered across memory. You can easily insert or delete nodes without shifting other elements, provided you know where to make the change.

## 4. Mechanics
- **Singly Linked List:** Node contains `data` and `next` pointer.
- **Doubly Linked List:** Node contains `data`, `next`, and `prev` pointers, allowing backward traversal.
- The list is tracked by holding a reference to the `head` node. The last node points to `Null` (or `None`).
- **Insertion/Deletion:** To insert node B between A and C, update A's `next` to B, and B's `next` to C.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Access/Search: $O(N)$ - Must traverse from the head.
  - Insertion/Deletion at Head: $O(1)$.
  - Insertion/Deletion at given node: $O(1)$ (assuming you already have the pointer to that node).
- **Space Complexity:** $O(N)$ - Plus the overhead of storing the pointer(s) in each node.

## 6. Tiny worked example
List: `1 -> 2 -> 3`
Insert `4` after `1`:
- Create node `4`.
- `4.next = 1.next` (which is `2`).
- `1.next = 4`.
Result: `1 -> 4 -> 2 -> 3`.

## 7. Code (Python, with type hints)
```python
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

def delete_node(head: Optional[ListNode], target: int) -> Optional[ListNode]:
    # Dummy node elegant pattern to handle head deletions easily
    dummy = ListNode(0)
    dummy.next = head
    curr = dummy
    
    while curr.next:
        if curr.next.val == target:
            curr.next = curr.next.next # Skip the target node
            break
        curr = curr.next
        
    return dummy.next
```

## 8. Common mistakes
- Losing the reference to the `head` of the list while iterating.
- `NullReferenceException` (or `NoneType` error) by trying to access `node.next.val` without checking if `node.next` is `None`.
- Failing to handle edge cases: empty list, one node list, or deleting the head node (using a Dummy Node solves this).

## 9. 30-second interview answer
"A Linked List is a sequence of nodes where each node points to the next. Unlike arrays, it doesn't require contiguous memory, allowing for $O(1)$ insertions and deletions if you have the reference. However, it lacks random access, meaning finding an element takes $O(N)$ time."

## 10. 2-minute interview answer
"Linked lists are a pointer-based data structure that trades $O(1)$ random access for $O(1)$ structural modification. Because nodes are scattered in the heap and linked via pointers, we never have to resize or shift elements like we do with dynamic arrays. This makes them ideal for building Stacks and Queues. However, this comes with two massive drawbacks: first, searching requires $O(N)$ sequential traversal. Second, they have terrible CPU cache locality. Because arrays are contiguous, the CPU can pre-fetch them into fast cache. Linked list nodes are randomly scattered, causing cache misses which makes them practically slower than arrays for most iterations, despite theoretical Big-O equivalence."

## 11. Follow-ups
- "How do you detect a cycle in a linked list?" (Floyd's Fast and Slow pointer technique).
- "Why are Dummy Nodes (Sentinel Nodes) useful?" (They eliminate the need for edge-case `if` statements when inserting/deleting at the head).

## 12. Deeper questions
- "How do you reverse a linked list?" (Iteratively keeping track of `prev`, `curr`, and `next` pointers, or recursively).

## 13. Related concepts
- **Trees / Graphs**: Simply linked lists where nodes have multiple pointers.
- **LRU Cache**: Built using a Hash Map + Doubly Linked List.

## 14. When it breaks / Edge cases
- Modifying a list while iterating over it can easily sever the rest of the list.
- Deep recursive traversal of a linked list will cause a Stack Overflow.

## 15. Comparison with alternative approaches
- **vs Arrays:** Arrays have $O(1)$ access and great cache locality, but $O(N)$ insertions. Linked lists have $O(N)$ access, poor cache locality, but $O(1)$ insertions.

---
*Where this shows up in ML:* 
While native linked lists are rare in highly optimized ML code (because GPUs require dense contiguous arrays/tensors for fast math), the *concept* of linked computation graphs is foundational to PyTorch's Autograd system. Each tensor operation generates a node, and nodes hold pointers to their creator functions, forming a directed acyclic graph (essentially a multi-linked list) used to trace backward for gradients.
