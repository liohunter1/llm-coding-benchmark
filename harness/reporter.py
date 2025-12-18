"""
Benchmark results reporter - generates reports and visualizations.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class BenchmarkReporter:
    """Generates benchmark reports and visualizations."""
    
    def __init__(self, output_dir: Path = Path("results")):
        """Initialize reporter."""
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_html_report(
        self,
        results: Dict[str, Any],
        output_file: Path
    ) -> None:
        """
        Generate HTML report from benchmark results.
        
        Args:
            results: Benchmark results dictionary
            output_file: Path to save HTML report
        """
        html_content = self._build_html(results)
        
        with open(output_file, "w") as f:
            f.write(html_content)
    
    def generate_comparison_report(
        self,
        results_list: List[Dict[str, Any]],
        output_file: Path
    ) -> None:
        """
        Generate comparison report for multiple model results.
        
        Args:
            results_list: List of benchmark results to compare
            output_file: Path to save comparison report
        """
        html_content = self._build_comparison_html(results_list)
        
        with open(output_file, "w") as f:
            f.write(html_content)
    
    def _build_html(self, results: Dict[str, Any]) -> str:
        """Build HTML report."""
        model = results.get("model", "Unknown")
        overall = results.get("overall", {})
        problems = results.get("problems", [])
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>LLM Benchmark Report - {model}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }}
        .metric {{ background: #e8f4f8; padding: 15px; border-radius: 5px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #0066cc; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f0f0f0; font-weight: bold; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>LLM Coding Benchmark Report</h1>
        <p><strong>Model:</strong> {model}</p>
        <p><strong>Date:</strong> {results.get('timestamp', 'N/A')}</p>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <div>Total Problems</div>
            <div class="metric-value">{overall.get('total_problems', 0)}</div>
        </div>
        <div class="metric">
            <div>Average Score</div>
            <div class="metric-value">{overall.get('average_score', 0):.1f}/100</div>
        </div>
        <div class="metric">
            <div>Pass Rate</div>
            <div class="metric-value">{overall.get('pass_rate', 0)*100:.1f}%</div>
        </div>
        <div class="metric">
            <div>Optimal Rate</div>
            <div class="metric-value">{overall.get('optimal_rate', 0)*100:.1f}%</div>
        </div>
    </div>
    
    <h2>Problem Results</h2>
    <table>
        <tr>
            <th>Problem ID</th>
            <th>Score</th>
            <th>Status</th>
        </tr>
        {''.join(f'<tr><td>{p.get("problem_id")}</td><td>{p.get("total_score", 0)}/100</td><td class="{"pass" if p.get("total_score", 0) >= 60 else "fail"}">{"✓ Pass" if p.get("total_score", 0) >= 60 else "✗ Fail"}</td></tr>' for p in problems)}
    </table>
</body>
</html>"""
        
        return html
    
    def _build_comparison_html(self, results_list: List[Dict[str, Any]]) -> str:
        """Build comparison HTML report."""
        models = [r.get("model", "Unknown") for r in results_list]
        
        html = """<!DOCTYPE html>
<html>
<head>
    <title>LLM Benchmark Comparison Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f0f0f0; font-weight: bold; }
        .winner { background: #c8e6c9; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>LLM Benchmark Comparison Report</h1>
        <p>Comparing: """ + ", ".join(models) + """</p>
    </div>
    
    <h2>Overall Metrics</h2>
    <table>
        <tr>
            <th>Model</th>
            <th>Average Score</th>
            <th>Pass Rate</th>
            <th>Optimal Rate</th>
        </tr>
        """ + "".join(f"""
        <tr>
            <td>{r.get('model')}</td>
            <td>{r.get('overall', {}).get('average_score', 0):.1f}/100</td>
            <td>{r.get('overall', {}).get('pass_rate', 0)*100:.1f}%</td>
            <td>{r.get('overall', {}).get('optimal_rate', 0)*100:.1f}%</td>
        </tr>
        """ for r in results_list) + """
    </table>
</body>
</html>"""
        
        return html
