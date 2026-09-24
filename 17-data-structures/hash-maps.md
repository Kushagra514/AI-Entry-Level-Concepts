# Hash Maps

## 1. Definition
A Hash Map (or Hash Table) is a data structure that maps keys to values for highly efficient lookups, insertions, and deletions using a hash function.

## 2. Intuition
Think of a coat check at a museum. You give them your coat (value), and they give you a ticket number (hash code). When you return, you don't search through all the coats; you hand them the ticket, they go straight to that specific hook (index), and hand you your coat instantly.

## 3. Why it exists
Arrays provide fast access but require knowing the exact numerical index. If you want to look up a user by their username (a string), an array requires a slow $O(N)$ linear search. Hash Maps solve this by converting the string into a numerical index, providing $O(1)$ average-case lookups by a meaningful key.

## 4. Mechanics
1. **Hash Function:** Converts a key (e.g., "apple") into an integer (hash code).
2. **Modulo:** The hash code is reduced to fit the array size (e.g., `hash % array_size`) to get an index.
3. **Storage:** The `(key, value)` pair is stored at that index in the underlying array.
4. **Collisions:** If two keys hash to the same index, they are handled via **Chaining** (storing a linked list at the index) or **Open Addressing** (finding the next empty slot).
5. **Resizing:** When the load factor (items/size) exceeds a threshold (e.g., 0.75), the array is resized (usually doubled) and all keys are rehashed.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Average: $O(1)$ for Search, Insert, and Delete.
  - Worst: $O(N)$ if all keys collide and form a single linked list (though modern implementations use Balanced Trees for bins, making it $O(\log N)$).
- **Space Complexity:** $O(N)$ to store $N$ key-value pairs, plus overhead for empty buckets.

## 6. Tiny worked example
Insert `("Cat", 5)` into array of size 10.
- `hash("Cat")` = 12345
- `12345 % 10` = 5
- Store `("Cat", 5)` at array index 5.
Look up "Cat": hash it, get 5, go to index 5, return 5.

## 7. Code (Python, with type hints)
```python
from typing import Optional

# Python's dict is a highly optimized hash map
hash_map = {}
hash_map["apple"] = 1  # O(1) insert
val = hash_map["apple"] # O(1) lookup
del hash_map["apple"]   # O(1) delete

# Conceptual chaining implementation snippet
class Node:
    def __init__(self, key: str, val: int):
        self.key = key
        self.val = val
        self.next: Optional['Node'] = None
```

## 8. Common mistakes
- Assuming Hash Maps maintain insertion order (Python 3.7+ does, but traditionally they do not, and C++/Java `unordered_map`/`HashMap` do not).
- Using mutable objects (like lists) as keys. Keys must be immutable (hashable).
- Forgetting that worst-case time complexity is $O(N)$.

## 9. 30-second interview answer
"A Hash Map is a data structure that provides average $O(1)$ time complexity for insertions, deletions, and lookups. It achieves this by passing keys through a hash function to compute an index in an underlying array. Collisions are typically resolved via chaining or open addressing."

## 10. 2-minute interview answer
"Hash Maps are the ultimate space-for-time tradeoff. They give us $O(1)$ lookups by mapping arbitrary keys to array indices using a hash function. The efficiency heavily depends on a good hash function that distributes keys uniformly to minimize collisions. When collisions inevitably occur, we handle them using chaining—attaching a linked list to the bucket—or open addressing. To prevent degradation to $O(N)$ time as the map fills up, it tracks a load factor. Once exceeded, it triggers an $O(N)$ resizing and rehashing operation to allocate a larger array. While they are incredibly fast, they are unordered and have higher memory overhead compared to plain arrays."

## 11. Follow-ups
- "How does Python handle collisions?" (Open addressing with a randomized probing sequence).
- "What is a Load Factor?" (The ratio of elements to total buckets. When it gets too high, the map resizes to maintain O(1) performance).

## 12. Deeper questions
- "If a malicious user knows your hash function, how can they crash your server?" (Hash DoS attack: they send millions of keys that all hash to the same bucket, forcing $O(N^2)$ insertion time. Solved by randomized hash seeds).

## 13. Related concepts
- **Hash Sets**: A Hash Map that only stores keys, useful for $O(1)$ membership checking.
- **Tries**: An alternative for string keys that supports prefix searching.

## 14. When it breaks / Edge cases
- Breaks when keys are mutable (their hash changes, losing them in the map).
- Terrible performance if the hash function is poor (e.g., always returns 1).

## 15. Comparison with alternative approaches
- **vs Binary Search Tree (BST):** BST provides $O(\log N)$ lookups and keeps keys sorted. Hash Map provides $O(1)$ lookups but is unordered.

---
*Where this shows up in ML:* 
Embeddings are essentially continuous representations of discrete Hash Map lookups. In standard NLP, vocabulary tokens are mapped to IDs via a Hash Map. During inference, KV-caching in LLMs uses hash-map-like semantics to store and retrieve previously computed Key-Value matrices for specific token positions.
