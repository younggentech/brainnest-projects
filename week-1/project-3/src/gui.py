

from tkinter import *


class WindowBudget:
    def __init__(self, budget_win:object):
        self.lbl1 = Label(budget_win, text="Amount")
        #self.lbl2 = Label(budget_win, text="Habits")
        self.txtfd1 = Entry()
        #self.txtfd2 = Entry()
        self.btn1 = Button(budget_win, text="Add new row")
        self.b1 = Button(budget_win, text="Add new row", command=self.test)
        self.lbl1.place(x=238, y=180)
        self.txtfd1.place(x=175, y=150)
        self.b1.place(x=50, y=150)

    def test(self):
        print("Hello")

