# Bit Manipulation

## 1. Definition
Bit manipulation involves applying logical operations directly to the individual bits (0s and 1s) of binary numbers to achieve highly optimized computational tasks.

## 2. Intuition
Instead of using math operators like `+`, `-`, `*`, or `/`, you act like an electrician flipping microscopic switches. Because CPUs execute these bitwise operations at the hardware level in a single clock cycle, it is the fastest possible way to compute certain mathematical or logical relationships.

## 3. Why it exists
It exists to maximize performance and minimize memory. Storing 32 boolean flags in an array takes 32 bytes. Storing them in a single 32-bit integer takes 4 bytes. Hardware drivers, cryptography, and ultra-optimized algorithmic solutions rely heavily on bits.

## 4. Mechanics
- **AND (`&`):** 1 if both bits are 1. Used to mask/extract bits.
- **OR (`|`):** 1 if either bit is 1. Used to set bits.
- **XOR (`^`):** 1 if bits are different. $x \oplus x = 0$. $x \oplus 0 = x$.
- **NOT (`~`):** Flips all bits.
- **Left Shift (`<<`):** Shifts bits left, filling with 0. Equivalent to multiplying by $2^k$.
- **Right Shift (`>>`):** Shifts bits right. Equivalent to integer division by $2^k$.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(1)$ for single operations.
- **Space Complexity:** $O(1)$.

## 6. Tiny worked example
Is a number even or odd?
Math: `n % 2 == 0`. (Division is a slow CPU instruction).
Bitwise: `n & 1 == 0`. (Fast).
If `n = 6` (110 in binary): `110 & 001 = 000` (Even).
If `n = 5` (101 in binary): `101 & 001 = 001` (Odd).

## 7. Code (Python, with type hints)
```python
def bit_tricks(n: int) -> int:
    # Is Even?
    is_even = (n & 1) == 0
    
    # Multiply by 2
    mult2 = n << 1
    
    # Clear the lowest set bit (useful for counting 1s)
    # 1010 -> 1000
    n = n & (n - 1)
    
    # Toggle the i-th bit
    i = 2
    n = n ^ (1 << i)
    
    return n
```

## 8. Common mistakes
- **Precedence errors:** Bitwise operators have very low precedence in Python/C++. Always wrap them in parentheses. E.g., `n & 1 == 0` evaluates as `n & (1 == 0)` in some languages, not `(n & 1) == 0`.
- Forgetting that negative numbers in Python have an infinite number of leading 1s (because Python has arbitrary-precision integers), making operations like `~` tricky without explicit 32-bit masking (`n & 0xFFFFFFFF`).

## 9. 30-second interview answer
"Bit manipulation leverages low-level CPU instructions like AND, OR, XOR, and Shifts to solve problems with maximum efficiency. It's commonly used to represent sets of booleans in $O(1)$ space, calculate powers of 2, or cancel out duplicate elements using the XOR property."

## 10. 2-minute interview answer
"Bit manipulation is an advanced optimization technique that replaces arithmetic with raw logical circuitry operations. The most critical operator in interviews is XOR (`^`), because of its cancellation property: $x \oplus x = 0$. This solves the classic 'Single Number' problem in $O(N)$ time and $O(1)$ space. Another vital pattern is using integers as 'Bitmasks' to represent subsets; a 32-bit integer can act as a Hash Set of 32 boolean flags, radically compressing DP states. Finally, Brian Kernighan’s algorithm `n & (n - 1)` drops the lowest set bit, allowing us to count 1-bits in time proportional to the number of set bits, rather than the total bits."

## 11. Follow-ups
- "How do you swap two variables without a temporary variable?" (`a = a^b`, `b = a^b`, `a = a^b`).

## 12. Deeper questions
- "How do you isolate the rightmost 1-bit?" (`n & -n`. Two's complement makes `-n` equal to `~n + 1`).

## 13. Related concepts
- **DP with Bitmasking**: Uses integers to track subset states.

## 14. When it breaks / Edge cases
- Python handles negative numbers differently than C++/Java because it lacks a fixed 32-bit limit, so you often need to manually mask with `0xFFFFFFFF`.

## 15. Comparison with alternative approaches
- **vs Modulo/Division:** Bitwise AND/Shifts are significantly faster on the CPU level.

---
*Where this shows up in ML:* 
In ultra-low precision Deep Learning (e.g., 1-bit or 2-bit quantization, BitNet), matrix multiplications are replaced entirely by bitwise XNOR and POPCOUNT operations, drastically accelerating hardware inference.
