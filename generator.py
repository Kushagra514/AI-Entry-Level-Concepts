import os
import json

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Add {os.path.basename(path)}"')

topic_template = """# {title}

## 1. Definition
[Define the concept strictly and accurately in one or two sentences.]

## 2. Intuition
[Explain it as if to a peer, using an analogy or simple mental model.]

## 3. Why it exists
[What historical or practical problem did this solve? What was broken before?]

## 4. Mechanics
[How does it work under the hood? Step-by-step breakdown.]

## 5. Complexity (Time & Space)
- **Time Complexity:** [Justified analysis]
- **Space Complexity:** [Justified analysis]

## 6. Tiny worked example
[A minimal numerical or trace example.]

## 7. Code (Python, with type hints)
```python
# Provide clean, typed, idiomatic code
```

## 8. Common mistakes
[What do candidates usually get wrong when implementing or explaining this?]

## 9. 30-second interview answer
[The elevator pitch version for a quick question.]

## 10. 2-minute interview answer
[The deep-dive version to lead the conversation.]

## 11. Follow-ups
[What will the interviewer ask next based on your 2-minute answer?]

## 12. Deeper questions
[Hard theoretical questions for strong candidates.]

## 13. Related concepts
[How does this connect to ML or other DSA concepts?]

## 14. When it breaks / Edge cases
[When does this approach fail?]

## 15. Comparison with alternative approaches
[Trade-offs against similar structures/algorithms.]

---
*Where this shows up in ML:* 
[Brief connection to AI/ML context]
"""

problem_template = """# Problem: {title}

## 1. Restate the problem
[In your own words]

## 2. Clarifying questions
[What to ask the interviewer]

## 3. Brute force
- **Approach:** 
- **Time/Space:** 

## 4. Optimization insight
[The single key realization]

## 5. Optimized approach
- **Approach:** 
- **Time/Space:** 

## 6. Data structure choice justification
[Why this and not alternative]

## 7. Clean code
```python
# Typed Python solution
```
*(Note on C++/Java idioms if relevant)*

## 8. Dry run on a small example
[Step-by-step trace]

## 9. Edge cases and how the code handles them
[Empty input, negatives, overflow, duplicates, etc.]

## 10. Follow-up variations
[What if constraints change?]

## 11. Related problems
[Similar patterns]
"""

