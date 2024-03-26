from tkinter import ttk, constants, StringVar, font

class SciCalcView:

    def __init__(self, root):
        self._root = root
        self._frame = None
        self._expression = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._expression = StringVar()
        entry_field = ttk.Entry(self._frame, textvariable=self._expression, justify=constants.RIGHT, font=('Helvetica', 14))
        entry_field.grid(row=0, column=0, columnspan=4, pady=10, ipady=15, sticky=constants.EW)

        buttons = [
            '7', '8', '9', '÷',
            '4', '5', '6', '×',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("Calc.TButton", font=('Helvetica', 16, 'bold'), background='lightgrey')
        style.map('Calc.TButton', background=[('active', 'white')])

        row_num, col_num = 1, 0
        for button_text in buttons:
            button = ttk.Button(self._frame, text=button_text, style="Calc.TButton", width=5)
            button.grid(row=row_num, column=col_num, padx=5, pady=5, sticky=constants.NSEW)
            col_num += 1
            if col_num > 3:
                col_num = 0
                row_num += 1
