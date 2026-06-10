from __future__ import annotations

from typing import Callable, TextIO

import numpy as np


def format_matrix_text(
    matrix,
    title: str = "Матриця",
    number_formatter: Callable[[float], str] | None = None,
    output: TextIO | None = None,
):
    arr = np.array(matrix, dtype=float)
    rows, cols = arr.shape
    formatter = number_formatter or (lambda value: np.format_float_positional(float(value), trim="-"))
    max_len = max((len(formatter(val)) for val in arr.flat), default=0)
    col_width = max(8, max_len + 2)

    lines = [f"\n{title}:"]
    header = " " * 10 + "".join([f"{'B'+str(j+1):>{col_width}}" for j in range(cols)])
    lines.append(header)
    lines.append("-" * (10 + col_width * cols))
    for i, row in enumerate(arr):
        row_label = f"A{i+1}:".ljust(10)
        row_vals = "".join([f"{formatter(val):>{col_width}}" for val in row])
        lines.append(f"{row_label}{row_vals}")
    lines.append("-" * (10 + col_width * cols))

    text = "\n".join(lines)
    if output is not None:
        output.write(text + "\n")
    return text
