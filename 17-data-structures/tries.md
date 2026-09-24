# Tries (Prefix Trees)

## 1. Definition
A Trie is an N-ary tree data structure used for efficiently storing and retrieving strings over a finite alphabet, where each node represents a single character.

## 2. Intuition
Think of a physical dictionary. You don't read every word to find "Apple". You flip to 'A', then go to 'P', then 'P'. A Trie maps this exact physical process into a tree structure, sharing the prefix "APP" for both "Apple" and "Application".

## 3. Why it exists
Searching for a prefix in a Hash Set of strings takes $O(N)$ time (since hashes don't preserve partial string matches). A Trie allows $O(L)$ prefix searching (where $L$ is word length) while compressing storage by sharing common prefixes.

## 4. Mechanics
- **Node:** Contains a Hash Map or Array of child nodes (e.g., size 26 for English letters) and a boolean `is_end_of_word`.
- **Insert:** Traverse the tree character by character. Create nodes for missing characters. Mark the last node as `is_end`.
- **Search:** Traverse character by character. If a character is missing, it doesn't exist. If you reach the end of the word, check `is_end`.
- **StartsWith:** Same as Search, but return `True` without checking `is_end`.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(L)$ for Insert, Search, and StartsWith, where $L$ is the length of the word. Independent of the number of words stored.
- **Space Complexity:** $O(N \times L)$ in the worst case (no shared prefixes), but heavily compressed in practice.

## 6. Tiny worked example
Insert "CAT" and "CAR".
- Root -> C -> A -> T (is_end=True)
- Insert "CAR": Root -> C (exists) -> A (exists) -> R (create, is_end=True).
Both words share the "CA" nodes.

## 7. Code (Python, with type hints)
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end = True

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return True
```

## 8. Common mistakes
- Forgetting the `is_end_of_word` flag, which makes it impossible to distinguish if "APP" is a word in the dictionary or just a prefix of "APPLE".
- Using an array of size 256 for children when a Hash Map is more memory efficient for sparse trees.

## 9. 30-second interview answer
"A Trie is a prefix tree used for string storage. It provides $O(L)$ time complexity for insertions and prefix searches, where $L$ is word length, beating Hash Sets for prefix operations. It is the core structure for autocomplete and spell checkers."

## 10. 2-minute interview answer
"Tries are specialized N-ary trees designed for string retrieval. While a Hash Set can find an exact word in $O(1)$ time, it completely fails at prefix matching (e.g., 'give me all words starting with auto-'). Tries solve this by storing characters hierarchically, implicitly sharing common prefixes. This yields $O(L)$ time for insertions and lookups, which is optimal. The main tradeoff is space; while prefix sharing saves memory, the pointer overhead for nodes can be massive compared to a flat array. In practice, Tries are the definitive choice for autocomplete systems, IP routing (longest prefix match), and word games like Boggle."

## 11. Follow-ups
- "How do you optimize a Trie's memory?" (Use a Radix Tree / Compressed Trie, which merges nodes with a single child into a single node holding a string).

## 12. Deeper questions
- "How does Aho-Corasick algorithm relate to Tries?" (It builds a Trie of search terms and adds 'failure links' (like KMP), allowing multiple substring searches simultaneously in $O(N)$ time).

## 13. Related concepts
- **Hash Maps**: The alternative for exact word matching.
- **Prefix Match**: The primary use case.

## 14. When it breaks / Edge cases
- Massive memory bloat if the alphabet is large (e.g., all Unicode characters) and there are no shared prefixes.

## 15. Comparison with alternative approaches
- **vs Hash Set:** Hash Set is $O(L)$ to hash a word, but takes more memory to store exact string copies and cannot do `startsWith` queries.

---
*Where this shows up in ML:* 
LLM Tokenizers (like WordPiece or BPE) often use Tries under the hood to efficiently match character sequences against the token vocabulary during the encoding phase.
