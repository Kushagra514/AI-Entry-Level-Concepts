# Pattern: In-Place Reversal of a LinkedList

## 1. Definition
The In-Place Reversal pattern is a technique used to reverse the links of a Linked List without using extra memory, strictly operating on the existing nodes.

## 2. Intuition
Imagine holding a chain of paperclips. To reverse the direction, you don't buy a new box of paperclips. You detach the second clip, hook it to the first clip facing backwards, detach the third, hook it to the second, and so on. You only need two hands (pointers) to manage the disconnections.

## 3. Why it exists
Reversing a list by copying values to an array, reversing the array, and building a new list takes $O(N)$ extra space. In-place reversal does it in $O(1)$ space, which is an absolute requirement for most Linked List interview questions.

## 4. Mechanics
You need three pointers: `prev`, `curr`, and `next_node`.
1. Initialize `prev = None`, `curr = head`.
2. While `curr` is not None:
   - Save the next node: `next_node = curr.next`.
   - Reverse the link: `curr.next = prev`.
   - Move `prev` forward: `prev = curr`.
   - Move `curr` forward: `curr = next_node`.
3. Return `prev` (the new head).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - One pass through the list.
- **Space Complexity:** $O(1)$ - Only three pointers used.

## 6. Tiny worked example
List: `1 -> 2 -> 3 -> None`. `prev = None`, `curr = 1`.
- Step 1: `next = 2`. `1.next = None`. `prev = 1`, `curr = 2`. (List: `1->None`, `2->3`)
- Step 2: `next = 3`. `2.next = 1`. `prev = 2`, `curr = 3`. (List: `2->1->None`, `3`)
- Step 3: `next = None`. `3.next = 2`. `prev = 3`, `curr = None`.
Return `prev` (3). Final list: `3 -> 2 -> 1 -> None`.

## 7. Code (Python, with type hints)
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    
    while curr:
        next_node = curr.next  # Save next
        curr.next = prev       # Reverse
        prev = curr            # Advance prev
        curr = next_node       # Advance curr
        
    return prev
```

## 8. Common mistakes
- **Losing the rest of the list:** If you do `curr.next = prev` before saving `curr.next` to a temporary variable, the rest of the list is permanently lost to garbage collection.
- Returning `curr` instead of `prev` at the end (since `curr` is None when the loop finishes).

## 9. 30-second interview answer
"The In-Place Reversal pattern uses three pointers (prev, curr, and next) to iteratively reverse the pointers of a Linked List. By saving the next node before overwriting the current node's pointer, we traverse and reverse the list in $O(N)$ time and strictly $O(1)$ space."

## 10. 2-minute interview answer
"Reversing a Linked List in-place is the foundational manipulation technique for node-based structures. The algorithm operates in $O(N)$ time and $O(1)$ space using a sliding window of three pointers. At every step, we cache the 'next' node to prevent losing the chain, repoint the 'current' node backwards to 'prev', and then slide both 'prev' and 'current' forward. This pattern is rarely asked in isolation; it is usually a subroutine. For example, to check if a Linked List is a palindrome, we use Fast/Slow pointers to find the middle, use In-Place Reversal to flip the second half, and then compare the two halves. It's also the core logic for reversing sub-lists, like 'Reverse Nodes in k-Group'."

## 11. Follow-ups
- "How do you reverse only a sub-list (e.g., from position M to N)?" (Traverse to M-1, save it as `before_M`, run the standard reversal loop $N-M$ times, then reconnect `before_M` to the new head, and the original M node to the rest of the list).

## 12. Deeper questions
- "Can you reverse a list recursively?" (Yes. `head.next.next = head; head.next = None`. It takes $O(N)$ space on the call stack, so iterative is strictly better for memory).

## 13. Related concepts
- **Fast & Slow Pointers**: Often combined with reversal (e.g., Palindrome Linked List).

## 14. When it breaks / Edge cases
- Null heads (`head is None`) or single-node lists. The standard logic handles these flawlessly without extra `if` statements.

## 15. Comparison with alternative approaches
- **vs Array copy:** Creating an array takes $O(N)$ memory, which fails the strict $O(1)$ requirement of these problems.

---
*Where this shows up in ML:* 
Not applicable.
