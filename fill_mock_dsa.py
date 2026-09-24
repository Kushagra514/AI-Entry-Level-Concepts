import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Mock DSA)"')

wc("24-dsa-mock-interviews/mock-dsa-01.md", r"""# DSA Mock Interview 1: Two Pointers & Arrays

## Problem Statement
**Interviewer:** Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice. Can you walk me through your thought process?

## The Interview Conversation

**Me (Clarification):** First, let me make sure I understand the constraints. Can the array contain negative numbers? And is the array sorted? 
**Interviewer:** Yes, there can be negative numbers. No, the array is not sorted.
**Me (Brute Force):** Got it. The most straightforward approach is to use a nested loop. For every element `nums[i]`, I can iterate through the rest of the array with a pointer `j` and check if `nums[i] + nums[j] == target`. But this would take $O(N^2)$ time, which isn't optimal for large arrays.
**Interviewer:** Correct. How can we improve the time complexity?
**Me (Insight):** If I'm looking at `nums[i]`, I exactly know the value I need to find to reach the target: `target - nums[i]`. If I can look up that complement in $O(1)$ time, I can solve the problem in a single pass. I can use a Hash Map to store the numbers I've seen so far and their indices.
**Interviewer:** Sounds good. What would the space complexity be?
**Me:** The space complexity would be $O(N)$ because in the worst-case scenario—where the pair is at the very end of the array—I would store $N-1$ elements in the Hash Map.
**Interviewer:** Perfect. Let's write the code.

## Code Implementation
```python
def twoSum(nums: List[int], target: int) -> List[int]:
    seen = {} # val -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

## Dry Run & Edge Cases
**Me:** Let's trace it with `nums = [3, 2, 4]` and `target = 6`.
1. `i = 0, num = 3`. Complement is `6 - 3 = 3`. Not in map. Map becomes `{3: 0}`.
2. `i = 1, num = 2`. Complement is `6 - 2 = 4`. Not in map. Map becomes `{3: 0, 2: 1}`.
3. `i = 2, num = 4`. Complement is `6 - 4 = 2`. `2` is in the map!
4. Return `[seen[2], 2]` which is `[1, 2]`.
A tricky edge case here is if the target is twice a number in the array, like `[3, 2, 4]` with target `6` hitting the first `3`. Because I check the complement in the map *before* adding the current number to the map, it correctly ignores using the same `3` twice.

## Follow-up Questions
**Interviewer:** That's completely correct. What if the input array is already sorted and we want to optimize for $O(1)$ space?
**Me:** If it's sorted, we don't need the hash map. We can use the Two Pointers technique. Place one pointer at the start `left = 0` and one at the end `right = len(nums) - 1`. If their sum is greater than the target, we decrement the right pointer to decrease the sum. If it's less, we increment the left pointer. This achieves $O(N)$ time and $O(1)$ space.
""")

wc("24-dsa-mock-interviews/mock-dsa-02.md", r"""# DSA Mock Interview 2: Linked Lists & Pointers

## Problem Statement
**Interviewer:** Given the `head` of a linked list, return the node where the cycle begins. If there is no cycle, return `null`. You must solve this in $O(1)$ space.

## The Interview Conversation

**Me (Clarification):** Does the cycle have to include the head, or can it start anywhere? And can the linked list be empty?
**Interviewer:** The cycle can start at any node. Yes, the list can be empty, which means no cycle.
**Me (Brute Force):** Without the space constraint, I would just traverse the list and add every node's memory reference to a Hash Set. The first node I encounter that is already in the set is the start of the cycle. But that uses $O(N)$ space.
**Interviewer:** Right. How do we do it in $O(1)$ space?
**Me (Insight):** I can use Floyd's Tortoise and Hare algorithm. First, I'll use a slow pointer (moves 1 step) and a fast pointer (moves 2 steps). If there is a cycle, they will eventually meet. If the fast pointer reaches the end of the list, there is no cycle.
**Interviewer:** Okay, that tells us *if* a cycle exists. How do you find the *start* of the cycle?
**Me (Math/Logic):** When they meet, the slow pointer has traveled distance $D$. The fast pointer has traveled $2D$. The difference $D$ is exactly a multiple of the cycle length. It mathematically works out that the distance from the head of the list to the cycle start is the exact same as the distance from the meeting point to the cycle start. So, if I reset the slow pointer to the head, and move both pointers 1 step at a time, they will collide exactly at the cycle start.

## Code Implementation
```python
def detectCycle(head: ListNode) -> ListNode:
    slow = head
    fast = head
    
    # Phase 1: Detect Cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            break
    else:
        # Loop finished without breaking, so no cycle
        return None
        
    # Phase 2: Find Start of Cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
        
    return slow
```

## Dry Run & Edge Cases
**Me:** Let's trace an edge case: no cycle. `1 -> 2 -> None`.
1. `slow=1, fast=1`. 
2. Loop starts because `fast(1)` and `fast.next(2)` are valid.
3. `slow=2, fast=None`.
4. Next loop check: `fast` is None. `while` loop exits normally. Hits the `else` block and returns `None`. Correct.
**Interviewer:** Very good use of Python's `while-else` construct.

## Follow-up Questions
**Interviewer:** If you only wanted to find the *length* of the cycle, how would you change the code?
**Me:** Once Phase 1 completes and `slow == fast`, I would just freeze the `slow` pointer in place. Then, I would advance the `fast` pointer 1 step at a time, keeping a counter, until it wrapped around and equalled `slow` again. The counter would be the length of the cycle.
""")

