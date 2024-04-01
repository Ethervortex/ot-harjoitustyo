from tkinter import ttk, constants

class SciCalcView:

    def __init__(self, root, controller):
        self._root = root
        self._controller = controller
        self._frame = None
        self._buttons = [
            'sin', 'cos', 'tan', '\u03c0', '(', ')', '\u00b1', '÷',
            'sin\u207B\u00B9', 'cos\u207B\u00B9', 'tan\u207B\u00B9', 'e', '7', '8', '9', '×',
            'x\u00b2', 'x\u02B8', '\u221ax', '\u00b3\u221ax', '4', '5', '6', '-',
            'log', 'ln', '10\u02E3', 'e\u02E3', '1', '2', '3', '+',
            'x!', 'nCr', 'mod', 'abs', '0', '.', '=', 
        ]
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._add_styles()
        self._add_widgets()
        self._arrange_widgets()

    def _add_styles(self):
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("MainFrame.TFrame", background='lightgrey')
        style.configure("Calc.TButton", font=('Montserrat', 15, 'bold'), background='lightgrey', padding=(5, 5))
        style.configure("Number.TButton", font=('Montserrat', 16, 'bold'), background='darkgrey')
        style.configure("BasicOperation.TButton", font=('Montserrat', 16, 'bold'), background='lightgreen')
        style.configure("Equal.TButton", font=('Montserrat', 16, 'bold'), background='#606060')

    def _add_widgets(self):
        self._frame = ttk.Frame(master=self._root, style="MainFrame.TFrame")
        self._entry_field = ttk.Entry(
            self._frame,
            textvariable=self._controller.equation,
            justify=constants.RIGHT,
            font=('Montserrat', 16)
        )
        self._add_buttons()

    def _add_buttons(self):
        self._buttons_widgets = []
        for button_text in self._buttons:
            button_style = (
                "Number.TButton" if button_text.isdigit() or button_text in ['.', '(', ')', '\u00b1']
                else "BasicOperation.TButton" if button_text in ['+', '-', '×', '÷']
                else "Equal.TButton" if button_text == '='
                else "Calc.TButton"
            )
            button = ttk.Button(
                self._frame,
                text=button_text,
                style=button_style,
                width=5,
                command=lambda text=button_text: self._controller.press(text)
            )
            self._buttons_widgets.append(button)

    def _arrange_widgets(self):
        self._entry_field.grid(row=0, column=0, columnspan=8, pady=10, ipady=15, sticky=constants.EW)
        self._arrange_buttons()

    def _arrange_buttons(self):
        row_num, col_num = 1, 0
        for button in self._buttons_widgets:
            button.grid(row=row_num, column=col_num, padx=5, pady=5, sticky=constants.NSEW)
            col_num += 1
            if button["text"] == '=':
                button.grid(columnspan=2)
                col_num += 1
            if col_num > 7:
                col_num = 0
                row_num += 1
