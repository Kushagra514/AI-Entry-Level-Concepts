# DP on Trees

## 1. Definition
DP on Trees (or Tree DP) is a pattern where dynamic programming is performed over the nodes of a tree structure, typically using a post-order Depth First Search (DFS) where a node's state depends on the computed states of its children.

## 2. Intuition
To know the optimal answer for a subtree rooted at node $U$, you first need the optimal answers for all subtrees rooted at $U$'s children. You gather the answers from the children, combine them with $U$'s own value, and return the result to $U$'s parent.

## 3. Why it exists
Trees inherently possess overlapping subproblems and optimal substructure. Many tree problems (like finding the largest independent set, or the maximum path sum) can be solved by deciding whether to include a node based on the optimal decisions made in its subtrees.

## 4. Mechanics
- **Traversal:** Post-order DFS. Process children first, then the parent.
- **State:** Usually `dp[u]` or `dp[u][state]`. For example, in "House Robber III", state is `(include_node, exclude_node)`.
- **Transitions:** At node `u`, iterate through its children `v`. `dp[u]` is updated using `dp[v]`.
- **Rerooting:** A more advanced technique to find the answer for *every* node as the root in $O(N)$ time. Do one bottom-up pass, then one top-down pass to pass the parent's contribution down.

## 5. Complexity (Time & Space)
- **Time:** $O(N)$ because every node and edge is visited a constant number of times.
- **Space:** $O(N)$ for the recursion stack and the DP array.

## 6. Tiny worked example
Tree Diameter (longest path). For a node $U$, the longest path passing through $U$ is `highest_child_depth + second_highest_child_depth`.
DFS returns the max depth of a subtree. As we compute this, we update a global `max_diameter` variable.

## 7. Code (Python)
```python
# House Robber III (Max independent set weight in a tree)
def rob(root):
    # Returns (max_if_robbed, max_if_not_robbed)
    def dfs(node):
        if not node:
            return (0, 0)
            
        left_rob, left_not = dfs(node.left)
        right_rob, right_not = dfs(node.right)
        
        # If we rob this node, we CANNOT rob its children
        rob_this = node.val + left_not + right_not
        
        # If we don't rob this node, we take the max of children (robbed or not)
        not_rob_this = max(left_rob, left_not) + max(right_rob, right_not)
        
        return (rob_this, not_rob_this)
        
    return max(dfs(root))
```

## 8. Common mistakes
- Passing states *down* the tree instead of passing results *up*. Top-down DP with memoization works, but bottom-up (returning tuples from DFS) is usually much cleaner.
- Modifying a global maximum incorrectly (e.g., forgetting that a path can go up through the parent and back down).

## 9. 30-second interview answer
"DP on Trees solves problems by computing optimal states for subtrees. It uses a post-order DFS where a parent node's DP state is calculated by aggregating the DP states returned by its children. It is highly efficient, running in $O(N)$ time, and is used for problems like Tree Diameter or Maximum Path Sum."

## 10. 2-minute interview answer
"Tree DP leverages the strict hierarchical structure of trees. Because there are no cycles, the subproblems are neatly isolated into subtrees. The standard pattern is a post-order DFS: we recursively call the DFS on a node's children, and the children return their optimal states. The parent node then combines these states to form its own optimal state. For example, in calculating the Maximum Path Sum, a node needs to know the maximum straight path down into its left and right subtrees. It combines them to see if the path arching over itself is the global maximum, but only returns the maximum single straight path up to its own parent. A more complex variant is 'Rerooting DP', used when you need to compute an answer for every node acting as the root. Instead of running an $O(N)$ DFS for every node (which is $O(N^2)$), we do it in two $O(N)$ passes: one bottom-up to get subtree answers, and one top-down to pass the remaining graph's answer from parent to child."

## 11. Follow-ups
- "What if the tree is an n-ary tree?" (The logic is identical. Instead of `left` and `right`, you iterate over the `children` array and accumulate the results).

## 12. Deeper questions
- "Explain the two passes of Rerooting DP." (Pass 1 (bottom-up): Compute the DP state for the subtree of every node assuming an arbitrary root, say 0. Pass 2 (top-down): To find the answer for node `v` when rooted at `v`, take the answer for its parent `u` (when rooted at `u`), subtract `v`'s subtree contribution to `u`, and add this remaining tree contribution to `v`'s state).

## 13. Related concepts
- **Graph DFS**: Tree DP is essentially post-order DFS with state combination.
- **State Machine DP**: Nodes often have multiple states (robbed/not robbed).

## 14. When it breaks / Edge cases
- Unusually deep trees (like a linked list) will cause recursion depth limit errors (`RecursionError` in Python). May need to increase recursion limit or use an explicit stack.

## 15. Comparison with alternative approaches
- **Tree DP vs Graph DP:** Trees are Directed Acyclic Graphs (if directed away from root). Tree DP doesn't need a `visited` set if you just pass the `parent` to avoid traversing backward.

---
*Where this shows up in ML:*
Belief propagation in tree-structured probabilistic graphical models.
