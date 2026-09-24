# SQL vs NoSQL

## 1. SQL (Relational)
Structured data, fixed schema, ACID guarantees, powerful query language.
Examples: PostgreSQL, MySQL, SQLite, Oracle.

## 2. NoSQL Categories
| Type | Example | Use Case |
|------|---------|----------|
| Document | MongoDB, CouchDB | JSON-like objects |
| Key-Value | Redis, DynamoDB | Cache, session |
| Column-family | Cassandra, HBase | Time-series, analytics |
| Graph | Neo4j | Social networks, recommendations |

## 3. CAP Theorem
A distributed system can guarantee at most 2 of 3:
- **Consistency**: every read gets the latest write.
- **Availability**: every request gets a response (not necessarily latest).
- **Partition Tolerance**: system works despite network partition.

Network partitions always happen → choose C or A during partition.
- CP: MongoDB, HBase, ZooKeeper.
- AP: Cassandra, DynamoDB, CouchDB.

## 4. PACELC
Extends CAP: even without partition, tradeoff between Latency and Consistency.

## 5. When to Use SQL
- Strong ACID requirements (banking, e-commerce orders)
- Complex queries with JOINs
- Data with clear relational structure
- Reporting and analytics

## 6. When to Use NoSQL
- Unstructured/semi-structured data
- Horizontal scalability needed
- High write throughput (Cassandra)
- Simple access patterns (key lookups)
- Schema evolves frequently

## 7. MongoDB vs PostgreSQL
```javascript
// MongoDB — document query
db.orders.find({ user_id: "u123", status: "shipped" })
         .sort({ created_at: -1 }).limit(10)
```
```sql
-- PostgreSQL — relational query
SELECT * FROM orders WHERE user_id = 'u123' AND status = 'shipped'
ORDER BY created_at DESC LIMIT 10;
```

## 8. Eventual Consistency
Nodes may temporarily have different values, but will converge. DynamoDB, Cassandra default.
Acceptable for: social media likes, product view counts, shopping cart.

## 9. Strong Consistency
All reads see the latest committed write. Required for: bank balances, inventory, seat booking.

## 10. Sharding (Horizontal Partitioning)
Split data across multiple nodes by shard key.
- Range sharding: users A-M → shard1, N-Z → shard2.
- Hash sharding: shard = hash(key) % N (even distribution).
- Problem: cross-shard JOINs are expensive.

## 11. Replication
Master-slave: writes to master, reads from slaves. Lag between master and slave.
Multi-master: writes to any node; conflict resolution needed.

## 12. Redis Use Cases
```python
import redis
r = redis.Redis()
r.set('session:abc', user_json, ex=3600)   # TTL 1hr
r.incr('page_views:home')                   # atomic counter
r.lpush('queue:emails', email_json)         # message queue
r.zadd('leaderboard', {user: score})        # sorted set
```

## 13. Cassandra Data Model
Design tables around query patterns (not normalization).
Wide rows: partition key + clustering columns.
No JOINs; denormalization is intentional.

## 14. Common Interview Scenario
"Design a social feed." → Use Cassandra for posts (high write, time-series) + Redis for feed cache + PostgreSQL for user profiles.

## 15. Decision Framework
```
Transactional + relational → PostgreSQL
Cache/session → Redis
Flexible schema, JSON → MongoDB
High-write time-series → Cassandra
Graph traversals → Neo4j
Full-text search → Elasticsearch
```
