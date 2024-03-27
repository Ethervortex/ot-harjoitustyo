from tkinter import Tk
from ui import CalcUI

def main():
    window = Tk()
    window.title("SciCalc")
    ui = CalcUI(window)
    ui.start()
    window.mainloop()

if __name__ == "__main__":
    main()
