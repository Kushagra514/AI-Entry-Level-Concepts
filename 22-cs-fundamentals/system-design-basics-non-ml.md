# System Design Basics

## 1. Definition
System Design is the process of architecting the high-level components (databases, servers, caches, queues) of a distributed software application to meet specific requirements for scalability, availability, and reliability.

## 2. Intuition
Building a shack (a local Python script) requires no planning. Building a skyscraper (Twitter) requires architects, load-bearing pillars, elevators, and fire escapes. System design is architecture for software.

## 3. Why it exists
A single server can only handle so much traffic before it crashes. When you get 1 million users, you must split the workload across multiple machines. But distributed machines fail, lose network connections, and overwrite each other's data. System design solves these distributed computing problems.

## 4. Mechanics
- **Load Balancers:** Sits in front of servers, distributing incoming traffic (Round Robin, Least Connections) so no single server is overwhelmed.
- **Caching (Redis/Memcached):** In-memory storage for frequently accessed data. Much faster than DB queries.
- **Message Queues (Kafka/RabbitMQ):** Asynchronous communication. Instead of the web server processing a video upload immediately, it puts a message in a queue and replies "Processing." A worker node reads the queue later.
- **CDN (Content Delivery Network):** Geographically distributed servers that cache static assets (Images, JS). A user in Tokyo downloads images from a Tokyo CDN, not a NY server.
- **Database Sharding/Replication:** Splitting DB data across multiple machines (Sharding) or keeping copies (Replication) to handle massive read/write loads.

## 5. Complexity (Time & Space)
- **Availability vs Consistency (CAP Theorem):** In distributed systems, if a network link breaks, you must choose between keeping the system up (Availability) but risking serving stale data, or shutting it down (Consistency).

## 6. Tiny worked example
*Designing a URL Shortener (bit.ly):*
1. **API:** `create(long_url)`, `redirect(short_url)`.
2. **DB:** Need fast key-value lookups. Use NoSQL (Cassandra) or simple RDBMS. `Hash(long_url) -> short_url`.
3. **Scale:** Reads are 100x more frequent than writes. Add a **Redis Cache** in front of the DB. If `short_url` is in Redis, return instantly.
4. **Traffic:** Put a Load Balancer in front of 10 stateless web servers.

## 7. Code (Python)
```python
# Conceptual Caching Pattern (Look-aside cache)
import redis
import db

cache = redis.Redis(host='localhost', port=6379)

def get_user_profile(user_id):
    # 1. Check cache first (takes 1 millisecond)
    profile = cache.get(f"user:{user_id}")
    if profile:
        return profile
        
    # 2. Cache miss. Hit the database (takes 50 milliseconds)
    profile = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    
    # 3. Write to cache for next time, set expiration (TTL) to avoid stale data
    cache.setex(f"user:{user_id}", 3600, profile)
    
    return profile
```

## 8. Common mistakes
- **Single Point of Failure (SPOF):** Having 5 web servers but only 1 database without a replica. If the DB dies, the whole system dies.
- **Over-engineering:** Proposing Kafka, microservices, and Cassandra for a system with 500 Daily Active Users. Start with a monolithic server and Postgres.

## 9. 30-second interview answer
"System design involves architecting scalable backend infrastructure. To scale out (horizontal scaling), we place a Load Balancer in front of stateless application servers. To relieve database pressure, we use Redis for caching frequent reads, and Kafka message queues to process heavy writes asynchronously. We serve static assets via CDNs to reduce latency, and scale databases using read-replicas and sharding."

## 10. 2-minute interview answer
"System design is about balancing tradeoffs between consistency, availability, and latency at scale. I typically approach a design by first estimating the capacity (QPS, storage). The standard scalable architecture begins with a Load Balancer distributing traffic across stateless horizontally-scaled application servers. Because the database is usually the primary bottleneck, we protect it using two layers. First, a caching layer (like Redis) stores results for read-heavy operations, utilizing a Cache-Aside or Write-Through strategy. Second, a Message Queue (like Kafka or RabbitMQ) acts as a buffer for write-heavy or slow operations, allowing the web servers to return HTTP 200s immediately while asynchronous workers process the tasks. For the data layer, we might use SQL for transactional consistency, with Read-Replicas to scale reads. If data volume is extreme, we shard the database or switch to a NoSQL solution. Finally, all static assets (images, CSS) are pushed to a CDN to ensure low latency for users globally. The key is ensuring no Single Point of Failure exists."

## 11. Follow-ups
- "What is Consistent Hashing?" (When sharding a DB or cache cluster, standard hashing `hash(key) % N` breaks completely if you add a new server (N+1). Consistent hashing maps keys to a ring, meaning adding/removing a server only remaps a fraction of the keys).

## 12. Deeper questions
- "How do you design a Feed system like Twitter?" (Fan-out on write vs Fan-out on read. For normal users, when they tweet, pre-compute and push the tweet to all followers' feed caches (Fan-out write). For celebrities with 50M followers, this is too expensive; instead, pull their tweets dynamically when followers load their feeds (Fan-out read)).

## 13. Related concepts
- **SQL vs NoSQL**: Core DB decision.
- **Computer Networks**: CDNs, latencies, protocols.

## 14. When it breaks / Edge cases
- Cache Stampede (Thundering Herd): A popular cache key expires. Suddenly, 10,000 concurrent requests all miss the cache at the same millisecond and hit the database simultaneously, crashing it.

## 15. Comparison with alternative approaches
- **Monolith vs Microservices:** Monolith is a single massive codebase; easy to deploy, hard to scale teams. Microservices break logic into tiny, independent network-connected services; scales organizationally, but introduces massive network complexity and distributed tracing nightmares.

---
*Where this shows up in ML:*
AI System Design (Serving models behind load balancers, async inference via queues, feature stores).
