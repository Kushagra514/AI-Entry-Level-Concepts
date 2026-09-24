# Database Indexing

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
