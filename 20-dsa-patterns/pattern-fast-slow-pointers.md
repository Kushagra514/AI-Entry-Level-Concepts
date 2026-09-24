# Pattern: Fast and Slow Pointers

## 1. Definition
Fast and Slow Pointers (also known as Floyd's Tortoise and Hare) is an algorithm that uses two pointers moving through a sequence at different speeds to detect cycles or find midpoints.

## 2. Intuition
Imagine two runners on a track. One runs at 1x speed (slow), the other at 2x speed (fast). If the track is a straight line, the fast runner finishes and the race ends. But if the track is a circle, the fast runner will eventually lap the slow runner and they will meet. 

## 3. Why it exists
Detecting cycles in a Linked List usually requires a Hash Set to track visited nodes, taking $O(N)$ space. Floyd's algorithm solves this in $O(1)$ space.

## 4. Mechanics
- **Cycle Detection:** Initialize `slow = head` and `fast = head`. Loop: `slow = slow.next`, `fast = fast.next.next`. If `slow == fast`, there is a cycle.
- **Find Midpoint:** When `fast` reaches the end of the list, `slow` will be exactly at the midpoint (because it travels half as fast).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - In the worst case, the fast pointer traverses the list a constant number of times.
- **Space Complexity:** $O(1)$ - Only two pointers are used.

## 6. Tiny worked example
List: 1 -> 2 -> 3 -> 4 -> 5 -> (points back to 3)
- Step 0: S=1, F=1
- Step 1: S=2, F=3
- Step 2: S=3, F=5
- Step 3: S=4, F=4 (Collision! Cycle detected).

## 7. Code (Python, with type hints)
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head: ListNode) -> bool:
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
            
    return False
```

## 8. Common mistakes
- **Null Reference Errors:** Forgetting to check `while fast and fast.next:`. If you only check `while fast:`, calling `fast.next.next` will throw an error when `fast.next` is None.
- Over-complicating cycle math. 

## 9. 30-second interview answer
"The Fast and Slow pointer technique uses two pointers moving at different speeds to process sequences. It is primarily used on Linked Lists to detect cycles using $O(1)$ space via Floyd's algorithm, or to find the midpoint of a list in a single pass."

## 10. 2-minute interview answer
"Floyd's Tortoise and Hare is the definitive pattern for Linked List topology problems. By advancing one pointer by one step and another by two steps, we gain profound insights in $O(N)$ time and $O(1)$ space. If the sequence has an end, the fast pointer hits a null reference, and the slow pointer perfectly rests at the midpoint—this is essential for algorithms like Merge Sort on linked lists. If the sequence has a cycle, the relative distance between the two pointers decreases by one step each iteration, guaranteeing they will collide inside the loop. A beautiful extension of this is finding the exact start of the cycle: after a collision, if you reset one pointer to the head and move both at 1x speed, they will magically collide exactly at the cycle entrance."

## 11. Follow-ups
- "How do you mathematically prove they will meet exactly at the cycle entrance?" (Let distance to cycle be $x$. Distance inside cycle to meeting point be $y$. Fast traveled $2(x+y)$, Slow traveled $x+y$. The remaining distance is exactly $x$).

## 12. Deeper questions
- "Can you use this pattern to find duplicate numbers in an array?" (Yes! If array values are in the range `[1, n]`, you can treat the array as a Linked List where `arr[i]` points to `arr[arr[i]]`. Finding the cycle entrance finds the duplicate in $O(1)$ space).

## 13. Related concepts
- **Two Pointers**: The parent category of this pattern.
- **Linked Lists**: The primary data structure.

## 14. When it breaks / Edge cases
- Fails or errors out on empty lists or single-node lists without cycles if null checks are missing.

## 15. Comparison with alternative approaches
- **vs Hash Set:** Hash Set takes $O(N)$ space but can detect cycles immediately. Fast/Slow takes $O(1)$ space but takes slightly longer as it must traverse the loop until collision.

---
*Where this shows up in ML:* 
While not directly used in ML math, understanding topological loops is relevant for verifying Directed Acyclic Graphs (DAGs) in computation graphs.
