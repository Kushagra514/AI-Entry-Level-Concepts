# Memory Management (Stack vs Heap, GC)

## 1. Definition
Memory Management is how an operating system or runtime environment allocates computer memory to a program during execution, and frees it when no longer needed.

## 2. Intuition
- **Stack Memory:** Like a stack of plates. Fast, organized, automatically managed. Used for local variables and function calls. When the function returns, the plate is removed.
- **Heap Memory:** Like a massive warehouse. Unorganized, dynamic. You have to ask the manager for a specific size box, remember where you put it, and explicitly throw it away when done.

## 3. Why it exists
A program needs to store data. If it knows exactly how much data it needs at compile time, it uses the Stack. If data grows dynamically at runtime (like an array of user inputs or a massive ML model), it must request space in the Heap.

## 4. Mechanics
- **Stack:** LIFO structure. Very fast allocation (just moving a pointer). Size is fixed and small (often 8MB). Causes `StackOverflowError` if you recurse too deeply.
- **Heap:** Large, dynamic pool. Allocation is slower (OS must find contiguous free blocks). Must be managed manually (C/C++ `malloc`/`free`) or by a Garbage Collector (Python/Java).
- **Garbage Collection (GC):**
  - *Reference Counting:* Every object counts how many variables point to it. If count hits 0, it is deleted. (Python uses this heavily).
  - *Tracing / Mark-and-Sweep:* Starts from root variables, traverses all references, marks everything it can reach, and sweeps (deletes) everything it cannot reach. Handles circular references.

## 5. Complexity (Time & Space)
- Manual memory management (C++) has zero runtime overhead but causes human errors (memory leaks). GC has significant runtime overhead (pausing the program to sweep) but ensures safety.

## 6. Tiny worked example
```python
def foo():
    x = 10 # 'x' (the integer 10) is a small, fixed size. Placed on Stack.
    y = [1, 2, 3] # The list can grow dynamically. Placed on Heap. 
    # 'y' on the Stack is just a pointer to the Heap memory.
# When foo() ends, 'x' and pointer 'y' are popped off the stack. 
# The list has 0 references, so the Garbage Collector deletes it from the Heap.
```

## 7. Code (Python)
```python
import sys
import gc

# Reference counting in action
a = []
print(sys.getrefcount(a)) # 2 (referenced by 'a' and by getrefcount's argument)

b = a
print(sys.getrefcount(a)) # 3 (referenced by 'a', 'b', and argument)

# Circular reference (A -> B, B -> A)
class Node: pass
n1 = Node()
n2 = Node()
n1.child = n2
n2.parent = n1

del n1
del n2
# Reference count never hits 0! Python's cyclic GC will detect and clean this up later.
gc.collect() 
```

## 8. Common mistakes
- **Memory Leaks in GC languages:** Assuming GC prevents all memory leaks. If you keep appending objects to a global list and never clear the list, the objects retain active references and will never be collected, crashing the server over time.
- **Stack Overflow:** Writing a recursive function without a proper base case, exceeding the small stack size limit.

## 9. 30-second interview answer
"Memory is primarily divided into the Stack and the Heap. The Stack is for static memory allocation, local variables, and function calls; it is fast and managed automatically by the CPU pointer. The Heap is for dynamic, runtime allocation; it is larger, slower, and managed via pointers. In languages like C, Heap memory must be freed manually. In Python or Java, a Garbage Collector automatically frees Heap memory when objects have zero references or become unreachable."

## 10. 2-minute interview answer
"Program memory is segmented into the Stack and the Heap. The Stack operates strictly LIFO, storing function frames and local variables. It is incredibly fast because allocating memory just involves moving a stack pointer, but its size is strictly limited, leading to Stack Overflows in deep recursion. The Heap is a vast region for dynamic allocation—used when data structures need to grow at runtime or persist across function calls. When you create an object, the object lives on the Heap, and a pointer to it lives on the Stack. Managing the Heap is complex. In C++, developers must manually `malloc` and `free` memory, which risks memory leaks or dangling pointers. Modern languages use Garbage Collection. Python primarily uses Reference Counting: every object tracks how many pointers target it, destroying itself immediately when the count reaches zero. Because reference counting fails on circular references (A points to B, B points to A), Python also runs a generational Mark-and-Sweep garbage collector periodically to find and destroy isolated cyclic islands."

## 11. Follow-ups
- "What is a Memory Leak?" (When memory is allocated on the heap but the program loses the pointer to it before freeing it, or when objects are held in global scope unintentionally, causing RAM usage to grow indefinitely).

## 12. Deeper questions
- "What is Memory Fragmentation?" (As the heap allocates and frees blocks of different sizes, free memory becomes scattered in tiny chunks. You might have 100MB free, but if it's in 1MB chunks, you cannot allocate a 10MB array. Solved by compacting garbage collectors).

## 13. Related concepts
- **Pointers**: Variables that hold memory addresses on the heap.
- **Operating Systems**: The OS provides virtual memory to the process heap.

## 14. When it breaks / Edge cases
- Pauses: Tracing Garbage Collectors often have to "Stop the World" (freeze the entire application) to safely traverse the memory graph. This ruins low-latency trading or real-time gaming.

## 15. Comparison with alternative approaches
- **GC vs Rust Ownership:** Rust guarantees memory safety without a garbage collector by enforcing strict compiler rules (Ownership and Borrowing) dictating exactly when memory should be freed at compile time, yielding C++ speed with Java safety.

---
*Where this shows up in ML:*
PyTorch memory management. Tensors sit on the GPU heap. If you store history for loss tracking (`losses.append(loss)` instead of `loss.item()`), you retain the entire massive computation graph in memory, causing an OOM error.
