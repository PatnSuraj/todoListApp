# tkinter for creating the app
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry # calendar widget
from datetime import datetime  # datetime module 

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        # empty list for tasks
        self.tasks = []

        self.task_entry = tk.Entry(root, width=40, font=('Arial', 12))
        self.task_entry.pack(pady=10)

        priority_frame = tk.Frame(root)
        priority_frame.pack(pady=5)
        self.priority_var = tk.StringVar()
        
        # task priorities
        priorities = ["High", "Medium", "Low"]
        self.priority_var.set(priorities[0])  # Default priority
        priority_label = tk.Label(priority_frame, text="Priority:")
        priority_label.pack(side=tk.LEFT)
        priority_dropdown = tk.OptionMenu(priority_frame, self.priority_var, *priorities)
        priority_dropdown.pack(side=tk.LEFT)

        # due dates frame
        due_date_frame = tk.Frame(root)
        due_date_frame.pack(pady=5)
        self.due_date_var = tk.StringVar()
        due_date_label = tk.Label(due_date_frame, text="Due Date:")
        due_date_label.pack(side=tk.LEFT)

        # calendar dates
        self.due_date_entry = DateEntry(due_date_frame, width=12, background='darkblue', foreground='white',
                                        borderwidth=2, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                                        mindate=datetime.now(), validate="focusout", validatecommand=(self.root.register(self.validate_date), '%P'))
        self.due_date_entry.pack(side=tk.LEFT)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # adding, removing, deleting and completing the tasks
        add_button = tk.Button(button_frame, text="Add Task", command=self.add_task, font=('Arial', 12), padx=10)
        add_button.pack(side=tk.LEFT)

        remove_button = tk.Button(button_frame, text="Remove Task", command=self.remove_task, font=('Arial', 12), padx=10)
        remove_button.pack(side=tk.LEFT)

        edit_button = tk.Button(button_frame, text="Edit Task", command=self.edit_task, font=('Arial', 12), padx=10)
        edit_button.pack(side=tk.LEFT)

        complete_button = tk.Button(button_frame, text="Mark as Completed", command=self.complete_task, font=('Arial', 12), padx=10)
        complete_button.pack(side=tk.LEFT)

        listbox_frame = tk.Frame(root)
        listbox_frame.pack()

        # format of the data
        self.tasks_listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, width=40, height=10, font=('Arial', 12))
        self.tasks_listbox.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.tasks_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_listbox.config(yscrollcommand=scrollbar.set)

        self.update_tasks_listbox()

    # data validation alerts for user to guide in the right path
    def validate_date(self, date_text):
        try:
            chosen_date = datetime.strptime(date_text, "%Y-%m-%d").date()
            current_date = datetime.now().date()
            if chosen_date < current_date:
                messagebox.showerror("Error", "Please select a date on or after the current date.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return False

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            completed = task.endswith("(Completed)")
            if completed:
                task = task[:-12]  # Remove "(Completed)"
            self.tasks_listbox.insert(tk.END, f"• {task}")

    # add task
    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        due_date = self.due_date_entry.get_date() if self.due_date_entry.get() else None

        if task:
            if due_date:
                task += f" (Due: {due_date.strftime('%Y-%m-%d')})"
            if priority:
                task += f" ({priority} Priority)"
            
            self.tasks.append(task)
            self.update_tasks_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    # remove task
    def remove_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    # edit task
    def edit_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            edited_task = simpledialog.askstring("Edit Task", "Edit Task:", initialvalue=self.tasks[selected_task_index[0]])
            if edited_task:
                self.tasks[selected_task_index[0]] = edited_task
                self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to edit.")

    # complete task
    def complete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            completed_task = self.tasks.pop(selected_task_index[0])
            completed_task = f"{completed_task} (Completed)"
            self.tasks.append(completed_task)
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as completed.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
