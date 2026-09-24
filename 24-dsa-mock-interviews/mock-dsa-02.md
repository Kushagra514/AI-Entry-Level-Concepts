# DSA Mock Interview 2: Linked Lists & Pointers

## Problem Statement
**Interviewer:** Given the `head` of a linked list, return the node where the cycle begins. If there is no cycle, return `null`. You must solve this in $O(1)$ space.

## The Interview Conversation

**Me (Clarification):** Does the cycle have to include the head, or can it start anywhere? And can the linked list be empty?
**Interviewer:** The cycle can start at any node. Yes, the list can be empty, which means no cycle.
**Me (Brute Force):** Without the space constraint, I would just traverse the list and add every node's memory reference to a Hash Set. The first node I encounter that is already in the set is the start of the cycle. But that uses $O(N)$ space.
**Interviewer:** Right. How do we do it in $O(1)$ space?
**Me (Insight):** I can use Floyd's Tortoise and Hare algorithm. First, I'll use a slow pointer (moves 1 step) and a fast pointer (moves 2 steps). If there is a cycle, they will eventually meet. If the fast pointer reaches the end of the list, there is no cycle.
**Interviewer:** Okay, that tells us *if* a cycle exists. How do you find the *start* of the cycle?
**Me (Math/Logic):** When they meet, the slow pointer has traveled distance $D$. The fast pointer has traveled $2D$. The difference $D$ is exactly a multiple of the cycle length. It mathematically works out that the distance from the head of the list to the cycle start is the exact same as the distance from the meeting point to the cycle start. So, if I reset the slow pointer to the head, and move both pointers 1 step at a time, they will collide exactly at the cycle start.

## Code Implementation
```python
def detectCycle(head: ListNode) -> ListNode:
    slow = head
    fast = head
    
    # Phase 1: Detect Cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            break
    else:
        # Loop finished without breaking, so no cycle
        return None
        
    # Phase 2: Find Start of Cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
        
    return slow
```

## Dry Run & Edge Cases
**Me:** Let's trace an edge case: no cycle. `1 -> 2 -> None`.
1. `slow=1, fast=1`. 
2. Loop starts because `fast(1)` and `fast.next(2)` are valid.
3. `slow=2, fast=None`.
4. Next loop check: `fast` is None. `while` loop exits normally. Hits the `else` block and returns `None`. Correct.
**Interviewer:** Very good use of Python's `while-else` construct.

## Follow-up Questions
**Interviewer:** If you only wanted to find the *length* of the cycle, how would you change the code?
**Me:** Once Phase 1 completes and `slow == fast`, I would just freeze the `slow` pointer in place. Then, I would advance the `fast` pointer 1 step at a time, keeping a counter, until it wrapped around and equalled `slow` again. The counter would be the length of the cycle.
