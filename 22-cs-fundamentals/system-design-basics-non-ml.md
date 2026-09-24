# Non-ML System Design Basics

## 1. Approach to System Design Interview
1. Clarify requirements (functional + non-functional: scale, latency, consistency)
2. Estimate capacity (QPS, storage, bandwidth)
3. High-level design (components, data flow)
4. Deep dive (DB schema, API, key algorithms)
5. Identify bottlenecks + mitigations

## 2. Capacity Estimation
```
Twitter-like feed:
- 100M DAU, 50 tweets/user/day read = 5B reads/day ≈ 60K QPS
- 1M new tweets/day, 140 bytes each = 140 MB/day ≈ 50 GB/year
- With media: 100x → 5 TB/year
```

## 3. Horizontal vs Vertical Scaling
- **Vertical (Scale up)**: bigger machine (more CPU/RAM). Limit: hardware cap.
- **Horizontal (Scale out)**: more machines. Requires stateless services, load balancers.
- Prefer horizontal for internet-scale applications.

## 4. Caching
```
Client-side (browser) → CDN → API Gateway cache → Application cache (Redis) → DB cache (query cache)
```
Cache-aside: app checks cache; miss → fetch DB → populate cache.
Write-through: write to cache + DB simultaneously.
Write-back: write to cache only; async flush to DB.
Eviction: LRU (most common), LFU, TTL.

## 5. CAP Theorem in System Design
Partition tolerance is mandatory in distributed systems.
Choose between:
- CP (consistency): bank transactions, inventory. Sacrifice availability on partition.
- AP (availability): social likes, DNS, CDN. Sacrifice consistency on partition.

## 6. Database Choices
```
User profiles, orders → PostgreSQL (relational, ACID)
Session, cache → Redis (key-value, in-memory)
Feed, events → Cassandra (high-write, time-series)
Search → Elasticsearch (full-text)
Media files → S3 + CDN
```

## 7. Message Queues
Decouple producers and consumers. Enable async processing.
```
Use cases: email sending, image resizing, event streaming, order processing
Tools: Kafka (streaming, replay), RabbitMQ (task queues), SQS (managed)
```
Kafka: topics, partitions, consumer groups, offset-based consumption, persistent log.

## 8. Microservices vs Monolith
| | Monolith | Microservices |
|--|----------|---------------|
| Deployment | Single unit | Independent |
| Scalability | Scale whole app | Scale per service |
| Complexity | Simple dev | Complex ops |
| Latency | In-process | Network calls |
| Start with | Monolith | Split when needed |

## 9. API Gateway
Single entry point: auth, rate limiting, routing, SSL termination, monitoring.
Nginx, Kong, AWS API Gateway, Envoy.

## 10. Rate Limiting
Prevent abuse. Implement at: client, API gateway, application.
Algorithms: token bucket (allow bursts), sliding window (precise), fixed window (simple).

## 11. Consistent Hashing
For distributed caching / sharding: map keys to nodes on a ring.
Adding/removing nodes only remaps 1/N of keys (vs all with modulo hashing).
Virtual nodes improve even distribution.

## 12. URL Shortener Design
```
API: POST /shorten → {short_url}, GET /{code} → redirect
Storage: Hash map: code → long_url (DynamoDB or Redis)
Encoding: Base62(auto-increment ID) or MD5(first 7 chars)
Scale: 100M URLs → ~7 bytes/code * 100M = 700 MB (fits in Redis)
```

## 13. Design a Feed System (Twitter-like)
```
Fanout on write: pre-compute feed for each follower on tweet creation → low read latency, high write cost.
Fanout on read: pull tweets from followees at read time → high read latency, low write cost.
Hybrid: fanout on write for regular users, fanout on read for celebrities (many followers).
```

## 14. Reliability Patterns
- **Circuit Breaker**: stop calling failing service. States: closed/open/half-open.
- **Retry with exponential backoff**: avoid thundering herd.
- **Bulkhead**: isolate failure (separate thread pools per service).
- **Health checks + auto-restart**: Kubernetes liveness/readiness probes.

## 15. Non-Functional Requirements Checklist
| Concern | Solution |
|---------|----------|
| High availability | Replication, multi-AZ, load balancer |
| Low latency | CDN, caching, DB indexes |
| Scalability | Horizontal scaling, sharding |
| Durability | DB replication, backups, WAL |
| Security | HTTPS, auth, rate limiting, input validation |
| Observability | Metrics, logs, traces (Prometheus, Grafana, Jaeger) |
