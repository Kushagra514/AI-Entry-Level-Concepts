import os

def write_and_commit(path, content):
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch A)"')

files = {}

files["18-algorithms/quick-sort.md"] = """# Quick Sort

## 1. Definition
Quick Sort is a highly efficient, divide-and-conquer, in-place sorting algorithm. It works by selecting a 'pivot' element and partitioning the other elements into two sub-arrays, according to whether they are less than or greater than the pivot.

## 2. Intuition
Imagine a gym teacher organizing students by height. They pick a random student (the pivot). They tell everyone shorter to stand on the left, and everyone taller to stand on the right. Now, the pivot is in their exact final position. They then do the same thing for the group on the left, and the group on the right, recursively.

## 3. Why it exists
While Merge Sort guarantees $O(N \\log N)$ time, it requires $O(N)$ extra memory. Quick Sort was developed to sort data *in-place*, drastically reducing memory overhead and taking advantage of CPU caching, making it practically faster for most real-world arrays.

## 4. Mechanics
1. **Choose Pivot:** Pick an element from the array (first, last, random, or median).
2. **Partition:** Rearrange the array so all elements smaller than the pivot are to its left, and all larger elements are to its right.
3. **Recursion:** Recursively apply the above steps to the sub-array of smaller elements and the sub-array of larger elements.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Best / Average: $O(N \\log N)$
  - Worst: $O(N^2)$ (occurs when the pivot is always the smallest or largest element, usually on an already sorted array with a naive pivot).
- **Space Complexity:** $O(\\log N)$ on average for the recursive call stack. $O(N)$ worst-case stack depth.

## 6. Tiny worked example
Array: `[10, 80, 30, 90, 40]`
- Pick pivot `40` (last element).
- Partition: `[10, 30]` (less) + `40` + `[80, 90]` (greater).
- `40` is locked. Recursively quicksort `[10, 30]` and `[80, 90]`.
- Array becomes `[10, 30, 40, 80, 90]`.

## 7. Code (Python, with type hints)
```python
from typing import List
import random

def quick_sort(arr: List[int], low: int, high: int) -> None:
    if low < high:
        # Partition the array and get the pivot index
        pi = partition(arr, low, high)
        
        # Recursively sort the sub-arrays
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr: List[int], low: int, high: int) -> int:
    # Pick a random pivot to avoid O(N^2) on sorted arrays
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    
    pivot = arr[high]
    i = low - 1  # Index of smaller element
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    # Swap pivot to its final position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

## 8. Common mistakes
- Using the first or last element as the pivot *without* randomization, which causes $O(N^2)$ time on already-sorted arrays (a common real-world scenario).
- Forgetting that Quick Sort is **Unstable**.
- Writing out-of-place Quick Sort in interviews (e.g., using list comprehensions `[x for x in arr if x < p]`). This is readable but ruins the $O(1)$ auxiliary space benefit, showing a lack of systems understanding.

## 9. 30-second interview answer
"Quick Sort is an in-place, divide-and-conquer sorting algorithm. It partitions an array around a pivot element and recursively sorts the left and right sides. It averages $O(N \\log N)$ time and $O(\\log N)$ space but can degrade to $O(N^2)$ if pivots are chosen poorly. It is unstable."

## 10. 2-minute interview answer
"Quick Sort is usually the fastest comparison-based sort in practice because its in-place partitioning makes it highly cache-efficient. The algorithm hinges on the partition step, where we place a pivot element in its final sorted position by swapping smaller elements to its left and larger to its right. Because it operates in-place, it only requires $O(\\log N)$ auxiliary space for the recursion stack. The critical flaw is its worst-case $O(N^2)$ time complexity, which happens if the data is already sorted and we naively pick the last element as a pivot. We mitigate this by choosing a random pivot or using the Median-of-Three method. Unlike Merge Sort, it is unstable, meaning it may swap the relative order of identical elements."

## 11. Follow-ups
- "What is Quickselect?" (A modification of Quick Sort that only recurses into one half of the partition to find the $K$-th largest element in average $O(N)$ time).

## 12. Deeper questions
- "How does Python's Timsort avoid Quick Sort's instability?" (It doesn't use Quick Sort at all; it uses Merge Sort and Insertion Sort).

## 13. Related concepts
- **Merge Sort**: The stable, out-of-place alternative.
- **Top-K Elements**: Solved via Quickselect.

## 14. When it breaks / Edge cases
- Deep recursion on worst-case pivots can cause Stack Overflows in languages without deep stack limits.

## 15. Comparison with alternative approaches
- **vs Merge Sort:** Quick Sort is in-place ($O(\\log N)$ space) and faster due to cache locality, but unstable. Merge Sort is out-of-place ($O(N)$ space) but stable and guaranteed $O(N \\log N)$ time.

---
*Where this shows up in ML:* 
Finding the Median or Top-K probabilities (e.g., Top-K sampling in LLM generation) uses Quickselect, which relies entirely on the Quick Sort partitioning subroutine.
"""

