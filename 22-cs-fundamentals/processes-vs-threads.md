# Processes vs Threads

## 1. Key Differences
| | Process | Thread |
|--|---------|--------|
| Memory | Isolated address space | Shared address space |
| Creation | Expensive (fork) | Cheap |
| Context switch | Expensive | Cheaper |
| Communication | IPC required | Shared memory |
| Crash isolation | Yes | No (crashes whole process) |
| Python GIL | Not affected | Affected |

## 2. Process Creation (fork/exec)
```python
import os
pid = os.fork()
if pid == 0:
    # child
    os.execv('/usr/bin/ls', ['ls', '-la'])
else:
    # parent
    os.wait()
```

## 3. Python multiprocessing
Bypasses GIL. Each process has own Python interpreter.
```python
from multiprocessing import Process, Pool
def square(x): return x*x
with Pool(4) as p:
    results = p.map(square, range(10))
```
Good for: CPU-bound tasks (number crunching, image processing).

## 4. Python threading
GIL prevents true parallel execution for CPU-bound code.
I/O operations release the GIL → threads useful for I/O-bound tasks.
```python
import threading
def fetch(url): ...  # network call
threads = [threading.Thread(target=fetch, args=(u,)) for u in urls]
for t in threads: t.start()
for t in threads: t.join()
```

## 5. Python asyncio
Single-threaded concurrency via event loop. `async/await` — cooperative multitasking.
```python
import asyncio
import aiohttp
async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()
async def main():
    async with aiohttp.ClientSession() as s:
        tasks = [fetch(s, u) for u in urls]
        return await asyncio.gather(*tasks)
```

## 6. GIL — Global Interpreter Lock
CPython mutex ensuring only one thread executes Python bytecode at a time.
Released during I/O, C extensions (numpy), and `time.sleep`.
Does NOT protect against all race conditions (e.g., list.append is atomic but += is not).

## 7. When to Use What
| Scenario | Best Tool |
|----------|-----------|
| CPU-bound parallel | multiprocessing |
| I/O-bound (many requests) | asyncio |
| I/O-bound (blocking libs) | threading |
| Mixed workload | ProcessPool + asyncio |

## 8. Process vs Thread Memory
Processes use virtual memory with page tables — OS maps virtual→physical.
Copy-on-write (COW): fork shares memory pages until one side modifies.

## 9. Context Switch Cost
Thread: save/restore registers + stack pointer (~microseconds).
Process: additionally flush TLB, switch page tables (~more expensive).

## 10. Thread Safety
```python
import threading
lock = threading.Lock()
counter = 0
def increment():
    global counter
    with lock:
        counter += 1
```

## 11. Race Condition Example
```python
# UNSAFE: read-modify-write not atomic
counter += 1   # 3 bytecodes: LOAD, ADD, STORE — GIL can switch between them
```

## 12. Daemon Threads
Threads that die when main thread exits. Useful for background tasks.
`t.daemon = True; t.start()`

## 13. concurrent.futures — High-Level API
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
with ThreadPoolExecutor(max_workers=5) as ex:
    futures = [ex.submit(fetch, url) for url in urls]
    results = [f.result() for f in futures]
```

## 14. Interview Question: asyncio vs threading
asyncio: cooperative, single-threaded, explicit yield points (`await`), scales to thousands of connections, no race conditions.
threading: preemptive, multiple OS threads, need locks, simpler to retrofit blocking code.

## 15. Key Takeaways
- Use `multiprocessing` for CPU parallelism in Python.
- Use `asyncio` for high-concurrency I/O.
- GIL means threads don't help for CPU work.
- Threads still useful for blocking I/O with legacy libraries.
