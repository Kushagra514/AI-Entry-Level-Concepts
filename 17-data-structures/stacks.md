# Stacks

## 1. Definition
A Stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle. The last element added is the first element removed.

## 2. Intuition
Think of a stack of plates at a buffet. You can only place a new plate on top (push), and when you need a plate, you take it off the top (pop). If you want the plate at the bottom, you must remove all the plates above it first.

## 3. Why it exists
Stacks are essential for managing sequential processes where you must return to previous states in reverse order. They elegantly handle nested structures, undo mechanisms, and backtracking without complex state-tracking logic.

## 4. Mechanics
- **Push:** Add an element to the top.
- **Pop:** Remove and return the top element.
- **Peek / Top:** View the top element without removing it.
- Internally, a stack can be implemented using a dynamic array (list) or a linked list (inserting/deleting at the head).

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Push, Pop, Peek: $O(1)$ (amortized if using a dynamic array).
  - Search: $O(N)$ (requires popping elements off to find a target).
- **Space Complexity:** $O(N)$ to store $N$ elements.

## 6. Tiny worked example
Stack: `[]`
- `Push(1)` -> `[1]`
- `Push(2)` -> `[1, 2]`
- `Pop()` -> Returns 2. Stack: `[1]`
- `Peek()` -> Returns 1. Stack: `[1]`

## 7. Code (Python, with type hints)
```python
from typing import List

class Stack:
    def __init__(self):
        # Using Python list as a dynamic array
        self.stack: List[int] = []
        
    def push(self, val: int) -> None:
        self.stack.append(val)
        
    def pop(self) -> int:
        if not self.is_empty():
            return self.stack.pop()
        raise IndexError("pop from empty stack")
        
    def is_empty(self) -> bool:
        return len(self.stack) == 0
```

## 8. Common mistakes
- Forgetting to check if the stack is empty before popping (IndexError).
- Using a stack when a queue (FIFO) is required (e.g., in BFS).
- In Python, using `insert(0, val)` to push, which is $O(N)$, instead of `append(val)`, which is $O(1)$.

## 9. 30-second interview answer
"A stack is a Last-In-First-Out (LIFO) data structure. It supports $O(1)$ push and pop operations. It's heavily used in parsing (like validating parentheses), evaluating expressions, and simulating recursion or backtracking via DFS."

## 10. 2-minute interview answer
"A stack enforces LIFO ordering, making it the perfect structure for state-reversal problems. Under the hood, they are usually implemented as dynamic arrays where we only interact with the final index, ensuring $O(1)$ amortized pushes and pops. Conceptually, every program relies on a stack—the Call Stack—to manage function execution and scoping. In algorithmic interviews, whenever a problem involves 'matching' nested elements like brackets, processing elements in reverse order of arrival, or exploring paths where we need to 'undo' a choice (backtracking/DFS), an explicit stack is the optimal tool."

## 11. Follow-ups
- "What is a Monotonic Stack?" (A stack whose elements are strictly increasing or decreasing. Used to find the 'next greater element' in $O(N)$ time).
- "How do you implement a Stack using Queues?" (You need two queues. To push, enqueue to Q2, then dequeue everything from Q1 to Q2, then swap names).

## 12. Deeper questions
- "If a recursive function stack overflows, how do you fix it?" (Convert the implicit call stack recursion into an iterative loop using an explicit Stack data structure allocated on the heap).

## 13. Related concepts
- **Depth-First Search (DFS)**: Uses a stack (either implicit call stack or explicit).
- **Monotonic Stack**: A pattern to solve nearest-greater-element problems.

## 14. When it breaks / Edge cases
- Popping from an empty stack is the most common failure state.

## 15. Comparison with alternative approaches
- **vs Queues:** Stacks are LIFO (DFS). Queues are FIFO (BFS).

---
*Where this shows up in ML:* 
In compiler pipelines for ML frameworks (like PyTorch JIT or XLA), stacks are used extensively to parse the Abstract Syntax Trees (ASTs) of Python code and convert them into static computation graphs.
