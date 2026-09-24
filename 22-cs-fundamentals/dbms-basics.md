# DBMS Basics

## 1. Relational Model
Data organized in tables (relations). Row = tuple, Column = attribute.
Schema defines structure; instance = actual data at a point in time.

## 2. Keys
- **Primary Key**: uniquely identifies each row. NOT NULL, unique.
- **Foreign Key**: references PK of another table. Enforces referential integrity.
- **Candidate Key**: minimal set of columns that uniquely identify a row.
- **Composite Key**: PK made of multiple columns.
- **Surrogate Key**: artificial PK (auto-increment ID).

## 3. SQL Joins
```sql
-- INNER JOIN: only matching rows from both tables
SELECT u.name, o.total FROM users u
JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN: all rows from left, NULLs for no match on right
SELECT u.name, o.total FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- FULL OUTER JOIN: all rows from both; NULL where no match
-- CROSS JOIN: cartesian product
```

## 4. Aggregate Functions
```sql
SELECT dept, COUNT(*), AVG(salary), MAX(salary), SUM(salary)
FROM employees
GROUP BY dept
HAVING AVG(salary) > 50000;
```

## 5. Subqueries
```sql
-- Correlated subquery (runs per row)
SELECT name FROM employees e
WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept=e.dept);

-- Non-correlated
SELECT name FROM employees WHERE dept_id IN (SELECT id FROM depts WHERE city='NYC');
```

## 6. Window Functions
```sql
SELECT name, salary,
    RANK() OVER (PARTITION BY dept ORDER BY salary DESC),
    LAG(salary) OVER (ORDER BY hire_date)
FROM employees;
```

## 7. Transactions
A sequence of operations treated as a unit. Either all succeed or all fail (rollback).
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- or ROLLBACK on error
```

## 8. ACID Properties
- **Atomicity**: all or nothing.
- **Consistency**: DB goes from valid state to valid state.
- **Isolation**: concurrent transactions don't interfere.
- **Durability**: committed data survives crashes.

## 9. Isolation Levels
| Level | Dirty Read | Non-Repeatable | Phantom |
|-------|-----------|----------------|---------|
| Read Uncommitted | Yes | Yes | Yes |
| Read Committed | No | Yes | Yes |
| Repeatable Read | No | No | Yes |
| Serializable | No | No | No |

## 10. ER Diagram Concepts
Entities, Attributes, Relationships. Cardinality: 1:1, 1:N, M:N.
M:N requires junction/bridge table.

## 11. Stored Procedures vs Functions
```sql
-- Function: returns value, used in SELECT
CREATE FUNCTION get_balance(uid INT) RETURNS DECIMAL AS ...

-- Stored Procedure: may have side effects, called with EXEC/CALL
CREATE PROCEDURE transfer(from_id INT, to_id INT, amount DECIMAL) AS ...
```

## 12. Views
Virtual table based on SELECT. Simplifies complex queries; can be updatable.
```sql
CREATE VIEW active_users AS SELECT * FROM users WHERE status='active';
```

## 13. Triggers
Automatically execute on INSERT/UPDATE/DELETE.
```sql
CREATE TRIGGER update_timestamp BEFORE UPDATE ON orders
FOR EACH ROW SET NEW.updated_at = NOW();
```

## 14. Common Interview SQL Questions
- Find second highest salary.
- Find employees who earn more than their manager.
- Delete duplicate rows keeping one.
- Find customers who never placed an order.

## 15. Quick Reference
```sql
-- Second highest salary
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);
-- Or:
SELECT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;
```
