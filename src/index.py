from tkinter import Tk
from ui import CalcUI

def main():
    """
    Main function to start the scientific calculator user interface. Creates a Tkinter window,
    sets the title, initializes the CalcUI class, and starts the main loop.
    """
    window = Tk()
    window.title("SciCalc")
    ui = CalcUI(window)
    ui.start()
    window.mainloop()

if __name__ == "__main__":
    main()
