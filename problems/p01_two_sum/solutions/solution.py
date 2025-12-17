"""
Reference solution for Two-Sum problem.
Time Complexity: O(n)
Space Complexity: O(n)
"""

def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find indices of two numbers that add up to target.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        List containing two indices [i, j] where nums[i] + nums[j] == target
        
    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
    """
    # Hash map to store {value: index}
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        # Check if complement exists in hash map
        if complement in seen:
            return [seen[complement], i]
        
        # Store current number and its index
        seen[num] = i
    
    # Problem guarantees exactly one solution exists
    # This line should never be reached
    return []


if __name__ == "__main__":
    # Test cases
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
    assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]
    
    print("✅ All tests passed!")