files["18-algorithms/bfs.md"] = """# Breadth-First Search (BFS)

## 1. Definition
Breadth-First Search (BFS) is a traversal algorithm for trees or graphs that explores all neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.

## 2. Intuition
Imagine dropping a stone in a calm pond. The ripples expand outward in perfect concentric circles. BFS works exactly like that: it explores the closest neighbors (distance 1), then the next circle of neighbors (distance 2), expanding evenly in all directions.

## 3. Why it exists
DFS plunges deep down one path, which is terrible if you are looking for the *shortest* path in an unweighted graph. BFS guarantees that the first time you reach a node, you have found the shortest path to it. 

## 4. Mechanics
1. Initialize a **Queue** and a **Visited Set**.
2. Push the starting node to the Queue and mark it as visited.
3. While the Queue is not empty:
   - Pop the front node.
   - Process the node.
   - Loop through its neighbors. If a neighbor is not visited, mark it visited and push it to the Queue.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V + E)$ where $V$ is Vertices and $E$ is Edges. We process every node and every edge once.
- **Space Complexity:** $O(V)$ in the worst case to hold the Queue and the Visited set. (In a tree, the bottom level can hold up to $V/2$ nodes).

## 6. Tiny worked example
Graph: `A - B, A - C, B - D`
1. Queue: `[A]`, Visited: `{A}`
2. Pop `A`. Neighbors: `B`, `C`. Queue: `[B, C]`, Visited: `{A, B, C}`
3. Pop `B`. Neighbors: `A` (visited), `D`. Queue: `[C, D]`, Visited: `{A, B, C, D}`
4. Pop `C`. No unvisited neighbors. Queue: `[D]`
5. Pop `D`. No unvisited neighbors. Done. Order: `A, B, C, D`.

## 7. Code (Python, with type hints)
```python
from typing import List, Dict, Set
from collections import deque

def bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    visited: Set[int] = {start}
    queue: deque = deque([start])
    order: List[int] = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return order
```

## 8. Common mistakes
- Marking nodes as visited *when they are popped* instead of *when they are added to the queue*. If you wait until they are popped, multiple nodes might add the same unvisited neighbor to the queue, causing massive memory bloat and redundancy.
- Using a `list` instead of `collections.deque` for the queue, turning an $O(1)$ pop into an $O(N)$ pop.

## 9. 30-second interview answer
"BFS is a graph and tree traversal algorithm that explores level by level. It uses a Queue to maintain the frontier and a Set to track visited nodes. It runs in $O(V + E)$ time and is the standard algorithm for finding the shortest path in unweighted graphs."

## 10. 2-minute interview answer
"BFS explores an unweighted graph uniformly in all directions, radiating outward. Because it processes all nodes at distance $K$ before any nodes at distance $K+1$, it is mathematically guaranteed to find the shortest path between the start node and any other reachable node. We implement it using a Queue for FIFO processing and a Hash Set to track visited nodes to avoid infinite cycles. A critical implementation detail is marking nodes as visited the moment they are added to the queue, not when they are processed, to prevent the queue from exploding with duplicates. It takes $O(V + E)$ time and $O(V)$ space."

## 11. Follow-ups
- "How do you track the actual shortest path, not just the distance?" (Maintain a `parent` dictionary mapping each neighbor back to the node that discovered it, then backtrack from the target to the start).

## 12. Deeper questions
- "What if the graph has weighted edges?" (BFS fails because the shortest path by edges might not be the shortest by weight. Use Dijkstra's Algorithm, which replaces the standard Queue with a Priority Queue).

## 13. Related concepts
- **Dijkstra's Algorithm**: Weighted BFS.
- **Topological Sort**: Kahn's algorithm is essentially a modified BFS based on in-degrees.

## 14. When it breaks / Edge cases
- Disconnected graphs: BFS only explores the connected component of the start node. You must loop over all vertices to guarantee full traversal.

## 15. Comparison with alternative approaches
- **vs DFS:** BFS uses more memory for wide trees but finds the shortest path. DFS uses less memory (proportional to depth, $O(H)$) and is better for maze-solving or topological sort, but cannot guarantee shortest paths.

---
*Where this shows up in ML:* 
In Knowledge Graphs (used heavily in GenAI RAG pipelines), BFS is used to find entities that are exactly $K$-hops away from a subject entity to expand context.
"""

