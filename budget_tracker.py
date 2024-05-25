import tkinter as tk
from tkinter import messagebox, ttk
import os


def save_transactions(transactions, filename='transactions.txt'):
    os.makedirs('budget', exist_ok=True)
    with open(os.path.join('budget', filename), 'w') as file:
        for transaction in transactions:
            file.write(f"{transaction['type']}|{transaction['category']}|{transaction['amount']}\n")

def load_transactions(filename='transactions.txt'):
    transactions = []
    data_file_path = os.path.join('budget', filename)
    if os.path.exists(data_file_path):
        with open(data_file_path, 'r') as file:
            for line in file:
                type, category, amount = line.strip().split('|')
                transactions.append({'type': type, 'category': category, 'amount': float(amount)})
    return transactions

def add_transaction(type, category, amount):
    if category and amount:
        try:
            amount = float(amount)
            transactions.append({'type': type, 'category': category, 'amount': amount})
            update_transaction_list()
            update_budget_display()
            save_transactions(transactions)
            clear_entries()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid amount.")
    else:
        messagebox.showwarning("Warning", "Please fill out all fields correctly.")

def delete_transaction():
    try:
        selected_task_index = main_text.curselection()[0]
        transactions.pop(selected_task_index)
        update_transaction_list()
        update_budget_display()
        save_transactions(transactions)
    except IndexError:
        messagebox.showwarning("Warning", "No transaction selected to delete.")

def edit_transaction():
    try:
        selected_task_index = main_text.curselection()[0]
        transaction = transactions[selected_task_index]

        category_entry.delete(0, tk.END)
        category_entry.insert(0, transaction['category'])

        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, transaction['amount'])

        transaction_type_combobox.set(transaction['type'])

        transactions.pop(selected_task_index)
        update_transaction_list()
        update_budget_display()
    except IndexError:
        messagebox.showwarning("Warning", "No transaction selected to edit.")

def update_transaction_list():
    main_text.delete(0, tk.END)
    for transaction in transactions:
        display_text = f"{transaction['type'].capitalize()} | {transaction['category']} | ${transaction['amount']:.2f}"
        main_text.insert(tk.END, display_text)

def calculate_budget():
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    return total_income - total_expenses

def update_budget_display():
    budget = calculate_budget()
    budget_label.config(text=f"Remaining Budget: ${budget:.2f}")

def analyze_expenses():
    categories = {}
    for transaction in transactions:
        if transaction['type'] == 'expense':
            if transaction['category'] not in categories:
                categories[transaction['category']] = 0
            categories[transaction['category']] += transaction['amount']
    
    analysis = "\n".join([f"Category: {category}, Total Spent: ${total:.2f}" for category, total in categories.items()])
    messagebox.showinfo("Expense Analysis", analysis)

def clear_entries():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    transaction_type_combobox.set('')


window = tk.Tk()
window.title("Budget Tracker")
window.geometry('900x600')

icon_path = 'Budget_icon.ico'
if os.path.exists(icon_path):
    window.iconbitmap(icon_path)


transactions = load_transactions()


header_frame = tk.Frame(window, bg='lightgreen')
header_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

tk.Label(header_frame, text='Budget Tracker', font='Arial 25 bold', bg='lightgreen', fg='black').pack(fill=tk.BOTH)
tk.Label(window, text='Transaction Info', font='Arial 18 bold', bg='lightgreen', fg='black').grid(row=1, column=0, padx=10, pady=10, sticky='w')
tk.Label(window, text='Transactions List', font='Arial 18 bold', bg='lightgreen', fg='black').grid(row=1, column=1, padx=10, pady=10, sticky='w')

main_text = tk.Listbox(window, height=20, bd=5, width=40, font="Arial 12")
main_text.grid(row=2, column=1, rowspan=6, padx=10, pady=10, sticky='nsew')

form_frame = tk.Frame(window)
form_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

tk.Label(form_frame, text="Category", font="Arial 12 bold").grid(row=0, column=0, padx=10, pady=5, sticky='w')
category_entry = tk.Entry(form_frame, bd=5, width=30, font="Arial 12")
category_entry.grid(row=1, column=0, padx=10, pady=5, sticky='w')

tk.Label(form_frame, text="Amount", font="Arial 12 bold").grid(row=2, column=0, padx=10, pady=5, sticky='w')
amount_entry = tk.Entry(form_frame, bd=5, width=30, font="Arial 12")
amount_entry.grid(row=3, column=0, padx=10, pady=5, sticky='w')

tk.Label(form_frame, text="Type", font="Arial 12 bold").grid(row=4, column=0, padx=10, pady=5, sticky='w')
transaction_type_combobox = ttk.Combobox(form_frame, values=["Income", "Expense"], font="Arial 12")
transaction_type_combobox.grid(row=5, column=0, padx=10, pady=5, sticky='w')

button_frame = tk.Frame(window)
button_frame.grid(row=8, column=0, columnspan=2, pady=10)

tk.Button(button_frame, text="Add", font='Arial 15 bold', width=10, bg='lightgreen', fg='black', command=lambda: add_transaction(transaction_type_combobox.get().lower(), category_entry.get(), amount_entry.get())).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Delete", font='Arial 15 bold', width=10, bg='lightgreen', fg='black', command=delete_transaction).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Edit", font='Arial 15 bold', width=10, bg='lightgreen', fg='black', command=edit_transaction).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="Analyze Expenses", font='Arial 15 bold', width=20, bg='lightgreen', fg='black', command=analyze_expenses).grid(row=1, column=0, columnspan=3, pady=10)

budget_label = tk.Label(window, text="Remaining Budget: $0.00", font="Arial 15 bold", bg='lightgreen', fg='black')
budget_label.grid(row=9, columnspan=2, pady=10)


window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(1, weight=1)


update_transaction_list()
update_budget_display()

window.mainloop()