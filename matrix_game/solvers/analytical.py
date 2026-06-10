import numpy as np


def _fmt_number(value):
    return np.format_float_positional(float(value), trim="-")


def solve_degenerate(matrix):
    print("КРОК 3: Розв'язання вирoдженого випадку")

    m, n = matrix.shape

    if m == 1 and n == 1:
        print(f"\nМатриця зведена до одного елемента: {_fmt_number(matrix[0, 0])}")
        print("Обидва гравці мають лише по одній стратегії після редукції.")

        p = np.array([1.0])
        q = np.array([1.0])
        v = matrix[0, 0]

        print("\nОптимальна стратегія гравця A: A1 з ймовірністю 1.0")
        print("Оптимальна стратегія гравця B: B1 з ймовірністю 1.0")
        print(f"Ціна гри: v = {_fmt_number(v)}")
        return p, q, v

    if m == 1:
        print("\nГравець A має лише одну стратегію після редукції.")
        print(f"Платежі: {matrix[0]}")

        p = np.array([1.0])
        min_col = np.argmin(matrix[0])
        v = matrix[0, min_col]

        q = np.zeros(n)
        q[min_col] = 1.0

        print("\nОптимальна стратегія гравця A: A1 з ймовірністю 1.0")
        print(f"Оптимальна стратегія гравця B: B{min_col+1} з ймовірністю 1.0")
        print(f"Ціна гри: v = {_fmt_number(v)}")
        return p, q, v

    if n == 1:
        print("\nГравець B має лише одну стратегію після редукції.")
        print(f"Платежі: {matrix[:, 0]}")

        q = np.array([1.0])
        max_row = np.argmax(matrix[:, 0])
        v = matrix[max_row, 0]

        p = np.zeros(m)
        p[max_row] = 1.0

        print(f"\nОптимальна стратегія гравця A: A{max_row+1} з ймовірністю 1.0")
        print("Оптимальна стратегія гравця B: B1 з ймовірністю 1.0")
        print(f"Ціна гри: v = {_fmt_number(v)}")
        return p, q, v

    return None


def solve_2x2(matrix):
    print("КРОК 3: Аналітичне розв'язання гри 2x2")

    a11, a12 = matrix[0]
    a21, a22 = matrix[1]

    print("\nМатриця гри:")
    print("    B1   B2")
    print(f"A1 [{_fmt_number(a11)} {_fmt_number(a12)}]")
    print(f"A2 [{_fmt_number(a21)} {_fmt_number(a22)}]")

    denominator_a = a11 - a21 - a12 + a22
    if abs(denominator_a) < 1e-10:
        print("\nПопередження: знаменник близький до нуля")
        return None

    p1 = (a22 - a21) / denominator_a
    p2 = 1 - p1

    print("\nОптимальна змішана стратегія гравця A:")
    print("p1 = (a22 - a21) / (a11 - a21 - a12 + a22)")
    print(f"p1 = ({a22} - {a21}) / ({a11} - {a21} - {a12} + {a22})")
    print(f"p1 = {_fmt_number(a22 - a21)} / {_fmt_number(denominator_a)} = {_fmt_number(p1)}")
    print(f"p2 = 1 - p1 = {_fmt_number(p2)}")

    tol = 1e-10
    if not np.isfinite(p1):
        print("\nПопередження: обчислене p1 не є скінченним числом")
        return None
    if p1 < -tol or p1 > 1 + tol:
        print(f"\nПопередження: обчислене p1 = {_fmt_number(p1)} поза діапазоном [0,1]")
        return None
    p1 = float(np.clip(p1, 0.0, 1.0))
    p2 = 1.0 - p1

    q1 = (a22 - a12) / denominator_a
    q2 = 1 - q1

    print("\nОптимальна змішана стратегія гравця B:")
    print("q1 = (a22 - a12) / (a11 - a21 - a12 + a22)")
    print(f"q1 = ({_fmt_number(a22)} - {_fmt_number(a12)}) / {_fmt_number(denominator_a)} = {_fmt_number(q1)}")
    print(f"q2 = 1 - q1 = {_fmt_number(q2)}")

    if not np.isfinite(q1):
        print("\nПопередження: обчислене q1 не є скінченним числом")
        return None
    if q1 < -tol or q1 > 1 + tol:
        print(f"\nПопередження: обчислене q1 = {_fmt_number(q1)} поза діапазоном [0,1]")
        return None
    q1 = float(np.clip(q1, 0.0, 1.0))
    q2 = 1.0 - q1

    v = (a11 * a22 - a12 * a21) / denominator_a

    print("\nЦіна гри:")
    print("v = (a11*a22 - a12*a21) / (a11 - a21 - a12 + a22)")
    print(f"v = ({_fmt_number(a11)}*{_fmt_number(a22)} - {_fmt_number(a12)}*{_fmt_number(a21)}) / {_fmt_number(denominator_a)}")
    print(f"v = {_fmt_number(a11 * a22 - a12 * a21)} / {_fmt_number(denominator_a)} = {_fmt_number(v)}")

    return np.array([p1, p2]), np.array([q1, q2]), v
