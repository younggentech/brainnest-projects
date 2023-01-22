from tkinter import *
from datetime import datetime


class WindowBudget:
    def __init__(self, budget_win: object):
        self.lbl1 = Label(budget_win, text="Amount")
        self.lbl2 = Label(budget_win, text="Habits")
        self.lbl3 = Label(budget_win, text="Total Budget")
        self.txtfd1 = Entry()
        self.txtfd2 = Entry()
        self.txtfd3 = Entry()
        self.btn1 = Button(budget_win, text="Add new row")
        self.b1 = Button(budget_win, text="Add new row", command=self.add_row)

        self.btn3 = Button(budget_win, text="Update Total Budget")
        self.b3 = Button(budget_win, text="Update Total Budget",
                         command=self.total_budget)
        self.lbl1.place(x=238, y=180)
        self.txtfd1.place(x=175, y=150)
        self.b1.place(x=50, y=150)
        self.lbl2.place(x=438, y=180)
        self.txtfd2.place(x=375, y=150)

        self.lbl3.place(x=50, y=50)
        self.txtfd3.place(x=215, y=50)
        self.b3.place(x=50, y=50)

    def add_row(self):
        timestamp = datetime.now()
        amount = self.txtfd1.get()
        habits = self.txtfd2.get()
        print(timestamp, amount, habits)
        # todo: here we can save the row

    def total_budget(self):
        total_budget = self.txtfd3.get()
        print(total_budget)
