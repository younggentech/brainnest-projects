from tkinter import *
from src.gui import WindowBudget


def start_gui():
    # TODO (Abdullah):
    #  link the events (DONE)
    #  validate the front-end (DONE)
    #  validate the back-end (DONE)
    #  add charts
    #  list of transactions (DONE)
    # TODO (NOT DONE)
    window = Tk()
    WindowBudget(window)
    window.title("Budget App - Life")
    window.geometry("800x600+10+10")
    window.mainloop()


#     one table: id, amount, reason
#       on the ui, we have a radio buttons, if income radio is select, the amount will be +
#       on the ui, we have a radio buttons, if outcome radio is select, the amount will be -


def main():
    start_gui()


if __name__ == "__main__":
    main()
