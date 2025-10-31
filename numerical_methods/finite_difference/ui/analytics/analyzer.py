# ui/analytics/analyzer.py
import numpy as np
from typing import Dict, Any

class ResultAnalyzer:
    """Класс для аналитики результатов"""

    def __init__(self, epsilon: float = 0.5e-6):
        self.epsilon = epsilon

    def analyze(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Анализирует результаты вычислений"""
        diff = results['diff']
        x = results['x']

        max_diff = np.max(np.abs(diff))
        max_diff_index = np.argmax(np.abs(diff))
        max_diff_x = x[max_diff_index]

        mean_diff = np.mean(np.abs(diff))
        std_diff = np.std(diff)

        # Проверка точности
        epsilon_type = "ε2" if results['task_type'] == 'main' else "ε1"
        is_precise = max_diff <= self.epsilon

        analysis = {
            'max_difference': max_diff,
            'max_difference_position': max_diff_x,
            'mean_difference': mean_diff,
            'std_difference': std_diff,
            'epsilon_type': epsilon_type,
            'is_precise': is_precise,
            'nodes_count': len(x),
            'task_type': results['task_type']
        }

        return analysis

    def generate_report(self, analysis: Dict[str, Any], n: int) -> str:
        """Генерирует текстовый отчет"""
        report = f"""
АНАЛИТИЧЕСКИЙ ОТЧЕТ

Задача: {analysis['task_type']}
Количество узлов сетки: n = {n}
Требуемая точность: ε = {self.epsilon:.1e}

РЕЗУЛЬТАТЫ:
Максимальная разность ({analysis['epsilon_type']}): {analysis['max_difference']:.2e}
Положение максимальной разности: x = {analysis['max_difference_position']:.6f}
Средняя разность: {analysis['mean_difference']:.2e}
Стандартное отклонение: {analysis['std_difference']:.2e}

ТОЧНОСТЬ: {'✅ ДОСТИГНУТА' if analysis['is_precise'] else '❌ НЕ ДОСТИГНУТА'}
"""
        return report.strip()