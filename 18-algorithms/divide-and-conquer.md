# Divide and Conquer

## 1. Definition
Divide and Conquer is an algorithm design paradigm that recursively breaks a problem into two or more smaller, **independent** subproblems, solves each subproblem, and combines their solutions into a solution for the original problem.

## 2. Intuition
You are asked to count how many words are in a 1000-page book. Instead of reading it yourself, you rip it in half and hand each half to a friend. Each friend rips their half in half and hands those to two more friends. Eventually, someone is counting words on a single page. You collect and add up all the counts.

## 3. Why it exists
Certain problems can be decomposed such that solving smaller instances is dramatically easier. The key distinction from Dynamic Programming: the subproblems must be **independent** (non-overlapping). If they overlap, memoization (DP) is needed.

## 4. Mechanics
Three steps in every D&C algorithm:
1. **Divide:** Split the problem into subproblems of the same type.
2. **Conquer:** Recursively solve each subproblem. Base case: problem is small enough to solve directly.
3. **Combine:** Merge the subproblem solutions into the final answer.

Time complexity is analyzed using the **Master Theorem**: $T(N) = aT(N/b) + f(N)$, where $a$ = subproblems, $b$ = factor of reduction, $f(N)$ = combine cost.

## 5. Complexity (Time & Space)
- **Merge Sort:** $T(N) = 2T(N/2) + O(N)$ → $O(N \log N)$.
- **Binary Search:** $T(N) = T(N/2) + O(1)$ → $O(\log N)$.
- **Karatsuba Multiplication:** $T(N) = 3T(N/2) + O(N)$ → $O(N^{1.585})$.
- **Space:** $O(\log N)$ call stack for balanced splits.

## 6. Tiny worked example
Count inversions in `[3, 1, 2]` (pairs where `arr[i] > arr[j]` for `i < j`).
- Divide: `[3, 1]` and `[2]`.
- Merge `[3,1]` → `[1, 3]`, count 1 inversion (`3 > 1`).
- Merge `[1, 3]` and `[2]` → `[1, 2, 3]`, count 1 inversion (`3 > 2`).
- Total: 2 inversions.

## 7. Code (Python, with type hints)
```python
from typing import List

# Classic D&C: Count Inversions (via Merge Sort)
def count_inversions(nums: List[int]) -> int:
    if len(nums) <= 1:
        return 0
    
    mid = len(nums) // 2
    left, right = nums[:mid], nums[mid:]
    
    count = count_inversions(left) + count_inversions(right)
    
    # Merge and count cross-inversions
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            nums[k] = left[i]; i += 1
        else:
            count += len(left) - i  # All remaining left elements > right[j]
            nums[k] = right[j]; j += 1
        k += 1
    nums[k:] = left[i:] or right[j:]
    return count
```

## 8. Common mistakes
- Applying D&C when subproblems **overlap** (should be DP instead).
- Missing the base case, causing infinite recursion.
- In Merge Sort: allocating new arrays in every recursive call leads to $O(N \log N)$ space usage rather than $O(N)$.

## 9. 30-second interview answer
"Divide and Conquer splits a problem into independent subproblems, solves them recursively, and combines the results. Examples include Merge Sort, Quick Sort, Binary Search, and the Fast Fourier Transform. Its time complexity is analyzed with the Master Theorem."

## 10. 2-minute interview answer
"Divide and Conquer is the paradigm behind the most important algorithms in computer science. Its power comes from exploiting recursive self-similarity: a sorted array can be split into two sorted halves. The key requirement is subproblem independence — unlike DP, once we split, neither half depends on the other's intermediate state. The combine step is where the real work happens: Merge Sort's $O(N)$ merge pass is what gives it $O(N \log N)$ total complexity. The Master Theorem provides an $O(1)$ mechanical way to analyze any D&C recurrence relation of the form $T(N) = aT(N/b) + f(N)$ without unrolling the recursion. Beyond sorting, D&C underlies matrix multiplication (Strassen's), computational geometry (closest pair of points), and the Fast Fourier Transform."

## 11. Follow-ups
- "State the three cases of the Master Theorem." (1: $f(N) = O(N^{\log_b a - \epsilon})$ → $T = O(N^{\log_b a})$. 2: $f(N) = O(N^{\log_b a})$ → $T = O(N^{\log_b a} \log N)$. 3: $f(N) = \Omega(N^{\log_b a + \epsilon})$ and regularity → $T = O(f(N))$).

## 12. Deeper questions
- "How does the Closest Pair of Points problem use D&C to beat $O(N^2)$?" (Split points by x-coordinate. Recurse on each half. The tricky combine step checks points near the center strip in $O(N)$ time using a geometric argument).

## 13. Related concepts
- **Merge Sort / Quick Sort**: The canonical D&C sorts.
- **Dynamic Programming**: Used when subproblems overlap.

## 14. When it breaks / Edge cases
- Unbalanced splits (like Quick Sort's worst case with a bad pivot) destroy the $O(\log N)$ depth guarantee and degrade to $O(N^2)$.

## 15. Comparison with alternative approaches
- **vs DP:** If subproblems are non-overlapping → D&C. If overlapping → DP. D&C does not cache; DP does.

---
*Where this shows up in ML:*
Distributed training (like Data Parallelism in PyTorch DDP) is conceptually Divide and Conquer: split the batch across GPUs, compute gradients independently, combine (all-reduce) the gradients.
