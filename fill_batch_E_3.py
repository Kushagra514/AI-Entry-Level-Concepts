import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch E)"')

wc("22-cs-fundamentals/operating-systems-basics.md", r"""# Operating Systems Basics

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
""")

wc("22-cs-fundamentals/processes-vs-threads.md", r"""# Processes vs. Threads

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
""")

wc("22-cs-fundamentals/dbms-basics.md", r"""# DBMS Basics

## 1. Definition
A Database Management System (DBMS) is software designed to store, retrieve, define, and manage data in a database. Relational DBMS (RDBMS) organizes data into tables (rows and columns) linked by relationships.

## 2. Intuition
Instead of saving application data in hundreds of messy `.txt` or `.csv` files and writing custom Python scripts to search them, a DBMS is a highly optimized, central warehouse. You ask it questions in a standardized language (SQL), and it handles the complex file I/O, caching, and multi-user concurrency automatically.

## 3. Why it exists
Applications need data to persist after the server reboots. Without a DBMS, handling concurrent writes (two users buying the last ticket), ensuring data integrity (preventing partial bank transfers), and fast lookups would require millions of lines of custom code per application.

## 4. Mechanics
- **Tables, Rows, Columns:** The core structure of RDBMS.
- **Primary Key (PK):** A unique identifier for a row (e.g., `user_id`).
- **Foreign Key (FK):** A column that references the PK of another table, establishing a relationship (e.g., `order.user_id` -> `user.user_id`).
- **Transactions:** A sequence of operations treated as a single logical unit of work (all succeed or all fail).
- **Joins:** Combining rows from two or more tables based on a related column.

## 5. Complexity (Time & Space)
- Relational databases scale vertically well but struggle with horizontal scaling (sharding) due to the complexity of maintaining joins and ACID properties across distributed servers.

## 6. Tiny worked example
*Inner Join:*
Table `Users`: `(1, Alice), (2, Bob)`
Table `Orders`: `(100, $50, user_id=1)`
`SELECT Users.name, Orders.amount FROM Users JOIN Orders ON Users.id = Orders.user_id;`
Result: `(Alice, $50)` (Bob is excluded because he has no orders).

## 7. Code (Python)
```sql
-- Core SQL concepts
CREATE TABLE Users (
    id INT PRIMARY KEY,
    email VARCHAR(255) UNIQUE
);

CREATE TABLE Orders (
    id INT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Transaction example
BEGIN TRANSACTION;
UPDATE Accounts SET balance = balance - 100 WHERE id = 1;
UPDATE Accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- If crash happens before COMMIT, changes roll back.
```

## 8. Common mistakes
- **N+1 Query Problem:** Fetching a list of $N$ users, then running a separate `SELECT` query in a loop to fetch the orders for each user. This hits the database $N+1$ times. Fix: Use a single `JOIN` query.
- Storing calculated/derived data (like `total_order_amount`) in the user table instead of calculating it on the fly, leading to data inconsistencies when an order is deleted.

## 9. 30-second interview answer
"A DBMS manages persistent data storage. Relational databases organize data into tables, using Primary Keys for identity and Foreign Keys for relationships. They provide SQL for declarative querying, support complex Joins to combine data, and guarantee ACID properties for transactions, ensuring data integrity even during crashes or high concurrency."

## 10. 2-minute interview answer
"A Database Management System is the persistence layer of almost all software. The dominant paradigm is the Relational model (PostgreSQL, MySQL), which enforces strict schemas using tables, rows, and columns. Relationships are established via Foreign Keys, ensuring Referential Integrity (you can't have an order for a user that doesn't exist). To retrieve data across these entities, we use JOIN operations—Inner Joins for intersections, and Left Joins to include unmatched records. A critical feature of a DBMS is the Transaction, which guarantees ACID properties. If a system crashes halfway through a bank transfer, the DBMS ensures the database isn't left in an inconsistent state; it rolls back the uncommitted transaction using the Write-Ahead Log (WAL). While Relational databases are exceptional at data integrity and complex queries, they scale vertically. In modern system design, if the data is highly unstructured or requires massive horizontal scaling across commodity hardware, we often look to NoSQL databases, trading some ACID guarantees for availability and partition tolerance."

## 11. Follow-ups
- "What is a Left Join vs an Inner Join?" (Inner join only returns rows with a match in both tables. Left join returns ALL rows from the left table, with `NULL` for the right table columns if there is no match).

## 12. Deeper questions
- "What is the Write-Ahead Log (WAL)?" (Before a database modifies actual data files on disk, it appends the change to a sequential log file. If power fails, the DB reads the WAL on reboot to redo committed transactions and undo uncommitted ones).

## 13. Related concepts
- **ACID**: The guarantees a transaction provides.
- **Indexing**: How the DBMS finds data fast.
- **Normalization**: How to design the tables.

## 14. When it breaks / Edge cases
- Deadlocks in databases occur when Transaction A locks Row 1 and needs Row 2, while Transaction B locks Row 2 and needs Row 1. The DBMS will detect this and automatically kill/abort one of the transactions.

## 15. Comparison with alternative approaches
- **RDBMS vs NoSQL:** RDBMS is for structured data requiring strong integrity and complex queries (finance, ecommerce). NoSQL is for unstructured, rapidly scaling, or document-based data (social media feeds, logging).

---
*Where this shows up in ML:*
Feature stores, querying datasets for training, understanding vector databases (which are specialized DBMS for AI).
""")

