import io
from contextlib import redirect_stdout

import numpy as np

SOLUTION_TOLERANCE = 1e-3

from formatting import format_matrix_text
from solvers.analytical import solve_2x2, solve_degenerate
from solvers.dominance import simplify_matrix
from solvers.graphical import solve_2x2_graphical, solve_2xn_graphical, solve_mx2_graphical
from solvers.saddle_point import check_saddle_point
from solvers.simplex import solve_with_simplex
from visualization.plots import plot_2x2_graphical, plot_2xn_graphical, plot_mx2_graphical


class MatrixGame:
    @staticmethod
    def _fmt_number(value):
        return np.format_float_positional(float(value), trim="-")

    def __init__(self, payoff_matrix):
        self.original_matrix = np.array(payoff_matrix, dtype=float)
        self.matrix = self.original_matrix.copy()
        self.m, self.n = self.matrix.shape

    def dispatch(self, matrix=None, show_plots=True):
        working_matrix = self.matrix if matrix is None else np.array(matrix, dtype=float)
        m, n = working_matrix.shape

        if m == 1 or n == 1:
            print("\n[Вибір методу] Вироджений випадок (тривіальний)")
            return solve_degenerate(working_matrix)

        if (m, n) == (2, 2):
            print("\n[Вибір методу] Обидва (графічний + аналітичний)")
            print("\nГрафічний метод")
            result_graph = solve_2x2_graphical(
                working_matrix,
                plotter=plot_2x2_graphical if show_plots else None,
            )
            print("\nАналітичний метод")
            result_anal = solve_2x2(working_matrix)
            return result_graph if result_graph is not None else result_anal

        if m == 2:
            print("\n[Вибір методу] Графічний 2×N")
            return solve_2xn_graphical(
                working_matrix,
                plotter=plot_2xn_graphical if show_plots else None,
            )

        if n == 2:
            print("\n[Вибір методу] Графічний M×2")
            return solve_mx2_graphical(
                working_matrix,
                plotter=plot_mx2_graphical if show_plots else None,
            )

        print("\n[Вибір методу] Симплекс (LP)")
        return solve_with_simplex(working_matrix, print_matrix_func=self.print_matrix)

    def print_matrix(self, matrix, title="Матриця", output=None):
        return format_matrix_text(matrix, title=title, number_formatter=self._fmt_number, output=output)

    def solve_to_data(self, matrix=None, show_plots=True):
        working_matrix = np.array(self.matrix if matrix is None else matrix, dtype=float)
        log_buf = io.StringIO()

        with redirect_stdout(log_buf):
            print(" " * 20 + "РОЗВ'ЯЗАННЯ МАТРИЧНОЇ ГРИ")
            print("\n[Вхідна матриця]")
            format_matrix_text(working_matrix, "Вихідна платіжна матриця", number_formatter=self._fmt_number, output=log_buf)

            has_saddle, saddle_value, saddle_row, saddle_col, _, _ = check_saddle_point(working_matrix)
            if has_saddle:
                value = float(saddle_value)
                reduced_matrix = working_matrix
                p = np.zeros(working_matrix.shape[0])
                q = np.zeros(working_matrix.shape[1])
                p[saddle_row] = 1.0
                q[saddle_col] = 1.0
            else:
                reduced_matrix, _ = simplify_matrix(working_matrix, print_matrix_func=self.print_matrix)
                result = self.dispatch(reduced_matrix, show_plots=show_plots)

                if result is None:
                    raise RuntimeError("Не вдалося знайти розв'язок")

                p, q, value = result
                value = float(value)

        return {
            "value": value,
            "p": p,
            "q": q,
            "original_shape": np.array(working_matrix).shape,
            "reduced_shape": reduced_matrix.shape,
            "reduced_matrix": reduced_matrix,
            "matrix": np.array(working_matrix, dtype=float),
            "log": log_buf.getvalue(),
            "is_saddle": has_saddle,
        }

    def solve(self, method=None):
        data = self.solve_to_data(show_plots=True)
        print(data["log"], end="")

        p = data["p"]
        q = data["q"]
        v = data["value"]

        if data["is_saddle"]:
            x_vector = "(" + ", ".join(str(int(x)) for x in p) + ")"
            y_vector = "(" + ", ".join(str(int(y)) for y in q) + ")"

            print(" " * 25 + "ПІДСУМКОВІ РЕЗУЛЬТАТИ")
            print(f"\nЦіна гри: v = {self._fmt_number(v)}")
            print("Програма заблокувала подальший перехід до симплекс-методу як обчислювально надлишковий.")
            print(f"Вектор оптимальних стратегій X^* = {x_vector}, Y^* = {y_vector} за ціни гри v = {self._fmt_number(v)}.")
            return

        print("\n" + "=" * 70)
        print(" " * 25 + "ПІДСУМКОВІ РЕЗУЛЬТАТИ")
        print("=" * 70)

        print(f"\nЦіна гри: v = {self._fmt_number(v)}")

        print("\nОптимальна змішана стратегія гравця A:")
        for i, prob in enumerate(p):
            if prob > 1e-6:
                print(f"  Стратегія A{i+1}: {self._fmt_number(prob)} ({self._fmt_number(prob*100)}%)")

        print("\nОптимальна змішана стратегія гравця B:")
        for j, prob in enumerate(q):
            if prob > 1e-6:
                print(f"  Стратегія B{j+1}: {self._fmt_number(prob)} ({self._fmt_number(prob*100)}%)")

        print("\n" + "=" * 70)
        print("ПЕРЕВІРКА РОЗВ'ЯЗКУ")
        print("=" * 70)

        expected_payoff = p @ self.matrix @ q
        print(f"\nОчікуваний виграш: p^T * A * q = {self._fmt_number(expected_payoff)}")
        print(f"Різниця з ціною гри: {self._fmt_number(abs(expected_payoff - v))}")

        if abs(expected_payoff - v) < SOLUTION_TOLERANCE:
            print("Розв'язок правильний!")
        else:
            print("Можлива помилка у розрахунках")
