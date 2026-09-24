# Search Variants

## 1. Definition
Variants of the classic Binary Search adapted for problems where the answer isn't an exact match but a boundary, a rotated array, or a 2D matrix.

## 2. Intuition
Binary Search is not just "find this value". It is a general-purpose tool for cutting a search space in half when the space is **monotone** (sorted or has a clear left/right boundary). All variants follow the same skeleton; only the condition and what you do with the bounds changes.

## 3. Why it exists
Interviewers rarely ask for plain Binary Search. Instead they dress it up: "the array was rotated", "find the leftmost position", "search a matrix". These variants test whether you have a deep mental model of the algorithm vs. a surface-level memorization.

## 4. Mechanics
**Key template (Left Boundary / Leftmost True):**
```
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    if condition(mid):  # True = valid half
        hi = mid
    else:
        lo = mid + 1
return lo
```
- **Find exact value:** standard `if arr[mid] == target`.
- **Leftmost occurrence:** move `hi = mid` even on match (keep searching left).
- **Rightmost occurrence:** move `lo = mid + 1` on match (keep searching right).
- **Rotated sorted array:** determine which half is sorted, then narrow bounds accordingly.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(\log N)$ for all variants.
- **Space Complexity:** $O(1)$ iterative; $O(\log N)$ recursive.

## 6. Tiny worked example
Leftmost occurrence of `2` in `[1, 2, 2, 2, 3]`:
- `lo=0, hi=4`. `mid=2`, `arr[2]=2`. Match! `hi=2`.
- `lo=0, hi=2`. `mid=1`, `arr[1]=2`. Match! `hi=1`.
- `lo=0, hi=1`. `mid=0`, `arr[0]=1`. No match. `lo=1`.
- `lo==hi==1`. Return `1`. (Correct: index of first `2`.)

## 7. Code (Python, with type hints)
```python
from typing import List

def search_rotated(nums: List[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        # Left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

def find_leftmost(nums: List[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(nums) and nums[lo] == target else -1
```

## 8. Common mistakes
- Off-by-one errors in `lo/hi` initialization and update: use `hi = n` (exclusive) for boundary searches and `hi = n-1` (inclusive) for exact searches.
- In rotated array search, forgetting to handle duplicates. Duplicates require `lo += 1` fallback when `nums[lo] == nums[mid]`.

## 9. 30-second interview answer
"Binary Search variants reuse the same halving skeleton but adapt the condition and bound updates. Leftmost/rightmost occurrence shifts bounds even on a match. Rotated-array search checks which half is sorted to decide which side to eliminate. All variants remain $O(\log N)$."

## 10. 2-minute interview answer
"The key to all Binary Search variants is internalizing a single invariant: at every step, the answer lies within `[lo, hi]`. In leftmost occurrence, when we find a match at `mid`, we don't immediately return — we keep the match as a candidate but continue searching left by setting `hi = mid`. When searching a rotated sorted array, we cannot directly compare `arr[mid]` to the target, because the array wraps around. Instead, we first determine which of the two halves is cleanly sorted by comparing `arr[lo]` to `arr[mid]`. Once we know which half is sorted, we check if the target lies within that half's bounds. If yes, we search there; otherwise, we search the other half. This restores the standard Binary Search logic and preserves $O(\log N)$."

## 11. Follow-ups
- "How do you binary-search a 2D matrix where each row is sorted?" (Treat the matrix as a flat array of size `M*N`. Map `mid` to `(mid // N, mid % N)` for the actual cell access).

## 12. Deeper questions
- "What is Exponential Search?" (For sorted arrays of unknown length. Double the index from 1, 2, 4, 8… until you overshoot, then Binary Search within `[prev, current]`. $O(\log N)$ overall).

## 13. Related concepts
- **Binary Search on Answer**: Binary searching the answer space rather than an array index.
- **Two Pointers**: An alternative for some sorted-array search problems.

## 14. When it breaks / Edge cases
- Rotated array with all duplicates (`[2, 2, 2, 2]`) degrades to $O(N)$ since you can't determine which half is sorted.

## 15. Comparison with alternative approaches
- **vs Hash Map:** Hash Map gives $O(1)$ exact lookup but requires $O(N)$ preprocessing space. Binary Search requires only sorted input and $O(1)$ space.

---
*Where this shows up in ML:*
Hyperparameter grid searches use binary-search-style pruning in tools like Optuna (Tree-structured Parzen Estimator).
