# Concurrency Basics

## 1. Concurrency vs Parallelism
- **Concurrency**: multiple tasks in progress at the same time (interleaved execution).
- **Parallelism**: multiple tasks running simultaneously (multi-core).
- asyncio is concurrent but not parallel. multiprocessing is both.

## 2. Race Condition
Outcome depends on order of thread/process execution.
```python
# Thread 1: x = x + 1
# Thread 2: x = x + 1
# Both read x=5, both write 6 → lost update
```

## 3. Mutex (Mutual Exclusion Lock)
Only one thread holds it at a time. Others block.
```python
lock = threading.Lock()
with lock:         # acquire on enter, release on exit
    shared_var += 1
```

## 4. Semaphore
Allows N concurrent accesses (generalized mutex where N=1).
```python
sem = threading.Semaphore(3)   # max 3 concurrent threads
with sem:
    access_db()
```

## 5. Condition Variable
Thread waits for a condition to become true.
```python
cond = threading.Condition()
# Producer
with cond:
    queue.append(item); cond.notify()
# Consumer
with cond:
    cond.wait_for(lambda: len(queue) > 0)
    item = queue.pop()
```

## 6. Deadlock
Two threads each hold a lock the other needs.
```python
# Thread 1: lock_a.acquire(); lock_b.acquire()
# Thread 2: lock_b.acquire(); lock_a.acquire()  → deadlock
```
Prevention: always acquire locks in the same order.

## 7. Livelock
Threads keep responding to each other without making progress (like two people dodging each other in a corridor).

## 8. Starvation
A thread is perpetually denied access to a resource because others keep acquiring it first. Fix: fair queuing (FIFO lock).

## 9. Python asyncio Concurrency Model
Event loop + coroutines. `await` yields control back to event loop.
```python
async def main():
    await asyncio.sleep(1)     # yields; loop can run other coroutines
    result = await some_io()
asyncio.run(main())
```

## 10. asyncio Primitives
```python
asyncio.Lock()        # async mutex
asyncio.Semaphore(n)  # async semaphore
asyncio.Event()       # set/wait
asyncio.Queue()       # async producer-consumer
```

## 11. Producer-Consumer Pattern
```python
q = asyncio.Queue()
async def producer():
    for i in range(5): await q.put(i); await asyncio.sleep(0.1)
async def consumer():
    while True:
        item = await q.get(); process(item); q.task_done()
```

## 12. Atomic Operations in Python
`list.append()`, `dict[k]=v` are GIL-atomic (single bytecode).
`counter += 1` is NOT atomic (LOAD, ADD, STORE).
Use `threading.Lock` or `queue.Queue` for safe sharing.

## 13. Thread Pool Pattern
```python
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as pool:
    futures = [pool.submit(task, arg) for arg in args]
    results = [f.result() for f in futures]
```

## 14. Common Concurrency Bugs
| Bug | Cause | Fix |
|-----|-------|-----|
| Race condition | Unsynchronized access | Lock |
| Deadlock | Circular lock acquisition | Lock ordering |
| Livelock | Reactive but no progress | Random backoff |
| Starvation | Unfair scheduling | Fair queue |
| Memory visibility | CPU caching | Memory barriers / lock |

## 15. Interview Tips
- Draw thread execution timeline to illustrate race conditions.
- Know difference: mutex vs semaphore vs condition variable.
- Explain GIL → why multiprocessing for CPU, asyncio for I/O.
- asyncio scales to 10k+ connections; threading saturates at ~100s.
