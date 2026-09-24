import os

def write_and_commit(path, content):
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch A)"')

files = {}

files["17-data-structures/stacks.md"] = """# Stacks

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
"""

files["17-data-structures/queues.md"] = """# Queues

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
"""

files["18-algorithms/binary-search.md"] = """# Binary Search

## 1. Definition
Binary Search is a divide-and-conquer algorithm that finds the position of a target value within a **sorted** array by repeatedly dividing the search interval in half.

## 2. Intuition
If you are looking for the word "Machine" in a physical dictionary, you don't start at page 1 and flip one by one. You open to the middle. If you see "Orange", you know "Machine" must be in the left half. You tear the book in half, discard the right side, and repeat until you find the word. 

## 3. Why it exists
Linear search takes $O(N)$ time, which is too slow for massive datasets. Binary search exists to exploit the property of "sortedness" (monotonicity), reducing the search time exponentially to $O(\\log N)$.

## 4. Mechanics
1. Initialize two pointers: `left = 0`, `right = len(array) - 1`.
2. Find the midpoint: `mid = left + (right - left) // 2`.
3. Check if `array[mid] == target`. If so, return `mid`.
4. If `array[mid] < target`, the target must be in the right half. Update `left = mid + 1`.
5. If `array[mid] > target`, the target must be in the left half. Update `right = mid - 1`.
6. Repeat until `left > right`.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\\log N)$ - The search space is halved every step.
- **Space Complexity:** $O(1)$ - Iterative implementation requires just three pointers (`left`, `right`, `mid`).

## 6. Tiny worked example
Array: `[2, 4, 6, 8, 10]`, Target: `8`
- `L=0`, `R=4`. `mid=2` (val `6`). `6 < 8`, so `L = 3`.
- `L=3`, `R=4`. `mid=3` (val `8`). `8 == 8`. Found at index 3.

## 7. Code (Python, with type hints)
```python
from typing import List

def binary_search(arr: List[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    
    while left <= right:
        # Prevents integer overflow in languages like Java/C++
        mid = left + (right - left) // 2 
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1
```

## 8. Common mistakes
- **Off-by-one errors:** Using `while left < right` instead of `<=`, or `left = mid` instead of `mid + 1`, causing infinite loops.
- Calculating mid as `(left + right) // 2`. In Python this is fine, but in Java/C++ it can cause integer overflow if left and right are huge. Use `left + (right - left) / 2`.
- Attempting to use Binary Search on an unsorted array.

## 9. 30-second interview answer
"Binary Search is an $O(\\log N)$ algorithm for finding a target in a sorted array. It works by repeatedly comparing the target to the middle element and halving the search space. It's incredibly fast but requires the data to be monotonic."

## 10. 2-minute interview answer
"Binary Search is the premier algorithm for optimizing $O(N)$ searches down to $O(\\log N)$, provided the search space is sorted or monotonic. The classic implementation uses a `while left <= right` loop and integer division to find the midpoint. The most critical part of writing it bug-free is ensuring the search boundaries shrink correctly (`left = mid + 1` and `right = mid - 1`) to avoid infinite loops. Beyond simple arrays, the most powerful application of this pattern in interviews is 'Binary Search on the Answer', where we binary search not over an array, but over a numerical range of possible answers, validating each midpoint using a helper function."

## 11. Follow-ups
- "How do you find the *first* occurrence of a target in an array with duplicates?" (Modify the check: if `arr[mid] == target`, don't return. Instead, record the index and shrink the right bound `right = mid - 1` to keep searching left).
- "What is `bisect` in Python?" (Python's built-in binary search library).

## 12. Deeper questions
- "How would you perform Binary Search on an array where the size is unknown or infinite?" (Start with bounds 0 and 1. If target > arr[1], double the bounds to 1 and 2, then 2 and 4, 4 and 8... until you bound the target, then do standard binary search. $O(\\log P)$ where P is position).

## 13. Related concepts
- **Binary Search Trees (BST)**: A tree structure built around the binary search concept.
- **Binary Search on Answer**: A master pattern for optimization problems.

## 14. When it breaks / Edge cases
- Breaks entirely if the array isn't sorted.
- Fails if the array contains duplicate targets and you are asked for a specific one (without modifying the standard template).

## 15. Comparison with alternative approaches
- **vs Hash Map:** Hash Map gives $O(1)$ search, but takes $O(N)$ space and loses sorted ordering (e.g., you can't easily find "the closest number" with a Hash Map, but you can with Binary Search).

---
*Where this shows up in ML:* 
In Decision Trees, finding the optimal threshold to split continuous numerical features often involves sorting the features and searching (though fully exhaustive trees check all points, optimized versions use bisecting logic). Additionally, in hyperparameter tuning, if a parameter's effect on loss is monotonic, one could conceptually binary-search for the optimal value.
"""

