import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime

window = tk.Tk()
window.title('To-Do List App')
window.geometry('750x500+300+150')

icon_path = 'Task_icon.ico'
if os.path.exists(icon_path):
    window.iconbitmap(icon_path)

def add_task():
    task_name = task_entry.get().strip()
    due_date = due_date_entry.get().strip()
    priority = priority_combobox.get().strip()
    status = status_combobox.get().strip()

    if task_name and priority in ["High", "Medium", "Low"] and status in ["Pending", "Completed"]:
        try:
            if due_date:
                datetime.strptime(due_date, '%Y-%m-%d')  
            task = f"{task_name} | {due_date} | {priority} | {status}\n"
            main_text.insert(tk.END, task)
            save_tasks()
            clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
    else:
        messagebox.showwarning("Warning", "Please fill out all fields correctly.")

def delete_task():
    try:
        selected_task_index = main_text.curselection()[0]
        main_text.delete(selected_task_index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected to delete.")

def edit_task():
    try:
        selected_task_index = main_text.curselection()[0]
        task_details = main_text.get(selected_task_index).split(' | ')

        task_entry.delete(0, tk.END)
        task_entry.insert(0, task_details[0])

        due_date_entry.delete(0, tk.END)
        due_date_entry.insert(0, task_details[1])

        priority_combobox.set(task_details[2])

        status_combobox.set(task_details[3])

        main_text.delete(selected_task_index)
    except IndexError:
        messagebox.showwarning("Warning", "No task selected to edit.")

def save_tasks():
    tasks = main_text.get(0, tk.END)
    os.makedirs('data', exist_ok=True)  
    with open(os.path.join('data', 'data.txt'), 'w') as file:
        file.writelines(tasks)

def load_tasks():
    data_file_path = os.path.join('data', 'data.txt')
    if not os.path.exists(data_file_path):
        return

    with open(data_file_path, 'r') as file:
        for line in file:
            main_text.insert(tk.END, line.strip())

def clear_entries():
    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    priority_combobox.set('')
    status_combobox.set('')


tk.Label(window, text='To-Do List', font='Arial 25 bold', bd=5, bg='lightblue', fg='black').pack(side='top', fill=tk.BOTH)
tk.Label(window, text='Add Task Info', font='Arial 18 bold', bd=5, bg='lightblue', fg='black').place(x=50, y=54)
tk.Label(window, text='Tasks List', font='Arial 18 bold', bd=5, bg='lightblue', fg='black').place(x=450, y=54)

main_text = tk.Listbox(window, height=9, bd=5, width=35, font="Arial 15 italic bold")
main_text.place(x=320, y=100)

tk.Label(window, text="Task Name", font="Arial 12 bold").place(x=20, y=120)
task_entry = tk.Entry(window, bd=5, width=30, font="Arial 10 bold")
task_entry.place(x=20, y=150)

tk.Label(window, text="Due Date (YYYY-MM-DD)", font="Arial 12 bold").place(x=20, y=190)
due_date_entry = tk.Entry(window, bd=5, width=30, font="Arial 10 bold")
due_date_entry.place(x=20, y=220)

tk.Label(window, text="Priority", font="Arial 12 bold").place(x=20, y=260)
priority_combobox = ttk.Combobox(window, values=["High", "Medium", "Low"], font="Arial 10 bold")
priority_combobox.place(x=20, y=290)

tk.Label(window, text="Status", font="Arial 12 bold").place(x=20, y=320)
status_combobox = ttk.Combobox(window, values=["Pending", "Completed"], font="Arial 10 bold")
status_combobox.place(x=20, y=350)

tk.Button(window, text="Add", font='Sarif 20 bold italic', width=10, bd=5, bg='lightblue', fg='black', command=add_task).place(x=90, y=410)
tk.Button(window, text="Delete", font='Sarif 20 bold italic', width=10, bd=5, bg='lightblue', fg='black', command=delete_task).place(x=290, y=410)
tk.Button(window, text="Edit", font='Sarif 20 bold italic', width=10, bd=5, bg='lightblue', fg='black', command=edit_task).place(x=490, y=410)


load_tasks()

window.mainloop()