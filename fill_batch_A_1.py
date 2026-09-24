import os

def write_and_commit(path, content):
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch A)"')

files = {}

files["16-dsa-foundations/recursion.md"] = """# Recursion

## 1. Definition
Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem, until it reaches a known base case.

## 2. Intuition
Imagine you are standing in a long line and want to know your position. You ask the person in front of you, "What's your position?" They don't know, so they ask the person in front of them. This continues until the person at the very front says, "I am number 1." The second person says, "I am 1 + 1 = 2," and so on, until the answer bubbles back to you.

## 3. Why it exists
It exists to elegantly solve problems that have a naturally recursive structure, such as tree traversals, graph algorithms, and divide-and-conquer strategies. Iterative solutions for these problems often require manually managing a stack, which makes code complex and harder to read.

## 4. Mechanics
Every recursive function needs two parts:
1. **Base Case:** The condition under which the function stops calling itself to prevent an infinite loop.
2. **Recursive Step:** The part of the function that breaks the problem into a smaller, simpler version of itself and calls the function again.
When a recursive call is made, the current function's state (variables) is paused and pushed onto the call stack until the child call returns.

## 5. Complexity (Time & Space)
- **Time Complexity:** Depends on the number of recursive calls and the work done per call. For branching recursion (like Naive Fibonacci), it can be $O(2^n)$.
- **Space Complexity:** $O(d)$, where $d$ is the maximum depth of the recursive call stack. Each active call consumes memory.

## 6. Tiny worked example
Factorial of 3:
- `fact(3)` calls `3 * fact(2)`
- `fact(2)` calls `2 * fact(1)`
- `fact(1)` calls `1 * fact(0)`
- `fact(0)` returns `1` (Base case)
- `fact(1)` returns `1 * 1 = 1`
- `fact(2)` returns `2 * 1 = 2`
- `fact(3)` returns `3 * 2 = 6`

## 7. Code (Python, with type hints)
```python
def factorial(n: int) -> int:
    # Base Case
    if n <= 1:
        return 1
    # Recursive Step
    return n * factorial(n - 1)
```

## 8. Common mistakes
- Forgetting the base case, leading to a `RecursionError` (Stack Overflow).
- Returning the recursive call incorrectly (e.g., calling the function but not returning its result).
- Passing the same arguments to the recursive call, preventing progression toward the base case.

## 9. 30-second interview answer
"Recursion is when a function calls itself to solve smaller subproblems of a larger problem. It requires a base case to terminate and a recursive step to shrink the input. It's highly readable for tree and graph problems but consumes $O(d)$ stack space where $d$ is the recursion depth."

## 10. 2-minute interview answer
"Recursion is a declarative approach to problem-solving that maps perfectly to naturally self-similar data structures like Trees and Graphs. Under the hood, it leverages the OS call stack to implicitly track state, avoiding the boilerplate of managing a manual stack. However, this comes with a space complexity cost proportional to the maximum recursion depth, $O(d)$. In environments without tail-call optimization, like Python, deep recursion can cause stack overflows. Therefore, while recursion is elegant for things like DFS or Merge Sort, we must be careful with linear recursion on large datasets, where iteration or memoization is safer."

## 11. Follow-ups
- "What happens if the base case is missing?" (Stack overflow because the call stack memory is exhausted).
- "How can you optimize recursive functions that compute the same states?" (Memoization/Dynamic Programming).

## 12. Deeper questions
- "What is Tail Call Optimization (TCO), and does Python support it?" (TCO is when the compiler reuses the current stack frame if the recursive call is the very last operation. Python does not support TCO by design to preserve stack traces).

## 13. Related concepts
- **Dynamic Programming**: Heavily relies on recursion + memoization.
- **Backtracking**: Uses recursion to explore search spaces and undo states.
- **Depth-First Search (DFS)**: Naturally implemented via recursion.

## 14. When it breaks / Edge cases
- Breaks when recursion depth exceeds the language's maximum stack limit (e.g., 1000 in Python).
- Breaks when the input size is massive and causes memory exhaustion.

## 15. Comparison with alternative approaches
- **vs Iteration:** Iteration has $O(1)$ space overhead (no call stack) and is generally faster due to lack of function call overhead, but is harder to write for complex branching logic like tree traversals.

---
*Where this shows up in ML:* 
Tree-based ML models (Decision Trees, Random Forests) are inherently recursive structures. The algorithms to split nodes during training (e.g., CART) are implemented recursively. Additionally, computation graphs in deep learning frameworks often use recursive graph traversals (DFS) during the backpropagation step to compute gradients via the chain rule.
"""

