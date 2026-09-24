# Common LLD Problems

## 1. Definition
This covers the implementations of the most frequently asked Low-Level Design interview questions: LRU Cache, Rate Limiter, and a generic Pub/Sub (Observer) system.

## 2. Intuition
These problems test specific intersections of Object-Oriented principles and Data Structures. You must know the optimal algorithmic data structures (e.g., Hash Map + Doubly Linked List for LRU) while encapsulating them in clean, modular class structures.

## 3. LRU Cache (Least Recently Used)
**Requirement:** Get and Put in $O(1)$ time. Evict the least recently used item when capacity is reached.
**Architecture:** `HashMap` (maps key to node) + `DoublyLinkedList` (maintains recency order).
- **Read:** Look up in map. Move node to head of DLL.
- **Write:** If exists, update value and move to head. If new, add to head. If over capacity, remove tail of DLL and delete from map.

```python
class Node:
    def __init__(self, k, v):
        self.key, self.val = k, v
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head # Dummy nodes
        
    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev
        
    def _add(self, node):
        p = self.head.next
        self.head.next, node.prev = node, self.head
        node.next, p.prev = p, node
        
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.val
        return -1
        
    def put(self, key, value):
        if key in self.cache: self._remove(self.cache[key])
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

## 4. Token Bucket Rate Limiter
**Requirement:** Allow a maximum of $N$ requests per timeframe. Allow bursts up to bucket capacity.
**Architecture:** Store `tokens` and `last_refill_time`. Upon request, refill tokens based on time elapsed, then consume one if available. Thread-safety (Locks) is critical here.

```python
import time, threading

class TokenBucket:
    def __init__(self, capacity, refill_rate_per_sec):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate_per_sec
        self.last_refill = time.time()
        self.lock = threading.Lock()
        
    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            
            # Refill tokens
            new_tokens = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
```

## 5. Pub/Sub (Observer Pattern)
**Requirement:** Let multiple subscribers listen to events published by a broker.
**Architecture:** `Publisher`, `Subscriber` (interface), `Topic`.

```python
class Topic:
    def __init__(self, name):
        self.name = name
        self.subscribers = []
        
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
        
    def publish(self, message):
        for sub in self.subscribers:
            sub.receive(self.name, message)

class Subscriber:
    def receive(self, topic_name, message):
        print(f"Received on {topic_name}: {message}")
```

## 6. Common mistakes
- **LRU Cache:** Forgetting to update the map when the tail node is evicted. You must delete `cache[lru_node.key]`, which is why the `Node` must store both `key` and `value`.
- **Rate Limiter:** Using a background thread to refill tokens every second. This is inefficient at scale. Always compute the refill lazily upon the incoming request using timestamps.
- **Not mentioning concurrency:** All three of these problems require mutex locks in production.

## 7. 30-second interview answer
"Common LLD problems merge data structures with OOP. The LRU Cache requires an O(1) combination of a Hash Map and a Doubly Linked List. The Rate Limiter is best implemented via the Token Bucket algorithm, utilizing lazy timestamp-based refills and mutex locks for thread safety. Pub/Sub systems rely entirely on the Observer design pattern to decouple publishers from subscribers."
