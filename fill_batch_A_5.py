import os

def write_and_commit(path, content):
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}"')
    os.system(f'git commit -m "Fill real content for {os.path.basename(path)} (Batch A)"')

files = {}

files["19-dp-deep-dive/knapsack-family.md"] = """# Knapsack DP Family

## 1. Definition
The Knapsack problem is a classic 2D Dynamic Programming pattern where you must choose a subset of items, each with a weight and a value, to maximize total value without exceeding a capacity constraint.

## 2. Intuition
Imagine you are a thief with a backpack that holds exactly 50 lbs. You break into a vault with various items (gold bars, jewels, TVs). A TV is valuable but heavy. A jewel is light and moderately valuable. You can't just take the most valuable items (they might be too heavy), nor just the lightest (they might be worthless). You must evaluate the tradeoff for every single item: "Do I take this, or leave it?"

## 3. Why it exists
A greedy approach (sorting by value-to-weight ratio) fails for the "0/1 Knapsack" (where items cannot be broken into fractions) because you might leave empty space in the bag that could have been filled perfectly by a suboptimal item. DP exists to exhaustively but efficiently explore the "take it or leave it" branches.

## 4. Mechanics
- **State:** `dp(i, c)` = the maximum value using a subset of items from index `0` to `i`, with remaining capacity `c`.
- **Transition (0/1 Knapsack):** For item `i`, you can either:
  1. Leave it: `dp(i-1, c)`
  2. Take it (if it fits): `val[i] + dp(i-1, c - weight[i])`
  `dp(i, c)` is the maximum of those two choices.
- **Variations:** 
  - *Unbounded Knapsack:* You can take item `i` infinitely many times. Transition uses `dp(i, c - weight[i])` instead of `i-1`.
  - *Subset Sum:* Can you achieve exactly capacity `c`? (Boolean return).

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \\times C)$ where $N$ is the number of items and $C$ is the capacity constraint. (Note: This is pseudo-polynomial, meaning it's proportional to the *value* of $C$, not the *length* of the input).
- **Space Complexity:** $O(N \\times C)$ for a 2D table. Can be space-optimized to $O(C)$ by only keeping the previous row.

## 6. Tiny worked example
Items (Wt, Val): A(1, 10), B(2, 15), C(3, 40). Capacity: 3.
- Cap 3, look at C: Take C (Val=40, Cap=0). Leave C (Look at A,B with Cap 3).
- Max is taking C (40).
- Wait, what about taking A and B? (W=3, Val=25). 40 > 25.
- DP table elegantly calculates this by building up from Capacity 0 to 3.

## 7. Code (Python, with type hints)
```python
from typing import List

def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    n = len(weights)
    # Space optimized to 1D array of size Capacity + 1
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Traverse backwards for 0/1 knapsack to avoid reusing the same item
        for c in range(capacity, weights[i] - 1, -1):
            dp[c] = max(dp[c], values[i] + dp[c - weights[i]])
            
    return dp[capacity]
```

## 8. Common mistakes
- **Traversal Direction in 1D Optimization:** In 0/1 Knapsack, if you optimize space to a 1D array, you *must* iterate the inner capacity loop backwards. If you iterate forwards, you might use the same item multiple times (which accidentally solves the Unbounded Knapsack problem!).
- Trying to use a Greedy algorithm (Value/Weight ratio) for 0/1 Knapsack. (Greedy only works for *Fractional* Knapsack).

## 9. 30-second interview answer
"The Knapsack pattern solves constrained optimization problems by deciding whether to 'take' or 'leave' an item. The state is defined by the current item index and the remaining capacity. It runs in $O(N \\times C)$ time. The 2D memory footprint can be optimized to $O(C)$ by storing only the previous row, iterating backwards to prevent item reuse."

## 10. 2-minute interview answer
"The 0/1 Knapsack problem is the archetype for 2D Dynamic Programming where decisions are constrained by a resource limit. Because a greedy value-to-weight ratio fails for indivisible items, we must evaluate the 'take it or leave it' branches. We define a 2D state `dp[i][c]`, representing the max value up to item `i` with capacity `c`. The transition equation takes the max of leaving the item `dp[i-1][c]` or taking it `value[i] + dp[i-1][c-weight[i]]`. While this takes $O(N \\times C)$ time and space, we can space-optimize it to $O(C)$ by noticing that row `i` only depends on row `i-1`. The trick in the 1D optimized version is that the capacity loop must run backwards; running it forwards would allow an item to recursively build on itself, transforming the algorithm into the Unbounded Knapsack solution."

## 11. Follow-ups
- "How do you solve Unbounded Knapsack (Coin Change)?" (Same 1D array optimization, but run the capacity loop forwards).
- "How do you solve Subset Sum (e.g., Partition Equal Subset Sum)?" (It's a knapsack where you don't maximize value, you just track boolean `True/False` if a capacity can be reached).

## 12. Deeper questions
- "Is $O(N \\times C)$ polynomial time?" (No, it's pseudo-polynomial. If $C$ is $10^9$, the algorithm takes billions of operations, even if $N$ is just 5. The input size of $C$ in binary is only ~30 bits, so time is exponential relative to the input *size*).

## 13. Related concepts
- **Subset Sum**: Exact same logic, boolean states.
- **Target Sum**: Adds subtraction to the choices.

## 14. When it breaks / Edge cases
- Breaks if $C$ is massive (e.g., $10^9$). You will get a Time Limit Exceeded (TLE) and Memory Error.

## 15. Comparison with alternative approaches
- **vs Fractional Knapsack:** If you can cut items in half (like gold dust), you just sort by Value/Weight ratio and take as much as you can. Greedy works. $O(N \\log N)$.

---
*Where this shows up in ML:* 
Resource allocation in AI infrastructure (e.g., bin-packing models onto limited GPU VRAM) is fundamentally a variation of the Knapsack problem.
"""

