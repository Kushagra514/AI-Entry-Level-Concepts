import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch E)"')

wc("22-cs-fundamentals/concurrency-basics.md", r"""# Concurrency Basics

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
""")

wc("22-cs-fundamentals/memory-management.md", r"""# Memory Management (Stack vs Heap, GC)

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
""")

wc("22-cs-fundamentals/indexing.md", r"""# Database Indexing

## 1. Definition
An index is a specialized data structure (typically a B-Tree or Hash Table) used by a database to quickly locate and access the data in a table, without having to scan every single row.

## 2. Intuition
An index in a database is exactly like an index at the back of a textbook. If you want to find information about "Transformers", you don't read the 1,000-page book from page 1 to 1,000 (a Full Table Scan). You look in the index, find "Transformers -> Page 450", and jump straight there.

## 3. Why it exists
As tables grow to millions of rows, a Full Table Scan (checking `WHERE email = 'a@b.com'` sequentially) becomes extremely slow ($O(N)$). Indexes reduce this lookup time to $O(\log N)$ or $O(1)$, which is the difference between a query taking 5 seconds and 5 milliseconds.

## 4. Mechanics
- **B-Tree Index (Balanced Tree):** The default for most relational databases. Keeps data sorted. Allows $O(\log N)$ point lookups (`=`) and range queries (`>`, `<`).
- **Hash Index:** Only allows exact matches (`=`) in $O(1)$ time. Cannot handle range queries.
- **Clustered Index:** Defines the physical sorting order of the data on the disk. There can be only ONE clustered index per table (usually the Primary Key).
- **Non-Clustered Index:** A separate structure that stores the indexed column and a pointer back to the actual data row. A table can have many non-clustered indexes.
- **Composite Index:** An index on multiple columns (e.g., `(last_name, first_name)`). Follows the *Leftmost Prefix Rule*: it can quickly search for `last_name`, or `last_name + first_name`, but CANNOT search efficiently for just `first_name`.

## 5. Complexity (Time & Space)
- **Time:** Search is $O(\log N)$. However, INSERT/UPDATE/DELETE operations become slower because the DB must update the index structure (rebalancing the tree) every time data changes.
- **Space:** Indexes consume additional disk space and RAM.

## 6. Tiny worked example
Table `Users` (1M rows). Query: `SELECT * FROM Users WHERE age = 30`.
Without index: DB reads all 1,000,000 rows, checks if `age == 30`.
With B-Tree index on `age`: DB traverses the tree. Root says "ages 1-50 go left". Next node says "ages 25-35 go right". Reaches the leaf node containing pointers for all 30-year-olds in 20 steps. Follows pointers to fetch data.

## 7. Code (Python)
```sql
-- Creating an index in SQL
CREATE INDEX idx_user_email ON Users(email);

-- Composite index
CREATE INDEX idx_last_first ON Users(last_name, first_name);

-- Analyzing if a query uses an index (Crucial debugging tool)
EXPLAIN SELECT * FROM Users WHERE email = 'test@test.com';
-- Output will say "Index Scan" instead of "Seq Scan" (Sequential Scan)
```

## 8. Common mistakes
- **Indexing every column:** This kills write performance. Every `INSERT` now has to update 15 different B-Trees. Only index columns heavily used in `WHERE`, `JOIN`, and `ORDER BY` clauses.
- **Violating the Leftmost Prefix Rule:** Having an index on `(country, city)` and writing `WHERE city = 'Paris'`. The DB cannot use the index because the leading column (`country`) is missing. It will do a full table scan.

## 9. 30-second interview answer
"Indexing is a performance tuning technique that uses specialized data structures—primarily B-Trees—to reduce query time from $O(N)$ full table scans to $O(\log N)$ lookups. A clustered index dictates the physical sorting of the table, while non-clustered indexes store pointers. While they drastically speed up read operations, they consume disk space and slow down write operations due to the overhead of updating the tree structure."

## 10. 2-minute interview answer
"Database indexing is the primary mechanism for optimizing query performance. The most common implementation is a B-Tree (specifically a B+ Tree). In a B+ Tree, the internal nodes contain routing keys, and all the actual data pointers sit in a linked list at the leaf level. This allows for extremely fast $O(\log N)$ lookups and highly efficient range scans (like `WHERE age BETWEEN 20 AND 30`) by traversing the linked leaves. There are two main types: Clustered and Non-Clustered. The Clustered index—usually the Primary Key—determines the actual physical order of the data on disk. You can only have one per table. Non-Clustered indexes are separate data structures pointing back to the physical rows. When designing indexes, you must balance reads and writes. Every index speeds up `SELECT` statements but adds overhead to `INSERT`, `UPDATE`, and `DELETE` operations because the B-Tree must be rebalanced. We also use Composite Indexes for multi-column queries, but they must be queried using the Leftmost Prefix Rule. To debug slow queries, we prepend `EXPLAIN` to the SQL statement to verify if the query optimizer is actually utilizing our indexes or falling back to a Sequential Scan."

## 11. Follow-ups
- "What happens if a Non-Clustered index doesn't contain all the columns requested in the SELECT statement?" (A "Bookmark Lookup" or "Key Lookup" occurs. The DB finds the row pointer in the index, then does an extra disk read to fetch the full row. If it contains all columns, it's a "Covering Index", which is much faster).

## 12. Deeper questions
- "Why use a B-Tree instead of a Binary Search Tree (BST) for databases?" (BSTs have 2 children per node, making them very deep. B-Trees can have hundreds of children per node, making them very shallow. Disk I/O is the main bottleneck; a shallow tree requires far fewer disk reads to reach the leaves).

## 13. Related concepts
- **DBMS Basics**: Where indexes live.
- **Vector Databases**: Use HNSW indexes instead of B-Trees for similarity search.

## 14. When it breaks / Edge cases
- **Cardinality:** Indexing a boolean column (e.g., `is_active`) is useless. If 50% of the table is True, the DB query optimizer will ignore the index and just do a Full Table Scan anyway, because the index overhead isn't worth it.

## 15. Comparison with alternative approaches
- **B-Tree vs Hash Index:** Hash is $O(1)$ but useless for `>` or `<`. B-Tree is $O(\log N)$ and handles ranges perfectly. RDBMS defaults to B-Tree.

---
*Where this shows up in ML:*
Optimizing analytical queries when preparing training data; understanding FAISS and vector indexing in RAG.
""")

