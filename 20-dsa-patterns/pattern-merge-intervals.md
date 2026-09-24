# Pattern: Merge Intervals

## 1. Definition
The Merge Intervals pattern is used to solve problems involving overlapping scheduling, time ranges, or coordinates by sorting them and sequentially merging overlapping bounds.

## 2. Intuition
Imagine a hotel reservation book. Someone books a room from Monday to Wednesday. Another books Tuesday to Thursday. To find out when the room is occupied, you sort the bookings by start day. You see Monday overlaps with Tuesday, so you combine them into a single "occupied" block from Monday to Thursday.

## 3. Why it exists
Brute forcing interval overlaps requires comparing every interval to every other interval ($O(N^2)$). By sorting them first, any overlapping intervals are guaranteed to be strictly adjacent to each other, allowing us to process them in a single linear pass.

## 4. Mechanics
1. **Sort:** Sort the list of intervals strictly by their **start time**.
2. **Initialize:** Push the first interval into a `merged` results list.
3. **Iterate:** For each subsequent interval, compare its `start` time to the `end` time of the last interval in the `merged` list.
4. **Merge:** If `start <= end`, they overlap. Update the `end` of the merged interval to be the `max(current_end, new_end)`.
5. **Add:** If they don't overlap, append the new interval to the `merged` list.

## 5. Complexity (Time & Space)
- **Time Complexity:** $O(N \log N)$ heavily dominated by the initial sorting step. The merge pass is $O(N)$.
- **Space Complexity:** $O(N)$ to hold the sorted output array (or $O(\log N)$ for the sorting algorithm overhead).

## 6. Tiny worked example
Intervals: `[[1,3], [8,10], [2,6], [15,18]]`
- Sort: `[[1,3], [2,6], [8,10], [15,18]]`
- `merged = [[1,3]]`
- Check `[2,6]`. 2 <= 3. Overlap! Update end to `max(3, 6) = 6`. `merged = [[1,6]]`.
- Check `[8,10]`. 8 > 6. No overlap. `merged = [[1,6], [8,10]]`.

## 7. Code (Python, with type hints)
```python
from typing import List

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        
        # Check for overlap
        if current[0] <= last_merged[1]:
            last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
            
    return merged
```

## 8. Common mistakes
- Forgetting to sort the array first.
- Merging the end times incorrectly by just taking the second interval's end time. E.g., merging `[1, 10]` and `[2, 5]` should yield `[1, 10]`, requiring `max(10, 5)`.
- Confusing "Merge Intervals" (sort by start time) with "Activity Selection / Greedy Interval Scheduling" (sort by end time).

## 9. 30-second interview answer
"The Merge Intervals pattern efficiently combines overlapping ranges. It requires sorting the intervals by their start times first, which takes $O(N \log N)$. Then, in a single $O(N)$ pass, we merge adjacent intervals if the current start time is less than or equal to the previous end time."

## 10. 2-minute interview answer
"Whenever a problem deals with timeframes, meetings, or continuous ranges, the Merge Intervals pattern is the standard approach. The core insight is that by sorting the intervals by their starting boundary, any intervals that overlap are forced to be adjacent in the sorted array. This allows us to reduce an $O(N^2)$ cross-check into an $O(N \log N)$ sort followed by a simple $O(N)$ linear scan. During the scan, we maintain a running list of merged blocks. If the next interval's start time falls within the previous block's end time, we merge them by extending the end time to the maximum of both boundaries. If not, we seal the block and start a new one."

## 11. Follow-ups
- "What if the intervals are a stream of data and you can't sort them upfront?" (You use a self-balancing BST (like a TreeMap in Java) to maintain sorted order on insertions, making each insert/merge $O(\log N)$).

## 12. Deeper questions
- "How do you find the intersection of two lists of disjoint intervals?" (Use Two Pointers, one on each list. The overlap is `[max(start1, start2), min(end1, end2)]`).

## 13. Related concepts
- **Sweep Line Algorithm**: A more advanced 1D variant for intervals, counting overlapping layers (+1 for start, -1 for end).

## 14. When it breaks / Edge cases
- Intervals that touch at the exact boundary (e.g., `[1,2]` and `[2,3]`). You must clarify with the interviewer if touching counts as overlapping (`<=` vs `<`).

## 15. Comparison with alternative approaches
- N/A

---
*Where this shows up in ML:* 
Time-series data processing often requires merging irregularly sampled sensor data windows.
