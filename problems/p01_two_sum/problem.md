# Problem P01: Two-Sum (Optimized)

## Problem Statement

Given an array of integers `nums` and an integer `target`, return **indices** of the two numbers such that they add up to `target`.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice.

You can return the answer in any order.

**Optimize for O(n) time complexity.**

---

## Examples

### Example 1:
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

### Example 2:
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

### Example 3:
```
Input: nums = [3,3], target = 6
Output: [0,1]
```

---

## Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- **Only one valid answer exists.**

---

## Hints

1. A brute force approach with nested loops is O(n²). Can you do better?
2. Think about using a hash map to store values you've seen.
3. For each number, check if `target - number` exists in your hash map.

---

## Function Signature

### Python
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    pass
```

### JavaScript
```javascript
function twoSum(nums, target) {
    // Your code here
}
```

### Java
```java
public class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Your code here
    }
}
```

### C++
```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // Your code here
    }
};
```

---

## Evaluation Criteria

Your solution will be evaluated on:

1. **Correctness** (60 points)
   - All test cases pass
   - Handles edge cases (duplicates, negatives, zero)

2. **Time Complexity** (30 points)
   - Achieves O(n) time complexity
   - Uses hash map approach

3. **Code Quality** (10 points)
   - Clear variable names
   - Proper error handling (if applicable)
   - Idiomatic code for the language
