# Bit Manipulation Interview Questions

---

## 1. Single Number

### 1. Restate the Problem
Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one. Must be linear runtime and constant extra space.

### 2. Clarify Edge Cases
- All elements appear exactly twice except one.
- Negative numbers allowed.

### 3. Brute Force Approach
Hash Map counting frequencies. Time: $O(N)$, Space: $O(N)$. Violates space constraint.

### 4. Key Insight
XOR bitwise operator (`^`). 
- $A \oplus A = 0$ (XORing a number with itself cancels it out).
- $A \oplus 0 = A$.
- XOR is associative and commutative. Therefore, if we XOR all numbers, pairs will cancel to 0, leaving only the single number.

### 5. Optimized Approach
Initialize `res = 0`. Iterate through all numbers in the array and do `res ^= num`. Return `res`.

### 6. Justification
Time: $O(N)$ for one pass. Space: $O(1)$ for the `res` variable.

### 7. Code (Python)
```python
from typing import List

def singleNumber(nums: List[int]) -> int:
    res = 0
    for num in nums:
        res ^= num
    return res
```

### 8. Dry Run
`nums = [4, 1, 2, 1, 2]`
- res = 0
- 0 ^ 4 = 4
- 4 ^ 1 = 5 (0100 ^ 0001 = 0101)
- 5 ^ 2 = 7 (0101 ^ 0010 = 0111)
- 7 ^ 1 = 6 (0111 ^ 0001 = 0110)
- 6 ^ 2 = 4 (0110 ^ 0010 = 0100)
- Returns 4.

### 9. Edge Cases Handled
Single element array immediately returns the element.

### 10. Follow-ups
- "What if every element appears THREE times except one?" -> XOR won't work perfectly here. You need to sum the bits of all numbers at each position and take modulo 3 (Single Number II).

### 11. Related Problems
Single Number II, Single Number III, Missing Number.

---

## 2. Counting Bits

### 1. Restate the Problem
Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` ($0 \le i \le n$), `ans[i]` is the number of `1`'s in the binary representation of `i`. Runs in $O(N)$ time.

### 2. Clarify Edge Cases
- $n = 0$? Return `[0]`.

### 3. Brute Force Approach
For each number from 0 to $n$, count the set bits by doing `x & (x-1)` in a loop. Time: $O(N \log N)$ (since $\log N$ is number of bits).

### 4. Key Insight
DP + Bit Manipulation. The number of 1s in $i$ is related to $i \gg 1$ (which is $i / 2$). If $i$ is even, it has the same number of 1s as $i/2$ (just shifted left, adding a 0). If $i$ is odd, it has one more 1 than $i/2$.

### 5. Optimized Approach
Create a DP array `ans = [0] * (n + 1)`. Loop from 1 to `n`. `ans[i] = ans[i >> 1] + (i & 1)`.

### 6. Justification
Time: $O(N)$ since calculating each element takes $O(1)$. Space: $O(N)$ for the result array.

### 7. Code (Python)
```python
def countBits(n: int) -> List[int]:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### 8. Dry Run
`n = 5`
- i=1: dp[1] = dp[0] + 1 = 1. (binary 1)
- i=2: dp[2] = dp[1] + 0 = 1. (binary 10)
- i=3: dp[3] = dp[1] + 1 = 2. (binary 11)
- i=4: dp[4] = dp[2] + 0 = 1. (binary 100)
- i=5: dp[5] = dp[2] + 1 = 2. (binary 101)
- Returns `[0, 1, 1, 2, 1, 2]`.

### 9. Edge Cases Handled
0 handled automatically via initialization.

### 10. Follow-ups
- "Can you explain an alternative bitwise DP relation?" -> `ans[i] = ans[i & (i-1)] + 1`. This uses the trick that `i & (i-1)` removes the rightmost set bit.

### 11. Related Problems
Number of 1 Bits (Hamming Weight).
