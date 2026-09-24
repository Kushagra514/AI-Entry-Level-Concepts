# Stacks & Queues Interview Questions

---

## 1. Valid Parentheses

### 1. Restate the Problem
Given a string containing just the characters `'(', ')', '{', '}', '[' and ']'`, determine if the input string is valid (every open bracket is closed by the same type of bracket in the correct order).

### 2. Clarify Edge Cases
- Empty string? Valid.
- String with only open or only close brackets? Invalid.

### 3. Brute Force Approach
Repeatedly replace `()`, `{}`, and `[]` with empty strings until no more replacements can be made. If the string becomes empty, it's valid. Time: $O(N^2)$.

### 4. Key Insight
A Stack perfectly models this LIFO (Last-In-First-Out) requirement. The last open bracket seen must be the first one closed.

### 5. Optimized Approach
Iterate through the string. If we see an open bracket, push it to the stack. If we see a close bracket, pop from the stack and check if it matches the corresponding open bracket. If the stack is empty when seeing a close bracket, or if the stack is not empty at the end, it's invalid.

### 6. Justification
Time: $O(N)$ since we iterate through the string once and push/pop take $O(1)$. Space: $O(N)$ for the stack in the worst case (all open brackets).

### 7. Code (Python)
```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            # Pop element if stack is not empty, else use dummy value
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack
```

### 8. Dry Run
`s = "{[]}"`
- '{' -> stack = ['{']
- '[' -> stack = ['{', '[']
- ']' -> pop '[', matches map[']']. stack = ['{']
- '}' -> pop '{', matches map['}']. stack = []
- Returns True.

### 9. Edge Cases Handled
- `]`: stack is empty, pops `#`, map[']'] is `[`, False.
- `[`: ends with stack not empty, `not stack` evaluates to False.

### 10. Follow-ups
- "What if there are other characters (letters) in the string?" -> Just ignore them and only process brackets.

### 11. Related Problems
Generate Parentheses, Minimum Remove to Make Valid Parentheses.

---

## 2. Min Stack

### 1. Restate the Problem
Design a stack that supports `push`, `pop`, `top`, and retrieving the minimum element in constant time ($O(1)$).

### 2. Clarify Edge Cases
- Popping an empty stack? Assume valid operations per constraints.
- Duplicate minimums? Should handle fine.

### 3. Brute Force Approach
Standard stack. When `getMin` is called, iterate through the entire stack to find the minimum. Time: $O(N)$ for `getMin`, $O(1)$ for others.

### 4. Key Insight
We can't just keep a single `min` variable, because if we pop the minimum, we wouldn't know the *second* minimum. Therefore, we must store the current minimum *at each state of the stack*.

### 5. Optimized Approach
Use two stacks (or store tuples in one stack). The main stack stores values. The `min_stack` stores the minimum value seen so far. When pushing `x`, we push `min(x, min_stack.top())` onto the `min_stack`. When popping, we pop both.

### 6. Justification
Time: $O(1)$ for all operations. Space: $O(N)$ for the extra `min_stack`.

