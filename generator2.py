import os

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Flesh out {os.path.basename(path)}"')

files_to_update = {}

files_to_update["16-dsa-foundations/big-o-notation.md"] = """# Big-O Notation & Complexity Analysis

## 1. Definition
Big-O notation is a mathematical framework used in computer science to describe the upper bound of an algorithm's runtime or space requirements as the input size ($n$) approaches infinity.

## 2. Intuition
Imagine you are downloading a file from the internet versus physically mailing a hard drive. Downloading speed depends on the file size (O(n)), but mailing a hard drive takes the same amount of time regardless of whether it's a 1GB or 1TB drive (O(1)). Big-O strips away hardware speeds and focuses on how the "work" scales.

## 3. Why it exists
Before standardized complexity analysis, engineers compared algorithms by timing them on specific hardware. This was inconsistent. Big-O was adopted to provide a hardware-agnostic, mathematical way to compare algorithms purely based on their scaling behavior.

## 4. Mechanics
We count the number of fundamental operations (comparisons, assignments) an algorithm makes relative to the input size $n$.
We drop constants: $O(2n) \\rightarrow O(n)$.
We drop non-dominant terms: $O(n^2 + n) \\rightarrow O(n^2)$.
Common complexities (best to worst): $O(1) < O(\\log n) < O(n) < O(n \\log n) < O(n^2) < O(2^n) < O(n!)$.

## 5. Complexity (Time & Space)
- **Time Complexity:** Describes how execution time scales. 
- **Space Complexity:** Describes how auxiliary memory scales (excluding the memory required to hold the input itself).

## 6. Tiny worked example
```python
def print_pairs(arr):
    for i in arr:           # Runs n times
        for j in arr:       # Runs n times
            print(i, j)     # Total: n * n = n^2 operations
```
This is $O(n^2)$ time.

## 7. Code (Python, with type hints)
```python
from typing import List

# O(1) Time
def get_first(arr: List[int]) -> int:
    return arr[0] if arr else -1

# O(n) Time
def linear_search(arr: List[int], target: int) -> bool:
    for num in arr:
        if num == target:
            return True
    return False
```

## 8. Common mistakes
- Confusing Best Case, Worst Case, and Average Case with Big-O, Big-Omega, and Big-Theta. Big-O is an upper bound; it can apply to the best case, but we usually use it to describe the worst case.
- Including the output array in space complexity (some interviewers exclude it, always clarify).

## 9. 30-second interview answer
"Big-O notation describes the asymptotic upper bound of an algorithm's time or space complexity. It tells us how the algorithm's performance scales as the input size grows infinitely large, ignoring constants and lower-order terms."

## 10. 2-minute interview answer
"Big-O notation is our theoretical framework for evaluating algorithm efficiency independent of hardware. We use it to describe how the number of operations or amount of auxiliary memory grows relative to the input size, $N$. We focus on the worst-case scenario and drop constants and lower-order terms because, at massive scale, the highest-order term dominates. For instance, an $O(N^2)$ algorithm might be faster than an $O(N \\log N)$ algorithm for small $N$ due to constant factors, but as $N$ grows, the $O(N \\log N)$ approach will inevitably win. Understanding Big-O is critical for building scalable systems, as it prevents us from deploying code that will catastrophically degrade under load."

## 11. Follow-ups
- "What's the difference between Big-O and Big-Theta?" (Big-O is upper bound, Big-Theta is tight bound).
- "Can an O(n) algorithm be slower than an O(n^2) algorithm?" (Yes, for small inputs if the constant factors in O(n) are massive).

## 12. Deeper questions
- "Explain Amortized time complexity." (When an operation is occasionally very slow but usually very fast, like dynamic array resizing, we average the cost over a sequence of operations).

## 13. Related concepts
- **Master Theorem**: Used to calculate Big-O for recursive divide-and-conquer algorithms.

## 14. When it breaks / Edge cases
- For very small $n$, Big-O is useless. Caching effects and constant factors dominate. (e.g., Insertion Sort $O(n^2)$ beats Merge Sort $O(n \\log n)$ for tiny arrays).

## 15. Comparison with alternative approaches
- Instead of Big-O, we could use empirical benchmarking, but that doesn't guarantee future scaling behavior.

---
*Where this shows up in ML:* 
Big-O is critical in ML system design. For example, standard Self-Attention in Transformers has a time and space complexity of $O(n^2)$ with respect to sequence length $n$. This quadratic scaling is the primary bottleneck in processing long contexts, leading to innovations like FlashAttention or linear attention approximations.
"""

