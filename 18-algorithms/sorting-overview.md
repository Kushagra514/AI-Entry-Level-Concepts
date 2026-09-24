# Sorting Algorithms Overview

## 1. Definition
Sorting algorithms rearrange a collection of items into a specific hierarchical order (e.g., numerical or lexicographical).

## 2. Intuition
If you have a hand of playing cards, you intuitively sort them so you can quickly see what you have and make decisions. Sorting algorithms are formal, step-by-step methods instructing computers how to achieve that ordered state.

## 3. Why it exists
Unsorted data requires $O(N)$ time to search. Sorted data unlocks Binary Search ($O(\log N)$), simplifies finding duplicates, and makes Two Pointer techniques viable. Sorting is the most fundamental preprocessing step in computer science.

## 4. Mechanics
Algorithms generally fall into two categories:
1. **Comparison-based:** Compare elements against each other (Bubble, Insertion, Merge, Quick, Heap). Mathematically bounded by a minimum worst-case time of $O(N \log N)$.
2. **Non-comparison-based:** Exploit properties of the data (like integers in a narrow range) to sort without direct comparisons (Counting, Radix, Bucket). Can achieve $O(N)$ time.

## 5. Complexity (Time & Space)
*(See specific algorithm files for deep dives. High-level summary:)*
- **O(N^2) Time:** Bubble, Selection, Insertion (Good for tiny or nearly-sorted data).
- **O(N log N) Time:** Merge (Stable, $O(N)$ space), Quick (Unstable, $O(\log N)$ space, worst $O(N^2)$), Heap (Unstable, $O(1)$ space).
- **O(N) Time:** Counting, Radix (Requires specific data types, $O(N)$ space).

## 6. Tiny worked example
*(Concepts: Stability and In-Place)*
- **Stability:** If you sort `[(Alice, 50), (Bob, 50)]` by score, a *stable* sort guarantees Alice remains before Bob. An *unstable* sort might flip them to `[(Bob, 50), (Alice, 50)]`.
- **In-Place:** Sorts by swapping elements within the original array (Quick, Heap). Out-of-place allocates a new array (Merge).

## 7. Code (Python, with type hints)
```python
# Python's built-in Timsort (a hybrid of Merge Sort and Insertion Sort)
# Time: O(N log N) worst case, O(N) best case (if already sorted).
# Space: O(N). It is a STABLE sort.
arr = [5, 2, 9, 1]
arr.sort() # In-place
new_arr = sorted(arr) # Out-of-place
```

## 8. Common mistakes
- Thinking $O(N \log N)$ is the absolute limit for all sorting (forgetting Radix/Counting sort).
- Not knowing the difference between Stable and Unstable sorts when an interviewer asks "sort by X, then sort by Y". (You must use a stable sort for the second pass).

## 9. 30-second interview answer
"Comparison-based sorting algorithms are mathematically bounded at $O(N \log N)$ time complexity. Merge Sort offers guaranteed $O(N \log N)$ time and stability but requires $O(N)$ space. Quick Sort is often faster in practice with $O(\log N)$ space but is unstable and has a worst-case $O(N^2)$. Python uses Timsort, a highly optimized stable hybrid."

## 10. 2-minute interview answer
"Understanding sorting is less about writing them from scratch and more about knowing their tradeoffs. For general purposes, an $O(N \log N)$ algorithm like Quick Sort or Merge Sort is standard. Merge Sort is stable, meaning it preserves the relative order of equal elements, which is crucial for multi-pass sorting, but it costs $O(N)$ memory. Quick Sort operates in-place, making it cache-friendly and faster in practice, though it is unstable and can degrade to $O(N^2)$ with a poor pivot. If we are sorting integers within a tightly constrained range, we can bypass the $O(N \log N)$ comparison bound entirely and use Counting Sort to achieve $O(N)$ time. In production, languages like Python and Java use hybrid algorithms like Timsort, combining the $O(N \log N)$ scaling of Merge Sort with the $O(N)$ best-case efficiency of Insertion Sort for nearly-sorted data."

## 11. Follow-ups
- "Why does Python use Timsort instead of Quicksort?" (Timsort is stable and heavily optimized for real-world data, which often contains partially sorted subsequences).

## 12. Deeper questions
- "Prove why comparison-based sorting cannot be faster than $O(N \log N)$." (A decision tree for sorting $N$ elements has $N!$ leaves. The minimum depth of a binary tree with $N!$ leaves is $\log(N!)$, which by Stirling's approximation is $O(N \log N)$).

## 13. Related concepts
- **Binary Search**: Only works on sorted data.
- **Two Pointers**: Often requires sorting the array first.

## 14. When it breaks / Edge cases
- Memory limits: Merge Sort breaks if you don't have enough RAM for the $O(N)$ overhead.

## 15. Comparison with alternative approaches
- If you only need the "Top K" elements, sorting the whole array in $O(N \log N)$ is suboptimal. Use a Heap ($O(N \log K)$) or Quickselect ($O(N)$).

---
*Where this shows up in ML:* 
Sorting is heavily used in ranking metrics (like NDCG or MAP in recommender systems) and in extracting the Top-K most probable tokens during LLM generation. It's also used to sort data points when calculating AUC-ROC.
