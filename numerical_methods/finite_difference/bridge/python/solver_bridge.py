# bridge/python/solver_bridge.py
import sys
import os
from typing import Dict, Any
import numpy as np

# Добавляем путь к скомпилированному модулю
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'build'))

try:
    import diffeq_solver  # Скомпилированный PyBind11 модуль
except ImportError:
    # Для отладки - заглушка
    class MockTaskData:
        def __init__(self):
            self.i = []; self.x = []; self.v = []; self.u = []
            self.x2 = []; self.v2 = []; self.diff = []

    class MockDiffeqSolver:
        def solve(self, problem_type, nodes):
            data = MockTaskData()
            if problem_type == "test":
                for i in range(nodes):
                    x = i / (nodes - 1)
                    data.i.append(i)
                    data.x.append(x)
                    data.v.append(x * (1 - x))
                    data.u.append(x * (1 - x) + 0.1)
                    data.diff.append(0.1)
            return data

    diffeq_solver = MockDiffeqSolver()

class DifferentialEquationSolver:
    """Мост между Python UI и C++ солвером"""

    def __init__(self):
        pass

    def solve(self, n: int, task_type: str) -> Dict[str, Any]:
        """
        Решает дифференциальное уравнение

        Args:
            n: Количество узлов сетки
            task_type: Тип задачи ('main' или 'test')

        Returns:
            Словарь с результатами вычислений
        """
        if task_type not in ['main', 'test']:
            raise ValueError(f"Unknown task type: {task_type}. Use 'main' or 'test'")

        # Вызываем C++ солвер
        result_data = diffeq_solver.solve(task_type, n)

        # Конвертируем в Python словарь
        return self._convert_to_dict(result_data, task_type)

    def _convert_to_dict(self, task_data, task_type: str) -> Dict[str, Any]:
        """Конвертирует TaskData в Python словарь"""
        base_data = {
            'i': np.array(task_data.i),
            'x': np.array(task_data.x),
            'v': np.array(task_data.v),
            'diff': np.array(task_data.diff),
            'task_type': task_type
        }

        if task_type == 'test':
            base_data['u'] = np.array(task_data.u)
        else:  # main task
            base_data['x2'] = np.array(task_data.x2)
            base_data['v2'] = np.array(task_data.v2)

        return base_data