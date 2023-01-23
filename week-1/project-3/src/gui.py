import tkinter as tk
import re
from .calls_to_db import get_all_transactions
from .db_transactions import open_db
from tkinter import *
from datetime import datetime
from tkinter import ttk


class WindowBudget:

    # the next functions, to validate the amount and goal fields/values.
    def validate_amount(self, *values):
        if not re.fullmatch("[0-9]*", str(self.amount.get())):
            self.add_transaction_button["state"] = "disabled"
        else:
            self.add_transaction_button["state"] = "normal"

    def validate_budget(self, *values):
        if not re.fullmatch("[0-9]*", str(self.budget.get())):
            self.update_goal_button["state"] = "disabled"
        else:
            self.update_goal_button["state"] = "normal"

    def __init__(self, budget_win: object):
        # String values to hold the amount value, budget value, and the selected radio button
        # from the window
        self.amount = tk.StringVar()
        self.amount.trace_add("write", self.validate_amount)

        self.budget = tk.StringVar()
        self.budget.trace_add("write", self.validate_budget)

        self.radio_button_selector = StringVar(None, "income")

        # The labels which will appear on the view
        self.amount_label = Label(budget_win, text="Amount")  # Amount labels
        self.habits_label = Label(budget_win, text="Habits")  # Habits labels
        self.goal_budget_label = Label(budget_win, text="Goal Budget")  # Goal labels

        # The input fields: amount, habits, and goal on the view
        self.amount_text_field = Entry(textvariable=self.amount)  # Amount input field
        self.habits_text_field = Entry()  # input field habits
        self.goal_budget_text_field = Entry(textvariable=self.budget)  # see comments above

        # The add buttons on the view: add new transaction, and update goal budget.
        self.add_transaction_button = Button(
            budget_win, text="Add new transaction", command=self.add_new_transaction
        )
        self.update_goal_button = Button(
            budget_win, text="Update Goal Budget", command=self.update_goal_budget
        )

        # The radio buttons for income and outcome
        self.outcome_radio_button = Radiobutton(
            budget_win, text="outcome", variable=self.radio_button_selector, value="outcome"
        )
        self.income_radio_button = Radiobutton(
            budget_win,
            text="income",
            variable=self.radio_button_selector,
            value="income",
        )

        # The table to list all the transactions.
        self.all_transactions_table = ttk.Treeview(budget_win, selectmode="browse")
        self.all_transactions_table["columns"] = ("1", "2", "3", "4")
        self.all_transactions_table["show"] = "headings"

        # Assigning the width and anchor to the respective columns
        self.all_transactions_table.column("1", width=90, anchor="c")
        self.all_transactions_table.column("2", width=90, anchor="se")
        self.all_transactions_table.column("3", width=90, anchor="se")
        self.all_transactions_table.column("4", width=90, anchor="se")

        # Assigning the heading names to the respective columns
        self.all_transactions_table.heading("1", text="Date")
        self.all_transactions_table.heading("2", text="Amount")
        self.all_transactions_table.heading("3", text="Habit")
        self.all_transactions_table.heading("4", text="Operation")

        # The locations of the widget on the windows
        self.amount_label.place(x=282, y=180)
        self.amount_text_field.place(x=220, y=150)
        self.add_transaction_button.place(x=50, y=150)
        self.habits_label.place(x=520, y=180)
        self.habits_text_field.place(x=438, y=150)

        self.goal_budget_label.place(x=400, y=50)
        self.goal_budget_text_field.place(x=215, y=50)
        self.update_goal_button.place(x=50, y=50)

        self.outcome_radio_button.place(x=650, y=175)
        self.income_radio_button.place(x=650, y=150)
        self.all_transactions_table.place(x=50, y=250)

        self.render_all_transactions()

    def render_all_transactions(self):
        self.clear_all_transactions()
        for transactions in get_all_transactions():
            print(transactions)
            self.all_transactions_table.insert("", "end", text="L1", values=transactions)

    def clear_all_transactions(self):
        for item in self.all_transactions_table.get_children():
            self.all_transactions_table.delete(item)

    def add_new_transaction(self):
        timestamp = datetime.now().timestamp()
        amount = self.amount_text_field.get()
        if not amount:
            self.amount_text_field.focus_set()
            self.amount_text_field.configure(background="red")
            return
        self.amount_text_field.configure(
            background=self.goal_budget_text_field["background"]
        )  # not sure about it, I want to change the background to default
        habits = self.habits_text_field.get()
        if not habits:
            self.habits_text_field.focus_set()
            self.habits_text_field.configure(background="red")
            return
        self.habits_text_field.configure(
            background=self.goal_budget_text_field["background"]
        )  # not sure about it, I want to change the background to default

        type_of_operation = self.radio_button_selector.get()
        print(timestamp, amount, habits, type_of_operation)
        # todo: here we can save the transaction (DONE)
        with open_db() as db:
            db.insert_transaction(timestamp, amount, type_of_operation, habits)
        self.render_all_transactions()

    def update_goal_budget(self):
        total_budget = self.goal_budget_text_field.get()
        timestamp = datetime.now()
        print(total_budget, timestamp)
        # todo: here we can save the goal (DONE)
        with open_db() as db:
            db.insert_goal(timestamp, total_budget)
