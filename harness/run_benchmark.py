"""
LLM Coding Benchmark Suite - Main benchmark runner
"""

import argparse
import os
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .llm_client import LLMClient
from .evaluator import ProblemEvaluator
from .reporter import BenchmarkReporter


class BenchmarkRunner:
    """Main benchmark orchestrator."""
    
    def __init__(
        self,
        model: str,
        problems: List[str],
        language: str = "python",
        output_dir: Path = Path("results")
    ):
        """
        Initialize benchmark runner.
        
        Args:
            model: LLM model name (e.g., "gpt-4-turbo")
            problems: List of problem IDs to run (e.g., ["p01", "p02"])
            language: Programming language for solutions
            output_dir: Directory to save results
        """
        self.model = model
        self.problems = problems
        self.language = language
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.llm_client = LLMClient(model=model)
        self.evaluator = ProblemEvaluator(language=language)
        
    def run(self) -> Dict[str, Any]:
        """
        Run the full benchmark.
        
        Returns:
            Dictionary containing benchmark results
        """
        print(f"\n{'=' * 60}")
        print(f"  LLM Coding Benchmark")
        print(f"  Model: {self.model}")
        print(f"  Language: {self.language}")
        print(f"  Problems: {len(self.problems)}")
        print(f"{'=' * 60}\n")
        
        results = {
            "model": self.model,
            "language": self.language,
            "timestamp": datetime.utcnow().isoformat(),
            "problems": []
        }
        
        for i, problem_id in enumerate(self.problems, 1):
            print(f"\n[{i}/{len(self.problems)}] Running {problem_id}...")
            
            try:
                problem_result = self._run_single_problem(problem_id)
                results["problems"].append(problem_result)
                
                score = problem_result["total_score"]
                print(f"  ✓ Completed: {score}/100")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                results["problems"].append({
                    "problem_id": problem_id,
                    "error": str(e),
                    "total_score": 0
                })
        
        # Calculate overall statistics
        results["overall"] = self._calculate_overall_stats(results["problems"])
        
        # Save results
        self._save_results(results)
        
        # Print summary
        self._print_summary(results)
        
        return results
    
    def _run_single_problem(self, problem_id: str) -> Dict[str, Any]:
        """Run benchmark for a single problem."""
        problems_dir = Path("problems")
        problem_dir = problems_dir / problem_id
        
        if not problem_dir.exists():
            raise FileNotFoundError(f"Problem directory not found: {problem_dir}")
        
        # Load problem statement
        problem_file = problem_dir / "problem.md"
        with open(problem_file) as f:
            problem_statement = f.read()
        
        # Get LLM solution
        print("  Querying LLM...")
        llm_response = self.llm_client.generate_solution(
            problem_statement=problem_statement,
            language=self.language
        )
        
        # Extract code from response
        code = self._extract_code(llm_response)
        
        # Save generated solution
        solution_file = problem_dir / f"llm_solution_{self.model}.{self._get_extension()}"
        with open(solution_file, "w") as f:
            f.write(code)
        
        # Evaluate solution
        print("  Evaluating solution...")
        evaluation = self.evaluator.evaluate(
            problem_id=problem_id,
            code=code
        )
        
        return {
            "problem_id": problem_id,
            "code": code,
            "evaluation": evaluation,
            "total_score": evaluation.get("total_score", 0)
        }
    
    def _extract_code(self, llm_response: str) -> str:
        """Extract code from LLM response."""
        # Look for code blocks
        import re
        
        # Try to find code fence
        pattern = r"```(?:python|javascript|java|cpp)?\n(.*?)```"
        matches = re.findall(pattern, llm_response, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code fence, return entire response
        return llm_response.strip()
    
    def _get_extension(self) -> str:
        """Get file extension for language."""
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "cpp": "cpp"
        }
        return extensions.get(self.language, "txt")
    
    def _calculate_overall_stats(self, problem_results: List[Dict]) -> Dict[str, Any]:
        """Calculate overall benchmark statistics."""
        scores = [p.get("total_score", 0) for p in problem_results]
        
        return {
            "total_problems": len(problem_results),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "pass_rate": sum(1 for s in scores if s >= 60) / len(scores) if scores else 0,
            "optimal_rate": sum(1 for s in scores if s >= 90) / len(scores) if scores else 0
        }
    
    def _save_results(self, results: Dict[str, Any]):
        """Save results to JSON file."""
        output_file = self.output_dir / f"{self.model}_{self.language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_file}")
    
    def _print_summary(self, results: Dict[str, Any]):
        """Print benchmark summary."""
        overall = results["overall"]
        
        print(f"\n{'=' * 60}")
        print(f"  Benchmark Summary")
        print(f"{'=' * 60}")
        print(f"  Total Problems:   {overall['total_problems']}")
        print(f"  Average Score:    {overall['average_score']:.1f}/100")
        print(f"  Pass Rate:        {overall['pass_rate']*100:.1f}%")
        print(f"  Optimal Rate:     {overall['optimal_rate']*100:.1f}%")
        print(f"{'=' * 60}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LLM Coding Benchmark Runner")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-5"), help="LLM model name")
    parser.add_argument("--problems", default="all", help="Comma-separated problem IDs or 'all'")
    parser.add_argument("--language", default="python", choices=["python", "javascript", "java", "cpp"])
    parser.add_argument("--output-dir", default="results", help="Output directory for results")
    
    args = parser.parse_args()
    
    # Determine which problems to run
    if args.problems == "all":
        problems_dir = Path("problems")
        problems = [p.name for p in problems_dir.iterdir() if p.is_dir()]
    else:
        problems = args.problems.split(",")
    
    # Run benchmark
    runner = BenchmarkRunner(
        model=args.model,
        problems=problems,
        language=args.language,
        output_dir=Path(args.output_dir)
    )
    
    runner.run()


if __name__ == "__main__":
    main()
