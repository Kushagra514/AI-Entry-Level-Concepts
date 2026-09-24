# CS Fundamentals & OOP One-Page Revision

## Object-Oriented Programming (OOP) Pillars
1. **Encapsulation:** Bundling data (attributes) and methods together, restricting direct access (private variables) to prevent accidental interference.
2. **Abstraction:** Hiding complex implementation details and showing only essential features (e.g., Abstract Classes / Interfaces).
3. **Inheritance:** Creating new classes based on existing classes to promote code reuse.
4. **Polymorphism:** The ability of different classes to be treated as instances of the same class through a common interface. (e.g., overriding a `draw()` method in `Circle` and `Square`).

## SOLID Principles
- **S - Single Responsibility:** A class should have one, and only one, reason to change.
- **O - Open/Closed:** Software entities should be open for extension but closed for modification.
- **L - Liskov Substitution:** Objects of a superclass should be replaceable with objects of a subclass without breaking the program.
- **I - Interface Segregation:** Many client-specific interfaces are better than one general-purpose interface.
- **D - Dependency Inversion:** Depend upon abstractions, not concretions. (Pass interfaces into constructors, don't instantiate concrete classes inside).

## Operating Systems
- **Process vs Thread:** A Process is an executing program with its own memory space (heavyweight). A Thread is a unit of execution within a process; threads share the same memory space (lightweight).
- **Context Switch:** The OS saving the state of the CPU for one process/thread and loading the state for another. Expensive for processes, cheaper for threads.
- **Concurrency vs Parallelism:** Concurrency is dealing with many things at once (time-slicing on 1 core). Parallelism is doing many things at once (multi-core).
- **Deadlock:** Occurs when two or more threads are blocked forever, waiting for each other. (Conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait).

## Database Management Systems (DBMS)
- **ACID Properties:**
  - **Atomicity:** All or nothing. (Transaction succeeds completely or fails completely).
  - **Consistency:** Database moves from one valid state to another.
  - **Isolation:** Concurrent transactions don't interfere with each other.
  - **Durability:** Once committed, data is saved permanently even if power fails.
- **SQL vs NoSQL:** SQL is relational, structured, uses ACID, and scales vertically. NoSQL is document/key-value, unstructured, uses CAP theorem (often BASE: Basically Available, Soft state, Eventual consistency), and scales horizontally.
- **Indexing (B-Trees):** Creating a data structure (B-Tree or Hash) on a column to speed up reads from $O(N)$ to $O(\log N)$, at the cost of slower writes and extra storage.

## Networking
- **TCP vs UDP:** TCP is connection-oriented, reliable, orders packets, and has flow control (HTTP, SSH). UDP is connectionless, fast, no guaranteed delivery (Video streaming, DNS).
