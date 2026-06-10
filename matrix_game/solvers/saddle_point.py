import numpy as np

def check_saddle_point(matrix):
    print("КРОК 1: Пошук сідлової точки")

    row_mins = np.min(matrix, axis=1)
    row_mins_str = "  ".join([f"{v:.2f}" for v in row_mins])
    print(f"\nМінімуми у рядках: [{row_mins_str}]")

    col_maxs = np.max(matrix, axis=0)
    col_maxs_str = "  ".join([f"{v:.2f}" for v in col_maxs])
    print(f"Максимуми у стовпцях: [{col_maxs_str}]")

    alpha = float(np.max(row_mins))
    max_row = int(np.argmax(row_mins))
    print(f"\nНижня ціна гри  α = max{{мінімуми рядків}} = {alpha:.4f}")
    print(f"  Досягається на стратегії A{max_row + 1}")

    beta = float(np.min(col_maxs))
    min_col = int(np.argmin(col_maxs))
    print(f"Верхня ціна гри  β = min{{максимуми стовпців}} = {beta:.4f}")
    print(f"  Досягається на стратегії B{min_col + 1}")

    if np.isclose(alpha, beta):
        print(f"\nЗНАЙДЕНО СІДЛОВУ ТОЧКУ!  α = β = {alpha:.4f}")
        print(f"  Ціна гри v = {alpha:.4f}")
        print(f"  Оптимальна стратегія гравця A: чиста стратегія A{max_row + 1}")
        print(f"  Оптимальна стратегія гравця B: чиста стратегія B{min_col + 1}")
        print("\n  Ітераційні методи (ЗЛП) не потрібні: розв'язок знайдено аналітично.")
        return True, alpha, max_row, min_col, alpha, beta

    print(f"\nСідлової точки немає (α = {alpha:.4f} ≠ β = {beta:.4f})")
    print("  Необхідно використати змішані стратегії.")
    return False, None, None, None, alpha, beta
