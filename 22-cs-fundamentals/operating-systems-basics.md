# Operating Systems Basics

## 1. What is an OS?
Software layer between hardware and applications.
Manages CPU, memory, I/O, file system, and provides process isolation.

## 2. Kernel vs User Space
- **Kernel space**: privileged mode, direct hardware access, OS code runs here.
- **User space**: restricted mode, applications run here.
- System calls cross the boundary: `read()`, `write()`, `fork()`, `exec()`.

## 3. System Calls
Interface for user programs to request kernel services.
```c
// In Python, abstractions over syscalls:
open(), read(), write()     # file I/O
os.fork()                   # create process
socket(), connect(), send() # networking
```
Syscall: user → trap → kernel → return result.

## 4. Process
An instance of a running program. Has: PID, memory (code/data/stack/heap), open file descriptors, CPU registers state.
States: New → Ready → Running → Waiting → Terminated.

## 5. Thread
Lightweight unit of execution within a process. Shares memory/code/data of process. Has own stack and registers.

## 6. Scheduling Algorithms
Goal: maximize CPU utilization, minimize wait time and response time.

## 7. FCFS (First-Come-First-Served)
Non-preemptive. Convoy effect: short jobs stuck behind long ones.
Avg waiting time = sum of burst times of jobs ahead.

## 8. SJF (Shortest Job First)
Optimal average waiting time. Requires knowing burst time in advance (impractical). Can cause starvation of long jobs.

## 9. Round Robin
Each process gets a time quantum Q. If not done, preempted and queued at back.
- Small Q → many context switches (overhead).
- Large Q → degenerates to FCFS.
- Typically Q = 10–100ms.

## 10. Priority Scheduling
Each process has priority; highest priority runs first.
Problem: starvation → fix with aging (increase priority over time).

## 11. Multi-Level Queue / Feedback Queue
Multiple queues with different priorities and scheduling policies.
Processes can move between queues based on behavior (I/O vs CPU bound).

## 12. Context Switch
Save current process state (PCB: process control block), load next process state.
Cost: ~1–10 µs; pure overhead (no useful work done).

## 13. Inter-Process Communication (IPC)
- Pipes (unidirectional byte stream)
- Message queues
- Shared memory (fastest)
- Sockets (cross-machine)
- Signals (async notifications)

## 14. Deadlock Conditions (Coffman)
1. Mutual Exclusion, 2. Hold and Wait, 3. No Preemption, 4. Circular Wait.
Prevention: eliminate one condition. Detection: resource allocation graph.

## 15. Key Metrics
| Algorithm | Avg Wait | Starvation | Preemptive |
|-----------|----------|------------|------------|
| FCFS | High | No | No |
| SJF | Optimal | Yes | Optional |
| Round Robin | Medium | No | Yes |
| Priority | Varies | Yes | Optional |
