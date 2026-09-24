# Database Normalization

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
