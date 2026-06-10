import numpy as np


def _format_vector(values):
    return "  ".join([f"{value:.2f}" for value in values])


def simplify_matrix(matrix, print_matrix_func=None):
    print("КРОК 2: Вилучення домінованих стратегій")

    working_matrix = np.array(matrix, dtype=float, copy=True)
    total_iterations = 0
    changed = True

    while changed:
        changed = False

        rows_active = np.ones(working_matrix.shape[0], dtype=bool)
        for i in range(working_matrix.shape[0]):
            if not rows_active[i]:
                continue
            for j in range(working_matrix.shape[0]):
                if i == j or not rows_active[j]:
                    continue
                if np.all(working_matrix[i] <= working_matrix[j]) and np.any(working_matrix[i] < working_matrix[j]):
                    total_iterations += 1
                    row_i_str = "  ".join([f"{v:.2f}" for v in working_matrix[i]])
                    row_j_str = "  ".join([f"{v:.2f}" for v in working_matrix[j]])
                    print(f"\n  Ітерація {total_iterations}: стратегія A{i+1} домінується стратегією A{j+1}")
                    print(f"    A{i+1}: [{row_i_str}] - видаляється")
                    print(f"    A{j+1}: [{row_j_str}]")
                    rows_active[i] = False
                    changed = True
                    break

        if changed:
            working_matrix = working_matrix[rows_active, :]
            continue

        cols_active = np.ones(working_matrix.shape[1], dtype=bool)
        for i in range(working_matrix.shape[1]):
            for j in range(working_matrix.shape[1]):
                if i == j or not cols_active[i] or not cols_active[j]:
                    continue

                col_i = working_matrix[:, i]
                col_j = working_matrix[:, j]

                if np.all(col_i >= col_j) and np.any(col_i > col_j):
                    total_iterations += 1
                    col_i_str = "  ".join([f"{v:.2f}" for v in col_i])
                    col_j_str = "  ".join([f"{v:.2f}" for v in col_j])
                    print(f"\n  Ітерація {total_iterations}: стратегія B{i+1} домінується стратегією B{j+1}")
                    print(f"    B{i+1}: [{col_i_str}] - видаляється")
                    print(f"    B{j+1}: [{col_j_str}]")
                    cols_active[i] = False
                    changed = True
                    break

        if changed:
            working_matrix = working_matrix[:, cols_active]

    if total_iterations == 0:
        print("\n  Домінованих стратегій не знайдено. Матриця залишається без змін.")
        return working_matrix, False

    print(f"\n  Загалом виконано ітерацій редукції: {total_iterations}")
    if print_matrix_func is not None:
        import sys

        print_matrix_func(
            working_matrix,
            "Матриця після вилучення домінованих стратегій",
            output=sys.stdout,
        )
    return working_matrix, True
