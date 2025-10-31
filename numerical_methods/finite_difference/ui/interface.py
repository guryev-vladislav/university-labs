# ui/interface.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from pathlib import Path
import sys
import os
import signal

# Добавляем пути для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bridge', 'python'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from bridge.python.solver_bridge import DifferentialEquationSolver
    from visualization.plotter import ResultPlotter
    from analytics.analyzer import ResultAnalyzer
except ImportError as e:
    print(f"Import error: {e}")


    # Создаем заглушки для отладки
    class DifferentialEquationSolver:
        def solve(self, n, task_type):
            import numpy as np
            x = np.linspace(0, 1, n)
            v = x * (1 - x)
            return {
                'x': x, 'v': v, 'diff': np.zeros(n),
                'task_type': task_type,
                'u': v + 0.1 if task_type == 'test' else None,
                'v2': v + 0.05 if task_type == 'main' else None
            }


    class ResultPlotter:
        def create_comparison_plot(self, results, n): return "plot.png"

        def create_error_analysis_plot(self, results, n): return "error_plot.png"


    class ResultAnalyzer:
        def __init__(self, epsilon=0.5e-6): pass

        def analyze(self, results):
            return {
                'max_difference': 0.1,
                'max_difference_position': 0.5,
                'task_type': results['task_type'],
                'mean_difference': 0.05,
                'std_difference': 0.02,
                'epsilon_type': 'ε1' if results['task_type'] == 'test' else 'ε2',
                'is_precise': False
            }

        def generate_report(self, analysis, n):
            return f"Отчет для {analysis['task_type']}, n={n}"