files_to_generate = {
    # 16-dsa-foundations
    "16-dsa-foundations/big-o-notation.md": topic_template.format(title="Big-O Notation & Complexity Analysis"),
    "16-dsa-foundations/time-vs-space-complexity.md": topic_template.format(title="Time vs Space Complexity Tradeoffs"),
    "16-dsa-foundations/recursion.md": topic_template.format(title="Recursion"),
    "16-dsa-foundations/recursion-vs-iteration.md": topic_template.format(title="Recursion vs Iteration"),
    "16-dsa-foundations/memoization.md": topic_template.format(title="Memoization"),
    "16-dsa-foundations/two-pointers.md": topic_template.format(title="Two Pointers Core Idea"),
    "16-dsa-foundations/sliding-window.md": topic_template.format(title="Sliding Window Core Idea"),
    "16-dsa-foundations/prefix-sums.md": topic_template.format(title="Prefix Sums"),
    "16-dsa-foundations/bit-manipulation.md": topic_template.format(title="Bit Manipulation Basics"),
    "16-dsa-foundations/amortized-analysis.md": topic_template.format(title="Amortized Analysis"),

    # 17-data-structures
    "17-data-structures/arrays.md": topic_template.format(title="Arrays"),
    "17-data-structures/strings.md": topic_template.format(title="Strings"),
    "17-data-structures/linked-lists.md": topic_template.format(title="Linked Lists"),
    "17-data-structures/stacks.md": topic_template.format(title="Stacks"),
    "17-data-structures/queues.md": topic_template.format(title="Queues"),
    "17-data-structures/deque.md": topic_template.format(title="Deque"),
    "17-data-structures/hash-maps.md": topic_template.format(title="Hash Maps"),
    "17-data-structures/hash-sets.md": topic_template.format(title="Hash Sets"),
    "17-data-structures/trees.md": topic_template.format(title="Trees"),
    "17-data-structures/binary-search-trees.md": topic_template.format(title="Binary Search Trees"),
    "17-data-structures/heaps-priority-queues.md": topic_template.format(title="Heaps & Priority Queues"),
    "17-data-structures/tries.md": topic_template.format(title="Tries"),
    "17-data-structures/graphs.md": topic_template.format(title="Graphs"),
    "17-data-structures/union-find-disjoint-set.md": topic_template.format(title="Union Find / Disjoint Set"),
    "17-data-structures/segment-trees-fenwick-trees.md": topic_template.format(title="Segment Trees / Fenwick Trees"),

    # 18-algorithms
    "18-algorithms/sorting-overview.md": topic_template.format(title="Sorting Algorithms Overview"),
    "18-algorithms/bubble-insertion-selection-sort.md": topic_template.format(title="O(n^2) Sorting"),
    "18-algorithms/merge-sort.md": topic_template.format(title="Merge Sort"),
    "18-algorithms/quick-sort.md": topic_template.format(title="Quick Sort"),
    "18-algorithms/heap-sort.md": topic_template.format(title="Heap Sort"),
    "18-algorithms/counting-radix-bucket-sort.md": topic_template.format(title="Linear Time Sorting"),
    "18-algorithms/binary-search.md": topic_template.format(title="Binary Search"),
    "18-algorithms/search-variants.md": topic_template.format(title="Binary Search Variants"),
    "18-algorithms/bfs.md": topic_template.format(title="Breadth-First Search (BFS)"),
    "18-algorithms/dfs.md": topic_template.format(title="Depth-First Search (DFS)"),
    "18-algorithms/topological-sort.md": topic_template.format(title="Topological Sort"),
    "18-algorithms/shortest-paths-dijkstra.md": topic_template.format(title="Dijkstra's Algorithm"),
    "18-algorithms/shortest-paths-bellman-ford.md": topic_template.format(title="Bellman-Ford Algorithm"),
    "18-algorithms/minimum-spanning-tree.md": topic_template.format(title="Minimum Spanning Tree (Prim & Kruskal)"),
    "18-algorithms/backtracking.md": topic_template.format(title="Backtracking"),
    "18-algorithms/greedy-algorithms.md": topic_template.format(title="Greedy Algorithms"),
    "18-algorithms/divide-and-conquer.md": topic_template.format(title="Divide and Conquer"),
    "18-algorithms/dynamic-programming.md": topic_template.format(title="Dynamic Programming Intro"),

    # 19-dp-deep-dive
    "19-dp-deep-dive/dp-intuition-and-identification.md": topic_template.format(title="DP Intuition and Identification"),
    "19-dp-deep-dive/1d-dp.md": topic_template.format(title="1D DP"),
    "19-dp-deep-dive/2d-dp.md": topic_template.format(title="2D DP"),
    "19-dp-deep-dive/knapsack-family.md": topic_template.format(title="Knapsack DP Family"),
    "19-dp-deep-dive/lis-lcs-edit-distance.md": topic_template.format(title="LIS, LCS, Edit Distance"),
    "19-dp-deep-dive/interval-dp.md": topic_template.format(title="Interval DP"),
    "19-dp-deep-dive/dp-on-trees.md": topic_template.format(title="DP on Trees"),
    "19-dp-deep-dive/dp-on-graphs.md": topic_template.format(title="DP on Graphs"),
    "19-dp-deep-dive/dp-with-bitmasking.md": topic_template.format(title="DP with Bitmasking"),

    # 20-dsa-patterns
    "20-dsa-patterns/pattern-two-pointers.md": topic_template.format(title="Pattern: Two Pointers"),
    "20-dsa-patterns/pattern-sliding-window.md": topic_template.format(title="Pattern: Sliding Window"),
    "20-dsa-patterns/pattern-fast-slow-pointers.md": topic_template.format(title="Pattern: Fast and Slow Pointers"),
    "20-dsa-patterns/pattern-merge-intervals.md": topic_template.format(title="Pattern: Merge Intervals"),
    "20-dsa-patterns/pattern-cyclic-sort.md": topic_template.format(title="Pattern: Cyclic Sort"),
    "20-dsa-patterns/pattern-in-place-reversal.md": topic_template.format(title="Pattern: In-place Reversal of a LinkedList"),
    "20-dsa-patterns/pattern-tree-bfs-dfs.md": topic_template.format(title="Pattern: Tree BFS/DFS"),
    "20-dsa-patterns/pattern-two-heaps.md": topic_template.format(title="Pattern: Two Heaps"),
    "20-dsa-patterns/pattern-subsets-backtracking.md": topic_template.format(title="Pattern: Subsets/Backtracking"),
    "20-dsa-patterns/pattern-topological-sort.md": topic_template.format(title="Pattern: Topological Sort"),
    "20-dsa-patterns/pattern-binary-search-on-answer.md": topic_template.format(title="Pattern: Binary Search on Answer"),
    "20-dsa-patterns/pattern-monotonic-stack.md": topic_template.format(title="Pattern: Monotonic Stack"),
    "20-dsa-patterns/pattern-union-find.md": topic_template.format(title="Pattern: Union Find"),
    "20-dsa-patterns/pattern-matching-mapping-problems-to-patterns.md": topic_template.format(title="Matching Problems to Patterns"),

    # 21-oop-and-lld
    "21-oop-and-lld/oop-fundamentals.md": topic_template.format(title="OOP Fundamentals"),
    "21-oop-and-lld/solid-principles.md": topic_template.format(title="SOLID Principles"),
    "21-oop-and-lld/design-patterns-overview.md": topic_template.format(title="Design Patterns Overview"),
    "21-oop-and-lld/low-level-design-questions.md": topic_template.format(title="LLD Question Approach"),
    "21-oop-and-lld/common-lld-problems.md": topic_template.format(title="Common LLD Problems"),

    # 22-cs-fundamentals
    "22-cs-fundamentals/operating-systems-basics.md": topic_template.format(title="OS Basics"),
    "22-cs-fundamentals/processes-vs-threads.md": topic_template.format(title="Processes vs Threads"),
    "22-cs-fundamentals/concurrency-basics.md": topic_template.format(title="Concurrency Basics"),
    "22-cs-fundamentals/memory-management.md": topic_template.format(title="Memory Management"),
    "22-cs-fundamentals/dbms-basics.md": topic_template.format(title="DBMS Basics"),
    "22-cs-fundamentals/sql-vs-nosql.md": topic_template.format(title="SQL vs NoSQL"),
    "22-cs-fundamentals/indexing.md": topic_template.format(title="Database Indexing"),
    "22-cs-fundamentals/normalization.md": topic_template.format(title="Database Normalization"),
    "22-cs-fundamentals/acid-properties.md": topic_template.format(title="ACID Properties"),
    "22-cs-fundamentals/computer-networks-basics.md": topic_template.format(title="Computer Networks Basics"),
    "22-cs-fundamentals/system-design-basics-non-ml.md": topic_template.format(title="System Design Basics (Non-ML)"),

    # 23-dsa-interview-questions
    "23-dsa-interview-questions/arrays-strings.md": problem_template.format(title="Arrays & Strings Problems"),
    "23-dsa-interview-questions/linked-lists.md": problem_template.format(title="Linked Lists Problems"),
    "23-dsa-interview-questions/stacks-queues.md": problem_template.format(title="Stacks & Queues Problems"),
    "23-dsa-interview-questions/trees-graphs.md": problem_template.format(title="Trees & Graphs Problems"),
    "23-dsa-interview-questions/heaps.md": problem_template.format(title="Heaps Problems"),
    "23-dsa-interview-questions/hashing.md": problem_template.format(title="Hashing Problems"),
    "23-dsa-interview-questions/recursion-backtracking.md": problem_template.format(title="Recursion & Backtracking Problems"),
    "23-dsa-interview-questions/dynamic-programming.md": problem_template.format(title="Dynamic Programming Problems"),
    "23-dsa-interview-questions/greedy.md": problem_template.format(title="Greedy Problems"),
    "23-dsa-interview-questions/binary-search.md": problem_template.format(title="Binary Search Problems"),
    "23-dsa-interview-questions/sorting.md": problem_template.format(title="Sorting Problems"),
    "23-dsa-interview-questions/bit-manipulation.md": problem_template.format(title="Bit Manipulation Problems"),
    "23-dsa-interview-questions/math-and-number-theory.md": problem_template.format(title="Math & Number Theory Problems"),
    "23-dsa-interview-questions/rapid-fire-dsa.md": problem_template.format(title="Rapid Fire DSA"),

    # 24-dsa-mock-interviews
    "24-dsa-mock-interviews/mock-dsa-01.md": "# Mock DSA 01\n\n[Record your mock interview session here: Problems, hints, mistakes, feedback.]",
    "24-dsa-mock-interviews/mock-dsa-02.md": "# Mock DSA 02\n\n[Record your mock interview session here: Problems, hints, mistakes, feedback.]",
    "24-dsa-mock-interviews/mock-dsa-03.md": "# Mock DSA 03\n\n[Record your mock interview session here: Problems, hints, mistakes, feedback.]",
    
    # ML placeholders
    "00-foundations/linear-algebra.md": topic_template.format(title="Linear Algebra for ML"),
    "00-foundations/probability-statistics.md": topic_template.format(title="Probability & Statistics"),
    "01-ml-basics/linear-regression.md": topic_template.format(title="Linear Regression"),
    "01-ml-basics/logistic-regression.md": topic_template.format(title="Logistic Regression"),
    "01-ml-basics/decision-trees.md": topic_template.format(title="Decision Trees"),
    "02-deep-learning/backpropagation.md": topic_template.format(title="Backpropagation"),
    "02-deep-learning/activation-functions.md": topic_template.format(title="Activation Functions"),
    "03-nlp/transformers.md": topic_template.format(title="Transformers"),
    "13-project-defense/NEXEN.md": "# NEXEN Project Defense\n[Details on rainfall regime-aware bias correction...]",
    "14-cheat-sheets/dsa-complexity.md": "# DSA Complexity Cheat Sheet\n[Big-O for all ops...]",
    "14-cheat-sheets/dsa-patterns.md": "# DSA Pattern Recognition Cheat Sheet\n[Keywords -> Pattern -> Data Structure]",
    "15-mock-interviews/mixed-mock-01.md": "# Mixed Mock 01 (ML + DSA)\n[1 DSA Problem + 1 ML Concept + Project deep-dive]"
}