wc("22-cs-fundamentals/normalization.md", r"""# Database Normalization

## 1. Definition
Normalization is the process of structuring a relational database in accordance with a series of so-called normal forms (1NF, 2NF, 3NF, etc.) to reduce data redundancy and improve data integrity.

## 2. Intuition
If you have a spreadsheet of orders and you write the customer's full address on every single order row, updating the customer's address means you have to update 50 different rows. If you miss one, the data is inconsistent. Normalization extracts the customer data into a separate table, so you only update it in one place.

## 3. Why it exists
To prevent Data Anomalies:
- **Update Anomaly:** Updating data in one place but forgetting to update duplicate data elsewhere.
- **Insertion Anomaly:** Being unable to add data because other data is missing (e.g., cannot add a new course to a university DB until a student enrolls in it).
- **Deletion Anomaly:** Deleting a row destroys unrelated data (e.g., deleting the last student in a course deletes the record of the course itself).

## 4. Mechanics
- **1NF (First Normal Form):** Atomic values. No arrays, lists, or comma-separated values in a single column. Every row must be unique (have a primary key).
- **2NF (Second Normal Form):** Must be in 1NF. No Partial Dependency. If the primary key is composite (e.g., `(Student_ID, Course_ID)`), non-key attributes (like `Student_Name`) must depend on the *entire* key, not just part of it. (Move `Student_Name` to a separate `Students` table).
- **3NF (Third Normal Form):** Must be in 2NF. No Transitive Dependency. Non-key attributes cannot depend on other non-key attributes. (If `ZipCode` determines `City`, move them to a `ZipCodes` table, don't keep `City` in the `Users` table).
- **BCNF (Boyce-Codd Normal Form):** A stricter version of 3NF addressing complex overlapping composite keys.

## 5. Complexity (Time & Space)
- **Space:** Decreases disk space by removing redundant data.
- **Time:** Slows down read queries because reconstructing the original data requires CPU-intensive `JOIN` operations.

## 6. Tiny worked example
*Unnormalized:* `Orders(OrderID, Item, User_Name, User_Address)`
*1NF:* Data is atomic, but `User_Address` repeats for every order.
*3NF:* 
Table `Users(UserID, Name, Address)`
Table `Orders(OrderID, Item, UserID_FK)`
Data is not redundant. Updating an address happens in exactly one place.

## 7. Code (Python)
```sql
-- Normalization requires creating tables with Foreign Keys

-- Users table (Handles the User concept)
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    zip_code VARCHAR(10)
);

-- Addresses table (Separated to satisfy 3NF, as ZipCode determines City/State)
CREATE TABLE ZipCodes (
    zip_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100),
    state VARCHAR(2)
);

-- Orders table (Uses Foreign Key to refer to User)
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    item_name VARCHAR(100),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
```

## 8. Common mistakes
- **Over-normalization:** Normalizing to 4NF or 5NF in a web application. This results in dozens of tiny tables, requiring massive 10-table JOINs for simple page loads, crushing performance. Most systems stop at 3NF.
- Assuming normalization is always the goal. In data warehouses and NoSQL, denormalization is preferred for read speed.

## 9. 30-second interview answer
"Normalization structures relational databases to eliminate data redundancy and prevent insertion, update, and deletion anomalies. The process follows normal forms: 1NF ensures atomic columns, 2NF eliminates partial dependencies on composite keys, and 3NF eliminates transitive dependencies between non-key columns. While it guarantees data integrity, it requires expensive JOIN operations to read data."

## 10. 2-minute interview answer
"Database Normalization is the foundational technique for schema design in relational databases. Its primary goal is to ensure data integrity by eliminating anomalies—situations where updating, inserting, or deleting data causes unintended inconsistencies because data is duplicated across rows. We achieve this by progressing through normal forms. First Normal Form (1NF) dictates that all columns hold atomic, indivisible values, forbidding lists or arrays in a cell. Second Normal Form (2NF) applies to tables with composite primary keys, demanding that all non-key columns depend on the entire composite key, removing partial dependencies. Third Normal Form (3NF) requires that non-key columns depend only on the primary key and not on other non-key columns, eliminating transitive dependencies. In practice, enterprise databases are usually normalized to 3NF. However, normalization is a tradeoff: it optimizes for write consistency and storage space at the expense of read latency, because queries now require complex JOINs. In read-heavy systems or analytics data warehouses (OLAP), we deliberately reverse this process—Denormalization—to speed up queries."

## 11. Follow-ups
- "What is Denormalization and when would you use it?" (Intentionally adding redundant data to a schema to improve read performance. Used in read-heavy applications, NoSQL databases, and Data Warehouses (Star Schema) to avoid slow JOINs).

## 12. Deeper questions
- "What's the difference between 3NF and BCNF?" (In 3NF, it's technically allowed for a part of the primary key to depend on a non-key attribute. BCNF strictly forbids this: for any dependency X -> Y, X must be a superkey. It's a stricter, edge-case version of 3NF).

## 13. Related concepts
- **DBMS Basics**: Joins and Foreign Keys make normalization possible.
- **SQL vs NoSQL**: NoSQL generally uses heavily denormalized data.

## 14. When it breaks / Edge cases
- Historical data records. If you normalize `Orders` to link to the `Products` table for the price, and the price changes next year, old orders will retroactively change value! You must denormalize and store the `price_at_purchase` directly in the `Order` row.

## 15. Comparison with alternative approaches
- **OLTP vs OLAP:** Online Transaction Processing (OLTP, like an app backend) is highly normalized. Online Analytical Processing (OLAP, like Snowflake) is denormalized for fast aggregate queries.

---
*Where this shows up in ML:*
Data engineering; preparing clean, denormalized flat files for model training from highly normalized production databases.
""")
print("Batch E Part 4 complete")
