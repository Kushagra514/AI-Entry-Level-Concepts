# DSA Mock Interview — Session 1

**Time:** 45 minutes | **Difficulty:** Medium | **Topics:** Arrays, Trees, DP

---

## Problem 1: Maximum Subarray (20 min)

**Interviewer:** "Given an integer array, find the contiguous subarray with the largest sum."

### Step 1 — Restate
"Find contiguous subarray (at least one element) with maximum sum. Return the sum."

### Step 2 — Clarify
- "Can all elements be negative?" → Yes. Return the maximum single element.
- "Is an empty subarray allowed?" → No. At least one element.

### Step 3 — Brute Force
Try all subarrays: $O(N^2)$ or $O(N^3)$. Too slow.

### Step 4 — Insight (Kadane's Algorithm)
"At each position, I make a binary choice: extend the existing subarray or start fresh. If the existing sum is negative, it only hurts to carry it forward."

### Step 5 — Optimized Approach
Maintain `curr_sum` (sum of best subarray ending here) and `max_sum`. At each element: `curr_sum = max(num, curr_sum + num)`. Update `max_sum`.

### Step 6 — Justification
$O(N)$ time, $O(1)$ space. Single pass, one decision per element.

### Step 7 — Code
```python
from typing import List

def maxSubArray(nums: List[int]) -> int:
    max_sum = curr_sum = nums[0]  # Initialize with first element
    
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)  # Extend or restart
        max_sum = max(max_sum, curr_sum)
    
    return max_sum
```

### Step 8 — Dry Run
`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`
- num=-2: curr=-2, max=-2
- num=1: curr=max(-2+1,1)=1, max=1
- num=-3: curr=max(1-3,-3)=-2, max=1
- num=4: curr=max(-2+4,4)=4, max=4
- num=-1: curr=3, max=4
- num=2: curr=5, max=5
- num=1: curr=6, max=6 ✓

### Step 9 — Edge Cases
- All negative → returns least negative (correctly handled by Kadane's)
- Single element → returns that element

### Step 10 — Follow-ups
"Return the subarray itself?" → Track start/end indices: reset `start = i` when restarting, update end when `max_sum` is updated.
"Circular array?" → `max(Kadane(nums), total_sum - min_subarray_sum)`.

---

## Problem 2: Lowest Common Ancestor of a BST (15 min)

**Interviewer:** "Given a BST and two nodes p and q, find their LCA."

### Key Insight
"In a BST, if both p and q are less than the current node, the LCA is in the left subtree. If both are greater, it's in the right subtree. Otherwise, the current node is the LCA."

### Code
```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = self.right = None

def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left    # Both in left subtree
        elif p.val > root.val and q.val > root.val:
            root = root.right   # Both in right subtree
        else:
            return root         # Split point = LCA
    return None
```

**Complexity:** $O(H)$ time, $O(1)$ space. $H = \log N$ for balanced BST.

**Follow-up:** "General binary tree (not BST)?" → DFS returning LCA: if left and right both return non-None, current is LCA. $O(N)$ time.

---

## Problem 3: Coin Change (10 min)

**Interviewer:** "Given coin denominations and an amount, find minimum coins needed."

### Key Insight
"Optimal substructure: min coins for amount $a$ = 1 + min coins for $a - \text{coin}$, for each coin."

### Code
```python
def coinChange(coins: List[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins for amount 0
    
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Complexity:** $O(\text{amount} \times \text{coins})$ time, $O(\text{amount})$ space.

**Follow-up:** "Why is Greedy wrong?" → Coins [1, 3, 4], amount 6: Greedy picks 4→then two 1s (3 coins). DP finds 3+3 (2 coins). Greedy only works for canonical coin systems like USD.