files["18-algorithms/sorting-overview.md"] = """# Sorting Algorithms Overview

## 1. Definition
Sorting algorithms rearrange a collection of items into a specific hierarchical order (e.g., numerical or lexicographical).

## 2. Intuition
If you have a hand of playing cards, you intuitively sort them so you can quickly see what you have and make decisions. Sorting algorithms are formal, step-by-step methods instructing computers how to achieve that ordered state.

## 3. Why it exists
Unsorted data requires $O(N)$ time to search. Sorted data unlocks Binary Search ($O(\\log N)$), simplifies finding duplicates, and makes Two Pointer techniques viable. Sorting is the most fundamental preprocessing step in computer science.

## 4. Mechanics
Algorithms generally fall into two categories:
1. **Comparison-based:** Compare elements against each other (Bubble, Insertion, Merge, Quick, Heap). Mathematically bounded by a minimum worst-case time of $O(N \\log N)$.
2. **Non-comparison-based:** Exploit properties of the data (like integers in a narrow range) to sort without direct comparisons (Counting, Radix, Bucket). Can achieve $O(N)$ time.

## 5. Complexity (Time & Space)
*(See specific algorithm files for deep dives. High-level summary:)*
- **O(N^2) Time:** Bubble, Selection, Insertion (Good for tiny or nearly-sorted data).
- **O(N log N) Time:** Merge (Stable, $O(N)$ space), Quick (Unstable, $O(\\log N)$ space, worst $O(N^2)$), Heap (Unstable, $O(1)$ space).
- **O(N) Time:** Counting, Radix (Requires specific data types, $O(N)$ space).

## 6. Tiny worked example
*(Concepts: Stability and In-Place)*
- **Stability:** If you sort `[(Alice, 50), (Bob, 50)]` by score, a *stable* sort guarantees Alice remains before Bob. An *unstable* sort might flip them to `[(Bob, 50), (Alice, 50)]`.
- **In-Place:** Sorts by swapping elements within the original array (Quick, Heap). Out-of-place allocates a new array (Merge).

## 7. Code (Python, with type hints)
```python
# Python's built-in Timsort (a hybrid of Merge Sort and Insertion Sort)
# Time: O(N log N) worst case, O(N) best case (if already sorted).
# Space: O(N). It is a STABLE sort.
arr = [5, 2, 9, 1]
arr.sort() # In-place
new_arr = sorted(arr) # Out-of-place
```

## 8. Common mistakes
- Thinking $O(N \\log N)$ is the absolute limit for all sorting (forgetting Radix/Counting sort).
- Not knowing the difference between Stable and Unstable sorts when an interviewer asks "sort by X, then sort by Y". (You must use a stable sort for the second pass).

## 9. 30-second interview answer
"Comparison-based sorting algorithms are mathematically bounded at $O(N \\log N)$ time complexity. Merge Sort offers guaranteed $O(N \\log N)$ time and stability but requires $O(N)$ space. Quick Sort is often faster in practice with $O(\\log N)$ space but is unstable and has a worst-case $O(N^2)$. Python uses Timsort, a highly optimized stable hybrid."

## 10. 2-minute interview answer
"Understanding sorting is less about writing them from scratch and more about knowing their tradeoffs. For general purposes, an $O(N \\log N)$ algorithm like Quick Sort or Merge Sort is standard. Merge Sort is stable, meaning it preserves the relative order of equal elements, which is crucial for multi-pass sorting, but it costs $O(N)$ memory. Quick Sort operates in-place, making it cache-friendly and faster in practice, though it is unstable and can degrade to $O(N^2)$ with a poor pivot. If we are sorting integers within a tightly constrained range, we can bypass the $O(N \\log N)$ comparison bound entirely and use Counting Sort to achieve $O(N)$ time. In production, languages like Python and Java use hybrid algorithms like Timsort, combining the $O(N \\log N)$ scaling of Merge Sort with the $O(N)$ best-case efficiency of Insertion Sort for nearly-sorted data."

## 11. Follow-ups
- "Why does Python use Timsort instead of Quicksort?" (Timsort is stable and heavily optimized for real-world data, which often contains partially sorted subsequences).

## 12. Deeper questions
- "Prove why comparison-based sorting cannot be faster than $O(N \\log N)$." (A decision tree for sorting $N$ elements has $N!$ leaves. The minimum depth of a binary tree with $N!$ leaves is $\\log(N!)$, which by Stirling's approximation is $O(N \\log N)$).

## 13. Related concepts
- **Binary Search**: Only works on sorted data.
- **Two Pointers**: Often requires sorting the array first.

## 14. When it breaks / Edge cases
- Memory limits: Merge Sort breaks if you don't have enough RAM for the $O(N)$ overhead.

## 15. Comparison with alternative approaches
- If you only need the "Top K" elements, sorting the whole array in $O(N \\log N)$ is suboptimal. Use a Heap ($O(N \\log K)$) or Quickselect ($O(N)$).

---
*Where this shows up in ML:* 
Sorting is heavily used in ranking metrics (like NDCG or MAP in recommender systems) and in extracting the Top-K most probable tokens during LLM generation. It's also used to sort data points when calculating AUC-ROC.
"""

