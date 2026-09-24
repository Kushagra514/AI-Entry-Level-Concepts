# Trees

## 1. Definition
A Tree is a hierarchical, acyclic data structure consisting of nodes connected by directed edges. It has a single root node, and every other node has exactly one parent.

## 2. Intuition
Think of a corporate org chart. The CEO (Root) is at the top. VPs (Children) report to the CEO. Managers report to VPs. A person cannot report to two managers (one parent rule), and there are no cycles (you can't report to someone who reports to you).

## 3. Why it exists
Linear data structures (Arrays, Linked Lists) require $O(N)$ time to search. Hash maps offer $O(1)$ search but destroy ordering. Trees exist to provide a middle ground: hierarchical ordering with the potential for $O(\log N)$ search, insertion, and deletion, while maintaining sorted relationships.

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
  - Searching/Inserting (in balanced structures): $O(\log N)$ based on Height.
- **Space Complexity:** $O(H)$ where $H$ is the height of the tree (for recursion stack). In the worst case (a stick), $H = N$.

## 6. Tiny worked example
Pre-order Traversal of:
    1
   / \
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
"A tree is a hierarchical, directed, acyclic graph. It consists of a root node with branching children. It is used to represent hierarchical data like file systems, and when structured as a Binary Search Tree, it can provide $O(\log N)$ search operations. We navigate it using DFS (Pre/In/Post-order) or BFS (Level-order)."

## 10. 2-minute interview answer
"Trees are fundamental nonlinear structures that represent hierarchical relationships. Unlike graphs, trees enforce a strict parent-child relationship with exactly one root and absolutely no cycles. The most common variant in interviews is the Binary Tree. We interact with trees using Depth-First Search for structural problems—where Pre-order is used for copying trees, In-order for getting sorted values out of a BST, and Post-order for deleting trees or calculating heights—or Breadth-First Search for level-by-level analysis. The efficiency of a tree is entirely dictated by its height; a perfectly balanced tree has a height of $\log N$, offering incredibly fast operations, while a degenerate tree degrades to a linked list with $O(N)$ operations."

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
- Degenerate trees (skewed entirely to the left or right) break the $O(\log N)$ time expectation, falling back to $O(N)$.

## 15. Comparison with alternative approaches
- **vs Linked List:** A linked list is mathematically just a unary tree (each node has exactly 1 child). Trees branch out, allowing logarithmic time complexity.

---
*Where this shows up in ML:* 
Decision Trees (and ensembles like Random Forests, XGBoost) use tree structures to partition data based on feature thresholds. The inference step for a single data point is literally traversing the tree from root to leaf based on `if/else` checks, taking $O(H)$ time.
