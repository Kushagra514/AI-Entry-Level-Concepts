# DSA Mock Interview 1: Two Pointers & Arrays

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
