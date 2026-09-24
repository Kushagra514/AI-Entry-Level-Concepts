# Database Normalization

## 1. Purpose
Eliminate data redundancy and anomalies (insert, update, delete anomalies).
Each normal form eliminates a specific type of dependency.

## 2. Functional Dependency
A → B: knowing A uniquely determines B.
Example: StudentID → StudentName, StudentID → DOB.

## 3. First Normal Form (1NF)
Rules: atomic values (no repeating groups, no arrays), each row unique.
```
Violation: courses = "Math, Physics, CS"   (multi-valued)
Fix: separate Courses table with one row per course.
```

## 4. Second Normal Form (2NF)
Must be in 1NF + no partial dependency (non-key attribute depends on PART of composite PK).
```
Table: (StudentID, CourseID) → Grade, StudentName
Violation: StudentName depends only on StudentID (partial dependency)
Fix: split into Student(StudentID, StudentName) + Enrollment(StudentID, CourseID, Grade)
```

## 5. Third Normal Form (3NF)
Must be in 2NF + no transitive dependency (non-key → non-key).
```
Table: EmployeeID → DeptID → DeptName
Violation: DeptName transitively depends on EmployeeID via DeptID
Fix: Department(DeptID, DeptName) + Employee(EmployeeID, DeptID)
```

## 6. Boyce-Codd Normal Form (BCNF)
Stricter than 3NF. For every functional dependency X → Y, X must be a superkey.
Handles anomalies 3NF misses with overlapping candidate keys.

## 7. 3NF vs BCNF
```
Course (Student, Subject, Teacher)
FDs: {Student,Subject}→Teacher; Teacher→Subject
3NF: satisfied (Teacher is candidate key for Subject)
BCNF: violated (Teacher→Subject but Teacher is not a superkey of the whole table)
```

## 8. 4NF — Multi-Valued Dependencies
Eliminate multi-valued dependencies. Rare in practice.

## 9. Anomalies Eliminated by Normalization
- **Insert anomaly**: can't add data without inserting other unrelated data.
- **Update anomaly**: same fact stored multiple times; inconsistent update.
- **Delete anomaly**: deleting one fact accidentally deletes another.

## 10. Denormalization
Intentional introduction of redundancy for performance (reduce JOINs).
```sql
-- Normalized: need JOIN orders + users to get user email
-- Denormalized: store user_email directly in orders table
```
Use when: read-heavy, analytical queries, JOINs are bottleneck.

## 11. Normalization in Practice
Most production databases aim for 3NF. BCNF and beyond are theoretical; full normalization may hurt performance.

## 12. Example — Full Normalization
```
Raw: (OrderID, CustomerName, CustomerCity, ProductName, Quantity, Price)
1NF: atomic values ✓ (already)
2NF: no partial deps → Customer(CustID, Name, City), Product(ProdID, Name, Price), Order(OrderID, CustID), OrderItem(OrderID, ProdID, Qty)
3NF: no transitive deps → already satisfied above
```

## 13. Star Schema vs Normalization
Data warehouses use star schema (denormalized): fact table + dimension tables.
Optimized for analytical queries, not OLTP.

## 14. Normalization Decision Guide
| Situation | Approach |
|-----------|----------|
| OLTP (transactions, writes) | Normalize to 3NF |
| OLAP (analytics, reads) | Denormalize / star schema |
| Read-heavy with known query patterns | Denormalize with indexes |
| Storage is a concern | Normalize |

## 15. Interview Quick Reference
| Form | Eliminates |
|------|-----------|
| 1NF | Non-atomic values, duplicate rows |
| 2NF | Partial dependencies on composite PK |
| 3NF | Transitive dependencies |
| BCNF | All non-trivial FDs must have superkey as determinant |
