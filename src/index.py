from tkinter import Tk
from ui import calcUI

def main():
    window = Tk()
    window.title("SciCalc")
    ui = calcUI(window)
    ui.start()
    window.mainloop()

if __name__ == "__main__":
    main()
