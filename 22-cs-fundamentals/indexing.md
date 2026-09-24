# Database Indexing

## 1. What is an Index?
Auxiliary data structure that speeds up data retrieval. Trade-off: faster reads, slower writes (index must be updated), extra storage.

## 2. B-Tree Index (Most Common)
Balanced tree. Leaf nodes contain data pointers; sorted order.
- O(log N) search, insert, delete.
- Supports: =, <, >, BETWEEN, ORDER BY, LIKE 'prefix%'.
- Default index type in PostgreSQL, MySQL.

## 3. Hash Index
Maps key → bucket with pointer. O(1) equality lookup.
- Only supports `=` — no range queries.
- Used in: hash partitioning, in-memory tables.

## 4. Clustered vs Non-Clustered Index
- **Clustered**: table data physically sorted by index key. Only ONE per table. (InnoDB: PK = clustered.)
- **Non-clustered**: separate structure with pointers to data rows. Multiple allowed.

## 5. B-Tree Index in PostgreSQL
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
-- Partial index (indexes subset of rows)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';
```

## 6. Composite Index
Index on multiple columns. Column order matters.
```sql
INDEX (a, b, c)
-- Usable for: WHERE a=..., WHERE a=... AND b=...
-- NOT usable for: WHERE b=..., WHERE c=...
-- Leftmost prefix rule
```

## 7. Index Selectivity
Selectivity = distinct values / total rows. High selectivity → index is useful.
- email: high selectivity (nearly unique) → good for index.
- gender: low selectivity (only 2-3 values) → full scan often faster.

## 8. Covering Index
Index contains all columns needed by query — no heap lookup needed.
```sql
CREATE INDEX idx_cover ON orders(user_id, status, total);
SELECT status, total FROM orders WHERE user_id = 5;
-- Index-only scan (very fast)
```

## 9. EXPLAIN / Query Plan
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'a@b.com';
-- Seq Scan → no index used
-- Index Scan → using index
-- Bitmap Heap Scan → used for multiple OR conditions
```

## 10. When Index is NOT Used
- Low selectivity column (gender, boolean).
- Query uses function on indexed column: `WHERE LOWER(email) = ...` (create functional index).
- Leading column of composite index not in WHERE.
- Very small table (full scan cheaper).

## 11. Index for Sorting
```sql
-- ORDER BY created_at DESC: index on (created_at DESC) avoids sort step
CREATE INDEX idx_created ON posts(created_at DESC);
```

## 12. GIN and GiST Indexes (PostgreSQL)
- **GIN** (Generalized Inverted Index): full-text search, JSONB, arrays. `@>`, `@@` operators.
- **GiST**: geometric data, range types, fuzzy search.

## 13. Index Maintenance
Indexes bloat over time with updates/deletes. Run `VACUUM` and `ANALYZE` in PostgreSQL.
`REINDEX` rebuilds bloated indexes.

## 14. Index Strategy for Interviews
1. Index columns in WHERE, JOIN, ORDER BY, GROUP BY.
2. Composite index: most selective / most-queried first.
3. Avoid over-indexing — each index slows writes.
4. Use partial indexes for sparse conditions.
5. Check EXPLAIN output to verify index is used.

## 15. Common Interview Questions
- Why doesn't my query use the index? (function on column, low selectivity, small table)
- Clustered vs non-clustered? (physical order vs pointer)
- How does B-tree differ from hash index? (range vs equality)
- What is a covering index? (all needed cols in index)
