# main.py
#!/usr/bin/env python3
"""
Главный файл для запуска приложения решения дифференциальных уравнений
"""

import sys
import os

# Добавляем пути к модулям
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'bridge', 'python'))
sys.path.append(os.path.join(current_dir, 'ui'))

try:
    from ui.interface import SolverApp
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Запуск в режиме консольного теста...")

    # Простой тест
    sys.path.append('build')
    try:
        import diffeq_solver
        result = diffeq_solver.solve('test', 11)
        print(f"✅ Модуль работает! Узлов: {len(result.x)}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    sys.exit(1)

def main():
    """Основная функция запуска"""
    print("Запуск приложения для решения дифференциальных уравнений...")

    try:
        app = SolverApp()
        app.run()
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()