files["18-algorithms/dfs.md"] = """# Depth-First Search (DFS)

## 1. Definition
Depth-First Search (DFS) is a traversal algorithm for trees or graphs that explores as far as possible along each branch before backtracking.

## 2. Intuition
Imagine exploring a massive maze. You pick a path and run down it as fast as you can. When you hit a dead end, you back up to the last intersection and try the next path. You keep plunging deep until you explore everything.

## 3. Why it exists
DFS exists to explore all possible configurations or paths in a search space. Because it relies on a stack (or recursion) rather than a wide queue, it is highly memory efficient for deep, branching structures compared to BFS.

## 4. Mechanics
1. Start at a node and mark it as visited.
2. Iterate through its neighbors.
3. If a neighbor hasn't been visited, recursively call DFS on that neighbor.
4. When all neighbors are explored, the function returns (backtracks).
*(Can also be implemented iteratively using an explicit Stack).*

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(V + E)$ - We visit every vertex and evaluate every edge exactly once.
- **Space Complexity:** $O(V)$ worst-case for the call stack (in a linked-list-like graph). In a balanced tree, space is $O(\\log V)$ for the height.

## 6. Tiny worked example
Graph: `A - B, A - C, B - D`
1. Start `A`. Mark `{A}`. Visit neighbor `B`.
2. At `B`. Mark `{A, B}`. Visit neighbor `D`.
3. At `D`. Mark `{A, B, D}`. No unvisited neighbors. Backtrack to `B`.
4. At `B`. No more unvisited neighbors. Backtrack to `A`.
5. At `A`. Visit neighbor `C`.
6. At `C`. Mark `{A, B, D, C}`. Done. Order: `A, B, D, C`.

## 7. Code (Python, with type hints)
```python
from typing import List, Dict, Set

def dfs_recursive(graph: Dict[int, List[int]], start: int, visited: Set[int] = None) -> List[int]:
    if visited is None:
        visited = set()
        
    visited.add(start)
    order = [start]
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            # Recursively explore deep
            order.extend(dfs_recursive(graph, neighbor, visited))
            
    return order
```

## 8. Common mistakes
- Forgetting to maintain a `visited` set for graphs, resulting in infinite recursion (Stack Overflow) if there's a cycle. (Trees don't need a visited set because they are acyclic directed).
- Thinking DFS will find the shortest path. It absolutely does not; it finds the *first* path.

## 9. 30-second interview answer
"DFS is a traversal algorithm that plunges as deep as possible into a graph before backtracking. It is typically implemented recursively, leveraging the call stack. It runs in $O(V + E)$ time and requires $O(H)$ space where $H$ is the max depth, making it memory-efficient for deep trees. It's ideal for cycle detection and topological sorting."

## 10. 2-minute interview answer
"DFS is the standard algorithm for exhaustive search and backtracking problems. By aggressively traversing down a single path until it terminates, it mimics human maze-solving. We implement it recursively, which inherently utilizes the OS call stack, or iteratively with an explicit Stack. For graphs, tracking visited nodes in a Hash Set is mandatory to prevent infinite loops on cycles. While BFS is required for shortest-path problems, DFS is vastly superior for cycle detection (by tracking the current recursion stack), Topological Sorting, and exploring permutations/combinations in backtracking, because its space complexity is bound by the maximum depth $O(H)$, rather than the maximum width."

## 11. Follow-ups
- "How do you detect a cycle using DFS?" (Pass an additional `current_path` set into the recursion. If you see a node that is in `current_path`, you have a back-edge, hence a cycle).
- "How do you implement DFS iteratively?" (Use a Stack. Push start, pop, mark visited, push neighbors).

## 12. Deeper questions
- "If a tree is highly unbalanced, what is the risk of recursive DFS?" (Stack Overflow. Python's recursion limit is usually 1000. An iterative stack on the heap is safer).

## 13. Related concepts
- **Backtracking**: Essentially DFS applied to an abstract state-space tree.
- **Topological Sort**: Done using DFS by pushing nodes to a stack *after* all their children are explored.

## 14. When it breaks / Edge cases
- Stack Overflow on deep graphs.
- Disconnected components require an outer loop over all vertices to trigger DFS.

## 15. Comparison with alternative approaches
- **vs BFS:** DFS uses less memory on wide trees and is easier to write (just recursion). BFS finds shortest paths and prevents getting "stuck" down an infinitely deep branch.

---
*Where this shows up in ML:* 
In PyTorch/TensorFlow, calculating gradients via Backpropagation is mathematically an application of the Chain Rule executed via a Depth-First Search post-order traversal over the computational graph.
"""

