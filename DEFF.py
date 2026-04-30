import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

def create_expense_tracker():
    root = tk.Tk()
    root.title("Expense Tracker")

    expenses = []

    try:
        with open("expenses.json", "r", encoding="utf-8") as f:
            expenses.extend(json.load(f))
    except FileNotFoundError:
        pass

    tk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
    category_var = tk.StringVar()
    category_combo = ttk.Combobox(
        root,
        textvariable=category_var,
        values=["Еда", "Транспорт", "Развлечения", "Жильё", "Другое"]
    )
    category_combo.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5)
    date_entry = tk.Entry(root)
    date_entry.grid(row=2, column=1, padx=5, pady=5)

    def add_expense():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительным числом")

            category = category_var.get()
            if not category:
                raise ValueError("Выберите категорию")

            date_str = date_entry.get()
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            expenses.append({
                "amount": amount,
                "category": category,
                "date": date_str
            })

            update_table()
            save_data()

            amount_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
            category_combo.set("")

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")

    tk.Button(root, text="Добавить расход", command=add_expense).grid(
        row=3, column=0, columnspan=2, pady=10
    )

    tree = ttk.Treeview(
        root,
        columns=("Amount", "Category", "Date"),
        show="headings"
    )
    tree.heading("Amount", text="Сумма")
    tree.heading("Category", text="Категория")
    tree.heading("Date", text="Дата")
    tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def update_table():
        for item in tree.get_children():
            tree.delete(item)
        for expense in expenses:
            tree.insert("", "end", values=(expense["amount"], expense["category"], expense["date"]))

    def save_data():
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(expenses, f, ensure_ascii=False, indent=4)

    tk.Label(root, text="Начало периода (ГГГГ-ММ-ДД):").grid(row=5, column=0, padx=5, pady=5)
    start_date_entry = tk.Entry(root)
    start_date_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(root, text="Конец периода (ГГГГ-ММ-ДД):").grid(row=6, column=0, padx=5, pady=5)
    end_date_entry = tk.Entry(root)
    end_date_entry.grid(row=6, column=1, padx=5, pady=5)

    sum_label = tk.Label(root, text="Сумма за период: 0")
    sum_label.grid(row=8, column=0, columnspan=2, pady=5)

    def calculate_period_sum():
        try:
            start_date = datetime.strptime(start_date_entry.get(), "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_entry.get(), "%Y-%m-%d").date()

            total = sum(
                expense["amount"] for expense in expenses
                if start_date <= datetime.strptime(expense["date"], "%Y-%m-%d").date() <= end_date
            )
            sum_label.config(text=f"Сумма за период: {total}")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты")

    tk.Button(root, text="Подсчитать сумму за период", command=calculate_period_sum).grid(
        row=7, column=0, columnspan=2, pady=10
    )

    tk.Label(root, text="Фильтр по категории:").grid(row=9, column=0, padx=5, pady=5)
    filter_category_var = tk.StringVar()
    filter_combo = ttk.Combobox(
        root,
        textvariable=filter_category_var,
        values=["Все", "Еда", "Транспорт", "Развлечения", "Жильё", "Другое"]
    )
    filter_combo.set("Все")
    filter_combo.grid(row=9, column=1, padx=5, pady=5)

    def apply_filter():
        selected_category = filter_category_var.get()

        for item in tree.get_children():
            tree.delete(item)

        filtered_expenses = expenses
        if selected_category != "Все":
            filtered_expenses = [
                exp for exp in expenses if exp["category"] == selected_category
            ]

        for expense in filtered_expenses:
            tree.insert("", "end", values=(expense["amount"], expense["category"], expense["date"]))

    tk.Button(root, text="Применить фильтр", command=apply_filter).grid(
        row=10, column=0, columnspan=2, pady=10
    )

    update_table()

    root.mainloop()


create_expense_tracker()