files["19-dp-deep-dive/lis-lcs-edit-distance.md"] = """# LIS, LCS, and Edit Distance

## 1. Definition
This covers the "Big Three" sequence-based DP problems:
1. **LIS (Longest Increasing Subsequence):** Find the longest subsequence in an array that is strictly increasing.
2. **LCS (Longest Common Subsequence):** Find the longest subsequence shared between two strings.
3. **Edit Distance (Levenshtein):** The minimum number of operations (insert, delete, replace) to transform string A into string B.

## 2. Intuition
- **LIS:** You have a timeline of stock prices. You want to pick days where the price goes up, skipping days it drops, to form the longest upward trend.
- **LCS:** You have two people's DNA. You want to find the longest sequence of genes they share in the same relative order, ignoring mutations in between.
- **Edit:** Autocorrect. You typed "speling". How many keystrokes to fix it to "spelling"? (Insert 1 'l').

## 3. Why it exists
String and sequence comparison is foundational to computer science (diff tools, spell checkers, bioinformatics). Pure recursion yields massive $O(2^N)$ or $O(3^N)$ trees because of the sheer number of subsequences. DP is required to make sequence alignment tractable.

## 4. Mechanics
- **LIS (1D Array):** `dp[i]` = max LIS ending exactly at `i`. For `j` from 0 to `i-1`: if `nums[j] < nums[i]`, `dp[i] = max(dp[i], dp[j] + 1)`.
- **LCS (2D Matrix):** Compare `str1[i]` and `str2[j]`. If match: `1 + dp[i-1][j-1]`. If mismatch: `max(dp[i-1][j], dp[i][j-1])`.
- **Edit (2D Matrix):** Compare `str1[i]` and `str2[j]`. If match: cost is `dp[i-1][j-1]`. If mismatch, take $1 + \\min$ of (Insert `dp[i][j-1]`, Delete `dp[i-1][j]`, Replace `dp[i-1][j-1]`).

## 5. Complexity (Time & Space)
- **LIS:** DP is $O(N^2)$ time, $O(N)$ space. (Can be optimized to $O(N \\log N)$ with Binary Search + Patience Sorting).
- **LCS & Edit:** $O(N \\times M)$ time and space for two strings of length N and M. Space can be optimized to $O(\\min(N, M))$ using two rows.

## 6. Tiny worked example
LCS of "ABC" and "AC":
- 'A' == 'A'. Match! Score is 1 + LCS("BC", "C").
- 'B' != 'C'. Mismatch. Max of LCS("C", "C") and LCS("BC", "").
- LCS("C", "C") matches. Score is 1. Total = 2.

## 7. Code (Python, with type hints)
```python
# Edit Distance
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # Optimization: Only need two rows
    prev = [j for j in range(n + 1)]
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]
            else:
                curr[j] = 1 + min(curr[j-1],    # Insert
                                  prev[j],      # Delete
                                  prev[j-1])    # Replace
        prev = curr.copy()
        
    return prev[n]
```

## 8. Common mistakes
- **Initialization in 2D DP:** Forgetting to initialize the first row and column in LCS or Edit Distance (e.g., comparing a string to an empty string requires 1 deletion per character).
- Confusing Substring (must be contiguous) with Subsequence (can skip characters).

## 9. 30-second interview answer
"LIS, LCS, and Edit Distance are the foundational sequence DP patterns. LIS uses a 1D state tracking the longest sequence ending at index `i`. LCS and Edit Distance compare two strings using a 2D state, evaluating whether characters match or mismatch, and transitioning based on insertions, deletions, or replacements in $O(N \\times M)$ time."

## 10. 2-minute interview answer
"Sequence alignment and comparison problems are solved using 2D DP. For Longest Common Subsequence and Edit Distance, we define a 2D state `dp[i][j]` representing the subproblem of comparing string A up to index `i` with string B up to index `j`. If the current characters match, the state transitions from `dp[i-1][j-1]`. If they mismatch, LCS takes the max of skipping a character in A or B, while Edit Distance takes the min of an insertion, deletion, or substitution, plus a cost of 1. Because `dp[i][j]` only relies on the current row and the row immediately above it (`i-1`), we can always optimize the $O(N \\times M)$ memory footprint down to $O(M)$ by storing just two rows. For LIS, the standard DP is $O(N^2)$, but interviewers often expect the optimal $O(N \\log N)$ solution utilizing a binary-searched 'patience sorting' array."

## 11. Follow-ups
- "Can you do LIS in $O(N \\log N)$?" (Yes, maintain an array `tails`. Iterate `nums`. If `x` is larger than all tails, append it. Else, binary search `tails` to find the smallest element $\\ge x$ and replace it).

## 12. Deeper questions
- "How is Git Diff implemented?" (Under the hood, `diff` algorithms use variations of Longest Common Subsequence to find what lines were added or removed).

## 13. Related concepts
- **Palindromic Subsequences**: Longest Palindromic Subsequence is just the LCS of a string and its reverse.

## 14. When it breaks / Edge cases
- If strings are massive (e.g., 100,000 characters), an $O(N^2)$ LCS DP will TLE.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Edit Distance (Levenshtein distance) is the standard metric for evaluating speech recognition (Word Error Rate - WER) and OCR systems. BLEU and ROUGE scores in NLP also share conceptual roots with N-gram sequence matching (similar to substring/subsequence logic).
"""