files["17-data-structures/trees.md"] = """# Trees

## 1. Definition
A Tree is a hierarchical, acyclic data structure consisting of nodes connected by directed edges. It has a single root node, and every other node has exactly one parent.

## 2. Intuition
Think of a corporate org chart. The CEO (Root) is at the top. VPs (Children) report to the CEO. Managers report to VPs. A person cannot report to two managers (one parent rule), and there are no cycles (you can't report to someone who reports to you).

## 3. Why it exists
Linear data structures (Arrays, Linked Lists) require $O(N)$ time to search. Hash maps offer $O(1)$ search but destroy ordering. Trees exist to provide a middle ground: hierarchical ordering with the potential for $O(\\log N)$ search, insertion, and deletion, while maintaining sorted relationships.

## 4. Mechanics
- **Root:** The topmost node.
- **Leaf:** A node with no children.
- **Height:** The length of the longest path from the root to a leaf.
- **Depth:** The length of the path from the root to a specific node.
- **Binary Tree:** A tree where each node has at most two children (left and right).
- Traversals: In-order (Left, Root, Right), Pre-order (Root, Left, Right), Post-order (Left, Right, Root).

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Traversing all nodes: $O(N)$.
  - Searching/Inserting (in balanced structures): $O(\\log N)$ based on Height.
- **Space Complexity:** $O(H)$ where $H$ is the height of the tree (for recursion stack). In the worst case (a stick), $H = N$.

## 6. Tiny worked example
Pre-order Traversal of:
    1
   / \\
  2   3
- Visit Root (1).
- Visit Left Subtree (2).
- Visit Right Subtree (3).
- Output: `[1, 2, 3]`.

## 7. Code (Python, with type hints)
```python
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    res = []
    if root:
        res.extend(inorder_traversal(root.left))
        res.append(root.val)
        res.extend(inorder_traversal(root.right))
    return res
```

## 8. Common mistakes
- Not checking for `None` (Null) nodes before accessing `.val` or `.left`.
- Confusing Height (max distance to leaf) with Depth (distance to root).
- Assuming standard trees are automatically balanced (they aren't; worst-case they become linked lists).

## 9. 30-second interview answer
"A tree is a hierarchical, directed, acyclic graph. It consists of a root node with branching children. It is used to represent hierarchical data like file systems, and when structured as a Binary Search Tree, it can provide $O(\\log N)$ search operations. We navigate it using DFS (Pre/In/Post-order) or BFS (Level-order)."

## 10. 2-minute interview answer
"Trees are fundamental nonlinear structures that represent hierarchical relationships. Unlike graphs, trees enforce a strict parent-child relationship with exactly one root and absolutely no cycles. The most common variant in interviews is the Binary Tree. We interact with trees using Depth-First Search for structural problems—where Pre-order is used for copying trees, In-order for getting sorted values out of a BST, and Post-order for deleting trees or calculating heights—or Breadth-First Search for level-by-level analysis. The efficiency of a tree is entirely dictated by its height; a perfectly balanced tree has a height of $\\log N$, offering incredibly fast operations, while a degenerate tree degrades to a linked list with $O(N)$ operations."

## 11. Follow-ups
- "What's the difference between a Tree and a Graph?" (A tree is a special type of graph that is connected and acyclic, with $V-1$ edges).
- "How do you serialize a tree into a string?" (Pre-order traversal, recording 'null' for empty children to preserve structure).

## 12. Deeper questions
- "What is an N-ary tree?" (A tree where nodes can have an arbitrary number of children, like a File System or a Trie).

## 13. Related concepts
- **Binary Search Tree (BST)**: A binary tree with sorted properties.
- **Trie**: A tree specifically designed for string prefixes.
- **Heaps**: Complete binary trees that satisfy the heap property.

## 14. When it breaks / Edge cases
- Degenerate trees (skewed entirely to the left or right) break the $O(\\log N)$ time expectation, falling back to $O(N)$.

## 15. Comparison with alternative approaches
- **vs Linked List:** A linked list is mathematically just a unary tree (each node has exactly 1 child). Trees branch out, allowing logarithmic time complexity.

---
*Where this shows up in ML:* 
Decision Trees (and ensembles like Random Forests, XGBoost) use tree structures to partition data based on feature thresholds. The inference step for a single data point is literally traversing the tree from root to leaf based on `if/else` checks, taking $O(H)$ time.
"""

