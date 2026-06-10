import os
import traceback

import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from game import MatrixGame


APP_TITLE = "Matrix Game Solver"
APP_BG = "#ffffff"
CARD_BORDER = "#d9e2ec"
TEXT_BG = "#ffffff"
TEXT_FG = "#1a2d3f"
FIELD_BG = "#ffffff"
FIELD_BORDER = "#cfd9e3"


class MatrixInputGrid(ttk.Frame):
    def __init__(self, master, rows=3, cols=3):
        super().__init__(master)
        self.rows_var = tk.IntVar(value=rows)
        self.cols_var = tk.IntVar(value=cols)
        self.entries = []

        controls = ttk.Frame(self, style="Card.TFrame")
        controls.pack(fill="x", pady=(0, 8))

        ttk.Label(controls, text="Рядки (A):").pack(side="left")
        ttk.Spinbox(controls, from_=1, to=20, width=5, textvariable=self.rows_var).pack(side="left", padx=(6, 12))

        ttk.Label(controls, text="Стовпці (B):").pack(side="left")
        ttk.Spinbox(controls, from_=1, to=20, width=5, textvariable=self.cols_var).pack(side="left", padx=(6, 12))

        ttk.Button(controls, text="Побудувати сітку", command=self.build_grid).pack(side="left")
        ttk.Button(controls, text="Заповнити нулями", command=self.fill_zeros).pack(side="left", padx=(8, 0))

        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=APP_BG)
        self.scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas, style="Card.TFrame")

        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.build_grid()

    def build_grid(self):
        for widget in self.inner.winfo_children():
            widget.destroy()

        r = max(1, int(self.rows_var.get()))
        c = max(1, int(self.cols_var.get()))

        self.entries = []

        ttk.Label(self.inner, text="").grid(row=0, column=0, padx=4, pady=4)
        for j in range(c):
            ttk.Label(self.inner, text=f"B{j+1}").grid(row=0, column=j + 1, padx=4, pady=4)

        for i in range(r):
            ttk.Label(self.inner, text=f"A{i+1}").grid(row=i + 1, column=0, padx=4, pady=4)
            row_entries = []
            for j in range(c):
                entry = ttk.Entry(self.inner, width=8)
                entry.insert(0, "0")
                entry.grid(row=i + 1, column=j + 1, padx=3, pady=3)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def fill_zeros(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(0, "0")

    def get_matrix(self):
        matrix = []
        for i, row in enumerate(self.entries, start=1):
            values = []
            for j, entry in enumerate(row, start=1):
                raw = entry.get().strip().replace(",", ".")
                if raw == "":
                    raise ValueError(f"Порожнє значення в A{i}, B{j}")
                try:
                    values.append(float(raw))
                except ValueError as err:
                    raise ValueError(f"Некоректне число в A{i}, B{j}: '{raw}'") from err
            matrix.append(values)
        return matrix


class MatrixGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.configure(bg=APP_BG)

        self.input_mode = tk.StringVar(value="keyboard")
        self.file_path_var = tk.StringVar(value="")
        self.show_full_log_var = tk.BooleanVar(value=False)
        self.show_plots_var = tk.BooleanVar(value=True)
        self.last_summary = ""
        self.last_log = ""

        self._setup_style()
        self._build_ui()
        self._set_initial_geometry()

    def _set_initial_geometry(self):
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = min(1120, max(960, screen_width - 80))
        height = min(760, max(680, screen_height - 120))

        self.minsize(min(980, max(960, screen_width - 120)), min(680, max(640, screen_height - 160)))

        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Main.TFrame", background=APP_BG)
        style.configure("Card.TFrame", background=APP_BG, relief="flat")
        style.configure("Title.TLabel", background=APP_BG, foreground="#12304a", font=("Segoe UI Semibold", 19))
        style.configure("Sub.TLabel", background=APP_BG, foreground="#4a6072", font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#1f3850", font=("Segoe UI Semibold", 11))

        style.configure(
            "Accent.TButton",
            font=("Segoe UI Semibold", 10),
            padding=(12, 7),
            foreground="#ffffff",
            background="#1f7ae0",
            borderwidth=0,
        )
        style.map("Accent.TButton", background=[("active", "#1563ba")])

        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 6))
        style.configure("TRadiobutton", background=APP_BG, font=("Segoe UI", 10))
        style.configure("TCheckbutton", background=APP_BG, font=("Segoe UI", 10))
        style.configure("TLabel", background=APP_BG)
        style.configure("TFrame", background=APP_BG)
        style.configure(
            "TEntry",
            fieldbackground=FIELD_BG,
            background=FIELD_BG,
            foreground=TEXT_FG,
            bordercolor=FIELD_BORDER,
            lightcolor=FIELD_BORDER,
            darkcolor=FIELD_BORDER,
            padding=4,
        )
        style.configure(
            "TSpinbox",
            fieldbackground=FIELD_BG,
            background=FIELD_BG,
            foreground=TEXT_FG,
            bordercolor=FIELD_BORDER,
            lightcolor=FIELD_BORDER,
            darkcolor=FIELD_BORDER,
            padding=4,
        )

    def _build_ui(self):
        root = ttk.Frame(self, style="Main.TFrame", padding=16)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text="Розв'язання матричних ігор", style="Title.TLabel").pack(anchor="w")

        top = ttk.Frame(root, style="Main.TFrame")
        top.pack(fill="x")

        self.input_card = tk.Frame(top, bg=APP_BG, highlightthickness=1, highlightbackground=CARD_BORDER, highlightcolor=CARD_BORDER, bd=0)
        self.input_card.pack(side="left", fill="both", expand=True)

        self.options_card = tk.Frame(top, bg=APP_BG, highlightthickness=1, highlightbackground=CARD_BORDER, highlightcolor=CARD_BORDER, bd=0)
        self.options_card.pack(side="left", fill="y", padx=(12, 0))

        input_body = ttk.Frame(self.input_card, style="Card.TFrame", padding=12)
        input_body.pack(fill="both", expand=True)

        ttk.Label(input_body, text="Введення матриці", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        mode_row = ttk.Frame(input_body, style="Card.TFrame")
        mode_row.pack(fill="x", pady=(0, 8))

        ttk.Radiobutton(
            mode_row,
            text="З клавіатури",
            value="keyboard",
            variable=self.input_mode,
            command=self._toggle_mode,
        ).pack(side="left")
        ttk.Radiobutton(
            mode_row,
            text="З файлу",
            value="file",
            variable=self.input_mode,
            command=self._toggle_mode,
        ).pack(side="left", padx=(12, 0))

        self.keyboard_frame = ttk.Frame(input_body, style="Card.TFrame")
        self.keyboard_frame.pack(fill="both", expand=True)
        self.grid_input = MatrixInputGrid(self.keyboard_frame, rows=3, cols=3)
        self.grid_input.pack(fill="both", expand=True)

        self.file_frame = ttk.Frame(input_body, style="Card.TFrame")
        ttk.Label(self.file_frame, text="Оберіть текстовий файл з матрицею:", style="CardTitle.TLabel").pack(anchor="w")
        file_row = ttk.Frame(self.file_frame, style="Card.TFrame")
        file_row.pack(fill="x", pady=(8, 0))
        ttk.Entry(file_row, textvariable=self.file_path_var).pack(side="left", fill="x", expand=True)
        ttk.Button(file_row, text="Огляд...", command=self._choose_file).pack(side="left", padx=(8, 0))

        ttk.Label(
            self.file_frame,
            text="Формат: числа через пробіл, один рядок матриці на рядок.",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(8, 0))

        options_body = ttk.Frame(self.options_card, style="Card.TFrame", padding=12)
        options_body.pack(fill="both", expand=True)

        ttk.Label(options_body, text="Параметри", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Checkbutton(
            options_body,
            text="Показувати графіки (де доступно)",
            variable=self.show_plots_var,
        ).pack(anchor="w")
        ttk.Checkbutton(
            options_body,
            text="Показувати детальний лог",
            variable=self.show_full_log_var,
            command=self._render_results,
        ).pack(anchor="w", pady=(6, 12))

        ttk.Button(
            options_body,
            text="Розв'язати гру",
            style="Accent.TButton",
            command=self._solve_matrix_game,
        ).pack(fill="x")

        ttk.Button(options_body, text="Зберегти лог у файл", command=self._save_log_to_file).pack(fill="x", pady=(8, 0))
        ttk.Button(options_body, text="Очистити", command=self._clear_results).pack(fill="x", pady=(8, 0))

        bottom = ttk.Frame(root, style="Main.TFrame")
        bottom.pack(fill="both", expand=True, pady=(12, 0))

        self.result_card = tk.Frame(bottom, bg=APP_BG, highlightthickness=1, highlightbackground=CARD_BORDER, highlightcolor=CARD_BORDER, bd=0)
        self.result_card.pack(fill="both", expand=True)

        result_body = ttk.Frame(self.result_card, style="Card.TFrame", padding=12)
        result_body.pack(fill="both", expand=True)

        ttk.Label(result_body, text="Результати", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        output_row = ttk.Frame(result_body, style="Card.TFrame")
        output_row.pack(fill="both", expand=True)

        self.output_text = tk.Text(
            output_row,
            wrap="word",
            font=("Consolas", 10),
            bg=TEXT_BG,
            fg=TEXT_FG,
            relief="flat",
            padx=10,
            pady=8,
        )
        self.output_scroll = ttk.Scrollbar(output_row, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=self.output_scroll.set)

        self.output_text.pack(side="left", fill="both", expand=True)
        self.output_scroll.pack(side="right", fill="y")

        self._toggle_mode()
        self._set_output("Тут з'явиться короткий підсумок: ціна гри та оптимальні стратегії.")

    def _toggle_mode(self):
        mode = self.input_mode.get()
        if mode == "keyboard":
            self.file_frame.pack_forget()
            self.keyboard_frame.pack(fill="both", expand=True)
        else:
            self.keyboard_frame.pack_forget()
            self.file_frame.pack(fill="both", expand=True)

    def _choose_file(self):
        path = filedialog.askopenfilename(
            title="Оберіть файл матриці",
            filetypes=[("Text files", "*.txt *.dat *.csv"), ("All files", "*.*")],
        )
        if path:
            self.file_path_var.set(path)

    def _parse_matrix_from_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        matrix = []
        expected_len = None
        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue

            row = [float(x.replace(",", ".")) for x in stripped.split()]
            if expected_len is None:
                expected_len = len(row)
            elif len(row) != expected_len:
                raise ValueError(f"Рядок {line_num}: різна кількість елементів")
            matrix.append(row)

        if not matrix:
            raise ValueError("Файл порожній або не містить коректної матриці")

        return matrix

    def _collect_matrix(self):
        if self.input_mode.get() == "keyboard":
            return self.grid_input.get_matrix()

        path = self.file_path_var.get().strip()
        if not path:
            raise ValueError("Оберіть файл")
        if not os.path.exists(path):
            raise ValueError("Файл не знайдено")
        return self._parse_matrix_from_file(path)

    @staticmethod
    def _format_strategies(label_prefix, probs):
        rows = []
        for idx, prob in enumerate(probs, start=1):
            if prob > 1e-8:
                value = np.format_float_positional(float(prob), trim="-")
                percent = np.format_float_positional(float(prob * 100), trim="-")
                rows.append(f"  {label_prefix}{idx}: {value} ({percent}%)")
        return "\n".join(rows) if rows else "  Немає значущих ймовірностей"

    def _compute_solution(self, matrix):
        game = MatrixGame(matrix)
        return game.solve_to_data(matrix, show_plots=self.show_plots_var.get())

    def _format_strategy_vector(self, probs):
        values = [np.format_float_positional(float(prob), trim="-") for prob in np.asarray(probs, dtype=float)]
        return "(" + ", ".join(values) + ")"

    def _set_output(self, text):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.configure(state="disabled")

    def _render_results(self):
        summary = self.last_summary if self.last_summary else ""
        if self.show_full_log_var.get():
            log = self.last_log if self.last_log else "Лог порожній."
            combined = summary + "\n\n" + "ДЕТАЛЬНИЙ ЛОГ:\n" + log
        else:
            combined = summary + "\n\n(Детальний лог приховано. Увімкніть 'Показувати детальний лог' для повного виводу.)"

        self._set_output(combined)

    def _save_log_to_file(self):
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Збереження логу", "Немає тексту для збереження.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Зберегти лог у файл",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="matrix_game_log.txt",
        )
        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content + "\n")

        messagebox.showinfo("Збереження логу", f"Лог збережено у файл:\n{file_path}")

    def _solve_matrix_game(self):
        try:
            matrix = self._collect_matrix()
            data = self._compute_solution(matrix)

            if data["is_saddle"]:
                p = data["p"]
                q = data["q"]
                summary = [
                    "Статус: знайдено сідлову точку (чисті стратегії).",
                    f"Ціна гри: v = {np.format_float_positional(float(data['value']), trim='-')}",
                    "Програма заблокувала подальший перехід до симплекс-методу як обчислювально надлишковий.",
                    f"Вектор оптимальних стратегій X^* = {self._format_strategy_vector(p)}, Y^* = {self._format_strategy_vector(q)}",
                    f"Розмір матриці: {data['original_shape'][0]} x {data['original_shape'][1]}",
                ]
            else:
                p = data["p"]
                q = data["q"]
                expected = float(p @ data["reduced_matrix"] @ q)
                summary = [
                    "Статус: знайдено розв'язок у змішаних стратегіях.",
                    f"Ціна гри: v = {np.format_float_positional(float(data['value']), trim='-')}",
                    f"Перевірка p^T A q: {np.format_float_positional(float(expected), trim='-')}",
                    f"Вихідна матриця: {data['original_shape'][0]} x {data['original_shape'][1]}",
                    f"Після редукції: {data['reduced_shape'][0]} x {data['reduced_shape'][1]}",
                    "",
                    "Оптимальна стратегія A:",
                    self._format_strategies("A", p),
                    "",
                    "Оптимальна стратегія B:",
                    self._format_strategies("B", q),
                ]

            self.last_summary = "\n".join(summary)
            self.last_log = data["log"] if data["log"].strip() else "Лог порожній."
            self._render_results()

        except ValueError as err:
            details = traceback.format_exc()
            self.last_summary = f"Помилка введення: {err}"
            self.last_log = details
            self._render_results()
            messagebox.showerror("Помилка введення", str(err))

        except RuntimeError as err:
            details = traceback.format_exc()
            self.last_summary = f"Помилка обчислення: {err}"
            self.last_log = details
            self._render_results()
            messagebox.showerror("Помилка обчислення", str(err))

        except Exception as err:
            details = traceback.format_exc()
            self.last_summary = f"Неочікувана помилка: {err}"
            self.last_log = details
            self._render_results()
            messagebox.showerror("Неочікувана помилка", str(err))

    def _clear_results(self):
        self.last_summary = ""
        self.last_log = ""
        self._set_output("")


def main():
    app = MatrixGameGUI()
    app.mainloop()
