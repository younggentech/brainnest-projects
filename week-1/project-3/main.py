from tkinter import *
from src.gui import WindowBudget

def start_gui():
    window = Tk()
    budget_window = WindowBudget(window)
    window.title("Budget App - Life")
    window.geometry("800x600+10+10")
    window.mainloop()

def main():
    start_gui()


if __name__ == "__main__":
    main()