files["18-algorithms/backtracking.md"] = """# Backtracking

## 1. Definition
Backtracking is an algorithmic paradigm that systematically searches for a solution to a problem among all available options. It does so by building candidates incrementally and abandoning ("backtracking" from) a candidate as soon as it determines the candidate cannot yield a valid solution.

## 2. Intuition
Imagine navigating a physical maze. You walk down a path, leaving a trail of breadcrumbs. You hit a dead end. You turn around, walk back along your breadcrumbs to the last intersection, pick up those crumbs, and try a different path. You "undo" your mistake and try again.

## 3. Why it exists
For problems requiring us to find *all* permutations, combinations, or a specific valid configuration (like Sudoku), there is no mathematical shortcut or greedy logic. We must exhaustively search. Backtracking organizes this exhaustive search, pruning invalid paths early (bounding) to save massive amounts of time compared to pure brute-force generation.

## 4. Mechanics
1. **Choose:** Pick an option and add it to the current state/path.
2. **Explore:** Recursively call the backtracking function with the new state.
3. **Un-choose (Backtrack):** Remove the option from the current state/path, returning it to how it was before step 1, so the next loop iteration can try a different option cleanly.
4. **Base Case:** If the state is a valid final solution, save a *copy* of it. If it violates constraints, return immediately (prune).

## 5. Complexity (Time & Space)
- **Time Complexity:** Usually exponential or factorial. $O(2^N)$ for subsets, $O(N!)$ for permutations.
- **Space Complexity:** $O(N)$ for the recursion stack and the path array.

## 6. Tiny worked example
Permutations of `[1, 2]`.
- Start: `[]`
- Loop: Pick `1`. Path: `[1]`.
  - Explore: Pick `2`. Path `[1, 2]`. Base case hit! Save `[1, 2]`.
  - Un-choose: Remove `2`. Path `[1]`.
- Un-choose: Remove `1`. Path: `[]`.
- Loop: Pick `2`. Path: `[2]`.
  - Explore: Pick `1`. Path `[2, 1]`. Base case hit! Save `[2, 1]`.
- Output: `[[1, 2], [2, 1]]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def permute(nums: List[int]) -> List[List[int]]:
    result = []
    
    def backtrack(path: List[int], used: List[bool]):
        if len(path) == len(nums):
            result.append(path.copy()) # MUST APPEND A COPY!
            return
            
        for i in range(len(nums)):
            if used[i]: continue
            
            # 1. Choose
            used[i] = True
            path.append(nums[i])
            
            # 2. Explore
            backtrack(path, used)
            
            # 3. Un-choose
            path.pop()
            used[i] = False
            
    backtrack([], [False] * len(nums))
    return result
```

## 8. Common mistakes
- **Not appending a copy:** `result.append(path)` in Python appends a *reference* to the list. When the list is later popped/modified during backtracking, the saved result changes too, leaving you with a list of empty arrays. Always use `path.copy()` or `path[:]`.
- Forgetting the "un-choose" step, leading to states bleeding into each other.

## 9. 30-second interview answer
"Backtracking is an optimized exhaustive search method used for permutations, combinations, and constraint satisfaction problems. It builds a state incrementally, recursively explores, and most importantly, 'undoes' the choice (backtracks) to allow the exploration of alternative paths. We prune invalid paths early to beat pure brute-force generation."

## 10. 2-minute interview answer
"Backtracking is essentially Depth-First Search applied to an abstract state-space tree. We use it when a problem asks for 'all possible ways' to arrange or combine elements, dictating an inherently exponential $O(2^N)$ or $O(N!)$ time complexity. The core template involves three steps inside a loop: choose an option, recursively explore that choice, and then 'un-choose' it by popping it off the state tracking array. This un-choosing ensures the state is perfectly clean for the next iteration of the loop. The critical bug candidates write is forgetting to deep-copy the path array when adding it to the final results list. To optimize, we focus heavily on bounding/pruning—if a partial state already violates a constraint, we return immediately, severing that entire branch of the recursion tree and saving massive computation."

## 11. Follow-ups
- "How do you handle duplicates in Permutations or Subsets?" (Sort the input array first. Inside the loop, if `i > start` and `nums[i] == nums[i-1]`, `continue` to skip the duplicate branch).

## 12. Deeper questions
- "What's the difference between Backtracking and Branch & Bound?" (Backtracking explores all valid solutions. Branch and Bound is used for optimization problems—if the current branch's 'best possible' score is worse than the current global best, it prunes the branch).

## 13. Related concepts
- **Depth-First Search (DFS)**: Backtracking is DFS.
- **Dynamic Programming**: If backtracking subproblems overlap, adding a memoization cache turns it into Top-Down DP.

## 14. When it breaks / Edge cases
- Breaks entirely on large $N$ (e.g., $N=50$). $O(2^{50})$ will never finish executing.

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
In traditional AI, constraint satisfaction problems (like Sudoku or scheduling algorithms) are solved using backtracking. In modern ML, Beam Search is somewhat related—it explores branches of generated text, but instead of exhaustive backtracking, it greedily prunes the tree to a fixed width (beam size) to maintain tractability.
"""

