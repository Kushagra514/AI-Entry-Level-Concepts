import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch E)"')

wc("22-cs-fundamentals/acid-properties.md", r"""# ACID Properties

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
""")

wc("22-cs-fundamentals/computer-networks-basics.md", r"""# Computer Networks Basics

## 1. Definition
Computer networking is the interconnection of multiple devices to share resources and exchange data, governed by standardized protocols, primarily the OSI model and the TCP/IP suite.

## 2. Intuition
Think of sending a letter. 
- Application (writing the letter).
- Transport (choosing Certified Mail for guaranteed delivery, or Standard Mail for speed).
- Network (the postal addressing system, ZIP codes).
- Data Link (the mail trucks moving between local post offices).
- Physical (the road).

## 3. Why it exists
To allow isolated computers to communicate globally. The rigid layered models ensure that a Python web server (Application) doesn't need to know if the user is on WiFi or Ethernet (Physical); the layers abstract away the complexity below them.

## 4. Mechanics
**TCP/IP (and OSI) Layers:**
- **L7 Application:** HTTP, DNS, WebSockets. Data formatting.
- **L4 Transport:** 
  - **TCP:** Connection-oriented, reliable, guarantees order (Handshake, ACKs). Used for Web/Email.
  - **UDP:** Connectionless, fast, unreliable (drops packets). Used for Video Streaming/Gaming.
- **L3 Network:** IP (Internet Protocol), Routers. Routing packets across the globe using IP addresses.
- **L2 Data Link:** MAC addresses, Switches. Moving frames within a local network (LAN).
- **L1 Physical:** Cables, Radio waves, Bits.

## 5. Complexity (Time & Space)
- **Latency Numbers:** L1 cache (0.5 ns) -> Main Memory (100 ns) -> SSD (15,000 ns) -> Network Ping inside datacenter (500,000 ns) -> Network Ping CA to Europe (150,000,000 ns). *Network calls are incredibly slow compared to CPU operations.*

## 6. Tiny worked example
User types `google.com`.
1. **DNS (L7):** Queries a DNS server to translate `google.com` to IP `142.250.190.46`.
2. **TCP (L4):** Performs 3-way handshake (`SYN`, `SYN-ACK`, `ACK`) with the IP on port 443.
3. **TLS (L7/L6):** Handshake to establish encryption keys (HTTPS).
4. **HTTP (L7):** Sends `GET / HTTP/1.1`.

## 7. Code (Python)
```python
import socket

# A basic TCP client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("google.com", 80)) # DNS resolution and TCP handshake
s.sendall(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

response = s.recv(4096)
print(response.decode().split('\n')[0]) # HTTP/1.1 200 OK
s.close()
```

## 8. Common mistakes
- **HTTP status code ignorance:** Assuming a 200 OK means the API call succeeded logically. An API might return 200 OK with `{"error": "invalid user"}`.
- **Ignoring network latency in design:** Making 100 sequential API calls in a loop instead of sending a single batch request. Sequential network calls compound the speed of light delay.

## 9. 30-second interview answer
"Computer networks rely on layered protocol models, primarily TCP/IP. The Application layer handles protocols like HTTP and DNS. The Transport layer ensures data delivery, utilizing TCP for reliable, ordered communication via handshakes, or UDP for fast, connectionless streaming. The Network layer uses IP addresses and routers to navigate the global internet, while the Data Link layer uses MAC addresses and switches for local delivery."

## 10. 2-minute interview answer
"Understanding networks requires understanding the OSI or TCP/IP layered abstractions, where each layer solves a specific problem without worrying about the layers below it. At the Application layer (L7), we deal with HTTP, REST APIs, and DNS (which acts as the internet's phonebook, translating domain names to IP addresses). When an app sends data, it passes to the Transport layer (L4). Here, we choose between TCP and UDP. TCP is connection-oriented; it uses a 3-way handshake, acknowledges received packets, and retransmits lost ones, making it essential for web traffic and file transfers. UDP just blasts packets into the void—it's lossy but very fast, perfect for video calls or real-time gaming. This segment is wrapped in an IP packet at the Network Layer (L3), which routers use to find the best path across the internet. Finally, the Data Link layer (L2) uses MAC addresses to hop the packet across individual physical links (like from your laptop to the WiFi router). In system design, knowing these limits is crucial—specifically the latency overhead of establishing TCP and TLS connections, which is why we use connection pooling and Keep-Alive headers in production."

## 11. Follow-ups
- "What happens during a TCP 3-way handshake?" (Client sends SYN (synchronize). Server replies with SYN-ACK. Client replies with ACK (acknowledge). Connection is established. Takes 1.5 round trips).

## 12. Deeper questions
- "What is a NAT (Network Address Translation)?" (IPv4 only has 4 billion addresses, which isn't enough for every device. Your home router has one public IP. All devices inside your home have private IPs (like 192.168.x.x). The router translates private IPs to its public IP and vice versa using port mapping).

## 13. Related concepts
- **System Design**: Networking is the foundation of distributed systems.
- **Processes vs Threads**: Using async/threads to handle slow network I/O.

## 14. When it breaks / Edge cases
- Packet Loss and TCP Congestion: If a network link gets saturated, routers drop packets. TCP detects this (missing ACKs), assumes the network is congested, and drastically cuts its sending speed (TCP Congestion Control window), ruining throughput.

## 15. Comparison with alternative approaches
- **HTTP/1.1 vs HTTP/2 vs HTTP/3:** HTTP/1.1 requires a new TCP connection (or blocked sequential requests) for each file. HTTP/2 multiplexes over a single TCP connection. HTTP/3 replaces TCP with QUIC (built on UDP) to eliminate Head-of-Line blocking.

---
*Where this shows up in ML:*
Distributed training (NCCL, InfiniBand vs Ethernet), serving models via REST/gRPC APIs.
""")

wc("22-cs-fundamentals/system-design-basics-non-ml.md", r"""# System Design Basics

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
""")
print("Batch E Part 5 complete")
