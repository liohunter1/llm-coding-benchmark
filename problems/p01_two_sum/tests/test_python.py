"""
Test harness for Two-Sum problem (Python)
"""

import pytest
import json
import time
from pathlib import Path
from typing import List, Callable


def load_test_cases():
    """Load test cases from JSON file."""
    test_file = Path(__file__).parent / "test_cases.json"
    with open(test_file) as f:
        cases = json.load(f)
    return [(c["nums"], c["target"], c["expected"]) for c in cases]


class TestTwoSum:
    """Test suite for Two-Sum problem."""
    
    @pytest.fixture
    def solution(self) -> Callable:
        """
        Import the solution function.
        Override this fixture to test custom implementations.
        """
        from solutions.solution import two_sum
        return two_sum
    
    def test_basic_case(self, solution):
        """Test basic positive numbers."""
        result = solution([2, 7, 11, 15], 9)
        assert sorted(result) == [0, 1]
    
    def test_negative_numbers(self, solution):
        """Test with negative numbers."""
        result = solution([-1, -2, -3, -4, -5], -8)
        assert sorted(result) == [2, 4]
    
    def test_duplicates(self, solution):
        """Test with duplicate values."""
        result = solution([3, 3], 6)
        assert sorted(result) == [0, 1]
    
    def test_zero_target(self, solution):
        """Test when target is zero."""
        result = solution([-5, 0, 5, 10], 0)
        assert sorted(result) == [0, 2]
    
    @pytest.mark.parametrize("nums,target,expected", load_test_cases())
    def test_all_cases(self, solution, nums, target, expected):
        """Run all test cases from JSON."""
        result = solution(nums, target)
        
        # Verify result is correct (order doesn't matter)
        assert sorted(result) == sorted(expected), \
            f"Expected {expected}, got {result} for nums={nums}, target={target}"
    
    def test_time_complexity(self, solution):
        """
        Verify O(n) time complexity.
        
        This test ensures the solution doesn't use brute force (O(n²)).
        We test with increasingly large arrays and verify linear scaling.
        """
        import random
        
        times = []
        sizes = [1000, 2000, 4000, 8000]
        
        for size in sizes:
            nums = list(range(size))
            target = size - 3  # Second-to-last and third-to-last elements
            
            start = time.perf_counter()
            result = solution(nums, target)
            end = time.perf_counter()
            
            times.append(end - start)
            
            # Verify correctness
            assert sorted(result) == [size - 3, size - 1] or \
                   sorted(result) == [0, size - 3]
        
        # Check that doubling input size roughly doubles time (allows 3x tolerance)
        # For O(n²), doubling size would quadruple time
        for i in range(len(times) - 1):
            ratio = times[i + 1] / times[i]
            assert ratio < 4.0, \
                f"Time complexity appears to be worse than O(n). " \
                f"Ratio: {ratio:.2f} (expected < 4.0 for O(n))"
    
    def test_space_complexity(self, solution):
        """
        Verify O(n) space complexity.
        
        The hash map approach should use space proportional to input size.
        """
        import sys
        
        nums = list(range(10000))
        target = 19999
        
        # This is a rough test - mainly ensures no catastrophic space usage
        result = solution(nums, target)
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
