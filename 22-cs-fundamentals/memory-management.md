# Memory Management

## 1. Memory Layout of a Process
```
High address
┌───────────────┐
│  Stack        │ ← grows downward (function calls, local vars)
├───────────────┤
│  ↓         ↑  │
│  Heap         │ ← grows upward (dynamic allocation)
├───────────────┤
│  BSS          │ ← uninitialized globals
├───────────────┤
│  Data         │ ← initialized globals
├───────────────┤
│  Text (Code)  │ ← read-only
Low address
```

## 2. Stack
- Automatic allocation/deallocation (LIFO).
- Fixed size (typically 1–8 MB).
- Stack overflow: infinite recursion, huge local arrays.
- Fast: just move stack pointer.

## 3. Heap
- Manual (C: malloc/free) or GC-managed (Python, Java).
- Slower: needs allocator to find free block.
- Fragmentation: internal (wasted inside allocated block) and external (free blocks scattered).

## 4. Garbage Collection Strategies
| Strategy | How | Used By |
|----------|-----|---------|
| Reference counting | Count references, free at 0 | Python (primary), Swift |
| Mark-and-sweep | Mark reachable, sweep rest | Python (cycles), Go |
| Generational GC | Separate young/old objects | Java, Python |
| Tracing GC | Trace from roots | JVM, V8 |

## 5. Python's Reference Counting
```python
import sys
a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount arg)
b = a
print(sys.getrefcount(a))  # 3
del b
# refcount drops; if 0, memory freed immediately
```

## 6. Cyclic Reference Problem
```python
a = []
a.append(a)   # a refers to itself; refcount never reaches 0
# Python's cyclic GC (gc module) handles this
```

## 7. Python's gc Module
```python
import gc
gc.collect()          # manually trigger cycle collection
gc.disable()          # disable automatic GC (for performance-critical sections)
gc.get_count()        # (gen0, gen1, gen2) counts
```
Generational: objects that survive GC are promoted to older generations.

## 8. Memory Leaks
Causes: forgotten references, event listeners not removed, circular references without GC, caches that grow unbounded.
```python
# Common Python leak: class-level mutable default
class Foo:
    items = []   # shared across ALL instances!
    def add(self, x): self.items.append(x)  # leaks
```

## 9. Memory Profiling in Python
```python
# memory_profiler
from memory_profiler import profile
@profile
def my_func(): ...

# tracemalloc
import tracemalloc
tracemalloc.start()
# ... code ...
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics('lineno')[:5]: print(stat)
```

## 10. Stack vs Heap — Python Specifics
Everything in Python is a heap object (even integers). Stack only holds frame pointers and local variable references.
`sys.setrecursionlimit(n)` controls Python stack depth (default 1000).

## 11. Virtual Memory
OS gives each process an illusion of large contiguous address space.
Pages (4KB) swapped between RAM and disk. Page fault → OS loads page from disk (slow!).

## 12. Memory Allocators
CPython uses its own allocator on top of malloc: PyMalloc for objects <512 bytes (pool-based, reduces fragmentation).

## 13. WeakRef — Avoid Cycles
```python
import weakref
class Node:
    def __init__(self): self.parent = None
node = Node()
ref = weakref.ref(node)   # doesn't increase refcount
```

## 14. Common Interview Questions
- What is a memory leak? How do you find it in Python?
- Explain stack overflow vs heap overflow.
- How does Python's GC work?
- Why is reference counting insufficient alone?

## 15. Key Facts
- Stack: fast, LIFO, size-limited, automatic.
- Heap: flexible, GC or manual, can fragment.
- Python: refcounting + cyclic GC + generational collection.
- `del x` doesn't guarantee memory freed — only decrements refcount.