files["16-dsa-foundations/two-pointers.md"] = """# Two Pointers Core Idea

## 1. Definition
The Two Pointers technique involves using two integer variables (pointers) to iterate through an iterable (like an array or string), often from different ends or at different speeds, to solve problems optimally.

## 2. Intuition
Imagine trying to find if a word is a palindrome. Instead of reversing the whole word and comparing it, you just point one finger at the first letter and one at the last letter. If they match, you move both fingers inward. You process the word efficiently by converging on the center.

## 3. Why it exists
Many naive solutions require nested loops ($O(n^2)$ time) to compare every pair of elements. Two Pointers allows us to reduce this to a single pass ($O(n)$ time) by intelligently moving pointers based on the sorted nature of the data or specific constraints.

## 4. Mechanics
- **Opposite Ends (Collision):** One pointer starts at index 0, the other at $n-1$. They move inward until they meet. Typically used on sorted arrays (e.g., Two Sum on sorted array).
- **Same Direction (Fast/Slow):** Both start at index 0. One moves faster than the other. Used for cycle detection or finding midpoints.
- **Two Iterables:** Pointers iterate over two different arrays simultaneously (e.g., merging two sorted arrays).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(n)$ - Each pointer traverses the sequence at most once.
- **Space Complexity:** $O(1)$ - Only two integer variables are used.

## 6. Tiny worked example
Find pair summing to 6 in sorted array: `[1, 2, 4, 5]`
- `L=1` (index 0), `R=5` (index 3). Sum = 6. Found!
- If target was 7: `L=1`, `R=5`. Sum = 6 < 7. Move L right.
- `L=2`, `R=5`. Sum = 7. Found!

## 7. Code (Python, with type hints)
```python
from typing import List

def two_sum_sorted(arr: List[int], target: int) -> List[int]:
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1  # Need a larger sum
        else:
            right -= 1 # Need a smaller sum
            
    return [-1, -1]
```

## 8. Common mistakes
- Using collision pointers on an **unsorted** array (the logic breaks because moving L/R doesn't guarantee an increase/decrease).
- Using `while left <= right` when `left < right` is required, leading to using the same element twice.
- Off-by-one errors when updating pointers.

## 9. 30-second interview answer
"Two Pointers is a space-efficient technique that uses two indices to traverse a data structure. It usually reduces an $O(n^2)$ search to $O(n)$. It is most commonly used on sorted arrays to find pairs, or on linked lists to detect cycles using fast and slow pointers."

## 10. 2-minute interview answer
"The Two Pointers pattern is a fundamental optimization technique for linear data structures. By using two indices, we can avoid nested iterations, trading $O(n^2)$ time for $O(n)$ time, while maintaining $O(1)$ space. The most common variant is the opposite-directional pointers used on sorted arrays; because the array is monotonic, we can deterministically decide which pointer to move to approach a target sum. Another critical variant is the fast/slow pointer technique, which is indispensable for linked lists where we lack random access, allowing us to find cycles or midpoints in a single pass. It's often the most elegant solution when space constraints prohibit using a Hash Map."

## 11. Follow-ups
- "What if the array is unsorted?" (You must sort it first $O(n \\log n)$, or use a Hash Map $O(n)$ time / $O(n)$ space).
- "How does this apply to linked lists?" (Fast and slow pointers - Floyd's Cycle Detection).

## 12. Deeper questions
- "Can you use 3 pointers?" (Yes, for 3Sum, we lock one element and use 2 pointers for the rest, reducing $O(n^3)$ to $O(n^2)$).

## 13. Related concepts
- **Sliding Window**: A specific subtype of two pointers where the elements *between* the pointers form a valid state.
- **Binary Search**: Sometimes confused, but Binary Search jumps halves, while Two Pointers moves step-by-step.

## 14. When it breaks / Edge cases
- Fails on unsorted arrays for pair-sum problems.
- Be careful with arrays of size 0 or 1.

## 15. Comparison with alternative approaches
- **vs Hash Map:** Hash map can solve Two Sum on *unsorted* arrays in $O(n)$ time, but uses $O(n)$ space. Two Pointers on a sorted array is $O(n)$ time and $O(1)$ space.

---
*Where this shows up in ML:* 
In NLP, when processing sequences or implementing custom tokenizers, two-pointer techniques are frequently used to scan strings, identify word boundaries, or strip whitespace efficiently without allocating new strings in memory.
"""

