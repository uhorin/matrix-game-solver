import numpy as np
import sys

from .graphical import solve_player_A_lp, solve_player_B_lp

def solve_with_simplex(matrix, print_matrix_func=None):
    print("КРОК 3: Розв'язання симплекс-методом (ЗЛП)")

    m, n = matrix.shape
    min_val = float(np.min(matrix))
    shift = 0.0
    if min_val <= 0:
        shift = abs(min_val) + 1.0
        print(f"\n  Матриця містить від'ємні або нульові елементи (min = {min_val:.4f}).")
        print(f"  Константа зсуву: k = |{min_val:.4f}| + 1 = {shift:.4f}")
        print("  Додаємо k до всіх елементів, умова v > 0 забезпечена.")
        working_matrix = matrix + shift
    else:
        working_matrix = matrix.copy()
        print(f"\n  Всі елементи матриці додатні (min = {min_val:.4f}). Зсув не потрібен.")

    if print_matrix_func is not None:
        print_matrix_func(working_matrix, "Робоча матриця (після зсуву)", output=sys.stdout)

    print("\nЗадача ЗЛП для гравця A (максимізація v)")
    print("  Мінімізувати: −v")
    print("  За умов:  −A^T · p + v·1 ≤ 0,   Σp_i = 1,   p_i ≥ 0")

    result_a = solve_player_A_lp(working_matrix)
    if result_a is None:
        print("Помилка при розв'язанні задачі для гравця A.")
        return None

    p, v_shifted = result_a
    v = float(v_shifted) - shift

    print("\nРезультат для гравця A (після нормалізації):")
    for i in range(m):
        print(f"    p{i+1} = {p[i]:.4f}")
    print(f" Ціна гри (з урахуванням зсуву k={shift:.4f}): v = {v:.4f}")

    print("\nЗадача ЗЛП для гравця B (мінімізація v)")
    print("  Мінімізувати: v")
    print("  За умов:  A · q − v·1 ≤ 0,   Σq_j = 1,   q_j ≥ 0")

    result_b = solve_player_B_lp(working_matrix)
    if result_b is None:
        print("Помилка при розв'язанні задачі для гравця B.")
        return None

    q, _ = result_b

    print("\n Результат для гравця B (після нормалізації):")
    for j in range(n):
        print(f"    q{j+1} = {q[j]:.4f}")

    return p, q, v
