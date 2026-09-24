# Common LLD Problems

## 1. LRU Cache (LC 146)
Classes: `LRUCache`, `DoublyLinkedList`, `DLinkedNode`.
```python
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}   # key -> node
        self.head, self.tail = DLinkedNode(), DLinkedNode()
        self.head.next = self.tail; self.tail.prev = self.head

    def get(self, key):
        if key not in self.cache: return -1
        self._move_to_front(self.cache[key])
        return self.cache[key].val

    def put(self, key, value):
        if key in self.cache:
            self.cache[key].val = value; self._move_to_front(self.cache[key])
        else:
            node = DLinkedNode(key, value)
            self.cache[key] = node; self._add_to_front(node)
            if len(self.cache) > self.cap:
                lru = self._pop_tail()
                del self.cache[lru.key]
```

## 2. Rate Limiter — Types
- **Token Bucket**: tokens refill at rate r; request consumes 1 token.
- **Leaky Bucket**: queue requests; drain at fixed rate.
- **Fixed Window Counter**: count per time window.
- **Sliding Window Log**: store timestamps of requests.

## 3. Token Bucket Rate Limiter
```python
import time
class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate; self.capacity = capacity
        self.tokens = capacity; self.last = time.time()
    def allow(self):
        now = time.time()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1; return True
        return False
```

## 4. Notification System — Entities
`NotificationService`, `Notification`, `Channel (Email/SMS/Push)`,
`User`, `NotificationPreference`, `TemplateEngine`.

## 5. Notification System — Design
```python
class Channel(ABC):
    @abstractmethod
    def send(self, user, message): ...
class EmailChannel(Channel):
    def send(self, user, message): ...  # SMTP call
class NotificationService:
    def __init__(self, channels: list[Channel]):
        self.channels = channels
    def notify(self, user, message):
        prefs = user.get_preferences()
        for ch in self.channels:
            if type(ch).__name__ in prefs: ch.send(user, message)
```

## 6. URL Shortener — Entities
`URLShortener`, `URLMapping`, `Base62Encoder`, `Analytics`, `Cache`.

## 7. URL Shortener — Design
```python
class URLShortener:
    BASE62 = "0-9A-Za-z"
    def __init__(self, db, cache):
        self.db = db; self.cache = cache; self.counter = 0
    def shorten(self, long_url) -> str:
        self.counter += 1
        short = self._encode(self.counter)
        self.db.save(short, long_url)
        return f"https://short.ly/{short}"
    def resolve(self, short) -> str:
        if short in self.cache: return self.cache[short]
        url = self.db.get(short); self.cache[short] = url; return url
    def _encode(self, num) -> str:
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        res = []
        while num: res.append(chars[num%62]); num //= 62
        return ''.join(reversed(res))
```

## 8. Designing a Logger
```python
class Logger:
    _instance = None
    LEVELS = ['DEBUG','INFO','WARN','ERROR']
    def __new__(cls): ...  # Singleton
    def log(self, level, msg):
        if self.LEVELS.index(level) >= self.LEVELS.index(self.min_level):
            self._write(f"[{level}] {msg}")
```

## 9. Vending Machine — States
Idle → HasMoney → Dispensing → OutOfStock. Use State pattern.

## 10. File System Design
`FileSystem`, `Entry (abstract)`, `File`, `Directory`.
Directory has list of Entry (composite pattern).

## 11. Pub-Sub System
`Broker`, `Topic`, `Publisher`, `Subscriber`, `Message`.
Subscriber registers to topics. Broker fans out messages.

## 12. Design Checklist
- [ ] Defined all core entities with fields
- [ ] Defined relationships (has-a, is-a)
- [ ] Identified key operations/methods
- [ ] Handled concurrency if needed
- [ ] Applied at least one design pattern
- [ ] Discussed extensibility

## 13. LRU Cache — Python Built-in
```python
from functools import lru_cache
from collections import OrderedDict
# OrderedDict: move_to_end(key), popitem(last=False)
```

## 14. Common Gotchas
- Thread safety in rate limiter (use `threading.Lock`).
- URL shortener: collision handling for same URL.
- LRU: O(1) get and put requires hash map + doubly linked list.

## 15. Design Quality Signals
| Signal | Good Design |
|--------|-------------|
| Extensibility | Adding new channel doesn't break existing code |
| Testability | Can inject mock DB/cache |
| SRP | Each class has one job |
| Performance | LRU O(1), Rate limiter O(1) |
