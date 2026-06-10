import numpy as np
from scipy.optimize import linprog


def _fmt_number(value):
    return np.format_float_positional(float(value), trim="-")

def solve_player_A_lp(matrix):
    m, n = matrix.shape
    c = np.zeros(m + 1)
    c[-1] = -1

    a_ub = np.hstack([-matrix.T, np.ones((n, 1))])
    b_ub = np.zeros(n)

    a_eq = np.zeros((1, m + 1))
    a_eq[0, :m] = 1
    b_eq = np.array([1.0])

    bounds = [(0, None) for _ in range(m)] + [(None, None)]
    result = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not result.success:
        return None

    p = np.clip(result.x[:m], 0.0, None)
    p_sum = p.sum()
    if p_sum > 0:
        p = p / p_sum
    return p, result.x[-1]


def solve_player_B_lp(matrix):
    m, n = matrix.shape
    c = np.zeros(n + 1)
    c[-1] = 1

    a_ub = np.hstack([matrix, -np.ones((m, 1))])
    b_ub = np.zeros(m)

    a_eq = np.zeros((1, n + 1))
    a_eq[0, :n] = 1
    b_eq = np.array([1.0])

    bounds = [(0, None) for _ in range(n)] + [(None, None)]
    result = linprog(c, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not result.success:
        return None

    q = np.clip(result.x[:n], 0.0, None)
    q_sum = q.sum()
    if q_sum > 0:
        q = q / q_sum
    return q, result.x[-1]


def solve_2x2_graphical(matrix, plotter=None):
    print("КРОК 3: Графічне розв'язання гри 2x2")

    a11, a12 = matrix[0]
    a21, a22 = matrix[1]

    print("\nМатриця гри:")
    print("    B1   B2")
    print(f"A1 [{_fmt_number(a11)} {_fmt_number(a12)}]")
    print(f"A2 [{_fmt_number(a21)} {_fmt_number(a22)}]")

    print("\nДля гравця A (параметр p = P(A1)):")
    print(f"f1(p) = a21 + (a11-a21)*p = {_fmt_number(a21)} + ({_fmt_number(a11-a21)})*p")
    print(f"f2(p) = a22 + (a12-a22)*p = {_fmt_number(a22)} + ({_fmt_number(a12-a22)})*p")
    print("A максимізує нижню огинаючу: g(p) = min(f1(p), f2(p))")

    denominator = a11 - a21 - a12 + a22
    p_candidates = [0.0, 1.0]
    if abs(denominator) > 1e-10:
        p_intersection = (a22 - a21) / denominator
        if 0.0 <= p_intersection <= 1.0:
            p_candidates.append(p_intersection)
            print(f"Точка перетину f1=f2: p* = {_fmt_number(p_intersection)}")
        else:
            print("Точка перетину f1=f2 поза [0, 1], перевіряємо лише межі")
    else:
        print("f1 і f2 паралельні або збігаються, перевіряємо лише межі")

    best_p = None
    best_g = -np.inf
    for p in p_candidates:
        f1 = a21 + (a11 - a21) * p
        f2 = a22 + (a12 - a22) * p
        g = min(f1, f2)
        if g > best_g:
            best_g = g
            best_p = p

    p1 = best_p
    p2 = 1 - p1
    v_from_p = best_g

    print(f"\nОптимум для A: p1 = {_fmt_number(p1)}, p2 = {_fmt_number(p2)}")
    print(f"Гарантований виграш A: v = {_fmt_number(v_from_p)}")

    print("\nДля гравця B (параметр q = P(B1)):")
    print(f"u1(q) = a12 + (a11-a12)*q = {_fmt_number(a12)} + ({_fmt_number(a11-a12)})*q")
    print(f"u2(q) = a22 + (a21-a22)*q = {_fmt_number(a22)} + ({_fmt_number(a21-a22)})*q")
    print("B мінімізує верхню огинаючу: h(q) = max(u1(q), u2(q))")

    q_candidates = [0.0, 1.0]
    if abs(denominator) > 1e-10:
        q_intersection = (a22 - a12) / denominator
        if 0.0 <= q_intersection <= 1.0:
            q_candidates.append(q_intersection)
            print(f"Точка перетину u1=u2: q* = {_fmt_number(q_intersection)}")
        else:
            print("Точка перетину u1=u2 поза [0, 1], перевіряємо лише межі")

    best_q = None
    best_h = np.inf
    for q in q_candidates:
        u1 = a12 + (a11 - a12) * q
        u2 = a22 + (a21 - a22) * q
        h = max(u1, u2)
        if h < best_h:
            best_h = h
            best_q = q

    q1 = best_q
    q2 = 1 - q1
    v_from_q = best_h

    print(f"\nОптимум для B: q1 = {_fmt_number(q1)}, q2 = {_fmt_number(q2)}")
    print(f"Мінімізований виграш A: v = {_fmt_number(v_from_q)}")

    p = np.array([p1, p2])
    q = np.array([q1, q2])
    v_check = p @ matrix @ q
    v = v_check

    print(f"\nПеревірка: p^T * A * q = {_fmt_number(v_check)}")
    print(f"Ціна гри: v = {_fmt_number(v)}")

    if plotter is not None:
        plotter(matrix, p1, q1, v)

    return p, q, v


def solve_2xn_graphical(matrix, plotter=None):
    print("КРОК 3: Графічне розв'язання гри 2 x n")

    m, n = matrix.shape
    if m != 2:
        print("Помилка: цей метод працює лише для матриць 2 x n")
        return None

    a1 = matrix[0, :]
    a2 = matrix[1, :]

    print("\nЛінії виграшу A від p = P(A1):")
    for j in range(n):
        slope = a1[j] - a2[j]
        intercept = a2[j]
        print(f"f{j+1}(p) = {intercept:.4f} + ({slope:.4f})*p")
    print("A максимізує нижню огинаючу: g(p) = min_j f_j(p)")

    p_candidates = [0.0, 1.0]
    for j in range(n):
        for k in range(j + 1, n):
            slope_j = a1[j] - a2[j]
            slope_k = a1[k] - a2[k]
            denom = slope_j - slope_k
            if abs(denom) < 1e-12:
                continue
            p_intersection = (a2[k] - a2[j]) / denom
            if 0.0 <= p_intersection <= 1.0:
                p_candidates.append(float(p_intersection))

    best_p = None
    best_g = -np.inf
    for p in p_candidates:
        values = a2 + (a1 - a2) * p
        g = np.min(values)
        if g > best_g:
            best_g = g
            best_p = p

    if best_p is None:
        print("Помилка: не вдалося визначити оптимальне p для графічного методу 2 x n")
        return None

    p = np.array([best_p, 1 - best_p])
    v_from_graph = best_g

    b_solution = solve_player_B_lp(matrix)
    if b_solution is None:
        print("Помилка: не вдалося знайти оптимальну стратегію B")
        return None
    q, v_b = b_solution

    v_check = p @ matrix @ q
    v = v_check

    print(f"\nОптимальна стратегія A: p1 = {_fmt_number(p[0])}, p2 = {_fmt_number(p[1])}")
    print(f"Оцінка з графіка: v = {_fmt_number(v_from_graph)}")
    print(f"Оцінка з LP для B: v = {_fmt_number(v_b)}")
    print(f"Перевірка p^T*A*q: v = {_fmt_number(v_check)}")

    if plotter is not None:
        plotter(matrix, p[0], v)
    return p, q, v


def solve_mx2_graphical(matrix, plotter=None):
    print("КРОК 3: Графічне розв'язання гри m x 2")

    m, n = matrix.shape
    if n != 2:
        print("Помилка: цей метод працює лише для матриць m x 2")
        return None

    b1 = matrix[:, 0]
    b2 = matrix[:, 1]

    print("\nЛінії виграшу A від q = P(B1):")
    for i in range(m):
        slope = b1[i] - b2[i]
        intercept = b2[i]
        print(f"u{i+1}(q) = {intercept:.4f} + ({slope:.4f})*q")
    print("B мінімізує верхню огинаючу: h(q) = max_i u_i(q)")

    q_candidates = [0.0, 1.0]
    for i in range(m):
        for k in range(i + 1, m):
            slope_i = b1[i] - b2[i]
            slope_k = b1[k] - b2[k]
            denom = slope_i - slope_k
            if abs(denom) < 1e-12:
                continue
            q_intersection = (b2[k] - b2[i]) / denom
            if 0.0 <= q_intersection <= 1.0:
                q_candidates.append(float(q_intersection))

    best_q = None
    best_h = np.inf
    for q in q_candidates:
        values = b2 + (b1 - b2) * q
        h = np.max(values)
        if h < best_h:
            best_h = h
            best_q = q

    q = np.array([best_q, 1 - best_q])
    v_from_graph = best_h

    a_solution = solve_player_A_lp(matrix)
    if a_solution is None:
        print("Помилка: не вдалося знайти оптимальну стратегію A")
        return None
    p, v_a = a_solution

    v_check = p @ matrix @ q
    v = v_check

    print(f"\nОптимальна стратегія B: q1 = {_fmt_number(q[0])}, q2 = {_fmt_number(q[1])}")
    print(f"Оцінка з графіка: v = {_fmt_number(v_from_graph)}")
    print(f"Оцінка з LP для A: v = {_fmt_number(v_a)}")
    print(f"Перевірка p^T*A*q: v = {_fmt_number(v_check)}")

    if plotter is not None:
        plotter(matrix, q[0], v)
    return p, q, v
