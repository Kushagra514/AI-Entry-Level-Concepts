# Counting, Radix, and Bucket Sort

## 1. Definition
Three non-comparison-based sorting algorithms that bypass the $O(N \log N)$ lower bound of comparison sorts by exploiting the structure of the input data.

## 2. Intuition
- **Counting Sort:** Count how many times each value appears. Then reconstruct the sorted array by outputting each value exactly that many times. Like counting votes: 3 votes for A, 5 for B, 1 for C → output AAABBBBBС.
- **Radix Sort:** Sort digit by digit, from least significant to most significant. Like sorting words alphabetically by first sorting all last letters, then all second-to-last letters, and so on.
- **Bucket Sort:** Distribute elements into evenly-spaced ranges ("buckets"), sort each small bucket individually, then concatenate.

## 3. Why it exists
Comparison sorts are bounded by $\Omega(N \log N)$ by the information-theoretic lower bound. If we know the range or structure of the input (integers in a range, uniform floats), we can sort faster.

## 4. Mechanics
- **Counting Sort:** Array `count[v]++`. Then prefix sum to find positions. Stable in $O(N + K)$ where $K$ is value range.
- **Radix Sort:** Apply stable Counting Sort on each digit position (units, tens, hundreds). $O(d(N + K))$ where $d$ is number of digits, $K$ is digit range (usually 10).
- **Bucket Sort:** Map each element to a bucket (`index = floor(N * element/max_val)`). Sort each bucket (insertion sort). Concatenate. $O(N)$ average for uniform distributions.

## 5. Complexity (Time & Space)
| Algorithm | Time | Space | Best For |
|---|---|---|---|
| Counting | $O(N+K)$ | $O(K)$ | Integers in small range |
| Radix | $O(d(N+K))$ | $O(N+K)$ | Large integers with bounded digits |
| Bucket | $O(N)$ avg | $O(N)$ | Uniformly distributed floats |

## 6. Tiny worked example
Counting Sort on `[3, 1, 2, 3, 1]`, range 1–3:
- Count: `[0, 2, 1, 2]` (counts for values 0, 1, 2, 3).
- Output: 1, 1, 2, 3, 3.

## 7. Code (Python, with type hints)
```python
from typing import List

def counting_sort(nums: List[int], max_val: int) -> List[int]:
    count = [0] * (max_val + 1)
    for n in nums:
        count[n] += 1
    result = []
    for val, freq in enumerate(count):
        result.extend([val] * freq)
    return result

def radix_sort(nums: List[int]) -> List[int]:
    max_val = max(nums)
    exp = 1
    while max_val // exp > 0:
        # Counting sort on current digit
        output = [0] * len(nums)
        count = [0] * 10
        for n in nums:
            count[(n // exp) % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for n in reversed(nums):
            idx = (n // exp) % 10
            output[count[idx] - 1] = n
            count[idx] -= 1
        nums = output
        exp *= 10
    return nums
```

## 8. Common mistakes
- Using Counting Sort when $K >> N$ (e.g., sorting 10 numbers in range 0–1,000,000,000). You'd allocate a billion-element count array. Use Radix Sort instead.
- Bucket Sort producing wrong output for non-uniform distributions (all elements in one bucket degrades to $O(N^2)$).

## 9. 30-second interview answer
"Counting, Radix, and Bucket sort bypass the $O(N \log N)$ comparison lower bound by leveraging input structure. Counting Sort is $O(N+K)$ for integers in a range $K$. Radix Sort handles large integers digit-by-digit in $O(d \cdot N)$. Bucket Sort achieves $O(N)$ average for uniformly distributed data."

## 10. 2-minute interview answer
"These three algorithms exploit the fact that for specific input types, we can extract more information per operation than a simple 'is A greater than B?' comparison. Counting Sort works when the value range $K$ is small — it literally counts occurrences and reconstructs the sorted output, achieving $O(N+K)$ with no comparisons whatsoever. Radix Sort generalizes this to large integers by applying Counting Sort on each digit independently, using the stability of Counting Sort to preserve ordering from previous passes. Bucket Sort is the probabilistic option — for uniformly distributed inputs, it guarantees constant-time sorting on average by distributing values into proportionally-sized bins, each of which is small enough to sort trivially."

## 11. Follow-ups
- "Why must Counting Sort be stable for Radix Sort to work?" (Radix Sort sorts digit-by-digit from LSD to MSD. If the inner sort is not stable, the relative order from previous digits is lost, corrupting the final result).

## 12. Deeper questions
- "Can you sort strings with Radix Sort?" (Yes. Sort character by character from the last character to the first, treating each character as a base-256 digit).

## 13. Related concepts
- **Comparison Sorts**: Merge Sort, Quick Sort as alternatives.
- **Stable Sort**: Required property for Radix Sort's sub-sort.

## 14. When it breaks / Edge cases
- Counting/Radix fail on floating-point numbers without transformation. Negative numbers require offsetting indices.

## 15. Comparison with alternative approaches
- **vs Merge Sort:** Merge Sort is simpler, general-purpose, but bounded at $O(N \log N)$. These specialized sorts can be faster in practice when constraints are satisfied.

---
*Where this shows up in ML:*
Radix sort is used in GPU-accelerated sorting algorithms inside CUDA for building spatial data structures (like BVH trees in ray tracing for neural rendering).
