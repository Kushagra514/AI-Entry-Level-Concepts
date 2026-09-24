# Processes vs. Threads

## 1. Definition
A **Process** is an independent executing program with its own isolated memory space. A **Thread** is a lightweight unit of execution within a process; multiple threads share the same memory space of their parent process.

## 2. Intuition
A **Process** is a house. It has its own address, its own fridge (memory), and locks on the doors. A **Thread** is a person living in the house. Multiple people (threads) can live in the same house (process), share the same fridge, and talk directly to each other, but they might bump into each other if they grab the same milk carton simultaneously.

## 3. Why it exists
Creating processes is slow and uses a lot of memory because the OS must allocate a brand new memory space. Threads allow for fast, lightweight concurrency. If a web server spawns a process per request, it will run out of RAM. If it spawns a thread, it scales to thousands of requests.

## 4. Mechanics
- **Process:** Heavyweight. Isolated memory. Communicates via Inter-Process Communication (IPC: pipes, sockets, message queues). Crashing does not affect other processes.
- **Thread:** Lightweight. Shared heap memory and open files, but has its own stack and registers. Communicates directly via shared variables. If one thread causes a segfault, the entire process (and all other threads) crashes.
- **Python GIL (Global Interpreter Lock):** In CPython, a mutex prevents multiple native threads from executing Python bytecodes simultaneously. Thus, Python threads do NOT run in true parallel on multiple CPU cores.

## 5. Complexity (Time & Space)
- Context switching between processes involves switching memory maps (TLB flush), which is expensive.
- Context switching between threads is much faster (only saving CPU registers).

## 6. Tiny worked example
You have a global variable `X = 0`.
If you spawn 2 **Processes** and both `X += 1`, they each modify their own isolated copy. Output: 1, 1.
If you spawn 2 **Threads** and both `X += 1`, they modify the shared variable. Output: 2 (if synchronized).

## 7. Code (Python)
```python
import multiprocessing
import threading

def worker(is_process):
    print(f"Running in {'Process' if is_process else 'Thread'}")

# Multi-processing (Bypasses GIL, true parallelism for CPU-bound tasks)
p = multiprocessing.Process(target=worker, args=(True,))
p.start()
p.join()

# Multi-threading (Blocked by GIL, good only for I/O-bound tasks)
t = threading.Thread(target=worker, args=(False,))
t.start()
t.join()
```

## 8. Common mistakes
- **Using Python Threads for CPU-bound tasks:** Due to the GIL, spawning 4 threads to do heavy math on a 4-core CPU will still only utilize 1 core (and might actually be slower due to context switching overhead). You MUST use `multiprocessing` for CPU-bound tasks in Python.
- Assuming thread safety. Modifying a shared dictionary from two threads simultaneously can cause race conditions.

## 9. 30-second interview answer
"A process is an isolated execution environment with its own memory space, while a thread is a lightweight execution unit that shares memory with other threads in the same process. Threads are faster to spawn and context-switch, but require synchronization (locks) to prevent race conditions. In Python, the GIL prevents threads from achieving true CPU parallelism, so we use multiprocessing for CPU-bound tasks and multithreading for I/O-bound tasks."

## 10. 2-minute interview answer
"The distinction between processes and threads is fundamental to concurrent programming. A process is a heavyweight OS primitive. When you start an application, the OS allocates an isolated virtual memory space. Because processes are isolated, they communicate using IPC mechanisms like pipes or sockets, making them highly fault-tolerant—a crash in one won't kill another. A thread, however, exists within a process. All threads in a process share the same heap memory, file descriptors, and code segment, though they maintain their own stack. This shared memory allows extremely fast communication, but introduces the danger of race conditions, requiring Mutexes or Semaphores for thread safety. In the context of Python, this distinction is critical because of the Global Interpreter Lock (GIL). The GIL ensures only one thread executes Python bytecode at a time. Therefore, Python threads are strictly for I/O-bound tasks (like making 100 API calls), where the thread releases the GIL while waiting for the network. For CPU-bound tasks (like matrix multiplication or model training), we must use the `multiprocessing` module to spawn separate processes, giving each its own GIL and achieving true multi-core parallelism."

## 11. Follow-ups
- "What is a Coroutine / Asyncio?" (A cooperative multitasking mechanism happening within a *single* thread. Functions explicitly yield control using `await`. It's even lighter than threads, perfect for massive I/O concurrency, e.g., FastAPI).

## 12. Deeper questions
- "How do processes communicate?" (IPC: Shared Memory mapping via `mmap`, Message Queues, Pipes, or local Sockets).

## 13. Related concepts
- **Concurrency & Locks**: Necessary because of threads.
- **Operating Systems**: The manager of these primitives.

## 14. When it breaks / Edge cases
- Deadlocks: Thread A locks Resource 1 and waits for Resource 2. Thread B locks Resource 2 and waits for Resource 1. Both freeze forever.

## 15. Comparison with alternative approaches
- **Multiprocessing vs Multithreading vs AsyncIO:**
  - Multiprocessing: CPU-bound (Data processing, ML training).
  - Multithreading: I/O-bound with blocking legacy code (File I/O).
  - AsyncIO: I/O-bound with modern non-blocking libraries (Web servers, APIs).

---
*Where this shows up in ML:*
PyTorch `DataLoader` uses multiprocessing (`num_workers=4`) to load batches in parallel on the CPU so the GPU doesn't starve waiting for data.
