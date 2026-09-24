# Binary Search Trees (BST)

## 1. Definition
A Binary Search Tree is a binary tree where every node satisfies a specific property: all nodes in its left subtree have smaller values, and all nodes in its right subtree have larger values.

## 2. Intuition
It's the data structure equivalent of the Binary Search algorithm. If you are looking for the number 50 and the root is 100, you know instantly you only need to search the left side of the tree. Every step down halves the search space.

## 3. Why it exists
Arrays allow $O(\log N)$ Binary Search but require $O(N)$ for insertion. Hash Maps allow $O(1)$ search and insertion but lose sorted order. BSTs exist to provide a compromise: $O(\log N)$ search *and* $O(\log N)$ insertion, while keeping the data perfectly sorted.

## 4. Mechanics
- **Search:** Compare target to root. If smaller, go left. If larger, go right. Repeat.
- **Insert:** Traverse as if searching. When you hit a `Null` spot, create the new node there.
- **Delete:** Harder. If leaf, just delete. If one child, bypass it. If two children, find the *in-order successor* (smallest node in the right subtree), swap values, and delete the successor.
- **In-Order Traversal** of a BST guarantees returning the elements in strictly increasing order.

## 5. Complexity (Time & Space)
- **Time Complexity:** 
  - Best/Average: $O(\log N)$ for Search, Insert, Delete.
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
"A Binary Search Tree is a tree where the left child is smaller than the parent, and the right is larger. This property allows for $O(\log N)$ search, insertion, and deletion. An in-order traversal of a BST yields sorted data. However, in the worst case, it can degrade to $O(N)$ if not balanced."

## 10. 2-minute interview answer
"Binary Search Trees maintain dynamic datasets in a sorted manner. The BST property—left descendants are strictly smaller, right are strictly greater—effectively embeds the Binary Search algorithm into a graph structure, yielding $O(\log N)$ performance for lookups and modifications. Furthermore, iterating through a BST in-order provides a sorted array for free. The critical flaw in a standard BST is that inserting ordered data creates a degenerate tree, ruining the time complexity to $O(N)$. In production systems, we never use standard BSTs; we use self-balancing variants like AVL trees or Red-Black trees that rotate nodes to guarantee $O(\log N)$ height."

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
