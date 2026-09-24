import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (DSA Qs)"')

wc("23-dsa-interview-questions/math-and-number-theory.md", r"""# Math & Number Theory Interview Questions

---

## 1. Valid Palindrome

### 1. Restate the Problem
Given a string `s`, return true if it is a palindrome, considering only alphanumeric characters and ignoring cases.

### 2. Clarify Edge Cases
- Empty string or single char? True.
- String with only punctuation? True.

### 3. Brute Force Approach
Create a new string filtering out non-alphanumeric chars and making it lowercase. Check if `new_s == new_s[::-1]`. Time: $O(N)$, Space: $O(N)$.

### 4. Key Insight
We can use Two Pointers to check in-place without creating a new string, achieving $O(1)$ space.

### 5. Optimized Approach
Initialize `l = 0`, `r = len(s) - 1`. While `l < r`: if `s[l]` is not alphanumeric, `l += 1`; if `s[r]` is not alphanumeric, `r -= 1`. If both are alphanumeric, compare them (lowercased). If they don't match, return False. Else, move both pointers.

### 6. Justification
Time: $O(N)$. Space: $O(1)$.

### 7. Code (Python)
```python
def isPalindrome(s: str) -> bool:
    l, r = 0, len(s) - 1
    
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
            
        if s[l].lower() != s[r].lower():
            return False
            
        l += 1
        r -= 1
        
    return True
```

### 8. Dry Run
`s = "A man, a plan, a canal: Panama"`
- Skips spaces and punctuation. Compares 'a' and 'a', 'm' and 'm'...
- Returns True.

### 9. Edge Cases Handled
`l < r` inside the nested while loops prevents index out of bounds if the string is entirely punctuation.

### 10. Follow-ups
- N/A.

### 11. Related Problems
Valid Palindrome II, Longest Palindromic Substring.

---

## 2. Pow(x, n)

### 1. Restate the Problem
Implement `pow(x, n)`, which calculates `x` raised to the power `n` ($x^n$).

### 2. Clarify Edge Cases
- $n = 0$? Return 1.
- $n < 0$? Calculate $1 / x^{-n}$.
- Extreme constraints? $n$ can be $-2^{31}$ to $2^{31}-1$.

### 3. Brute Force Approach
Multiply $x$ by itself $n$ times. Time: $O(N)$. Fails for $n = 2^{31}$.

### 4. Key Insight
Binary Exponentiation. $x^n$ can be calculated as $(x^2)^{n/2}$ if $n$ is even, and $x \cdot (x^2)^{n//2}$ if $n$ is odd. This halves $n$ at each step.

### 5. Optimized Approach
Handle negative $n$ by $x = 1/x$ and $n = -n$. Loop while $n > 0$. If $n$ is odd, multiply `res` by $x$. Then $x = x \cdot x$ and $n = n // 2$.

### 6. Justification
Time: $O(\log N)$. Space: $O(1)$ for iterative approach.

### 7. Code (Python)
```python
def myPow(x: float, n: int) -> float:
    if n < 0:
        x = 1 / x
        n = -n
        
    res = 1.0
    while n:
        if n % 2 == 1:
            res *= x
        x *= x
        n //= 2
        
    return res
```

### 8. Dry Run
`x = 2, n = 10`
- n=10 (even). res=1. x=4. n=5
- n=5 (odd). res=4. x=16. n=2
- n=2 (even). res=4. x=256. n=1
- n=1 (odd). res=4*256=1024. x=65536. n=0.
- Returns 1024.

### 9. Edge Cases Handled
$n=-2^{31}$ negates safely in Python (unbounded ints). In C/Java, `-n` for `MIN_VALUE` causes overflow, requiring special handling.

### 10. Follow-ups
- N/A.

### 11. Related Problems
Sqrt(x).
""")

wc("23-dsa-interview-questions/rapid-fire-dsa.md", r"""# Rapid Fire DSA Patterns

---

## 1. Find the Duplicate Number

### 1. Restate the Problem
Given an array of integers `nums` containing $n + 1$ integers where each integer is in the range $[1, n]$ inclusive. There is only one repeated number in `nums`, return this repeated number. Must solve in $O(N)$ time and $O(1)$ space without modifying the array.

### 2. Clarify Edge Cases
- Modifying array not allowed.
- Multiple duplicates of the same number are allowed (e.g., `[1, 2, 2, 2]`).

### 3. Brute Force Approach
Hash set to detect cycle. Time $O(N)$, Space $O(N)$. Fails space constraint.

### 4. Key Insight
Because the values are from 1 to $n$, we can treat the array as a linked list where `index` points to `value`. A duplicate means two indices point to the same value, creating a cycle. We can use Floyd's Tortoise and Hare algorithm.

### 5. Optimized Approach
Initialize `slow` and `fast` to `nums[0]`. Move `slow` by 1 step (`nums[slow]`) and `fast` by 2 steps (`nums[nums[fast]]`) until they meet. Then, reset `slow` to `nums[0]` and move both by 1 step. Where they meet again is the duplicate (cycle start).

### 6. Justification
Time: $O(N)$. Space: $O(1)$.

### 7. Code (Python)
```python
from typing import List

def findDuplicate(nums: List[int]) -> int:
    slow, fast = nums[0], nums[0]
    
    # Phase 1: Detect cycle
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
            
    # Phase 2: Find cycle start
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
        
    return slow
```

### 8. Dry Run
`nums = [1, 3, 4, 2, 2]`
- slow=1, fast=1
- slow=nums[1]=3, fast=nums[nums[1]]=nums[3]=2
- slow=nums[3]=2, fast=nums[nums[2]]=nums[4]=2
- Met at 2.
- slow reset to 1 (nums[0]). fast stays at 2.
- slow=nums[1]=3, fast=nums[2]=4.
- slow=nums[3]=2, fast=nums[4]=2.
- Met at 2. Return 2.

### 9. Edge Cases Handled
Cycles are guaranteed to exist per the Pigeonhole Principle.

### 10. Follow-ups
- "What if the array can't be mapped to indices (e.g., negative numbers)?" -> Can't use cycle sort. Use binary search on the range of numbers $O(N \log N)$.

### 11. Related Problems
Linked List Cycle II, Missing Number.

---

## 2. Invert a Binary Tree (Rapid Fire Edition)

### 1. Restate the Problem
Invert a binary tree.

### 5. Optimized Approach
Simple DFS. Swap left and right.

### 7. Code (Python)
```python
def invertTree(root):
    if not root: return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

---

## 3. Top K Frequent Elements (Rapid Fire Edition)

### 1. Restate the Problem
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

### 4. Key Insight
Count frequencies using a Hash Map. Then use Bucket Sort instead of a Heap for strictly $O(N)$ time.

### 7. Code (Python)
```python
from collections import Counter

def topKFrequent(nums: List[int], k: int) -> List[int]:
    count = Counter(nums)
    freq = [[] for _ in range(len(nums) + 1)]
    
    for num, c in count.items():
        freq[c].append(num)
        
    res = []
    for i in range(len(freq) - 1, 0, -1):
        for num in freq[i]:
            res.append(num)
            if len(res) == k:
                return res
```

### 6. Justification
Time: $O(N)$ (counting is $N$, bucket sorting is $N$). Space: $O(N)$ for hash map and buckets.
""")
print("DSA Qs 7 complete")
