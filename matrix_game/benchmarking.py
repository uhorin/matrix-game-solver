import time
import numpy as np
from game import MatrixGame


def plot_benchmark_results(benchmark_results):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Попередження: matplotlib не встановлено, графік не побудовано.")
        return

    if not benchmark_results:
        print("Немає даних для побудови графіка.")
        return

    sizes = [item[0] for item in benchmark_results]
    times = [item[1] for item in benchmark_results]

    plt.figure(figsize=(7, 4.5))
    plt.plot(sizes, times, marker='o', linestyle='-', color='#1f7ae0', linewidth=2, label='Емпіричний час')
    plt.xlabel("Розмірність квадратної платіжної матриці (m = n)", fontsize=10)
    plt.ylabel("Середній час виконання процесу, сек", fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("time_complexity_graph.png", dpi=300)
    plt.show()

def run_performance_benchmark():
    print("ТЕСТУВАННЯ ОБЧИСЛЮВАЛЬНОЇ СКЛАДНОСТІ МАТРИЧНИХ ІГОР")
    print(f"{'Розмірність (m x n)':<25} | {'Серія (ітерацій)':<18} | {'Сер. час (сек)':<15}")
    print("-" * 80)

    test_sizes = [10, 20, 50, 100, 150, 200, 300, 500]

    iterations_map = {
        10: 50,
        20: 50,
        50: 20,
        100: 10,
        150: 5,
        200: 5,
        300: 3,
        500: 1
    }

    benchmark_results = []

    for size in test_sizes:
        iterations = iterations_map[size]
        execution_times = []
        skipped_iterations = 0

        for _ in range(iterations):
            low, high = -100, 100
            raw_matrix = np.random.uniform(low, high, size=(size, size))

            game_instance = MatrixGame(raw_matrix)

            game_instance.print_matrix = lambda *args, **kwargs: None

            start_time = time.perf_counter()

            try:
                import io
                from contextlib import redirect_stdout
                f = io.StringIO()
                with redirect_stdout(f):
                    game_instance.solve()
            except Exception as e:
                skipped_iterations += 1
                continue

            end_time = time.perf_counter()
            diff = end_time - start_time
            execution_times.append(diff)

        if execution_times:
            avg_time = np.mean(execution_times)
            size_label = f"{size} x {size}"
            print(f"{size_label:<25} | {iterations:<18} | {avg_time:.6f} | skipped: {skipped_iterations}")
            benchmark_results.append((size, avg_time))
        elif skipped_iterations:
            size_label = f"{size} x {size}"
            print(f"{size_label:<25} | {iterations:<18} | n/a      | skipped: {skipped_iterations}")

    print("Тестування успішно завершено.")

    plot_benchmark_results(benchmark_results)

if __name__ == "__main__":
    run_performance_benchmark()