class SolverApp:
    """Графический интерфейс для решения дифференциальных уравнений"""

    def __init__(self):
        self.solver = DifferentialEquationSolver()
        self.plotter = ResultPlotter()
        self.analyzer = ResultAnalyzer()

        self.current_results = None
        self.current_analysis = None

        # Обработка Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

        self.setup_ui()

    def signal_handler(self, signum, frame):
        """Обработчик Ctrl+C"""
        print("\nЗавершение работы...")
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

    def setup_ui(self):
        """Настраивает графический интерфейс"""
        self.root = tk.Tk()
        self.root.title("Численные методы - Решение ДУ")
        self.root.geometry("1200x800")

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Параметры решения")
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Выбор задачи
        ttk.Label(control_frame, text="Тип задачи:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.task_var = tk.StringVar(value="test")
        task_combo = ttk.Combobox(control_frame, textvariable=self.task_var,
                                  values=["test", "main"], state="readonly")
        task_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Количество узлов
        ttk.Label(control_frame, text="Количество узлов (n):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.n_var = tk.StringVar(value="100")
        n_entry = ttk.Entry(control_frame, textvariable=self.n_var)
        n_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Кнопка решения
        self.solve_btn = ttk.Button(control_frame, text="Решить", command=self.solve)
        self.solve_btn.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

        # Прогресс бар
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.grid(row=2, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=5)

        # Фрейм для результатов
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Левая панель - графики
        left_frame = ttk.Frame(results_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # График решений
        solution_frame = ttk.LabelFrame(left_frame, text="График решений")
        solution_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 5))

        self.solution_fig, self.solution_ax = plt.subplots(figsize=(6, 4))
        self.solution_canvas = FigureCanvasTkAgg(self.solution_fig, solution_frame)
        self.solution_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # График ошибки
        error_frame = ttk.LabelFrame(left_frame, text="График ошибки")
        error_frame.pack(fill=tk.BOTH, expand=True, padx=(0, 5), pady=(5, 0))

        self.error_fig, self.error_ax = plt.subplots(figsize=(6, 4))
        self.error_canvas = FigureCanvasTkAgg(self.error_fig, error_frame)
        self.error_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Правая панель - аналитика
        right_frame = ttk.Frame(results_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(5, 0))

        # Аналитический отчет
        analysis_frame = ttk.LabelFrame(right_frame, text="Аналитический отчет")
        analysis_frame.pack(fill=tk.BOTH, expand=True)

        self.analysis_text = tk.Text(analysis_frame, width=40, height=20, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(analysis_frame, orient=tk.VERTICAL, command=self.analysis_text.yview)
        self.analysis_text.configure(yscrollcommand=scrollbar.set)

        self.analysis_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки экспорта
        export_frame = ttk.Frame(right_frame)
        export_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Button(export_frame, text="Сохранить графики",
                   command=self.save_plots).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(export_frame, text="Сохранить отчет",
                   command=self.save_report).pack(side=tk.LEFT)

    def on_closing(self):
        """Обработчик закрытия окна"""
        print("Закрытие приложения...")
        self.root.quit()
        self.root.destroy()

    def solve(self):
        """Запускает решение в отдельном потоке"""
        try:
            n = int(self.n_var.get())
            task_type = self.task_var.get()

            if n < 3:
                messagebox.showerror("Ошибка", "Количество узлов должно быть не менее 3")
                return

            # Блокируем интерфейс
            self.solve_btn.config(state='disabled')
            self.progress.start()

            # Запускаем в отдельном потоке
            thread = threading.Thread(target=self._solve_thread, args=(n, task_type))
            thread.daemon = True
            thread.start()

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число узлов")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при решении: {str(e)}")
            self._enable_interface()

    def _solve_thread(self, n: int, task_type: str):
        """Поток для решения уравнения"""
        try:
            # Вызываем C++ солвер
            results = self.solver.solve(n, task_type)
            analysis = self.analyzer.analyze(results)

            # Обновляем UI в основном потоке
            self.root.after(0, self._update_interface, results, analysis, n)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка при решении: {str(e)}"))
        finally:
            self.root.after(0, self._enable_interface)

    def _update_interface(self, results: dict, analysis: dict, n: int):
        """Обновляет интерфейс с результатами"""
        self.current_results = results
        self.current_analysis = analysis

        # Обновляем графики
        self._update_plots(results, n)

        # Обновляем аналитику
        report = self.analyzer.generate_report(analysis, n)
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, report)

    def _update_plots(self, results: dict, n: int):
        """Обновляет графики"""
        # График решений
        self.solution_ax.clear()
        x = results['x']

        self.solution_ax.plot(x, results['v'], 'b-', linewidth=2, label='v(x)')

        if results['task_type'] == 'test':
            self.solution_ax.plot(x, results['u'], 'r--', linewidth=2, label='u(x)')
            title_suffix = 'v(x) и аналитическое u(x)'
        else:
            self.solution_ax.plot(x, results['v2'], 'g--', linewidth=2, label='v2(x)')
            title_suffix = 'v(x) и v2(x)'

        self.solution_ax.set_xlabel('x')
        self.solution_ax.set_ylabel('Решение')
        self.solution_ax.set_title(f'Сравнение решений ({title_suffix}), n={n}')
        self.solution_ax.legend()
        self.solution_ax.grid(True, alpha=0.3)
        self.solution_canvas.draw()

        # График ошибки
        self.error_ax.clear()
        self.error_ax.plot(x, results['diff'], 'r-', linewidth=2, label='Разность')
        self.error_ax.set_xlabel('x')
        self.error_ax.set_ylabel('Разность')
        self.error_ax.set_title(f'Разность решений, n={n}')
        self.error_ax.legend()
        self.error_ax.grid(True, alpha=0.3)
        self.error_canvas.draw()

    def _enable_interface(self):
        """Включает интерфейс после решения"""
        self.solve_btn.config(state='normal')
        self.progress.stop()

    def save_plots(self):
        """Сохраняет графики в файлы"""
        if self.current_results is None:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения")
            return

        n = len(self.current_results['x'])
        task_type = self.current_results['task_type']

        try:
            # Создаем графики
            plot1 = self.plotter.create_comparison_plot(self.current_results, n)
            plot2 = self.plotter.create_error_analysis_plot(self.current_results, n)

            messagebox.showinfo("Успех", f"Графики сохранены:\n{plot1}\n{plot2}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении графиков: {str(e)}")

    def save_report(self):
        """Сохраняет отчет в файл"""
        if self.current_analysis is None:
            messagebox.showwarning("Предупреждение", "Нет отчета для сохранения")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if filename:
            try:
                n = len(self.current_results['x'])
                report = self.analyzer.generate_report(self.current_analysis, n)

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)

                messagebox.showinfo("Успех", f"Отчет сохранен: {filename}")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении отчета: {str(e)}")

    def run(self):
        """Запускает приложение"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()