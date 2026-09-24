# Linked Lists Interview Questions

---

## 1. Reverse a Linked List

### 1. Restate the Problem
Given the `head` of a singly linked list, reverse the list and return the reversed list.

### 2. Clarify Edge Cases
- Empty list? Return `None`.
- Single node? Return the node.

### 3. Brute Force Approach
Traverse the list, store all values in an array, reverse the array, create a new linked list. Time: $O(N)$, Space: $O(N)$.

### 4. Key Insight
We can reverse the pointers in-place by keeping track of the `prev`, `curr`, and `next` nodes.

### 5. Optimized Approach
Initialize `prev = None`, `curr = head`. Loop while `curr` is not None: temporarily store `next_node = curr.next`, point `curr.next` to `prev`, step forward by setting `prev = curr` and `curr = next_node`.

### 6. Justification
Time: $O(N)$ as we traverse exactly once. Space: $O(1)$ as we only use three pointers.

### 7. Code (Python)
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head: ListNode) -> ListNode:
    prev = None
    curr = head
    
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
        
    return prev
```

### 8. Dry Run
`1 -> 2 -> 3`
- init: prev=None, curr=1
- loop 1: next_node=2, 1.next=None, prev=1, curr=2
- loop 2: next_node=3, 2.next=1, prev=2, curr=3
- loop 3: next_node=None, 3.next=2, prev=3, curr=None
- exit loop. return prev (3). List is `3 -> 2 -> 1`.

### 9. Edge Cases Handled
Empty list handles perfectly: `curr` is None, loop doesn't run, returns `prev` (None).

### 10. Follow-ups
- "Can you do it recursively?" -> Yes, base case is `not head or not head.next`. Recursive call reverses the rest. Then `head.next.next = head` and `head.next = None`.

### 11. Related Problems
Reverse Linked List II, Palindrome Linked List.

---

## 2. Linked List Cycle

### 1. Restate the Problem
Given the `head` of a linked list, determine if it has a cycle.

### 2. Clarify Edge Cases
- Can nodes have duplicate values? Yes, value doesn't matter, only memory reference.
- Empty list? No cycle.

### 3. Brute Force Approach
Store every visited node in a Hash Set. If we encounter a node already in the set, there is a cycle. Time: $O(N)$, Space: $O(N)$.

### 4. Key Insight
Floyd's Cycle-Finding Algorithm (Tortoise and Hare). If two runners move at different speeds (1 step vs 2 steps), they will eventually meet if there is a cycle.

### 5. Optimized Approach
Initialize `slow` and `fast` pointers to `head`. Move `slow` by 1 and `fast` by 2. If they ever equal each other, return True. If `fast` or `fast.next` reaches `None`, return False.

### 6. Justification
Time: $O(N)$. Space: $O(1)$ because no auxiliary data structures are used.

### 7. Code (Python)
```python
def hasCycle(head: ListNode) -> bool:
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
            
    return False
```

### 8. Dry Run
`1 -> 2 -> 3 -> 4 -> (points to 2)`
- init: slow=1, fast=1
- step 1: slow=2, fast=3
- step 2: slow=3, fast=2 (wrapped)
- step 3: slow=4, fast=4. Match! True.

### 9. Edge Cases Handled
No cycle handles correctly via the `while fast and fast.next` condition.

### 10. Follow-ups
- "How do you find the *start* node of the cycle?" -> When they meet, reset `slow` to `head`. Move both by 1 step. Where they meet again is the start of the cycle.

### 11. Related Problems
Linked List Cycle II, Find the Duplicate Number.

---

## 3. Merge Two Sorted Lists

### 1. Restate the Problem
Merge two sorted linked lists into one sorted linked list.

### 2. Clarify Edge Cases
- What if one list is empty? Return the other list.
- Different lengths? Yes.

### 3. Brute Force Approach
Extract all elements to an array, sort the array, build a new list. Time: $O(N \log N)$, Space: $O(N)$.

### 4. Key Insight
Since the lists are already sorted, we can use a Two Pointers approach, comparing the heads of both lists and appending the smaller one to our new list.

### 5. Optimized Approach
Use a dummy node to easily keep track of the head of the new list. Use a `tail` pointer. While both lists have nodes, compare their values, attach the smaller to `tail.next`, and advance the pointer. After the loop, attach the remaining nodes of the non-empty list.

### 6. Justification
Time: $O(N + M)$ where N and M are the lengths of the lists. Space: $O(1)$ since we are just moving pointers, not creating new nodes.

### 7. Code (Python)
```python
def mergeTwoLists(list1: ListNode, list2: ListNode) -> ListNode:
    dummy = ListNode()
    tail = dummy
    
    while list1 and list2:
        if list1.val < list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
        
    tail.next = list1 if list1 else list2
    
    return dummy.next
```

### 8. Dry Run
`L1 = [1, 3]`, `L2 = [2, 4]`
- Compare 1 and 2. Attach 1. `L1` points to 3.
- Compare 3 and 2. Attach 2. `L2` points to 4.
- Compare 3 and 4. Attach 3. `L1` points to None.
- Loop ends. Attach remaining `L2` (4).
- Result: `1 -> 2 -> 3 -> 4`.

### 9. Edge Cases Handled
Empty inputs instantly fall through the while loop and attach the other list (or None).

### 10. Follow-ups
- "Merge K sorted lists?" -> Use a Min-Heap of size K, time $O(N \log K)$.

### 11. Related Problems
Merge K Sorted Lists, Sort List.

---

## 4. Remove Nth Node From End of List

### 1. Restate the Problem
Remove the $n$-th node from the end of a linked list and return its head.

### 2. Clarify Edge Cases
- Removing the head? Yes, if $n$ equals the length of the list.
- Can $n$ be larger than list length? Constraints usually say $1 \le n \le \text{length}$.

### 3. Brute Force Approach
Pass 1: Count the total length $L$. Pass 2: Traverse to $L - n$ and delete the node. Time: $O(N)$ (two passes). Space: $O(1)$.

### 4. Key Insight
We can do it in one pass using two pointers (`fast` and `slow`). Give `fast` a head start of $n$ steps. When `fast` reaches the end, `slow` will be exactly at the node *before* the one to delete.

### 5. Optimized Approach
Use a dummy node pointing to `head` (handles removing the first element gracefully). Move `fast` $n+1$ steps ahead. Then move `fast` and `slow` together until `fast` is None. Delete the node by `slow.next = slow.next.next`.

### 6. Justification
Time: $O(N)$ (one pass). Space: $O(1)$.

### 7. Code (Python)
```python
def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy
    
    # Move fast ahead by n + 1 steps
    for _ in range(n + 1):
        fast = fast.next
        
    # Move both until fast reaches the end
    while fast:
        slow = slow.next
        fast = fast.next
        
    # Remove the nth node
    slow.next = slow.next.next
    
    return dummy.next
```

### 8. Dry Run
`1 -> 2 -> 3 -> 4 -> 5`, `n = 2`
- fast moves 3 steps to `3`.
- slow=dummy, fast=3. Move both.
- slow=1, fast=4
- slow=2, fast=5
- slow=3, fast=None. Loop ends.
- `slow.next` (3.next, which is 4) points to 5.
- List is `1 -> 2 -> 3 -> 5`.

### 9. Edge Cases Handled
Removing the first element: `fast` hits `None` immediately after the first loop, `slow` stays at `dummy`, `dummy.next` updates correctly.

### 10. Follow-ups
- N/A (this is the optimal).

### 11. Related Problems
Middle of the Linked List.
