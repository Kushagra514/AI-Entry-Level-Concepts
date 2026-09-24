# DSA Patterns One-Page Revision

## 1. Sliding Window
- **Signal:** "Find the longest/shortest/max/min *contiguous* subarray or substring."
- **Mechanics:** Expand `right` pointer to add elements. If condition violates, shrink `left` pointer until valid.
- **Time:** $O(N)$ (Each element added and removed at most once). Space: $O(1)$ or $O(K)$.
- **Trap:** Doesn't work for subsequences (non-contiguous) or if negative numbers break the monotonic property of the sum.

## 2. Two Pointers
- **Signal:** "Find a pair in a *sorted* array" or "Remove duplicates in-place".
- **Mechanics:** Start at `left=0` and `right=len-1`. If sum too big, `right--`. If sum too small, `left++`.
- **Time:** $O(N \log N)$ if sorting needed, else $O(N)$. Space: $O(1)$.

## 3. Fast & Slow Pointers (Floyd's Tortoise & Hare)
- **Signal:** "Linked list cycle", "Find middle of linked list", "Find duplicate number in array 1 to N".
- **Mechanics:** `slow` moves 1 step, `fast` moves 2 steps. If they meet, cycle exists. To find cycle start: reset `slow` to head, move both 1 step until they meet again.
- **Time:** $O(N)$. Space: $O(1)$.

## 4. Overlapping Intervals
- **Signal:** "Merge intervals", "Meeting rooms", "Insert interval".
- **Mechanics:** Sort by start time. Iterate. If `current.start <= last_merged.end`, overlap exists $\to$ `last_merged.end = max(last_merged.end, current.end)`.
- **Time:** $O(N \log N)$ (sorting bottleneck).

## 5. Monotonic Stack
- **Signal:** "Next greater element", "Next smaller element", "Daily Temperatures".
- **Mechanics:** Keep a stack of indices. For "Next Greater", stack must be strictly decreasing. If current element $>$ stack top, pop stack top (current element is its next greater).
- **Time:** $O(N)$ (each element pushed/popped once). Space: $O(N)$.

## 6. Top K Elements (Heaps)
- **Signal:** "Kth largest/smallest", "Top K frequent".
- **Mechanics:** Use a Min-Heap of size K for "Kth largest" (keeps track of the K largest seen so far, root is the Kth). 
- **Time:** $O(N \log K)$. Space: $O(K)$.

## 7. Dynamic Programming (DP)
- **Signal:** "Find the max/min ways", "Optimize a value", "Overlapping subproblems".
- **Mechanics:** Define state (what do I need to know?). Define transition (how do I move from `i` to `i+1`?). Base cases.
- **Trap:** Always try to solve it top-down with Memoization (DFS + Cache) first to understand the tree, then convert to bottom-up (Array) for space optimization.

## 8. Binary Search on Answer
- **Signal:** "Find the minimum maximum...", "Find the maximum minimum...". You can easily verify if an answer $X$ is valid in $O(N)$.
- **Mechanics:** Set `L` to min possible answer, `R` to max possible answer. `mid = (L+R)/2`. If `isValid(mid)`, search lower/higher depending on optimization goal.
