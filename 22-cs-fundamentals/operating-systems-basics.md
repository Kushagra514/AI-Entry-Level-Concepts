# Operating Systems Basics

## 1. Definition
An Operating System (OS) is the system software that manages computer hardware, software resources, and provides common services for computer programs. It acts as an intermediary between users/applications and the hardware.

## 2. Intuition
Imagine a busy restaurant. The hardware is the kitchen (stoves, ingredients). The applications are the customers making orders. The OS is the Kitchen Manager—it decides which order gets cooked first (Scheduling), ensures cooks don't fight over the same pan (Concurrency), and makes sure there's enough space in the fridge (Memory Management).

## 3. Why it exists
Without an OS, every application would have to write its own drivers for the hard drive, manage its own RAM directly, and handle its own CPU execution. The OS abstracts these hardware details via a standard API (System Calls), providing security, stability, and multiplexing.

## 4. Mechanics
- **Kernel vs User Space:** The kernel is the core OS program with unrestricted hardware access (Ring 0). Applications run in restricted User Space (Ring 3). A transition requires a System Call (context switch).
- **CPU Scheduling:** Determines which process runs. Algorithms: FCFS (First Come First Serve), SJF (Shortest Job First), Round Robin (time slicing).
- **Virtual Memory:** Gives each process the illusion of having a massive, contiguous block of RAM by mapping virtual addresses to physical addresses using a Page Table.
- **File System:** Maps hierarchical paths (e.g., `/home/user/file.txt`) to physical blocks on a disk.

## 5. Complexity (Time & Space)
- Context switching (saving the state of one process and loading another) is computationally expensive, taking microseconds and invalidating CPU caches.

## 6. Tiny worked example
*System Call:* A Python script calls `print("Hello")`.
Python translates this to the C `write()` function.
`write()` triggers an interrupt (`INT 0x80` or `syscall`).
CPU switches to Kernel Mode.
Kernel executes the device driver for the terminal.
Kernel switches back to User Mode.

## 7. Code (Python)
```python
import os

# Interacting with the OS via system calls (wrapped by Python)
print(f"Current Process ID: {os.getpid()}")

# Forking creates an exact duplicate process at the OS level
pid = os.fork()
if pid == 0:
    print("I am the child process.")
else:
    print(f"I am the parent, created child {pid}.")
```

## 8. Common mistakes
- Confusing a program with a process. A program is a static file on disk (e.g., `chrome.exe`). A process is a running instance of that program in memory, with its own program counter and registers.
- Assuming User Space code can directly touch hardware. All hardware access (disk, network, screen) MUST go through a Kernel System Call.

## 9. 30-second interview answer
"An Operating System manages hardware resources and provides a stable abstraction layer for applications. Its core components are the Kernel (which handles privileged operations via system calls), the Scheduler (which multiplexes CPU time across processes), the Memory Manager (which uses virtual memory and paging to isolate applications), and the File System."

## 10. 2-minute interview answer
"The Operating System is the critical abstraction layer between software and hardware. The core of the OS is the Kernel, which runs in privileged mode. User applications run in restricted mode and must request hardware access—like reading a file or sending a network packet—via System Calls, which trigger a context switch. The OS has three main management duties. First, CPU Scheduling: the OS uses algorithms like Round Robin to rapidly switch the CPU between processes, creating the illusion of parallel multitasking. Second, Memory Management: the OS provides Virtual Memory, ensuring process isolation. Even if a process tries to access a restricted address, the Page Table will trigger a Segmentation Fault rather than corrupting another app's memory. Finally, Concurrency and Inter-Process Communication (IPC): because processes have isolated memory, the OS provides tools like pipes, sockets, and shared memory to allow them to communicate safely."

## 11. Follow-ups
- "What is a Context Switch?" (Saving the CPU registers, program counter, and state of the currently running process to its Process Control Block (PCB), and loading the state of the next process to run).

## 12. Deeper questions
- "What causes a Page Fault?" (When a process tries to access a memory page that is in its virtual address space but is currently swapped out to the hard disk. The OS pauses the process, loads the page from disk to RAM, and resumes).

## 13. Related concepts
- **Processes vs Threads**: The entities the OS schedules.
- **Concurrency**: Handled heavily by OS primitives (Mutexes, Semaphores).

## 14. When it breaks / Edge cases
- Thrashing: When RAM is full, the OS spends more time swapping pages in and out of the hard drive than actually executing code, causing the system to grind to a halt.

## 15. Comparison with alternative approaches
- **Monolithic vs Microkernel:** Monolithic (Linux) puts everything (drivers, file systems) in the kernel space for speed. Microkernel (macOS/Mach) keeps only the bare minimum in the kernel and runs drivers in user space for stability (if a driver crashes, the kernel doesn't panic).

---
*Where this shows up in ML:*
Understanding GPU context switching, out-of-memory (OOM) killer terminating training scripts, multiprocessing DataLoaders.