files["17-data-structures/hash-maps.md"] = """# Hash Maps

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
  - Worst: $O(N)$ if all keys collide and form a single linked list (though modern implementations use Balanced Trees for bins, making it $O(\\log N)$).
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
- **vs Binary Search Tree (BST):** BST provides $O(\\log N)$ lookups and keeps keys sorted. Hash Map provides $O(1)$ lookups but is unordered.

---
*Where this shows up in ML:* 
Embeddings are essentially continuous representations of discrete Hash Map lookups. In standard NLP, vocabulary tokens are mapped to IDs via a Hash Map. During inference, KV-caching in LLMs uses hash-map-like semantics to store and retrieve previously computed Key-Value matrices for specific token positions.
"""

files["17-data-structures/strings.md"] = """# Strings

## 1. Definition
A String is a sequence of characters, usually implemented as an array of bytes or unicode code points, used to represent text. In many languages (like Python and Java), strings are immutable.

## 2. Intuition
A string is just an array where every element is a character instead of a number. However, because text encoding (like ASCII vs UTF-8) and language semantics vary, strings have special built-in methods and performance quirks that standard arrays do not.

## 3. Why it exists
Computers natively only understand numbers (binary). Strings exist as an abstraction layer to let humans process, store, and manipulate text easily, handling the complex translation between human letters and computer bytes.

## 4. Mechanics
In memory, strings are stored sequentially. In languages where they are immutable (Python, Java), any modification (like concatenation or replacing a character) requires allocating a completely new contiguous block of memory and copying the old contents over. 

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Access (by index): $O(1)$
  - Search (substring): $O(N \\times M)$ naive, $O(N + M)$ with KMP/Rabin-Karp.
  - Concatenation: $O(N + M)$ because a new string must be built.
- **Space Complexity:** $O(N)$ where $N$ is the number of characters.

## 6. Tiny worked example
String concatenation in Python:
`a = "AI"`
`b = "ML"`
`c = a + b` -> A new memory block of size 4 is allocated, "AI" is copied, then "ML" is copied. `c` points to `"AIML"`.

## 7. Code (Python, with type hints)
```python
def is_palindrome(s: str) -> bool:
    # O(N) time and O(N) space using slicing
    return s == s[::-1]

def is_palindrome_optimized(s: str) -> bool:
    # O(N) time and O(1) space using Two Pointers
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

## 8. Common mistakes
- Building strings in a loop using `+=` in Python or Java. This creates $O(N^2)$ time complexity because every addition allocates a new string. (Always use `"".join(list_of_strings)` or `StringBuilder`).
- Confusing byte length with character length (e.g., emojis in UTF-8 take 4 bytes but are 1 character).

## 9. 30-second interview answer
"Strings are arrays of characters used to represent text. In many modern languages, they are immutable, meaning any modification results in the creation of a new string object in memory. Therefore, string manipulation must be handled carefully to avoid $O(N^2)$ time complexity during concatenation."

## 10. 2-minute interview answer
"Strings fundamentally act like arrays of characters, but their immutability in languages like Python and Java is their defining feature in interviews. Immutability makes them safe to use as Hash Map keys and thread-safe, but it introduces massive performance traps. If you concatenate strings in a loop, you are constantly allocating new memory blocks and copying data, resulting in $O(N^2)$ complexity. The optimal approach is to collect characters into a mutable list and join them at the very end in $O(N)$ time. Furthermore, string matching isn't trivial; while naive searching is $O(N \\times M)$, we rely on algorithms like KMP or Rolling Hashes (Rabin-Karp) for optimal $O(N + M)$ substring search."

## 11. Follow-ups
- "Why are strings immutable in Python?" (To ensure they are hashable for use in dictionaries/sets, and for memory efficiency via string interning).
- "How do you search for a substring efficiently?" (KMP Algorithm, Rabin-Karp, or Tries).

## 12. Deeper questions
- "Explain how Rolling Hash (Rabin-Karp) works for string matching." (Computes a hash of a sliding window. When moving the window, it drops the old character's value and adds the new one in $O(1)$ time, avoiding re-hashing the whole string).

## 13. Related concepts
- **Arrays**: Strings are essentially constrained arrays.
- **Tries**: The optimal data structure for storing dictionaries of strings.

## 14. When it breaks / Edge cases
- Fails on multi-byte characters (UTF-8 emojis) if treated blindly as ASCII arrays. Reversing a string with an emoji by byte will corrupt it.

## 15. Comparison with alternative approaches
- **vs Character Arrays (C-strings):** Mutable, but prone to buffer overflows and missing null-terminators. Modern immutable strings prioritize safety and hashability over raw mutation speed.

---
*Where this shows up in ML:* 
Strings are the raw input for all NLP. However, neural networks cannot process strings. The fundamental pipeline of NLP is breaking strings down (Tokenization), converting those tokens to integers (Vocabulary Mapping), and then into dense floats (Embeddings).
"""

