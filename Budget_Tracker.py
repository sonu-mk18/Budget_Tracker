import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Create a DataFrame to store the expenses
expense_data = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Budget Tracker with Expense Categorization")

        # Setup Income Entry
        self.income_label = tk.Label(root, text="Enter Monthly Income: ")
        self.income_label.grid(row=0, column=0)

        self.income_entry = tk.Entry(root)
        self.income_entry.grid(row=0, column=1)

        # Setup Expense Entry
        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD): ")
        self.date_label.grid(row=1, column=0)

        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=1, column=1)

        self.category_label = tk.Label(root, text="Expense Category: ")
        self.category_label.grid(row=2, column=0)

        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=2, column=1)

        self.amount_label = tk.Label(root, text="Amount: ")
        self.amount_label.grid(row=3, column=0)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=3, column=1)

        self.notes_label = tk.Label(root, text="Notes (optional): ")
        self.notes_label.grid(row=4, column=0)

        self.notes_entry = tk.Entry(root)
        self.notes_entry.grid(row=4, column=1)

        # Buttons
        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=5, column=0, columnspan=2)

        self.show_summary_button = tk.Button(root, text="Show Summary", command=self.show_summary)
        self.show_summary_button.grid(row=6, column=0, columnspan=2)

        self.show_graph_button = tk.Button(root, text="Show Graph", command=self.show_graph)
        self.show_graph_button.grid(row=7, column=0, columnspan=2)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        notes = self.notes_entry.get()

        if not date or not category or not amount:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        global expense_data
        new_expense = pd.DataFrame([{"Date": date, "Category": category, "Amount": amount, "Notes": notes}])
        expense_data = pd.concat([expense_data, new_expense], ignore_index=True)

        # Clear the input fields
        self.date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Expense Added Successfully!")

    def show_summary(self):
        # Calculate Total Income, Total Expenses, and Savings
        try:
            income = float(self.income_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid income amount.")
            return

        total_expenses = expense_data["Amount"].sum()
        savings = income - total_expenses

        summary = f"Total Income: ${income}\n"
        summary += f"Total Expenses: ${total_expenses}\n"
        summary += f"Savings: ${savings}\n"

        # Show Expense Breakdown by Category
        category_expenses = expense_data.groupby("Category")["Amount"].sum()
        summary += "\nExpenses by Category:\n"
        for category, amount in category_expenses.items():
            summary += f"{category}: ${amount}\n"

        messagebox.showinfo("Summary", summary)

    def show_graph(self):
        # Create a pie chart for the categorized expenses
        if expense_data.empty:
            messagebox.showerror("Error", "No expenses to show.")
            return

        category_expenses = expense_data.groupby("Category")["Amount"].sum()

        plt.figure(figsize=(8, 6))
        category_expenses.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title("Expenses by Category")
        plt.ylabel('')  # Hide the y-label to clean up the chart
        plt.show()


# Initialize the app
root = tk.Tk()
app = BudgetTrackerApp(root)
root.mainloop()