files["18-algorithms/greedy-algorithms.md"] = """# Greedy Algorithms

## 1. Definition
A Greedy Algorithm is an algorithmic paradigm that builds up a solution piece by piece, always choosing the next piece that offers the most immediate (local) benefit, with the hope that these local optimums lead to a global optimum.

## 2. Intuition
Imagine you are at a buffet and want to maximize the calories on your plate. A greedy approach would be to look at all the food, grab the highest-calorie item you see (pizza), then the next highest (cake), until your plate is full. You don't calculate combinations; you just take the best thing available right now.

## 3. Why it exists
Dynamic programming is powerful but requires $O(N^2)$ or $O(N \\times C)$ time and space. Greedy algorithms, when mathematically applicable, solve optimization problems in $O(N)$ or $O(N \\log N)$ time (usually just requiring a sort), making them incredibly fast and memory-efficient.

## 4. Mechanics
1. **Sort/Prioritize:** Often, the input must be sorted by some metric (e.g., end time, value/weight ratio).
2. **Iterate:** Go through the sorted data.
3. **Select:** If the current item satisfies the constraints, take it. Do not look back or reconsider.
4. **Update state:** Adjust remaining capacity or current end time.

## 5. Complexity (Time & Space)
- **Time Complexity:** Usually $O(N \\log N)$ because sorting is required. If already sorted, $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary space (ignoring the sorting overhead).

## 6. Tiny worked example
Activity Selection / Meeting Rooms:
Meetings: `[(1,3), (2,5), (4,6)]`. Goal: Maximize non-overlapping meetings.
- Sort by end time: `(1,3), (2,5), (4,6)`.
- Take `(1,3)`. Current end time = 3.
- Next is `(2,5)`. Starts at 2. $2 < 3$. Conflict! Skip.
- Next is `(4,6)`. Starts at 4. $4 \\ge 3$. Take it.
Result: 2 meetings.

## 7. Code (Python, with type hints)
```python
from typing import List

# Classic Interval Scheduling / Activity Selection
def max_non_overlapping(intervals: List[List[int]]) -> int:
    if not intervals: return 0
    
    # Sort strictly by END time
    intervals.sort(key=lambda x: x[1])
    
    count = 1
    current_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        start, end = intervals[i]
        if start >= current_end:
            # No overlap, greedily take it
            count += 1
            current_end = end
            
    return count
```

## 8. Common mistakes
- **Using Greedy when DP is required:** E.g., the 0/1 Knapsack problem or Coin Change with non-standard denominations (like coins of 1, 3, 4 to make 6. Greedy takes 4+1+1=3 coins. DP takes 3+3=2 coins).
- Sorting by the wrong metric. In Interval Scheduling, sorting by start time fails; you must sort by end time to free up the resource as early as possible.

## 9. 30-second interview answer
"Greedy algorithms make locally optimal choices at each step, hoping to find a global optimum. They are extremely fast—usually $O(N \\log N)$ due to sorting—and $O(1)$ space. However, they only work if the problem satisfies the Greedy Choice Property, meaning a local best choice never compromises the overall solution. Otherwise, you must use Dynamic Programming."

## 10. 2-minute interview answer
"Greedy algorithms are highly efficient, single-pass decision-makers. They avoid the exhaustive branching of Backtracking and the memory overhead of Dynamic Programming. We typically apply them by sorting the input by a specific heuristic—like finishing time in interval problems or edge weight in spanning trees—and then iterating through, picking the best valid option without ever looking back. The catch is that they are mathematically brittle. To use a Greedy algorithm, you must be confident the problem exhibits the 'Greedy Choice Property'. For example, Dijkstra's algorithm and Kruskal's MST are greedy and perfectly optimal. But for problems like the 0/1 Knapsack, taking the immediately most valuable item might block you from taking two smaller items that total a higher value, forcing you to use DP instead."

## 11. Follow-ups
- "How do you prove a greedy algorithm is correct?" (Usually by a 'proof by contradiction' or 'exchange argument', showing that swapping the greedy choice for any other choice yields a worse or equal result).

## 12. Deeper questions
- "What is a Matroid?" (An abstract mathematical structure that, if a problem maps to it, guarantees a Greedy algorithm will yield the optimal solution).

## 13. Related concepts
- **Dynamic Programming**: The fallback when Greedy fails.
- **Minimum Spanning Trees**: Kruskal's and Prim's are famous greedy algorithms.
- **Dijkstra's Algorithm**: A greedy algorithm for shortest paths.

## 14. When it breaks / Edge cases
- Breaks when future choices are heavily constrained by current choices in non-uniform ways (e.g., negative weights in Dijkstra's).

## 15. Comparison with alternative approaches
- **vs DP:** DP is safe but slow/memory-intensive. Greedy is fast but risky (must mathematically prove it works).

---
*Where this shows up in ML:* 
Decision Trees (CART algorithm) are fundamentally Greedy algorithms. At each node, the tree greedily picks the feature and threshold that minimizes Gini Impurity or Entropy *right now*, without looking ahead to see if a worse split now might lead to better splits deeper in the tree.
"""

for path, content in files.items():
    write_and_commit(path, content)

print("Batch A - Part 5 Complete")