files["17-data-structures/binary-search-trees.md"] = """# Binary Search Trees (BST)

## 1. Definition
A Binary Search Tree is a binary tree where every node satisfies a specific property: all nodes in its left subtree have smaller values, and all nodes in its right subtree have larger values.

## 2. Intuition
It's the data structure equivalent of the Binary Search algorithm. If you are looking for the number 50 and the root is 100, you know instantly you only need to search the left side of the tree. Every step down halves the search space.

## 3. Why it exists
Arrays allow $O(\\log N)$ Binary Search but require $O(N)$ for insertion. Hash Maps allow $O(1)$ search and insertion but lose sorted order. BSTs exist to provide a compromise: $O(\\log N)$ search *and* $O(\\log N)$ insertion, while keeping the data perfectly sorted.

## 4. Mechanics
- **Search:** Compare target to root. If smaller, go left. If larger, go right. Repeat.
- **Insert:** Traverse as if searching. When you hit a `Null` spot, create the new node there.
- **Delete:** Harder. If leaf, just delete. If one child, bypass it. If two children, find the *in-order successor* (smallest node in the right subtree), swap values, and delete the successor.
- **In-Order Traversal** of a BST guarantees returning the elements in strictly increasing order.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Best/Average: $O(\\log N)$ for Search, Insert, Delete.
  - Worst: $O(N)$ if the tree becomes completely unbalanced (a straight line).
- **Space Complexity:** $O(H)$ for the recursive call stack.

## 6. Tiny worked example
Tree: Root=5, Left=3, Right=8.
Insert `4`:
- Compare `4` to `5`. Smaller, go left.
- Compare `4` to `3`. Larger, go right.
- `3.right` is empty. Attach `4` as the right child of `3`.

## 7. Code (Python, with type hints)
```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

def search_bst(root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
    # Iterative search is space O(1)
    curr = root
    while curr:
        if target == curr.val:
            return curr
        elif target < curr.val:
            curr = curr.left
        else:
            curr = curr.right
    return None
```

## 8. Common mistakes
- Assuming a BST is self-balancing. A standard BST can become a linked list if you insert sorted data (e.g., `1, 2, 3, 4, 5`).
- Verifying a BST by only checking `node.left < node < node.right`. You must check the *entire* subtree (i.e., pass `min` and `max` bounds down the recursion).

## 9. 30-second interview answer
"A Binary Search Tree is a tree where the left child is smaller than the parent, and the right is larger. This property allows for $O(\\log N)$ search, insertion, and deletion. An in-order traversal of a BST yields sorted data. However, in the worst case, it can degrade to $O(N)$ if not balanced."

## 10. 2-minute interview answer
"Binary Search Trees maintain dynamic datasets in a sorted manner. The BST property—left descendants are strictly smaller, right are strictly greater—effectively embeds the Binary Search algorithm into a graph structure, yielding $O(\\log N)$ performance for lookups and modifications. Furthermore, iterating through a BST in-order provides a sorted array for free. The critical flaw in a standard BST is that inserting ordered data creates a degenerate tree, ruining the time complexity to $O(N)$. In production systems, we never use standard BSTs; we use self-balancing variants like AVL trees or Red-Black trees that rotate nodes to guarantee $O(\\log N)$ height."

## 11. Follow-ups
- "How do you validate if a tree is a valid BST?" (Recursive DFS, passing down `low` and `high` boundaries for each node).
- "How do you balance a BST?" (Extract elements via in-order traversal, then rebuild the tree by recursively picking the middle element as the root).

## 12. Deeper questions
- "What is an AVL Tree vs a Red-Black Tree?" (Both are self-balancing BSTs. AVL enforces strict height balance, faster for lookups. Red-Black is loosely balanced, faster for frequent insertions/deletions. C++ `std::map` uses Red-Black).

## 13. Related concepts
- **Binary Search**: The algorithm the tree is built to support.
- **B-Trees**: A generalization of BSTs optimized for disk/database storage (many children per node).

## 14. When it breaks / Edge cases
- Breaks (becomes $O(N)$) if elements are inserted in already sorted or reverse-sorted order.

## 15. Comparison with alternative approaches
- **vs Hash Map:** Hash Map gives $O(1)$ lookups, but BSTs maintain sorted order allowing range queries (e.g., "Find all values between 10 and 20"), which Hash Maps cannot do.

---
*Where this shows up in ML:* 
While vanilla BSTs are rare in ML code, advanced search trees like KD-Trees and Ball Trees (generalizations of BSTs for multi-dimensional space) are heavily used for K-Nearest Neighbors (KNN) algorithms to efficiently query the closest points in vector space without $O(N)$ scanning.
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch A - Part 3 Complete")
