import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SolutionAnalyzer:
    def __init__(self):
        self.solution_data = None
        self.system_type = None

    def set_solution_data(self, solution_data: List[Dict[str, Any]], system_type: str):
        self.solution_data = solution_data
        self.system_type = system_type

    def get_statistics(self) -> Dict[str, Any]:
        if not self.solution_data:
            logger.warning("No solution data available for analysis")
            return {}

        df = pd.DataFrame(self.solution_data)

        stats = {
            'total_steps': len(df),
            'final_x': df['x'].iloc[-1],
            'final_u': df['u'].iloc[-1],
            'max_step_size': df['step_size'].max(),
            'min_step_size': df['step_size'].min(),
            'mean_step_size': df['step_size'].mean(),
            'total_step_reductions': df['step_reductions'].sum(),
            'total_step_increases': df['step_increases'].sum(),
        }

        if self.system_type == "task2":
            stats['final_u1'] = df['u1'].iloc[-1]
            stats['max_u1'] = df['u1'].max()
            stats['min_u1'] = df['u1'].min()

        if 'error_estimate' in df.columns:
            stats['max_error_estimate'] = df['error_estimate'].abs().max()
            stats['mean_error_estimate'] = df['error_estimate'].abs().mean()

        return stats

    def get_convergence_info(self) -> Dict[str, Any]:
        if not self.solution_data or len(self.solution_data) < 2:
            return {}

        df = pd.DataFrame(self.solution_data)

        convergence = {
            'step_size_variation': df['step_size'].std() / df['step_size'].mean(),
            'step_adjustment_frequency': (df['step_reductions'] + df['step_increases']).sum() / len(df),
        }

        return convergence

    def generate_report(self) -> str:
        stats = self.get_statistics()
        convergence = self.get_convergence_info()

        report_lines = []
        report_lines.append("SOLUTION ANALYSIS REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"System type: {self.system_type}")
        report_lines.append(f"Total steps: {stats.get('total_steps', 'N/A')}")
        report_lines.append(f"Final x: {stats.get('final_x', 'N/A'):.6f}")
        report_lines.append(f"Final u: {stats.get('final_u', 'N/A'):.6f}")

        if 'final_u1' in stats:
            report_lines.append(f"Final u': {stats['final_u1']:.6f}")

        report_lines.append(f"Step size range: {stats.get('min_step_size', 'N/A'):.2e} - {stats.get('max_step_size', 'N/A'):.2e}")
        report_lines.append(f"Total step reductions: {stats.get('total_step_reductions', 'N/A')}")
        report_lines.append(f"Total step increases: {stats.get('total_step_increases', 'N/A')}")

        if 'max_error_estimate' in stats:
            report_lines.append(f"Maximum error estimate: {stats['max_error_estimate']:.2e}")

        report_lines.append(f"Step size variation: {convergence.get('step_size_variation', 'N/A'):.4f}")

        return "\n".join(report_lines)