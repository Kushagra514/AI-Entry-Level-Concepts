# Concurrency Basics

## 1. Definition
Concurrency is the ability of a program to be broken into parts that can be executed out of order or in partial order, without affecting the final outcome. It allows multiple tasks to make progress seemingly at the same time.

## 2. Intuition
Imagine a chef cooking dinner. **Sequential:** Chop onions, then boil water, then cook pasta. Takes 30 mins. **Concurrent:** Put water on to boil, switch to chopping onions while waiting, switch to pasta when water boils. Takes 15 mins. The chef (CPU) is doing one thing at a time but switching contexts rapidly. **Parallel:** Two chefs, one chops while the other boils.

## 3. Why it exists
Modern computers have multiple cores, and external systems (network, disk) are slow. Without concurrency, a web server would completely freeze and ignore all users while waiting 500ms for a database query to return.

## 4. Mechanics
- **Race Condition:** Two threads read/write shared data simultaneously, leading to unpredictable results.
- **Mutex (Mutual Exclusion):** A lock. Only one thread can acquire it at a time. Used to protect Critical Sections (shared data).
- **Semaphore:** A signaling mechanism with a counter. A Binary Semaphore acts like a mutex. A Counting Semaphore allows $N$ threads to access a resource (like 5 DB connections in a pool).
- **Deadlock:** Thread A holds Lock 1, wants Lock 2. Thread B holds Lock 2, wants Lock 1. Both freeze forever.

## 5. Complexity (Time & Space)
- Adding locks decreases concurrency. If everything is locked, the program becomes sequential and slow. Lock contention (threads waiting for locks) wastes CPU cycles.

## 6. Tiny worked example
*Race Condition:* `balance = 10`. Thread 1 reads 10. Thread 2 reads 10. Thread 1 adds 5, writes 15. Thread 2 subtracts 5, writes 5. Final balance is 5, but it should be 10!
*Fix:* Thread 1 acquires `mutex`. Reads 10, writes 15, releases `mutex`. Thread 2 acquires `mutex`, reads 15, writes 10. Correct.

## 7. Code (Python)
```python
import threading

balance = 0
lock = threading.Lock() # Mutex

def increment():
    global balance
    for _ in range(100000):
        # Critical Section protected by lock
        with lock:
            balance += 1

threads = [threading.Thread(target=increment) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()

print(balance) # Always exactly 200000. Without lock, it would be random.
```

## 8. Common mistakes
- **Forgetting to release a lock:** If an exception occurs inside the critical section, the lock might never be released, deadlocking the system. Always use context managers (`with lock:`) or `try...finally`.
- **Livelock:** Threads constantly react to each other to avoid a deadlock, but never make progress (like two people in a hallway stepping side-to-side repeatedly to let the other pass).

## 9. 30-second interview answer
"Concurrency is the execution of multiple tasks over overlapping time periods. It introduces challenges like race conditions when shared data is accessed. We solve this using synchronization primitives like Mutexes to lock critical sections, or Semaphores to limit access to a pool of resources. A major pitfall is Deadlocks, where threads freeze while waiting for locks held by each other."

## 10. 2-minute interview answer
"Concurrency allows a system to handle multiple tasks simultaneously, which is critical for I/O bound systems like web servers. However, when multiple threads access the same memory space, we encounter Race Conditions—where the final output depends on the unpredictable timing of the OS scheduler. To guarantee atomicity, we use synchronization primitives. A Mutex is used to lock a Critical Section of code, ensuring only one thread executes it at a time. A Semaphore is used to manage a pool of resources, acting like a bouncer tracking how many slots are left. While locks prevent race conditions, they introduce the risk of Deadlocks. A deadlock occurs if four Coffman conditions are met: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. In modern systems design, we often try to avoid locks entirely by using message passing architectures (like Go's channels or Erlang's actors) where state is not shared, or by using Async/Await paradigms which rely on a single-threaded event loop to handle massive concurrency without race conditions."

## 11. Follow-ups
- "What's the difference between Concurrency and Parallelism?" (Concurrency is dealing with many things at once—structuring a program. Parallelism is doing many things at once—executing tasks simultaneously on multiple CPU cores).

## 12. Deeper questions
- "How do you prevent deadlocks?" (The easiest way is to eliminate the 'Circular Wait' condition by imposing a strict global ordering on locks. If every thread must acquire Lock A before Lock B, a deadlock between A and B is impossible).

## 13. Related concepts
- **Processes vs Threads**: Where concurrency happens.
- **AsyncIO**: Single-threaded concurrency.

## 14. When it breaks / Edge cases
- Priority Inversion: A low-priority thread holds a lock. A high-priority thread wants it and blocks. A medium-priority thread preempts the low-priority thread, effectively delaying the high-priority thread indefinitely. (Famously occurred on the Mars Pathfinder).

## 15. Comparison with alternative approaches
- **Shared Memory (Locks) vs Message Passing (Channels):** "Do not communicate by sharing memory; instead, share memory by communicating." Passing data through queues is often safer than locking shared variables.

---
*Where this shows up in ML:*
Asynchronous data loading, multi-threaded CPU inference, GPU kernel synchronization.
