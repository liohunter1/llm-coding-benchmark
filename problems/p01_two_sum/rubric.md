# Evaluation Rubric: P01 - Two-Sum

## Total Points: 100

---

## 1. Correctness (60 points)

### Test Case Scoring

| Test Case | Points | Description |
|-----------|--------|-------------|
| Basic case | 5 | `[2, 7, 11, 15], target=9` |
| Middle indices | 5 | `[3, 2, 4], target=6` |
| Duplicates | 10 | `[3, 3], target=6` |
| Negative numbers | 10 | `[-1, -2, -3, -4, -5], target=-8` |
| Zero target | 10 | `[-5, 0, 5, 10], target=0` |
| Large numbers | 10 | `[1000000000, -1000000000, ...]` |
| Minimum size | 5 | `[1, 2], target=3` |
| Last elements | 5 | Solution at end of array |

**Scoring**: 
- **Pass all cases**: 60 points
- **Fail 1-2 cases**: 40 points  
- **Fail 3-4 cases**: 20 points  
- **Fail 5+ cases**: 0 points

---

## 2. Time Complexity (30 points)

### Expected Complexity: O(n)

| Implementation | Points | Description |
|----------------|--------|-------------|
| Hash map (single pass) | 30 | Optimal solution |
| Hash map (two pass) | 25 | Correct complexity, suboptimal |
| Sorting + two pointers | 15 | O(n log n) - acceptable but not optimal |
| Brute force (nested loops) | 0 | O(n²) - fails requirement |

**Verification Method**:
- Instrumentation: Count hash map lookups
- Timing: Test with arrays of size 1000, 2000, 4000
- Code analysis: Check for nested loops

**Deductions**:
- -5 points: Unnecessary redundant operations
- -10 points: Multiple passes when single pass possible

---

## 3. Space Complexity (0 points, but noted)

- **O(n)**: Expected (hash map)
- **O(1)**: Not achievable for this approach
- **O(n²)** or worse: Red flag (likely buggy code)

---

## 4. Code Quality (10 points)

### Clarity (5 points)
- ✅ **5 points**: Descriptive variable names (`seen`, `complement`)
- ⚠️ **3 points**: Acceptable names (`map`, `diff`)
- ❌ **0 points**: Cryptic names (`m`, `x`, `a`)

### Error Handling (3 points)
- ✅ **3 points**: Handles edge cases gracefully
- ⚠️ **1 point**: Assumes valid input
- ❌ **0 points**: Crashes on edge cases

### Best Practices (2 points)
- ✅ **2 points**: Idiomatic code for language
- ⚠️ **1 point**: Works but non-idiomatic
- ❌ **0 points**: Anti-patterns present

---

## Common LLM Failures

### ❌ Failure Pattern 1: Brute Force

**Code**:
```python
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

**Score**: 60/100 (Correct but O(n²))

---

### ❌ Failure Pattern 2: Returns Values Instead of Indices

**Code**:
```python
def two_sum(nums, target):
    seen = set()
    for num in nums:
        if target - num in seen:
            return [num, target - num]  # ❌ Wrong!
        seen.add(num)
```

**Score**: 0/100 (Incorrect output format)

---

### ❌ Failure Pattern 3: Doesn't Handle Duplicates

**Code**:
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        seen[num] = i  # ❌ Overwrites duplicate!
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen and seen[complement] != i:
            return [i, seen[complement]]
```

**Score**: 40/100 (Fails duplicate test case)

---

## ✅ Reference Solution

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

**Score**: 100/100
- ✅ Correctness: All test cases pass
- ✅ Time Complexity: O(n)
- ✅ Space Complexity: O(n)
- ✅ Code Quality: Clear, idiomatic

---

## Grading Script Output Example

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Two-Sum Evaluation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Correctness:                      60/60 ✅
  ✅ basic_case                    (5/5)
  ✅ middle_indices                (5/5)
  ✅ duplicates                    (10/10)
  ✅ negative_numbers              (10/10)
  ✅ zero_target                   (10/10)
  ✅ large_numbers                 (10/10)
  ✅ minimum_size                  (5/5)
  ✅ last_elements                 (5/5)

Time Complexity:                  30/30 ✅
  Algorithm: Hash map (single pass)
  Measured: O(n)

Code Quality:                     10/10 ✅
  Clarity:        5/5
  Error Handling: 3/3
  Best Practices: 2/2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL SCORE: 100/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
