"""
Problem evaluator - runs tests and grades solutions.
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Any


class ProblemEvaluator:
    """Evaluates LLM-generated solutions against test suites."""
    
    def __init__(self, language: str = "python"):
        """
        Initialize evaluator.
        
        Args:
            language: Programming language for solutions
        """
        self.language = language
    
    def evaluate(self, problem_id: str, code: str) -> Dict[str, Any]:
        """
        Evaluate a solution for a problem.
        
        Args:
            problem_id: Problem identifier (e.g., "p01_two_sum")
            code: Generated code to evaluate
            
        Returns:
            Dictionary with evaluation results
        """
        problem_dir = Path("problems") / problem_id
        
        # Save code to temporary file
        temp_file = problem_dir / f"temp_solution.{self._get_extension()}"
        with open(temp_file, "w") as f:
            f.write(code)
        
        try:
            # Run tests
            test_results = self._run_tests(problem_dir, temp_file)
            
            # Grade based on rubric
            score = self._calculate_score(test_results, problem_dir)
            
            return {
                "test_results": test_results,
                "total_score": score,
                "passed": test_results.get("passed", False)
            }
        
        finally:
            # Cleanup
            if temp_file.exists():
                temp_file.unlink()
    
    def _run_tests(self, problem_dir: Path, solution_file: Path) -> Dict[str, Any]:
        """Run test suite for the problem."""
        if self.language == "python":
            return self._run_python_tests(problem_dir, solution_file)
        else:
            raise NotImplementedError(f"Language {self.language} not yet supported")
    
    def _run_python_tests(self, problem_dir: Path, solution_file: Path) -> Dict[str, Any]:
        """Run Python pytest suite."""
        test_file = problem_dir / "tests" / "test_python.py"
        
        if not test_file.exists():
            raise FileNotFoundError(f"Test file not found: {test_file}")
        
        # Run pytest
        result = subprocess.run(
            ["pytest", str(test_file), "-v", "--tb=short", "--json-report", "--json-report-file=report.json"],
            capture_output=True,
            text=True,
            cwd=problem_dir
        )
        
        # Parse results
        report_file = problem_dir / "report.json"
        if report_file.exists():
            with open(report_file) as f:
                report = json.load(f)
            report_file.unlink()  # Cleanup
            
            return {
                "passed": result.returncode == 0,
                "total_tests": report.get("summary", {}).get("total", 0),
                "passed_tests": report.get("summary", {}).get("passed", 0),
                "failed_tests": report.get("summary", {}).get("failed", 0),
                "output": result.stdout
            }
        else:
            # Fallback to basic parsing
            return {
                "passed": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
    
    def _calculate_score(self, test_results: Dict[str, Any], problem_dir: Path) -> int:
        """Calculate score based on test results and rubric."""
        # Load rubric (if exists)
        rubric_file = problem_dir / "rubric.md"
        
        # Basic scoring if no detailed rubric
        if not rubric_file.exists():
            return 100 if test_results.get("passed", False) else 0
        
        # Detailed scoring
        passed_tests = test_results.get("passed_tests", 0)
        total_tests = test_results.get("total_tests", 1)
        
        # Correctness: 60 points
        correctness_score = (passed_tests / total_tests) * 60 if total_tests > 0 else 0
        
        # Complexity: 30 points (assume optimal if all tests pass)
        complexity_score = 30 if test_results.get("passed", False) else 0
        
        # Code quality: 10 points (basic heuristic)
        quality_score = 10 if test_results.get("passed", False) else 5
        
        return int(correctness_score + complexity_score + quality_score)
    
    def _get_extension(self) -> str:
        """Get file extension for language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "cpp": "cpp"
        }
        return extensions.get(self.language, "txt")