wc("24-dsa-mock-interviews/mock-dsa-03.md", r"""# DSA Mock Interview 3: Dynamic Programming

## Problem Statement
**Interviewer:** You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If it cannot be made, return `-1`. 

## The Interview Conversation

**Me (Clarification):** Can we assume we have an infinite number of each coin? And is the `amount` guaranteed to be positive?
**Interviewer:** Yes, infinite coins. The amount can be 0 or positive.
**Me (Brute Force):** A brute force approach would be to try every possible combination of coins using a recursive DFS tree. For an amount $A$, we branch out for every coin $C$. The time complexity would be $O(S^N)$ where $S$ is the amount, which is exponential and will time out.
**Interviewer:** Exactly. What makes this problem suitable for dynamic programming?
**Me (Insight):** It has optimal substructure and overlapping subproblems. To find the minimum coins for amount 11, if I try using a 5 coin, the answer is `1 + min_coins(6)`. We will calculate `min_coins(6)` multiple times across different branches, so we should memoize it or build it bottom-up.
**Interviewer:** Let's do the bottom-up approach. What will your state represent?
**Me:** I'll create a 1D array `dp` of size `amount + 1`. `dp[i]` will store the minimum number of coins needed to make amount `i`. I'll initialize the array with a dummy "infinity" value, like `amount + 1`, and set `dp[0] = 0`.

## Code Implementation
```python
def coinChange(coins: List[int], amount: int) -> int:
    # Initialize DP array with 'infinity'
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != amount + 1 else -1
```

## Dry Run & Edge Cases
**Me:** Let's trace `coins = [2], amount = 3`.
- `dp` initialized to `[0, 4, 4, 4]`.
- `a=1`: `1 - 2 < 0`. `dp[1]` remains `4`.
- `a=2`: `2 - 2 >= 0`. `dp[2] = min(4, 1 + dp[0]) = 1`.
- `a=3`: `3 - 2 >= 0`. `dp[3] = min(4, 1 + dp[1]) = min(4, 1 + 4) = 5`.
- Loop finishes. `dp[3]` is `5`. Since `5 != 4` is true, wait—ah! `5 != amount + 1`, so my return check `dp[amount] != amount + 1` would actually return `5` instead of `-1`! My initialization of `amount + 1` is safe, but because I did `1 + dp[a-c]`, a failed path `1 + 4` became `5`.
**Interviewer:** Good catch! How do you fix it?
**Me:** I should only use the result of `dp[a - c]` if it's a valid amount. Or simpler, use `float('inf')` for initialization so `1 + inf = inf`. Let me rewrite that line.

## Code Implementation (Fixed)
```python
def coinChange(coins: List[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != float('inf') else -1
```

## Follow-up Questions
**Interviewer:** Much better. What is the time and space complexity?
**Me:** Time complexity is $O(\text{amount} \times \text{len(coins)})$ because of the nested loops. Space complexity is $O(\text{amount})$ to store the DP array.
""")
print("Mock DSA complete")
