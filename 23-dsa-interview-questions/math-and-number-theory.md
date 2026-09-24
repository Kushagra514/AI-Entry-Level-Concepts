# Math & Number Theory Interview Questions

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
