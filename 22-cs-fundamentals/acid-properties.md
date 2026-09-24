# ACID Properties

## 1. Definition
ACID is a set of four properties—Atomicity, Consistency, Isolation, Durability—that guarantee database transactions are processed reliably, even in the event of errors, power failures, or concurrent access.

## 2. Intuition
Imagine a $100 bank transfer from Alice to Bob.
- **Atomicity:** It's all or nothing. We don't take money from Alice and fail to give it to Bob.
- **Consistency:** Alice + Bob's total money must be exactly the same before and after. No money vanishes.
- **Isolation:** If Charlie transfers money to Alice at the exact same millisecond, the DB handles them sequentially, avoiding math errors.
- **Durability:** Once the bank says "Transfer Complete," it's saved. If the power cuts 1 second later, the data isn't lost.

## 3. Why it exists
Financial systems, inventory management, and healthcare data cannot tolerate partial updates, race conditions, or lost data. ACID properties ensure that developers don't have to write complex failure-recovery and concurrency-locking code into every application.

## 4. Mechanics
- **Atomicity:** Managed by the transaction manager. Uses rollback logs. If an error occurs before `COMMIT`, everything is rolled back.
- **Consistency:** Managed by DB constraints (Foreign Keys, `UNIQUE`, `CHECK > 0`). The transaction is aborted if it violates rules.
- **Isolation:** Managed by concurrency control (Locks, MVCC - Multi-Version Concurrency Control). Prevents "Dirty Reads" (reading uncommitted data) or "Phantom Reads".
- **Durability:** Managed by the Write-Ahead Log (WAL). Data is written to a sequential disk log before it's written to the actual DB files. If power fails, the DB replays the WAL on reboot.

## 5. Complexity (Time & Space)
- Guaranteeing Isolation (especially the highest level: Serializable) causes major performance bottlenecks as concurrent transactions must wait in line for locks.

## 6. Tiny worked example
```sql
BEGIN TRANSACTION;
UPDATE Accounts SET balance = balance - 100 WHERE name = 'Alice';
-- Power outage happens here!
-- Atomicity ensures Alice's balance reverts to original value on reboot.
-- Without it, Alice lost 100, Bob got nothing.
UPDATE Accounts SET balance = balance + 100 WHERE name = 'Bob';
COMMIT;
```

## 7. Code (Python)
```python
import psycopg2

conn = psycopg2.connect(dsn)
# In Python DB-API, a transaction starts automatically
try:
    with conn.cursor() as cur:
        cur.execute("UPDATE inventory SET qty = qty - 1 WHERE item_id = 5")
        cur.execute("INSERT INTO orders (item_id, user) VALUES (5, 'John')")
    # Both succeeded: Durability & Atomicity guaranteed after commit
    conn.commit() 
except Exception as e:
    # Something failed (e.g. qty < 0 violating Consistency)
    # Atomicity guarantees the inventory update is reverted
    conn.rollback() 
```

## 8. Common mistakes
- Confusing the 'C' in ACID (Consistency) with the 'C' in CAP Theorem (Consistency). In ACID, it means "Data conforms to schema rules/constraints." In CAP, it means "All distributed nodes return the exact same data."
- Using `Serializable` isolation level everywhere. It guarantees perfect isolation but destroys concurrency performance. Most databases default to `Read Committed`.

## 9. 30-second interview answer
"ACID defines the guarantees of database transactions. Atomicity ensures transactions are 'all or nothing'. Consistency ensures data always satisfies schema constraints. Isolation ensures concurrent transactions don't interfere with each other, preventing race conditions. Durability uses Write-Ahead Logging to ensure committed transactions survive system crashes. These properties are the cornerstone of Relational Databases."

## 10. 2-minute interview answer
"ACID properties are the bedrock of reliable transaction processing in databases like PostgreSQL. Atomicity guarantees that a multi-step transaction is treated as a single unit; if one step fails, the entire transaction rolls back, preventing partial states. Consistency guarantees the transaction transitions the database from one valid state to another, strictly enforcing constraints like Foreign Keys or unique indexes. Isolation is the most complex property, dealing with concurrency. It ensures that multiple simultaneous transactions don't corrupt each other. Databases implement varying isolation levels—from 'Read Uncommitted' (fastest but allows dirty reads) up to 'Serializable' (perfect isolation, implemented via strict locking or MVCC, but heavily impacts throughput). Finally, Durability guarantees that once a transaction returns a success message, the data is permanent. This is typically achieved using a Write-Ahead Log (WAL), where changes are sequentially appended to a disk log before the actual data pages are modified, allowing the database to rebuild state if power is lost."

## 11. Follow-ups
- "What is MVCC (Multi-Version Concurrency Control)?" (A lock-free way to implement Isolation. Instead of locking a row during an update, the DB creates a new version of the row. Readers read the old version, writers write the new version, so 'readers don't block writers').

## 12. Deeper questions
- "What is the difference between a Dirty Read and a Phantom Read?" (Dirty read: reading data from an uncommitted transaction that might get rolled back. Phantom read: running `SELECT count(*)` twice in a transaction, and a concurrent transaction inserts a new row in between, changing the count).

## 13. Related concepts
- **DBMS Basics**: The system that implements ACID.
- **SQL vs NoSQL**: NoSQL often relaxes ACID (using BASE) to scale.

## 14. When it breaks / Edge cases
- Distributed Transactions: Guaranteeing ACID across multiple microservices or distributed databases requires complex, slow algorithms like Two-Phase Commit (2PC).

## 15. Comparison with alternative approaches
- **ACID vs BASE:** RDBMS uses ACID (Strong consistency). NoSQL uses BASE (Basically Available, Soft state, Eventual consistency). BASE trades strict correctness for massive scalability and speed.

---
*Where this shows up in ML:*
Irrelevant for training models, but critical for ML deployment (e.g., deducting user credits for API inference must be an ACID transaction).
