# Pattern: Monotonic Stack

## 1. Definition
A Monotonic Stack is a stack whose elements are guaranteed to be strictly increasing or strictly decreasing. It is used to find the "Next Greater" or "Next Smaller" element in an array in $O(N)$ time.

## 2. Intuition
Imagine a line of people of varying heights looking to their right. You want to know who is the first person taller than you. If someone behind you is shorter than you, they are totally irrelevant because anyone looking right will see *you* before they see the shorter person. A monotonic stack naturally "hides" these irrelevant shorter people, maintaining only the relevant tall people in order.

## 3. Why it exists
Finding the "Next Greater Element" with nested loops takes $O(N^2)$. A Monotonic Stack prunes the search space by aggressively discarding elements that can no longer be the answer, reducing the problem to $O(N)$ time.

## 4. Mechanics
To find the **Next Greater Element**:
1. Iterate through the array.
2. While the stack is not empty AND the current element is *greater* than the top of the stack:
   - Pop the top element. The current element is the "Next Greater" answer for the popped element.
3. Push the current element (or its index) onto the stack.
*Result: The stack remains monotonically decreasing.*

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - Every element is pushed exactly once and popped at most once.
- **Space Complexity:** $O(N)$ - For the stack.

## 6. Tiny worked example
Array: `[2, 1, 5, 3]`
- `2`: Stack `[2]`.
- `1`: $1 \not> 2$. Push. Stack `[2, 1]`.
- `5`: $5 > 1$. Pop `1`. (Next greater for 1 is 5). 
       $5 > 2$. Pop `2`. (Next greater for 2 is 5). 
       Push 5. Stack `[5]`.
- `3`: $3 \not> 5$. Push. Stack `[5, 3]`.
(Elements left in stack have no greater element).

## 7. Code (Python, with type hints)
```python
from typing import List

def next_greater_elements(nums: List[int]) -> List[int]:
    n = len(nums)
    res = [-1] * n
    stack = [] # Stores INDICES, not values
    
    for i in range(n):
        # While stack has items and current element is strictly greater
        while stack and nums[i] > nums[stack[-1]]:
            popped_idx = stack.pop()
            res[popped_idx] = nums[i]
            
        stack.append(i)
        
    return res
```

## 8. Common mistakes
- Storing **values** in the stack instead of **indices**. You usually need the index to map the answer back to the output array.
- Confusing whether to use a Monotonic Increasing or Decreasing stack. (Rule of thumb: Looking for Next Greater -> Decreasing Stack. Next Smaller -> Increasing Stack).

## 9. 30-second interview answer
"A Monotonic Stack maintains elements in a strictly increasing or decreasing order. It is the optimal $O(N)$ pattern for finding the 'Next Greater' or 'Next Smaller' element. By popping elements that violate the monotonic property, it efficiently resolves pending queries."

## 10. 2-minute interview answer
"The Monotonic Stack is a specialized application of the LIFO principle used to optimize $O(N^2)$ range queries down to $O(N)$ time. It solves 'Next Greater Element' problems—like finding the next warmer day in a list of temperatures. As we iterate, we push indices onto the stack. If we encounter a value that breaks the monotonic property (e.g., a larger value when maintaining a decreasing stack), we know we have found the exact 'Next Greater' answer for the elements currently on the stack. We pop them off, record the answer, and push the new element. Because every element is pushed and popped exactly once, the time complexity is strictly linear."

## 11. Follow-ups
- "What if the array is circular?" (Loop through the array twice `range(2 * n)`, using `i % n` for the index).

## 12. Deeper questions
- "How does this apply to the 'Largest Rectangle in Histogram' problem?" (You use an increasing monotonic stack to find the Next Smaller and Previous Smaller elements simultaneously, which defines the boundaries of the rectangle for each bar).

## 13. Related concepts
- **Stacks**: The underlying data structure.
- **Sliding Window Maximum**: Uses a Monotonic *Deque*.

## 14. When it breaks / Edge cases
- Repeated elements (e.g., `[2, 2, 2]`) must be handled carefully with strictly greater `>` vs greater-than-equal `>=` depending on problem constraints.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Not heavily used in ML modeling, but crucial in systems engineering and competitive programming.