# Example of a fully fleshed out Tier 1 file
arrays_content = """# Arrays

## 1. Definition
An array is a linear data structure that stores a collection of elements in contiguous memory locations, allowing for constant-time access via an index.

## 2. Intuition
Think of an array like a row of mailboxes side-by-side. If you know the address of the first mailbox and they are all exactly the same size, you can instantly find any mailbox by calculating its offset, without having to walk past all the previous ones.

## 3. Why it exists
It exists to provide extremely fast, predictable read and write access to elements by position. Before arrays, linked structures required sequential traversal (walking element by element) which is slow and cache-unfriendly.

## 4. Mechanics
When an array is declared with size `N`, the OS allocates a contiguous block of memory. 
The address of element `i` is calculated as: `Memory_Address = Base_Address + (i * Element_Size)`.
In Python, lists are dynamic arrays (arrays of pointers to objects). When they fill up, they allocate a new, larger block of memory (usually 1.125x to 2x size), copy old elements over, and free the old block.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Access: O(1) - Address calculation is constant time.
  - Search: O(n) - Unsorted requires checking each element. O(log n) if sorted (binary search).
  - Insertion/Deletion at end: O(1) amortized.
  - Insertion/Deletion at arbitrary index: O(n) - Requires shifting subsequent elements.
- **Space Complexity:** O(n) - Stores n elements. Dynamic arrays might have up to O(n) wasted capacity.

## 6. Tiny worked example
Array: `[10, 20, 30]`
Memory Base: `0x1000`, Element Size: 4 bytes.
Access index `2`: `0x1000 + (2 * 4) = 0x1008`. Value at `0x1008` is `30`.

## 7. Code (Python, with type hints)
```python
from typing import List

def insert_element(arr: List[int], val: int, index: int) -> None:
    # Python's insert handles shifting, which is O(n) under the hood
    arr.insert(index, val)
```

## 8. Common mistakes
- Confusing array length with array capacity.
- Forgetting that dynamic array resizing takes O(n) time for that specific operation, making it O(1) *amortized*, not absolute.
- In Python, forgetting that `arr.pop(0)` or `arr.insert(0, val)` is O(n).

## 9. 30-second interview answer
"An array is a contiguous memory structure giving O(1) read/write by index. Its main tradeoff is that insertions or deletions in the middle take O(n) time because of shifting. Dynamic arrays automatically resize but incur an O(n) copy cost occasionally, keeping append amortized O(1)."

## 10. 2-minute interview answer
"Arrays provide O(1) random access because they are stored contiguously in memory, allowing direct address calculation. This contiguous nature also makes them highly cache-friendly, exploiting CPU spatial locality. However, this is a double-edged sword: inserting or deleting at an arbitrary index requires shifting elements, an O(n) operation. Dynamic arrays, like Python's list or C++'s vector, handle the fixed-size limitation by allocating a larger contiguous block when capacity is reached and copying elements over. This resizing is O(n), but since it happens infrequently, appending remains O(1) amortized. When working with large datasets, the cache efficiency of arrays often makes them practically faster than theoretically similar data structures like linked lists."

## 11. Follow-ups
- "Why is an array cache-friendly?" (Spatial locality: loading one element loads nearby elements into the CPU cache line).
- "How do you avoid the O(n) deletion cost if order doesn't matter?" (Swap with the last element and pop the last element in O(1)).

## 12. Deeper questions
- "How does Python implement a list? Does it store actual values contiguously?" (No, Python lists are arrays of *pointers* to PyObjects. Real contiguous data requires `array.array` or NumPy).

## 13. Related concepts
- **Strings**: Often implemented as immutable arrays of characters.
- **Hash Maps**: Use arrays under the hood to store buckets.

## 14. When it breaks / Edge cases
- Fails when memory is highly fragmented (OS can't find a large enough contiguous block).
- Terrible for queues (if using `pop(0)`) — use `collections.deque` instead.

## 15. Comparison with alternative approaches
- **vs Linked List:** Arrays have O(1) access and better cache locality. Linked lists have O(1) arbitrary insertion (if pointer is known) and no resizing overhead, but terrible cache locality and O(n) access.

---
*Where this shows up in ML:* 
Arrays (specifically multidimensional arrays or tensors) are the fundamental data structure for all ML. Neural networks rely heavily on dense contiguous arrays to allow for hardware-accelerated (GPU) matrix multiplication (BLAS routines). Poor memory contiguity in PyTorch (`.contiguous()`) ruins performance.
"""

files_to_generate["17-data-structures/arrays.md"] = arrays_content

for path, content in files_to_generate.items():
    write_file(path, content)

print(f"Generated {len(files_to_generate)} files.")
