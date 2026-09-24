# SQL vs NoSQL

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