files["18-algorithms/merge-sort.md"] = """# Merge Sort

## 1. Definition
Merge Sort is a stable, divide-and-conquer, comparison-based sorting algorithm that recursively splits an array into halves, sorts them, and merges them back together.

## 2. Intuition
If you have a messy stack of 100 papers to alphabetize, you could split it into two stacks of 50, hand one to a friend, and both alphabetize your stacks. When you're done, you look at the top paper of each stack and repeatedly take the alphabetically smaller one, perfectly merging the two sorted stacks into one.

## 3. Why it exists
Older algorithms like Insertion or Bubble sort took $O(N^2)$ time, which scales terribly. Merge Sort was invented by John von Neumann in 1945 to guarantee an $O(N \\log N)$ worst-case time complexity, providing a mathematical ceiling on how slow sorting could be.

## 4. Mechanics
1. **Divide:** Recursively divide the array into two halves until you have sub-arrays of size 1 (which are inherently sorted).
2. **Conquer/Merge:** Take two sorted sub-arrays and merge them into a single sorted array. 
3. To merge: use two pointers, one at the start of each sub-array. Compare the elements, copy the smaller one to a temporary array, and move the pointer forward.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \\log N)$ in Best, Average, and Worst cases. The array is split in half $\\log N$ times, and merging takes $O(N)$ time at each level.
- **Space Complexity:** $O(N)$ - Requires a temporary array of size $N$ to hold the merged elements.

## 6. Tiny worked example
`[38, 27, 43, 3]`
- Split: `[38, 27]` and `[43, 3]`
- Split: `[38]`, `[27]` and `[43]`, `[3]`
- Merge: `[27, 38]` and `[3, 43]`
- Merge: Compare 27 and 3. Take 3. Compare 27 and 43. Take 27. Compare 38 and 43. Take 38. Take 43. -> `[3, 27, 38, 43]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # The '<=' ensures STABILITY. 
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # Append any remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged
```

## 8. Common mistakes
- Forgetting that array slicing in Python (`arr[:mid]`) creates copies, which is fine for readability but adds overhead. In strict interviews, you should pass index pointers `(arr, start, end)` to save memory.
- Using `<` instead of `<=` during the merge step, which breaks the **stability** of the sort.

## 9. 30-second interview answer
"Merge Sort is a divide-and-conquer algorithm with a guaranteed $O(N \\log N)$ time complexity. It works by recursively halving the array until size 1, then merging the sorted halves. It is a stable sort, but its main drawback is requiring $O(N)$ auxiliary space."

## 10. 2-minute interview answer
"Merge sort is the textbook example of divide-and-conquer. Because it strictly halves the data $\\log N$ times and merges them in $N$ operations per level, it strictly guarantees $O(N \\log N)$ time across best, average, and worst cases. Furthermore, it is a stable sort—if two elements are equal, their original relative order is preserved, which is vital when sorting objects by multiple criteria. However, because it cannot easily merge arrays in-place without degrading to $O(N^2)$, it requires $O(N)$ auxiliary memory. Therefore, for purely in-memory arrays, Quicksort is often preferred for cache locality, but Merge Sort shines for Linked Lists or external sorting where data doesn't fit in RAM."

## 11. Follow-ups
- "Why is Merge Sort better than Quick Sort for Linked Lists?" (Linked lists don't have random access, making Quick Sort's pivot swapping inefficient. Merge Sort easily splits linked lists and merges them by just changing pointers in $O(1)$ space).

## 12. Deeper questions
- "How does Merge Sort apply to External Sorting?" (If you have 100GB of data and 1GB of RAM, you chunk the data into 1GB files, sort them in RAM, and then stream them back using the Merge step of Merge Sort).

## 13. Related concepts
- **Count Inversions**: A classic hard interview problem solved by slightly modifying the Merge Sort merge step.
- **Divide and Conquer**: The overarching algorithmic paradigm.

## 14. When it breaks / Edge cases
- Fails in highly memory-constrained embedded environments due to the $O(N)$ space requirement.

## 15. Comparison with alternative approaches
- **vs Quick Sort:** Quick Sort is usually faster in practice (better cache locality) and uses $O(\\log N)$ space, but is unstable and has a worst-case of $O(N^2)$. Merge Sort is stable, strictly $O(N \\log N)$, but takes $O(N)$ space.

---
*Where this shows up in ML:* 
When training models on datasets too large to fit in RAM (e.g., shuffling terabytes of TFRecords), distributed systems use External Merge Sort to order and process the data chunks on disk.
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch A - Part 2 Complete")