### 7. Code (Python)
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(val, self.min_stack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

### 8. Dry Run
`push(-2), push(0), push(-3), getMin(), pop(), top(), getMin()`
- push -2: stk=[-2], min=[-2]
- push 0: stk=[-2, 0], min=[-2, -2]
- push -3: stk=[-2, 0, -3], min=[-2, -2, -3]
- getMin: returns -3
- pop: stk=[-2, 0], min=[-2, -2]
- top: returns 0
- getMin: returns -2

### 9. Edge Cases Handled
Empty minimum stack on first push handled correctly.

### 10. Follow-ups
- "Can you optimize the space?" -> Yes, instead of storing duplicates in `min_stack`, only push to `min_stack` if `val <= min_stack[-1]`. Pop from `min_stack` only if the popped value equals `min_stack[-1]`.

### 11. Related Problems
Max Stack, Sliding Window Maximum.

---

## 3. Implement Queue using Stacks

### 1. Restate the Problem
Implement a FIFO queue using only two LIFO stacks. Support `push`, `pop`, `peek`, and `empty`.

### 2. Clarify Edge Cases
- All operations valid. No popping empty queues.

### 3. Brute Force Approach
N/A, this is a design problem.

### 4. Key Insight
A stack reverses order. Two stacks reverse the order twice, bringing it back to the original FIFO order.

### 5. Optimized Approach
Maintain `stack_in` and `stack_out`. For `push`, push to `stack_in`. For `pop` or `peek`, if `stack_out` is empty, pop all elements from `stack_in` and push them to `stack_out`. Then pop/peek from `stack_out`.

### 6. Justification
Time: `push` is $O(1)$. `pop`/`peek` is Amortized $O(1)$ (worst case $O(N)$ when moving elements, but each element is moved exactly once). Space: $O(N)$ for the stacks.

### 7. Code (Python)
```python
class MyQueue:
    def __init__(self):
        self.s_in = []
        self.s_out = []

    def push(self, x: int) -> None:
        self.s_in.append(x)

    def _move(self):
        if not self.s_out:
            while self.s_in:
                self.s_out.append(self.s_in.pop())

    def pop(self) -> int:
        self._move()
        return self.s_out.pop()

    def peek(self) -> int:
        self._move()
        return self.s_out[-1]

    def empty(self) -> bool:
        return not self.s_in and not self.s_out
```

### 8. Dry Run
`push(1), push(2), peek(), pop(), empty()`
- push 1: in=[1], out=[]
- push 2: in=[1, 2], out=[]
- peek: move all -> in=[], out=[2, 1]. returns 1
- pop: out pops 1. out=[2]. returns 1
- empty: in and out are not empty (out has 2). returns False

### 9. Edge Cases Handled
Subsequent pushes while `s_out` is full just go to `s_in`, maintaining correct order since they are newer than what is in `s_out`.

### 10. Follow-ups
- "Can you implement a Stack using Queues?" -> Yes, use one Queue, push element, then pop and push all existing elements behind it.

### 11. Related Problems
Implement Stack using Queues.

---

## 4. Daily Temperatures (Monotonic Stack)

### 1. Restate the Problem
Given an array of daily temperatures, return an array where `answer[i]` is the number of days you have to wait after the $i$-th day to get a warmer temperature. If none, keep 0.

### 2. Clarify Edge Cases
- No warmer days? Output 0.

### 3. Brute Force Approach
For each day, scan the rest of the array until a higher temperature is found. Time: $O(N^2)$, Space: $O(1)$.

### 4. Key Insight
We need to find the "next greater element". A Monotonic Decreasing Stack is perfect for this. It stores indices of days waiting for a warmer day.

### 5. Optimized Approach
Iterate through the array. While the current temp is greater than the temp at the index at the top of the stack, we found a warmer day for that past day! Pop it, calculate the difference in indices, and save it in the answer array. Then push the current day's index.

### 6. Justification
Time: $O(N)$ because every index is pushed and popped at most once. Space: $O(N)$ for the stack and output array.

### 7. Code (Python)
```python
from typing import List

def dailyTemperatures(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    ans = [0] * n
    stack = []  # stores indices
    
    for i, t in enumerate(temperatures):
        while stack and t > temperatures[stack[-1]]:
            prev_i = stack.pop()
            ans[prev_i] = i - prev_i
        stack.append(i)
        
    return ans
```

### 8. Dry Run
`T = [73, 74, 75, 71, 69, 72, 76, 73]`
- i=0, T=73: stack=[0]
- i=1, T=74: 74 > T[0](73). pop 0. ans[0] = 1-0 = 1. stack=[1]
- i=2, T=75: 75 > T[1](74). pop 1. ans[1] = 2-1 = 1. stack=[2]
- i=3, T=71: 71 < 75. stack=[2, 3]
- i=4, T=69: 69 < 71. stack=[2, 3, 4]
- i=5, T=72: 72 > T[4](69). pop 4, ans[4]=1. 72 > T[3](71). pop 3, ans[3]=2. stack=[2, 5]

### 9. Edge Cases Handled
Decreasing temperatures just stack up and default 0s remain in `ans`.

### 10. Follow-ups
- N/A.

### 11. Related Problems
Next Greater Element, Largest Rectangle in Histogram.
