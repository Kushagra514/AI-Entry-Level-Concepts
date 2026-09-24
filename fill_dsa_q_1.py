import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (DSA Qs)"')

wc("23-dsa-interview-questions/arrays-strings.md", r"""# Arrays & Strings Interview Questions

---

## 1. Two Sum

### 1. Restate the Problem
Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`. Exactly one solution exists.

### 2. Clarify Edge Cases
- Are there negative numbers? Yes.
- Can I use the same element twice? No.
- Is the array sorted? No.

### 3. Brute Force Approach
Nested loops. For each element `nums[i]`, iterate through the rest of the array `nums[j]` to see if `nums[i] + nums[j] == target`. Time: $O(N^2)$, Space: $O(1)$.

### 4. Key Insight
If we are looking at `nums[i]`, we specifically need `target - nums[i]`. We can store every number we've seen so far in a Hash Map (val -> index). This allows $O(1)$ lookups for the needed complement.

### 5. Optimized Approach
Iterate through the array. For each number, calculate its complement. Check if the complement is in the Hash Map. If yes, return the current index and the complement's index. If no, add the current number to the Hash Map.

### 6. Justification
Time complexity is $O(N)$ because we traverse the array once and hash map lookups are $O(1)$. Space complexity is $O(N)$ because in the worst case we store $N-1$ elements in the map.

### 7. Code (Python)
```python
from typing import List

def twoSum(nums: List[int], target: int) -> List[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

### 8. Dry Run
`nums = [2, 7, 11, 15]`, `target = 9`
- i=0, num=2: comp=7. Not in seen. seen = {2: 0}
- i=1, num=7: comp=2. In seen! Return `[seen[2], 1]` -> `[0, 1]`.

### 9. Edge Cases Handled
Target is exactly twice a number (e.g., `[3, 2, 4]`, target `6`). Handled because we check the map *before* adding the current number, ensuring we don't reuse it.

### 10. Follow-ups
- "What if the array is sorted?" -> Use Two Pointers ($O(N)$ time, $O(1)$ space).

### 11. Related Problems
Three Sum, Four Sum, Subarray Sum Equals K.

---

## 2. Best Time to Buy and Sell Stock

### 1. Restate the Problem
Given an array `prices` where `prices[i]` is the price of a given stock on the $i$-th day, maximize profit by choosing a single day to buy and a different day in the future to sell.

### 2. Clarify Edge Cases
- What if prices strictly decrease? Return 0 (no transaction).
- Can I short sell? No.

### 3. Brute Force Approach
Try every pair `(i, j)` where $j > i$. Compute `prices[j] - prices[i]` and track max. Time: $O(N^2)$.

### 4. Key Insight
To maximize profit if we sell on day `i`, we MUST have bought at the absolute lowest price seen *before* day `i`.

### 5. Optimized Approach
Maintain a `min_price` variable (initialized to infinity) and a `max_profit` variable (initialized to 0). Iterate through the array once. Update `min_price` if the current price is lower. Else, update `max_profit` if `current_price - min_price` is greater than `max_profit`.

### 6. Justification
Single pass gives $O(N)$ time. We only store two variables, giving $O(1)$ space.

### 7. Code (Python)
```python
from typing import List

def maxProfit(prices: List[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
            
    return max_profit
```

### 8. Dry Run
`prices = [7, 1, 5, 3, 6, 4]`
- 7: min=7, max=0
- 1: min=1, max=0
- 5: min=1, max=(5-1)=4
- 3: min=1, max=4
- 6: min=1, max=(6-1)=5
- 4: min=1, max=5. Return 5.

### 9. Edge Cases Handled
Empty array (usually constrained to >=1). Strictly decreasing `[7, 6, 4, 3, 1]` returns 0.

### 10. Follow-ups
- "What if you can buy and sell multiple times?" -> Greedy approach: add all positive differences between consecutive days.

### 11. Related Problems
Stock Buy and Sell II/III/IV.

---

## 3. Longest Substring Without Repeating Characters

### 1. Restate the Problem
Find the length of the longest substring without repeating characters in a given string.

### 2. Clarify Edge Cases
- What character set? (Assume ASCII).
- Empty string? Return 0.

### 3. Brute Force Approach
Generate all substrings ($O(N^2)$), check each for duplicates ($O(N)$). Total: $O(N^3)$.

### 4. Key Insight
Use a Sliding Window. As we expand the right edge, if we encounter a duplicate character, we shrink the left edge until the duplicate is removed from the window.

### 5. Optimized Approach
Use a hash map to store the most recent index of each character. Iterate with `right` pointer. If `s[right]` is in the map, jump the `left` pointer to `map[s[right]] + 1` (but only if this index is greater than the current `left`). Update the max length.

### 6. Justification
Time: $O(N)$ because `right` moves forward $N$ times and `left` jumps forward. Space: $O(1)$ since the character set is bounded (e.g., 256 ASCII characters).

### 7. Code (Python)
```python
def lengthOfLongestSubstring(s: str) -> int:
    char_index_map = {}
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        if s[right] in char_index_map:
            # Don't let left pointer move backwards
            left = max(left, char_index_map[s[right]] + 1)
            
        char_index_map[s[right]] = right
        max_len = max(max_len, right - left + 1)
        
    return max_len
```

### 8. Dry Run
`s = "abba"`
- right=0, 'a': map={'a':0}, max=1
- right=1, 'b': map={'a':0, 'b':1}, max=2
- right=2, 'b': in map! left = max(0, 1+1) = 2. map={'a':0, 'b':2}, max=2
- right=3, 'a': in map! left = max(2, 0+1) = 2. map={'a':3, 'b':2}, max=2 (len: 3-2+1=2)

### 9. Edge Cases Handled
`abba` forces the `max(left, ...)` check so `left` doesn't incorrectly jump backwards to index 1 when seeing the second 'a'.

### 10. Follow-ups
- "What if the string contains only lowercase english letters?" -> Can use a boolean array of size 26 instead of a hash map.

### 11. Related Problems
Longest Repeating Character Replacement, Minimum Window Substring.

---

## 4. Valid Anagram

### 1. Restate the Problem
Given two strings `s` and `t`, return true if `t` is an anagram of `s`.

### 2. Clarify Edge Cases
- Do case and spaces matter? (Assume lowercase letters only).
- Different lengths? Immediately false.

### 3. Brute Force Approach
Sort both strings and compare. Time: $O(N \log N)$, Space: $O(1)$ or $O(N)$ depending on language sorting implementation.

### 4. Key Insight
An anagram means the exact same frequency of characters. We can count the characters in both strings and compare the counts.

### 5. Optimized Approach
Create an array of size 26 (for a-z). Increment counts for characters in `s`, decrement for `t`. If all elements in the array are 0 at the end, it's an anagram.

### 6. Justification
Time: $O(N)$ to iterate through the strings. Space: $O(1)$ because the frequency array size is constant (26), regardless of string length.

### 7. Code (Python)
```python
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
        
    counts = [0] * 26
    for i in range(len(s)):
        counts[ord(s[i]) - ord('a')] += 1
        counts[ord(t[i]) - ord('a')] -= 1
        
    for count in counts:
        if count != 0:
            return False
            
    return True
```

### 8. Dry Run
`s = "ab"`, `t = "ba"`
- `s[0]='a'`: counts[0]=1, `t[0]='b'`: counts[1]=-1
- `s[1]='b'`: counts[1]=0, `t[1]='a'`: counts[0]=0
- All counts are 0. True.

### 9. Edge Cases Handled
Different lengths caught immediately.

### 10. Follow-ups
- "What if inputs contain Unicode characters?" -> Use a Hash Map instead of a fixed size 26 array.

### 11. Related Problems
Group Anagrams, Find All Anagrams in a String.
""")

wc("23-dsa-interview-questions/linked-lists.md", r"""# Linked Lists Interview Questions

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
""")
print("DSA Qs 1 complete")
