# ACID Properties

## 1. Overview
ACID = Atomicity, Consistency, Isolation, Durability.
Guarantees database transactions are processed reliably.

## 2. Atomicity
All operations in a transaction succeed, or ALL are rolled back. No partial updates.
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- If second UPDATE fails, first is also rolled back
COMMIT;
```
Implementation: Undo Log / Rollback Segments.

## 3. Consistency
Transaction brings DB from one valid state to another. All integrity constraints maintained.
Example: if balance cannot go negative (CHECK constraint), transaction violating this is rolled back.
Note: Consistency is partly guaranteed by the application (business rules) + DB constraints.

## 4. Isolation
Concurrent transactions execute as if serialized. Intermediate state is invisible to others.
```sql
-- Without isolation:
T1 reads balance=100; T2 reads balance=100
T1 deducts 50 → 50; T2 deducts 50 → 50; both commit
-- Final balance: 50 instead of 0 → lost update
```

## 5. Durability
Once committed, data survives system failures (crash, power loss).
Implementation: Write-Ahead Logging (WAL) — changes written to log before disk pages.
On crash recovery, replay WAL.

## 6. Isolation Levels
```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;  -- PostgreSQL default
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;    -- strictest
```

## 7. Read Anomalies
| Anomaly | Description |
|---------|-------------|
| Dirty Read | Read uncommitted data from another transaction |
| Non-Repeatable Read | Same row read twice gives different values |
| Phantom Read | Same query returns different set of rows |
| Lost Update | Two transactions overwrite each other |

## 8. Read Uncommitted
Lowest isolation. Allows dirty reads. Rarely used; no locks on reads.

## 9. Read Committed
Default in PostgreSQL. No dirty reads. Re-reads can see committed changes by others (non-repeatable reads).

## 10. Repeatable Read
Snapshot of DB at transaction start. Same rows read twice → same result.
Prevents dirty + non-repeatable reads. Phantoms still possible (in MySQL, InnoDB uses gap locks to prevent).

## 11. Serializable
Strictest. Transactions appear to execute serially. Implemented via:
- Two-Phase Locking (2PL)
- Serializable Snapshot Isolation (SSI) in PostgreSQL

## 12. MVCC (Multi-Version Concurrency Control)
PostgreSQL and MySQL InnoDB use MVCC: readers don't block writers and vice versa.
Each transaction sees a snapshot. Old versions kept until no longer needed.

## 13. WAL (Write-Ahead Log)
```
Before any data page is modified on disk:
1. Log record written to WAL (durable)
2. Data page updated in memory (buffer pool)
3. Data page flushed to disk lazily

On crash: replay WAL → recover committed changes.
```

## 14. BASE vs ACID (NoSQL)
- **Basically Available**: system always responds.
- **Soft state**: state may change even without input (eventual consistency).
- **Eventually Consistent**: all nodes converge eventually.
NoSQL systems (Cassandra, DynamoDB) typically offer BASE semantics.

## 15. Interview Tips
- Explain each property with a bank transfer example.
- Know: isolation level = trade-off between correctness and concurrency.
- MVCC enables high concurrency without heavy locking.
- Durability = WAL/journaling + fsync to disk.
