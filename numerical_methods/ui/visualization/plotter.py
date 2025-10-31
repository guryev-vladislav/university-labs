# ui/visualization/plotter.py
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, Any

class ResultPlotter:
    """Класс для визуализации результатов"""

    def __init__(self, output_dir: str = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        plt.style.use('seaborn-v0_8')

    def create_comparison_plot(self, results: Dict[str, Any], n: int) -> str:
        """Создает график сравнения решений"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        x = results['x']
        task_type = results['task_type']

        # Верхний график - решения
        ax1.plot(x, results['v'], 'b-', linewidth=2, label='v(x)')

        if task_type == 'test':
            ax1.plot(x, results['u'], 'r--', linewidth=2, label='u(x)')
            title_suffix = 'v(x) и аналитическое u(x)'
        else:
            ax1.plot(x, results['v2'], 'g--', linewidth=2, label='v2(x)')
            title_suffix = 'v(x) и v2(x)'

        ax1.set_xlabel('x')
        ax1.set_ylabel('Решение')
        ax1.set_title(f'Сравнение решений ({title_suffix}), n={n}')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Нижний график - ошибка
        ax2.plot(x, results['diff'], 'r-', linewidth=2, label='Разность')
        ax2.set_xlabel('x')
        ax2.set_ylabel('Разность')
        ax2.set_title(f'Разность решений, n={n}')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = self.output_dir / f'comparison_{task_type}_{n}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        return str(filename)

    def create_error_analysis_plot(self, results: Dict[str, Any], n: int) -> str:
        """Создает детальный анализ ошибки"""
        fig, ax = plt.subplots(figsize=(10, 6))

        x = results['x']
        diff = results['diff']

        ax.semilogy(x, np.abs(diff), 'r-', linewidth=2, label='|Разность|')
        ax.set_xlabel('x')
        ax.set_ylabel('Абсолютная разность (лог. шкала)')
        ax.set_title(f'Анализ ошибки, n={n}')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = self.output_dir / f'error_analysis_{results["task_type"]}_{n}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        return str(filename)