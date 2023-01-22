from tkinter import *
from datetime import datetime


class WindowBudget:
    def __init__(self, budget_win: object):
        self.lbl_amount = Label(budget_win, text="Amount")  # Amount labels
        self.lbl_habits = Label(budget_win, text="Habits")  # Habits labels
        self.lbl_goalbudget = Label(budget_win, text="Goal Budget")  # Goal labels
        self.lbl_outcome = Label(budget_win, text="empty")
        self.lbl_income = Label(budget_win, text="empty")
        self.txt_fd_amount = Entry()  # Amount input field
        self.txt_fd_habits = Entry()  # input field habits
        self.txt_fd_goalbudget = Entry()  # see comments above
        self.btn1_trx = Button(budget_win, text="Add new transaction")
        self.b1_trx = Button(
            budget_win, text="Add new transaction", command=self.add_new_trx
        )

        self.radiobtn_selector = StringVar(None, "income")

        self.btn5_outcome = Radiobutton(
            budget_win, text="outcome", variable=self.radiobtn_selector, value="outcome"
        )
        self.btn7_income = Radiobutton(
            budget_win,
            text="income",
            command=self.radio_button,
            variable=self.radiobtn_selector,
            value="income",
        )

        self.btn3_goalbudget = Button(budget_win, text="Update Goal Budget")
        self.b3_goalbudget = Button(
            budget_win, text="Update Goal Budget", command=self.update_goal_budget
        )

        self.lbl_amount.place(x=282, y=180)
        self.txt_fd_amount.place(x=220, y=150)
        self.b1_trx.place(x=50, y=150)
        self.lbl_habits.place(x=520, y=180)
        self.txt_fd_habits.place(x=438, y=150)

        self.lbl_goalbudget.place(x=50, y=50)
        self.txt_fd_goalbudget.place(x=215, y=50)
        self.b3_goalbudget.place(x=50, y=50)

        self.btn5_outcome.place(x=650, y=175)
        self.btn7_income.place(x=650, y=150)

    def add_new_trx(self):
        timestamp = datetime.now().timestamp()
        amount = self.txt_fd_amount.get()
        if not amount:
            self.txt_fd_amount.focus_set()
            self.txt_fd_amount.configure(background="red")
            return
        self.txt_fd_amount.configure(
            background=self.txt_fd_goalbudget["background"]
        )  # not sure about it, i want to change the background to default
        habits = self.txt_fd_habits.get()
        if not habits:
            self.txt_fd_habits.focus_set()
            self.txt_fd_habits.configure(background="red")
            return
        self.txt_fd_habits.configure(
            background=self.txt_fd_goalbudget["background"]
        )  # not sure about it, i want to change the background to default

        type_of_operation = self.radiobtn_selector.get()
        print(timestamp, amount, habits, type_of_operation)
        # todo: here we can save the row

    def update_goal_budget(self):
        total_budget = self.txt_fd_goalbudget.get()
        timestamp = datetime.now()
        print(total_budget, timestamp)

    def radio_button(self):
        print(self.radiobtn_selector.get())
        # TODO: (Esteban) - initial set values is not gathered
        #   Method returns None or income.