wc("22-cs-fundamentals/sql-vs-nosql.md", r"""# SQL vs NoSQL

## 1. Definition
**SQL (Relational):** Databases (PostgreSQL, MySQL) that store data in structured tables with strict schemas and relationships.
**NoSQL (Non-Relational):** Databases (MongoDB, Cassandra, Redis) that store data in flexible formats like JSON documents, key-value pairs, wide-columns, or graphs.

## 2. Intuition
- **SQL** is a spreadsheet with strict rules. If a column is "Integer", you cannot put a word there. If you want to add a "Middle Name" column, you have to alter the whole table.
- **NoSQL** is a folder full of word documents. One document can have 3 fields, the next can have 10 fields. It's totally flexible.

## 3. Why it exists
SQL databases were designed in the 1970s when storage was expensive, requiring data deduplication (normalization). They scale *vertically* (buying a bigger server). In the 2000s, web-scale companies needed databases that could scale *horizontally* across thousands of cheap servers. NoSQL emerged by relaxing strict ACID constraints to achieve massive distributed scale (CAP Theorem).

## 4. Mechanics
- **Schema:** SQL is rigid (schema-on-write). NoSQL is flexible (schema-on-read).
- **Scaling:** SQL scales Vertically. NoSQL scales Horizontally (sharding is built-in).
- **Relations:** SQL uses JOINs. NoSQL typically denormalizes data (nesting related data inside the same document) because distributed JOINs are terribly slow.
- **NoSQL Types:**
  - *Document:* MongoDB (JSON objects).
  - *Key-Value:* Redis, DynamoDB (Fast lookups, caching).
  - *Wide-Column:* Cassandra (Time-series, heavy writes).
  - *Graph:* Neo4j (Social networks, recommendation engines).

## 5. Complexity (Time & Space)
- Distributed NoSQL systems replicate data across nodes. They trade immediate consistency (Time) for high availability.

## 6. Tiny worked example
*SQL (Requires 2 tables + JOIN):*
Table Users: `id: 1, name: John`
Table Addresses: `user_id: 1, city: NY`

*NoSQL (Document DB - nested data):*
```json
{
  "_id": 1,
  "name": "John",
  "address": {"city": "NY"}
}
```

## 7. Code (Python)
```python
# SQL Approach (psycopg2)
cursor.execute("SELECT u.name, a.city FROM users u JOIN addresses a ON u.id = a.user_id")

# NoSQL Approach (MongoDB / pymongo)
# Data is already nested, fetch in one call, no JOIN needed
user = db.users.find_one({"_id": 1}) 
print(user["name"], user["address"]["city"])
```

## 8. Common mistakes
- **Treating MongoDB like PostgreSQL:** Trying to build a highly normalized schema with manual document references in NoSQL, essentially performing "application-level joins." In NoSQL, data that is read together should be stored together (nested).
- Assuming NoSQL means "no ACID." Modern NoSQL databases (like MongoDB 4.0+) support multi-document ACID transactions, though they come with a performance penalty.

## 9. 30-second interview answer
"SQL databases are relational, schema-rigid, scale vertically, and rely on ACID properties and JOINs—best for complex queries and financial data. NoSQL databases are non-relational, schema-flexible, and scale horizontally across distributed clusters. NoSQL databases usually denormalize data to avoid JOINs and are best for unstructured data, rapid iteration, and massive scale."

## 10. 2-minute interview answer
"The choice between SQL and NoSQL comes down to schema flexibility, scaling, and the CAP theorem. SQL databases (like Postgres) enforce strict schemas, ensuring data integrity. They use normalization to reduce redundancy and rely on JOINs for querying. However, they are fundamentally designed to run on a single machine, meaning they scale vertically. When data volume exceeds what one server can handle, SQL becomes a bottleneck. NoSQL databases (like MongoDB or Cassandra) were built for horizontal scalability. They relax the rigid table structure, storing data as JSON documents, Key-Value pairs, or Wide-Columns. Because data is distributed across many nodes, NoSQL systems usually denormalize data—nesting an address inside a user document—so that a single read operation retrieves all necessary data without requiring a slow, distributed JOIN. Under the CAP theorem, distributed NoSQL databases often trade strong Consistency for high Availability and Partition tolerance, utilizing 'eventual consistency'. I would choose SQL for a billing system, and NoSQL for a massive IoT telemetry stream or an evolving product catalog."

## 11. Follow-ups
- "What is the CAP Theorem?" (In a distributed data store, you can only guarantee two out of three: Consistency (all nodes see the same data), Availability (every request receives a response), and Partition Tolerance (system works despite network drops). Because network partitions are inevitable, you must choose between CP and AP).

## 12. Deeper questions
- "What is Eventual Consistency?" (If you update a profile picture on Node A, it might take 2 seconds to replicate to Node B. If a friend reads from Node B immediately, they see the old picture. Eventually, all nodes converge to the same state. Standard in NoSQL).

## 13. Related concepts
- **Normalization**: The standard for SQL.
- **ACID**: The standard for SQL transactions.

## 14. When it breaks / Edge cases
- If you use NoSQL for a highly connected social network, you will struggle to query relationships (e.g., "Friends of friends who like Pizza"). You should use a Graph Database (Neo4j) instead.

## 15. Comparison with alternative approaches
- **NewSQL:** A newer category (e.g., CockroachDB, Spanner) that provides the horizontal scalability of NoSQL but retains the strict ACID guarantees and relational structure of SQL.

---
*Where this shows up in ML:*
Storing model telemetry and logs (NoSQL/ElasticSearch). Managing training datasets metadata (SQL).
""")
print("Batch E Part 3 complete")
