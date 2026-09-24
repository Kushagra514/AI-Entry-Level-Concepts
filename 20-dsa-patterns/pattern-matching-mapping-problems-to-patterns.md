# Pattern Matching: Mapping Problems to Patterns

## 1. Definition
This is a meta-skill for coding interviews: reading a plain-English prompt, identifying algorithmic "keywords" or constraints, and instantly mapping them to the correct DSA pattern.

## 2. Intuition
You are a doctor diagnosing a patient. You don't try every medicine randomly. You listen to symptoms: "Cough, fever, loss of taste." Diagnosis: COVID-19. Treatment: Antivirals. In interviews, symptoms are constraints: "Sorted array, $O(\log N)$." Diagnosis: Binary Search. Treatment: Left/Right pointers.

## 3. Why it exists
Interviewers intentionally disguise classic algorithms behind wordy stories. Without pattern matching, candidates waste 20 minutes trying to invent a novel algorithm. With it, candidates derive the optimal algorithm in 60 seconds.

## 4. Mechanics (Symptom -> Pattern)
- **"Sorted Array" + "Target Sum"**: Two Pointers.
- **"Sorted Array" + "$O(\log N)$"**: Binary Search.
- **"Subarray / Substring" + "Max/Min Length"**: Sliding Window.
- **"Top K / Kth Largest"**: Heap / Priority Queue.
- **"Next Greater Element"**: Monotonic Stack.
- **"Combinations / Permutations / Subsets"**: Backtracking.
- **"All possible ways / Maximize/Minimize (with overlap)"**: Dynamic Programming.
- **"Connected Components / Network"**: BFS/DFS or Union-Find.
- **"Task Scheduling / Prerequisites"**: Topological Sort.
- **"Range from 1 to N" + "Missing/Duplicate"**: Cyclic Sort.
- **"Overlapping Times / Meetings"**: Merge Intervals.

## 5. Complexity (Time & Space)
- N/A

## 6. Tiny worked example
Prompt: *Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be. You must write an algorithm with $O(\log N)$ runtime.*
- Symptoms: "Sorted Array", "Target value", "$O(\log N)$".
- Diagnosis: Binary Search.

## 7. Code (Python, with type hints)
*(N/A - This is a conceptual mapping skill)*

## 8. Common mistakes
- **Ignoring Constraints:** Missing $N \le 20$ (screams $O(2^N)$ Backtracking) or $N \le 10^5$ (screams $O(N)$ or $O(N \log N)$, making $O(N^2)$ DP impossible).
- **False Positives:** Seeing "maximize" and assuming DP, when the problem might have the Greedy Choice Property (e.g., Interval Scheduling).

## 9. 30-second interview answer
"I map problems to patterns by identifying structural keywords and analyzing time complexity constraints. For example, 'Top K' triggers Heaps, 'contiguous subarrays' triggers Sliding Window, and $O(\log N)$ on a sorted array strictly points to Binary Search."

## 10. 2-minute interview answer
"The most critical skill in an interview is translating the prompt's constraints into a known architectural pattern. My thought process evaluates three things: the data structure, the mathematical keywords, and the Big-O bounds. If I see a string and the word 'substring', I immediately set up a Sliding Window. If the problem asks for 'all possible combinations', I know it's an $O(2^N)$ Backtracking problem. If it asks to 'minimize the maximum' across an array, I use Binary Search on Answer. Constraints give it away: an input size of $N=10^6$ means I can only afford an $O(N)$ algorithm, immediately ruling out nested loops or 2D DP. By applying this heuristic mapping, I spend my time writing clean code instead of struggling with algorithm design."

## 11. Follow-ups
- "What if multiple patterns seem to apply?" (Choose the one that satisfies the optimal time complexity. E.g., 'Target Sum' can be done via Hash Map $O(N)$ time/$O(N)$ space, or Two Pointers if sorted $O(N)$ time/$O(1)$ space. Mention both, implement the best).

## 12. Deeper questions
- "How do you identify a Monotonic Queue (Deque) problem?" (It is the exact intersection of 'Sliding Window' and 'Max/Min Element'—e.g., Sliding Window Maximum).

## 13. Related concepts
- **All DSA Patterns**

## 14. When it breaks / Edge cases
- FAANG 'Hard' problems often require *combining* two patterns (e.g., Binary Search over a Sliding Window validation function).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Translating a business problem ("we need to predict house prices") to an ML architecture (Regression vs Classification, tabular vs text).
