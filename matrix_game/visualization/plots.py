import numpy as np


def _get_pyplot(error_message):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print(error_message)
        print("Встановіть пакет командою: pip install matplotlib")
        return None
    return plt


def plot_2x2_graphical(matrix, p1, q1, v):
    plt = _get_pyplot("\nУвага: matplotlib не встановлено, графіки не побудовано.")
    if plt is None:
        return

    a11, a12 = matrix[0]
    a21, a22 = matrix[1]

    p_grid = np.linspace(0, 1, 300)
    f1 = a21 + (a11 - a21) * p_grid
    f2 = a22 + (a12 - a22) * p_grid
    lower_envelope = np.minimum(f1, f2)

    q_grid = np.linspace(0, 1, 300)
    u1 = a12 + (a11 - a12) * q_grid
    u2 = a22 + (a21 - a22) * q_grid
    upper_envelope = np.maximum(u1, u2)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)

    axes[0].plot(p_grid, f1, label="f1(p): B1", color="tab:blue", linewidth=2)
    axes[0].plot(p_grid, f2, label="f2(p): B2", color="tab:orange", linewidth=2)
    axes[0].plot(
        p_grid,
        lower_envelope,
        label="min(f1, f2)",
        color="k",
        linestyle=(0, (1, 1)),
        linewidth=2,
    )
    axes[0].scatter([p1], [v], color="red", s=60, zorder=5, label=f"Оптимум A (p*={p1:.3f}, v={v:.3f})")
    axes[0].set_xlabel("p = P(A1)")
    axes[0].set_ylabel("Очікуваний виграш A")
    axes[0].set_xlim(0, 1)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(q_grid, u1, label="u1(q): A1", color="tab:purple", linewidth=2)
    axes[1].plot(q_grid, u2, label="u2(q): A2", color="tab:brown", linewidth=2)
    axes[1].plot(
        q_grid,
        upper_envelope,
        label="max(u1, u2)",
        color="k",
        linestyle=(0, (1, 1)),
        linewidth=2,
    )
    axes[1].scatter([q1], [v], color="red", s=60, zorder=5, label=f"Оптимум B (q*={q1:.3f}, v={v:.3f})")
    axes[1].set_xlabel("q = P(B1)")
    axes[1].set_ylabel("Очікуваний виграш B")
    axes[1].set_xlim(0, 1)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    plt.show()


def plot_2xn_graphical(matrix, p_opt, v_opt):
    plt = _get_pyplot("\nУвага: matplotlib не встановлено, графік для 2 x n не побудовано.")
    if plt is None:
        return

    _, n = matrix.shape
    p_grid = np.linspace(0, 1, 400)
    line_values = []
    for j in range(n):
        values = matrix[1, j] + (matrix[0, j] - matrix[1, j]) * p_grid
        line_values.append(values)
    lines = np.array(line_values)
    lower_envelope = np.min(lines, axis=0)

    plt.figure(figsize=(9, 6))
    for j in range(n):
        plt.plot(p_grid, lines[j], linewidth=1.8, label=f"f{j+1}(p), B{j+1}")
    plt.plot(p_grid, lower_envelope, label="min_j f_j(p)", color="k", linestyle=(0, (1, 1)), linewidth=2.2)
    plt.scatter([p_opt], [v_opt], color="red", s=70, zorder=5, label=f"Оптимум (p*={p_opt:.3f}, v={v_opt:.3f})")
    plt.xlabel("p = P(A1)")
    plt.ylabel("Очікуваний виграш A")
    plt.xlim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend(loc="best")
    plt.show()


def plot_mx2_graphical(matrix, q_opt, v_opt):
    plt = _get_pyplot("\nУвага: matplotlib не встановлено, графік для m x 2 не побудовано.")
    if plt is None:
        return

    m, _ = matrix.shape
    q_grid = np.linspace(0, 1, 400)
    line_values = []
    for i in range(m):
        values = matrix[i, 1] + (matrix[i, 0] - matrix[i, 1]) * q_grid
        line_values.append(values)
    lines = np.array(line_values)
    upper_envelope = np.max(lines, axis=0)

    plt.figure(figsize=(9, 6))
    for i in range(m):
        plt.plot(q_grid, lines[i], linewidth=1.8, label=f"u{i+1}(q), A{i+1}")
    plt.plot(q_grid, upper_envelope, label="max_i u_i(q)", color="k", linestyle=(0, (1, 1)), linewidth=2.2)
    plt.scatter([q_opt], [v_opt], color="red", s=70, zorder=5, label=f"Оптимум (q*={q_opt:.3f}, v={v_opt:.3f})")

    plt.xlabel("q = P(B1)")
    plt.ylabel("Очікуваний виграш B")
    plt.xlim(0, 1)
    plt.grid(True, alpha=0.3)
    plt.legend(loc="best")
    plt.show()