files_to_update["20-dsa-patterns/pattern-sliding-window.md"] = """# Pattern: Sliding Window

## 1. Definition
The Sliding Window pattern involves creating a "window" over a subset of an array or string (often defined by two pointers, `left` and `right`) and shifting that window to solve problems involving contiguous subarrays or substrings.

## 2. Intuition
Imagine looking at a long landscape through a small rectangular window. Instead of picking up the window and moving it to every possible spot from scratch, you slowly slide it to the right, adding a new slice of the landscape on the right and losing a slice on the left. You only update what changed at the edges.

## 3. Why it exists
It exists to optimize $O(n^2)$ brute-force solutions that repeatedly evaluate overlapping subarrays. By keeping a running state of the window, we reuse the overlapping computations.

## 4. Mechanics
1. Initialize `left` and `right` pointers at the start (or `window_start`, `window_end`).
2. Expand the window by moving `right` and adding `arr[right]` to the window's state.
3. If the window violates a condition (or reaches a fixed size), shrink it by moving `left` and removing `arr[left]` from the state until the condition is valid again.
4. Update the global answer (e.g., max length, min length) at valid states.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N)$ - Both `left` and `right` pointers only move forward. Each element is processed at most twice (once added, once removed).
- **Space Complexity:** $O(1)$ to $O(K)$ depending on the state being tracked (e.g., a hash map of character counts).

## 6. Tiny worked example
Find max sum of subarray of size 3 in `[2, 1, 5, 1, 3, 2]`
- Window `[2, 1, 5]`: sum = 8. Max = 8.
- Slide right: add `1`, remove `2`. Window `[1, 5, 1]`: sum = 7. Max = 8.
- Slide right: add `3`, remove `1`. Window `[5, 1, 3]`: sum = 9. Max = 9.

## 7. Code (Python, with type hints)
```python
from typing import List

def max_sub_array_of_size_k(k: int, arr: List[int]) -> int:
    max_sum = 0
    window_sum = 0
    window_start = 0

    for window_end in range(len(arr)):
        window_sum += arr[window_end]  # add the next element

        # slide the window if we've hit the size k
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]  # subtract the element going out
            window_start += 1  # slide the window ahead
            
    return max_sum
```

## 8. Common mistakes
- Confusing *fixed* window (size $K$ is given) with *dynamic* window (shrink/expand based on a condition like sum < $S$).
- Forgetting to remove the `arr[left]` element from the state when shrinking the window.
- Off-by-one errors when checking window size (`window_end - window_start + 1`).

## 9. 30-second interview answer
"Sliding Window is an optimization technique used for problems involving contiguous subarrays or substrings. By maintaining a dynamic or fixed-size window and updating the state incrementally as the window shifts, it reduces nested loops ($O(N^2)$) to a single linear pass ($O(N)$)."

## 10. 2-minute interview answer
"Whenever a problem asks for the longest, shortest, or optimal contiguous subarray or substring, Sliding Window is my first thought. Instead of re-evaluating overlapping subarrays from scratch, we maintain a state—like a running sum or a frequency map—within a window defined by two pointers. We expand the right edge to explore new elements, and if a constraint is violated, we shrink the left edge until the window is valid again. This guarantees that both pointers only move forward, turning an $O(N^2)$ brute-force approach into an $O(N)$ time complexity solution. It perfectly balances exploring the search space while caching the overlapping computations."

## 11. Follow-ups
- "What if the array contains negative numbers and we need a dynamic window for a target sum?" (Sliding window breaks here because expanding doesn't guarantee the sum increases. We need Prefix Sums + Hash Map instead).

## 12. Deeper questions
- "How would you implement a sliding window minimum/maximum over an array?" (Requires an auxiliary Monotonic Deque to maintain the optimal elements in the window in $O(N)$).

## 13. Related concepts
- **Two Pointers**: Sliding window is a specific subtype of Two Pointers.
- **Prefix Sums**: Often used as an alternative when sliding window doesn't work (e.g., negative numbers).

## 14. When it breaks / Edge cases
- Fails when the target condition doesn't have a monotonic property (e.g., if adding an element might make a previously invalid window valid, you don't know when to shrink).

## 15. Comparison with alternative approaches
- **vs Dynamic Programming:** DP solves subsets/subsequences (non-contiguous). Sliding Window solves contiguous segments.

---
*Where this shows up in ML:* 
In NLP, n-grams extraction relies on a sliding window over tokens. In Time Series forecasting, we create training datasets by passing a sliding window over historical data (e.g., taking the past 7 days to predict the 8th day).
"""

for path, content in files_to_update.items():
    write_file(path, content)

print("Updated heavily requested templates.")
