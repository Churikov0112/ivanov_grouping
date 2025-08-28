import tkinter as tk
from tkinter import messagebox, ttk
from models import User, GroupMatcher
from utils import export_groups_to_csv, visualize_groups
import random

class MatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Формирование групп")
        self.users = []
        self.user_id_counter = 0

        self.create_form()
        self.create_buttons()
        self.create_output()

    def create_form(self):
        self.form_frame = tk.LabelFrame(self.root, text="Добавить нового пользователя", padx=10, pady=10)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.entries = {}

        fields = [
            ("Политические взгляды (0–1):", "politics"),
            ("Любовь к приключениям (0–1):", "adventure"),
            ("Доход (0–1):", "income"),
            ("Толерантность к мату (0–1):", "tolerance"),
            ("Желаемый размер группы (мин 2):", "group_size"),
        ]

        for i, (label_text, key) in enumerate(fields):
            label = tk.Label(self.form_frame, text=label_text)
            label.grid(row=i, column=0, sticky="e", padx=(0, 5), pady=2)
            entry = tk.Entry(self.form_frame, width=10)
            entry.grid(row=i, column=1, pady=2, sticky="w")
            self.entries[key] = entry

        options = ["politics", "adventure", "income", "tolerance"]
        trait_labels = {
            "politics": "Политические взгляды",
            "adventure": "Любовь к приключениям",
            "income": "Доход",
            "tolerance": "Толерантность к мату"
        }

        tk.Label(self.form_frame, text="Важный признак:").grid(row=5, column=0, sticky="e", padx=(0, 5), pady=(10, 2))
        self.important_var = tk.StringVar()
        imp_box = ttk.Combobox(self.form_frame, textvariable=self.important_var, values=[trait_labels[o] for o in options], state="readonly")
        imp_box.grid(row=5, column=1, sticky="w", pady=(10, 2))

        tk.Label(self.form_frame, text="Менее важный признак:").grid(row=6, column=0, sticky="e", padx=(0, 5), pady=2)
        self.flexible_var = tk.StringVar()
        flex_box = ttk.Combobox(self.form_frame, textvariable=self.flexible_var, values=[trait_labels[o] for o in options], state="readonly")
        flex_box.grid(row=6, column=1, sticky="w", pady=2)

        self.trait_label_map = {v: k for k, v in trait_labels.items()}

        self.add_btn = tk.Button(self.form_frame, text="Добавить пользователя", command=self.add_user)
        self.add_btn.grid(row=7, column=0, columnspan=2, pady=(10, 2))

        self.random_btn = tk.Button(self.form_frame, text="Случайный пользователь", command=self.fill_random_user)
        self.random_btn.grid(row=8, column=0, columnspan=2, pady=(5, 0))

    def create_buttons(self):
        self.control_frame = tk.Frame(self.root)
        self.control_frame.grid(row=1, column=0, pady=5)

        tk.Button(self.control_frame, text="Сформировать группы", command=self.make_groups).grid(row=0, column=0, padx=5)
        tk.Button(self.control_frame, text="Экспорт в CSV", command=self.export_csv).grid(row=0, column=1, padx=5)
        tk.Button(self.control_frame, text="Визуализировать", command=self.visualize).grid(row=0, column=2, padx=5)

    def create_output(self):
        self.output_frame = tk.LabelFrame(self.root, text="Результаты", padx=10, pady=10)
        self.output_frame.grid(row=2, column=0, padx=10, pady=10)

        self.output_text = tk.Text(self.output_frame, height=15, width=60)
        self.output_text.pack()

    def add_user(self):
        try:
            for key, entry in self.entries.items():
                if not entry.get().strip():
                    raise ValueError(f"Поле '{key}' не заполнено.")

            if not self.important_var.get() or not self.flexible_var.get():
                raise ValueError("Выберите важный и гибкий признак.")

            important = self.trait_label_map.get(self.important_var.get())
            flexible = self.trait_label_map.get(self.flexible_var.get())

            if important == flexible:
                raise ValueError("Важный и гибкий признаки не должны совпадать.")

            politics = float(self.entries["politics"].get())
            adventure = float(self.entries["adventure"].get())
            income = float(self.entries["income"].get())
            tolerance = float(self.entries["tolerance"].get())
            group_size = int(self.entries["group_size"].get())

            for val, name in zip([politics, adventure, income, tolerance],
                                 ["Политика", "Приключения", "Доход", "Толерантность"]):
                if not 0 <= val <= 1:
                    raise ValueError(f"{name} должно быть от 0 до 1.")

            user = User(
                self.user_id_counter, politics, adventure, income, tolerance,
                group_size, important, flexible
            )

            self.users.append(user)
            self.user_id_counter += 1
            self.output_text.insert(tk.END, f"Добавлен {user}\n")

            for entry in self.entries.values():
                entry.delete(0, tk.END)
            self.important_var.set('')
            self.flexible_var.set('')

        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", str(ve))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Непредвиденная ошибка: {e}")

    def make_groups(self):
        matcher = GroupMatcher(self.users)
        self.groups = matcher.match()
        self.output_text.insert(tk.END, "\nСформированы группы:\n")
        for i, group in enumerate(self.groups):
            members = ", ".join(str(u) for u in group)
            self.output_text.insert(tk.END, f"Группа {i + 1}: {members}\n")

    def export_csv(self):
        if hasattr(self, "groups"):
            export_groups_to_csv(self.groups)
            messagebox.showinfo("Успех", "Группы сохранены в groups.csv")

    def visualize(self):
        if hasattr(self, "groups"):
            visualize_groups(self.groups)

    def fill_random_user(self):
        self.entries["politics"].delete(0, tk.END)
        self.entries["politics"].insert(0, f"{round(random.uniform(0, 1), 2)}")

        self.entries["adventure"].delete(0, tk.END)
        self.entries["adventure"].insert(0, f"{round(random.uniform(0, 1), 2)}")

        self.entries["income"].delete(0, tk.END)
        self.entries["income"].insert(0, f"{round(random.uniform(0, 1), 2)}")

        self.entries["tolerance"].delete(0, tk.END)
        self.entries["tolerance"].insert(0, f"{round(random.uniform(0, 1), 2)}")

        self.entries["group_size"].delete(0, tk.END)
        self.entries["group_size"].insert(0, str(random.randint(2, 5)))

        options = ["politics", "adventure", "income", "tolerance"]
        trait_labels = {
            "politics": "Политические взгляды",
            "adventure": "Любовь к приключениям",
            "income": "Доход",
            "tolerance": "Толерантность к мату"
        }

        important, flexible = random.sample(options, 2)
        self.important_var.set(trait_labels[important])
        self.flexible_var.set(trait_labels[flexible])
