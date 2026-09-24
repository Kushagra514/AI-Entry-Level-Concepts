# Hashing Interview Questions

---

## 1. Group Anagrams

### 1. Restate the Problem
Given an array of strings `strs`, group the anagrams together.

### 2. Clarify Edge Cases
- Empty array? Return `[]`.
- Strings are lowercase English letters.

### 3. Brute Force Approach
Compare every string with every other string using a helper `isAnagram` function. Time: $O(N^2 \cdot K)$.

### 4. Key Insight
Anagrams share the same "signature". If we sort an anagram (e.g., `eat` -> `aet`, `tea` -> `aet`), they become identical. We can use this sorted version as a key in a Hash Map.

### 5. Optimized Approach
Initialize a `defaultdict(list)`. For each string, sort its characters to create a key. Append the original string to the list corresponding to that key. Finally, return the map's values.

### 6. Justification
Time: $O(N \cdot K \log K)$ where $N$ is number of strings and $K$ is max length of a string (due to sorting). Space: $O(N \cdot K)$ to store the map.

### 7. Code (Python)
```python
from collections import defaultdict
from typing import List

def groupAnagrams(strs: List[str]) -> List[List[str]]:
    ans = defaultdict(list)
    
    for s in strs:
        # Sort string to use as key
        key = tuple(sorted(s))
        ans[key].append(s)
        
    return list(ans.values())
```

### 8. Dry Run
`["eat", "tea", "tan"]`
- "eat" -> sorted: ('a','e','t'). ans[aet] = ["eat"]
- "tea" -> sorted: ('a','e','t'). ans[aet] = ["eat", "tea"]
- "tan" -> sorted: ('a','n','t'). ans[ant] = ["tan"]
- Return `[["eat", "tea"], ["tan"]]`.

### 9. Edge Cases Handled
Empty strings sort to `()` and group together correctly.

### 10. Follow-ups
- "Can you optimize the $O(K \log K)$ sorting step?" -> Yes, use a character count tuple of size 26 as the key instead of sorting. Time drops to $O(N \cdot K)$.

### 11. Related Problems
Valid Anagram.

---

## 2. Longest Consecutive Sequence

### 1. Restate the Problem
Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. Must run in $O(N)$ time.

### 2. Clarify Edge Cases
- Empty array? Return 0.
- Duplicates? They don't increase sequence length.

### 3. Brute Force Approach
Sort the array and count consecutive elements. Time: $O(N \log N)$. Fails the $O(N)$ constraint.

### 4. Key Insight
A Hash Set provides $O(1)$ lookups. A sequence only starts when `num - 1` is NOT in the set. If we only start counting from the true "start" of a sequence, we avoid redundant work.

### 5. Optimized Approach
Add all numbers to a Hash Set. Iterate through the set. If `num - 1` is in the set, skip it (it's not the start). If `num - 1` is NOT in the set, it's the start. Loop checking if `num + 1`, `num + 2`, etc., are in the set. Update max length.

### 6. Justification
Time: $O(N)$. Even though there's a nested while loop, the inner loop only runs for the *start* of a sequence, meaning each number is visited at most twice. Space: $O(N)$ for the set.

### 7. Code (Python)
```python
def longestConsecutive(nums: List[int]) -> int:
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Only check if it's the start of a sequence
        if (num - 1) not in num_set:
            current_num = num
            current_streak = 1
            
            while (current_num + 1) in num_set:
                current_num += 1
                current_streak += 1
                
            longest = max(longest, current_streak)
            
    return longest
```

### 8. Dry Run
`nums = [100, 4, 200, 1, 3, 2]`
- set: {1, 2, 3, 4, 100, 200}
- num=1: 0 not in set. while 2,3,4 in set -> streak=4. max=4.
- num=2: 1 is in set. Skip.
- num=3: 2 is in set. Skip.
- num=4: 3 is in set. Skip.
- num=100: 99 not in set. streak=1.
- Return 4.

### 9. Edge Cases Handled
Empty arrays handled smoothly. Duplicates eliminated by `set()`.

### 10. Follow-ups
- N/A.

### 11. Related Problems
Find All Numbers Disappeared in an Array.
