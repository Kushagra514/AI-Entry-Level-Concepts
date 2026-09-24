# Strings

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
  - Search (substring): $O(N \times M)$ naive, $O(N + M)$ with KMP/Rabin-Karp.
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
"Strings fundamentally act like arrays of characters, but their immutability in languages like Python and Java is their defining feature in interviews. Immutability makes them safe to use as Hash Map keys and thread-safe, but it introduces massive performance traps. If you concatenate strings in a loop, you are constantly allocating new memory blocks and copying data, resulting in $O(N^2)$ complexity. The optimal approach is to collect characters into a mutable list and join them at the very end in $O(N)$ time. Furthermore, string matching isn't trivial; while naive searching is $O(N \times M)$, we rely on algorithms like KMP or Rolling Hashes (Rabin-Karp) for optimal $O(N + M)$ substring search."

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
