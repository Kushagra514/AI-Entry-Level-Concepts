# DP on Trees

## 1. Core Idea
Post-order DFS: compute child subtree answers first, then combine at parent.
State: dp[node] = some optimal value for the subtree rooted at node.

## 2. Template
```python
def dfs(node, parent):
    result = base_case
    for child in graph[node]:
        if child == parent: continue
        child_val = dfs(child, node)
        result = combine(result, child_val)
    return result
```

## 3. Tree Diameter (LC 543)
At each node, diameter passing through it = left_depth + right_depth.
```python
def diameterOfBinaryTree(root):
    ans = [0]
    def depth(node):
        if not node: return 0
        L, R = depth(node.left), depth(node.right)
        ans[0] = max(ans[0], L + R)
        return 1 + max(L, R)
    depth(root)
    return ans[0]
```

## 4. Max Path Sum (LC 124)
Path can start/end anywhere. At each node, gain = node.val + max(0,left) + max(0,right).
```python
def maxPathSum(root):
    best = [float('-inf')]
    def dp(node):
        if not node: return 0
        l = max(dp(node.left), 0)
        r = max(dp(node.right), 0)
        best[0] = max(best[0], node.val + l + r)
        return node.val + max(l, r)   # only one branch for parent
    dp(root)
    return best[0]
```

## 5. House Robber III (LC 337)
State: (rob_root, skip_root). Can't rob adjacent nodes.
```python
def rob(root):
    def dp(node):
        if not node: return (0, 0)  # (rob, skip)
        lr, ls = dp(node.left)
        rr, rs = dp(node.right)
        rob_cur = node.val + ls + rs
        skip_cur = max(lr, ls) + max(rr, rs)
        return (rob_cur, skip_cur)
    return max(dp(root))
```

## 6. Binary Tree Cameras (LC 968)
State per node: 0=needs cover, 1=has camera, 2=covered no camera.

## 7. Rerooting Technique
Compute dp[root] in O(N), then re-root answers for all nodes in second DFS pass.
Useful when answer for each node as root is needed.

## 8. DP on General Trees (N-ary)
```python
def tree_dp(node, par, graph, vals):
    dp = [0] * 2   # dp[0]=skip, dp[1]=take
    dp[1] = vals[node]
    for child in graph[node]:
        if child == par:
            continue
        c = tree_dp(child, node, graph, vals)
        dp[0] += max(c)
        dp[1] += c[0]   # if we take node, children must be skipped
    return dp
```

## 9. Counting Paths / Subtree Sizes
sz[u] = 1 + sum(sz[child]). Used in centroid decomposition, LCA preprocessing.

## 10. Lowest Common Ancestor (Binary Lifting)
Precompute anc[node][j] = 2^j-th ancestor. dp[node][j] = dp[dp[node][j-1]][j-1].

## 11. DP on Tree + Knapsack
"Select k nodes from subtree" — dp[node][k] = max value with k nodes chosen.
Time: O(N²) with careful merging.

## 12. Interview Pattern
- Identify: what info does parent need from child?
- Return tuple from DFS when multiple states needed.
- Track global answer in a nonlocal/list variable.

## 13. Common Mistakes
- Forgetting to block parent edge in undirected tree DFS.
- Returning wrong value up the recursion (confusing subtree answer vs path answer).

## 14. Complexity
O(N) time and space for most tree DP (single pass DFS).

## 15. Key Problems List
| Problem | State |
|---------|-------|
| Diameter | depth from each node |
| Max Path Sum | max one-sided gain |
| House Robber III | (rob, skip) pair |
| Tree Cameras | 3-state coverage |
| Max Independent Set | (include, exclude) |