files["17-data-structures/linked-lists.md"] = """# Linked Lists

## 1. Definition
A Linked List is a linear data structure where elements (nodes) are not stored contiguously in memory. Instead, each node contains data and a pointer/reference to the next node in the sequence.

## 2. Intuition
Imagine a scavenger hunt. You are given a clue that leads you to location A. At location A, you find a prize (data) and the next clue (pointer) leading you to location B. You cannot jump directly to location C; you must follow the clues in order.

## 3. Why it exists
Arrays require a contiguous block of memory and resizing them is expensive $O(N)$. Linked Lists solve this by allowing data to be scattered across memory. You can easily insert or delete nodes without shifting other elements, provided you know where to make the change.

## 4. Mechanics
- **Singly Linked List:** Node contains `data` and `next` pointer.
- **Doubly Linked List:** Node contains `data`, `next`, and `prev` pointers, allowing backward traversal.
- The list is tracked by holding a reference to the `head` node. The last node points to `Null` (or `None`).
- **Insertion/Deletion:** To insert node B between A and C, update A's `next` to B, and B's `next` to C.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Access/Search: $O(N)$ - Must traverse from the head.
  - Insertion/Deletion at Head: $O(1)$.
  - Insertion/Deletion at given node: $O(1)$ (assuming you already have the pointer to that node).
- **Space Complexity:** $O(N)$ - Plus the overhead of storing the pointer(s) in each node.

## 6. Tiny worked example
List: `1 -> 2 -> 3`
Insert `4` after `1`:
- Create node `4`.
- `4.next = 1.next` (which is `2`).
- `1.next = 4`.
Result: `1 -> 4 -> 2 -> 3`.

## 7. Code (Python, with type hints)
```python
from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

def delete_node(head: Optional[ListNode], target: int) -> Optional[ListNode]:
    # Dummy node elegant pattern to handle head deletions easily
    dummy = ListNode(0)
    dummy.next = head
    curr = dummy
    
    while curr.next:
        if curr.next.val == target:
            curr.next = curr.next.next # Skip the target node
            break
        curr = curr.next
        
    return dummy.next
```

## 8. Common mistakes
- Losing the reference to the `head` of the list while iterating.
- `NullReferenceException` (or `NoneType` error) by trying to access `node.next.val` without checking if `node.next` is `None`.
- Failing to handle edge cases: empty list, one node list, or deleting the head node (using a Dummy Node solves this).

## 9. 30-second interview answer
"A Linked List is a sequence of nodes where each node points to the next. Unlike arrays, it doesn't require contiguous memory, allowing for $O(1)$ insertions and deletions if you have the reference. However, it lacks random access, meaning finding an element takes $O(N)$ time."

## 10. 2-minute interview answer
"Linked lists are a pointer-based data structure that trades $O(1)$ random access for $O(1)$ structural modification. Because nodes are scattered in the heap and linked via pointers, we never have to resize or shift elements like we do with dynamic arrays. This makes them ideal for building Stacks and Queues. However, this comes with two massive drawbacks: first, searching requires $O(N)$ sequential traversal. Second, they have terrible CPU cache locality. Because arrays are contiguous, the CPU can pre-fetch them into fast cache. Linked list nodes are randomly scattered, causing cache misses which makes them practically slower than arrays for most iterations, despite theoretical Big-O equivalence."

## 11. Follow-ups
- "How do you detect a cycle in a linked list?" (Floyd's Fast and Slow pointer technique).
- "Why are Dummy Nodes (Sentinel Nodes) useful?" (They eliminate the need for edge-case `if` statements when inserting/deleting at the head).

## 12. Deeper questions
- "How do you reverse a linked list?" (Iteratively keeping track of `prev`, `curr`, and `next` pointers, or recursively).

## 13. Related concepts
- **Trees / Graphs**: Simply linked lists where nodes have multiple pointers.
- **LRU Cache**: Built using a Hash Map + Doubly Linked List.

## 14. When it breaks / Edge cases
- Modifying a list while iterating over it can easily sever the rest of the list.
- Deep recursive traversal of a linked list will cause a Stack Overflow.

## 15. Comparison with alternative approaches
- **vs Arrays:** Arrays have $O(1)$ access and great cache locality, but $O(N)$ insertions. Linked lists have $O(N)$ access, poor cache locality, but $O(1)$ insertions.

---
*Where this shows up in ML:* 
While native linked lists are rare in highly optimized ML code (because GPUs require dense contiguous arrays/tensors for fast math), the *concept* of linked computation graphs is foundational to PyTorch's Autograd system. Each tensor operation generates a node, and nodes hold pointers to their creator functions, forming a directed acyclic graph (essentially a multi-linked list) used to trace backward for gradients.
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch A - Part 1 Complete")
