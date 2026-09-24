# LIS, LCS, and Edit Distance

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
- **Edit (2D Matrix):** Compare `str1[i]` and `str2[j]`. If match: cost is `dp[i-1][j-1]`. If mismatch, take $1 + \min$ of (Insert `dp[i][j-1]`, Delete `dp[i-1][j]`, Replace `dp[i-1][j-1]`).

## 5. Complexity (Time & Space)
- **LIS:** DP is $O(N^2)$ time, $O(N)$ space. (Can be optimized to $O(N \log N)$ with Binary Search + Patience Sorting).
- **LCS & Edit:** $O(N \times M)$ time and space for two strings of length N and M. Space can be optimized to $O(\min(N, M))$ using two rows.

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
"LIS, LCS, and Edit Distance are the foundational sequence DP patterns. LIS uses a 1D state tracking the longest sequence ending at index `i`. LCS and Edit Distance compare two strings using a 2D state, evaluating whether characters match or mismatch, and transitioning based on insertions, deletions, or replacements in $O(N \times M)$ time."

## 10. 2-minute interview answer
"Sequence alignment and comparison problems are solved using 2D DP. For Longest Common Subsequence and Edit Distance, we define a 2D state `dp[i][j]` representing the subproblem of comparing string A up to index `i` with string B up to index `j`. If the current characters match, the state transitions from `dp[i-1][j-1]`. If they mismatch, LCS takes the max of skipping a character in A or B, while Edit Distance takes the min of an insertion, deletion, or substitution, plus a cost of 1. Because `dp[i][j]` only relies on the current row and the row immediately above it (`i-1`), we can always optimize the $O(N \times M)$ memory footprint down to $O(M)$ by storing just two rows. For LIS, the standard DP is $O(N^2)$, but interviewers often expect the optimal $O(N \log N)$ solution utilizing a binary-searched 'patience sorting' array."

## 11. Follow-ups
- "Can you do LIS in $O(N \log N)$?" (Yes, maintain an array `tails`. Iterate `nums`. If `x` is larger than all tails, append it. Else, binary search `tails` to find the smallest element $\ge x$ and replace it).

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
