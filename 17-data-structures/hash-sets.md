# Hash Sets

## 1. Definition
A Hash Set is a data structure that stores a collection of unique elements with no particular order, providing $O(1)$ average-case time for insertion, deletion, and membership checking via hashing.

## 2. Intuition
Imagine a stadium with 10,000 numbered seats. A Hash Set is like a VIP list tied to those seat numbers. If name "Alice" hashes to seat 4271, you instantly check seat 4271. No searching needed. Each seat holds only one person (uniqueness).

## 3. Why it exists
Checking if an element is in a Python `list` takes $O(N)$ time (linear scan). A Hash Set compresses that check to $O(1)$ by computing the element's location mathematically, making "have we seen this before?" instant.

## 4. Mechanics
- **Hashing:** The element is passed through a hash function that returns an integer bucket index.
- **Collision Handling:** Multiple elements can hash to the same bucket. Python resolves collisions via open addressing with probing.
- **Resize:** When the load factor exceeds a threshold (~0.75), the internal array doubles and all elements are rehashed to the new buckets.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(1)$ average for add, remove, and contains. $O(N)$ worst case if many elements hash to the same bucket (pathological inputs or poor hash functions).
- **Space Complexity:** $O(N)$ to store the elements.

## 6. Tiny worked example
Check for duplicates in `[1, 3, 4, 3, 1]`:
- Add 1. Seen: `{1}`.
- Add 3. Seen: `{1, 3}`.
- Add 4. Seen: `{1, 3, 4}`.
- Check 3: `3 in {1, 3, 4}` → True. **Duplicate found in $O(1)$!**

## 7. Code (Python, with type hints)
```python
from typing import List

def has_duplicate(nums: List[int]) -> bool:
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}
union = a | b        # {1, 2, 3, 4}
intersection = a & b # {2, 3}
difference = a - b   # {1}
```

## 8. Common mistakes
- Using a `list` for `seen` tracking. `if n in my_list` is $O(N)$; `if n in my_set` is $O(1)$.
- Trying to add mutable objects (lists, dicts) to a set. Only hashable (immutable) types are allowed. Use `frozenset` or `tuple` for compound keys.

## 9. 30-second interview answer
"A Hash Set stores unique elements and provides $O(1)$ average-case lookup. It is the definitive structure for deduplication and membership testing, trading $O(N)$ space for instant 'have we seen this?' answers — used in cycle detection, two-sum, and visited-node tracking."

## 10. 2-minute interview answer
"Hash Sets are the backbone of optimizing linear-scan membership checks. When a brute-force approach nests two loops to compare every pair of elements, we usually eliminate the inner loop entirely by checking a Hash Set instead. The set computes the element's index via a hash function in $O(1)$ time, so repeated membership tests cost nothing. The practical engineering tradeoff is space: we consume $O(N)$ auxiliary memory. In graph traversal, maintaining a `visited` set is what distinguishes an $O(V+E)$ BFS from an infinite loop. In Two-Sum, storing complements in a set transforms an $O(N^2)$ nested-loop solution into an $O(N)$ single-pass one."

## 11. Follow-ups
- "How does a Hash Set differ from a Hash Map?" (A Hash Map stores key-value pairs. A Hash Set is a Hash Map where the key is the element itself and the value is a trivial boolean/sentinel).

## 12. Deeper questions
- "What is a perfect hash function?" (A hash function where no two inputs produce the same output, eliminating all collisions. Practically impossible for arbitrary inputs, but achievable for small, fixed-key domains).

## 13. Related concepts
- **Hash Maps**: The generalization with values attached.
- **Bloom Filters**: A probabilistic, memory-compressed alternative that allows false positives.

## 14. When it breaks / Edge cases
- Pathological hash collisions degrade $O(1)$ to $O(N)$. Python mitigates this via hash randomization (seeded on process start).

## 15. Comparison with alternative approaches
- **vs Sorted Array (Binary Search):** Sorted array gives $O(\log N)$ lookup but $O(N)$ insertion. Hash Set gives $O(1)$ for both but uses more memory and loses order.

---
*Where this shows up in ML:*
Vocabulary deduplication during tokenizer training; tracking visited nodes in graph-based reasoning over knowledge graphs.
